"""Part 4: Sharing (SG-17), Nano Server (SG-18, SG-19), NTFS permissions (SG-20, SG-21)."""


def part4(s):
    s.part("PART 4 — FILE SHARING, NANO SERVER AND NTFS PERMISSIONS (SG-17 to SG-21)")
    s.src("Share Permission handout (dnsstuff + Lepide articles); Share Permission lab diagram (Faculty/Students, Svr1/Svr6/Client1); share-permission lab video; Server Storage slides (SMB/NFS, share profiles, SMB cmdlets); Module 2A slides (Nano Server mentions); AD DS Issues slides (djoin).")

    # ---------------- SG-17 ----------------
    s.h2("SG-17  How to share a folder (Windows Server 2016 / 2019 / 2022)")
    s.h3("Method 1: Server Manager → File and Storage Services (lab method)")
    s.steps([
        "Server Manager → **File and Storage Services** → **Shares** → TASKS → **New Share…** (the File Server role service must be installed).",
        "Choose a **profile**: **SMB Share – Quick** (basic Windows share), **SMB Share – Advanced** (adds folder owners and *access-denied assistance*, data classification and **quotas**; needs FSRM), **SMB Share – Applications** (settings for Hyper-V or SQL over SMB), **NFS Share – Quick / Advanced** (for **Linux/UNIX** clients).",
        "Pick the server and a volume or custom path (lab: `D:\\Shares\\Faculty` on **CA-VAN-SVR6**), then the share name (the UNC path shows as `\\\\ca-van-svr6\\Faculty`).",
        "Other settings: **Enable access-based enumeration (ABE)**, allow caching (offline files), **encrypt data access** (SMB 3 encryption), continuous availability (clusters).",
        "**Specify permissions** → Customize permissions → **Disable inheritance** → *Remove all inherited permissions* → add the right groups (see SG-21) → set the **Share** tab permissions → Create.",
    ])
    s.h3("Other methods")
    s.table(["Method", "How"], [
        ["File Explorer: Advanced Sharing", "Right-click folder → Properties → **Sharing** → **Advanced Sharing** → tick *Share this folder* → share name, *Limit the number of simultaneous users*, **Permissions** (share) → OK. Then use the **Security** tab for NTFS."],
        ["File Explorer: simple sharing", "Right-click → Give access to / Share… (the wizard sets share Full Control for Everyone + NTFS for the chosen users)."],
        ["Computer Management", "`compmgmt.msc` (or `fsmgmt.msc`) → System Tools → **Shared Folders** → Shares → New Share. Also shows Sessions and Open Files."],
        ["PowerShell", "`New-SmbShare -Name Faculty -Path D:\\Shares\\Faculty -ChangeAccess \"ADATUM\\Faculty\" -FullAccess \"ADATUM\\Domain Admins\" -FolderEnumerationMode AccessBased`"],
        ["Command prompt", "`net share Faculty=D:\\Shares\\Faculty /GRANT:ADATUM\\Faculty,CHANGE`  ·  `net share` (list)  ·  `net share Faculty /delete`"],
    ], widths=(2.0, 5.5))
    s.code("""Get-SmbShare ; Get-SmbShareAccess -Name Faculty
Grant-SmbShareAccess -Name Faculty -AccountName ADATUM\\Students -AccessRight Read -Force
Revoke-SmbShareAccess / Block-SmbShareAccess (explicit deny)
Set-SmbShare -Name Faculty -FolderEnumerationMode AccessBased -EncryptData $true
Remove-SmbShare -Name Faculty
Get-SmbSession ; Get-SmbOpenFile ; Close-SmbOpenFile        # who is connected / what's open
Set-SmbBandwidthLimit -Category VirtualMachine -BytesPerSecond 100MB   (needs FS-SMBBW feature)
New-PSDrive -Name F -PSProvider FileSystem -Root \\\\ca-van-svr6\\Faculty -Persist ;  net use F: \\\\ca-van-svr6\\Faculty""",
           title="SMB share cmdlets (Server Storage slides)")
    s.bullets([
        "**Hidden shares** end in `$` (e.g. `Payroll$`). Admin shares are created automatically: `C$`, `ADMIN$`, `IPC$`, and on DCs `SYSVOL` and `NETLOGON`.",
        "**SMB uses TCP 445** (legacy NetBIOS over TCP/IP uses 137–139). **NFS uses TCP/UDP 2049** (NFS 4.1 supports Kerberos v5 authentication).",
    ])
    s.table(["SMB version", "Introduced with", "Notes"], [
        ["SMB 1.0 / CIFS", "Windows 2000 / XP / 2003", "**Insecure; disable it** (WannaCry). Not installed by default since 2016 1709 / 2019."],
        ["SMB 2.0 / 2.1", "Vista / 2008 ; 7 / 2008 R2", "Fewer commands, larger reads and writes, leases"],
        ["SMB 3.0", "Windows 8 / Server 2012", "**SMB encryption**, Transparent Failover, **SMB Direct (RDMA)**, Multichannel, Scale-Out File Server"],
        ["SMB 3.0.2", "8.1 / 2012 R2", "Improved SMB Direct, SMB1 removable"],
        ["SMB 3.1.1", "Windows 10 / 2016, 2019, 2022", "Pre-authentication integrity (SHA-512), AES-128-GCM; **2022: AES-256, SMB compression, SMB over QUIC (Azure Edition)**"],
    ], widths=(1.4, 2.0, 4.1))
    s.box("instructor", [
        "**Access-based enumeration:** \"Users only see the folders they have permission to. Students don't see each other's folders, so there are fewer help-desk calls.\" Turn it on in the share settings, or with `Set-SmbShare -FolderEnumerationMode AccessBased`.",
        "Lab topology: **CA-VAN-SVR1** 192.168.239.1/24 (AD DS + DNS, DNS 127.0.0.1) · **CA-VAN-SVR6** 192.168.239.6/24 (file server, DNS → .1) · **CA-VAN-CLIENT1** 192.168.239.20/24 (DNS → .1). Faculty user **F1**; student users **S1**, **S2**.",
    ])

    # ---------------- SG-18 ----------------
    s.h2("SG-18  Nano Server: what, benefits, services, djoin, scenarios")
    s.tag("supp", "The course slides only mention Nano Server in passing: \"headless configuration\", \"Group Policy not supported on Nano Server\", \"Nano Server (DHCP x)\", \"Linux Containers on Windows (Nano image)\", and DNS on Nano.")
    s.p("**Nano Server** (introduced in Windows Server 2016) is a stripped-down, **headless**, 64-bit-only install option with **no GUI, no local logon and no Remote Desktop**. It's even smaller than Server Core and is managed **only remotely**. Since version 1709, Microsoft supports Nano Server **only as a container base image** (`mcr.microsoft.com/windows/nanoserver`), so new infrastructure roles should use Server Core. The exam asks about the original 2016 design.")
    s.table(["Benefit", "Detail"], [
        ["Tiny footprint", "VHD about 400–500 MB (roughly 93% smaller than Desktop Experience); boots in seconds; uses very little RAM."],
        ["Fewer patches and reboots", "Microsoft quoted about 92% fewer critical bulletins and 80% fewer reboots."],
        ["Smaller attack surface", "Fewer services and ports, no GUI or browser, 64-bit apps only."],
        ["Density", "More VMs or containers per host; ideal for cloud fabric."],
    ], widths=(1.8, 5.7))
    s.table(["Supported (add as packages)", "Not supported"], [
        ["**Hyper-V** host (`-Compute`)\n**Failover Clustering** (`-Clustering`)\n**File Server / Storage**, Scale-Out File Server (`-Storage`)\n**DNS Server** (`Microsoft-NanoServer-DNS-Package`)\n**IIS** web server (`Microsoft-NanoServer-IIS-Package`)\nWindows / Hyper-V **containers** (`-Containers`)\nWindows Defender (`-Defender`), DSC, Shielded VM, Secure Startup, SCVMM agent",
         "**AD DS** (can't be a DC)\n**DHCP Server** (the slide's \"DHCP x\")\n**Group Policy** (use DSC or PowerShell instead)\nRemote Desktop Services, Print, Fax, WSUS\nFull .NET Framework (CoreCLR only), 32-bit (WOW64) apps\nLocal GUI tools, Server Manager *on the box*, RDP\nNIC Teaming LBFO (use Switch Embedded Teaming)"],
    ], widths=(3.75, 3.75), first_col_bold=False)
    s.h3("Management options")
    s.bullets([
        "**PowerShell remoting** (`Enter-PSSession`, `Invoke-Command`), **PowerShell Direct** from the Hyper-V host, **Windows Admin Center**, Server Manager or MMC **from another machine**, WMI/CIM, and DSC.",
        "**Nano Server Recovery Console:** a text console on the local screen for emergency network, firewall and WinRM settings.",
        "Because Nano isn't domain-joined at build time, add it to TrustedHosts first: `Set-Item WSMan:\\localhost\\Client\\TrustedHosts \"192.168.239.30\" -Force`.",
    ])
    s.h3("Offline domain join with djoin.exe")
    s.p("**Why:** Nano has no join dialog, and the image is usually built (or the machine deployed) while it **can't reach a DC**. Offline domain join pre-creates the computer account and packages the secret into a **blob file** that the target consumes later.")
    s.code("""REM 1) On a domain-joined machine (run as a user allowed to create computer accounts):
djoin.exe /provision /domain adatum.com /machine Nano1 /savefile C:\\odjblob
REM    -> creates CN=Nano1 in AD (Computers container, or /machineou "OU=Servers,DC=adatum,DC=com")

REM 2) Copy the blob to the Nano Server:
$s = New-PSSession -ComputerName 192.168.239.30 -Credential ~\\Administrator
Copy-Item C:\\odjblob -Destination C:\\ -ToSession $s

REM 3) On the Nano Server (remote session):
djoin /requestodj /loadfile C:\\odjblob /windowspath %windir% /localos
shutdown /r /t 5          (or Restart-Computer)""", title="Offline domain join (Nano Server)")
    s.table(["Scenario needing djoin", "Why"], [
        ["Nano Server", "No interactive join UI. Join through `djoin` or by injecting the blob with `New-NanoServerImage -DomainBlobPath`."],
        ["Mass deployment / imaging", "Join hundreds of VMs or VDI images without a DC connection at first boot (blob in `unattend.xml`)."],
        ["Branch office / isolated build network", "The machine is built where no DC is reachable, then shipped."],
        ["DirectAccess / remote clients", "`djoin /provision … /reuse /policynames` packages the DirectAccess GPO so the client can connect from the Internet."],
    ], widths=(2.3, 5.2))

    # ---------------- SG-19 ----------------
    s.h2("SG-19  How to create and deploy a Nano Server")
    s.tag("supp")
    s.steps([
        "Copy the **NanoServerImageGenerator** folder from the Windows Server **2016** media (`D:\\NanoServer\\NanoServerImageGenerator`) to `C:\\Nano`.",
        "`Import-Module C:\\Nano\\NanoServerImageGenerator -Verbose`",
        "Build the image with **New-NanoServerImage** (command below). `-DeploymentType Guest` makes a VM image; `Host` is for physical hardware (add `-OEMDrivers`). A `.vhdx` target is for a Gen 2 VM, `.vhd` for Gen 1, `.wim` for physical deployment through WDS.",
        "Create the VM from the VHDX: `New-VM -Name Nano1 -Generation 2 -MemoryStartupBytes 512MB -VHDPath C:\\Nano\\Nano1.vhdx -SwitchName External` then `Start-VM Nano1`.",
        "Log on to the **Recovery Console** to check the IP, or set it from the image options. Add it to TrustedHosts, then `Enter-PSSession -ComputerName 192.168.239.30 -Credential ~\\Administrator`.",
        "Domain-join it (djoin, above) and add roles later if needed: `Install-PackageProvider NanoServerPackage` → `Find-NanoServerPackage` → `Install-NanoServerPackage Microsoft-NanoServer-DNS-Package` → `Enable-WindowsOptionalFeature -Online -FeatureName DNS-Server-Full-Role`. Offline, use `Edit-NanoServerImage -Packages …`.",
        "Manage it from Server Manager or WAC on another server. The GUI alternative is the **Nano Server Image Builder** wizard.",
    ])
    s.code("""New-NanoServerImage -Edition Standard -DeploymentType Guest -MediaPath D:\\ `
  -BasePath C:\\Nano\\Base -TargetPath C:\\Nano\\Nano1.vhdx -ComputerName Nano1 `
  -AdministratorPassword (Read-Host -AsSecureString) `
  -Packages Microsoft-NanoServer-DNS-Package,Microsoft-NanoServer-IIS-Package -Storage -Compute `
  -DomainBlobPath C:\\odjblob `                  # or -DomainName adatum.com if the build host is joined
  -InterfaceNameOrIndex Ethernet -Ipv4Address 192.168.239.30 -Ipv4SubnetMask 255.255.255.0 `
  -Ipv4Gateway 192.168.239.254 -Ipv4Dns 192.168.239.1 -EnableRemoteManagementPort""", title="Build a Nano Server VHDX")
    s.box("trap", [
        "- Nano Server can run **DNS** (DNS lecture question: **yes**) and **IIS**, but **not DHCP** and **not AD DS**, and **Group Policy doesn't apply** to it.",
        "- In 2019/2022 Nano Server exists **only as a container image**. A question asking for the minimal install option for infrastructure roles on 2019/2022 wants **Server Core**.",
    ])

    # ---------------- SG-20 ----------------
    s.h2("SG-20  NTFS basic permissions compared (Full Control vs Modify, etc.)")
    s.p("NTFS permissions are stored in each file's or folder's **ACL** (made up of ACEs). They **apply to local and network access** and are set on the **Security** tab. Each can be **Allow** or **Deny**.")
    s.table(["Basic permission", "What the user can do", "Compared with the one above it"], [
        ["**Full Control**", "Everything in Modify **plus Change Permissions, Take Ownership and Delete Subfolders and Files** (even without delete rights on those files).", "—"],
        ["**Modify**", "Read, run, write, create **and delete** files and folders, and change attributes.", "Lacks **Change permissions** and **Take ownership** (the classic exam answer)."],
        ["**Read & Execute**", "Read everything **and run programs and scripts**; traverse folders.", "Modify adds write and **delete**."],
        ["**List Folder Contents**", "(Folders only) See names of files and subfolders and traverse. **Inherited by folders only, not files.**", "Like Read & Execute, but it doesn't apply to files."],
        ["**Read**", "View files, their contents, attributes and permissions.", "Read & Execute adds running programs."],
        ["**Write**", "Create files and folders, write data and attributes. **No delete, and no reading** unless Read is also granted.", "Modify = Read & Execute + Write + **Delete**."],
        ["**Special permissions**", "A custom mix of the 13 advanced permissions (Advanced button).", ""],
    ], widths=(1.5, 3.6, 2.4))
    s.table(["Advanced (special) permission", "FC", "M", "R&X", "LFC", "R", "W"], [
        ["Traverse folder / execute file", "✔", "✔", "✔", "✔", "", ""],
        ["List folder / read data", "✔", "✔", "✔", "✔", "✔", ""],
        ["Read attributes / extended attributes", "✔", "✔", "✔", "✔", "✔", ""],
        ["Create files / write data", "✔", "✔", "", "", "", "✔"],
        ["Create folders / append data", "✔", "✔", "", "", "", "✔"],
        ["Write attributes / extended attributes", "✔", "✔", "", "", "", "✔"],
        ["**Delete subfolders and files**", "✔", "", "", "", "", ""],
        ["Delete", "✔", "✔", "", "", "", ""],
        ["Read permissions", "✔", "✔", "✔", "✔", "✔", "✔"],
        ["**Change permissions**", "✔", "", "", "", "", ""],
        ["**Take ownership**", "✔", "", "", "", "", ""],
    ], widths=(3.0, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75), size=8)
    s.tag("extra", "The advanced-permission matrix is standard Microsoft documentation; the handout lists only the basic five.")
    s.h3("Share permissions (network only)")
    s.table(["Share permission", "Allows"], [
        ["**Read**", "View file and folder names and data, run programs. **Default: Everyone = Read** (since Server 2003)."],
        ["**Change**", "Read + create, modify and **delete** files and folders. (\"Never assigned by default\", per the handout.)"],
        ["**Full Control**", "Change + **change share permissions** (and take ownership over the share). Administrators have it by default."],
    ], widths=(1.5, 6.0))
    s.table(["", "Share permissions", "NTFS permissions"], [
        ["Applies to", "**Network access only** (through the share)", "**Local and network** access"],
        ["Granularity", "Whole share (all subfolders and files)", "Per file or folder, with inheritance"],
        ["File systems", "NTFS, ReFS, FAT, FAT32", "NTFS (and ReFS)"],
        ["Levels", "Read / Change / Full Control", "Full Control / Modify / Read & Execute / List Folder Contents / Read / Write + special"],
        ["Extra", "Can **limit concurrent connections**", "Auditing (SACL), ownership, inheritance, EFS"],
    ], widths=(1.3, 3.0, 3.2))
    s.box("trap", [
        "- **Effective access over the network = the MOST RESTRICTIVE of (combined share) and (combined NTFS).** Share Full Control + NTFS Read = **Read**. Share Read + NTFS Modify = **Read**. Locally, only NTFS counts.",
        "- **Within one set, permissions are cumulative** (the union of all the user's groups), and **Deny wins over Allow** at the same level. Precedence: **explicit Deny > explicit Allow > inherited Deny > inherited Allow**, so an explicit Allow beats an inherited Deny.",
        "- The handout sentence \"NTFS permissions only apply to users who are locally logged on\" is **wrong**. NTFS applies locally **and** over the network; it's *share* permissions that apply only over the network (the second article in the handout gets it right).",
    ])
    s.table(["Worked example", "Effective result"], [
        ["Bob is in Sales (NTFS Modify) and Interns (NTFS Read). Share: Everyone Full Control.", "**Modify** (NTFS is cumulative; the share isn't limiting)"],
        ["Same, but the share is Everyone **Read**", "**Read** (the most restrictive of share and NTFS)"],
        ["Sales has NTFS Modify; Interns has NTFS **Deny Write**; Bob is in both", "Read and execute plus delete, but **no write** (Deny overrides)"],
        ["Bob logs on **locally** at the server; share = Read; NTFS = Modify", "**Modify** (share permissions don't apply locally)"],
        ["Folder inherits Deny Read from its parent, but has an explicit Allow Read for Bob", "**Bob can read** (explicit Allow beats inherited Deny)"],
    ], widths=(4.8, 2.7))
    s.table(["Copy / move a file", "Permissions afterwards"], [
        ["**Copy** (any volume)", "Inherits the permissions of the **destination** folder; the copier becomes the owner"],
        ["**Move within the same NTFS volume**", "**Keeps** its original permissions (only the pointer moves)"],
        ["**Move to a different volume**", "Inherits the **destination** permissions (it's really a copy + delete)"],
    ], widths=(2.6, 4.9))
    s.tag("extra", "Copy and move rules, and the Deny precedence detail.")

    # ---------------- SG-21 ----------------
    s.h2("SG-21  Assigning appropriate permissions (lab walkthrough + best practice)")
    s.h3("Share-permission lab (Faculty / Students on CA-VAN-SVR6)")
    s.steps([
        "In ADUC create **domain local** groups **Faculty** (member F1) and **Students** (members S1, S2), following IGDLA.",
        "On Svr6, create `D:\\Shares\\Faculty` and `D:\\Shares\\Assignment` with subfolders `Student1` and `Student2`.",
        "New Share (SMB Quick) → **Enable access-based enumeration**.",
        "Customize permissions → **Disable inheritance** → *Remove all inherited permissions from this object* (otherwise **D:\\'s default Users: Read & Execute entry would let every domain user in**).",
        "NTFS: **Domain Admins = Full Control**, **Faculty = Modify** on both folders, **Students = Read** on Assignment (or *This folder only*), **S1 = Modify on Student1 only**, **S2 = Modify on Student2 only**. The instructor also removed the local *Administrators* group.",
        "Share tab: Faculty and Students = **Change** (NTFS does the fine-grained control), Domain Admins = Full Control.",
        "Test from Client1: log on as S1 → `\\\\ca-van-svr6\\Assignment`. S1 sees only *Student1* (thanks to ABE) and can save files there; S2's folder is invisible. F1 sees and edits everything.",
    ])
    s.qa([
        ["Why remove inherited permissions?", "Inherited entries from the volume root (Users: Read & Execute / Create folders; CREATOR OWNER) would give all domain users access. Start clean, then add only the required groups."],
        ["Why grant share Change but NTFS Modify?", "The share permission is only the outer gate (it must allow at least what NTFS allows). NTFS applies to local and network access and can differ per subfolder. Many admins use share Everyone/Authenticated Users Full Control and control everything with NTFS."],
        ["Why Modify rather than Full Control for Faculty?", "Least privilege: Faculty must create, edit and delete, but shouldn't **change permissions or take ownership**. Only admins get Full Control."],
        ["Which share profile for Linux clients?", "**NFS Share – Quick** (Server for NFS role service)."],
        ["What does access-denied assistance (SMB Advanced) do?", "When access is denied, users see a custom message and can e-mail the folder owner for access (needs FSRM)."],
        ["How can a user check what access they actually have?", "Folder Properties → Security → Advanced → **Effective Access** tab → select the user → View effective access."],
    ])
    s.h3("Best practices (handout)")
    s.bullets([
        "**Assign permissions to groups, never to individual users** (IGDLA).",
        "**Least privilege:** give only what the job needs; remove temporary access afterwards; restrictive-then-relax beats permissive.",
        "**Be careful with Everyone** (it includes Guest). Prefer *Authenticated Users* or specific groups.",
        "**Don't overuse explicit Deny** on widely used shares; use it only to override something already granted.",
        "**Watch the Administrators group:** members have full access to all shares. Audit membership changes.",
        "**Group folders by security requirement** under one parent and share the parent, instead of sharing each subfolder.",
    ])
    s.code("""icacls D:\\Shares\\Faculty                                    # view the ACL
icacls D:\\Shares\\Faculty /inheritance:r                     # remove inheritance (r = remove inherited ACEs)
icacls D:\\Shares\\Faculty /grant "ADATUM\\Faculty:(OI)(CI)M"   # Modify, inherited by subfolders and files
icacls D:\\Shares\\Assignment\\Student1 /grant "ADATUM\\S1:(OI)(CI)M"
icacls D:\\Data /deny "ADATUM\\Interns:(W)"
takeown /f D:\\Data /r /d y                                   # take ownership
Get-Acl D:\\Shares\\Faculty | Format-List ; Set-Acl""", title="Command-line NTFS management")
    s.tag("extra", "icacls and Get-Acl syntax.")
