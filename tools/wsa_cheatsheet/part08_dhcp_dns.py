"""Part 8: DHCP (SG-29 to SG-32).  Part 9: DNS (SG-33 to SG-35)."""


def part8(s):
    s.part("PART 8 — DHCP (SG-29 to SG-32)")
    s.src("Module 9 DHCP slides (p1–p29); DHCP Lease Time article; DHCP Superscope handout; Lab \"Deploy a DHCP Server\"; DHCP Relay Agent topology + video; DHCP Policy lab doc; DHCP Failover video; Week 10 discussion prompts.")

    # ---------------- SG-29 ----------------
    s.h2("SG-29  DHCP: what it is, its services, scopes")
    s.p("**Dynamic Host Configuration Protocol (DHCP)** automatically leases IP configuration to clients: address, mask, **default gateway, DNS servers, DNS domain name** and other options. Server = **UDP 67**, client = **UDP 68** (DHCPv6: 547 / 546). Windows DHCP serves both IPv4 and IPv6.")
    s.table(["Automatic (DHCP)", "Manual (static)"], [
        ["Supplies IP addresses automatically", "Type each IP address by hand"],
        ["Ensures correct configuration information", "A typo is always possible"],
        ["Updates client configuration automatically (change an option once)", "Can cause communication and network problems"],
        ["Removes a common source of network problems; computers can move freely", "Frequent moves increase admin work"],
    ], widths=(3.75, 3.75), first_col_bold=False)
    s.h3("Install and post-install (slides p9–p12)")
    s.steps([
        "The DHCP server needs a **static IP** (lab: CA-VAN-SVR1, 192.168.239.1).",
        "Server Manager → Add Roles and Features → **DHCP Server**, or `Install-WindowsFeature DHCP -IncludeManagementTools` (the slide shows the older `Add-WindowsFeature DHCP`).",
        "**Complete DHCP configuration** (notification flag): (a) **create the DHCP security groups** *DHCP Administrators* (full management) and *DHCP Users* (read-only view), both domain local; (b) **restart the DHCP Server service**; (c) **authorize the server in AD DS**.",
        "Check bindings: right-click server → **Add/Remove Bindings** (slide p14) and make sure the right NIC is used.",
    ])
    s.box("key", [
        "**Authorization (slide p10):** a domain-joined Windows DHCP server checks AD for the list of authorized servers when it starts. **If its IP isn't on the list, the service won't hand out leases.** This protects clients from *rogue domain-joined Windows* DHCP servers, but **not** from rogue routers, access points or non-domain devices (use switch **port security / DHCP snooping**).",
        "You must be an **Enterprise Admin** (log on as `Adatum\\administrator`). Running as a local admin gives **\"DHCP authorization error 20079\"** and the *Use the following user's credentials* option is greyed out. **Unauthorize a server before retiring it.** List authorized servers with `netsh dhcp show server` or `Get-DhcpServerInDC`.",
    ])
    s.h3("Scope: what it must and may contain (slide p15)")
    s.table(["Must contain", "May contain"], [
        ["A **range** of IP addresses (start–end)\nA **subnet mask**\nA **lease duration** (default **8 days**)",
         "**Exclusions** (addresses for static servers and printers)\n**Reservations** (a fixed IP for a **MAC address**)\nOptions: default gateway (003), DNS servers (006), DNS domain name (015), WINS (044/046)\nA delay (the ms before sending an OFFER, for split scopes)"],
    ], widths=(3.0, 4.5), first_col_bold=False)
    s.table(["Option level (slide p16)", "Applies to", "Precedence"], [
        ["Server options", "Every scope on the server", "Lowest"],
        ["Scope options", "One scope", "Overrides server"],
        ["Class / policy options", "Clients that match a vendor or user class or a policy", "Overrides scope"],
        ["Reservation options", "One reserved client", "**Highest** (the most specific wins)"],
    ], widths=(2.2, 3.3, 2.0))
    s.table(["Common option", "Code", "Common option", "Code"], [
        ["Router (default gateway)", "**003**", "WINS/NBNS servers", "044"],
        ["DNS servers", "**006**", "WINS node type", "046"],
        ["DNS domain name", "**015**", "PXE boot server host name / boot file name", "066 / 067"],
        ["Lease time", "051", "Vendor class identifier", "060"],
    ], widths=(2.4, 1.35, 2.4, 1.35))

    # ---------------- SG-30 ----------------
    s.h2("SG-30  DHCP lease generation: DORA")
    s.table(["Step", "Message", "Direction", "What happens"], [
        ["1", "**DHCPDISCOVER**", "Client → **broadcast** (src 0.0.0.0:68 → 255.255.255.255:67)", "\"Is there a DHCP server out there?\""],
        ["2", "**DHCPOFFER**", "Server(s) → client (broadcast per slide)", "Each server that has a free address offers one (IP, mask, lease, options)."],
        ["3", "**DHCPREQUEST**", "Client → **broadcast**", "The client accepts **one** offer (it names the chosen server). Broadcasting it tells the other servers to withdraw their offers."],
        ["4", "**DHCPACK**", "Chosen server → client (broadcast per slide)", "Confirms the lease and records it in the database. (**DHCPNAK** = refused, so start again.)"],
    ], widths=(0.4, 1.4, 2.4, 3.3), size=8)
    s.box("memory", "**D-O-R-A: Discover, Offer, Request, Acknowledge.** The whole lease *generation* is broadcast (slide p6), which is why routers break it unless they're RFC 1542-compliant or you have a relay agent. Other messages: DHCPDECLINE (the client found the address in use), DHCPRELEASE (`ipconfig /release`), DHCPINFORM (options only).")
    s.tag("extra", "In practice OFFER and ACK can be unicast, depending on the client's broadcast flag. For the exam, use the course's \"all four are broadcasts\".")

    # ---------------- SG-31 ----------------
    s.h2("SG-31  When clients renew their lease")
    s.table(["Point in the lease", "Client action", "Sent as"], [
        ["**50 %** (T1)", "**Renewal**: DHCPREQUEST **directly to the server that gave the lease**; DHCPACK extends it", "**Unicast**"],
        ["**87.5 %** (T2)", "If 50% renewal failed: **rebind**, a DHCPREQUEST to **any** DHCP server", "**Broadcast**"],
        ["**100 %** (expired)", "Lease lost: stop using the IP and **start DORA again** with DHCPDISCOVER (APIPA 169.254.x.x if nobody answers)", "Broadcast"],
        ["Restart / reconnect", "The client tries to renew its previous address (INIT-REBOOT REQUEST)", "Broadcast"],
        ["Manual", "`ipconfig /renew` (request now) / `ipconfig /release` (give it up)", "—"],
    ], widths=(1.4, 4.6, 1.5))
    s.p("Example: an 8-day lease renews after **4 days** (T1), rebinds after **7 days** (T2), and expires after 8 days.", size=9)
    s.h3("Lease duration guidance (DHCP Lease Time article + lab question)")
    s.table(["Environment", "Suggested lease", "Why"], [
        ["Wired office desktops (Windows default)", "**8 days**", "Stable devices; little renewal traffic"],
        ["Home routers", "24 h (1,440 min / 86,400 s)", "Typical consumer default"],
        ["**Wireless / Wi-Fi** clients", "**About 24 hours or less**", "Devices come and go; short leases return addresses to the pool quickly"],
        ["Guest networks", "About 8 hours", "One visit ≈ one working day"],
        ["Hotspots, coffee shops", "**About 1 hour**", "High turnover. Article example: a 200-address pool with a 1-hour lease serves about 130 new guests every hour"],
    ], widths=(2.3, 1.7, 3.5))
    s.bullets([
        "Keep **about 20% of the pool free** as headroom. Leave room outside the pool for static devices (e.g. pool .10–.200; servers and printers below .10 or above .200).",
        "Shorter leases mean more DHCP traffic and server load, but faster reclamation. Longer leases mean less traffic, but the pool can be exhausted by devices that have left.",
    ])

    # ---------------- SG-32 ----------------
    s.h2("SG-32  Create a scope; DHCP proxy (relay agent); superscope")
    s.h3("New Scope Wizard (lab Task 3)")
    s.steps([
        "Tools → **DHCP** → expand `ca-van-svr1.adatum.com` → right-click **IPv4** → **New Scope**.",
        "**Scope name** + description (make it meaningful, e.g. *Vancouver-239*).",
        "**IP Address Range**: start/end (e.g. 192.168.239.100–.200) and **subnet mask** / length 24. (Alternatively use .1–.254 and exclude the static ranges.)",
        "**Add Exclusions and Delay**: excluded range(s); **delay** in ms before sending OFFER (used by the secondary server in a split scope).",
        "**Lease Duration**: default **8 days**.",
        "**Configure DHCP Options**: Yes → **Router (default gateway)** → **Domain Name and DNS Servers** (add primary and secondary DNS) → **WINS Servers** (skip).",
        "**Activate Scope**: **Yes**. *An unactivated scope hands out nothing* (the lab stresses this).",
        "Repeat for the **Houston** scope (172.16.30.0/24), then on the client remove the static IP and run `ipconfig /release`, `ipconfig /renew`, `ipconfig /all`. Check **Address Leases** in the DHCP console.",
    ])
    s.code("""Install-WindowsFeature DHCP -IncludeManagementTools
netsh dhcp add securitygroups ; Restart-Service DHCPServer          # or Add-DhcpServerSecurityGroup
Add-DhcpServerInDC -DnsName ca-van-svr1.adatum.com -IPAddress 192.168.239.1
Add-DhcpServerv4Scope -Name "Vancouver" -StartRange 192.168.239.100 -EndRange 192.168.239.200 `
   -SubnetMask 255.255.255.0 -LeaseDuration 8.00:00:00 -State Active
Add-DhcpServerv4ExclusionRange -ScopeId 192.168.239.0 -StartRange 192.168.239.100 -EndRange 192.168.239.110
Set-DhcpServerv4OptionValue -ScopeId 192.168.239.0 -Router 192.168.239.254 -DnsServer 192.168.239.1 -DnsDomain adatum.com
Add-DhcpServerv4Reservation -ScopeId 192.168.239.0 -IPAddress 192.168.239.150 -ClientId "00-15-5D-01-02-03" -Name Printer1
Get-DhcpServerv4Lease -ScopeId 192.168.239.0 ; Get-DhcpServerv4ScopeStatistics ; Get-DhcpServerInDC""",
           title="DHCP in PowerShell")
    s.tag("extra", "The cmdlets; the lab uses the GUI.")

    s.h3("DHCP relay agent (\"DHCP proxy\")")
    s.p("DHCP DISCOVER is a broadcast, and **routers don't forward broadcasts**. A **DHCP relay agent** on the client subnet listens for DHCP broadcasts and **forwards them as unicast** to a DHCP server on another subnet, filling in the *giaddr* field so the server picks the **scope that matches the client's subnet**. It's needed when routers are **not RFC 1542-compliant** (no `ip helper-address`). (Slide p17.)")
    s.steps([
        "Install the **Remote Access** role → role service **Routing** (it also adds DirectAccess and VPN).",
        "Tools → **Routing and Remote Access** → right-click server → *Configure and Enable* → Custom configuration → **LAN routing** → Start service.",
        "Expand **IPv4** → right-click **General** → **New Routing Protocol** → **DHCP Relay Agent**.",
        "Right-click **DHCP Relay Agent** → Properties → **add the DHCP server's IP** (192.168.239.1).",
        "Right-click **DHCP Relay Agent** → **New Interface** → choose the interface facing the client subnet (hop-count and boot thresholds can stay at their defaults).",
    ])
    s.p("Lab relay topology: DHCP server **192.168.239.1**; remote subnets Houston **172.16.30.1**, Mexico **172.16.40.1**, Portland **172.16.50.1**, gateway 192.168.239.1. Create one scope per remote subnet on Svr1.", size=9)
    s.h3("Superscopes and multicast scopes (slide p22 + Superscope handout)")
    s.bullets([
        "**Superscope** = an administrative grouping of several scopes that serve **one physical network segment carrying more than one logical IP subnet (a multinet)**. Uses: the first subnet is **running out of addresses** (add a second subnet on the same wire), **renumbering** from one subnet to another, clients behind one relay agent that use several subnets, and two DHCP servers on one segment each managing part of a superscope.",
        "Create: right-click IPv4 → **New Superscope** → name → choose member scopes. `Add-DhcpServerv4Superscope -SuperscopeName Multinet -ScopeId 192.168.239.0,192.168.240.0`.",
        "**Multicast scope** (MADCAP) hands out **multicast group addresses** (224.0.0.0–239.255.255.255, normally 239.x admin-scoped) to apps such as video streaming or imaging (WDS multicast).",
    ])
    s.h3("DHCP policies (policy-based assignment, DHCP Policy lab)")
    s.p("Hand out different IPs, options or leases based on **vendor class, user class, MAC address, FQDN or relay agent information** (slide p21).", size=9)
    s.steps([
        "DHCP → IPv4 → right-click → **Define User Classes** → Add → Display name **Sales**, ASCII data `sales`. (User classes **can't be defined for IPv6**.)",
        "Scope **Office** (192.168.239.100–.200) → **Policies** → New Policy **sales** → Condition: **User Class Equals Sales** → IP range **.190–.200** → options → lease **8 hours**.",
        "Client: `ipconfig /setclassid \"Ethernet0\" sales` → `ipconfig /release` → `ipconfig /renew` → `ipconfig /all` shows the class ID and an address from .190–.200.",
        "Task: add a **Finance** class and policy with range .100–.150.",
    ])
    s.h3("High availability: split scope vs failover vs cluster")
    s.table(["Option", "How it works", "Pros / cons"], [
        ["**DHCP cluster**", "Failover Clustering with the DHCP database on shared storage", "True HA, but needs shared storage and a cluster"],
        ["**Split scope**", "Two servers each own part of one subnet (slide: Server A .1–.150, Server B .151–.254). The secondary has a **delay (500 ms)** so the primary usually answers first. Microsoft's rule of thumb: **80/20**. Right-click scope → **Advanced → Split-Scope**", "Simple, works on 2008. **No shared lease state**, and if one server dies only its part of the pool is available"],
        ["**DHCP failover** (2012+)", "Two servers **share and replicate the lease database** for the same scopes. Modes: **Load balance** (default 50:50, both active) or **Hot standby** (one active, the standby keeps a **5% reserve**). IPv4 only, 2 servers per relationship", "The recommended option. Needs a unique relationship name, MCLT and shared secret"],
    ], widths=(1.3, 4.0, 2.2), size=8)
    s.table(["Failover setting (slide p26)", "Meaning"], [
        ["**Relationship name**", "Must be **unique** per server (e.g. *Svr1-Svr2*). Slide question \"Any problem?\": reusing a name, or adding a scope that's already in another relationship, fails."],
        ["**MCLT (Maximum Client Lead Time)**", "How long a partner may extend a lease beyond what the other knows, and how long it waits before **taking over the whole scope** after the partner is marked down (default **1 hour**)."],
        ["**Auto state switchover interval**", "How long a lost-contact partner waits before deciding the other is **down** (Partner Down state)."],
        ["**Message authentication / shared secret**", "A password that validates failover messages."],
        ["**Port / firewall**", "**TCP 647**. Rules *Microsoft-Windows-DHCP-Failover-TCP-In/Out* are created automatically when DHCP is installed."],
    ], widths=(2.3, 5.2))
    s.code("""Add-DhcpServerv4Failover -ComputerName ca-van-svr1 -Name "Svr1-Svr2" -PartnerServer ca-van-svr2.adatum.com `
  -ScopeId 192.168.239.0 -LoadBalancePercent 50 -MaxClientLeadTime 01:00:00 -SharedSecret "Pa55w.rd"
# Hot standby:  -ServerRole Standby -ReservePercent 5
Get-DhcpServerv4Failover ; Invoke-DhcpServerv4FailoverReplication""", title="Failover (video: right-click scope → Configure Failover → partner Svr2 → MCLT 1 h → Load balance → shared secret)")
    s.box("instructor", "Failover video test: **stop the DHCP service on Svr1**, run `ipconfig /release` + `/renew` on the client, and it **still gets an IP, now from Svr2**. Both consoles show the same leases because the database is replicated.")
    s.h3("Database, migration and security")
    s.bullets([
        "**Database:** `Dhcp.mdb` in **`%systemroot%\\System32\\DHCP`**. **Backed up automatically every 60 minutes** to `...\\DHCP\\backup`, or manually (right-click server → Backup / Restore). **Reconcile** (scope or IPv4 → Reconcile All Scopes) fixes inconsistencies between the database and the registry.",
        "**Migrate:** `Export-DhcpServer -ComputerName OLD -File C:\\dhcp.xml -Leases` then `Import-DhcpServer -File C:\\dhcp.xml -BackupPath C:\\dhcpbak -Leases`, or `netsh dhcp server export C:\\dhcp.txt all` / `import`. Unauthorize the old server afterwards.",
        "**Security (slides p19–p20):** disconnect unused LAN drops; require authenticated Layer-2 connections (802.1X); enable **DHCP audit logging** (Event Viewer → Applications and Services Logs → Microsoft → Windows → **DHCP-Server**; text logs in `%windir%\\System32\\dhcp\\DhcpSrvLog-*.log`); **DHCP name protection** uses a **DHCID** record so a non-Windows device can't overwrite a Windows machine's DNS name.",
    ])
    s.h3("DHCP lab: Questions & Answers")
    s.qa([
        ["Role-based vs feature-based installation, and which is which?", "The same wizard path: it installs roles (DHCP, DNS, AD DS) **and** features (BitLocker, Failover Clustering, .NET) on one server. The alternative is *Remote Desktop Services installation* (scenario-based, multi-server)."],
        ["What are the DHCP Administrators and DHCP Users groups?", "Domain local groups created by post-install. **DHCP Administrators** can manage scopes, options and leases (but authorizing a server needs Enterprise Admin). **DHCP Users** have **read-only** access to the console."],
        ["Lease duration for wireless devices, and why?", "Shorter (hours to about a day), because mobile devices join and leave often. A long lease would keep addresses tied up by devices that are gone and exhaust the pool."],
        ["What is WINS? WINS vs DNS?", "**WINS** (Windows Internet Name Service) dynamically maps flat **NetBIOS names** (15 characters) to IPs for legacy apps (NetBIOS name service UDP 137, WINS replication TCP 42). **DNS** resolves **hierarchical FQDNs**, is the Internet standard, and is required by AD. WINS is legacy and deprecated."],
        ["Does the client have to join the domain to use Windows DHCP?", "**No.** Any DHCP client (workgroup PCs, phones, printers, Linux) gets a lease. Only the *server* needs to be authorized in AD."],
        ["Does the client get its IP from your scope?", "Confirm with `ipconfig /all` (*DHCP Server* = 192.168.239.1, lease obtained and expiry) and DHCP console → scope → **Address Leases**."],
        ["In which scenarios must you deploy a DHCP relay agent?", "When the DHCP server is on a **different subnet** from the clients and the router doesn't forward DHCP broadcasts (non-RFC 1542, no ip-helper). Example: one central DHCP server for the Houston, Mexico and Portland subnets."],
        ["Why do you get error 20079 when authorizing?", "You're signed in as a local or non-Enterprise admin. Sign out and sign in as `Adatum\\administrator`, then authorize."],
        ["DHCP Policy challenge: the lease shows 1 hour instead of the 8-hour policy. Why? (hint: relay agent)", "The client isn't matching the policy on the server it actually leased from. When the request arrives **through a relay agent**, the server picks the scope for the relay's subnet (giaddr), and that scope (and its 1-hour lease) has no *sales* policy, or the class ID wasn't set on the adapter that's actually connected. Fix: put the policy on the scope the relay maps to (or set it server-wide), check the class with `ipconfig /all`, then release and renew."],
    ])
    s.h3("Troubleshooting DHCP (slide p29 discussion): model answers")
    s.tag("model")
    s.table(["Problem", "Causes", "Fixes"], [
        ["**Address conflicts**", "Static devices inside the pool, overlapping scopes on two servers, a rogue DHCP server, a restored old database", "Exclude static ranges or use reservations; enable server **Conflict detection attempts** (Properties → Advanced, 1–2 pings before leasing); don't overlap scopes (use failover); remove the rogue server; reconcile scopes"],
        ["**Failure to obtain an address** (client shows 169.254.x.x)", "Service stopped, server **not authorized**, scope **not activated**, pool exhausted, no relay across a router, wrong binding, firewall on UDP 67/68, VLAN issue", "Start or authorize the server, activate the scope, configure a relay or ip-helper, check bindings, `ipconfig /renew`, check the DHCP-Server event log"],
        ["**Address from the wrong scope**", "A rogue server answers first; the relay points to the wrong server or giaddr; multinet without a superscope; policy conditions", "Find the server with `ipconfig /all`; fix the relay settings; create a **superscope**; review policies and the switch VLAN config"],
        ["**Database corruption or loss**", "Disk failure, unclean shutdown", "Restore from the automatic backup (`...\\dhcp\\backup`) or a manual backup; **Reconcile All Scopes**; with failover, resync from the partner; `jetpack dhcp.mdb tmp.mdb` to compact"],
        ["**Pool exhausted**", "Too many clients, leases too long, rogue or stale devices", "Shorten the lease, widen the scope or add a superscope, delete stale leases, add failover capacity, monitor with `Get-DhcpServerv4ScopeStatistics` or IPAM (keep 20% free)"],
    ], widths=(1.6, 2.7, 3.2), size=8)
    s.h3("Week 10 discussion: model answers")
    s.tag("model")
    s.qa([
        ["What is DHCP?", "A client/server protocol (UDP 67/68) that automatically assigns IP configuration from a central server using DORA, with leases that renew at 50% and 87.5%."],
        ["Scope vs superscope?", "A scope is the pool and options for **one** subnet. A superscope groups several scopes so one DHCP server can serve a **physical segment that has multiple logical subnets** (multinet)."],
        ["What is split-scope?", "A fault-tolerance design where two DHCP servers each own a non-overlapping part of one subnet's range (e.g. 80/20), with a delay on the secondary. Simple, but there's no lease sharing. It has been replaced by DHCP failover."],
        ["Multicast vs unicast vs broadcast?", "**Unicast**: one sender to one receiver (e.g. DHCP renewal). **Broadcast**: one to **all** hosts on the local subnet, not routed (DHCPDISCOVER, ARP). **Multicast**: one to a **subscribed group** (224.0.0.0/4, IGMP; e.g. video streaming, OSPF, WDS imaging); it can be routed. IPv6 has no broadcast."],
    ], title=None)


def part9(s):
    s.part("PART 9 — DNS (SG-33 to SG-35)")
    s.src("Module 8 DNS slides (p1–p41); 9 Windows DNS mistakes article; DNS Topics doc (forwarder vs conditional forwarder vs stub; zone types); Secondary DNS Zone lab + video; DNS Exercise / Namespace Design; Optional DNSSEC lab; How to Configure Linux DNS handout; Week 9 discussion prompts.")

    # ---------------- SG-33 ----------------
    s.h2("SG-33  DNS and zones")
    s.p("**DNS (Domain Name System)** is the hierarchical, distributed naming service of TCP/IP and the Internet. It resolves names (FQDNs) to IP addresses like a phone book, and IPs back to names. **AD DS depends on DNS**: clients find DCs through **SRV records**. DNS servers are also called **name servers**.")
    s.table(["Component (slide p9)", "Meaning"], [
        ["DNS namespace", "The hierarchy: root `.` → TLD (`com`, `ca`, `uk`, `jp`) → second-level domain registered to an organization (`adatum`) → subdomains (`bby`) → hosts. E.g. `computer01.unitedstates.microsoft.com`."],
        ["DNS server", "Holds a database of names and IPs (zones) and answers queries."],
        ["DNS zone", "A **portion of the namespace** that one server is authoritative for, stored as a zone file or in AD. It's split off **for administrative reasons**."],
        ["Resolver", "The client component that sends queries (the DNS Client service, which caches answers)."],
        ["Resource records", "The entries: A, AAAA, SRV, PTR, MX, CNAME, NS, SOA, TXT."],
    ], widths=(1.8, 5.7))
    s.bullets([
        "**Forward lookup zone**: name → IP (A, AAAA, CNAME, MX, SRV). **Reverse lookup zone**: IP → name (**PTR**), e.g. `239.168.192.in-addr.arpa` for 192.168.239.0/24 (IPv6: `ip6.arpa`).",
        "**Five deployment steps (slide p10):** (1) install DNS on one or more servers (for redundancy and performance), (2) configure the servers, (3) create forward and reverse lookup zones, (4) add resource records, (5) point clients at the DNS servers. **Slide question: can DNS run on Nano Server? Yes** (the DNS package).",
        "**Authoritative** answer: from a server that holds a **complete copy of the zone** (valid **SOA + NS** records, and the NS records should match the SOA). **Non-authoritative** answer: comes from a server's **cache** of something it learned from another server.",
    ])
    s.h3("Zone types")
    s.table(["Zone type", "Copy", "Storage", "Key facts"], [
        ["**Primary**", "**Read/write** master (authoritative)", "Text file `%systemroot%\\System32\\dns\\<zone>.dns`", "Easy to back up and restore. Single master: the primary must be up to make changes"],
        ["**Secondary**", "**Read-only** copy, received by **zone transfer**", "Text file", "Copied from a primary, **another secondary or an AD-integrated** zone; adds load balancing and fault tolerance. Windows can be secondary to a **Unix/BIND primary**. Can't edit records"],
        ["**Stub**", "Only **SOA, NS and glue A records** for the zone", "File or AD", "**Not authoritative**; redirects queries to the zone's real name servers and updates itself automatically when their NS records change"],
        ["**AD-integrated** (primary or stub)", "Read/write on **every DC** that has it (**multi-master**)", "Stored in the **AD database** (DomainDnsZones / ForestDnsZones partitions)", "**Only available on DCs**; replicated by AD (attribute-level); **secure dynamic updates**; ACL-based delegated admin; HA. **Harder to restore in a disaster**"],
    ], widths=(1.3, 1.9, 1.9, 2.4), size=8)
    s.table(["AD-integrated replication scope", "Partition", "Replicates to"], [
        ["To all DNS servers on DCs in this **forest**", "ForestDnsZones", "Every DC running DNS in the forest (e.g. `_msdcs.adatum.com`)"],
        ["To all DNS servers on DCs in this **domain** (default)", "DomainDnsZones", "DCs running DNS in the domain"],
        ["To all DCs in this domain (Windows 2000 compatible)", "Domain partition", "All DCs, even those without DNS"],
        ["Custom application partition", "Your own", "The DCs you enlist"],
    ], widths=(2.9, 1.5, 3.1))
    s.h3("Recursive vs iterative queries; forwarders; root hints")
    s.table(["Term", "Meaning"], [
        ["**Recursive query**", "\"Give me the final answer or an error.\" A client asks its DNS server; that server does all the work."],
        ["**Iterative query**", "\"Give me the best answer you have (often a referral).\" With no forwarder, the DNS server goes **root → TLD → authoritative server** step by step (slide p22)."],
        ["**Root hints**", "The list of the **13 root server names (A–M.ROOT-SERVERS.NET)** that a DNS server uses to start iterative resolution. Used **only if forwarders aren't configured or fail** (server Properties → Root Hints, slide p25)."],
        ["**Forwarder**", "A DNS server (e.g. the ISP's, or 8.8.8.8) that this server sends **all** queries it can't answer to. Why use one (slide question): it controls and centralizes outbound DNS traffic, builds a shared cache, and lets only one server talk to the Internet through the firewall. Set it in Properties → **Forwarders** (the *Use root hints if no forwarders are available* box)."],
        ["**Conditional forwarder**", "Forwards only queries **for a specific domain** (e.g. `indy.com` → 192.168.239.4). **It overrides the server-level forwarders for that domain.** Lives in the *Conditional Forwarders* node and can be AD-replicated."],
        ["**Stub zone**", "Like a self-updating conditional forwarder: it keeps the target zone's **NS list current automatically**."],
        ["**Zone delegation**", "The parent zone hands authority for a subdomain (e.g. `bby.adatum.com`) to other servers using NS + glue records (**New Delegation**). Spreads load and administration (slide p35)."],
    ], widths=(1.7, 5.8))
    s.box("key", [
        "**Slide p37 guidance.** Use a **conditional forwarder** when the other name is a **different domain**, even a different TLD (adatum.com ↔ indy.com, a partner company), and you want all resolution for it to take one specific path. Use a **stub zone** when the domain is **below a higher level**, i.e. a **delegation below a delegation**, and you want the NS list to stay current automatically.",
    ])
    s.h3("Resource records (SG-35 overlap)")
    s.table(["Record", "Purpose", "Example"], [
        ["**A** / **AAAA**", "Host name → IPv4 / IPv6", "`ca-van-svr1  A  192.168.239.1`"],
        ["**CNAME**", "Alias → canonical name", "`www  CNAME  web1.adatum.com.`"],
        ["**MX**", "Mail server for the domain; **lower preference number = tried first**", "`@  MX 10  mail.adatum.com.`"],
        ["**NS**", "Authoritative name servers for the zone", "`@  NS  ca-van-svr1.adatum.com.`"],
        ["**SOA**", "**One per zone**: primary NS, admin e-mail (`hostmaster.adatum.com.`), **serial number**, refresh, retry, expire, minimum TTL", "See SOA table below"],
        ["**SRV**", "**Service → host + port**: priority, weight, port, target. DCs register them dynamically **by service and site**", "`_ldap._tcp.dc._msdcs.adatum.com  SRV 0 100 389 ca-van-svr1.adatum.com.`"],
        ["**PTR**", "IP → name (reverse zone)", "`1  PTR  ca-van-svr1.adatum.com.`"],
        ["**TXT / SPF**", "Free text; **SPF** lists allowed mail senders (with MX and DKIM/DMARC, it fights **e-mail spoofing**); domain verification", "`@ TXT \"v=spf1 mx -all\"`"],
        ["Glue A", "The A record of a name server that lives **inside** the zone it serves, included with the delegation to break the circular lookup", "`ns1.bby.adatum.com A 192.168.239.3` in the parent"],
        ["DHCID", "Used by DHCP name protection", ""],
    ], widths=(1.0, 3.6, 2.9), size=8)
    s.box("key", "**SRV benefits (slide p21):** DCs register SRV records **by service and site**, so clients find a DC **in their own site** before crossing WAN links, which keeps WAN traffic down.")
    s.code("""Add-DnsServerResourceRecordA -ZoneName Adatum.com -Name CA-VAN-Svr3 -IpAddress 192.168.239.4      # slide p18
Add-DnsServerResourceRecordCName -ZoneName adatum.com -Name www -HostNameAlias web1.adatum.com
Add-DnsServerResourceRecordMX -ZoneName adatum.com -Name "." -MailExchange mail.adatum.com -Preference 10
Add-DnsServerResourceRecordPtr -ZoneName 239.168.192.in-addr.arpa -Name 1 -PtrDomainName ca-van-svr1.adatum.com
Add-DnsServerPrimaryZone -Name adatum.com -ReplicationScope Domain          # AD-integrated
Add-DnsServerPrimaryZone -NetworkId 192.168.239.0/24 -ReplicationScope Forest   # reverse zone
Add-DnsServerSecondaryZone -Name adatum.com -ZoneFile adatum.com.dns -MasterServers 192.168.239.1
Add-DnsServerStubZone -Name indy.com -MasterServers 192.168.239.4 -ReplicationScope Forest
Add-DnsServerConditionalForwarderZone -Name indy.com -MasterServers 192.168.239.4 -ReplicationScope Forest
Add-DnsServerForwarder -IPAddress 8.8.8.8 ; Get-DnsServerZone ; Get-DnsServerResourceRecord -ZoneName adatum.com""",
           title="DNS PowerShell (DnsServer module)")

    s.h3("Secondary zone lab (CA-VAN-SVR4/5)")
    s.steps([
        "Prepare Svr4/Svr5 (**full clone**, sysprepped): static IP, **remove IPv6**, set the time zone, join adatum.com. The instructor also **disabled Edge on servers** (virus risk).",
        "From Svr1's Server Manager: **Add Servers** → Svr4 → Add Roles → DNS **installed remotely** on Svr4.",
        "On Svr4: DNS Manager → Forward Lookup Zones → **New Zone** → **Secondary zone** → name `adatum.com` → **Master DNS server: 192.168.239.1** → Finish.",
        "The zone shows **\"Zone not loaded by DNS server\"** because the primary refuses the transfer. **Fix on the PRIMARY (Svr1):** adatum.com → Properties → **Zone Transfers** → tick **Allow zone transfers** → **Only to the following servers** → add Svr4's IP → **Notify…** → *Automatically notify* the listed servers → OK.",
        "On Svr4: right-click the zone → **Transfer from Master** (or Reload). Records appear. They're **read-only**, so you can't create records on the secondary.",
        "Check the **SOA** tab on both servers: same **serial number**, primary server = ca-van-svr1, responsible person = hostmaster.",
    ])
    s.table(["SOA field (Windows defaults, DNS lab)", "Value", "Meaning"], [
        ["Serial number", "Increments on every change", "The secondary transfers only if the primary's serial is **higher** (zone version)"],
        ["Primary server", "ca-van-svr1.adatum.com", "The master name server"],
        ["Responsible person", "hostmaster.adatum.com.", "Admin e-mail (the first `.` stands for `@`)"],
        ["Refresh interval", "**15 minutes**", "How often the secondary checks the serial"],
        ["Retry interval", "**10 minutes**", "Retry after a failed refresh"],
        ["Expires after", "**1 day**", "The secondary stops answering if it can't reach the master for this long"],
        ["Minimum (default) TTL", "**1 hour**", "Default cache time of the zone's records (and the negative-cache TTL)"],
    ], widths=(2.6, 1.8, 3.1))
    s.qa([
        ["Why \"Zone not loaded by DNS server\" on the new secondary?", "The primary doesn't allow zone transfers to it. Enable Zone Transfers → *Only to the following servers* (+ Notify) on the primary, then *Transfer from Master*."],
        ["Can you create a record on the secondary?", "**No.** A secondary zone is a read-only copy; changes are made on the primary."],
        ["How do you know a zone is secondary?", "The zone type on its General tab, and the **SOA**: its primary server is the *other* server. Records can't be edited."],
        ["The primary fails for good. What now?", "On the secondary, Zone Properties → General → **Change** zone type → **Primary** (the instructor says *change*, not *promote*). Update the clients' DNS settings and NS records."],
        ["Why do the serial numbers match on Svr1 and Svr4?", "The zone transferred successfully; both hold the same zone version."],
        ["Zone transfer port?", "**TCP 53** (AXFR full or IXFR incremental)."],
        ["Primary vs AD-integrated for redundancy?", "AD-integrated replicates multi-master through AD to every DC (no secondaries needed inside the domain). Secondaries are for non-DC servers or other platforms."],
    ], title="DNS lab: Questions & Answers")

    # ---------------- SG-34 ----------------
    s.h2("SG-34  Split DNS; DNS port")
    s.box("key", [
        "**DNS port: 53, UDP and TCP** (Windows and Linux, slide p3). **UDP 53** for normal queries (up to 512 bytes, or EDNS0 up to about 4 KB). **TCP 53** for **zone transfers (AXFR/IXFR)** and large responses (DNSSEC). Modern encrypted DNS: DoH = 443, DoT = 853.",
    ])
    s.p("**Split DNS** (split-brain) uses **separate internal and external DNS** for the same domain name for security (slides p38–p41):")
    s.steps([
        "**Internal** clients and servers send **all** DNS queries to the **AD-integrated DNS servers on the DCs** inside the firewall.",
        "The internal DNS returns IP addresses to them, including **internal** IPs for internal hosts.",
        "The **external DNS server in the perimeter network (DMZ)** answers Internet clients and **hosts only the records that must be resolved from outside**, such as the mail and web servers.",
    ])
    s.bullets([
        "The internal DNS **must stay separate and unreachable from outside** the firewall, so internal hostnames and IPs are never exposed. **External records must still be resolvable internally** (copy them into the internal zone, or forward).",
        "Course topology: the DMZ (133.12.10.x) holds WAP / ADFS / RD Gateway / IIS, while the LAN DC (192.168.239.x) runs AD DS / AD CS / DNS / DHCP.",
        "Alternative: **DNS policies** (2016+) answer differently based on the client subnet (`Add-DnsServerQueryResolutionPolicy`).",
    ])
    s.h3("DNS namespace design exercise (Adatum.com worksheet)")
    s.table(["Location", "Domain", "Example FQDNs"], [
        ["Root / external (perimeter network)", "**adatum.com**", "`www.adatum.com`, `ftp.adatum.com`, `mail.adatum.com`"],
        ["Internal root (separate from external)", "**int.adatum.com**", "—"],
        ["Human Resources", "**hr.int.adatum.com**", "`file1.hr.int.adatum.com`, `bkpg.hr.int.adatum.com`, `www.hr.int.adatum.com`, `wk8.hr.int.adatum.com`"],
        ["Sales", "**sl.int.adatum.com**", "`file1.sl.int.adatum.com`, `db.sl.int.adatum.com`, `wk1.sl.int.adatum.com`"],
        ["Production", "**pr.int.adatum.com**", "`file1.pr.int.adatum.com` … `file3.pr`, `wk2.pr.int.adatum.com`, `wk46.pr.int.adatum.com`"],
    ], widths=(2.3, 1.7, 3.5), size=8)
    s.p("Design rules from the exercise: every domain sits under adatum.com; the internal network uses a **different domain** (int.adatum.com) from the external one; each division gets its **own subdomain** (via **New Delegation** or a new domain folder); host names describe the function (`file`, `db`, `wk`, `www`, `bkpg`). The DNS-lab variant used `file.hr.adatum.com`.", size=9)

    # ---------------- SG-35 ----------------
    s.h2("SG-35  Protecting DNS; records; nslookup")
    s.h3("DNS security features (slides p28–p34)")
    s.table(["Protection", "What it does", "How / default"], [
        ["**DNSSEC**", "Adds digital signatures, giving resolvers **proof of identity (origin and integrity) of records and verified denial of existence**. **No confidentiality and no availability.**", "DNS Manager → zone → **DNSSEC → Sign the Zone**, or `Invoke-DnsServerZoneSign`"],
        ["**DNS socket pool**", "**Source-port randomization** for outgoing queries, so attackers can't guess the socket (anti cache poisoning)", "`dnscmd /Config /SocketPoolSize <0–10,000>` (default 2,500), then restart DNS"],
        ["**DNS cache locking**", "Cached records **can't be overwritten** while their TTL is still valid (a percentage of the TTL)", "`dnscmd /Config /CacheLockingPercent 100` or `Set-DnsServerCache -LockingPercent 100` (**default 100%**)"],
        ["**Secure cache against pollution**", "Ignores records in a referral that aren't from the queried domain", "Advanced tab, **on by default**"],
        ["**Secure dynamic updates**", "Only authenticated domain members can register or update their records", "AD-integrated zones only (default for them)"],
        ["**Restrict zone transfers**", "Transfer only to named secondaries (stops attackers mapping the network)", "Zone → Zone Transfers → *Only to the following servers*"],
        ["**Delegated administration**", "**Least privilege**: only *DnsAdmins* members manage DNS (DnsAdmins can even run code on DCs)", "Zone ACLs / DnsAdmins group"],
        ["Disable recursion on external DNS", "Stops the DMZ server being used as an open resolver (amplification attacks)", "Advanced → Disable recursion; `Set-DnsServerRecursion -Enable $false`"],
        ["Response Rate Limiting, DNS policies, split DNS, firewall, logging", "Limit floods (RRL, 2016+), filter queries, separate internal and external", "`Set-DnsServerResponseRateLimiting`"],
    ], widths=(1.7, 3.3, 2.5), size=8)
    s.tag("extra", "The last two rows and the default socket-pool size.")
    s.h3("DNSSEC (optional lab)")
    s.steps([
        "DNS Manager → right-click zone **adatum.com** → **DNSSEC → Sign the Zone** → *Customize zone signing parameters*.",
        "**Key Master**: the DNS server (a DC) that generates and manages the keys.",
        "**KSK** (Key Signing Key: signs the DNSKEY set; longer-lived) and **ZSK** (Zone Signing Key: signs all the other records). Accept or define the algorithms and rollover.",
        "**Next Secure**: **NSEC3** (hashed authenticated denial of existence, which **prevents zone walking**) vs NSEC.",
        "**Trust anchors**: enable distribution of trust anchors to all DNS servers (they appear under **Trust Points** as **DNSKEY**). Then confirm signing; new record types appear: **RRSIG, DNSKEY, NSEC3, (DS** in the parent).",
        "Make clients **require** validation with a GPO: GPMC → Computer Configuration\\Policies\\Windows Settings\\**Name Resolution Policy** (NRPT) → suffix `adatum.com` (or prefix, FQDN, subnet, any) → **Enable DNSSEC in this rule** + **Require DNS clients to check that name and address data has been validated** (optional IPsec) → Create → Apply. On the client: `gpupdate /force`, `gpresult /r`, `Get-DnsClientNrptPolicy`, `Resolve-DnsName ca-van-svr1.adatum.com -DnssecOk`.",
    ])
    s.h3("TTL, aging and scavenging (slides p32–p33)")
    s.bullets([
        "**TTL** = how long a record may be cached. Set it to suit the record (short before a migration).",
        "**Aging** applies to **dynamic** records (it can be enabled on static ones). Each record has a timestamp. **No-refresh interval** (default 7 days): the timestamp **can't** be refreshed, though other changes such as an IP change are allowed, which **cuts replication traffic**. **Refresh interval** (default 7 days): the timestamp may be refreshed.",
        "**Scavenging** deletes stale records **after no-refresh + refresh = 14 days by default**. It's **not enabled by default**, needs settings on both the server and the zone, and can seem to happen randomly. Static records (timestamp 0) are never scavenged.",
        "`Set-DnsServerScavenging -ScavengingState $true -ScavengingInterval 7.00:00:00 -ApplyOnAllZones` · `Set-DnsServerZoneAging adatum.com -Aging $true -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00`",
    ])
    s.h3("Advanced tab, debug logging and other server settings")
    s.bullets([
        "**Advanced tab** (slide p23): disable recursion (which also disables forwarders), **round robin** (rotates multiple A records for load distribution), **netmask ordering** (returns the IP on the client's subnet first), **secure cache against pollution**. **Round robin, netmask ordering and secure cache are on by default.**",
        "**Debug logging** (slide p27, disabled by default, with processing and storage overhead): Properties → Debug Logging → *Log packets for debugging* → direction (outgoing/incoming), contents (queries/transfers, updates, notifications), transport (**UDP/TCP**), type (request/response), filter by IP, log file path and max size (default 500,000,000 bytes). **Event Logging** and **Monitoring** (simple and recursive test queries) are separate tabs.",
    ])
    s.h3("nslookup and other DNS tools")
    s.code("""nslookup ca-van-svr1.adatum.com              # non-interactive (Server/Address lines = which DNS answered)
nslookup 192.168.239.1                       # reverse lookup (needs a PTR / reverse zone)
nslookup                                     # interactive mode:
  > server 192.168.239.4                     #   query a specific DNS server
  > set type=srv                             #   also: a, aaaa, mx, ns, soa, ptr, cname, txt, any
  > _ldap._tcp.dc._msdcs.adatum.com          #   find DCs (SRV: priority 0, weight 100, port 389)
  > set type=mx
  > alnorthamerica.com                       #   check mail routing
  > set debug                                #   show full packets / TTLs
  > ls -d adatum.com                         #   attempt a zone transfer (should be refused!)
  > exit
Resolve-DnsName adatum.com -Type MX -Server 192.168.239.1   ;  Resolve-DnsName www.bcit.ca -DnsOnly
ipconfig /displaydns   ipconfig /flushdns   ipconfig /registerdns     (client cache / re-register A + PTR)
Clear-DnsServerCache ; dnscmd /clearcache ; Test-DnsServer -IPAddress 192.168.239.1 ; dcdiag /test:dns
net stop netlogon && net start netlogon      # DC re-registers its SRV records (%systemroot%\\System32\\config\\netlogon.dns)""")
    s.box("trouble", [
        "**DNS Record Issues slides (p19–p20), alnorthamerica.com:** the first zone has its only **MX → mail.alnorthamerica.com** (an A record pointing at the same web-hosting IP 72.10.34.68), so mail goes to the web host. The second zone shows mail moved to Google Workspace: **five MX records (1 ASPMX, 5 ALT1/ALT2, 10 ALT3/ALT4)**, a TXT verification record, and the old `mail` A record removed. **Tools to identify the problem:** `nslookup -type=mx alnorthamerica.com`, `Resolve-DnsName -Type MX`, `dig mx`, online checkers (MXToolbox), `Test-NetConnection mail.alnorthamerica.com -Port 25`, the e-mail bounce headers.",
    ])
    s.h3("9 Windows DNS mistakes to avoid (lecture article)")
    s.table(["Mistake", "Do this instead"], [
        ["1. **\"Lonely island\"**: a DC points only to itself (127.0.0.1) for DNS", "Point each DC at a partner DC first and itself second, so it can still find the domain after a restart"],
        ["2. DNS servers **too far** from clients", "Put DNS near users (under about 25 ms) in every site"],
        ["3. **Not using AD-integrated zones**", "Use them for multi-master, secure and replicated zones"],
        ["4. **Requiring secure updates** when non-Windows clients exist", "Linux and macOS clients can't register with secure-only zones. Use DHCP to register them or allow nonsecure on a separate zone"],
        ["5. **Missing PTR / reverse zones**", "Create reverse zones; many apps and logs need reverse lookups"],
        ["6. **Forwarding to distant servers**", "Forward to nearby, fast resolvers"],
        ["7. **Forwarding loops**", "Make sure server A doesn't forward to B while B forwards to A"],
        ["8. **No aging or scavenging**", "Enable it to remove stale dynamic records"],
        ["9. **Zone transfers allowed to anyone or externally**", "Restrict transfers to named secondaries only"],
    ], widths=(3.6, 3.9), size=8)
    s.h3("Linux DNS with BIND (handout)")
    s.code("""yum install bind bind-utils                         # package 'named'
/etc/named.conf          options { listen-on port 53 { 127.0.0.1; 192.168.239.10; };  allow-query { localhost; 192.168.239.0/24; };
                                   recursion yes;  dnssec-validation yes; };
/etc/named.rfc1912.zones zone "Adatum.com" IN { type master; file "Adatum.com.db"; allow-update { none; }; };
/var/named/Adatum.com.db $TTL 86400
                         @ IN SOA ns1.Adatum.com. root.Adatum.com. ( 2024010101 ; serial
                                     1D ; refresh   1H ; retry   1W ; expire   3H ; minimum )
                         @ IN NS ns1.Adatum.com.     ns1 IN A 192.168.239.10     www IN A 192.168.239.20
chown named:named /var/named/Adatum.com.db ; named-checkconf ; named-checkzone Adatum.com /var/named/Adatum.com.db
firewall-cmd --permanent --add-port=53/udp ; firewall-cmd --permanent --add-port=53/tcp ; firewall-cmd --reload
systemctl enable --now named ; systemctl restart named ; netstat -antp | grep :53
host -t ns Adatum.com ; dig @localhost www.Adatum.com""")
    s.p("A Windows server can be a **secondary** to this BIND primary (add `allow-transfer { <windows-ip>; };`).", size=9)

    s.h3("Week 9 discussion: model answers")
    s.tag("model")
    s.qa([
        ["Iterative vs recursive queries?", "Recursive: the client asks its DNS server for the **complete** answer, and that server does the work. Iterative: each server returns its best answer or a **referral**, and the asking DNS server walks root → TLD → authoritative itself."],
        ["What is split DNS?", "Separate internal (AD-integrated, internal IPs) and external (DMZ, public records only) DNS for the same namespace, so internal names aren't exposed (SG-34)."],
        ["Authoritative vs non-authoritative?", "Authoritative: from a server holding the zone (SOA + NS). Non-authoritative: from a server's cache of an answer learned elsewhere."],
        ["What is a glue A record?", "An A record for a name server that sits **inside the zone being delegated** (ns1.bby.adatum.com for bby.adatum.com). The parent stores it with the NS delegation so resolvers can reach the NS without a circular lookup."],
        ["What is WINS?", "Windows Internet Name Service: a legacy NetBIOS name-to-IP database (flat 15-character names) for pre-AD apps. Replaced by DNS (GlobalNames zone)."],
        ["Primary vs secondary vs stub zone?", "Primary = writable master. Secondary = read-only transferred copy for redundancy and load. Stub = only SOA/NS/glue, so it points to the authoritative servers and isn't authoritative itself."],
        ["Forwarder vs conditional forwarder vs stub zone? (DNS Topics doc)", "A forwarder sends **all** unresolved queries to one upstream server. A conditional forwarder sends queries **for one domain** to specified IPs (static, and it beats general forwarders). A stub zone does the same job but **learns and updates the NS list automatically** from the target zone."],
    ], title=None)
