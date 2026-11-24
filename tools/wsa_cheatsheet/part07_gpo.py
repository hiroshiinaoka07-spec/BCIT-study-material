"""Part 7: Group Policy and security policies (SG-26 to SG-28)."""


def part7(s):
    s.part("PART 7 — GROUP POLICY AND SECURITY POLICIES (SG-26 to SG-28)")
    s.tag("supp", "The Week 12 GPO lecture and lab were not in the course folder. The only course material here is the Week 12 and makeup discussion prompts, the ADSI Edit screenshot of the default domain password values (DC slide p32), and the GPMC / NRPT / gpupdate / gpresult steps in the optional DNSSEC lab.")

    # ---------------- SG-26 ----------------
    s.h2("SG-26  What is a GPO and why do we use it?")
    s.p("A **Group Policy Object (GPO)** is a named collection of settings (security policy, registry-based Administrative Templates, scripts, software installation, folder redirection, firewall rules, preferences) that AD applies **automatically** to the **users and computers** in the **site, domain or OU** it's **linked** to. It's how one admin configures and enforces thousands of machines consistently.")
    s.table(["GPO part", "Applies to / when", "Examples"], [
        ["**Computer Configuration**", "Computer objects, at **startup** and every refresh", "Password and lockout policy, audit, user rights, firewall, startup scripts, BitLocker, Windows Update"],
        ["**User Configuration**", "User objects, at **logon** and every refresh", "Desktop restrictions, drive maps, folder redirection, logon scripts, Control Panel lockdown"],
        ["**Policies** vs **Preferences**", "Policies are enforced and reverted when the GPO is removed (written under `HKLM\\SOFTWARE\\Policies` / `HKCU\\SOFTWARE\\Policies`). Preferences are defaults the user can change, they \"tattoo\" (persist), and they support item-level targeting.", "Policy: hide Control Panel. Preference: map drive `H:`, create a shortcut, deploy a printer or registry value"],
    ], widths=(1.8, 3.0, 2.7))
    s.h3("Where a GPO lives")
    s.table(["Component", "Location", "Replicated by"], [
        ["**GPC** (Group Policy Container)", "AD: `CN={GUID},CN=Policies,CN=System,DC=adatum,DC=com` (version, status, links)", "AD replication"],
        ["**GPT** (Group Policy Template)", "**SYSVOL**: `\\\\adatum.com\\SYSVOL\\adatum.com\\Policies\\{GUID}\\` (`GPT.INI`, `Machine\\`, `User\\`, `Registry.pol`, scripts)", "**DFS-R** (FRS before 2008)"],
        ["Default GPOs", "**Default Domain Policy** (linked to the domain: **password, lockout and Kerberos policy**) and **Default Domain Controllers Policy** (linked to the *Domain Controllers* OU: **user rights, audit** for DCs)", ""],
        ["Local GPO", "`%SystemRoot%\\System32\\GroupPolicy` (edit with `gpedit.msc`; security part with `secpol.msc`)", "Not replicated"],
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
        ["**WMI filtering**", "Applies only if a WMI query is true (e.g. `SELECT * FROM Win32_OperatingSystem WHERE ProductType = 3` for servers)."],
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
    s.h3("User Rights Assignment: who may do what (selected defaults)")
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
