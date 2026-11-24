"""Part 3: Active Directory Domain Services (SG-6 to SG-16)."""


def part3(s):
    s.part("PART 3 — ACTIVE DIRECTORY DOMAIN SERVICES (SG-6 to SG-16)")
    s.src("Domain Controller lecture slides (p1–p48); SS64 group-scopes handout; AD DS vs Azure AD vs Azure AD DS handout; Repadmin handout; forced DC removal handout; Lab 2A, Lab 2B; videos: install AD DS, subdomain, domain tree, second DC, trust relationship; AD DS Issues slides; Week 3–4 discussion prompts.")

    s.h3("AD DS in one paragraph")
    s.p("**Active Directory Domain Services (AD DS)** is Microsoft's directory service: a distributed, replicated, hierarchical database of **objects** (users, groups, computers, printers, OUs). Each object is made of **attributes**, and which attributes an object can have is defined by the **schema**. AD DS provides centralized **authentication** (who are you? Kerberos v5, NTLM), **authorization** (what can you access? SIDs in tokens checked against ACLs), and centralized **management** (Group Policy, delegation). Clients find it with **DNS SRV records** and query it with **LDAP**.")
    s.table(["Term", "Meaning"], [
        ["Object / attribute", "An object is a thing (a user); attributes are its properties (sAMAccountName, mail, memberOf)."],
        ["Container vs leaf object", "A container holds other objects (OU, domain, the built-in Users and Computers containers); a leaf holds nothing (a user or computer)."],
        ["Organizational Unit (OU)", "A container you create to **delegate administration** and **link GPOs**. The built-in *Users* and *Computers* folders are containers, not OUs, so you can't link a GPO to them."],
        ["Domain", "An administrative boundary and a **replication boundary** for the domain partition. Every DC in a domain holds the same domain data."],
        ["Tree", "One or more domains with a **contiguous namespace** (adatum.com → bby.adatum.com), joined by automatic two-way transitive parent-child trusts."],
        ["Forest", "One or more trees sharing **one schema, one configuration partition and one Global Catalog**. The **forest is the security boundary**. The first domain is the **forest root domain**."],
        ["Trust", "Lets users in one domain access resources in another. Parent-child and tree-root trusts are automatic, two-way and transitive. Manual ones are external, forest, shortcut and realm trusts."],
        ["Site", "One or more well-connected **IP subnets**. Controls replication traffic and which DC a client uses (the closest one)."],
        ["SYSVOL", "A shared folder on every DC (`%SystemRoot%\\SYSVOL`; shares **SYSVOL** and **NETLOGON**) that holds **GPO templates and logon scripts**, replicated by DFS-R."],
        ["Default protocols", "**LDAP 389** (LDAPS 636), **GC 3268** (GC over SSL 3269), **Kerberos 88**, DNS 53, SMB 445, RPC 135 + dynamic ports, kpasswd 464, NTP 123 (UDP)."],
    ], widths=(1.7, 5.8))
    s.table(["", "AD DS (on-prem)", "Azure AD / Entra ID", "Azure AD Domain Services"], [
        ["What", "Traditional directory on DCs you manage", "Cloud identity service (IDaaS)", "Managed domain run by Microsoft in Azure"],
        ["Protocols", "LDAP, Kerberos, NTLM", "OAuth 2.0, OpenID Connect, SAML, Graph API", "LDAP, Kerberos, NTLM"],
        ["Structure", "OUs, domains, forests, trusts", "Flat tenant; no OUs or GPOs", "Domain join, Group Policy, LDAP; flat OU structure"],
        ["Management", "Group Policy", "Intune / MDM, Conditional Access", "Group Policy (limited)"],
        ["Typical use", "Corporate LAN, legacy apps", "SaaS / Microsoft 365 sign-in, SSO", "**Lift-and-shift** legacy apps to Azure VMs"],
        ["Limits", "You patch and secure the DCs", "No Kerberos/LDAP for legacy apps", "**No schema extensions, no Domain/Enterprise Admin rights, one-way outbound forest trust only**"],
    ], widths=(0.9, 2.1, 2.2, 2.3), size=8)

    # ---------------- SG-6 ----------------
    s.h2("SG-6  What is a Domain Controller? How do you deploy AD DS?")
    s.p("A **Domain Controller (DC)** is a server running the AD DS role that holds a copy of the AD database (`ntds.dit`), authenticates users and computers (it runs the **Kerberos KDC**), applies security policy, hosts **SYSVOL**, and replicates changes **multi-master** with the other DCs. A **member server** is joined to the domain but doesn't hold AD (for example a file server). Best practice: **at least 2 DCs per domain** (BCIT runs 8), use an RODC or BitLocker where physical security is weak, and put DNS on the DCs.")
    s.h3("Before you promote (prerequisites)")
    s.bullets([
        "**Static IP address**. The first DC's DNS points to itself (`127.0.0.1` or its own IP, which is what the lab used). Additional DCs point to an existing DC.",
        "Set the final **computer name** first (renaming a DC later is painful).",
        "A **strong local Administrator password** (it becomes the domain Administrator in a new forest).",
        "An NTFS volume for SYSVOL. Reachable DNS. Correct time (Kerberos allows at most **5 minutes** of clock skew).",
        "New child domain or tree: use **Enterprise Admin** credentials. Additional DC: **Domain Admin** credentials (not local). The server does **not** need to be domain-joined before promotion (subdomain video).",
    ])
    s.h3("GUI deployment (Lab 2A / Lab 2B)")
    s.steps([
        "Server Manager → Manage → **Add Roles and Features** → **Role-based or feature-based installation** → select the server → tick **Active Directory Domain Services** → Add Features → Install.",
        "Click the yellow notification flag → **Promote this server to a domain controller**.",
        "**Deployment Configuration**: choose **Add a new forest** (root domain `adatum.com`), **Add a new domain to an existing forest** (Child: parent `adatum.com`, new name `bby`; or Tree: `indy.com`), or **Add a domain controller to an existing domain** (second DC).",
        "**Domain Controller Options**: forest and domain functional levels, **DNS server**, **Global Catalog**, **Read-only domain controller (RODC)**, site, **DSRM password**.",
        "**DNS Options**: the warning \"A delegation for this DNS server cannot be created…\" is normal for a new forest. For a **child domain**, ask for a delegation in the parent zone.",
        "**Additional Options**: NetBIOS name (`ADATUM`, at most 15 characters), or *Install from media* / *Replicate from* (any DC).",
        "**Paths**: Database, Log files, SYSVOL (defaults `C:\\Windows\\NTDS`, `C:\\Windows\\SYSVOL`). Best practice is to put the database and logs on separate disks for performance and recovery.",
        "**Review Options → View script** (shows the PowerShell below) → **Prerequisites Check** → **Install**. The server reboots and you log on as `ADATUM\\Administrator`.",
    ])
    s.code("""Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Import-Module ADDSDeployment
Install-ADDSForest -CreateDnsDelegation:$false -DatabasePath "C:\\Windows\\NTDS" `
  -DomainMode "WinThreshold" -DomainName "adatum.com" -DomainNetbiosName "ADATUM" `
  -ForestMode "WinThreshold" -InstallDns:$true -LogPath "C:\\Windows\\NTDS" `
  -NoRebootOnCompletion:$false -SysvolPath "C:\\Windows\\SYSVOL" -Force:$true
# WinThreshold = Windows Server 2016 functional level (the highest for 2016/2019/2022)""",
           title="Lab 2A: new forest in PowerShell (the script the wizard generates)")
    s.code("""Install-ADDSDomain -NewDomainName bby -ParentDomainName adatum.com -DomainType ChildDomain `
  -InstallDns -CreateDnsDelegation -Credential (Get-Credential ADATUM\\Administrator)       # child domain
Install-ADDSDomain -NewDomainName indy.com -ParentDomainName adatum.com -DomainType TreeDomain  # new tree
Install-ADDSDomainController -DomainName adatum.com -InstallDns -Credential (Get-Credential) # extra DC
Install-ADDSDomainController -DomainName adatum.com -ReadOnlyReplica -SiteName Branch       # RODC
Uninstall-ADDSDomainController                                                               # demote""",
           title="Other deployment cmdlets")
    s.box("instructor", [
        "- **Server Core DCs** are installed in two phases: `Install-WindowsFeature AD-Domain-Services`, then `Install-ADDSForest` or `Install-ADDSDomainController` (there's no GUI wizard).",
        "- **Install From Media (IFM)** for slow WAN branches: on an existing DC run `ntdsutil` → `activate instance ntds` → `ifm` → `create full c:\\ifm`, copy the folder to the branch, then promote with *Install from media*. Only the delta replicates over the WAN.",
        "- **DSRM password** (Directory Services Restore Mode) is the local admin password used to boot the DC into DSRM to **repair or restore AD** (authoritative restore) or to force a demotion. Store it safely.",
    ])
    s.h3("Verify the new DC")
    s.code("""dcdiag /v                                  # full DC health test (run after every promotion)
dcdiag /test:dns
repadmin /replsummary                      # replication health (see SG-8)
nslookup  ->  set type=srv  ->  _ldap._tcp.dc._msdcs.adatum.com      # DC locator SRV records
nltest /dsgetdc:adatum.com                 # which DC does this client find?
Get-Service ADWS, KDC, Netlogon, DNS, NTDS
net share                                  # SYSVOL and NETLOGON must be shared""")
    s.p("The SRV answer looks like `_ldap._tcp.dc._msdcs.adatum.com SRV service location: priority = 0, weight = 100, port = 389, svr hostname = ca-van-svr1.adatum.com` (slide p30).", size=9)
    s.h3("Joining a client or member server to the domain")
    s.steps([
        "Same virtual network as the DC (the lab uses **VMnet9**, host-only). Static IP or DHCP, with **preferred DNS = the DC's IP (192.168.239.1)**.",
        "`ping 192.168.239.1` and `ping adatum.com`. If the ping fails, add the ICMP firewall rule on the DC (Part 1).",
        "System Properties → Change → Domain: `adatum` (NetBIOS) or `adatum.com` (FQDN) → enter domain credentials → restart. PowerShell: `Add-Computer -DomainName adatum.com -Credential ADATUM\\Administrator -Restart`.",
        "Log on as `ADATUM\\user`, then check with `hostname`, `whoami`, `whoami /user`, `echo %logonserver%`.",
    ])
    s.box("trouble", [
        "**\"An Active Directory Domain Controller for the domain could not be contacted\":** the client's DNS points to the router, 8.8.8.8 or nothing. Point it to the DC and `ipconfig /flushdns`.",
        "**Child domain promotion fails with a DNS error (Lab 2B):** the parent zone has no delegation for `bby.adatum.com`. On Svr1, open DNS → adatum.com → **New Delegation** → `bby` → Svr3's IP. The new DC's DNS must point to the parent DC during promotion.",
        "**New tree (indy.com): \"YOU CAN NOT PING INDY.COM\" (domain tree video):** adatum's DNS doesn't know the indy.com zone. Add a **conditional forwarder** (or stub zone) for indy.com on Svr1 and for adatum.com on Svr4, or store both zones as AD-integrated with forest-wide replication.",
        "**\"The security database on the server does not have a computer account for this workstation trust relationship\" / \"The trust relationship between this workstation and the primary domain failed\" (trust relationship video):** the computer account's password no longer matches the one AD holds. Causes: restoring or reverting the DC or client snapshot, a cloned (non-sysprepped) machine, or a deleted computer object (C1 was missing from *Computers*). **Fix used in the lab:** join a workgroup, restart, rejoin the domain. Faster supplemental fixes: `Test-ComputerSecureChannel -Repair -Credential ADATUM\\Administrator` or `Reset-ComputerMachinePassword`.",
        "**Too many joins by a normal user:** \"Your computer could not be joined… exceeded the maximum number of computer accounts\". `ms-DS-MachineAccountQuota` = 10. Pre-stage the computer account or use an admin account.",
    ])

    s.h3("Lab 2A: Questions & Answers")
    s.qa([
        ["Define Active Directory.", "Microsoft's directory service: a hierarchical, replicated database of network objects that provides centralized authentication, authorization and management (Group Policy) for a Windows domain."],
        ["What is a domain controller?", "A server with the AD DS role that stores a copy of the directory, authenticates logons (Kerberos KDC), hosts SYSVOL and replicates with other DCs."],
        ["Trees vs forests?", "A tree is domains in one contiguous namespace. A forest is one or more trees sharing a schema, configuration and GC; it is the security boundary."],
        ["Default directory-access protocol?", "**LDAP** (Lightweight Directory Access Protocol), TCP/UDP **389** (LDAPS 636, GC 3268)."],
        ["Which tools edit AD?", "ADUC (`dsa.msc`) and the AD Administrative Center for everyday objects; **ADSI Edit** (`adsiedit.msc`) for raw attributes and partitions; the AD PowerShell module; AD Schema snap-in; Sites and Services; Domains and Trusts."],
        ["What is SYSVOL?", "A shared folder on every DC containing Group Policy templates (`\\\\adatum.com\\SYSVOL\\adatum.com\\Policies`) and logon scripts (the NETLOGON share), replicated to all DCs by DFS-R."],
        ["What is Kerberos?", "The default AD authentication protocol (v5, port 88). It's ticket-based: the KDC's Authentication Service issues a **TGT**, and the Ticket-Granting Service issues **service tickets**. It provides mutual authentication, the password never crosses the network, and it requires time sync (5-minute skew)."],
        ["Domain Admins vs Enterprise Admins?", "Domain Admins administer one domain. Enterprise Admins (forest root only, universal group) administer the whole forest."],
        ["Why does the wizard warn about DNS delegation?", "There's no parent zone you control (you don't own `.com`'s DNS), so no delegation can be created. That's expected for a new forest root; ignore it."],
        ["What is the NetBIOS domain name for?", "Pre-Windows 2000 / legacy logon name (`ADATUM\\user`), at most 15 characters."],
        ["Why separate the database and log paths?", "Performance (sequential log writes vs random database I/O) and recoverability (if one disk fails, the other still holds data needed for restore)."],
        ["Role-based vs Remote Desktop Services installation?", "Role-based or feature-based installs roles and features on a single server. Remote Desktop Services (scenario-based) installation deploys RDS components across several servers."],
        ["Does a client need to be on the same network and DNS as the DC to join?", "Yes. It must resolve the domain's SRV records through DNS (point DNS at the DC) and reach the DC (same VMnet9 or routed)."],
        ["One DC still runs 2012 R2. Can you raise the domain functional level to 2016?", "**No.** Every DC in the domain must run 2016 or later. Upgrade or demote the 2012 R2 DC first."],
    ])
    s.h3("Lab 2B + videos (child domain, second DC, tree): Questions & Answers")
    s.qa([
        ["Must Svr3 join adatum.com before becoming the bby child DC?", "No. Give it a static IP with DNS pointing to the parent DC (Svr1), choose *Add a new domain to an existing forest → Child Domain*, parent `adatum.com`, name `bby`, and supply **Enterprise Admin** credentials. Install DNS + GC and set the DSRM password."],
        ["How do you know Svr3 is a subdomain DC?", "Server Manager shows the domain **bby.adatum.com**; DNS on Svr1 shows a delegated **bby** folder under adatum.com; Sites and Services lists it under the site; its FQDN is `ca-van-svr3.bby.adatum.com`."],
        ["Is ca-van-svr3 visible in the parent's ADUC (adatum.com → Domain Controllers)?", "No. It belongs to the bby.adatum.com domain partition. You'd have to connect ADUC to bby.adatum.com, or search the GC."],
        ["An account created on Svr2 (a second DC in adatum.com). Is it visible on Svr1?", "**Yes.** Same domain, so the domain partition replicates multi-master between Svr1 and Svr2 (force it with `repadmin /replicate`)."],
        ["Is that account visible on Svr3 (bby)?", "**No** in bby's ADUC, because it's a different domain partition. (It is in the GC, so a forest-wide search finds it.)"],
        ["A WinServer account created on Svr3. Visible on Svr1 or Svr2?", "**No.** It lives in bby.adatum.com."],
        ["Can adatum\\administrator log on to Svr3 (child)?", "**Yes.** Enterprise Admin, transitive trust."],
        ["Can bby\\administrator log on to Svr1 (parent DC)?", "**No.** It's only a Domain Admin of bby and has no *Allow log on locally* right on the parent's DCs."],
        ["Second DC: which credentials and options?", "*Add a domain controller to an existing domain*, **domain admin** (not local) credentials, DNS + GC, Replicate from: Any DC. Then run `dcdiag /v` and test replication with `repadmin /replicate`."],
        ["Child vs tree: what's the difference?", "Child shares the parent's namespace (bby.adatum.com). Tree is a new namespace in the same forest (indy.com). Both get automatic two-way transitive trusts and share the schema and GC."],
        ["Online vs offline domain join? (AD DS Issues slides)", "Online: the machine contacts a DC during the join. Offline: `djoin.exe /provision` on a DC-connected machine creates a blob, then `djoin /requestodj` applies it on the target with no DC connectivity (used for Nano Server, see SG-18)."],
    ])

    # ---------------- SG-7 ----------------
    s.h2("SG-7  How many PDC Emulators are required?")
    s.box("key", "**Exactly one PDC Emulator per domain.** Number required = number of domains in the forest. adatum.com + bby.adatum.com = **2 PDC Emulators**; add indy.com and you need 3. (A forest always has just one Schema Master and one Domain Naming Master.)")
    s.tag("extra", "What the PDC Emulator does (the slides only list the role).")
    s.bullets([
        "**Time source:** the PDC Emulator of the **forest root domain** is the top of the domain time hierarchy. Point it to an external NTP source: `w32tm /config /manualpeerlist:\"pool.ntp.org\" /syncfromflags:manual /reliable:yes /update`. Kerberos fails beyond 5 minutes of skew.",
        "**Password changes** are sent to it urgently. A logon that fails on another DC is retried against the PDC before it's rejected.",
        "**Account lockout** processing.",
        "Default DC for **Group Policy editing** (GPMC targets the PDC, which avoids SYSVOL conflicts).",
        "Acts as a Windows NT 4.0 PDC for legacy clients (hence the name).",
        "It's the most heavily used FSMO role, so put it on a well-resourced, reliable DC.",
    ])

    # ---------------- SG-8 ----------------
    s.h2("SG-8  AD DS database (partitions), sites, trees and forests")
    s.h3("Directory partitions (naming contexts)")
    s.table(["Partition", "Replicated to", "Contains"], [
        ["**Schema**", "Every DC in the **forest**", "Definitions of every object class and attribute (the blueprint). One schema per forest; written only on the Schema Master."],
        ["**Configuration**", "Every DC in the **forest**", "Forest topology: sites, subnets, site links, services, partitions, display specifiers."],
        ["**Domain**", "Every DC in **that domain** (a partial copy goes to every GC)", "Users, groups, computers, OUs, GPO links for the domain."],
        ["**Application**", "DCs you choose (a custom scope)", "App data, mainly AD-integrated DNS: `DomainDnsZones`, `ForestDnsZones`. No security principals."],
    ], widths=(1.3, 2.2, 4.0))
    s.table(["Database file", "Purpose"], [
        ["`%SystemRoot%\\NTDS\\ntds.dit`", "The AD database (ESE / Jet engine). Location is set at promotion."],
        ["`edb.log`, `edbXXXXX.log`", "Transaction logs. Changes are written here first, then committed to ntds.dit."],
        ["`edb.chk`", "Checkpoint file that tracks which log entries have been committed."],
        ["`edbres00001.jrs`, `edbres00002.jrs`", "Reserve log files that let AD shut down cleanly if the disk fills up."],
        ["`%SystemRoot%\\SYSVOL`", "Group Policy templates and scripts (not part of ntds.dit, replicated by DFS-R)."],
    ], widths=(2.4, 5.1))
    s.code("""regsvr32 schmmgmt.dll        # register the AD Schema snap-in, then:  mmc -> File -> Add/Remove Snap-in -> Active Directory Schema
adsiedit.msc                 # connect to: Default naming context / Configuration / Schema""", title="View the partitions")
    s.h3("Sites and replication")
    s.bullets([
        "**Site** = one or more IP **subnets** joined by fast, reliable links. When a computer starts, it finds a DC **in its own site** (DC locator uses site-specific SRV records).",
        "**Intra-site replication** is change-notification based (seconds) and uncompressed. **Inter-site replication** is scheduled over **site links** (default every 180 minutes, cost 100) and compressed.",
        "**KCC (Knowledge Consistency Checker)** builds the replication topology automatically, re-checking **every 15 minutes**. One **bridgehead server** per site handles inter-site traffic.",
        "Tool: **AD Sites and Services** (`dssite.msc`): create sites, subnets, site links; NTDS Settings → *Replicate Now*. The default site is *Default-First-Site-Name*.",
    ])
    s.h3("Repadmin: replication troubleshooting (handout + lab audit)")
    s.table(["Command", "What it does"], [
        ["`repadmin /replsummary`", "**Run this first.** Summary of replication success or failure for every DC (largest delta, fails/total)."],
        ["`repadmin /showrepl *`", "Inbound replication partners and the last attempt for each partition (`/csv` for Excel)."],
        ["`repadmin /queue`", "Pending inbound replication requests."],
        ["`repadmin /syncall <DSA> [<NC>] [flags]`", "Sync one DC with **all** its partners. If you omit the naming context, it uses the Configuration partition. Handout flags: `/a` abort if a server is unavailable, `/h` help, `/i` iterate indefinitely, `/s` don't sync (test only), `/q` quiet. Common real-world form: `repadmin /syncall /AdeP` (all partitions, DNs, enterprise-wide, push)."],
        ["`repadmin /replicate ca-van-svr1 ca-van-svr2 dc=adatum,dc=com`", "Force replication **to** Svr1 **from** Svr2 for that partition (slide p44: \"Sync from ca-van-svr2 to ca-van-svr1 completed successfully\")."],
        ["`repadmin /kcc`", "Force the KCC to recalculate the topology now (it normally runs every 15 minutes)."],
        ["`repadmin /showobjmeta DC \"CN=User1,...\"`", "Per-attribute version and originating DC, to find which change won a conflict."],
        ["`repadmin /showattr DC \"DN\"`", "Show an object's attributes (LDAP 389; use the GC port 3268 for a forest-wide view)."],
        ["`repadmin /prp view RODC1 allow`", "View or edit an **RODC Password Replication Policy** (add / delete / move / view). Run it against a writable DC. You can't edit the Deny list this way."],
    ], widths=(3.3, 4.2), size=8)
    s.p("Lab audit order: `/replsummary` → `/queue` → `/showrepl` → `/syncall` → `/kcc` → `/replicate`. RODCs only ever appear as **destination** DSAs (replication is one-way, inbound only). Handout fix example: stop the KDC service, restart AD DS, then re-replicate.", size=9)
    s.h3("Removing a dead DC (forced removal / metadata cleanup handout)")
    s.bullets([
        "**ADUC** → Domain Controllers → right-click the dead DC → Delete → tick **\"Delete this Domain Controller anyway. It is permanently offline and can no longer be removed using the removal wizard\"**. Confirm whether it was a GC, and **transfer or seize its FSMO roles** to another DC.",
        "Or **Sites and Services** → server → NTDS Settings → Delete, then delete the server object.",
        "Or **ntdsutil** (classic method):",
    ])
    s.code("""ntdsutil
  metadata cleanup
    connections
      connect to server CA-VAN-SVR1        (a healthy DC)
      quit
    select operation target
      list domains        -> select domain 0
      list sites          -> select site 0
      list servers in site -> select server 1   (the dead DC)
      quit
    remove selected server
  quit""")
    s.p("Afterwards, **clean up DNS**: delete the dead DC's A, NS and SRV records (under `_msdcs`, `_sites`, `_tcp`, `_udp`).", size=9)

    # ---------------- SG-9 ----------------
    s.h2("SG-9  Global Catalog (GC) and how many you need")
    s.p("A **Global Catalog server** is a DC that also stores a **read-only partial replica of every object in every domain of the forest**, limited to the **Partial Attribute Set (PAS)**, the commonly searched attributes, plus its own domain in full. It listens on **TCP 3268** (3269 over SSL).")
    s.table(["The GC is used for", "Why"], [
        ["Forest-wide **searches**", "Find a user or printer in any domain without querying each domain's DCs."],
        ["**UPN logon** (`user@adatum.com`)", "Resolves the UPN to the right domain."],
        ["**Universal group membership** at logon", "Universal group memberships are only stored in the GC. Without a GC, logon fails or uses cached credentials, unless *Universal Group Membership Caching* is enabled for the site."],
        ["Exchange address book / Outlook GAL", "Exchange depends heavily on GCs."],
    ], widths=(2.4, 5.1))
    s.box("key", [
        "**Recommended number (study guide): at least 2 GCs** for fault tolerance, and ideally **one GC in every site**. The first DC in a forest is automatically a GC. Lab 2B ticked *Global Catalog* on every new DC.",
        "**Configure:** AD Sites and Services → Sites → *site* → Servers → *DC* → right-click **NTDS Settings** → Properties → tick **Global Catalog** (slide p22).",
    ])
    s.qa([
        ["Slide p22 question: should **all** DCs be GCs? Benefits vs drawbacks?", "**Benefits:** faster logons and searches (no WAN lookups), redundancy, and the Infrastructure Master placement problem disappears (if every DC is a GC, the IM can be anywhere). **Drawbacks:** more storage and **more replication traffic** (every domain's PAS replicates to every DC), significant over slow WAN links in big multi-domain forests. Modern guidance for most organizations is to make every DC a GC."],
        ["Slide p42 issue: adding ACIT Universal (adatum) to CIT Local (bby) shows \"The following object was not found… it may take 15 minutes or more to replicate to the global catalog\". Why?", "The universal group was just created; the object hasn't replicated to the GC that the bby DC is using yet. Wait for replication or force it (`repadmin /syncall`), then retry. Universal group membership lives in the GC."],
    ], title="Questions & Answers")
    s.code("""Get-ADDomainController -Filter {IsGlobalCatalog -eq $true} | Select Name, Site
Set-ADObject (Get-ADDomainController CA-VAN-SVR2).NTDSSettingsObjectDN -Replace @{options='1'}   # make it a GC
nltest /dsgetdc:adatum.com /gc""", title="GC commands")
    s.tag("extra", "PowerShell lines above.")

    # ---------------- SG-10 ----------------
    s.h2("SG-10  FSMO (Operations Master) roles: list and explain")
    s.p("Most AD changes are **multi-master** (made on any DC). Five operations are **single-master** to avoid conflicts. These are the **FSMO roles** (Flexible Single Master Operations). There are **2 forest-wide + 3 per domain**, so a forest with *n* domains has **2 + 3n role holders**.")
    s.table(["Role", "Scope (how many)", "What it does", "If it's down…", "Console to view / transfer"], [
        ["**Schema Master**", "Forest (1)", "The only DC that can **write schema changes** (new classes and attributes, `adprep /forestprep`, Exchange install).", "Can't extend the schema; otherwise unnoticed.", "**AD Schema** snap-in (`regsvr32 schmmgmt.dll` first) → right-click → Operations Master"],
        ["**Domain Naming Master**", "Forest (1)", "Adds or removes **domains** and application partitions in the forest; keeps domain names unique.", "Can't add or remove domains (e.g. Lab 2B child domain fails).", "**AD Domains and Trusts** → right-click root → Operations Master"],
        ["**RID Master**", "Domain (1 each)", "Hands each DC a **pool of 500 RIDs**. A SID is domain SID + RID, so this guarantees unique SIDs.", "When a DC's pool is used up, it can't create new users, groups or computers.", "**ADUC** → right-click domain → Operations Masters → RID tab"],
        ["**PDC Emulator**", "Domain (1 each)", "Time sync root, urgent password changes, lockouts, GPO-editing target, legacy NT PDC (see SG-7).", "Noticed immediately: time drift, password and lockout issues.", "**ADUC** → Operations Masters → PDC tab"],
        ["**Infrastructure Master**", "Domain (1 each)", "Updates **cross-domain references** (e.g. a bby user in an adatum group): refreshes the phantom's DN and SID.", "Stale names for cross-domain group members.", "**ADUC** → Operations Masters → Infrastructure tab"],
    ], widths=(1.2, 0.9, 2.3, 1.5, 1.6), size=8)
    s.tag("extra", "The course lists the roles and consoles. The function descriptions, transfer and seize steps, and placement rules come from Microsoft documentation and the Week 4 discussion topics.")
    s.box("memory", "**\"SD-RPI\": Schema, Domain naming (forest); RID, PDC, Infrastructure (domain).** Or \"**S**ome **D**omains **R**eally **P**refer **I**ndependence\".")
    s.code("""netdom query fsmo                                            # all 5 holders (Week 4 discussion: how to determine)
Get-ADForest | Select SchemaMaster, DomainNamingMaster
Get-ADDomain | Select PDCEmulator, RIDMaster, InfrastructureMaster
# TRANSFER (both DCs online, graceful)
Move-ADDirectoryServerOperationMasterRole -Identity CA-VAN-SVR2 -OperationMasterRole PDCEmulator,RIDMaster,InfrastructureMaster
#   roles can also be numbers: 0=PDC 1=RID 2=Infrastructure 3=Schema 4=DomainNaming
# SEIZE (old holder permanently dead) - add -Force, or ntdsutil:
ntdsutil  ->  roles  ->  connections  ->  connect to server CA-VAN-SVR2  ->  quit
          ->  seize pdc | seize rid master | seize infrastructure master | seize schema master | seize naming master""", title="Find, transfer and seize FSMO roles")
    s.box("trap", [
        "- **Transfer** = graceful, the current holder is online. **Seize** = a last resort when the holder is gone for good. **Never bring a DC back online after its RID, Schema or Domain Naming role was seized** (wipe and rebuild it).",
        "- **Infrastructure Master should not be on a GC** *unless* every DC is a GC or there's only one domain. A GC already holds the cross-domain data, so the IM never sees anything to update.",
        "- Placement: forest roles on a forest-root DC; PDC + RID together on the strongest DC of each domain.",
    ])

    # ---------------- SG-11 ----------------
    s.h2("SG-11  Domain and forest functional levels: when to raise the DFL")
    s.p("A **functional level** sets which AD features are available and which **minimum DC operating system** is allowed. It provides **backward compatibility**: a low level lets older DCs stay; a higher level unlocks features but blocks older DCs. The **domain functional level (DFL)** is per domain; the **forest functional level (FFL)** is for the whole forest.")
    s.table(["Level", "msDS-Behavior-Version", "Notable features unlocked"], [
        ["2008", "3", "DFS-R SYSVOL replication, Fine-Grained Password Policies, AES Kerberos"],
        ["2008 R2", "4", "**AD Recycle Bin** (FFL), Authentication Mechanism Assurance, managed service accounts"],
        ["2012", "5", "KDC support for claims and compound authentication (Dynamic Access Control)"],
        ["2012 R2", "6", "Protected Users group hardening, Authentication Policies and Silos"],
        ["**2016** (`WinThreshold`)", "**7** (seen in ADSI Edit, slide p32)", "Privileged Access Management (FFL), automatic NTLM secret rolling. **This is the highest level for 2016, 2019 and 2022 DCs. There is no \"2019\" or \"2022\" level.**"],
        ["2025", "10", "32K database pages, new security features (needs all DCs on 2025)"],
    ], widths=(1.5, 1.6, 4.4))
    s.tag("extra", "Version numbers and per-level features.")
    s.bullets([
        "**Rules:** DFL can't be higher than the **oldest DC OS in that domain**. FFL can't be higher than the **lowest DFL in the forest**. Raising is effectively **one-way**.",
        "**When to raise the DFL:** after **every DC in the domain** runs the newer OS (the old DCs are upgraded or demoted) **and** you need a feature of that level. Example: Lab 2A, with a 2012 R2 DC still present, you can't go to 2016.",
        "**Raise the DFL:** **ADUC** (or AD Domains and Trusts) → right-click the domain → **Raise Domain Functional Level**. **Raise the FFL:** **AD Domains and Trusts** → right-click *Active Directory Domains and Trusts* → **Raise Forest Functional Level** (slide p24).",
    ])
    s.code("""Get-ADDomain | Select DomainMode ;  Get-ADForest | Select ForestMode
Set-ADDomainMode -Identity adatum.com -DomainMode Windows2016Domain
Set-ADForestMode -Identity adatum.com -ForestMode Windows2016Forest""")

    # ---------------- SG-12 ----------------
    s.h2("SG-12  \"Adding attributes to an object changes the schema\"")
    s.box("key", "**True.** The **schema** defines every object class and the attributes each class may or must have. Adding a *new* attribute (or class) is a **schema extension**. **Filling in a value** of an existing attribute (e.g. a user's phone number) **does not** change the schema.")
    s.bullets([
        "The schema is **forest-wide** (one schema partition, replicated to every DC in the forest). Only the **Schema Master** can write it, and you must be in **Schema Admins**.",
        "Schema changes are **permanent**. You can't delete an attribute, only **deactivate (defunct)** it, so test in a lab first.",
        "Typical extenders: Exchange, `adprep /forestprep` before adding DCs with a newer OS, LAPS, SCCM.",
        "Tools: AD Schema snap-in (`regsvr32 schmmgmt.dll`), `ldifde -i -f ext.ldf`, ADSI Edit (Schema partition).",
    ])
    s.p("**Week 3 discussion, \"What is the AD schema?\"** It is the formal definition of every object class (user, computer, group…) and attribute (syntax, single- or multi-valued, indexed, whether it's in the GC's partial attribute set) that can exist in the forest. It's like a database schema: every DC enforces it so all replicas stay consistent.", size=9)

    # ---------------- SG-13 ----------------
    s.h2("SG-13  FQDN (Fully Qualified Domain Name)")
    s.p("An FQDN is the complete DNS name of a host: **host name + domain name(s) + top-level domain** (+ the implied root dot). Examples: `AcctDirPC.adatum.com` (slide), `ca-van-svr1.adatum.com`, child-domain DC `ca-van-svr3.bby.adatum.com`, `www.bcit.ca.` (trailing dot = root).")
    s.table(["Piece", "Example", "Notes"], [
        ["Host label", "ca-van-svr1", "At most 63 characters per label; letters, digits and hyphens"],
        ["Domain / subdomain", "adatum / bby.adatum", "The AD domain name = the DNS zone name"],
        ["TLD", "com / ca / local", "Use a domain you own (e.g. `ad.adatum.com`); avoid `.local` for new designs"],
        ["Whole FQDN", "ca-van-svr1.adatum.com", "At most 255 characters. Compare the **NetBIOS** name (`CA-VAN-SVR1`, at most 15 characters, flat)"],
    ], widths=(1.5, 2.2, 3.8))

    # ---------------- SG-14 ----------------
    s.h2("SG-14  Read-Only Domain Controller (RODC): what, why, how")
    s.p("An **RODC** (introduced in Windows Server 2008) holds a **read-only** copy of the AD database (except the password secrets it's allowed to cache) and a read-only DNS zone. Changes can't be made on it; replication is **one-way, inbound only**. It's designed for sites with **poor physical security** (branch offices, retail stores) or **slow or unreliable WAN links**.")
    s.table(["Feature", "Benefit"], [
        ["Read-only AD DS database", "A stolen or compromised RODC can't push malicious changes into the domain."],
        ["Unidirectional replication", "Less WAN traffic; the RODC only receives changes."],
        ["**Password Replication Policy (PRP)**", "By default it caches **no** passwords. Add branch users and computers to **Allowed RODC Password Replication Group**. Admins are in the **Denied** group. If the RODC is stolen, reset only the passwords it cached."],
        ["Read-only DNS", "Clients resolve names locally; updates are referred to a writable DC."],
        ["**Administrator role separation**", "A local branch user can be made the RODC's admin (patches, drivers) **without** being a Domain Admin."],
        ["Filtered Attribute Set (FAS)", "Sensitive app attributes (e.g. BitLocker keys) don't replicate to RODCs."],
    ], widths=(2.4, 5.1))
    s.h3("How to deploy (slide p34)")
    s.steps([
        "**Prerequisites:** a writable DC running 2008 or later in the domain (it must hold the PDC Emulator role), forest functional level 2003 or higher, and `adprep /rodcprep` on older forests.",
        "**Option A, one step:** Server Manager → AD DS → Promote → *Add a domain controller to an existing domain* → tick **Read only domain controller (RODC)** → pick the site, the delegated admin and the PRP accounts.",
        "**Option B, staged (two-step) install:** in **ADUC** → right-click **Domain Controllers** → **Pre-create Read-only Domain Controller account** (name, site, delegated admin). A branch tech then promotes the server and it **attaches to the pre-created account**.",
        "PowerShell: `Install-ADDSDomainController -DomainName adatum.com -ReadOnlyReplica -SiteName Branch -InstallDns` (or `Add-ADDSReadOnlyDomainControllerAccount` to pre-create).",
        "Manage the PRP: DC properties → **Password Replication Policy** tab, or `repadmin /prp`.",
    ])
    s.tag("extra", "Prerequisites, PowerShell and FAS details.")
    s.box("trap", "An RODC **can't hold FSMO roles**, can't be the first DC in a domain, and it **forwards password changes and writes** to a writable DC. It isn't \"a backup DC\". Use a second writable DC for redundancy.")

    # ---------------- SG-15 ----------------
    s.h2("SG-15  Group types and scopes (Domain Local, Global, Universal, Distribution); nesting")
    s.table(["Group type", "Has a SID?", "Use"], [
        ["**Security group**", "Yes", "Assign **permissions** (ACLs) and **user rights**; can also be mail-enabled."],
        ["**Distribution group**", "**No**", "**E-mail lists only** (Exchange/Outlook). Can't secure resources. You can convert distribution ↔ security."],
    ], widths=(1.8, 1.0, 4.7))
    s.table(["Scope", "Can contain (members)", "Can be a member of", "Permissions can be granted on", "Replication"], [
        ["**Local** (SAM, non-DC)", "Users, global and universal groups from any trusted domain; local users", "Nothing (only local)", "That one computer", "Not in AD"],
        ["**Domain Local (DL)**", "Users, computers, **global** and **universal** groups from **any domain in the forest** (or trusted forests); **DL groups from the same domain**", "Other DL groups **in the same domain** (and machine-local groups)", "Resources **in its own domain**", "Domain partition only"],
        ["**Global (G)**", "Users, computers and other **global groups from the SAME domain only**", "Universal and DL groups in any domain; global groups in the same domain", "Any domain in the forest / trusting domains", "Domain partition (group name only in GC)"],
        ["**Universal (U)**", "Users, computers, **global and universal** groups from **any domain in the forest** (**no DL**)", "Universal and DL groups in any domain", "Any domain in the forest", "**Membership stored in the GC** (more GC replication when it changes)"],
    ], widths=(1.15, 2.1, 1.65, 1.35, 1.25), size=8)
    s.box("memory", [
        "**Global = \"who\"** (people grouped by role, same domain). **Domain Local = \"what\"** (permission on a resource). **Universal = \"glue\"** between domains of a multi-domain forest; keep its membership static (SS64), because every change replicates to every GC.",
        "**Wrong-way nesting is blocked:** a DL can't go into a Global, and a Universal can't go into a Global (SS64: \"you can't add a DL to a Global\").",
    ])
    s.h3("Nesting exercise (slides p38–p41): Downtown OU (adatum.com) and BBY OU (bby.adatum.com)")
    s.table(["#", "Can you add…", "…into…", "Answer", "Reason"], [
        ["1", "ACIT Faculty Global (G, adatum)", "ACIT Global (G, adatum)", "**Yes**", "Global into global, same domain"],
        ["2", "ACIT Universal (U)", "ACIT Global (G)", "**No**", "A global accepts only same-domain users and globals"],
        ["3", "ACIT Local (DL)", "ACIT Faculty Global (G)", "**No**", "A DL can't be a member of a global"],
        ["4", "ACIT Global (G)", "ACIT Universal (U)", "**Yes**", "Global into universal is allowed"],
        ["5", "ACIT Universal (U)", "ACIT Local (DL)", "**Yes**", "Universal into DL is allowed"],
        ["6", "CIT Global (G, bby)", "ACIT Global (G, adatum)", "**No**", "Global groups only take members from their own domain"],
        ["7", "CIT Local (DL, bby)", "ACIT Local (DL, adatum)", "**No**", "A DL can only nest a DL from the **same** domain"],
        ["8", "ACIT Universal (U, adatum)", "CIT Universal (U, bby)", "**Yes**", "Universal accepts universals from any domain in the forest"],
        ["9", "ACIT Universal (U, adatum)", "CIT Local (DL, bby)", "**Yes**", "DL accepts universals from any domain (wait for GC replication, slide p42)"],
        ["10", "ACIT Global (G, adatum)", "CIT Universal (U, bby)", "**Yes**", "Universal accepts globals from any domain in the forest"],
    ], widths=(0.3, 1.9, 1.8, 0.6, 2.9), size=8)
    s.h3("Scope conversion rules")
    s.tag("extra")
    s.table(["Convert", "Allowed when…"], [
        ["Global → Universal", "The group is not itself a member of another global group"],
        ["Domain Local → Universal", "The group contains no other DL groups"],
        ["Universal → Global", "It contains no universal groups (and no members from other domains)"],
        ["Universal → Domain Local", "Always"],
        ["Global ↔ Domain Local", "Not directly. Go through Universal."],
    ], widths=(2.2, 5.3))
    s.bullets([
        "**Group membership is evaluated at logon** (it's in the Kerberos token), so users must **log off and on** after being added (SS64).",
        "A user in more than about **1,015 groups** can't log on (token size limit).",
        "Changing a group needs Account Operators, Domain Admins, Enterprise Admins, or delegated rights.",
        "PowerShell: `New-ADGroup -Name \"ACL_Sales_Read\" -GroupScope DomainLocal -GroupCategory Security -Path \"OU=Groups,DC=adatum,DC=com\"`; `Add-ADGroupMember ACL_Sales_Read -Members Sales,Auditors`; `Get-ADGroupMember`, `Get-ADPrincipalGroupMembership user1`.",
    ])

    # ---------------- SG-16 ----------------
    s.h2("SG-16  IGDLA (AGDLP / AGUDLP)")
    s.p("**I**dentities (user and computer accounts) → **G**lobal groups (by role or department) → **D**omain **L**ocal groups (by resource and access level) → **A**ccess / permissions assigned to the DL. In multi-domain forests, add **U**niversal groups between global and DL (**IGUDLA / AGUDLP**).")
    s.code("""Users: Ann, Bob  ->  G_Sales (Global)        \\
Users: Cat       ->  G_Auditors (Global)     -->  ACL_Sales_Read (Domain Local)  -->  NTFS Read on \\\\SVR6\\Sales
                                              /
Multi-domain:   G_Sales(adatum) + G_Sales(bby) -> U_Sales_All (Universal) -> ACL_Sales_Read (DL)""", title="Slide example: ACL_Sales_Read (DL) contains Sales and Auditors (Global)")
    s.bullets([
        "**Why bother:** it separates *people* from *resources*. When staff change roles, you edit one global group, never the ACLs. SS64 example: 5 departments × 15 resources managed directly = 75 permission entries, but with role and resource groups it drops to **28**.",
        "**Never assign permissions directly to users**, and never put users directly in DL groups in large environments.",
        "Naming conventions help: `G_` / `GG_` for global, `DL_` / `ACL_` for domain local, `U_` for universal.",
    ])
    s.box("instructor", "The share-permission lab follows IGDLA: domain local groups **Faculty** (F1) and **Students** (S1, S2) are granted NTFS and share permissions on the Faculty and Assignment folders (Part 4).")

    s.h3("Week 3–4 discussion questions: model answers")
    s.tag("model")
    s.qa([
        ["What is AD DS and why do we need it?", "A central identity and policy store. Without it, every server has its own local accounts (no single sign-on, no central password policy, no Group Policy, no delegation). With it, there's one logon for all resources, central security policy, scalable delegation and auditing."],
        ["Does Linux have AD DS?", "Not natively. **Samba 4** can act as an AD-compatible DC (LDAP, Kerberos, DNS, Group Policy basics). **FreeIPA / Red Hat IdM** is the Linux-native equivalent (LDAP + Kerberos + DNS + CA). Linux clients join AD with `realmd`/`sssd` (`realm join adatum.com`)."],
        ["Network bridge vs switch?", "Both are Layer-2 devices that forward frames by MAC address. A bridge typically joins two segments in software (e.g. VMware *bridged* networking puts a VM on the host's LAN). A switch is a multi-port hardware bridge (ASICs, VLANs, full duplex on each port), giving each port its own collision domain."],
        ["How do you determine FSMO holders, and transfer or seize them?", "`netdom query fsmo`, or `Get-ADDomain` / `Get-ADForest`, or the three consoles. Transfer with `Move-ADDirectoryServerOperationMasterRole` or the consoles. Seize with `-Force` or `ntdsutil roles seize` only when the holder is permanently lost (see SG-10)."],
        ["Group nesting best practices?", "Follow IGDLA/AGUDLP; keep universal membership static (nest globals inside it); avoid deep or circular nesting; use clear naming; document groups and review them regularly; never grant permissions to users directly."],
    ], title=None)
