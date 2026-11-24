"""Front matter, Part 1 (platform: SG 1-3) and Part 2 (accounts & SIDs: SG 4-5)."""
from lib import SUPP_TAG, EXTRA_TAG, MODEL_TAG

STUDY_GUIDE_MAP = [
    ("1", "Windows Server 2016 / 2019 / 2022 upgrade", "Part 1", "Partial + Supplemental"),
    ("2", "New features: Linux Secure Boot, PowerShell Direct, Shielded VM / Host Guardian Service, ReFS", "Part 1", "Course"),
    ("3", "Standard vs Datacenter edition", "Part 1", "Course"),
    ("4", "Account types; built-in user accounts", "Part 2", "Partial + Supplemental"),
    ("5", "Command to make a cloned machine generate its own SID", "Part 2", "Course"),
    ("6", "What is a Domain Controller; how to deploy AD DS", "Part 3", "Course"),
    ("7", "How many PDC Emulators are required", "Part 3", "Course + Supplemental"),
    ("8", "AD DS database (partitions), site, trees, forests", "Part 3", "Course"),
    ("9", "Global Catalog; recommended number of GCs", "Part 3", "Course"),
    ("10", "FSMO roles: list and explain each", "Part 3", "Partial + Supplemental"),
    ("11", "Domain / forest functional levels; when to raise the DFL", "Part 3", "Course"),
    ("12", "Adding attributes to an AD object changes the schema", "Part 3", "Course"),
    ("13", "FQDN", "Part 3", "Course"),
    ("14", "RODC: what, why, how to deploy", "Part 3", "Course + Supplemental"),
    ("15", "Domain local, global, universal, distribution groups; nesting", "Part 3", "Course"),
    ("16", "IGDLA", "Part 3", "Course"),
    ("17", "How to share a folder", "Part 4", "Course"),
    ("18", "Nano Server: benefits, services, offline domain join (djoin), scenarios", "Part 4", "Supplemental"),
    ("19", "How to create / deploy Nano Server", "Part 4", "Supplemental"),
    ("20", "NTFS basic permissions (Full Control vs Modify, etc.)", "Part 4", "Course"),
    ("21", "Assigning appropriate permissions", "Part 4", "Course"),
    ("22", "IPv4 / IPv6; private vs public IP", "Part 5", "Course"),
    ("23", "Storage pool; media types; parity vs two-way vs three-way mirror", "Part 6", "Course"),
    ("24", "Block-level vs file-level storage", "Part 6", "Course"),
    ("25", "RAID 0 / 1 / 5", "Part 6", "Course"),
    ("26", "GPO and why we use it", "Part 7", "Supplemental"),
    ("27", "Security policies: default values", "Part 7", "Supplemental (some course values)"),
    ("28", "User Rights Assignment, Security Options, Security Templates, Audit Policy", "Part 7", "Supplemental"),
    ("29", "DHCP, its services, scope", "Part 8", "Course"),
    ("30", "DHCP lease generation (DORA)", "Part 8", "Course"),
    ("31", "When clients renew", "Part 8", "Course"),
    ("32", "Create a scope; DHCP proxy (relay); superscope", "Part 8", "Course"),
    ("33", "DNS; zones", "Part 9", "Course"),
    ("34", "Split DNS; DNS port", "Part 9", "Course"),
    ("35", "Protecting DNS; records; nslookup", "Part 9", "Course"),
    ("36", "Virtualization Type I vs Type II", "Part 10", "Course + Supplemental"),
    ("37", "Virtual switch", "Part 10", "Course"),
    ("38", "VPN protocols and ports", "Part 11", "Supplemental"),
]


def front_matter(s):
    d = s.doc
    t = d.add_paragraph()
    t.alignment = 1
    from docx.shared import Pt, RGBColor
    r = t.add_run("WINDOWS SERVER ADMINISTRATION")
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor.from_string("1F3864")
    t2 = d.add_paragraph()
    t2.alignment = 1
    r = t2.add_run("ACIT 3420 — Final Exam Comprehensive Cheat Sheet")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor.from_string("1F4E79")
    t3 = d.add_paragraph()
    t3.alignment = 1
    r = t3.add_run("Windows Server 2016 / 2019 / 2022  •  AD DS  •  File Services  •  Storage  •  Group Policy  •  DHCP  •  DNS  •  Hyper-V  •  Remote Access")
    r.font.size = Pt(9)
    r.italic = True

    s.p("Built from every file in `Window-server-admin`: the Final Exam Study Guide (the blueprint, so Parts 1–11 follow its 38 items in order), "
        "the lecture slide decks, handouts and articles, the lab instructions and lab videos (transcribed, with on-screen text read from video frames), "
        "and the weekly discussion prompts. Study-guide item numbers appear as **SG-n** in every heading.")

    s.h3("How to read this document")
    s.table(
        ["Marker", "Meaning"],
        [
            ["No tag", "Content taken from course files (slides, labs, videos, handouts). A gray Sources: line names the files."],
            [SUPP_TAG, "The study guide lists this topic, but no lecture, lab or video covering it was in the course folder yet (e.g. Week 12 Group Policy, Nano Server, VPN). Written from standard Microsoft documentation and practice."],
            [EXTRA_TAG, "Extra detail added to a topic the course does cover (e.g. exact upgrade paths, cmdlet syntax not shown on a slide)."],
            [MODEL_TAG, "The course asked the question (discussion forum, lab review, slide quiz) but the folder had no answer key, so this is a written model answer."],
            ["EXAM TRAP box (red)", "A distinction that is easy to get wrong on a multiple-choice or short-answer question."],
            ["INSTRUCTOR CALLOUT box (blue)", "Something the instructor stressed verbally in a lecture or lab video."],
            ["TROUBLESHOOTING box (orange)", "A symptom, its cause and the fix, mostly from problems hit in the labs."],
            ["KEY TAKEAWAY / MEMORY AID (green / purple)", "Summary lines and mnemonics to memorise."],
            ["Lab Questions & Answers (purple table)", "Every question asked in a lab handout or lab video, with its answer."],
        ],
        widths=(2.3, 5.2),
    )

    s.h3("Course material not yet unlocked by the instructor")
    s.p("These study-guide topics had no lecture, lab or video in the course folder when this sheet was built. They're still fully covered, but every such section carries the red tag. **Check them against the instructor's slides once they're released** and trust the instructor's version if anything differs.", size=9)
    s.table(["Locked / missing material", "Study-guide items affected", "Where covered here"], [
        ["Week 12 Group Policy lecture and lab (only discussion titles available)", "SG-26, SG-27, SG-28", "Part 7"],
        ["Week 15 Maintenance, Monitoring and Hybrid Cloud (only discussion titles)", "— (discussion only)", "Part 12"],
        ["Makeup: Server Hardening and Security bonus (titles only)", "— (discussion only)", "Part 7 (model answers)"],
        ["Remote Access / VPN lecture", "SG-38", "Part 11"],
        ["Nano Server lecture (slides only mention it)", "SG-18, SG-19", "Part 4"],
        ["Detailed FSMO role explanations and account types (slides only list them)", "SG-4, SG-10 (partial)", "Parts 2–3"],
        ["Exact in-place upgrade paths", "SG-1 (partial)", "Part 1"],
    ], widths=(3.6, 1.9, 2.0), header_fill="B03A2E", zebra="FBE5E1")

    s.h3("Study Guide coverage map (exam blueprint order)")
    s.table(["SG #", "Study-guide topic", "Where", "Coverage"],
            [list(r) for r in STUDY_GUIDE_MAP], widths=(0.45, 4.6, 0.7, 1.75), size=8)

    s.h3("Table of contents")
    s.p("Word fills in page numbers when the document opens. If you see a placeholder instead, right-click it and choose Update Field, then Update entire table.",
        size=8, italic=True, color="7F7F7F")
    s.toc()


def part1(s):
    s.part("PART 1 — WINDOWS SERVER PLATFORM (SG-1 to SG-3)")
    s.src("Windows Server Introduction slides; Module 2A Installation and Configuration slides; Lab 1A/1B; Evaluation-period handout; Server Core video; Lenovo x3650 M5 IMM handout; Week 1–2 discussion prompts.")

    s.h3("Foundations: what makes a server a server (Intro module)")
    s.bullets([
        "**Server** = hardware + OS that provides services (roles) to clients: file, print, web (IIS), identity (AD DS), DNS, DHCP, virtualization (Hyper-V), remote access, and so on.",
        "**Hardware design goals:** performance, availability (redundancy), cost. A server has redundant PSUs (at least 2), ECC RAM, hot-swap disks, multiple NICs, and out-of-band management.",
        "**CPU:** server CPUs are Intel Xeon or AMD EPYC. CISC (x86/x64) vs RISC (ARM, used in some cloud servers). 32-bit addresses up to 4 GB RAM; 64-bit addresses far more (the slide says 1 TB+). **Every Windows Server since 2008 R2 is 64-bit only.**",
        "**RAM:** ECC (Error-Correcting Code) RAM detects and corrects single-bit errors, which is why servers use it.",
        "**Storage:** DAS, NAS, SAN, and Storage Spaces Direct (S2D). See Part 6.",
        "**NICs:** 1 / 10 / 25 / 100 GbE; RDMA NICs (SMB Direct) offload transfers from the CPU; NIC teaming adds redundancy and bandwidth.",
        "**KVM switch:** one keyboard, video and mouse shared across many servers in a rack. **IMM / iDRAC / iLO:** out-of-band management controller (lab handout: Lenovo x3650 M5 **Integrated Management Module**, configured from UEFI setup with an IP address so the server can be managed even when the OS is down).",
        "**Firmware:** BIOS (legacy, MBR boot) vs **UEFI** (GPT boot, Secure Boot, faster, >2 TB boot disks). Gen 2 Hyper-V VMs use UEFI.",
        "**Servicing channels:** **LTSC** (Long-Term Servicing Channel: new release every 2–3 years, 5 years mainstream + 5 extended = 10 years support; Desktop Experience available) vs **SAC** (Semi-Annual Channel: Server Core only, 18-month support; discontinued after version 20H2). Windows Server 2016/2019/2022/2025 are LTSC releases.",
    ])

    # ---------------- SG-1 ----------------
    s.h2("SG-1  Windows Server 2016 / 2019 / 2022 — upgrading")
    s.p("An **upgrade** replaces the OS but keeps roles, settings, files and apps. A **clean install** wipes the target volume. A **migration** moves roles and data from an old server to a new one, which is the preferred approach for domain controllers and production servers.")
    s.h3("What the course said")
    s.bullets([
        "**AD DS upgrade:** DCs running **Windows Server 2008 R2 SP1, 2012 and 2012 R2** can be upgraded or replaced by Windows Server 2019 DCs. Adding a newer DC runs `adprep /forestprep` and `/domainprep` automatically (2012+).",
        "**Cluster OS Rolling Upgrade (new in 2016):** upgrade Hyper-V / Scale-Out File Server cluster nodes one at a time with no downtime. The cluster runs in mixed mode until you run `Update-ClusterFunctionalLevel`.",
        "**Pre-installation checklist (Module 2A):** disconnect the UPS serial/USB cable (setup may misdetect it), back up the server, disable antivirus, have the mass-storage (RAID/HBA) drivers ready, and check hardware compatibility and minimum requirements.",
        "**Post-installation tasks:** set a static IP, rename the computer, join the domain, set the time zone, run Windows Update, add roles and features, enable Remote Desktop, and configure the firewall.",
        "**Install options are fixed at install time:** Server Core vs Desktop Experience.",
    ])
    s.box("trap", [
        "Since **Windows Server 2016** you **cannot switch** between Server Core and Desktop Experience after installation, and an in-place upgrade cannot change the install option either. You must reinstall. (In 2012/2012 R2 you could add or remove `Server-Gui-Shell` / `Server-Gui-Mgmt-Infra`.) This is the Lab 1B question: \"Can you install Server Core and later upgrade it to Desktop Experience?\" Answer: **No.**",
    ])
    s.h3("Upgrade paths and rules")
    s.tag("extra", "Exact paths come from Microsoft's upgrade matrix; the slides only cover the AD DS case.")
    s.table(["Upgrade FROM", "Supported in-place upgrade TO", "Notes"], [
        ["Windows Server 2012 R2", "2016, 2019 (2025 also accepts 2012 R2)", "The N+2 rule: at most two versions in one jump (2025 relaxes this)"],
        ["Windows Server 2016", "2019, 2022", ""],
        ["Windows Server 2019", "2022, 2025", ""],
        ["Windows Server 2022", "2025", ""],
        ["2008 / 2008 R2 / 2012", "No direct path to 2019/2022", "Upgrade in steps (e.g. 2012 → 2016 → 2019), or migrate"],
    ], widths=(1.7, 2.6, 3.2))
    s.bullets([
        "**Edition rules:** Standard → Standard or Datacenter; Datacenter → Datacenter only (never downgrade an edition). Evaluation → licensed: `DISM /online /Set-Edition:ServerStandard /ProductKey:XXXXX-... /AcceptEula`. List options with `DISM /online /Get-TargetEditions`.",
        "**Architecture:** x64 → x64 only. No 32-bit server since 2008.",
        "**Language:** must match the installed OS language.",
        "**How:** mount the ISO, run `setup.exe`, and pick \"Keep files, settings, and apps\" (upgrade) or \"Nothing\" (clean install).",
        "**Domain controllers:** best practice is not to upgrade in place. Add a new DC, let it replicate, transfer the FSMO roles, then demote the old DC (`Uninstall-ADDSDomainController`) and raise the functional levels.",
        "**Migration tools:** Storage Migration Service (2019+, through Windows Admin Center), Windows Server Migration Tools, the DHCP export/import cmdlets, and ADMT for cross-forest moves.",
    ])

    # ---------------- SG-2 ----------------
    s.h2("SG-2  New features: Linux Secure Boot, PowerShell Direct, Shielded VMs / HGS, ReFS")
    s.src("Module 2A slides (What's new in 2016/2019/2022); Hyper-V lecture slides and lecture video; Server Storage slides.")
    s.table(["Feature", "What it is / why it matters", "Key facts"], [
        ["**Linux Secure Boot** (2016)", "Gen 2 Linux VMs can boot with UEFI Secure Boot. The firmware checks the signatures of the boot loader and kernel drivers, which blocks rootkits and bootkits.",
         "Gen 2 VMs only. Select the **Microsoft UEFI Certificate Authority** template (the default Microsoft Windows template does not boot Linux):\n`Set-VMFirmware VM1 -SecureBootTemplate MicrosoftUEFICertificateAuthority`"],
        ["**PowerShell Direct** (2016)", "Run PowerShell inside a VM from its Hyper-V host over the VMBus, with **no network connection, firewall rule or remote-management configuration**.",
         "`Enter-PSSession -VMName VM1`\n`Invoke-Command -VMName VM1 -ScriptBlock {...}`\nHost and guest must be 2016+ / Windows 10+; you need Hyper-V admin rights on the host plus guest credentials; the VM must be running locally."],
        ["**Shielded VMs + Host Guardian Service** (2016)", "Protect a VM from a malicious or compromised fabric administrator. The VM's disks are BitLocker-encrypted with a vTPM, and it only starts on hosts that HGS has attested as healthy.",
         "Gen 2 VM + vTPM + BitLocker. HGS attestation modes: **TPM-trusted** (strongest), **Host-key** (2019+), Admin-trusted (AD group, deprecated in 2019). A stolen VHDX will not run on another host. 2019 added Linux shielded VMs."],
        ["**ReFS** (Resilient File System)", "A file system built for integrity and scale: checksums, integrity streams, allocate-on-write (no in-place overwrite), online scrubbing and salvage (no `chkdsk` needed).",
         "Max volume about 2^78 bytes (the slide figure); no boot volume; no EFS, quotas or compression. Block cloning makes VHDX checkpoint merges and fixed-VHDX creation fast. Deduplication on ReFS since 2019. Format: `Format-Volume -DriveLetter E -FileSystem ReFS`"],
    ], widths=(1.35, 3.0, 3.15))
    s.h3("What's new, by version (lecture lists)")
    s.table(["2016", "2019", "2022"], [
        ["PowerShell Direct\nShielded VMs / HGS\nNano Server\nWindows/Hyper-V containers + Docker\nStorage Spaces Direct (S2D)\nStorage Replica\nRolling cluster upgrade\nHot add/remove memory and NICs\nNested virtualization\nWindows Defender built in\nLinux Secure Boot\nPowerShell 5.x",
         "System Insights (predictive analytics)\nHybrid Azure: Azure Backup, File Sync, Azure Network Adapter (point-to-site VPN)\nWindows Admin Center\nDefender ATP\nStorage Migration Service\nKubernetes and Linux containers\nServer Core App Compatibility Feature on Demand\nWSL (Windows Subsystem for Linux)\nTwo-node cluster with a USB/file-share witness\nS2D up to 4 PB; ReFS dedup\nCore image 5 GB → 1.58 GB",
         "**Secured-core server:** TPM 2.0, DRTM (System Guard), DMA protection, VBS, HVCI, Credential Guard\nTLS 1.3 on by default\nDNS-over-HTTPS client\nSMB AES-256 encryption; SMB compression\nAzure Arc, hotpatch (Azure Edition)\nSMB over QUIC (Azure Edition)\nContainers about 40% smaller, faster start\nNested virtualization on AMD CPUs"],
    ], widths=(2.5, 2.5, 2.5), first_col_bold=False)
    s.box("instructor", [
        "In the Hyper-V lecture video the instructor demonstrated PowerShell Direct from the host with `Enter-PSSession -VMName` and contrasted it with normal remoting (`Enter-PSSession -ComputerName DC2` from DC1), which needs the network and WinRM. **PowerShell Direct goes host → VM only; it cannot go VM → host or VM → VM.**",
    ])

    # ---------------- SG-3 ----------------
    s.h2("SG-3  Standard vs Datacenter (and the other editions)")
    s.src("Module 2A slide \"Standard vs Datacenter\" (p7), Editions slides; Week 1–2 discussion bonus scenarios.")
    s.table(["Feature (2022 slide)", "Standard", "Datacenter"], [
        ["Best for", "Physical or lightly virtualized environments", "Highly virtualized data centers and cloud"],
        ["Licensing model", "Core-based + CALs", "Core-based + CALs"],
        ["Max users", "Based on CALs", "Based on CALs"],
        ["Max sockets / cores", "64 sockets / unlimited cores", "64 sockets / unlimited cores"],
        ["Max RAM", "48 TB", "48 TB"],
        ["**OS environments (VMs) per license**", "**2 VMs + 1 Hyper-V host**", "**Unlimited VMs**"],
        ["Hyper-V isolated containers", "2", "Unlimited"],
        ["Windows Server containers", "Unlimited", "Unlimited"],
        ["Can be a Hyper-V host / join a domain", "Yes / Yes", "Yes / Yes"],
        ["Storage Spaces Direct, Shielded VMs/HGS, Software-Defined Networking", "No", "Yes"],
        ["Storage Replica", "Limited (1 partnership, 1 volume up to 2 TB)", "Full"],
    ], widths=(2.6, 2.4, 2.5))
    s.tag("extra", "The last two rows and the licensing details below are supplemental.")
    s.bullets([
        "**Core licensing:** license every physical core, with a minimum of 8 cores per CPU and 16 per server. Every user or device also needs a **CAL** (User CAL or Device CAL). Standard lets you stack licenses: each extra full license covers 2 more VMs.",
        "**Essentials:** small business, **25 users / 50 devices**, single CPU (up to 10 cores), no CALs needed.",
        "**Datacenter: Azure Edition:** runs on Azure / Azure Stack HCI and adds **Hotpatch** (patch without rebooting), **SMB over QUIC** and **Azure Extended Network**.",
        "**Hyper-V Server** (free, no GUI, menu-driven like sconfig, Type 1 hypervisor; the slide lists 64 sockets / 24 TB). The **last free release was Hyper-V Server 2019**; Microsoft did not ship a 2022 version.",
        "**Storage Server** (OEM-only): Workgroup edition = 50 users, 1 CPU core, 32 GB RAM; Standard edition can run DNS and DHCP but **not AD DS, AD CS or the full File Server roles** (slide).",
    ])
    s.box("trap", [
        "- Standard and Datacenter have the **same scalability limits** (sockets, RAM, cores). The exam difference is **virtualization rights** (2 VMs vs unlimited) plus the Datacenter-only features (S2D, Shielded VMs, SDN).",
        "- Both editions can be domain controllers, both can be Hyper-V hosts, and both need CALs.",
    ])
    s.h3("Discussion bonus scenarios: choose the edition and install option")
    s.tag("model")
    s.table(["Scenario (Module 2A discussion)", "Best choice", "Why"], [
        ["Small legal firm, about 20 staff, one server for files, printing and a database", "**Essentials** (or Standard if it grows past 25 users)", "Under 25 users / 50 devices, no CALs needed, lowest cost."],
        ["Branch office running AD DS, DNS and DHCP, managed remotely from head office, minimal hardware", "**Standard, Server Core** (or an RODC on Core)", "Core has a smaller attack surface, fewer patches, and needs less RAM and disk; it is managed with RSAT, WAC or PowerShell remoting."],
        ["IIS web server that must use minimal resources", "**Server Core** (Nano Server as a container image for modern apps)", "IIS runs on Core and needs no GUI."],
        ["Psychology department with 122 users, a few servers, 1–2 VMs", "**Standard** + 122 User CALs", "Too many users for Essentials; light virtualization doesn't justify Datacenter."],
        ["Private cloud with dozens of VMs per host, S2D, shielded VMs", "**Datacenter**", "Unlimited VMs; S2D, HGS and SDN are Datacenter-only."],
    ], widths=(2.6, 1.9, 3.0))

    # --------- Installation, requirements, management ---------
    s.h3("Installation options and minimum requirements")
    s.table(["Item", "Server Core", "Desktop Experience"], [
        ["What you get", "No GUI shell: command prompt, PowerShell, `sconfig`. Smaller footprint, fewer patches and reboots, smaller attack surface.", "Full GUI, Server Manager, MMC consoles. Easier to use, but larger and needs more patching."],
        ["Typical roles", "AD DS, DNS, DHCP, File Server, Hyper-V, IIS", "Remote Desktop Session Host, apps that need a GUI, admin jump boxes"],
        ["Min CPU", "1.4 GHz, 64-bit, NX/DEP, CMPXCHG16b, LAHF/SAHF, PrefetchW, SLAT (EPT/NPT)", "Same"],
        ["Min RAM", "**512 MB** (800 MB to install in a VM)", "**2 GB**"],
        ["Min disk", "**32 GB**", "32 GB (more recommended; Lab 1B used 120 GB)"],
        ["Other", "Gigabit Ethernet; UEFI 2.3.1c + Secure Boot and TPM 2.0 for some security features", "Same"],
    ], widths=(1.2, 3.2, 3.1))
    s.box("instructor", "Lab 1B VM settings: **2 GB RAM, 120 GB disk, Desktop Experience**, and enable **VT-x/EPT (Intel) or AMD-V/RVI** in the VMware processor settings so Hyper-V can be nested later. Use a **complex password**, because AD DS promotion fails otherwise.")
    s.h3("Roles vs role services vs features")
    s.table(["Term", "Definition", "Example"], [
        ["Role", "The server's main function or service for the network", "AD DS, DNS Server, DHCP Server, Hyper-V, File and Storage Services, Remote Access, IIS"],
        ["Role service", "A sub-component of a role", "Remote Access → DirectAccess and VPN (RAS), Routing; File Services → DFS Namespaces, iSCSI Target Server"],
        ["Feature", "Supporting capability, not a primary service", "Failover Clustering, BitLocker, .NET, Telnet Client, RSAT, Windows Server Backup"],
    ], widths=(1.2, 3.0, 3.3))
    s.code("""Get-WindowsFeature | Where Installed            # list installed roles/features
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-WindowsFeature DHCP, DNS -IncludeManagementTools -ComputerName CA-VAN-SVR2
Uninstall-WindowsFeature Web-Server -Remove        # -Remove deletes the payload (Features on Demand)
Add-WindowsFeature DHCP                            # older alias used on the DHCP slide""", title="PowerShell: roles and features")

    s.h3("Management tools (Module 2A)")
    s.table(["Tool", "Use / notes"], [
        ["Server Manager", "Add roles and features, manage several servers (All Servers → Add Servers). Can install roles on remote servers."],
        ["RSAT", "Remote Server Administration Tools for Windows 10/11 clients (Features on Demand)."],
        ["Windows Admin Center (WAC)", "Browser-based management (2019+), manages Core servers and hybrid Azure."],
        ["PowerShell remoting / WinRM", "`Enter-PSSession -ComputerName X`, `Invoke-Command`. WinRM listens on TCP 5985 (HTTP) / 5986 (HTTPS). `Enable-PSRemoting` (on by default on servers)."],
        ["PowerShell Direct", "Host → VM over the VMBus (see SG-2)."],
        ["Remote Desktop", "TCP **3389**. Enable it in `sconfig` option 7 or System Properties."],
        ["MMC snap-ins", "ADUC `dsa.msc`, DNS `dnsmgmt.msc`, DHCP `dhcpmgmt.msc`, GPMC `gpmc.msc`, Sites and Services `dssite.msc`, Domains and Trusts `domain.msc`, ADSI Edit `adsiedit.msc`, Computer Management `compmgmt.msc`, Disk Management `diskmgmt.msc`."],
        ["Core built-in tools (slide)", "`cmd.exe`, `powershell.exe`, `sconfig.cmd`, `regedt32.exe`, `msinfo32.exe`, `taskmgr.exe`, `notepad.exe`."],
        ["Group Policy", "Configure many servers at once. **Not supported on Nano Server.**"],
    ], widths=(1.8, 5.7))
    s.box("note", "Remote management needs firewall exceptions: Remote Event Log Management, Remote Service Management, Windows Remote Management and File and Printer Sharing (ICMP echo), depending on the tool.")

    s.h3("Server Core with sconfig (Server Core lab video)")
    s.table(["sconfig option", "What it does"], [
        ["1", "Domain / workgroup membership (join a domain, restart)"],
        ["2", "Computer name"],
        ["3", "Add a local administrator"],
        ["4", "Configure remote management (WinRM; allow ping)"],
        ["5–6", "Windows Update settings / install updates"],
        ["7", "Remote Desktop (enable or disable)"],
        ["8", "Network settings: static IP, mask, gateway, **DNS server**"],
        ["9", "Date and time"],
        ["13–15", "Restart / shut down / exit to the command line (PowerShell on 2022)"],
    ], widths=(1.2, 6.3))
    s.code("""netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv4:8,any dir=in action=allow
Enter-PSSession -ComputerName CA-VAN-SVR9          # prompt becomes [CA-VAN-SVR9.Adatum.com]: PS C:\\>
New-NetFirewallRule -DisplayName "Allow ICMPv4" -Protocol ICMPv4 -IcmpType 8 -Direction Inbound -Action Allow""",
           title="Server Core: allow ping, then manage it remotely")
    s.box("trouble", [
        "**Symptom:** you can't ping the new Server Core (or any new server) VM. **Cause:** Windows Firewall blocks inbound ICMPv4 echo by default. **Fix:** add the ICMP rule above (the video did exactly this), then add the server to Server Manager → All Servers and manage it remotely.",
    ])

    s.h3("Evaluation period and activation (lab handout)")
    s.code("""slmgr -dlv        # detailed license info: remaining time, rearm count
slmgr -dli        # basic license info
slmgr -rearm      # reset the 180-day evaluation clock (up to 6 times, about 3 years total), then Restart-Computer
slmgr /ipk <key>  # install a product key;   slmgr /ato  = activate online
SLUI 4            # telephone activation""", title="Software Licensing Manager")

    s.h3("Lab 1A / 1B: Questions & Answers")
    s.qa([
        ["Why choose \"I will install the OS later\" and the correct guest OS profile in VMware?", "VMware Easy Install skips choices like the edition. The guest profile sets the right virtual hardware and drivers; a wrong profile causes video and driver problems."],
        ["Where should VM files be stored?", "In a dedicated local folder, **not OneDrive** (syncing corrupts or slows the VMDKs). Splitting the virtual disk into multiple files makes it easier to move and copy."],
        ["Why add a TPM to the Windows 11 VM?", "Windows 11 requires TPM 2.0 and Secure Boot (UEFI). Windows 10 needs only TPM 1.2+ if you want BitLocker."],
        ["The VM booted to PXE / \"no operating system\". Why?", "You didn't press a key fast enough at \"Press any key to boot from CD/DVD\", so firmware fell through to network (PXE) boot. Restart and press a key."],
        ["Which partitions does Windows Setup create on a UEFI/GPT disk?", "EFI System Partition (about 100 MB, FAT32), MSR (Microsoft Reserved, 16 MB), the Windows (C:) partition, and a Recovery partition."],
        ["How do you list installed updates?", "`wmic qfe list` (or `Get-HotFix`)."],
        ["Can Server Core be upgraded to Desktop Experience later?", "**No** (2016 and later). Reinstall."],
        ["Why does the lab require a complex Administrator password?", "Password complexity is enforced and the account becomes the domain admin when you promote to a DC. A weak password stops `dcpromo` / `Install-ADDSForest`."],
        ["Bridged vs NAT vs Host-only (VMware)?", "Bridged: the VM joins the host's physical LAN with its own IP. NAT: the VM shares the host's IP and reaches the Internet, but outsiders can't reach it without port forwarding. Host-only: a private network with the host only, no Internet (the course uses **VMnet9** host-only for the lab domain)."],
        ["How do you test connectivity?", "`ping 8.8.8.8` (Internet over IP), `ping google.com` (DNS), `ipconfig /all`."],
    ])
    s.box("trouble", [
        "**VMware Workstation install error 1327 (invalid drive):** a stale install path in the registry. Fix the value at `HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\VMware\\VMwarePlayer\\InstallPath64` so it points to a valid drive (Error 1327 lab handout), then rerun setup.",
        "**12th-gen and later Intel CPUs (Lab 1B note):** if Hyper-V or VT-x is unavailable inside VMware, make sure Windows features like VBS, Memory Integrity and Hyper-V on the host aren't taking the hypervisor, and enable VT-x/EPT in the VM's processor settings.",
    ])

    s.h3("Week 1–2 discussion questions: model answers")
    s.tag("model")
    s.qa([
        ["What is NAT?", "Network Address Translation rewrites private source IPs (RFC 1918) to a public IP at the router or firewall, so many hosts share one public address. PAT/overload also tracks port numbers. It saves IPv4 addresses and hides internal addressing, but breaks end-to-end connectivity (port forwarding is needed for inbound traffic)."],
        ["Minimum requirements for Server 2016 to 2025?", "64-bit 1.4 GHz CPU with NX, SLAT and SSE4.2 (2025 also needs POPCNT/SSE4.2); RAM: Core 512 MB, Desktop Experience 2 GB; disk 32 GB; Gigabit NIC. 2025 recommends UEFI, Secure Boot and TPM 2.0."],
        ["What's new since 2019?", "2022: Secured-core, TLS 1.3, DoH, SMB AES-256 and compression, Azure Arc, hotpatch (Azure Edition), smaller containers. 2025: hotpatching through Azure Arc, AD 32K database pages and functional level 10, NVMe performance, SMB over QUIC in all editions, GPU partitioning, in-place upgrade from 2012 R2."],
        ["Virtualization Type I vs Type II?", "See SG-36 (Part 10)."],
        ["What is a SID and its components?", "See SG-5 (Part 2)."],
    ], title=None)


def part2(s):
    s.part("PART 2 — ACCOUNTS, SIDs AND CLONING (SG-4, SG-5)")
    s.src("SID-myth article (Russinovich); PsTools / PsGetSid lab video; Lab 1B Sysprep steps; VirtualBox clone note; Module 2A Sysprep slide; DHCP slide p12 (ADUC Users container groups); Lab 2A review questions.")

    s.h2("SG-4  Account types and built-in user accounts")
    s.tag("supp", "The course mentions accounts only in passing (local Administrator, domain admin vs domain user, ADUC default groups). This section fills the gaps.")
    s.table(["Account type", "Stored in", "Scope / use"], [
        ["**Local user account**", "SAM database on that computer (`%SystemRoot%\\System32\\config\\SAM`)", "Logs on only to that machine. Member servers and clients have them; **DCs have no local SAM accounts** (except the DSRM admin)."],
        ["**Domain user account**", "AD DS database `ntds.dit` on every DC", "Logs on anywhere in the domain or trusted domains; authenticated by Kerberos through a DC."],
        ["**Built-in account**", "Created by Windows at install / promotion", "Administrator, Guest, krbtgt, DefaultAccount (below)."],
        ["**Computer account**", "AD (Computers container by default), named `NAME$`", "Created when a machine joins the domain. It has a password that changes automatically every 30 days and is used for the secure channel. A broken secure channel gives the \"trust relationship\" error."],
        ["**Service accounts**", "Local or AD", "LocalSystem, LocalService, NetworkService; **sMSA** (2008 R2), **gMSA** (2012+, password managed by AD, usable on many servers), virtual accounts `NT SERVICE\\<svc>`."],
        ["**Group account**", "SAM (local groups) or AD", "Collects users for assigning rights and permissions (Part 3, SG-15)."],
    ], widths=(1.6, 2.4, 3.5))
    s.table(["Built-in user account", "RID", "Default state", "Purpose / best practice"], [
        ["Administrator", "500", "Enabled", "Full control. **Rename it, use a strong password, and use named admin accounts instead.** It can't be deleted or locked out (locally)."],
        ["Guest", "501", "**Disabled**", "Anonymous-style access with no password. Leave it disabled."],
        ["krbtgt (domain only)", "502", "Disabled", "The KDC service account; its password hash signs all Kerberos tickets (TGTs). Reset it twice after a compromise."],
        ["DefaultAccount", "503", "Disabled", "\"Default System Managed Account\" used by the OS."],
        ["WDAGUtilityAccount", "504", "Disabled", "Defender Application Guard (clients)."],
        ["New user accounts", "**1000+** (local) / 1100+ (domain)", "—", "RIDs are issued by the **RID Master** in pools of 500 per DC."],
    ], widths=(1.6, 1.0, 1.1, 3.8))
    s.table(["Well-known identity", "SID", "Meaning"], [
        ["Everyone", "S-1-1-0", "All users, including Guest (Anonymous Logon is excluded by default since Server 2003)"],
        ["Authenticated Users", "S-1-5-11", "Anyone who logged on with valid credentials"],
        ["SYSTEM (LocalSystem)", "S-1-5-18", "The OS itself; the most powerful local identity"],
        ["LOCAL SERVICE / NETWORK SERVICE", "S-1-5-19 / S-1-5-20", "Low-privilege service identities (NETWORK SERVICE uses the computer account on the network)"],
        ["BUILTIN\\Administrators / Users", "S-1-5-32-544 / -545", "Built-in local groups"],
        ["Domain Admins / Enterprise Admins", "<domainSID>-512 / <rootSID>-519", "Admins of one domain / of the whole forest"],
    ], widths=(2.2, 1.8, 3.5))
    s.h3("Default groups in the ADUC Users and Builtin containers (DHCP slide p12)")
    s.table(["Group", "Scope", "Purpose"], [
        ["Domain Admins", "Global", "Full control of the domain. Member of each domain machine's local Administrators group."],
        ["Enterprise Admins", "**Universal** (forest root only)", "Full control of the forest: add or remove domains, configure sites, authorize DHCP across the forest."],
        ["Schema Admins", "Universal (forest root)", "Modify the schema."],
        ["Domain Users / Domain Computers / Domain Controllers / Domain Guests", "Global", "All users / workstations and member servers / DCs / guests of the domain."],
        ["DnsAdmins, DHCP Administrators, DHCP Users", "Domain Local", "Manage DNS / manage DHCP / read-only view of DHCP."],
        ["DnsUpdateProxy", "Global", "DHCP servers that register DNS records for clients."],
        ["Allowed / Denied RODC Password Replication Group", "Domain Local", "Which accounts' passwords an RODC may or may not cache."],
        ["Cloneable Domain Controllers", "Global", "DCs allowed to be cloned (virtual DC cloning, 2012+)."],
        ["Account / Server / Print / Backup Operators", "Builtin (Domain Local)", "Delegated admin tasks: manage users, manage DC services, printers, backups. They can log on locally to DCs."],
    ], widths=(2.6, 1.4, 3.5))
    s.qa([
        ["Domain Admins vs Enterprise Admins?", "Domain Admins control **one domain** (all of its DCs and members). Enterprise Admins exist only in the **forest root** domain and control the **whole forest**: creating child domains (Lab 2B needs Enterprise Admin credentials), sites, and authorizing DHCP. The root domain's Administrator is in both."],
        ["Can a domain user join computers to the domain?", "Yes. By default any authenticated user can join **up to 10** computers (`ms-DS-MachineAccountQuota` = 10, seen in ADSI Edit). Domain admins have no limit. Set the quota to 0 to restrict it (AD DS Issues slides)."],
        ["Why can adatum\\administrator log on to the bby.adatum.com DC, but bby\\administrator can't log on to the adatum.com DC?", "adatum\\administrator is an **Enterprise Admin**, a member of every domain's Administrators group in the forest (and there is a two-way transitive trust). bby\\administrator is only a Domain Admin of the child, with no rights on the parent's DCs."],
    ], title="Lab Questions & Answers (accounts)")

    s.h2("SG-5  Making a clone generate its own SID: Sysprep")
    s.p("**Answer the exam wants:** run **System Preparation (Sysprep) with Generalize** before you clone or capture the image:")
    s.code("""C:\\Windows\\System32\\Sysprep\\sysprep.exe /generalize /oobe /shutdown
REM  GUI: System Cleanup Action = Enter System Out-of-Box Experience (OOBE), tick "Generalize", Shutdown Options = Shutdown
REM  optional: /mode:vm  (VM-only generalize, faster; same hypervisor)   /unattend:C:\\unattend.xml""", title="Run from an elevated cmd in C:\\Windows\\System32\\Sysprep (Lab 1B)")
    s.bullets([
        "**/generalize** removes machine-specific data (the **machine SID**, computer name, event logs, restore points), resets the activation clock and forces PnP re-detection. **/oobe** shows the out-of-box welcome screens on next boot. **/shutdown** turns the VM off so you can clone it or make it a template.",
        "The **new SID is generated on the first boot** of each clone, when it goes through OOBE.",
        "**NewSID** (Sysinternals) was **retired in 2009**. Sysprep is the only supported method.",
        "**Domain controllers can't be sysprepped.** Use virtual **DC cloning** (2012+: add the source DC to *Cloneable Domain Controllers*, run `New-ADDCCloneConfigFile`, then copy the VM) or install a new DC.",
    ])
    s.h3("SID anatomy (PsGetSid video + SID article)")
    s.code("""S-1-5-21-986110594-2717085484-131591559-500
| | |  |-------- domain / machine identifier -------| |
| | |                                                 +-- RID (Relative ID) 500 = built-in Administrator
| | +-- 21 = sub-authority: "NT non-unique" (domain or local machine accounts)
| +-- 5 = identifier authority (NT Authority)
+-- S = it's a SID; 1 = revision level""")
    s.bullets([
        "**Machine/domain SID** = `S-1-5-21-x-y-z`. Account SID = machine/domain SID + RID. Built-in Administrator = **500**, Guest = 501; your own accounts start at **1000** (local). The domain user in the video had RID 1506342. (Linux equivalent: regular UIDs start at 1000 and root is 0.)",
        "**LSASS** builds an **access token** at logon containing the user SID + group SIDs. Windows compares those SIDs with the ACLs on resources, never names. That's why renaming an account keeps its permissions, but deleting and recreating it doesn't.",
        "**The SID myth (Russinovich):** duplicate machine SIDs on workgroup or member machines are *not* actually a security hole, because domain accounts use the domain SID and remote access uses account SIDs. **Exceptions:** DCs (the domain SID must be unique), and Microsoft *still only supports* sysprepped images (WSUS and some software track machines by SID).",
    ])
    s.code("""whoami /user                         # SID of the current user
psgetsid                             # machine SID (Sysinternals PsTools)
psgetsid administrator               # SID of an account
Get-LocalUser | Select Name, SID
Get-ADDomain | Select DomainSID
wmic useraccount get name,sid""", title="Find SIDs")
    s.box("trouble", [
        "**Cloned VM can't join the domain, or two machines fight over the computer account (VirtualBox/VMware clone note):** the clone wasn't sysprepped, so it has the same machine SID and name. **Fix:** run `sysprep /generalize /oobe /shutdown` on the clone (or rebuild from a sysprepped template), then rename and join.",
        "**Linked clones (Lab 1B):** never delete or move the base (parent) VM, because every linked clone depends on its disk. Use *full clones* for long-lived servers (the DNS lab used a full clone).",
    ])
    s.qa([
        ["Do you run Sysprep inside every clone?", "No. Run it **once on the base VM**, shut it down, and clone. Each clone generalizes and gets a new SID at first boot (OOBE). Only run it on a clone if that clone was copied from a non-sysprepped machine."],
        ["What happens to activation after Sysprep?", "/generalize resets the activation (rearm) clock, which you can do a limited number of times."],
        ["Why must two DCs never share a SID?", "The domain SID is the prefix of every domain account SID. Duplicate DC or domain SIDs break authentication and trusts. Use DC cloning or a fresh promotion."],
        ["Task: install PsTools and check your SID", "Download Sysinternals PSTools, unzip, open cmd in that folder, run `psgetsid` (machine) and `psgetsid %username%`, and compare with `whoami /user`."],
    ])
