# OCR every frame of the silent Windows Server videos with the built-in Windows.Media.Ocr engine.
# Run with Windows PowerShell 5.1 (WinRT projection is unavailable in PowerShell 7).
param([string]$Root = (Split-Path $PSScriptRoot -Parent))

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics, ContentType = WindowsRuntime]

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$type) {
    $t = $asTaskGeneric.MakeGenericMethod($type).Invoke($null, @($op))
    $t.Wait(-1) | Out-Null
    $t.Result
}

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$outDir = Join-Path $Root "_wsa_extract\ocr"
New-Item -ItemType Directory -Force $outDir | Out-Null

$videos = @(
  "DHCP", "DHCP Failover", "DHCP Relay Agent (Challenge)", "DNS Lab", "Group Nesting",
  "How to Install the Second Domain Controller", "How to install and configure subdomain",
  "How to install and configure a domain tree controller",
  "How to fix your client lost the trust relationship witht your domain", "add another server to manage",
  "Remove Client from Domain", "Storage Pool and iSCSI Server", "Hyper-V",
  "PStools installation and comments for psgetsid", "Windows 2016 Server Core Installation and Configuration",
  "Windows Server 2022 Domain Controller Installation", "How to configure Second Domain SubDomain and Domain Tree",
  "Lenovo Server IMM", "Install Widnows Server 2022", "Virtualbox Configurations", "Virtualbox Clone Machine",
  "Windows 10 Installation", "Class Demo", "How to share permission", "How to Configure Vmware Network", "Lecture Video"
)

foreach ($v in $videos) {
    $frames = Get-ChildItem (Join-Path $Root "transcripts\$v\frames") -Filter *.jpg | Sort-Object Name
    $sb = New-Object System.Text.StringBuilder
    foreach ($f in $frames) {
        $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
        $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bmp = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $res = Await ($engine.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
        [void]$sb.AppendLine("===== $($f.BaseName)")
        foreach ($line in $res.Lines) { [void]$sb.AppendLine($line.Text) }
        $stream.Dispose()
    }
    $safe = ($v -replace '[^\w]+', '_')
    [IO.File]::WriteAllText((Join-Path $outDir "$safe.txt"), $sb.ToString())
    "{0,4} frames  {1}" -f $frames.Count, $v
}
