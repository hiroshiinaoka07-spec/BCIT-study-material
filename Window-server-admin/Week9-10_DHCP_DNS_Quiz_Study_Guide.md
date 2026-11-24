# ACIT 3420 quiz study guide — Week 9 (Module 8: DNS) and Week 10 (Module 9: DHCP)

Sources: Module 8 slides (`ACIT3420 DNS`), DNS Topics, *9 Windows DNS mistakes to avoid*, Linux DNS handout, Week 9 Lab 6 (secondary zone, namespace design, DNSSEC, DNS exercise), Module 9 slides (`ACIT3420 DHCP`), DHCP Lease Time, Superscopes handout, and Week 10 Lab 7 (deploy DHCP, relay agent, failover, policies).

The Week 9 discussion board is the closest thing to a quiz outline. It asks: what DNS is and why you need it, the four zone types, every DNS record, how you protect DNS, and forwarder vs conditional forwarder vs stub zone. Week 10 is the DHCP role: DORA, leases, scopes, relay, superscopes, failover, and troubleshooting.

---

## Part 1 — Week 9, Module 8: Windows Server DNS

### Learning objectives

- Implement DNS servers
- Configure zones and records
- Configure name resolution between zones
- Integrate DNS with AD DS
- Configure advanced DNS settings (forwarders, root hints, logging, DNSSEC, aging, scavenging, delegation)

### What DNS is, and why you need it

**Domain Name System (DNS)** is the naming service used by TCP/IP and the Internet. A client that wants `www.bcit.ca` or a corporate server does not know the IP. DNS looks it up, the same way a phone book maps a name to a number. DNS servers are also called **name servers**.

**Port 53, TCP and UDP**, on both Windows and Linux.

- **UDP 53** carries ordinary queries.
- **TCP 53** carries zone transfers (AXFR / IXFR) and large answers, including DNSSEC.

What DNS does for this course:

| Job | How |
|---|---|
| Name → IP | Forward lookup, **A** (IPv4) and **AAAA** (IPv6) |
| IP → name | Reverse lookup, **PTR** |
| Find a mail server | **MX** |
| Find a network service (especially a domain controller) | **SRV** |
| Give an extra name to an existing host | **CNAME** |
| Say which servers are authoritative | **NS** and **SOA** |
| Publish text, including anti-spoofing policy | **TXT / SPF** |

**Active Directory depends on DNS.** Clients find domain controllers, global catalog servers, and Kerberos through SRV records. If DNS is wrong, logon, Group Policy, and replication fail.

### FQDN and the hierarchy

A **hostname** plus a **domain** plus a **top-level domain** is a **fully qualified domain name (FQDN)**.

`AcctDirPC.adatum.com`

- Hostname: `AcctDirPC`
- Second-level domain: `adatum` (registered to a person or organization)
- Top-level domain: `com` (generic) or a country code (`us`, `uk`, `de`, `jp`, `ca`, `au`)

The tree on the hierarchy slide, read from the root down:

```
Root (.)
├── com
│   ├── microsoft
│   │   ├── server1
│   │   └── www
│   ├── intel
│   └── contoso
│       ├── www
│       ├── corporate
│       │   └── server1          → server1.corporate.contoso.com
│       └── sales
│           └── computer1        → computer1.sales.contoso.com
├── edu
│   └── mit
├── gov
│   └── usa
└── au
    └── gov
```

A host is one computer or device in a domain. A **namespace** is the whole hierarchy, so a node can be named relative to the root, for example `computer01.unitedstates.microsoft.com`.

### DNS components

| Component | Meaning |
|---|---|
| DNS namespace | Hierarchical names: root → TLD → second-level domain → subdomains → hosts |
| DNS server | Holds the database of names and addresses and answers queries |
| DNS zone | One **portion** of the namespace, split off so it can be administered separately. It holds the records |
| DNS resolver | The client service that asks for host-to-IP mappings (Windows DNS Client, which also caches answers) |
| Resource records | The actual database rows: A, AAAA, SRV, PTR, and the rest |

### How a name is resolved (slide: www.bcit.ca)

1. The workstation sends a **recursive** query to its local DNS server: “What is the IP of www.bcit.ca? Give me the final answer.”
2. If the local server is not authoritative and has no forwarder that can answer, it starts an **iterative** walk at the **root**.
3. The root returns a referral to the **.ca** servers.
4. .ca returns a referral to the **bcit.ca** servers.
5. bcit.ca (authoritative) returns **142.232.230.10**, and the local server hands that answer back to the workstation.

| Query type | Who asks | What they get back |
|---|---|---|
| **Recursive** | Usually the client, asking its configured DNS server | The final answer, or an error. The server does the work |
| **Iterative** | A DNS server asking another DNS server | The best answer that server has, often a **referral** to someone closer |

### Authoritative vs non-authoritative

- **Authoritative:** the answer comes from a server that holds a **complete copy** of that zone. A complete copy has a valid **SOA**, valid **NS** records, and those NS records match the servers listed in the SOA. A server is authoritative **only for the zones it holds**.
- **Non-authoritative:** the answer comes from **cache**. The server learned it from someone else and is not authoritative for that domain. `nslookup` labels cached answers this way.

### Five steps to deploy DNS

1. Install DNS on one or more servers (redundancy and performance; a DNS server at each site).
2. Configure the DNS servers.
3. Create **forward** and **reverse** lookup zones.
4. Add resource records to both.
5. Point clients at those DNS servers.

Slide question: **Can DNS run on Nano Server? Yes.** DNS is a role you can install there.

Lab hardware note: most DNS servers are light. The secondary-zone lab quotes about a 1.4 GHz 64-bit CPU, 512 MB RAM, and 32 GB disk, unless the server answers thousands of queries a minute.

Install path: Server Manager → Manage → Add Roles and Features → Role-based → **DNS Server** → Add Features → Install. PowerShell on the slide for records is below; the role itself is `Install-WindowsFeature DNS -IncludeManagementTools`.

### Forward vs reverse zones

| Zone | Question it answers | Typical records |
|---|---|---|
| **Forward lookup** | Name → IP | A, AAAA, CNAME, MX, SRV, NS, SOA, TXT |
| **Reverse lookup** | IP → name | **PTR**, in an `in-addr.arpa` zone (IPv6: `ip6.arpa`) |

Example reverse zone for 192.168.239.0/24: `239.168.192.in-addr.arpa`. The octets are reversed.

### Zone types (memorize this table)

The New Zone Wizard offers Primary, Secondary, and Stub, plus the checkbox **Store the zone in Active Directory** (only if the DNS server is a **writable domain controller**).

| Type | Copy | Where it lives | What to remember |
|---|---|---|---|
| **Primary** | **Read/write.** This is the authority you edit | Text file, `%systemroot%\System32\dns\<zone>.dns` | Easy to back up and restore. Changes can be made only while the primary is available. One primary master in a classic (non-AD) design |
| **Secondary** | **Read-only** copy, filled by **zone transfer** | Text file | Can be a copy of a primary, another secondary, **or an AD-integrated zone**. Used for remote sites, load balancing, and fault tolerance. **Windows can be secondary to a Unix/BIND primary.** You cannot add records on it |
| **Stub** | Only the records needed to **find the name servers**: **SOA, NS, and glue A** | File or AD | The server is **not authoritative**. It redirects the query to a server that can answer, and it **updates the NS list by itself** when the real name servers change. Saves bandwidth because it does not copy the whole zone |
| **AD-integrated** | Read/write on **every DC** that holds the zone (**multi-master**) | Inside AD DS, not a zone file | **Only on a domain controller.** Replicated by AD at the **attribute** level. Supports **secure dynamic updates** and **ACLs** (delegated admin). High availability. **Harder to restore after a disaster** than a simple zone file |

**Benefits of an AD-integrated zone (slide list):**

- Multi-master updates (any DC with the zone can accept a change)
- Zone data replicates with AD DS
- Secure dynamic updates
- Detailed security: delegate zones and set ACLs

AD replication scopes you should be able to name:

| Scope | Replicates to |
|---|---|
| All DNS servers in this **forest** | Every DC running DNS in the forest (`ForestDnsZones`; `_msdcs` is typically forest-wide) |
| All DNS servers in this **domain** (usual default) | DCs running DNS in that domain (`DomainDnsZones`) |
| All domain controllers in this domain (Windows 2000 compatible) | Every DC, including ones without DNS |
| Custom application partition | Only the DCs you enlist |

### Resource records — explain each one

**Forward lookup**

| Record | What it maps | Details that show up on a quiz |
|---|---|---|
| **A** | Hostname → **IPv4** | `CA-VAN-Svr3` → `192.168.239.4` |
| **AAAA** | Hostname → **IPv6** | Same idea as A, for IPv6 |
| **CNAME** | Alias → the real (canonical) name | `www` → `web1.adatum.com`. The target should have an A/AAAA. Do not point MX at a CNAME |
| **MX** | Domain → mail server | Preference is a number. **Lower number is tried first.** Data looks like `10 mail.adatum.com.` |
| **SRV** | Service → host, port, protocol | Fields: **service, protocol, priority, weight, port, target**. Needs a matching **A** record for the target. Usually created automatically by the application (domain controllers do this themselves) |
| **NS** | Domain → authoritative name servers | Who is allowed to answer for the zone |
| **SOA** | **One per zone** | Primary name server, administrator email, **serial number**, refresh, retry, expire, minimum TTL |
| **TXT / SPF** | Free text | **SPF** lists which hosts may send mail for the domain. Together with MX it is how you fight **email spoofing**. Also used for site verification (`google-site-verification=...`) |

**Reverse lookup**

| Record | What it maps |
|---|---|
| **PTR** | IP address → name |

**Glue A record:** an A record for a name server that lives **inside** the zone being delegated (for example `ns1.bby.adatum.com` while delegating `bby.adatum.com`). The parent zone stores that A record next to the NS record so resolvers can reach the name server without a circular lookup.

**DHCID:** not a normal host record. DHCP **name protection** writes it so a non-Windows device cannot overwrite a Windows computer’s DNS registration.

**PowerShell from the slide:**

```powershell
Add-DnsServerResourceRecordA -ZoneName Adatum.com -Name CA-VAN-Svr3 -IpAddress 192.168.239.4
```

**SOA fields (Windows defaults used in the DNS lab)**

| Field | Typical value | Meaning |
|---|---|---|
| Serial number | Increases on every change | A secondary transfers only when the primary’s serial is **higher** |
| Primary server | `ca-van-svr1.adatum.com` | The master name server |
| Responsible person | `hostmaster.adatum.com.` | Admin email. The first dot stands for `@` → `hostmaster@adatum.com` |
| Refresh | **15 minutes** | How often the secondary checks the serial |
| Retry | **10 minutes** | How soon to retry after a failed refresh |
| Expires after | **1 day** | If the secondary cannot reach the master this long, it **stops answering** |
| Minimum (default) TTL | **1 hour** | How long resolvers may cache records from this zone (also the negative-cache TTL) |

**SRV records you can see in `_msdcs.Adatum.com` (the DNS Manager screenshot)**

| Name | Protocol | Port | What it is |
|---|---|---|---|
| `_gc` | TCP | **3268** | Global catalog |
| `_kerberos` | TCP and UDP | **88** | Kerberos |
| `_kpasswd` | TCP and UDP | **464** | Kerberos password change |
| `_ldap` | TCP | **389** | LDAP / domain controller locator |

Format in the console is `[priority][weight][port] hostname`, for example `[0][100][389] CA-VAN-Svr1.Adatum.com`.

**Why SRV records matter (slide benefits):**

- Domain controllers register SRV records **dynamically, by service and by site**.
- A client uses the SRV records for **its own site** first, and only then tries a DC across a WAN link.
- That keeps inter-site traffic down.

### The alnorthamerica.com record problem (slides “DNS Record Issues”)

**Before:** the zone’s only MX is `10 mail.alnorthamerica.com.`, and `mail` is an **A** record at **72.10.34.68**, the same address as the apex, wildcard, `ftp`, and `www`. Mail is being delivered to the **web host**, not a mail platform.

**After:** the `mail` A record is gone. Mail is five Google MX records, and a TXT verification record is present:

| Preference | Mail exchanger |
|---|---|
| **1** | `ASPMX.L.GOOGLE.COM.` (tried first) |
| **5** | `ALT1.ASPMX.L.GOOGLE.COM.` |
| **5** | `ALT2.ASPMX.L.GOOGLE.COM.` |
| **10** | `ALT3.ASPMX.L.GOOGLE.COM.` |
| **10** | `ALT4.ASPMX.L.GOOGLE.COM.` |

TTL on those rows is **43200** seconds (12 hours).

**Tools the slide asks for:** `nslookup` (`set type=mx`), `Resolve-DnsName -Type MX`, `dig`, an online checker such as MXToolbox, and a port-25 test (`Test-NetConnection mail.alnorthamerica.com -Port 25`). Bounce headers from a failed message also show which host accepted the mail.

### Forwarder vs conditional forwarder vs stub zone

This is a listed discussion question. Learn the difference cold.

By default, if the DNS server does not know the answer it walks the tree itself (root → TLD → authoritative). A **forwarder** changes that.

| Mechanism | When it is used | How it behaves |
|---|---|---|
| **Forwarder** | All names this server cannot answer itself (external / offsite names) | Sends those queries to one or more upstream DNS servers (ISP, or 8.8.8.8). One place for a cache, one server allowed through the firewall, controlled outbound traffic. Server Properties → **Forwarders**. Leave “use root hints if no forwarders are available” if you still want a fallback |
| **Conditional forwarder** | **One specific domain name**, which can even be a **different TLD** (a partner such as `indy.com`) | Every query for that name takes one path, to the IP you type. It **overrides** the general forwarder for that name only. It is a **static** list of IPs. It can be stored in AD and replicated. Lives under the **Conditional Forwarders** node |
| **Stub zone** | Usually a name **below** a higher-level domain, a **delegation below a delegation** | Same job as pointing at the other domain’s name servers, but the list of NS (and glue A) records **updates itself**. Not authoritative |

**Why forwarders exist (slide question):** you control where queries go and how much traffic leaves the network, which makes resolution faster and more predictable for internal computers.

**Root hints:** the built-in list of root name servers. A root server answers records in the root zone and otherwise returns the authoritative servers for the right TLD. Your DNS server uses root hints to **start** an iterative query. They matter for any server that is authoritative only for a lower part of the namespace and still has to find other zones. Root hints are used when **no forwarder is configured, or the forwarders fail**.

**Zone delegation** is related but different. A subdomain (`sales.adatum.com`) can be its own zone on another server. The parent publishes NS records (and glue) with **New Delegation**. That spreads query load and lets another team administer the child zone.

**Slide guidance, worded as a rule:**

- Conditional forwarder: the other name is a **different domain**, you want **all** resolution for it to follow one path.
- Stub zone: the name sits **under** a domain you already know about, and you want the NS list kept current without editing it by hand.

### Split DNS

Organizations keep **internal DNS** and **external DNS** separate.

1. Internal clients and servers send **all** queries to the **AD-integrated DNS servers** on the domain controllers, inside the firewall.
2. Those servers answer with internal addresses (and they must still be able to resolve the company’s own public names, such as mail and web).
3. An **external DNS server in the perimeter (DMZ)** answers Internet clients. It hosts **only** records that must be visible from outside (mail, web, FTP).

The internal zone stays unreachable from outside the firewall so internal host names and IPs are not published. External records still have to resolve for internal users.

### Secondary zone lab (what the quiz can pull from the steps)

Topology in the lab: primary is the domain controller (**CA-VAN-SVR1**, 192.168.239.1, zone `adatum.com`). Secondary is **CA-VAN-SVR4**.

1. Install the DNS role on Svr4.
2. DNS Manager → Forward Lookup Zones → **New Zone** → **Secondary** → zone name `adatum.com` → master IP **192.168.239.1**.
3. The zone shows **“Zone not loaded by DNS server.”** Cause: the primary has not allowed the transfer.
4. On the **primary**: zone → Properties → **Zone Transfers** → **Allow zone transfers** → **Only to the following servers** → add Svr4’s IP → **Notify** those same servers.
5. Back on Svr4, refresh or **Transfer from Master**. Records appear and match the SOA serial on both servers.
6. You **cannot** create a record on the secondary. It is read-only. Edits happen on the primary, and the serial number bumps so the secondary picks them up.

If the primary is gone for good, on the secondary open the zone → General → **Change** the zone type to **Primary**, then point clients and NS records at it.

Zone transfer uses **TCP 53**.

### Advanced server settings (Advanced tab)

Defaults that are **already on**:

- **Round robin** — if several A records exist for one name, the server **rotates** which address it returns first. That spreads load.
- **Netmask ordering** — if several addresses exist, prefer the one on the **client’s subnet**.
- **Secure cache against pollution** — ignore extra records in a referral that are not for the name that was queried (anti cache-poisoning).

You can also **disable recursion** on this tab. A server that is only supposed to answer for its own zones (a public authoritative server) should not recurse, or it can be abused as an open resolver.

### Debug logging

DNS **debug logging** writes a detailed file of DNS packets and messages. It is a troubleshooting tool. It costs CPU and disk, so leave it off when you are finished. It is separate from the ordinary event log and from the Monitoring tab (simple query test and recursive query test).

### TTL, aging, scavenging

| Term | Meaning |
|---|---|
| **TTL** | How long a resolver may **cache** a record. Shorten it before you change an address so old data dies quickly |
| **Aging** | Applies to **dynamic** records (you can turn it on for static ones too). Each dynamic record has a **timestamp** |
| **No-refresh interval** | During this window the **timestamp cannot be updated**. Other changes are still allowed (a new IP, a port change). This **cuts replication traffic**. Default **7 days** |
| **Refresh interval** | During this window **any** data can change, including the timestamp. Default **7 days** |
| **Scavenging** | Deletes records that were **not refreshed** after no-refresh + refresh. Default total is **14 days**. **Off by default.** Must be turned on at the **server and the zone**. It can look like it runs at odd times. Static records (timestamp 0) are not scavenged |

### How you protect DNS

The security goal: stop false records from being added, and stop clients from being sent to the wrong address (phishing).

| Control | What it stops | How |
|---|---|---|
| **DNSSEC** | Forged or altered records | Proves **identity** of the records and gives a **verified denial** (“this name really does not exist”). It does **not** provide confidentiality or availability |
| **Socket pool** | An attacker guessing the source port of a query (cache poisoning) | Random source ports. `dnscmd /Config /SocketPoolSize` with a value from **0 to 10,000** |
| **Cache locking** | Overwriting a cached record while its TTL is still valid | `dnscmd /Config /CacheLockingPercent` or `Set-DnsServerCache -LockingPercent`. **100** means the record cannot be overwritten for the whole TTL |
| **Secure cache against pollution** | Bogus extra records stuck into a referral | Advanced tab, on by default |
| **Secure dynamic updates** | Unauthenticated clients registering names | AD-integrated zones only |
| **Restrict zone transfers** | An outsider downloading your whole zone (network map) | “Only to the following servers,” never “to any server,” and not to the Internet |
| **Least privilege** | Too many people administering DNS | DnsAdmins and zone ACLs. Only people who need DNS should have it |
| **Split DNS** | Publishing internal names outside | Separate internal and external zones |
| **Disable recursion** on a public authoritative server | Being used in an amplification attack | Advanced tab |
| **Debug / audit logging** | You cannot investigate what you did not record | Turn on while troubleshooting |

**DNSSEC lab (optional, still fair game):**

1. DNS Manager → zone `adatum.com` → **DNSSEC → Sign the Zone** → **Customize zone signing parameters**.
2. **Key Master** is the DNS server (the DC) that generates and manages the keys.
3. **KSK (Key Signing Key)** signs the DNSKEY set. **ZSK (Zone Signing Key)** signs the other records. Accept the defaults in the lab.
4. **NSEC3** (the lab’s “nsce3”) is authenticated denial of existence using hashes, so an attacker cannot walk the zone name by name. **NSEC** is the older, walkable version.
5. **Enable distribution of trust anchors.** They show up under **Trust Points** as **DNSKEY**. Signing also adds **RRSIG**, **DNSKEY**, **NSEC3**, and a **DS** record belongs in the parent.
6. You can **unsign** the zone later.
7. Clients do not validate until policy says so. In GPMC, create a GPO → Computer Configuration → Policies → Windows Settings → **Name Resolution Policy** (NRPT).
   - **Suffix** `adatum.com` covers that name and its children.
   - **Prefix** `www` covers any host whose name starts with www.
   - **FQDN** is one exact name.
   - **Subnet (IPv4/IPv6)** applies to reverse lookups.
   - **Any** is the default rule.
8. On the DNSSEC tab: **Enable DNSSEC in this rule**, and **Require DNS clients to check that name and address data has been validated**. IPsec between client and DNS server is optional.
9. On the client: `gpupdate /force`, then `gpresult /r`, and confirm the GPO applied.

### Delegated administration

DNS is critical. Restrict who can change it. **Least privilege** applies: DnsAdmins (and zone ACLs on an AD-integrated zone) instead of giving everyone Domain Admin.

### Namespace design exercise (Adatum)

Rules from the lab:

- Root name is **adatum.com**. Every other domain is **under** it.
- Internal network uses a **different domain** from the external network.
- Three internal divisions, each its **own subdomain**: Sales, Human Resources, Production.
- Host names describe the **function** (file, db, www, mail, wk for workstation).
- Three perimeter servers (Web, FTP, email) stay in **adatum.com**, the external name.

One layout that satisfies the worksheet:

| Place | Domain | Example FQDNs |
|---|---|---|
| External / perimeter | `adatum.com` | `www.adatum.com`, `ftp.adatum.com`, `mail.adatum.com` |
| Internal root | `int.adatum.com` | (the internal parent; not published outside) |
| Human Resources | `hr.int.adatum.com` | `file1.hr.int.adatum.com`, `www.hr.int.adatum.com` |
| Sales | `sl.int.adatum.com` | `file1.sl.int.adatum.com`, `db.sl.int.adatum.com` |
| Production | `pr.int.adatum.com` | `file1.pr.int.adatum.com`, `wk2.pr.int.adatum.com` |

The DNS-lab variant sometimes uses names directly under the division, such as `file.hr.adatum.com`. Either way, external hosts stay in `adatum.com`, and each division is its own child zone (New Delegation or its own zone).

### Nine Windows DNS mistakes

| # | Mistake | Do this instead |
|---|---|---|
| 1 | **Lonely island.** A DC uses only itself (`127.0.0.1` or its own IP) for DNS. With AD-integrated DNS it can become an island and replication fails | Point each DC at **another DC first**, itself second. The first DC may point at itself only until the second DC exists |
| 2 | DNS servers too far from clients | Keep a DNS server local. Aim for under 25 ms, under 50 ms is acceptable. A caching-only DNS server on a file/print server is enough if the site has no DC |
| 3 | AD zones stored as files instead of in AD | Use **AD-integrated** zones for internal DNS: multi-master, replicated, secure updates |
| 4 | **Secure updates only**, in a network that also has Linux or Mac | Those clients cannot register. Allow DHCP to register them, or allow nonsecure updates on a zone that needs them. The article’s point is that more registered names make machines easier to find. (Secure-only is still the right default for a pure Windows domain.) |
| 5 | No **PTR** / no `in-addr.arpa` zone | Build the reverse zone. Logs and many apps need IP → name |
| 6 | Forwarding to a DNS server on the other side of the world | Forward to a **nearby** resolver. A Tokyo DC that forwards to Dallas gets slow lookups and non-local CDN answers |
| 7 | **Forwarding loop.** A forwards to B and B forwards to A | Queries are stateless, so the two servers bounce the same question forever and can fill a WAN link. Forward one way, or use root hints |
| 8 | Aging and scavenging left off | Stale dynamic records pile up (machines that were shut down years ago). Turn scavenging on |
| 9 | Zone transfers open to the world, or blocked from your own secondaries | Allow transfers **internally to the servers you name**. Do not allow them to arbitrary external hosts |

### Linux DNS (BIND) — enough to recognize the handout

The handout builds BIND (`named`) on `Ca-Van-Ns1` at **192.168.239.10**.

- Config: `/etc/named.conf`
- Zone files: `/var/named` (example `Adatum.com.db`)
- `listen-on port 53 { 127.0.0.1; 192.168.239.10; };`
- `recursion yes;` and `dnssec-validation yes;` for a recursive resolver. The file’s own comment: an **authoritative** server should **not** recurse, and a public recursive server must limit `allow-query` or it becomes an amplification amplifier
- Root hints zone: `zone "." IN { type hint; file "named.ca"; };`
- A master zone: `type master; file "Adatum.com.db";`
- Open the firewall: `firewall-cmd --permanent --add-port=53/udp` and `53/tcp`, then `--reload`
- `systemctl restart named`, then `netstat` shows TCP 53 on 192.168.239.10 and 127.0.0.1 (and TCP 953, BIND’s control channel)
- A Windows DNS server can be a **secondary** of this BIND primary if the zone allows transfers to the Windows server’s IP

### DNS commands worth knowing

```text
nslookup ca-van-svr1.adatum.com          name → IP (also shows which server answered)
nslookup 192.168.239.1                   IP → name (needs a PTR)
nslookup
  server 192.168.239.4                   ask a specific DNS server
  set type=mx                            also: a, aaaa, srv, ns, soa, ptr, cname, txt
  adatum.com
  set type=srv
  _ldap._tcp.dc._msdcs.adatum.com
  ls -d adatum.com                       zone transfer; should FAIL if transfers are locked down
ipconfig /displaydns
ipconfig /flushdns
ipconfig /registerdns                    client re-registers its A and PTR
```

```powershell
Resolve-DnsName adatum.com -Type MX -Server 192.168.239.1
Resolve-DnsName ca-van-svr1.adatum.com -DnssecOk
Get-DnsClientNrptPolicy
Clear-DnsServerCache
```

Restarting the **Netlogon** service on a DC re-registers its SRV records (`net stop netlogon` / `net start netlogon`). The file the DC registers from is `%systemroot%\System32\config\netlogon.dns`.

### Week 9 discussion — short answers

**What is DNS? Why do we need it? What does it do?**
DNS is the TCP/IP naming service (port 53 TCP/UDP) that maps FQDNs to IPs and IPs back to names, and publishes where services and mail servers are. Clients, including AD clients looking for a domain controller, cannot connect by name without it.

**Primary vs secondary vs stub vs AD-integrated?**
Primary is the writable copy in a zone file. Secondary is a read-only transferred copy for load and fault tolerance. Stub holds only SOA, NS, and glue A records and is not authoritative. AD-integrated stores the zone in AD on domain controllers, is multi-master, replicates with AD, and supports secure dynamic updates.

**Explain each record.**
Use the record table above. If you only remember six: A/AAAA (host), PTR (reverse), CNAME (alias), MX (mail, low number wins), SRV (service + port, how AD finds DCs), NS + SOA (who is authoritative, one SOA per zone).

**How do you protect DNS?**
DNSSEC, socket-pool randomization, cache locking, secure cache against pollution, secure dynamic updates, zone transfers limited to named servers, least privilege, split DNS, and recursion disabled on public authoritative servers.

**Forwarder vs conditional forwarder vs stub?**
A forwarder gets every query the server cannot answer. A conditional forwarder gets queries for one domain, sent to a fixed IP list. A stub zone also aims queries at another domain’s name servers, but it keeps that NS list up to date by itself and is the usual choice for a delegated child zone.

---

## Part 2 — Week 10, Module 9: DHCP

### Module map

- Overview of the DHCP server role
- Deploying DHCP (install, authorize, scopes, options, relay)
- Managing and troubleshooting (security, policies, superscopes, multicast, high availability, failover, database, migration)

### What DHCP does

**Dynamic Host Configuration Protocol** hands out IP configuration automatically: address, subnet mask, default gateway, DNS servers, DNS domain name, and other options.

Windows DHCP supports **IPv4 and IPv6**.

Ports: server **UDP 67**, client **UDP 68**. (DHCPv6 is UDP 547 / 546. The IPv4 pair is the one this module drills.)

| Automatic (DHCP) | Manual (static) |
|---|---|
| Supplies addresses automatically | You type every address |
| Pushes a consistent set of options | A typo is easy |
| Change an option once and clients pick it up | A wrong gateway or DNS server breaks communication |
| Computers can move without a renumbering project | Every move is admin work |

A **non-DHCP client** (server, router, some printers) keeps a **static** address. That address must be **excluded** from the pool or reserved, or the server may lease it to someone else.

The client does **not** have to be domain-joined. Phones, printers, and Linux hosts get leases. Authorization in AD is a requirement on the **server**, not the client.

### Lease generation — DORA

All four messages on the generation slide are **broadcasts**. Routers do not forward broadcasts, which is why a relay agent exists.

| Step | Message | Who → who | What it means |
|---|---|---|---|
| 1 | **DHCPDISCOVER** | Client broadcasts | “Is there a DHCP server?” Source is 0.0.0.0:68, destination 255.255.255.255:67 |
| 2 | **DHCPOFFER** | Every server with a free address | “You can have this IP, mask, lease, and options.” |
| 3 | **DHCPREQUEST** | Client broadcasts | “I accept **this** server’s offer.” The broadcast tells the other servers to take their offers back |
| 4 | **DHCPACK** | The chosen server | “The lease is yours.” It is written to the DHCP database. **DHCPNAK** means refused; the client starts over |

Memory hook: **D**iscover, **O**ffer, **R**equest, **A**cknowledge.

Other messages worth one line each:

- **DHCPDECLINE** — the client found the address already in use (ARP conflict).
- **DHCPRELEASE** — the client gives the address back (`ipconfig /release`).
- **DHCPINFORM** — the client already has an address and only wants options.

### Lease renewal — 50%, 87.5%, 100%

The lease article calls the halfway timer **T1** and the later timer **T2**. An 8-day lease renews at day 4 and rebinds at day 7.

| Point | What the client does | How it is sent |
|---|---|---|
| **50%** (T1), renewal | **DHCPREQUEST** straight to the server that issued the lease. **DHCPACK** extends it and **resets both timers** | Unicast to that server |
| **87.5%** (T2), rebinding | The 50% attempt failed (server down). The client asks **any** DHCP server to extend the lease | Broadcast |
| **100%** | The lease is dead. The client stops using the address and starts **DORA** again with DHCPDISCOVER. If nobody answers, Windows uses **APIPA, 169.254.0.0/16** | Broadcast |
| Boot with a lease still valid | The client tries to get **the same** address back before asking for a new one | REQUEST |
| You force it | `ipconfig /renew` and `ipconfig /release` | — |

The slide’s wording: if renewal fails after 50%, the renewal process runs again after 87.5%. If that also fails, generation starts over with DISCOVER.

Worked example from the lease article: lease = 8 days. At day 4 the client tries to renew. If it succeeds on day 5, the 8-day clock starts over. A 1-hour guest lease tries to renew at 30 minutes; if it succeeds at 35 minutes, that address stays reserved until the new hour ends (about 95 minutes total in the article’s coffee-shop math).

### How long should the lease be?

| Network | Lease | Why |
|---|---|---|
| Wired office (Windows scope default) | **8 days** | Desktops stay put. A shorter lease only adds DHCP traffic |
| Home | **24 hours** (1440 minutes, 86400 seconds) is the usual router default; 8 days is also fine | The device count barely changes |
| Wireless | **About 24 hours or less** | Devices leave and hold addresses if the lease is long |
| Office guest | **About 8 hours** | One visit is about a work day |
| Hotspot / café | **About 1 hour** | High turnover |

Keep about **20% of the pool free**. Size the pool for the number of devices and add 20%, or shorten the lease until it fits.

Café example: 400 visitors a day, 30–60 minutes each, pool of 200 addresses (192.168.0.10–192.168.0.210). A 24-hour lease fills the pool after the first 200 guests and everyone else is stuck. A **1-hour** lease returns addresses fast enough that the same 200 addresses can serve on the order of 130 guests an hour.

Leave addresses **outside** the pool for static devices. A common pattern is a pool from `.10` to `.200`, with servers and printers at `.201` and above (or below `.10`). A printer left on DHCP can change address after a long shutdown, and every PC that was pointed at the old address breaks.

The lease article’s last line: when you build DHCP and DNS together in a company, also turn on **DNS scavenging** so dynamic registrations do not live forever.

### Install and post-install

The DHCP server itself needs a **static IP**. Lab server: **CA-VAN-SVR1, 192.168.239.1**.

Install:

- Server Manager → Add Roles and Features → **DHCP Server**, or
- `Add-WindowsFeature DHCP` (current equivalent: `Install-WindowsFeature DHCP -IncludeManagementTools`)

**Post-install wizard** (the flag in Server Manager), in this order:

1. **Create security groups**
   - **DHCP Administrators** — domain local. Full management of scopes, options, and leases. Authorizing a server in AD still needs **Enterprise Admin**.
   - **DHCP Users** — domain local. **Read-only** console access.
   - The Users container screenshot also shows **DnsUpdateProxy** (global): DNS clients permitted to register records, used when DHCP registers names on behalf of clients.
2. **Restart the DHCP Server service** so those groups take effect. The wizard says this in the summary.
3. **Authorize the server in AD DS** as `ADATUM\Administrator`. You can skip authorization, but a domain-joined server that is not authorized will not lease addresses.

**Add/Remove Bindings** (right-click the server): choose which NIC actually hands out leases. A multi-homed server with the wrong binding offers addresses on the wrong network.

### Authorization

A domain-joined Windows DHCP server asks a domain controller for the list of authorized servers when the service starts.

- If **its own IP is on the list**, the service starts and answers clients.
- If **its IP is not on the list**, the service does **not** start serving clients.

That blocks a rogue **domain-joined Windows** DHCP server. It does **not** block a rogue router, access point, or non-domain device. For those you use switch port security or DHCP snooping, and you disconnect unused wall ports.

Authorize while logged on as an **Enterprise Admin** (`Adatum\Administrator`). A local admin gets **error 20079**, and “use the following user’s credentials” is greyed out. **Unauthorize** a server before you retire it, or its address stays on the authorized list.

```text
netsh dhcp show server
Get-DhcpServerInDC
Add-DhcpServerInDC -DnsName ca-van-svr1.adatum.com -IPAddress 192.168.239.1
```

### Scopes — required vs optional

You must create a **scope** before any address is handed out. An **inactive** scope hands out nothing. The lab’s last wizard page is **Activate Scope: Yes**.

| A scope must have | A scope may have |
|---|---|
| A **range** of IP addresses (start and end) | An exclusion range |
| A **subnet mask** | A reservation (one IP pinned to one **MAC**) |
| A **lease duration** (default **8 days**) | Options: gateway, DNS, domain name, WINS |
| | A response **delay** in milliseconds (used by split scope) |

New Scope Wizard order (lab):

1. Name and description (make it meaningful, e.g. Vancouver-239).
2. Start, end, and mask (length 24 = 255.255.255.0). Example range 192.168.239.100–200, or the whole subnet with exclusions.
3. Exclusions and delay.
4. Lease duration.
5. Configure options: **Yes**.
6. Router (option 003), DNS domain and DNS servers (015 and 006), WINS (skip unless you still have it).
7. Activate.

The relay lab also builds a scope per remote subnet (Houston 172.16.30.0/24, Mexico 172.16.40.0/24, Portland 172.16.50.0/24) on the central server 192.168.239.1.

Check a client with `ipconfig /release`, `ipconfig /renew`, `ipconfig /all`. **DHCP Server** should be 192.168.239.1, and the lease should appear under the scope’s **Address Leases**.

### DHCP options and precedence

Options are the extra settings in the lease. They can be set at four levels. **The most specific one wins.**

| Level | Applies to | Precedence |
|---|---|---|
| Server options | Every scope on that server | Lowest |
| Scope options | One scope | Beats server |
| Class / policy options | Clients that match a vendor class, user class, or policy | Beats scope |
| Reservation options | One reserved client | Highest |

| Option | Code | Option | Code |
|---|---|---|---|
| Router (default gateway) | **003** | WINS/NBNS servers | 044 |
| DNS servers | **006** | WINS node type | 046 |
| DNS domain name | **015** | Lease time | 051 |
| PXE boot server / boot file | 066 / 067 | Vendor class identifier | 060 |

**WINS** (Windows Internet Name Service) maps flat **NetBIOS** names (15 characters) to IPs for old applications. NetBIOS name service is UDP 137; WINS replication is TCP 42. **DNS** maps hierarchical FQDNs and is required by AD. WINS is legacy. The scope wizard still offers it; skip it unless the question is about a network that still has NetBIOS apps.

### Reservations vs exclusions

- **Exclusion:** a range (or address) the server will **never** lease. Use it for static servers and printers.
- **Reservation:** one address leased **only** to one **MAC address**. The client is still a DHCP client (it still receives options and renews), but it always gets the same IP. Useful for printers you want to keep on DHCP.

### DHCP relay agent

DISCOVER is a broadcast. A router that is **not RFC 1542 compliant** drops it, so clients on another subnet never hear the server.

A **DHCP relay agent** sits on the clients’ subnet, hears the broadcast, and forwards it as a **unicast** to the DHCP server. The return path is unicast back through the relay. The relay fills in the gateway address (**giaddr**) so the server chooses the **scope that matches the clients’ subnet**.

Slide picture: Subnet A has the DHCP server, Subnet B has the clients and the relay, and the router between them does not forward the broadcasts.

Install path in the lab:

1. Install the **Remote Access** role, role service **Routing**.
2. Routing and Remote Access → Configure and Enable → custom → **LAN routing** → start the service.
3. IPv4 → General → New Routing Protocol → **DHCP Relay Agent**.
4. Relay agent → Properties → add the DHCP server IP (**192.168.239.1**).
5. Relay agent → **New Interface** → the NIC that faces the clients.

Deploy a relay (or a router `ip helper-address`) whenever the DHCP server is on a **different subnet** and the router will not forward DHCP broadcasts. One central server can serve Houston, Mexico, and Portland this way, with one scope per subnet.

### Policies (policy-based assignment)

A policy gives different addresses, options, or lease times based on:

- **Vendor class** (set by the hardware vendor)
- **User class** (defined by the administrator)
- **MAC address**
- **FQDN**
- **Relay agent information** (which subnet the request came from)

Lab pattern:

1. IPv4 → **Define User Classes** → Add → display name **Sales**, ASCII data `sales`. User classes are an IPv4 feature in this lab.
2. On the Office scope (192.168.239.100–200) → Policies → New Policy **sales** → condition **User Class equals Sales** → address range **.190–.200** → lease **8 hours**.
3. On the client: `ipconfig /setclassid "Ethernet0" sales`, then `/release` and `/renew`. `ipconfig /all` shows the class ID and an address from .190–.200.
4. The follow-up task is a **Finance** class with range .100–.150.

If a client that should match still gets the ordinary lease (for example 1 hour instead of the policy’s 8 hours), the request is landing on a **different scope** than the one that has the policy. That happens when a **relay** sets giaddr to another subnet. Put the policy on the scope the relay actually selects, or define it so it applies to that scope, and confirm the class ID with `ipconfig /all`.

### Superscopes and multicast scopes

**Superscope** = an administrative group of scopes (**member scopes**) so one DHCP server can lease from **more than one scope onto one physical network**.

That physical network is using more than one logical IP subnet. The handout calls this a **multinet**.

Uses:

- The current scope is almost **out of addresses**, and you add a second subnet on the same wire.
- The original scope already covers the entire classful network, so you need another range on the same segment.
- Clients are being **renumbered** from an old subnet to a new one over time.
- Clients sit behind a relay, and the far network is itself a multinet.
- Two DHCP servers on the same segment each manage a different logical network, grouped under a superscope.

Create it: right-click IPv4 → **New Superscope** → name → pick the member scopes.

**Multicast scope (MADCAP)** leases **multicast group addresses** (224.0.0.0–239.255.255.255, usually the 239.x admin range) for applications such as video or WDS multicast imaging. That is not the same as a unicast DHCP scope.

| Delivery | Meaning | DHCP example |
|---|---|---|
| **Unicast** | One sender, one receiver | Renewal at 50% (client → its own server) |
| **Broadcast** | One sender, every host on the **local** subnet; routers do not forward it | DISCOVER, and the rest of DORA on the course slides |
| **Multicast** | One sender, a **subscribed group**; can be routed | Multicast scopes, streaming, WDS |

### High availability

Three designs are on the slides. **DHCP failover** is the one Microsoft wants for Server 2012 and later.

| Design | How it works | Tradeoff |
|---|---|---|
| **DHCP cluster** | Failover Clustering, DHCP database on **shared storage**, two cluster members | Real failover, but you must build a cluster and shared storage |
| **Split scope** | Two servers each own a **non-overlapping** piece of the **same** subnet. Slide example: Server A **192.168.0.1–150**, Server B **192.168.0.151–254**, secondary **delay 500 ms** so the primary usually answers first. Common ratio **80/20** | Simple. There is **no shared lease database**. If one server dies, only its slice of the pool is left |
| **DHCP failover** | Two servers provide addresses for the **same** scopes and **replicate the lease database** | The current answer. IPv4, two servers per relationship |

**How to split a scope (slide steps):**

1. Install DHCP on the second server.
2. On the server that has the scope, open the DHCP console and select the scope.
3. Right-click → **Advanced → Split-Scope**.
4. Next past the intro.
5. Type the second server’s name or IP (or Add Server) → Next, then set the percentage and the delay.

**DHCP failover:**

- The two servers share one or more scopes.
- The **relationship name must be unique** (example `Svr1-Svr2`). Reusing a name, or adding a scope that is already in another relationship, fails. That is the slide’s “Any problem?”
- **Load sharing (load balance):** both servers are active, default **50/50**.
- **Hot standby:** one server is active; the standby keeps a small reserve (often **5%**) so it can answer during an outage before it takes the whole scope.

| Failover setting | Meaning |
|---|---|
| **MCLT (Maximum Client Lead Time)** | How long a partner may extend a lease beyond what the other partner knows about, and how long it waits before taking over the scope once the partner is considered down. Lab/video default **1 hour** |
| **Auto state switchover interval** | How long loss of contact lasts before the partner is treated as **down** (Partner Down) and this server takes over |
| **Shared secret** | A password that authenticates failover messages |
| **TCP 647** | Failover traffic. Installing DHCP creates firewall rules **Microsoft-Windows-DHCP-Failover-TCP-In** and **TCP-Out** |

Video check: stop the DHCP service on Svr1, then `ipconfig /release` and `/renew` on the client. The client still gets an address, now from Svr2, and both consoles show the same leases because the database replicated.

### Database, backup, migration

| Item | Fact |
|---|---|
| File | **`Dhcp.mdb`** (leases, scopes, reservations, options) |
| Folder | **`%systemroot%\System32\DHCP`** |
| Automatic backup | Every **60 minutes**, into the `backup` subfolder. You can also right-click the server → **Backup** / **Restore** |
| Repair | **Reconcile** the scope (or Reconcile All Scopes) when the database and the registry disagree |
| Move the service | Export from the old server, import on the new one, then **unauthorize** the old server |

```powershell
Export-DhcpServer -ComputerName OLD -File C:\dhcp.xml -Leases
Import-DhcpServer -File C:\dhcp.xml -BackupPath C:\dhcpbak -Leases
```

Netsh equivalent: `netsh dhcp server export C:\dhcp.txt all` and `netsh dhcp server import C:\dhcp.txt all`.

Audit log (text): `%windir%\System32\dhcp\DhcpSrvLog-*.log`.

### DHCP security

1. **Limit who can plug in.** Disconnect unused LAN drops. Require authenticated Layer 2 (802.1X).
2. **Audit.** Event Viewer → Applications and Services Logs → Microsoft → Windows → **DHCP-Server** (the DHCP-Operational log).
3. **Name protection.** Stops a non-Windows OS from overwriting a Windows computer’s DNS name when both want the same name. It records the original registrant with a **DHCID** resource record.
4. **Authorization** in AD, covered above.
5. **Conflict detection:** server Properties → Advanced → conflict detection attempts (1 or 2). The server pings an address before leasing it. Use this when static devices might overlap the pool.

### Troubleshooting (the slide’s discussion list)

| Problem | Likely cause | What you do |
|---|---|---|
| **Address conflicts** | A static device sits inside the pool; two servers have overlapping ranges; a rogue DHCP server; an old database was restored | Exclude static ranges or reserve them; turn on conflict detection; do not overlap scopes (use failover); find and remove the rogue; reconcile |
| **Client gets no address** (169.254.x.x) | Service stopped; server **not authorized**; scope **not activated**; pool empty; no relay across a router; wrong binding; firewall blocking UDP 67/68 | Start and authorize the service, activate the scope, fix the relay or ip-helper, check bindings, `ipconfig /renew`, read the DHCP-Server log |
| **Address from the wrong scope** | A rogue server answered first; relay giaddr points at the wrong subnet; a multinet has no superscope; a policy matched unexpectedly | `ipconfig /all` shows **which DHCP server** answered; fix the relay; build a superscope; review policies and the VLAN |
| **Database corrupt or lost** | Disk failure, bad shutdown | Restore the 60-minute backup or a manual backup; Reconcile All Scopes; if failover is on, replicate from the partner |
| **Pool exhausted** | Too many clients, leases too long, guests, stale leases | Shorten the lease (especially wireless and guest), widen the scope or add a superscope, delete stale leases, keep about 20% free |

### Week 10 short answers

**What is DHCP?**
A protocol (UDP 67/68) that leases IP configuration from a central server. Clients get an address with DORA, renew at 50% of the lease (unicast), rebind at 87.5% (broadcast), and start over at 100%.

**Scope vs superscope?**
A scope is the pool, mask, lease, and options for **one subnet**. A superscope groups several scopes so one server can serve **one physical segment that has several logical subnets** (a multinet).

**What is split-scope?**
Two DHCP servers divide one subnet’s range (for example 80/20) and do not share leases. The secondary waits (500 ms on the slide) so the primary answers first. Failover replaces this when you need a shared lease database.

**What is a relay agent?**
A service on the client subnet that turns DHCP broadcasts into unicasts aimed at a DHCP server on another subnet, and stamps the request with the client subnet so the right scope is chosen. You need it when the router is not RFC 1542 compliant and has no helper address.

**Multicast vs unicast vs broadcast?**
Unicast is one-to-one (a renewal). Broadcast is one-to-everyone on the local subnet and is not routed (DISCOVER). Multicast is one-to-a-group (224.0.0.0/4) and can be routed; a multicast scope hands out those group addresses.

---

## Part 3 — practice questions

Answer from memory, then check the sections above.

**DNS**

1. What port and protocols does DNS use, and which one carries a zone transfer?
2. Build the FQDN for a host named `computer1` in the `sales` domain of `contoso` under `.com`.
3. List the five deployment steps.
4. What three things make a response authoritative?
5. Compare primary, secondary, stub, and AD-integrated zones in one sentence each. Which one is multi-master? Which one is not authoritative?
6. Which records are in a stub zone?
7. A secondary zone says “Zone not loaded by DNS server.” What do you change, and on which server?
8. Can you add an A record on a secondary zone?
9. Name every field stored in an SOA record. What does the serial number control?
10. An MX preference of 1 vs 10: which server is tried first?
11. What four things does an SRV record tell a client, and why do site-specific SRV records reduce WAN traffic?
12. What ports do `_ldap`, `_kerberos`, `_gc`, and `_kpasswd` use?
13. On the first alnorthamerica.com screenshot, why is mail broken? What changed on the second screenshot?
14. A client asks its DNS server for `www.bcit.ca` and that server asks the root. Which query is recursive and which is iterative?
15. When do you pick a forwarder, a conditional forwarder, and a stub zone?
16. What are root hints used for?
17. Describe split DNS in three steps. What is allowed to exist on the external server?
18. What does DNSSEC prove, and what does it deliberately not provide?
19. What do socket pool and cache locking protect against? What is the cache-locking cmdlet?
20. No-refresh interval vs refresh interval vs scavenging. What is the 14-day figure? Is scavenging on by default?
21. Round robin vs netmask ordering. Which three Advanced-tab options are on by default?
22. State all nine DNS mistakes in a few words each.
23. Why must the internal domain in the Adatum worksheet differ from `adatum.com`, and where do www, ftp, and mail go?
24. A DC’s only DNS server is 127.0.0.1. What fails, and how do you fix the NIC DNS settings once a second DC exists?

**DHCP**

25. Write the four DORA messages in order and say which ones are broadcasts.
26. At 50%, 87.5%, and 100% of an 8-day lease, what does the client send, and to whom?
27. A wireless scope is set to 8 days and the pool keeps filling up with devices that left yesterday. What lease do you use instead, and why?
28. A café has 200 addresses and 400 short visits a day. Why does a 24-hour lease fail?
29. List the three post-install tasks. What does each security group do?
30. A domain-joined DHCP server’s service will not hand out addresses. It was installed while you were logged on as the local administrator. What is the error, and who must authorize it?
31. What must a scope contain? What happens if you finish the wizard and leave the scope inactive?
32. Option codes 003, 006, and 015.
33. In what order do server, scope, class, and reservation options win?
34. Exclusion vs reservation.
35. When do you install a DHCP relay agent? What field tells the server which scope to use?
36. What is a superscope, and name two situations that need one?
37. Split scope vs failover: which one replicates leases? What are the two failover modes? What are MCLT, the state switchover interval, the shared secret, and TCP 647?
38. Where is `Dhcp.mdb`, how often is it backed up, and what does Reconcile do?
39. What is DHCP name protection, and which record does it add?
40. A client shows 169.254.x.x. Give four causes.
41. Two PCs got the same address. Give three causes.
42. The pool is empty even though half the leased devices are gone. Give two fixes.
43. Does a workgroup PC need to join the domain before it can get a lease?
44. What is WINS, and how is it different from DNS?

### Answer key (compressed)

1. Port 53, UDP and TCP. Zone transfers use TCP 53.
2. `computer1.sales.contoso.com`.
3. Install DNS, configure the servers, create forward and reverse zones, add records, point clients at the servers.
4. A complete zone copy: valid SOA, valid NS records, and those NS records match the SOA.
5. Primary: writable file. Secondary: read-only transfer. Stub: SOA+NS+glue only, not authoritative. AD-integrated: stored in AD, multi-master, DCs only. Multi-master = AD-integrated. Not authoritative = stub.
6. SOA, NS, glue host (A).
7. On the **primary**: Zone Transfers → allow → only the secondary’s IP → Notify. Then transfer from master on the secondary.
8. No. Read-only.
9. Primary server, admin email, serial, refresh, retry, expire, minimum TTL. The serial is the zone version; secondaries transfer when it increases.
10. Preference 1.
11. Service, protocol, priority/weight, port, and target host. Clients pick a DC in their own site before crossing the WAN.
12. LDAP TCP 389, Kerberos 88, GC TCP 3268, kpasswd 464.
13. MX pointed at `mail.alnorthamerica.com`, an A record on the web host 72.10.34.68. Afterward, five Google MX records (1, 5, 5, 10, 10) and the mail A record removed.
14. Client → local DNS is recursive. Local DNS → root / .ca / bcit.ca is iterative.
15. Forwarder: all unknown names, one upstream. Conditional forwarder: one foreign domain, fixed IPs. Stub: a child/delegated zone whose NS list should stay current by itself.
16. Finding the root servers so iterative resolution can start when forwarders are absent or down.
17. Internal clients use AD-integrated DNS inside the firewall; that DNS answers them; the DMZ DNS answers the Internet and publishes only public records (mail, web).
18. Origin and integrity of records, and authenticated denial of existence. No confidentiality, no availability.
19. Guessable source ports, and overwrites of cached records during TTL. `Set-DnsServerCache -LockingPercent` (or `dnscmd /Config /CacheLockingPercent`).
20. No-refresh: timestamp frozen (default 7 days) to cut replication. Refresh: timestamp may update (7 days). Scavenging deletes the record after both have passed (14 days). Off by default.
21. Round robin rotates addresses. Netmask ordering prefers the client’s subnet. Both, plus secure cache against pollution, default on.
22. DC DNS points only at itself; DNS too far from users; zones not in AD; secure-only updates with non-Windows clients; no PTRs; forwarders too far away; forwarder loop; no scavenging; zone transfers open externally.
23. The lab requires the internal namespace to be separate from the external one. www, ftp, and mail stay in `adatum.com` on the perimeter.
24. The DC can become a replication island. Point it at the other DC first and itself second.
25. DISCOVER, OFFER, REQUEST, ACK. All four are broadcasts on the module slide.
26. 50% (day 4): unicast REQUEST to the original server. 87.5% (day 7): broadcast REQUEST to any server. 100% (day 8): DISCOVER, full DORA. APIPA if nobody answers.
27. About 24 hours or less, so addresses return to the pool when devices leave.
28. The first 200 guests hold every address for a full day.
29. Create DHCP Administrators and DHCP Users, restart the DHCP service, authorize in AD. Administrators manage DHCP; Users are read-only.
30. Error 20079. An Enterprise Admin (`ADATUM\Administrator`) must authorize it.
31. Range, subnet mask, lease duration. An inactive scope leases nothing.
32. 003 gateway, 006 DNS servers, 015 DNS domain name.
33. Reservation > class/policy > scope > server.
34. Exclusion: never lease it (static devices). Reservation: always lease that IP to one MAC.
35. Clients and the DHCP server are on different subnets and the router does not forward DHCP broadcasts. giaddr selects the scope.
36. A group of scopes for one physical network with multiple logical subnets. Use it when a subnet runs out of addresses, or while renumbering onto a new range.
37. Failover replicates leases; split scope does not. Load balance and hot standby. MCLT is the lead time before a partner fully takes a scope (often 1 hour). Switchover interval is how long contact can be lost before the partner is marked down. Shared secret authenticates failover messages. TCP 647.
38. `%systemroot%\System32\DHCP\Dhcp.mdb`, every 60 minutes. Reconcile repairs mismatches between the database and the registry.
39. It stops a non-Windows host from stealing a Windows host’s DNS name, using a DHCID record.
40. Service stopped, not authorized, scope inactive, pool exhausted, no relay, wrong binding, UDP 67/68 blocked. Any four.
41. Static address inside the pool, overlapping scopes, rogue DHCP server.
42. Shorten the lease; delete stale leases; enlarge the scope or add a superscope. Any two.
43. No.
44. WINS maps flat NetBIOS names for legacy apps. DNS maps hierarchical FQDNs and is what AD requires.
