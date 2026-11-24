param(
    [string]$Docx = (Join-Path $PSScriptRoot "..\Windows_Server_Admin_Final_Cheat_Sheet.docx"),
    [switch]$Pdf
)
$Docx = (Resolve-Path $Docx).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $pages = $doc.ComputeStatistics(2)
    $doc.Save()
    if ($Pdf) {
        $pdfPath = [IO.Path]::ChangeExtension($Docx, ".preview.pdf")
        $doc.ExportAsFixedFormat($pdfPath, 17)
        "PDF: $pdfPath"
    }
    "Pages: $pages"
    $doc.Close()
} finally {
    $word.Quit()
}
