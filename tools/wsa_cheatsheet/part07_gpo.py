"""Part 7: Group Policy and security policies (SG-26 to SG-28)."""


def part7(s):
    s.part("PART 7 — GROUP POLICY AND SECURITY POLICIES (SG-26 to SG-28)")
    s.src("Week 11 Module 10 GPO lecture (GPO.pdf); Account Lockout Policy discussion handout; Restricting Group Policy with WMI Filtering; Group Policy WMI filters for Windows; Office Administrative Templates handout (Ali Tajran); Map a shared folder handout; Week 12 Lab 8 (desktop wallpaper GPO, optional folder redirection); GPO lab video; Office ADMX import video; map-a-shared-folder video.")

    # ---------------- SG-26 ----------------
    s.h2("SG-26  What is a GPO and why do we use it?")
    s.p("A **Group Policy Object (GPO)** is a named collection of settings (security policy, registry-based Administrative Templates, scripts, software installation, folder redirection, firewall rules, preferences) that AD applies **automatically** to the **users and computers** in the **site, domain or OU** it's **linked** to. It's how one admin configures and enforces thousands of machines consistently.")
    s.table(["GPO part", "Applies to / when", "Examples"], [
        ["**Computer Configuration**", "Computer objects, at **startup** and every refresh", "Password and lockout policy, audit, user rights, firewall, startup scripts, BitLocker, Windows Update"],
        ["**User Configuration**", "User objects, at **logon** and every refresh", "Desktop restrictions, drive maps, folder redirection, logon scripts, Control Panel lockdown"],
        ["**Policies** vs **Preferences**", "Policies are enforced and reverted when the GPO is removed (written under `HKLM\\SOFTWARE\\Policies` / `HKCU\\SOFTWARE\\Policies`). Preferences are defaults the user can change, they \"tattoo\" (persist), and they support item-level targeting.", "Policy: hide Control Panel. Preference: map drive `H:`, create a shortcut, deploy a printer or registry value"],
    ], widths=(1.8, 3.0, 2.7))
    s.p("The lecture definition: Group Policy is the mechanism for **controlling and deploying operating-system settings** to computers across the network. It gives centralized control of **user settings and computer settings**, can **deploy applications**, and controls the **user experience**. Settings apply at **computer startup and shutdown** and at **user logon and logoff**. You configure one or more GPOs, then **link** them to AD DS containers. Every object in that container receives the settings.", size=9)
    s.h3("Three types of GPO (lecture)")
    s.table(["Type", "Where", "What it is"], [
        ["**Local GPO**", "That computer only. Edit with **`gpedit.msc`**", "One machine. Not stored in AD and not replicated."],
        ["**Domain GPO**", "Active Directory. Create and link in **GPMC** (`gpmc.msc`); edit in **GPME** (Group Policy Management Editor)", "The GPOs you deploy to sites, domains and OUs."],
        ["**Starter GPO**", "GPMC → **Starter GPOs**", "A **template**: a pre-configured baseline of settings. Build new GPOs from it when several OUs need almost the same policy with small differences (the wallpaper lab says to do this for Start menu and taskbar restrictions that vary by OU)."],
    ], widths=(1.5, 2.6, 3.4))
    s.h3("Administrative Template states (lecture)")
    s.table(["State", "What it does to the registry"], [
        ["**Not Configured**", "Default for most settings. Processing this GPO **does not touch** the registry value, whatever it currently is."],
        ["**Enabled**", "The policy is **explicitly turned on**, whatever the previous state was."],
        ["**Disabled**", "The policy is **explicitly turned off**, whatever the previous state was."],
    ], widths=(1.8, 5.7))
    s.h3("What the lecture says you typically use GPOs for")
    s.bullets([
        "Apply **security settings** (including the firewall).",
        "Manage **desktop application** settings.",
        "Deploy application software. The slide contrasts **WDS** (image a machine) with **GPOs** (assign or publish software to machines that already exist).",
        "**Folder redirection** (the optional lab redirects Documents).",
        "Configure **network settings** (the drive-map handout maps shares with Group Policy Preferences).",
    ])
    s.h3("Why GPO instead of editing the registry (lecture table)")
    s.table(["", "Text config file / Registry (`regedit`)", "Group Policy"], [
        ["Keeping machines current", "Hard to keep up to date", "**Centralized**: one change hits every computer in scope"],
        ["Undoing a change", "Changes **cannot be rolled back**", "Policy settings are **removed or updated** on the next refresh when they no longer apply"],
    ], widths=(1.8, 2.6, 3.1))
    s.h3("Limitations of GPO (lecture)")
    s.bullets([
        "GPOs run **sequentially**. A long list makes **logon slow**.",
        "Flexibility is limited, and the triggers are limited: **startup, logon, or the background interval**. They do not fire on an arbitrary event.",
        "They are **difficult to maintain**.",
        "**No version control.** Changes to GPO settings are **not audited** by Group Policy itself.",
    ])
    s.h3("What 2016 / 2019 / 2022 added (lecture)")
    s.bullets([
        "You can import these policy types onto **Nano Server (2016)**: **registry settings (`.pol`)**, **security settings (`.inf`)**, and **audit settings (`.csv`)**.",
        "The administrative templates now include the **Windows 10 / 11** templates.",
    ])
    s.h3("Where a GPO lives")
    s.table(["Component", "Location", "Replicated by"], [
        ["**GPC** (Group Policy Container)", "AD: `CN={GUID},CN=Policies,CN=System,DC=adatum,DC=com` (version, status, links)", "AD replication"],
        ["**GPT** (Group Policy Template)", "**SYSVOL**: `\\\\adatum.com\\SYSVOL\\adatum.com\\Policies\\{GUID}\\` (`GPT.INI`, `Machine\\`, `User\\`, `Registry.pol`, scripts)", "**DFS-R** (FRS before 2008)"],
        ["Default GPOs", "**Default Domain Policy** (linked to the domain: **password, lockout and Kerberos policy**) and **Default Domain Controllers Policy** (linked to the *Domain Controllers* OU: **user rights, audit** for DCs)", ""],
        ["Local GPO", "`%SystemRoot%\\System32\\GroupPolicy` (edit with `gpedit.msc`; security part with `secpol.msc`)", "Not replicated"],
        ["Local policy cache", "`C:\\Windows\\System32\\GroupPolicy\\DataStore`", "Not replicated. The lecture asks why this folder exists: the client **caches** Group Policy here so settings still apply when the computer is **disconnected**, then refreshes when it reconnects if a background refresh was missed."],
        ["Administrative Templates", "**Local store** `C:\\Windows\\PolicyDefinitions` (`.admx` plus a language folder such as `en-US` for `.adml`). **Central Store** `\\\\adatum.com\\SYSVOL\\adatum.com\\Policies\\PolicyDefinitions`. The lecture calls these the local and nonlocal template locations. If the Central Store exists, GPMC loads templates from there.", "DFS-R (the Central Store only)"],
    ], widths=(1.9, 4.3, 1.3))
    s.h3("Processing order and precedence: LSDOU")
    s.code("""Local GPO  ->  Site GPOs  ->  Domain GPOs  ->  OU GPOs (parent OU -> child OU)
                (applied first)                       (applied LAST = WINS on conflict)""")
    s.table(["Mechanism", "Effect"], [
        ["**Last writer wins**", "The GPO closest to the object (the deepest OU) overrides conflicting settings from above. Non-conflicting settings combine."],
        ["**Link order**", "Several GPOs on one container: **link order 1 = highest precedence** (it's processed last)."],
        ["**Block Inheritance** (on a domain or OU)", "Stops GPOs from parent containers from applying, **except Enforced ones**."],
        ["**Enforced** (on a GPO link; formerly *No Override*)", "The GPO **can't be blocked** and **wins** over conflicting settings in lower GPOs."],
        ["**Security filtering**", "The GPO applies only to principals with **Read + Apply group policy** (default: *Authenticated Users*). Since MS16-072, computers also need Read (*Domain Computers*)."],
        ["**WMI filtering**", "Applies only if a WMI query is true. The lecture's example filter is named *Windows 10 or Windows Server 2016*: namespace `root\\CIMv2`, `Select * From Win32_OperatingSystem Where Version Like \"10.%\"`. WMI filters are **expensive** (they slow Group Policy processing)."],
        ["**Loopback processing** (Merge / Replace)", "Applies *User* settings based on the **computer's** OU (kiosks, RDS hosts, labs)."],
        ["**Link enabled / GPO status**", "Disable the link, or disable the unused Computer or User half, to speed up processing."],
    ], widths=(2.3, 5.2))
    s.box("trap", [
        "- **Domain account password, lockout and Kerberos policies come ONLY from GPOs linked at the DOMAIN level** (normally the Default Domain Policy). Linking a password policy to an OU changes only *local* SAM accounts of the computers in that OU. For different password rules per group, use **FGPP** (below).",
        "- GPOs can't be linked to the built-in **Users** or **Computers** containers, only to sites, domains and OUs.",
        "- Enforced beats Block Inheritance. If two Enforced GPOs conflict, the **higher** one in the hierarchy (closer to the domain) wins.",
    ])
    s.h3("Refresh and tools")
    s.bullets([
        "**Background refresh:** members and users every **90 minutes + a random 0–30 minutes**; **DCs every 5 minutes**. Also at startup and logon. Software installation and folder redirection apply **only at startup or logon**. Security settings are re-applied every 16 hours even if unchanged.",
        "`gpupdate /force` (re-apply everything; `/target:computer`, `/boot`, `/logoff`) · `Invoke-GPUpdate -Computer CA-VAN-CLIENT1 -Force` (remote).",
        "`gpresult /r` (summary of applied and **filtered** GPOs) · `gpresult /h C:\\report.html` · `rsop.msc` · GPMC **Group Policy Results** (what actually applied) and **Group Policy Modeling** (what-if).",
        "Consoles: `gpmc.msc` (create, link, back up, delegate), Group Policy Management Editor, `gpedit.msc` (local), `secpol.msc`.",
    ])
    s.code("""New-GPO -Name "Sec-Baseline" | New-GPLink -Target "OU=Servers,DC=adatum,DC=com" -LinkEnabled Yes
Set-GPLink -Name "Sec-Baseline" -Target "OU=Servers,DC=adatum,DC=com" -Enforced Yes -Order 1
Set-GPInheritance -Target "OU=Lab,DC=adatum,DC=com" -IsBlocked Yes
Set-GPRegistryValue -Name "Sec-Baseline" -Key "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\Terminal Services" -ValueName fDenyTSConnections -Type DWord -Value 0
Get-GPO -All | Select DisplayName, GpoStatus ; Get-GPOReport -All -ReportType Html -Path C:\\gpo.html
Backup-GPO -All -Path C:\\GPOBackup ; Restore-GPO -Name "Sec-Baseline" -Path C:\\GPOBackup
Get-GPResultantSetOfPolicy -ReportType Html -Path C:\\rsop.html -Computer CA-VAN-CLIENT1""", title="GroupPolicy PowerShell module")
    s.h3("WMI filters (lecture + the two handouts)")
    s.p("A WMI filter is one or more **WQL** queries. The client runs the query while processing the GPO; the GPO applies only if the computer matches. Use one when objects sit in a **flat OU** and you still need to target by OS, network, installed software, or hardware. Filters are stored in AD at `CN=SOM,CN=WMIPolicy,CN=System,<domain>` (class `msWMI-Som`; visible in ADSI Edit). Create them in GPMC → **WMI Filters** → New → namespace **`root\\CIMv2`** → Save, then on the GPO's **Scope** tab pick the filter. A filtered-out GPO shows in `gpresult /r` as **Filtering: Denied (WMI Filter)**.")
    s.table(["Target", "Query (root\\CIMv2)"], [
        ["Windows 10 client (lecture + handout)", "`Select * from Win32_OperatingSystem where Version like \"10.%\" and ProductType=\"1\"`"],
        ["Windows Server 2016-era server, not a client (lecture slide, filter name *Windows Server 2016*)", "`select * from Win32_OperatingSystem where Version like \"10%\" and ProductType > 1`"],
        ["Any Windows Server (handout: 2016 = version `10.%`)", "`select * from Win32_OperatingSystem WHERE Version LIKE \"10.%\" AND (ProductType = \"2\" or ProductType = \"3\")`"],
        ["Domain controller / server / desktop", "`ProductType=2` DC, `ProductType=3` server, `ProductType=1` desktop"],
        ["64-bit only", "`Select * from Win32_Processor where AddressWidth = \"64\"`"],
        ["Laptop (battery present)", "`SELECT * FROM Win32_Battery WHERE (BatteryStatus <> 0)`"],
        ["Mobile PC (`PCSystemType` 2 = mobile)", "`SELECT * FROM Win32_ComputerSystem WHERE PCSystemType = \"2\"`"],
        ["VMware VM", "`SELECT Model FROM Win32_ComputerSystem WHERE Model = \"VMWare Virtual Platform\"`"],
        ["Computer name prefix", "`SELECT Name FROM Win32_ComputerSystem WHERE Name LIKE 'lon-pc%'`"],
        ["At least 1 GB RAM", "`Select * from Win32_ComputerSystem where TotalPhysicalMemory >= 1073741824`"],
    ], widths=(3.2, 4.3), size=8)
    s.p("Version prefixes from the handout: **10.%** = Windows 10 / Server 2016, **6.3%** = 8.1 / 2012 R2, **6.2%** = 8 / 2012, **6.1%** = 7 / 2008 R2, **6.0%** = Vista / 2008, **5.2%** = 2003, **5.1%** = XP. Test a query on the target computer before you link it: `Get-WmiObject -Query 'Select * from Win32_OperatingSystem where Version like \"10.%\" and ProductType=\"1\"'`. Output means the computer matches; no output means the GPO will be denied. `Get-WmiObject Win32_OperatingSystem | Select Version, ProductType, OSArchitecture, BuildNumber` shows the values to filter on.", size=9)
    s.h3("Slow link and disconnected clients (lecture)")
    s.bullets([
        "**Slow link** default: a connection **below 500 Kbps**. Set it at **Computer Configuration → Policies → Administrative Templates → System → Group Policy → Configure Group Policy slow link detection**. Type **0** to turn slow-link detection off (every connection is treated as fast).",
        "On a slow link, only **Security Settings** and **Administrative Templates** apply by default. The lecture highlights **Configure registry policy processing** and **Configure security policy processing** as the extensions that still run. Folder redirection, software installation and drive maps do not.",
        "**Disconnected** computers use the cached policy in `GroupPolicy\\DataStore` and catch up on the next refresh after they rejoin the network.",
    ])
    s.h3("Delegating Group Policy (lecture)")
    s.p("These tasks are delegated separately: **creating** GPOs, **editing** GPOs, **managing links** for a site, domain or OU, running **Group Policy Modeling**, reading **Group Policy Results**, and **creating WMI filters**. Group Policy Results from another computer also needs inbound firewall rules for **WinRM** (the slide labels it WRM), **WMI**, and **Remote Service Management**.")
    s.box("instructor", [
        "Course use of GPOs (optional DNSSEC lab): **GPMC** → edit a GPO → **Computer Configuration\\Policies\\Windows Settings\\Name Resolution Policy** → create an **NRPT** rule (suffix `adatum.com`, *Enable DNSSEC* + *Require DNS clients to check that name and address data has been validated*) → Apply → on the client run `gpupdate /force` then `gpresult /r` to confirm the GPO applied (Part 9).",
    ])
    s.box("trouble", [
        "- **GPO not applying:** check that the link is enabled, the object is in the right OU (user settings follow the user, computer settings follow the computer), security or WMI filtering (shown as *Denied* in `gpresult /r`), Block Inheritance, client DNS pointing at a DC, and replication (GPMC → **Status** tab compares SYSVOL and AD versions).",
        "- **Events:** Event Viewer → Applications and Services Logs → Microsoft → Windows → **GroupPolicy → Operational**.",
        "- **User settings in a GPO linked to a computers-only OU** do nothing unless **loopback** is enabled.",
    ])
    s.h3("Week 12 discussion: model answers")
    s.tag("model")
    s.qa([
        ["What is GPO?", "A Group Policy Object: a container of settings stored in AD (GPC) and SYSVOL (GPT), linked to sites, domains and OUs, that centrally configures and enforces settings on users and computers."],
        ["Why do we need GPO? (Regedit vs GPO)", "**Regedit** = manual, one machine at a time, error-prone, no scoping, no reporting, changes persist forever. **GPO** = one change applies automatically to thousands of machines, scoped by OU, security group or WMI; it re-applies (users can't permanently undo it), policy settings are removed when out of scope, it can be backed up, reported (RSoP) and delegated, and it covers security settings, software, scripts and firewall, not just registry values."],
        ["What is ADMX?", "XML-based **Administrative Template** files (Vista/2008+, replacing `.adm`). The `.admx` file is language-neutral and defines each policy and the registry key it sets; the `.adml` file holds the language strings (`en-US\\`). Local store: `C:\\Windows\\PolicyDefinitions`. **Central Store**: create `\\\\adatum.com\\SYSVOL\\adatum.com\\Policies\\PolicyDefinitions` and copy the ADMX/ADML there so every admin edits with the same templates (e.g. the Microsoft Edge, Chrome or Office ADMX packs)."],
        ["What is Fine-Grained Password Policy (FGPP)?", "**Password Settings Objects (PSOs)** that give **different password and lockout rules to specific users or global groups** in one domain (e.g. 15-character passwords for admins). Requires **DFL 2008+**. Stored in `CN=Password Settings Container,CN=System`. **Lowest precedence number wins**; a PSO linked directly to a user beats group PSOs; with no PSO, the Default Domain Policy applies. PSOs can't be linked to OUs (use shadow groups). Created in **ADAC** or PowerShell."],
        ["What is SYSVOL?", "The System Volume: a folder on every DC (`C:\\Windows\\SYSVOL`) shared as **SYSVOL** and **NETLOGON**. It holds GPO templates, logon scripts and the ADMX Central Store, and it replicates to all DCs of the domain with **DFS-R**."],
    ], title=None)
    s.code("""New-ADFineGrainedPasswordPolicy -Name "PSO-Admins" -Precedence 10 -MinPasswordLength 15 `
  -ComplexityEnabled $true -PasswordHistoryCount 24 -MaxPasswordAge "30.00:00:00" -MinPasswordAge "1.00:00:00" `
  -LockoutThreshold 5 -LockoutDuration "00:30:00" -LockoutObservationWindow "00:30:00" -ReversibleEncryptionEnabled $false
Add-ADFineGrainedPasswordPolicySubject "PSO-Admins" -Subjects "Domain Admins"
Get-ADUserResultantPasswordPolicy -Identity admin1      # which PSO wins for this user""", title="FGPP")

    s.h2("Week 12 Lab 8 — create and link a GPO (desktop wallpaper)")
    s.p("Lab topology: domain controller **CA-VAN-SVR1** (`192.168.239.1`, Adatum.com). The lab video's client is **CA-VAN-C1**, Windows Server 2016 Standard, domain-joined, address from DHCP, signed in as **test1**. The handout also allows a Windows 10 or Windows 7/8 Pro or Enterprise client; a static IP means you do not need DHCP. Create OUs **Finance** and **Lab**, user **test1** in Finance and **test2** in Lab. The handout names the GPO **Set Desktop Wallpaper**. The lab video names it **Finance Desktop Wallpaper** and links it to the **Finance** OU only (Enforced **No**, Link Enabled **Yes**, security filtering **Authenticated Users**).")
    s.steps([
        "On the DC, Server Manager → **Tools → Group Policy Management**. Expand the forest and domain, then select **Group Policy Objects**. The two GPOs already there are **Default Domain Policy** and **Default Domain Controllers Policy**, created by the domain promotion, not by a user account you made.",
        "Right-click **Group Policy Objects → New**. Name it **Set Desktop Wallpaper**. Pick a **Source Starter GPO** only when you will stamp out several near-identical GPOs.",
        "Right-click the new GPO → **Edit**. A new GPO is an empty template until you define settings. Go to **User Configuration → Policies → Administrative Templates → Desktop → Desktop → Desktop Wallpaper**.",
        "On the DC, create **Dep_Wallpaper**, share it, and give **Everyone Read**. Put a **$** on the share name (**Dep_Wallpaper$**) to hide it. Confirm the client can open `\\\\CA-VAN-Svr1\\Dep_Wallpaper`.",
        "Set Desktop Wallpaper to **Enabled**. Wallpaper path is the **UNC** `\\\\CA-VAN-Svr1\\Dep_Wallpaper\\Finance.jpg` (a local path would point at the client, where the file is not). Style: Center, Tile, or Stretch. The user cannot change it. If the file is missing at logon, **no wallpaper is shown**.",
        "Right-click the **Finance** OU → **Link an Existing GPO** → Set Desktop Wallpaper. Link order on the lecture's GPMC screenshot: order **1** (Desktop Wallpaper) beats order **2**.",
        "Sign in on the client as **test1**. The wallpaper appears. Sign in as **test2**: it does **not**, because test2 is in the Lab OU and the GPO is linked only to Finance. User settings follow the **user's** OU.",
        "Link the same GPO to **Adatum.com** (the domain) and sign in as test2 again. The wallpaper **does** appear: a GPO linked to the domain applies to every user in the domain.",
        "Prove it: `gpupdate /force`, then `gpresult /r /scope:user`. The lab video uses the verbose form `gpresult /Scope user /v`. The handout's fix when nothing applies is **reboot the DC and the client** and **turn the client firewall off**.",
    ])
    s.box("trouble", [
        "The lab video's own checklist, once the wallpaper does not show: **(1) Permission?** The share is fine if Everyone has Read. **(2) Is the GPO applying?** `gpupdate /force` should report that both computer and user policy updated, and `gpresult` should list **Finance Desktop Wallpaper** under *Applied Group Policy Objects*. **(3) Is the GPO setting itself wrong?** If the GPO applied and the share is readable but the desktop did not change, the wallpaper UNC does not point at a file the client can open. The policy stores the path; it does not copy the jpg for you. The GPT itself is the folder under `\\\\CA-VAN-Svr1\\SYSVOL\\Adatum.com\\Policies\\{GUID}`.",
    ])
    s.qa([
        ["How do you delete an OU?", "In **Active Directory Users and Computers**, turn on **View → Advanced Features**, open the OU → **Object** tab, clear **Protect object from accidental deletion**, then right-click the OU → **Delete**. Or `Remove-ADOrganizationalUnit -Identity \"OU=Lab,DC=adatum,DC=com\" -Recursive -Confirm:$false` after clearing that flag (`Set-ADOrganizationalUnit -ProtectedFromAccidentalDeletion $false`)."],
        ["How many GPOs exist before you create one, and who created them?", "**Two**: Default Domain Policy and Default Domain Controllers Policy. They are created automatically when the domain is created."],
        ["What are the Default Domain Policy password settings? (lecture slide and the lab question)", "**History 24, maximum age 42 days, minimum age 1 day, length 7, complexity Enabled, reversible encryption Disabled.** Lockout threshold **0**. Kerberos: enforce user logon restrictions **Enabled**, service ticket **600 minutes**, user ticket **10 hours**."],
        ["Why can't test2 see the wallpaper, then why can they after the domain link?", "The GPO was linked only to **Finance**, and test2 is in **Lab**. User Configuration follows the user object. Linking the GPO to the **domain** puts every user, including test2, in scope."],
        ["What does the hidden share `$` do?", "`Dep_Wallpaper$` is a **hidden share**: it does not appear in Network browsing. Clients still open it by typing the UNC."],
        ["Optional lab: lock down a CIT student lab", "Link a GPO to the **Lab** OU. **User Configuration → Administrative Templates → Control Panel → Prohibit access to Control Panel and PC settings** (the lab screenshot is the \"this operation has been cancelled due to restrictions\" dialog). **User Configuration → Administrative Templates → System → Prevent access to registry editing tools**. Reuse **Desktop Wallpaper**. Block USB with **Administrative Templates → System → Removable Storage Access → All Removable Storage classes: Deny all access** (this one wins over the per-device settings; the lecture shows it there)."],
    ], title="Lab Questions & Answers (Week 12 wallpaper GPO)")

    s.h3("Optional challenge lab: folder redirection")
    s.p("The lab client must be a **desktop OS** (Windows 7, 8, 8.1 or 10 Pro or higher). It tells you not to use **Windows Server 2016 as the client**: folder redirection is demonstrated on a user desktop, and Server 2016 is the DC and file server in this lab. You need a DC, DHCP, and a domain-joined client; an OU **Finance** with users test1 and test2 and a group **Finance**.")
    s.steps([
        "On the DC create `C:\\Employee_Redir`. **File and Storage Services → Shares → Tasks → New Share → SMB Share – Quick** (Advanced adds quotas, classification and access-denied assistance). Share name **Employee_Redir$**. The **remote path** is the UNC clients use (`\\\\CA-VAN-Svr1\\Employee_Redir$`). The **local path** is the folder on the server's disk.",
        "Enable **access-based enumeration**. Then **Customize permissions**. **Administrators** (and SYSTEM) have Full Control because they own the folder and the default ACL grants it. To remove **ADATUM\\Users** you must first **disable inheritance**; otherwise the inherited ACE cannot be deleted. After inheritance is off, the ACEs that remain are **explicit** (set on this folder) rather than inherited.",
        "Add the **Finance** group. Show advanced permissions and allow **Create folders / append data**, or members cannot create folders inside the share. **Everyone** gets read and write by adding Everyone and ticking Read and Write (or Modify) on both the share permission and the NTFS ACL.",
        "New GPO **Finance_Folder_Redirection**, same create-and-link steps as the wallpaper lab. Edit → **User Configuration → Policies → Windows Settings → Folder Redirection**. Right-click **Documents → Properties**.",
        "**Basic** redirects everyone's folder to one location. **Advanced** uses a different location per group. **Not configured** does not redirect. Under Basic, the target can be the user's **home directory**, **a folder per user under a root path** (`\\\\CA-VAN-Svr1\\Employee_Redir$\\%username%\\Documents` — the usual choice; the system creates the folder and the ACL), **one folder for every user**, or **back to the local profile**.",
        "On the **Settings** tab: **Grant the user exclusive rights** (only that user can open their folder), **Move the contents** of Documents, and optionally apply the policy to Windows 2000/XP/2003. Policy removal is either **leave the folder in the new location** or **redirect it back to the local profile**.",
        "On the client run `gpupdate /force` and answer **Y** to log off. Documents then syncs. On the server, `Employee_Redir` contains a folder **named after the user**. A second account creates a second folder. The same account on a second domain-joined client sees the same documents.",
    ])
    s.qa([
        ["Why does an administrator get a warning opening that user's Documents on the server?", "**Grant the user exclusive rights** removes administrators from the ACL. The fix is to clear that checkbox before the policy applies, or afterwards take ownership of the folder and grant Domain Admins access."],
        ["When does folder redirection apply?", "At **logon** only, not on the 90-minute background refresh. That is why `gpupdate /force` has to log the user off."],
    ], title="Lab Questions & Answers (folder redirection)")

    s.h3("Map a shared folder to a drive letter (lecture handout)")
    s.p("Topology on the handout: **CA-VAN-Svr1** `192.168.239.1` (AD DS, DHCP, DNS), **CA-VAN-Svr6** `192.168.239.6` (file server), **CA-VAN-Client1**, all on subnet `255.255.255.0` through **Switch (NAT 9)**, gateway `192.168.239.254`, client DNS `192.168.239.1`. Faculty users **F1** and **F2** both map to the **Faculty** share (folders F1 and F2 inside it). Students **S1** and **S2** each map to their own folder in the Students share. **S3 is excluded** (the red X on the diagram): item-level targeting or security filtering keeps that user out. The lecture video builds this on **CA-VAN-SVR1** in an OU named **CIT**, with security groups **Faculty** and **Students** and users such as Lei Zhang, Lisa, Tim and Tom Lin added to those groups. The VMs in that recording are the file server, **DC1**, and the client.")
    s.steps([
        "Share the Faculty and Students folders on **CA-VAN-Svr6** (Part 4). Put the users in the Faculty and Students groups.",
        "GPMC → new GPO linked to the OU that holds the users → Edit → **User Configuration → Preferences → Windows Settings → Drive Maps**.",
        "New → **Mapped Drive**. Action **Create** (or **Update**). Location `\\\\CA-VAN-Svr6\\Faculty`, drive letter (for example **F:**), **Reconnect**. Label it Faculty.",
        "On the **Common** tab tick **Item-level targeting** → Targeting → New Item → **Security Group** → Faculty. Repeat for Students with `\\\\CA-VAN-Svr6\\Students` (or a per-user path `\\\\CA-VAN-Svr6\\Students\\%LogonUser%`) targeted at the Students group, and do not target S3.",
        "On the client, `gpupdate /force` and sign in again. Preferences apply at logon. Confirm with `gpresult /r /scope:user` and `net use`.",
    ])

    s.h3("Install Office Administrative Templates (Ali Tajran handout)")
    s.steps([
        "From the Microsoft Download Center, download **Administrative Template files (ADMX/ADML) and Office Customization Tool for Office 365 ProPlus, Office 2019, and Office 2016**. They are not installed by default. The ADMX/ADML files are the **same** in the 32-bit and 64-bit downloads (the bitness matters for the Office Customization Tool, not for the templates).",
        "Run the download as administrator, accept the license, and extract to a folder such as **Office ADMX**. You get an `admx` folder (and language folders) plus a spreadsheet of the settings.",
        "Copy the `.admx` files to the store. One DC and no Central Store: `C:\\Windows\\PolicyDefinitions` (the handout goes from 196 items to 208, **12** new files: access16, excel16, lync16, office16, onent16, outlk16, ppt16, proj16, pub16, teams16, visio16, word16). Copy the matching `.adml` files into `C:\\Windows\\PolicyDefinitions\\en-US`. Overwrite if the files are already there so you have the current Office and Microsoft 365 settings.",
        "Prefer the **Central Store** when you have more than one DC: `\\\\adatum.com\\SYSVOL\\adatum.com\\Policies\\PolicyDefinitions` (and `\\en-US`). Every admin then sees the same templates, and you do not copy them onto each DC.",
        "Verify: GPMC → edit the Default Domain Policy → **Computer Configuration → Policies → Administrative Templates** and the same path under **User Configuration**. Before the copy there is no Microsoft Office node. After it, Office, Word, Excel, Outlook and the rest appear.",
    ])

    # ---------------- SG-27 ----------------
    s.h2("SG-27  Security policies: default values to memorize")
    s.p("**Path:** Group Policy Management Editor → **Computer Configuration → Policies → Windows Settings → Security Settings** → *Account Policies* (Password, Account Lockout, Kerberos) · *Local Policies* (Audit Policy, **User Rights Assignment**, **Security Options**) · Event Log · Restricted Groups · System Services · Registry · File System · Windows Defender Firewall · Advanced Audit Policy Configuration. Locally: `secpol.msc`.")
    s.h3("Password Policy (Account Policies)")
    s.table(["Setting", "Default (Default Domain Policy)", "Stand-alone server default", "Notes"], [
        ["Enforce password history", "**24** passwords remembered", "0", "Range 0–24"],
        ["Maximum password age", "**42** days", "42 days", "0 = never expires; range 1–999"],
        ["Minimum password age", "**1** day", "0 days", "Stops users cycling through the history straight back to the old password"],
        ["Minimum password length", "**7** characters", "0", "Up to 14 (128 with *Relax minimum password length limits*)"],
        ["Password must meet complexity requirements", "**Enabled**", "Enabled", "3 of 4 character categories (upper, lower, digit, symbol), at least 6 characters, mustn't contain the account name"],
        ["Store passwords using reversible encryption", "**Disabled**", "Disabled", "Enable only for CHAP/Digest. It's effectively plaintext"],
    ], widths=(2.4, 1.8, 1.3, 2.0), size=8)
    s.box("instructor", "ADSI Edit on the domain head object (DC slide p32) shows the same defaults stored as attributes: **maxPwdAge = 42 days, minPwdAge = 1 day, minPwdLength = 7, pwdHistoryLength = 24, lockoutThreshold = 0, lockoutDuration / lockOutObservationWindow = 30 minutes, ms-DS-MachineAccountQuota = 10, msDS-Behavior-Version = 7 (2016)**.")
    s.h3("Account Lockout Policy")
    s.table(["Setting", "Default", "Notes"], [
        ["Account lockout threshold", "**0 invalid attempts = accounts never lock**", "A common hardened value is 5–10. (Windows 11 22H2+ clients now ship with a local default of 10.)"],
        ["Account lockout duration", "**Not defined** (it only becomes meaningful once the threshold > 0; Windows then suggests **30 minutes**)", "0 = locked until an admin unlocks it"],
        ["Reset account lockout counter after", "**Not defined** (suggested **30 minutes**)", "Must be ≤ lockout duration"],
    ], widths=(2.2, 3.0, 2.3))
    s.h3("Account lockout handout: think twice before a low threshold")
    s.p("The course reading argues that a threshold of **5 or 6** locks out real users. The counter is not a simple \"5 tries inside a window.\" Each bad password increments **`badPwdCount`**. The reset timer is the gap **between** failed attempts: another failure before *Reset account lockout counter after* elapses increments the count again, and hitting the threshold locks the account. Things that trip it without a person typing: an iPhone or iPad still using an **expired Exchange password**, a service or scheduled task with a **stale password**, several **RDS or Citrix** sessions (including disconnected ones) at the moment of a password change, a user signed in on several computers, and applications that cache AD credentials.")
    s.bullets([
        "The study guide wants the **default**, which is threshold **0** (never lock). The handout's suggested starting point, if you must lock accounts, is **threshold 50** (the maximum is **999**), **reset counter after 1 minute**, **duration 5 minutes**. A 30-minute duration is longer than you need to slow a brute-force attack, and a low threshold lets an attacker **deny service** by locking accounts on purpose.",
        "The handout would rather stop brute force at the **edge** (it uses a Citrix NetScaler example that locks the source IP, not the AD account) and rely on a strong password policy.",
        "List locked accounts: `Import-Module ActiveDirectory` then `Search-ADAccount -LockedOut`.",
    ])
    s.h3("Kerberos Policy (domain only)")
    s.table(["Setting", "Default"], [
        ["Enforce user logon restrictions", "Enabled"],
        ["Maximum lifetime for service ticket", "**600 minutes** (10 h)"],
        ["Maximum lifetime for user ticket (TGT)", "**10 hours**"],
        ["Maximum lifetime for user ticket renewal", "**7 days**"],
        ["Maximum tolerance for computer clock synchronization", "**5 minutes**"],
    ], widths=(4.0, 3.5))
    s.box("memory", "**\"24-42-1-7, complexity on, lockout 0\"**: history 24, max age 42, min age 1, length 7, complex Enabled, reversible Disabled, threshold 0 (never). **Kerberos: 10 hours / 7 days / 5 minutes / 600 minutes.**")

    # ---------------- SG-28 ----------------
    s.h2("SG-28  User Rights Assignment, Security Options, Security Templates, Audit Policy")
    s.h3("Settings the GPO lecture walks through")
    s.table(["Setting", "Path in the GPO editor"], [
        ["**Configure user Group Policy loopback processing mode**", "Computer Configuration → Policies → Administrative Templates → System → **Group Policy**. **Replace** = the computer's user settings replace the user's. **Merge** = both apply, and the computer's win on a conflict."],
        ["**Display Shutdown Event Tracker**", "Computer Configuration → Policies → Administrative Templates → **System**. Enable and choose Always to force a shutdown reason."],
        ["**Display information about previous logons during user logon**", "Computer Configuration → Policies → Administrative Templates → Windows Components → **Windows Logon Options**."],
        ["**Allow log on locally** and **Allow log on through Remote Desktop Services**", "Computer Configuration → Policies → Windows Settings → Security Settings → Local Policies → **User Rights Assignment**. The lecture highlights these two. On a member server, Allow log on through Remote Desktop Services is **Not Defined** in the Default Domain Policy (the local default is Administrators and Remote Desktop Users)."],
        ["**All Removable Storage classes: Deny all access**", "Administrative Templates → System → **Removable Storage Access**. This one overrides the per-device deny-read and deny-write settings. The wallpaper lab uses it to block USB in a student lab."],
        ["**Configure Automatic Updates**", "Administrative Templates → Windows Components → **Windows Update**. The lecture sets it **Enabled**, option **3 – Auto download and notify for install** (2 = notify before download; 4 = scheduled install, with day and time, shown as every day at 03:00)."],
    ], widths=(2.6, 4.9), size=8)
    s.p("Scoping example from the last lecture slides: a GPO named **Server updates** is linked to the domain with a WMI filter **Windows Server 2016** (`Version like \"10%\" and ProductType > 1`), so clients do not receive the server update settings. A second screenshot scopes the same idea with **security filtering** instead of WMI: remove the broad default and add the server groups (the slide shows `CCBD-DC$`, `CCBD-RDS$`, `CCBD-SAP$` and `CCB-SERVERS$`).", size=9)
    s.h3("User Rights Assignment: who may do what (selected defaults)")
    s.tag("extra", "The lecture shows where User Rights Assignment is and highlights Allow log on locally and Allow log on through Remote Desktop Services. The principal lists below are the Microsoft defaults.")
    s.table(["User right", "Member server default", "Domain controller default"], [
        ["**Allow log on locally**", "Administrators, Backup Operators, Users", "Administrators, Backup Operators, **Account Operators, Print Operators, Server Operators**, ENTERPRISE DOMAIN CONTROLLERS (**not** Domain Users)"],
        ["**Allow log on through Remote Desktop Services**", "Administrators, Remote Desktop Users", "**Administrators** only"],
        ["Access this computer from the network", "Everyone, Administrators, Users, Backup Operators", "Everyone, Administrators, Authenticated Users, ENTERPRISE DOMAIN CONTROLLERS, Pre-Windows 2000 Compatible Access"],
        ["Deny log on locally / Deny access from network", "Guest", "(not defined)"],
        ["**Add workstations to domain**", "—", "**Authenticated Users** (limited to 10 by `ms-DS-MachineAccountQuota`)"],
        ["Back up / Restore files and directories", "Administrators, Backup Operators", "+ Server Operators"],
        ["Change the system time", "Administrators, LOCAL SERVICE", "+ Server Operators"],
        ["Shut down the system", "Administrators, Backup Operators", "Administrators, Backup, Server and Print Operators"],
        ["Force shutdown from a remote system", "Administrators", "Administrators, Server Operators"],
        ["Take ownership of files or other objects", "Administrators", "Administrators"],
        ["Debug programs / Load and unload device drivers", "Administrators", "Administrators (+ Print Operators for drivers)"],
        ["Manage auditing and security log", "Administrators", "Administrators"],
        ["Log on as a service / as a batch job", "NT SERVICE\\ALL SERVICES / Administrators, Backup Operators, Performance Log Users", "Same"],
    ], widths=(2.2, 2.3, 3.0), size=8)
    s.box("key", "**Configure:** GPMC → edit the GPO (Default Domain Controllers Policy for DCs, a custom GPO for servers) → Computer Configuration → Policies → Windows Settings → Security Settings → Local Policies → **User Rights Assignment** → double-click the right → *Define these policy settings* → Add User or Group. **A GPO setting replaces the whole list; it doesn't append to it.** This explains the Lab 2B result that `bby\\administrator` can't log on to the parent DC: only the parent's groups appear in its *Allow log on locally* list.")
    s.h3("Security Options (selected defaults and hardening)")
    s.tag("extra", "Not in the GPO lecture. These are the Microsoft defaults and the usual hardening choices.")
    s.table(["Security Option", "Default", "Hardening tip"], [
        ["Accounts: Administrator account status", "Enabled", "Rename it (*Accounts: Rename administrator account*) and use named admin accounts"],
        ["Accounts: Guest account status", "**Disabled**", "Keep it disabled"],
        ["Accounts: Limit local account use of blank passwords to console logon only", "Enabled", "Keep"],
        ["Interactive logon: Do not require CTRL+ALT+DEL", "Disabled (so CTRL+ALT+DEL **is** required)", "Keep (secure attention sequence)"],
        ["Interactive logon: Don't display last signed-in", "Disabled", "Enable on shared or kiosk servers"],
        ["Interactive logon: Message title/text for users attempting to log on", "Blank", "Legal notice banner"],
        ["Interactive logon: Machine inactivity limit", "Not defined", "900 seconds"],
        ["Interactive logon: Number of previous logons to cache", "10", "Lower it on servers (0–2)"],
        ["Network security: Do not store LAN Manager hash value", "Enabled", "Keep"],
        ["Network security: LAN Manager authentication level", "Not defined (effectively *Send NTLMv2 response only*)", "*Send NTLMv2 only. Refuse LM & NTLM*"],
        ["Microsoft network server: Digitally sign communications (always)", "Enabled on DCs, disabled on members (up to 2022)", "Enable everywhere (on by default in 2025)"],
        ["Domain member: Maximum machine account password age", "30 days", "Keep"],
        ["UAC: Run all administrators in Admin Approval Mode", "Enabled", "Keep"],
        ["UAC: Admin Approval Mode for the built-in Administrator", "Disabled", "Enable"],
        ["UAC: Elevation prompt behaviour (admins / standard users)", "Prompt for consent for non-Windows binaries / Prompt for credentials", "Prompt for credentials on the secure desktop"],
        ["Audit: Force audit policy subcategory settings to override category settings", "Enabled", "Keep (needed for Advanced Audit Policy)"],
    ], widths=(3.0, 2.3, 2.2), size=8)
    s.h3("Security templates")
    s.tag("supp", "The study guide lists security templates. The GPO lecture and lab do not cover them.")
    s.bullets([
        "A **security template** is an `.inf` text file holding security settings (account policies, local policies, event log, restricted groups, services, registry and file ACLs). It gives you a **repeatable baseline**.",
        "Tools: **Security Templates** snap-in (create and edit `.inf` files; default custom path `Documents\\Security\\Templates`) and **Security Configuration and Analysis** snap-in (Open Database `.sdb` → Import Template → **Analyze Computer Now** compares the machine with the template, and **Configure Computer Now** applies it).",
        "**Deploy to many machines:** GPMC → edit GPO → Computer Configuration → Policies → Windows Settings → right-click **Security Settings → Import Policy…** → pick the `.inf`.",
        "Built-in reference templates: `%SystemRoot%\\inf\\defltbase.inf`, `defltsv.inf`, `DC security.inf`. Microsoft now publishes **Security Baselines** in the **Security Compliance Toolkit** (with `LGPO.exe` and *Policy Analyzer*).",
    ])
    s.code("""secedit /export /cfg C:\\Sec\\current.inf                       # export the current local security settings
secedit /analyze /db C:\\Sec\\sec.sdb /cfg C:\\Sec\\baseline.inf /log C:\\Sec\\analyze.log
secedit /configure /db C:\\Sec\\sec.sdb /cfg C:\\Sec\\baseline.inf /areas SECURITYPOLICY USER_RIGHTS
secedit /validate C:\\Sec\\baseline.inf""", title="secedit")
    s.h3("Audit Policy")
    s.tag("supp", "The study guide lists audit policy. The GPO lecture and lab do not cover it. The only course mention is that Nano Server can import audit settings from a .csv file.")
    s.table(["Basic audit category", "Audits", "Typical setting"], [
        ["Audit **account logon** events", "Credential validation **on the DC** (Kerberos / NTLM) for domain accounts", "Success, Failure"],
        ["Audit **logon** events", "Logon and logoff **on the machine** the user accesses", "Success, Failure"],
        ["Audit **account management**", "User or group created, changed, deleted, enabled, disabled; password resets", "Success"],
        ["Audit **directory service access**", "Access to AD objects that have SACLs", "Success (DCs)"],
        ["Audit **object access**", "Files, folders, registry keys, printers. **Needs a SACL on the object too**", "Success/Failure on sensitive data"],
        ["Audit **policy change**", "Changes to audit, user rights or trust policy", "Success"],
        ["Audit **privilege use**", "Use of user rights (e.g. take ownership)", "Failure"],
        ["Audit **process tracking**", "Process start and exit", "Usually off (noisy)"],
        ["Audit **system** events", "Startup, shutdown, security log cleared, system time change", "Success"],
    ], widths=(2.2, 3.6, 1.7), size=8)
    s.bullets([
        "**Basic** audit policy (9 categories above) is at *Local Policies\\Audit Policy*. **Advanced Audit Policy Configuration** (10 categories, about 58 subcategories such as *Logon*, *Credential Validation*, *File System*) is at *Security Settings\\Advanced Audit Policy Configuration*. **Don't mix the two.**",
        "**Defaults:** Windows Server audits key **Success** events out of the box (logon, account logon, account management, policy change, system, plus DS access on DCs). **Object access, privilege use and process tracking aren't audited by default.** Check the real effective settings with `auditpol /get /category:*`.",
        "**Auditing a folder (object access):** (1) enable *Audit object access* (or *Audit File System*) in a GPO; (2) folder → Properties → Security → Advanced → **Auditing** tab → Add principal (e.g. Everyone) → Success/Failure → which accesses; (3) read the **Security** log in Event Viewer.",
    ])
    s.table(["Event ID", "Meaning", "Event ID", "Meaning"], [
        ["**4624**", "Successful logon", "**4625**", "Failed logon"],
        ["4634 / 4647", "Logoff", "**4740**", "Account locked out"],
        ["4720", "User account created", "4726", "User account deleted"],
        ["4728 / 4732 / 4756", "Member added to global / local / universal group", "4738", "User account changed"],
        ["4768 / 4771", "Kerberos TGT requested / pre-auth failed", "4776", "NTLM credential validation"],
        ["4663", "Object access attempt", "4719", "Audit policy changed"],
        ["**1102**", "Security log cleared", "4672", "Special (admin) privileges assigned at logon"],
    ], widths=(1.2, 2.55, 1.2, 2.55), size=8)
    s.code("""auditpol /get /category:*
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /category:"Account Management" /success:enable
auditpol /backup /file:C:\\audit.csv ; auditpol /restore /file:C:\\audit.csv
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20""", title="Audit commands")

    s.h3("Makeup bonus (Windows Server Hardening and Security): model answers")
    s.tag("model")
    s.qa([
        ["What is the principle of least privilege and how should it be applied?", "Every user, service and admin gets **only the access needed, only for as long as it's needed**. Apply it with role groups (IGDLA), separate admin accounts (no browsing or email as an admin), tiered admin and PAW, Just-Enough/Just-In-Time admin (JEA, PAM), gMSAs for services, removing users from local Administrators (LAPS for unique local admin passwords), reviewing group membership regularly, and NTFS **Modify** instead of Full Control."],
        ["How can GPOs help secure a Windows Server environment?", "Centrally enforce password, lockout and Kerberos policy (plus FGPP for admins); audit policy; user rights (deny RDP or local logon for service accounts); Security Options (NTLMv2 only, SMB signing, rename Administrator, disable Guest); **Restricted Groups** to control local Administrators membership; Defender Firewall rules; AppLocker/WDAC; disable SMBv1; BitLocker, LAPS, Windows Update/WSUS; removable-media restrictions; legal banner and screen lock; import Microsoft security baselines."],
        ["Best practices for Windows Defender Firewall?", "Keep it **on for all three profiles** (Domain, Private, Public); **default inbound = block, outbound = allow** (or block for high-security servers); allow only the ports each role needs (scoped by remote IP or subnet); manage it centrally with GPO and disable local rule merging; turn on logging of dropped packets (`%systemroot%\\system32\\LogFiles\\Firewall\\pfirewall.log`); use connection security (IPsec) rules for sensitive traffic; review rules regularly. Cmdlets: `New-NetFirewallRule`, `Get-NetFirewallProfile`, `Set-NetFirewallProfile -All -Enabled True`."],
        ["What is the Security Configuration Wizard (SCW)?", "A 2003 SP1–2012 R2 tool (`scw.exe`, `scwcmd`) that built a **role-based security policy**: it asks which roles the server performs, then disables unneeded services, closes firewall ports, sets registry, audit and SMB/LDAP signing options. The policy (XML) can be applied to other servers or converted to a GPO (`scwcmd transform`). It **reduces the attack surface** consistently. **It was removed in Server 2016+**, replaced by Microsoft Security Baselines (Security Compliance Toolkit), Server Core or minimal installs, WAC and Defender."],
        ["Why have a disaster recovery plan and what should it include?", "Outages, ransomware, hardware failure and disasters will happen. A DR plan reduces downtime and data loss and is often legally required. Include: a risk assessment and business impact analysis; **RTO/RPO** per system; an inventory and dependency map (AD, DNS, DHCP first); a **backup strategy (3-2-1, offline or immutable copy)**, including AD **system state** and DSRM passwords; recovery procedures (authoritative or non-authoritative AD restore, FSMO seizure, Hyper-V Replica or Azure Site Recovery); contacts, roles and a communication plan; an alternate site; and **regular testing** and updates."],
    ], title=None)
