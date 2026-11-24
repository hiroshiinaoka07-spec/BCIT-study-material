"""Part 12: Week 15 topics (not yet released) + appendices."""


def part12(s):
    s.part("PART 12 — WEEK 15: MAINTENANCE, MONITORING, HYBRID CLOUD")
    s.tag("supp", "The Week 15 lecture and lab haven't been unlocked yet. Only the discussion-forum titles were available, so everything below is written from standard Microsoft and Azure documentation.")
    s.qa([
        ["What is hybrid cloud?", "An environment that **combines on-premises infrastructure (or a private cloud) with public cloud services (Azure, AWS)**, connected by networking (S2S VPN / ExpressRoute) and shared identity (**AD DS synchronized to Entra ID with Entra Connect**), so workloads and data can move between them and be managed together (**Azure Arc**, Windows Admin Center)."],
        ["Benefits of hybrid cloud?", "Scale into the cloud on demand (burst) while keeping sensitive or regulated data on-prem; pay-as-you-go cost instead of capex; cloud DR and backup (**Azure Site Recovery, Azure Backup**); **Azure File Sync** for branch file servers; gradual migration; one identity and SSO; central management and security (Arc, Defender for Cloud, Update Manager); hotpatching for Azure Edition."],
        ["Strategies to harden your server?", "Install the **minimum**: Server Core, only the roles you need, remove unused features (SMBv1). Patch regularly (WSUS / Update Manager). Apply **Microsoft security baselines through GPO**; least privilege and separate admin accounts; LAPS; Credential Guard; Secured-core / Secure Boot / TPM; BitLocker; Defender AV + EDR; **Defender Firewall on, inbound default-deny**; disable unused services; strong password, lockout and FGPP policies; audit and forward logs (SIEM); restrict RDP (NLA, RD Gateway, MFA); TLS 1.2+ and SMB signing or encryption; tested backups."],
        ["Virtualization in cloud computing? Virtualization vs cloud?", "Virtualization is the **technology** (a hypervisor) that abstracts hardware into VMs. **Cloud computing is a service model built on top of virtualization**: on-demand self-service, broad network access, resource pooling, rapid elasticity and measured (pay-per-use) service (the NIST definition). You can virtualize without a cloud (a Hyper-V host in a closet). A cloud adds automation, a self-service portal, multi-tenancy and billing."],
        ["IaaS vs PaaS vs SaaS?", "**IaaS**: the provider runs hardware, network and virtualization; **you manage the OS and up** (Azure VMs, AWS EC2). **PaaS**: the provider also runs the OS and runtime; you deploy code and data (Azure App Service, Azure SQL Database). **SaaS**: a complete application you just use (Microsoft 365, Salesforce, Gmail). Responsibility moves to the provider as you go IaaS → PaaS → SaaS."],
        ["How do you ensure high availability in a virtualized infrastructure?", "**Failover clustering** of Hyper-V hosts with shared storage (CSV / SAN / **S2D**) so VMs restart on surviving nodes; **live migration** for planned maintenance; **Hyper-V Replica** or Azure Site Recovery for DR; redundant NICs (SET teaming), switches, PSUs and storage paths (MPIO); anti-affinity so paired VMs (two DCs) run on different hosts; guest clustering (shared VHDX/VHDS); load balancers; at least N+1 capacity; monitoring and backups."],
        ["Security considerations for virtualized environments?", "Protect the **hypervisor/host** first (Server Core host, patched, no other roles, admin access restricted, separate management network); **shielded VMs / HGS**, vTPM, BitLocker; isolate traffic with VLANs, private switches and DHCP/Router Guard; prevent **VM sprawl** (inventory, retire unused VMs); secure the VM files and backups (a VHDX is the whole server); limit checkpoint use; keep integration services current; enable Secure Boot; monitor east-west traffic; control who can export or copy VMs."],
    ], title="Week 15 discussion: model answers")
    s.h3("Server maintenance and monitoring quick reference")
    s.tag("supp")
    s.table(["Tool", "Use"], [
        ["Event Viewer (`eventvwr.msc`)", "System, Application, Security, Setup logs; Applications and Services Logs (DNS Server, DHCP-Server, Directory Service, GroupPolicy); custom views; event subscriptions (forwarding)"],
        ["Performance Monitor (`perfmon`)", "Counters (Processor % Processor Time, Memory Available MBytes, PhysicalDisk Avg. Disk sec/Read, Network Bytes Total/sec); **Data Collector Sets**; baselines"],
        ["Resource Monitor / Task Manager", "Real-time CPU, memory, disk and network per process"],
        ["Reliability Monitor, `msinfo32`, System Insights (2019+)", "Stability history; system info; predictive capacity forecasting"],
        ["Windows Server Backup (`wbadmin`)", "Full server / bare-metal / **system state** (AD) backups: `wbadmin start systemstatebackup -backuptarget:E:`"],
        ["WSUS / Windows Update / Azure Update Manager", "Patch approval and deployment"],
        ["Windows Admin Center, Azure Monitor / Arc", "Browser-based or hybrid monitoring and management"],
    ], widths=(2.5, 5.0))


def appendices(s):
    s.part("APPENDIX A — PORT NUMBERS MASTER TABLE")
    s.table(["Service", "Port / protocol", "Service", "Port / protocol"], [
        ["**DNS**", "**53 UDP + TCP** (TCP for zone transfers)", "**DHCP** server / client", "**UDP 67 / 68**"],
        ["DHCPv6 client / server", "UDP 546 / 547", "**DHCP failover**", "**TCP 647**"],
        ["**Kerberos**", "**88** TCP/UDP", "kpasswd (Kerberos password change)", "464"],
        ["**LDAP** / LDAPS", "**389** / **636**", "**Global Catalog** / GC SSL", "**3268** / 3269"],
        ["**SMB** (file sharing)", "**TCP 445**", "NetBIOS name / datagram / session", "UDP 137, UDP 138, TCP 139"],
        ["RPC endpoint mapper", "TCP 135 (+ dynamic 49152–65535)", "NTP / W32Time", "UDP 123"],
        ["**RDP**", "**TCP 3389**", "**WinRM** HTTP / HTTPS", "**5985 / 5986**"],
        ["**iSCSI**", "**TCP 3260**", "iSNS", "TCP 3205"],
        ["NFS", "2049", "WINS replication", "TCP 42"],
        ["HTTP / HTTPS", "80 / 443", "FTP data / control", "20 / 21"],
        ["SMTP / submission", "25 / 587", "SSH", "22"],
        ["**PPTP**", "**TCP 1723 + GRE (IP 47)**", "**L2TP/IPsec**", "**UDP 500, 4500, 1701 + ESP (IP 50)**"],
        ["**SSTP**", "**TCP 443**", "**IKEv2**", "**UDP 500, 4500**"],
        ["**RADIUS** auth / accounting", "**UDP 1812 / 1813**", "Teredo", "UDP 3544"],
        ["DNS over HTTPS / TLS", "443 / 853", "SNMP", "UDP 161/162"],
    ], widths=(1.8, 2.0, 1.9, 1.8), size=8)

    s.part("APPENDIX B — LAB TOPOLOGY AND IP PLAN")
    s.table(["Host", "IP / role (as used in the labs)"], [
        ["CA-VAN-SVR1", "**192.168.239.1/24**: first DC, forest root **adatum.com** (NetBIOS ADATUM), DNS (points to itself), DHCP, GC"],
        ["CA-VAN-SVR2", "192.168.239.2: second DC in adatum.com (DNS + GC); DHCP failover partner"],
        ["CA-VAN-SVR3", "Child-domain DC **bby.adatum.com** (DNS → Svr1 during promotion)"],
        ["CA-VAN-SVR4", "Domain-tree DC **indy.com** (tree lab) / secondary DNS server (DNS lab; the instructor used .5)"],
        ["CA-VAN-SVR6", "**192.168.239.6**: member file server (share-permission lab) + Hyper-V host"],
        ["CA-VAN-SVR7", "iSCSI target + storage pool server (5 × 10 GB SCSI disks)"],
        ["CA-VAN-SVR9", "Server Core VM (sconfig, remote management)"],
        ["CA-VAN-CLIENT1 / C1", "**192.168.239.20**, DNS 192.168.239.1: domain client (DHCP, share and iSCSI tests)"],
        ["Remote DHCP subnets", "Houston 172.16.30.0/24 (GW .1), Mexico 172.16.40.0/24, Portland 172.16.50.0/24 (relay lab)"],
        ["Network", "VMware **VMnet9 host-only** (local DHCP off). DMZ in the topology diagram: 133.12.10.x (WAP, ADFS, RD Gateway, IIS); S2S VPN to Azure"],
    ], widths=(1.8, 5.7))

    s.part("APPENDIX C — TROUBLESHOOTING INDEX (symptom → fix)")
    s.table(["Symptom", "Likely cause → fix", "See"], [
        ["Can't ping a server", "Firewall blocks ICMPv4 echo → add the ICMP rule / enable File and Printer Sharing (Echo)", "Part 1"],
        ["Clone won't join the domain / duplicate SID", "Not sysprepped → `sysprep /generalize /oobe /shutdown`", "SG-5"],
        ["\"DC could not be contacted\" when joining", "Client DNS isn't pointing at the DC → set DNS to 192.168.239.1", "SG-6"],
        ["Child-domain promotion fails", "No delegation in the parent zone → New Delegation `bby` on Svr1", "SG-6"],
        ["Can't ping or resolve indy.com", "No cross-tree DNS → conditional forwarder or stub zone", "SG-6 / SG-33"],
        ["\"Trust relationship … failed\"", "Machine password mismatch (snapshot or restore) → rejoin, or `Test-ComputerSecureChannel -Repair`", "SG-6"],
        ["User can't join more than 10 PCs", "`ms-DS-MachineAccountQuota` = 10 → pre-stage or use an admin account", "SG-4"],
        ["Universal group \"not found\" when nesting cross-domain", "GC replication delay (15+ min) → wait or `repadmin /syncall`", "SG-9"],
        ["Replication errors", "`repadmin /replsummary` → `/showrepl` → `/syncall` → `/kcc`; check DNS and time", "SG-8"],
        ["Can't raise DFL to 2016", "An older DC (2012 R2) still exists → upgrade or demote it first", "SG-11"],
        ["Users see folders they shouldn't", "Inherited permissions / ABE off → disable inheritance, enable ABE", "SG-21"],
        ["Disks missing from the Primordial pool", "Disks initialized or partitioned → `Clear-Disk` / diskpart `clean`", "SG-23"],
        ["Client gets 169.254.x.x", "DHCP unauthorized, scope not activated, no relay → fix", "SG-29 / SG-32"],
        ["DHCP authorize error 20079", "Not logged in as an Enterprise Admin → log on as Adatum\\administrator", "SG-29"],
        ["Secondary zone \"not loaded by DNS server\"", "Zone transfers not allowed on the primary → allow to the secondary IP + Notify", "SG-33"],
        ["GPO not applying", "Wrong OU, security filtering, block inheritance, DNS → `gpresult /r`, `gpupdate /force`", "SG-26"],
        ["Hyper-V won't install in a VMware VM", "VT-x/EPT not exposed → tick *Virtualize Intel VT-x/EPT*; check `systeminfo`", "SG-36"],
        ["VMware won't start VMs on a Hyper-V or WSL2 host", "The hypervisor is taken → disable Hyper-V / Virtual Machine Platform / Memory Integrity", "SG-36"],
        ["VMware install error 1327", "Bad InstallPath64 registry value → fix the path", "Part 1"],
    ], widths=(2.4, 4.3, 0.8), size=8)

    s.part("APPENDIX D — LAST-MINUTE RAPID REVIEW")
    s.bullets([
        "Standard vs Datacenter: same limits; **2 VMs vs unlimited**; S2D, Shielded VMs and SDN are Datacenter-only. Essentials = **25 users / 50 devices**.",
        "Core ↔ Desktop Experience **can't be switched** (2016+). In-place upgrade: up to 2 versions ahead.",
        "New SID for a clone: **`sysprep /generalize /oobe /shutdown`**. Administrator RID **500**, new accounts **1000+**.",
        "**One PDC Emulator per domain.** FSMO = 5 roles: Schema and Domain Naming (forest), RID, PDC and Infrastructure (domain). `netdom query fsmo`.",
        "Partitions: Schema and Configuration (forest), Domain, Application (DNS). `ntds.dit` in `%SystemRoot%\\NTDS`.",
        "GC: partial copy of every object in the forest, port **3268**, universal groups, UPN logon. **At least 2**, ideally one per site.",
        "Functional level 2016 (`WinThreshold`) is the highest for 2016/2019/2022. Raise the DFL only after every DC runs that OS. DFL in ADUC, FFL in AD Domains and Trusts.",
        "Adding attributes = **schema change** (forest-wide, Schema Master, irreversible).",
        "RODC: read-only, one-way replication, PRP caches no passwords by default, admin role separation, pre-create the account in ADUC.",
        "Global = same-domain members; DL = members from anywhere, permissions in its own domain; Universal = forest-wide, stored in the GC, no DL members. **IGDLA.** Distribution groups have no SID.",
        "NTFS Full Control − Modify = **change permissions + take ownership** (+ delete subfolders and files). Share = Read / Change / Full Control. **Most restrictive of share and NTFS** applies over the network; **Deny wins**.",
        "Private IPs: 10/8, 172.16/12, 192.168/16; APIPA 169.254/16. IPv6: global 2000::/3, link-local FE80::/10, ULA FC00::/7, multicast FF00::/8, loopback ::1.",
        "Storage Spaces minimum disks: simple 1, two-way mirror **2**, parity **3**, three-way mirror **5**, dual parity **7**. Thin vs fixed provisioning.",
        "RAID 0 striping (no fault tolerance), RAID 1 mirroring (50%), RAID 5 striping + parity (minimum 3 disks, n−1 capacity). RAID ≠ backup.",
        "Block (SAN, iSCSI 3260, FC, LUN; databases) vs file (NAS, SMB 445 / NFS). iSCSI target / initiator / IQN, **mutual CHAP**.",
        "GPO order **LSDOU**, last one wins; Enforced beats Block Inheritance; refresh every 90 ± 30 min (DCs 5 min). Domain password policy comes **only from domain-level GPOs** (FGPP for exceptions).",
        "Password defaults **24 / 42 / 1 / 7 / complexity on**; lockout threshold **0**. Kerberos **10 h / 7 d / 5 min**.",
        "DHCP **DORA** (broadcast), UDP 67/68; renew at **50%** (unicast), rebind at **87.5%** (broadcast), at 100% start over. Default lease **8 days**. Authorize in AD; activate the scope.",
        "Relay agent = RRAS → IPv4 → General → New Routing Protocol → DHCP Relay Agent. Superscope = multinet. Failover: load balance or hot standby, MCLT, TCP 647.",
        "DNS **port 53 UDP/TCP**. Zones: primary (read/write), secondary (read-only, zone transfer), stub (SOA/NS/glue), AD-integrated (DCs, multi-master, secure updates). Split DNS = internal AD DNS + external DMZ DNS.",
        "DNS protection: DNSSEC (KSK/ZSK, RRSIG, DNSKEY, NSEC3, trust anchors, NRPT), socket pool, cache locking 100%, secure cache against pollution, restricted zone transfers, secure updates, least-privilege DnsAdmins.",
        "nslookup: `set type=srv` → `_ldap._tcp.dc._msdcs.adatum.com`; `set type=mx`; `server x.x.x.x`.",
        "Hyper-V = **Type 1**; VMware Workstation and VirtualBox = Type 2. Gen 2 = UEFI, SCSI boot, 64-bit, Secure Boot. VHDX up to 64 TB. Production checkpoint = VSS, disk only. **Checkpoint ≠ backup.**",
        "Switches: **External** (everyone, bound to a NIC), **Internal** (VMs + host), **Private** (VMs only).",
        "VPN: PPTP 1723 + GRE 47 (avoid); L2TP/IPsec UDP 500/4500/1701 + ESP 50; **SSTP 443**; **IKEv2 500/4500** (mobile, Always On VPN); RADIUS 1812/1813.",
    ])
    s.p("End of cheat sheet. Good luck on the final!", italic=True, color="7F7F7F")
