# ACIT 3420 quiz study guide — Week 9 (Module 8: DNS) and Week 10 (Module 9: DHCP)

Sources: Module 8 slides (`ACIT3420 DNS`), DNS Topics, *9 Windows DNS mistakes to avoid*, Linux DNS handout, Week 9 Lab 6 (secondary zone, namespace design, DNSSEC, DNS exercise), Module 9 slides (`ACIT3420 DHCP`), DHCP Lease Time, Superscopes handout, and Week 10 Lab 7 (deploy DHCP, relay agent, failover, policies).

The Week 9 discussion board is the closest thing to a quiz outline. It asks: what DNS is and why you need it, the four zone types, every DNS record, how you protect DNS, and forwarder vs conditional forwarder vs stub zone. Week 10 is the DHCP role: DORA, leases, scopes, relay, superscopes, failover, and troubleshooting.

---

## Part 1 — Week 9, Module 8: Windows Server DNS

### Learning objectives

- Implementing DNS servers
- Configuring zones and records in DNS
- Configuring name resolution between DNS zones
- Configuring DNS integration with AD DS
- Configuring advanced DNS settings

### What DNS is, and why you need it

**Domain Name System (DNS)** is the naming service used by TCP/IP and the Internet. A client that wants `www.bcit.ca` or a corporate server does not know the IP. DNS looks it up, the same way a phone book maps a name to a number. DNS servers are also called **name servers**.

**Port 53, TCP and UDP**, on both Windows and Linux.

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

The secondary-zone lab states that DNS also lets clients locate network services, including **AD DS domain controllers**, **global catalog** servers, and messaging servers. If DNS is configured wrong or is not working, those services are inaccessible to servers and clients.

### FQDN and the hierarchy

A **hostname** plus a **domain** plus a **top-level domain** is a **fully qualified domain name (FQDN)**.

`AcctDirPC.adatum.com`

- Hostname: `AcctDirPC`
- Second-level domain: `adatum` (registered to a person or organization)
- Top-level domain: `com` (generic) or a country code. The slide lists `us`, `uk`, `de`, and `jp`. The hierarchy diagram also shows `au`

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
| DNS resolver | The client service that asks for host-to-IP mappings. The lab calls it the DNS Client service |
| Resource records | The actual database rows: A, AAAA, SRV, PTR, and the rest |

### How a name is resolved (slide: www.bcit.ca)

The diagram on the resolution slide, in order:

1. The workstation asks its local DNS server: “What is the IP address of www.bcit.ca?”
2. The local server asks a **root** DNS server.
3. The local server asks a **.ca** DNS server.
4. The local server asks the **bcit.ca** DNS server.
5. The answer returned to the workstation is **142.232.230.10**.

The forwarders slide names step 2 onward an **iterative** query: the server contacts the root, then further DNS servers, until it finds the authoritative server. The secondary-zone lab says a DNS server answers both **recursive** and **iterative** queries.

### Authoritative vs non-authoritative

- **Authoritative:** the answer comes from a server that holds a **complete copy** of that zone. A complete copy has a valid **SOA**, valid **NS** records, and those NS records match the servers listed in the SOA. A server is authoritative **only for the zones it holds**.
- **Non-authoritative:** the answer comes from **cache**. The server learned it from a server that is not authoritative for that domain.

### Five steps to deploy DNS

1. Install DNS on one or more servers (redundancy and performance; a DNS server at each site).
2. Configure the DNS servers.
3. Create **forward** and **reverse** lookup zones.
4. Add resource records to both.
5. Point clients at those DNS servers.

The install slide asks whether DNS can be deployed on Nano Server. It does not mark an answer.

Lab hardware note: most DNS servers do not need much hardware unless they answer thousands of requests a minute. The secondary-zone lab says most systems only need a 1.4GB, 64-bit processor, 512 MB of RAM, and 32 GB of free disk space, and that a DNS server should be available at each site, with more than one server for redundancy.

Install path from that lab: Server Manager → Manage → Add Roles and Features → Role-based → **DNS Server** → Add Features → Install.

### Forward vs reverse zones

| Zone | Question it answers | Typical records |
|---|---|---|
| **Forward lookup** | Name → IP | A, AAAA, CNAME, MX, SRV, NS, SOA, TXT |
| **Reverse lookup** | IP → name | **PTR**. The mistakes article calls these reverse zones `in-addr.arpa` zones |

### Zone types (memorize this table)

The New Zone Wizard offers Primary, Secondary, and Stub, plus the checkbox **Store the zone in Active Directory** (only if the DNS server is a **writable domain controller**).

| Type | Copy | Where it lives | What to remember |
|---|---|---|---|
| **Primary** | **Read/write** copy of the DNS database | Text file. The lab says that file is created in `c:\windows\system32\DNS`, and that the zone is not stored in AD | Easy to back up and recover. The primary must be available to make changes. The lab note says there is only **one** primary DNS server for the domain, and it does not replicate to another DNS server |
| **Secondary** | **Read-only** copy | Text file | Can be a copy of a primary, another secondary, **or an AD-integrated zone**. The New Zone Wizard says this balances load on the primary and provides fault tolerance. The lab uses it for remote sites and fault tolerance. **Windows can be a secondary to a Unix primary.** The lab asks you to confirm you cannot add a record on it |
| **Stub** | Only the records used to **locate name servers**: **SOA, NS, and glue host (A)** | The wizard calls it a copy of those records | The server holding the stub is **not authoritative**. It redirects the query to a server that can answer. The lab says it is read-only and saves bandwidth because it does not transfer the whole zone |
| **AD-integrated** | **Multi-master** updates | Inside AD DS, not a zone file | **Only on a domain controller** (the wizard: only if the DNS server is a writable DC). Replicated by AD at the **attribute** level. Secure dynamic updates. Delegated administration and ACLs. High availability. **Harder to restore after a disaster** than a zone file. The mistakes article says this replication can be to all DNS servers in the **domain** or the **forest** |

**Benefits of an AD-integrated zone (slide list):**

- Multi-master updates (any DC with the zone can accept a change)
- Zone data replicates with AD DS
- Secure dynamic updates
- Detailed security: delegate zones and set ACLs

The DNS Manager screenshot shows folders named **DomainDnsZones** and **ForestDnsZones**. The mistakes article is the source that says an AD-integrated zone can replicate to all DNS servers in the domain or in the forest.

### Resource records — explain each one

**Forward lookup**

| Record | What it maps | Details that show up on a quiz |
|---|---|---|
| **A** | Hostname → **IPv4** | `CA-VAN-Svr3` → `192.168.239.4` |
| **AAAA** | Hostname → **IPv6** | Same idea as A, for IPv6 |
| **CNAME** | Alias → another record | The slide calls it an alternative name or alias for another record |
| **MX** | Domain → mail server | The record-issues screenshots put a number in front of the mail host, for example `10 mail.alnorthamerica.com.` |
| **SRV** | Service → host | Slide fields: **service, target port, priority**, plus a host **(A)** record. Usually created automatically by the application. The console shows the data as `[priority][weight][port] hostname` |
| **NS** | Domain → authoritative name servers | Who is allowed to answer for the zone |
| **SOA** | **One per zone** | Primary name server, administrator email, **serial number**, and refresh time |
| **TXT / SPF** | Text | The slide groups **TXT or SPF** with **MX** under **email spoofing**. The record-issues screenshot also has a `google-site-verification=...` TXT record |

**Reverse lookup**

| Record | What it maps |
|---|---|
| **PTR** | IP address → name |

**Glue host (A) record:** named on the zone-type slide and in the lab’s stub-zone note, together with SOA and NS. The stub zone holds these so it can locate the name servers. The lab says that is why a stub zone does not have to transfer the whole zone.

**PowerShell from the slide:**

```powershell
Add-DnsServerResourceRecordA -ZoneName Adatum.com -Name CA-VAN-Svr3 -IpAddress 192.168.239.4
```

The slide’s SOA contents are: one per zone, primary name server, administrator email, serial number, and refresh time.

**SRV records on the DNS Manager screenshot (`_msdcs.Adatum.com`)**

| Name | Folder on the screenshot | Data shown |
|---|---|---|
| `_gc` | tcp | `[0][100][3268]` |
| `_kerberos` | tcp and udp | `[0][100][88]` |
| `_kpasswd` | tcp and udp | `[0][100][464]` |
| `_ldap` | tcp | `[0][100][389]` |

The host on those rows is `CA-VAN-Svr1.Adatum.com` or `CA-VAN-Svr2.Adatum.com`. One `_gc` row is `[0][100][3268] CA-BBY-Svr2.BBY.Adatum.com`.

**Why SRV records matter (slide benefits):**

- Domain controllers register SRV records **dynamically, by service and by site**.
- A client uses the SRV records for **its own site** first, and only then tries a DC across a WAN link.
- That keeps inter-site traffic down.

### The alnorthamerica.com record problem (slides “DNS Record Issues”)

**Before:** the zone’s only MX is `10 mail.alnorthamerica.com.`, and `mail` is an **A** record at **72.10.34.68**, the same address as the apex, the wildcard, `ftp`, and `www`.

**After:** the `mail` A record is gone. Mail is five Google MX records, and a TXT verification record is present:

| Preference | Mail exchanger |
|---|---|
| **1** | `ASPMX.L.GOOGLE.COM.` |
| **5** | `ALT1.ASPMX.L.GOOGLE.COM.` |
| **5** | `ALT2.ASPMX.L.GOOGLE.COM.` |
| **10** | `ALT3.ASPMX.L.GOOGLE.COM.` |
| **10** | `ALT4.ASPMX.L.GOOGLE.COM.` |

TTL on those rows is **43200**.

The slide asks which tools can identify the problem. It does not list the tools.

### Forwarder vs conditional forwarder vs stub zone

This is a listed discussion question. Learn the difference cold.

By default, if the DNS server does not know the answer it walks the tree itself (root → TLD → authoritative). A **forwarder** changes that.

| Mechanism | When it is used | How it behaves |
|---|---|---|
| **Forwarder** | External or offsite names this server does not answer itself | The forwarding slide: a forwarder is a DNS server designated to resolve external or offsite names. You control where queries and traffic go |
| **Conditional forwarder** | **One domain name**, which can be in a **different top-level domain** | The guidance slide: use it when you want all resolution for that name to take one path |
| **Stub zone** | A name **below** a higher-level domain, described as a **delegation below a delegation** | SOA, NS, and glue host (A) only. Not authoritative. The lab says this saves bandwidth |

**Why forwarders exist (slide question):** you control where queries go and how much traffic leaves the network, which makes resolution faster and more predictable for internal computers.

**Root hints:** the list a DNS server uses to find the root servers when it performs an iterative query. A root server answers records in the root zone, and for other requests it returns the authoritative servers for the right TLD. The slide says root hints matter for servers that are authoritative only for a lower part of the namespace and still have to find the authoritative server for another zone.

**Zone delegation:** a subdomain is a child of a parent and shares that parent’s suffix. It can be its own zone on another server. The slide says that spreads the query load across servers.

**Slide guidance, worded as a rule:**

- Conditional forwarder: the name is a **different domain** (it can even be a different top-level domain), and you want **all** resolution for it to take one path.
- Stub zone: the name sits **below** a higher-level domain (a delegation below a delegation).

### Split DNS

Organizations keep **internal DNS** and **external DNS** separate.

1. Internal clients and servers send **all** queries to the **AD-integrated DNS servers** on the domain controllers, inside the firewall.
2. Those servers answer with internal addresses (and they must still be able to resolve the company’s own public names, such as mail and web).
3. An **external DNS server in the perimeter network** answers Internet clients. It hosts **only** records that are resolved from the outside, such as the mail and web servers.

The internal zone stays unreachable from outside the firewall so internal host names and IPs are not published. External records still have to resolve for internal users.

### Secondary zone lab (what the quiz can pull from the steps)

Topology in the lab: primary is the domain controller (**CA-VAN-SVR1**, 192.168.239.1, zone `adatum.com`). Secondary is **CA-VAN-SVR4**.

1. Install the DNS role on Svr4.
2. DNS Manager → Forward Lookup Zones → **New Zone** → **Secondary** → zone name `adatum.com` → master IP **192.168.239.1**.
3. The zone shows **“Zone not loaded by DNS server.”** The lab asks you to explain that error, then continues with the primary.
4. On the **primary**: zone → Properties → **Zone Transfers** → **Allow zone transfers** → **Only to the following servers** → add Svr4’s IP → **Notify** those same servers.
5. Back on Svr4, refresh DNS Manager and check whether the secondary zone is there.
6. The lab asks whether you can add a record on the secondary, and why or why not. The zone-type notes call the secondary a read-only copy.

### Advanced server settings (Advanced tab)

Defaults that are **already on**:

- **Round robin** — if several A records exist for one name, the server **rotates** which address it returns first. That spreads load.
- **Netmask ordering** — if several addresses exist, prefer the one on the **client’s subnet**.
- **Secure cache against pollution** — ignore extra records in a referral that are not for the name that was queried (anti cache-poisoning).

You can also enable or disable **recursion** on this tab. The slide lists that with the other Advanced options. The Linux handout, not this slide, is where recursion on an authoritative server is discussed.

### Debug logging

DNS **debug logging** is a troubleshooting tool for detailed, file-based analysis of DNS packets and messages. The slide says it has a processing and storage overhead.

### TTL, aging, scavenging

| Term | Meaning |
|---|---|
| **TTL** | How long a resolver may **cache** a record. Shorten it before you change an address so old data dies quickly |
| **Aging** | Applies to **dynamic** records (you can turn it on for static ones too). Each dynamic record has a **timestamp** |
| **No-refresh interval** | The **timestamp cannot be updated**. Other changes are still allowed (an IP address change, or a service change such as a port). This reduces replication traffic and keeps records from being removed too quickly |
| **Refresh interval** | **Any** data can change, including the timestamp |
| **Scavenging** | Removes outdated records after the no-refresh interval plus the refresh interval. The slide’s default total is **14 days**. **Not configured by default.** It requires several settings, and it can appear to happen at random |

### How you protect DNS

The security goal: stop false records from being added, and stop clients from being sent to the wrong address (phishing).

| Control | What it stops | How |
|---|---|---|
| **DNSSEC** | Forged or altered records | Proves **identity** of the records and gives a **verified denial** (“this name really does not exist”). It does **not** provide confidentiality or availability |
| **Socket pool** | An attacker guessing the source port of a query (cache poisoning) | Random source ports. `dnscmd /Config /SocketPoolSize` with a value from **0 to 10,000** |
| **Cache locking** | Overwriting a cached record while its TTL is still valid | `dnscmd /Config /CacheLockingPercent` or `Set-DnsServerCache -LockingPercent`. **100** means the record cannot be overwritten for the whole TTL |
| **Secure cache against pollution** | Bogus extra records stuck into a referral | Advanced tab, on by default |
| **Secure dynamic updates** | Named on the AD-integrated benefits slide | AD-integrated zones |
| **Restrict zone transfers** | The mistakes article: an outsider can download the whole zone | Allow transfers internally to the servers you name. Do not allow them to arbitrary external hosts. The lab uses “Only to the following servers” |
| **Least privilege** | The delegated-administration slide | Restrict DNS administration to the people who need it |
| **Split DNS** | Publishing internal names outside | Separate internal and external zones |

**DNSSEC lab (optional, still fair game):**

1. DNS Manager → zone `adatum.com` → **DNSSEC → Sign the Zone** → **Customize zone signing parameters**.
2. **Key Master** is the DNS server (the DC) that generates and manages the keys.
3. Add the **Key Signing Key** and the **Zone Signing Key**, accepting the default values.
4. Choose **nsce3** with the default values. That is the spelling in the lab.
5. Enable distribution of trust anchors. Check that **DNSKEY** records were created in the **Trust Points** zone.
6. You can **unsign** the zone later.
7. In GPMC, create a GPO, then Computer Configuration → Policies → Windows Settings → **Name Resolution Policy** (NRPT). The lab’s own examples:
   - **Suffix** `microsoft.com` covers that name and its child domains.
   - **Prefix** `www` covers a query for any server named www in any domain.
   - **FQDN** is one complete name.
   - **Subnet (IPv4 or IPv6)** applies to reverse lookups.
   - **Any** is the default rule for anything another rule does not cover.
8. On the DNSSEC tab: **Enable DNSSEC in this rule**, and require clients to check that name and address data has been validated. The lab notes that IPsec can be required between the client and the DNS server for that namespace.
9. On the client: `gpupdate /force`, then `gpresult /r`, and confirm the DNSSEC GPO applied.

### Delegated administration

The slide says DNS administration should be restricted to the people who need it, and that least privilege applies. The AD-integrated benefits slide adds delegated administration of zones and ACLs.

### Namespace design exercise (Adatum)

Rules from the lab:

- Root name is **adatum.com**. Every other domain is **under** it.
- Internal network uses a **different domain** from the external network.
- Three internal divisions, each its **own subdomain**: Sales, Human Resources, Production.
- Host names describe the **function** (file, db, www, mail, wk for workstation).
- Three perimeter servers (Web, FTP, email) stay in **adatum.com**, the external name.

The worksheet figure already fills in these names:

| Place | Domain | Example FQDNs |
|---|---|---|
| External / perimeter | `adatum.com` | `www.adatum.com`, `ftp.adatum.com`, `mail.adatum.com` |
| Internal root | `int.adatum.com` | (the internal parent; not published outside) |
| Human Resources | `hr.int.adatum.com` | `file1.hr.int.adatum.com`, `www.hr.int.adatum.com` |
| Sales | `sl.int.adatum.com` | `file1.sl.int.adatum.com`, `db.sl.int.adatum.com` |
| Production | `pr.int.adatum.com` | `file1.pr.int.adatum.com`, `wk2.pr.int.adatum.com` |

External hosts on that figure stay in `adatum.com`: `www`, `ftp`, and `mail`. Each division is a child of `int.adatum.com`.

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
- `systemctl restart named`, then `netstat` shows TCP 53 on 192.168.239.10 and 127.0.0.1. The same output also shows TCP 953 on 127.0.0.1
- A Windows DNS server can be a **secondary** of this BIND primary if the zone allows transfers to the Windows server’s IP

The secondary-zone lab names **nslookup** as the tool for managing and troubleshooting DNS. It does not give a command list. The DNSSEC lab uses `gpupdate /force` and `gpresult /r`.

### Week 9 discussion — short answers

**What is DNS? Why do we need it? What does it do?**
DNS is the TCP/IP naming service (port 53 TCP and UDP) that maps a name to an IP, the way a phone book maps a name to a number. The lab adds that clients use it to find domain controllers, global catalog servers, and messaging servers. If it is wrong, those services are inaccessible.

**Primary vs secondary vs stub vs AD-integrated?**
Primary is the writable copy in a zone file. Secondary is a read-only transferred copy for load and fault tolerance. Stub holds only SOA, NS, and glue A records and is not authoritative. AD-integrated stores the zone in AD on domain controllers, is multi-master, replicates with AD, and supports secure dynamic updates.

**Explain each record.**
Use the record table above: A and AAAA, PTR, CNAME, MX, SRV, NS, SOA, and TXT/SPF.

**How do you protect DNS?**
DNSSEC (identity of the records and verified denial of existence; not availability or confidentiality), socket pool, cache locking, secure cache against pollution, secure dynamic updates, zone transfers limited to named servers, least privilege, and split DNS.

**Forwarder vs conditional forwarder vs stub?**
A forwarder resolves external or offsite names and lets you control query traffic. A conditional forwarder is for one domain, even a different top-level domain, when all resolution for that name should take one path. A stub zone is for a name below a higher-level domain. It holds SOA, NS, and glue A records, is not authoritative, and does not transfer the whole zone.

---

## Part 2 — Week 10, Module 9: DHCP

### Module map

- Overview of the DHCP server role
- Deploying DHCP (install, authorize, scopes, options, relay)
- Managing and troubleshooting (security, policies, superscopes, multicast, high availability, failover, database, migration)

### What DHCP does

**Dynamic Host Configuration Protocol** hands out IP configuration automatically: address, subnet mask, default gateway, DNS servers, DNS domain name, and other options.

The benefits slide says the Microsoft DHCP service also supports **IPv6**.

| Automatic (DHCP) | Manual (static) |
|---|---|
| Supplies addresses automatically | You type every address |
| Pushes a consistent set of options | A typo is easy |
| Change an option once and clients pick it up | A wrong gateway or DNS server breaks communication |
| Computers can move without a renumbering project | Every move is admin work |

The allocation slide shows a **non-DHCP client** with a static configuration next to the DHCP clients. The lease article says routers, switches, and printers typically use a static address, and that a printer left on DHCP can change address after a long shutdown.

The deploy lab asks whether the client must join the domain before it can use Windows DHCP. The lab does not answer that question.

### Lease generation — DORA

The generation slide says all four messages are **broadcasts**.

| Step | Message | What the slide says |
|---|---|---|
| 1 | **DHCPDISCOVER** | The client broadcasts it |
| 2 | **DHCPOFFER** | The DHCP servers broadcast it |
| 3 | **DHCPREQUEST** | The client broadcasts it |
| 4 | **DHCPACK** | The chosen server broadcasts it |

Memory hook: **D**iscover, **O**ffer, **R**equest, **A**cknowledge. The DHCP lab uses `ipconfig /release` and `ipconfig /renew` to test a client. The scope wizard can set a delay between receiving DISCOVER and sending OFFER.

### Lease renewal — 50%, 87.5%, 100%

The lease article calls the halfway timer **T1** and the later timer **T2**. For an 8-day lease, halfway is day 4.

| Point | What the materials say |
|---|---|
| **50%** (T1) | The renewal slide: the client sends **DHCPREQUEST**, and the server sends **DHCPACK**. The article says the client tries to keep the same address. If that renewal succeeds, T1 and T2 reset and the lease starts over |
| **87.5%** (T2) | The 50% renewal failed. The article calls this rebinding: the client tries to extend the lease with **any** active DHCP server. The slide says the renewal process begins again at 87.5% |
| **100%** | The slide says lease generation starts over with a broadcast **DHCPDISCOVER** |
| Boot while a lease is still valid | The article says the client confirms that existing lease and resumes it, instead of starting a brand-new lease |

The slide’s wording: if renewal fails after 50%, the renewal process runs again after 87.5%. If that also fails, generation starts over with DISCOVER.

Worked example from the lease article: lease = 8 days. At day 4 the client tries to renew. If it succeeds on day 5, the 8-day clock starts over. A 1-hour guest lease tries to renew at 30 minutes; if it succeeds at 35 minutes, that address stays reserved until the new hour ends (about 95 minutes total in the article’s coffee-shop math).

### How long should the lease be?

| Network | Lease | Why |
|---|---|---|
| Wired / enterprise | **8 days** | The article calls this typical for wired devices. The scope wizard’s default lease is also 8 days. A shorter lease only adds DHCP traffic |
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
- `Add-WindowsFeature DHCP`

**Post-install tasks on the slide, in this order:**

1. Create the DHCP security groups. The lab asks what the **DHCP Administrators** group and the **DHCP Users** group are. It does not define them.
2. Restart the DHCP Server service.
3. Authorize the DHCP server in AD DS.

The lab says to do that authorization while logged on as the domain administrator, `Adatum\Administrator`.

### Authorization

A domain-joined Windows DHCP server asks a domain controller for the list of authorized servers when the service starts.

- If **its own IP is on the list**, the service starts and answers clients.
- If **its IP is not on the list**, the service does **not** start serving clients.

The lab says this blocks a rogue **domain-joined Windows** DHCP server. It does **not** stop rogue access points, non-domain-joined devices, or other devices from handing out addresses. Those have to be limited with **port security**. The security slide also says to disconnect unused LAN drops and to require authenticated Layer 2 connections.

If you are not logged on as `Adatum\Administrator`, “use the following user’s credentials” is greyed out and authorization returns **error 20079**. Sign in as the domain administrator and authorize manually. **Unauthorize** a server in Manage Authorized Servers before you retire it. The lab says **netsh** can list the DHCP servers. It does not print the command.

### Scopes — required vs optional

You must create a **scope** before any address is handed out. An **inactive** scope hands out nothing. The lab’s last wizard page is **Activate Scope: Yes**.

| A scope must have | A scope may have |
|---|---|
| A **range** of IP addresses (start and end) | An exclusion range |
| A **subnet mask** | A reservation (one IP pinned to one **MAC**) |
| A **lease duration** (the wizard default is **8 days**) | A delay between DISCOVER and OFFER |
| | | Options: router, DNS servers, DNS domain name. The wizard also has a WINS page |

New Scope Wizard order (lab):

1. Name and description. The lab says to use a meaningful name and a description.
2. Start address, end address, and subnet mask. The lab also says you can use the whole range (1–254) and then exclude addresses for member servers. The policy lab’s office range is 192.168.239.100–200 with mask 255.255.255.0.
3. Exclusions and delay.
4. Lease duration.
5. Configure options: **Yes**.
6. Router (default gateway), then domain name and DNS servers. The WINS Servers page is next. The lab asks what WINS is and how it differs from DNS. It does not answer that.
7. Activate.

The relay lab also builds a scope per remote subnet (Houston 172.16.30.0/24, Mexico 172.16.40.0/24, Portland 172.16.50.0/24) on the central server 192.168.239.1.

Check a client with `ipconfig /release`, `ipconfig /renew`, `ipconfig /all`. **DHCP Server** should be 192.168.239.1, and the lease should appear under the scope’s **Address Leases**.

### DHCP options and precedence

The options slide says DHCP options are common configuration values, and they can be set at the **server**, **scope**, **class**, and **reservation** levels. The common scope options it names are the **router (default gateway)**, the **DNS domain name**, and the **DNS servers**. The slide does not give option numbers or a precedence order.

### Reservations vs exclusions

- **Exclusion:** the scope wizard has an exclusions page. The deploy lab says to exclude addresses for member servers. The lease article says to leave addresses outside the pool for static devices such as routers, switches, and printers.
- **Reservation:** the allocation slide says an address can be reserved based on the client’s MAC address.

### DHCP relay agent

DISCOVER is a broadcast. A router that is **not RFC 1542 compliant** drops it, so clients on another subnet never hear the server.

A **DHCP relay agent** sits on the clients’ subnet, hears the broadcast, and relays it to a DHCP server on another subnet. The relay slide marks the forwarded path as **unicast**.

Slide picture: Subnet A has the DHCP server, Subnet B has the clients and the relay, and the router between them does not forward the broadcasts.

Install path in the lab:

1. Install the **Remote Access** role, role service **Routing**.
2. Routing and Remote Access → Configure and Enable → custom → **LAN routing** → start the service.
3. IPv4 → General → New Routing Protocol → **DHCP Relay Agent**.
4. Relay agent → Properties → add the DHCP server IP (**192.168.239.1**).
5. Relay agent → **New Interface** → the NIC that faces the clients.

The deploy lab’s challenge is to discuss when you have to deploy a relay. The topology for that lab has remote subnets (Houston 172.16.30.0/24, Mexico 172.16.40.0/24, Portland 172.16.50.0/24) and the DHCP server at 192.168.239.1. The slide’s case is a router that is not RFC 1542 compliant, so it does not forward the DHCP broadcast.

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
3. On the client the lab uses `ipconfig /setclassid "Ethernet" sales`, then `/release` and `/renew`.
4. The follow-up task is a **Finance** class whose policy range is 192.168.239.100–192.168.239.150.

The lab’s challenge: the address range can be right while the lease time is still 1 hour instead of the policy’s 8 hours. The only hint in the lab is **DHCP relay agent**. It does not explain further. The lab also says you can define vendor classes for IPv4 and IPv6, but you cannot define a user class for IPv6.

### Superscopes and multicast scopes

**Superscope** = an administrative group of scopes (**member scopes**) so one DHCP server can lease from **more than one scope onto one physical network**.

That physical network is using more than one logical IP subnet. The handout calls this a **multinet**.

Uses:

- The current scope is almost **out of addresses**, and you add a second subnet on the same wire.
- The original scope already covers the entire classful network, so you need another range on the same segment.
- Clients are being **renumbered** from an old subnet to a new one over time.
- Clients sit behind a relay, and the far network is itself a multinet.
- Two DHCP servers on the same segment each manage a different logical network, grouped under a superscope.

The module slide is titled configuring superscopes and multicast scopes. The superscope handout is the text that defines a superscope. That handout does not define a multicast scope.

### High availability

Three designs are on the slides. **DHCP failover** is the one Microsoft wants for Server 2012 and later.

| Design | How it works | Tradeoff |
|---|---|---|
| **DHCP cluster** | Failover Clustering, DHCP database on **shared storage**, two cluster members | Real failover, but you must build a cluster and shared storage |
| **Split scope** | Two servers each own a **non-overlapping** piece of the **same** subnet. The slide’s example is Server A **192.168.0.1–150** and Server B **192.168.0.151–254**, with the delay set to **500 ms** | The two ranges do not overlap. The slide does not say the servers share a lease database |
| **DHCP failover** | Two DHCP servers provide addresses and options to the **same** subnets or scopes | The slide names two modes: hot standby and load sharing. Each relationship needs a unique name |

**How to split a scope (slide steps):**

1. Install DHCP on the second server.
2. On the server that has the scope, open the DHCP console and select the scope.
3. Right-click → **Advanced → Split-Scope**.
4. Next past the intro.
5. Type the second server’s name or IP (or Add Server) → Next, then set the percentage and the delay.

**DHCP failover:**

- The **relationship name must be unique**. The slide’s example is `Svr1-Svr2`, followed by “Any problem?”
- The two modes on the slide are **hot standby** and **load sharing**. The slide does not give a split percentage for either mode.

| Failover setting | What the slide says |
|---|---|
| **MCLT (Maximum Client Lead Time)** | Determines when a failover partner assumes control of the subnet or scope |
| **Auto state switchover interval** | Determines when a failover partner is considered to be down |
| **Shared secret** | A password that can validate the failover messages |
| **TCP 647** | Installing DHCP auto-configures the firewall rules **Microsoft-Windows-DHCP-Failover-TCP-In** and **TCP-Out** |

### Database, backup, migration

| Item | Fact |
|---|---|
| File | **`Dhcp.mdb`** (leases, scopes, reservations, options) |
| Folder | **`%systemroot%\System32\DHCP`** |
| Automatic backup | Every **60 minutes**, or you can back it up manually |
| Repair | **Reconcile** the database to repair inconsistencies |
| Move the service | Export the data from the old server to a file and import that file on the new server. The slide says you can use PowerShell or NetShell. It does not show the commands |

### DHCP security

1. **Limit physical access.** Disconnect unused LAN drops. Require authenticated Layer 2 connections.
2. **Audit.** Enable DHCP auditing in the DHCP-Operational log: Event Viewer → Applications and Services Logs → Microsoft → Windows → **DHCP-Server**.
3. **Name protection.** Stops a non-Windows OS from overwriting a Windows computer’s DNS name when both want the same name. It uses a **DHCID** resource record for the device that originally requested the name.
4. **Authorization** in AD, covered above. The lab adds port security for devices that authorization does not stop.

### Troubleshooting (the slide’s discussion list)

The slide asks how you address these when DHCP is not configured properly. It does not print the answers. Related facts that are in the module:

- **Failure to obtain an address.** An unauthorized domain-joined server does not service clients. A scope that was not activated does not provide service. A relay is required when the router does not forward the broadcast.
- **Database corruption or loss.** The database is backed up every 60 minutes, or manually, and reconcile repairs inconsistencies. You can also export it and import it on another server.
- **Pool exhausted.** The lease article says to shorten the lease or enlarge the pool, and to keep about 20% free. The superscope handout covers a scope whose pool is nearly depleted.
- **Address conflicts** and **an address from the wrong scope** are on the discussion list. The materials do not give a cause list for either one.

### Week 10 short answers

**What is DHCP?**
It hands out IP configuration automatically. Clients get an address with DORA (all four messages are broadcasts on the slide). Renewal is attempted at 50% of the lease. If that fails, it is attempted again at 87.5%. At 100% the client starts over with DISCOVER.

**Scope vs superscope?**
A scope is the pool, mask, lease, and options for **one subnet**. A superscope groups several scopes so one server can serve **one physical segment that has several logical subnets** (a multinet).

**What is split-scope?**
The slide splits one subnet across two servers, for example 192.168.0.1–150 and 192.168.0.151–254, and sets a 500 ms delay. Failover is the other design on that slide: two servers serve the same scopes, in hot standby or load sharing.

**What is a relay agent?**
It listens for DHCP broadcasts and relays them to a DHCP server on another subnet. The slide shows that forwarded path as unicast. You need it when the router is not RFC 1542 compliant.

---

## Part 3 — practice questions

Answer from memory, then check the sections above.

**DNS**

1. What port and protocols does DNS use?
2. Build the FQDN for a host named `computer1` in the `sales` domain of `contoso` under `.com`.
3. List the five deployment steps.
4. What three things make a response authoritative?
5. Compare primary, secondary, stub, and AD-integrated zones in one sentence each. Which one is multi-master? Which one is not authoritative?
6. Which records are in a stub zone?
7. A secondary zone says “Zone not loaded by DNS server.” What do you change, and on which server?
8. Can you add an A record on a secondary zone?
9. What does the slide say an SOA record contains?
10. On the first alnorthamerica.com screenshot, where does the MX point? What replaced it on the second screenshot?
11. What does the slide say an SRV record contains, and why do site-specific SRV records reduce WAN traffic?
12. What ports do `_ldap`, `_kerberos`, `_gc`, and `_kpasswd` use?
13. Which tools does the record-issues slide say you should use?
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
26. At 50%, 87.5%, and 100% of the lease, what does the client do?
27. A wireless scope is set to 8 days and the pool keeps filling up with devices that left yesterday. What lease do you use instead, and why?
28. A café has 200 addresses and 400 short visits a day. Why does a 24-hour lease fail?
29. List the three post-install tasks. What does the lab ask about the two DHCP security groups?
30. Authorization fails with a greyed-out credentials option. What is the error, and which account does the lab say to use?
31. What must a scope contain? What happens if you leave the scope inactive?
32. Which scope options does the options slide name?
33. At which four levels can DHCP options be set?
34. Exclusion vs reservation.
35. When does the relay slide say you need a DHCP relay agent?
36. What is a superscope, and name two situations that need one?
37. What address split and delay does the split-scope slide show? What are the two failover modes, and what do MCLT, the state switchover interval, the shared secret, and TCP 647 mean on the slide?
38. Where is `Dhcp.mdb`, how often is it backed up, and what does Reconcile do?
39. What is DHCP name protection, and which record does it add?
40. Name two module facts that explain a client getting no address.
41. The discussion asks how you address address conflicts. Does the module give the causes?
42. The pool is exhausted. Give two fixes that are in the lease article or the superscope handout.
43. Does the deploy lab say whether a client must join the domain to get a lease?
44. Does the scope lab define WINS?

### Answer key (compressed)

1. Port 53, TCP and UDP, on Windows and Linux.
2. `computer1.sales.contoso.com`.
3. Install DNS, configure the servers, create forward and reverse zones, add records, point clients at the servers.
4. A complete zone copy: valid SOA, valid NS records, and those NS records match the SOA.
5. Primary: writable file. Secondary: read-only copy. Stub: SOA, NS, and glue A only, and not authoritative. AD-integrated: stored in AD, multi-master, domain controllers only. Multi-master is AD-integrated. Not authoritative is the stub.
6. SOA, NS, glue host (A).
7. On the **primary**: Zone Transfers → allow → only the secondary’s IP → Notify. Then refresh the secondary.
8. The lab asks you to check. The zone notes call a secondary read-only.
9. One per zone, primary name server, administrator email, serial number, and refresh time.
10. Before: MX `10 mail.alnorthamerica.com.` and `mail` is an A record at 72.10.34.68, the same address as www. After: that mail A record is gone, and the MX rows are the five Google hosts with preferences 1, 5, 5, 10, and 10.
11. Service, target port, priority, and a host A record. Clients use the SRV records for their own site before crossing a WAN link.
12. On the screenshot: `_ldap` tcp 389, `_kerberos` tcp and udp 88, `_gc` tcp 3268, `_kpasswd` tcp and udp 464.
13. The slide asks the question and does not name the tools.
14. The forwarders slide calls the walk from the local server to the root, then .ca, then bcit.ca an iterative query. The lab says the DNS server answers both recursive and iterative queries. The diagram’s first step is the workstation asking the local server.
15. Forwarder: external or offsite names. Conditional forwarder: one domain, even a different top-level domain, all resolution taking one path. Stub: a name below a higher-level domain; SOA, NS, and glue A only.
16. Finding the root servers so a server can perform an iterative query.
17. Internal clients use AD-integrated DNS inside the firewall; that DNS answers them; the external DNS answers Internet clients and hosts only records resolved from outside, such as mail and web.
18. Proof of identity of the records, and verified denial of existence. Not availability or confidentiality.
19. Guessing the source port of a query, and replacing a cached record while its TTL is still in force. `Set-DnsServerCache -LockingPercent`. The slide’s dnscmd line is `dnscmd /Conifg /CatcheLockingPercent 100`.
20. No-refresh: the timestamp cannot be updated. Refresh: any data, including the timestamp, can change. Scavenging runs after both intervals. The slide’s combined default is 14 days. Scavenging is not configured by default.
21. Round robin rotates which address is returned first. Netmask ordering prefers the address on the client’s subnet. Both, plus secure cache against pollution, are on by default.
22. DC DNS points only at itself; DNS too far from users; zones not in AD; secure-only updates with non-Windows clients; no PTRs; forwarders too far away; forwarder loop; no scavenging; zone transfers open externally.
23. The worksheet requires the internal domain to differ from the external one. On the figure, www, ftp, and mail stay in `adatum.com`.
24. The DC can become an island and replication can fail. Point each DC at another DC, not only at itself.
25. DISCOVER, OFFER, REQUEST, ACK. The generation slide says all four are broadcasts.
26. 50%: DHCPREQUEST, then DHCPACK; the article says this is the attempt to keep the same address. 87.5%: the renewal process runs again, and the article says the client tries any active DHCP server. 100%: DHCPDISCOVER.
27. About 24 hours, because wireless devices leave and a long lease holds their addresses.
28. The first 200 guests hold every address for a full day.
29. Create the DHCP security groups, restart the DHCP service, authorize in AD. The lab asks what DHCP Administrators and DHCP Users are, and it does not define them.
30. Error 20079. Log on as `Adatum\Administrator`.
31. A range of addresses, a subnet mask, and a lease duration. The lab says you have to activate the scope or DHCP will not provide service.
32. Router (default gateway), DNS domain name, and DNS servers.
33. Server, scope, class, and reservation. The slide does not rank them.
34. An exclusion is a range the scope wizard keeps out of the pool. A reservation pins an address to a MAC address. The allocation slide says addresses can be reserved by MAC.
35. When the router is not RFC 1542 compliant and does not forward DHCP broadcasts to the server on another subnet.
36. A group of member scopes so one server can lease from more than one scope onto one physical network (a multinet). Two cases from the handout: the current pool is nearly depleted, or clients are being renumbered onto a new scope.
37. The slide’s split is 192.168.0.1–150 and 192.168.0.151–254, with a 500 ms delay. Failover modes are hot standby and load sharing. MCLT is when the partner assumes control of the scope. The switchover interval is when the partner is considered down. The shared secret validates failover messages. TCP 647 is the failover firewall rule created when DHCP is installed.
38. `%systemroot%\System32\DHCP\Dhcp.mdb`. Backed up every 60 minutes, or manually. Reconcile repairs inconsistencies in the database.
39. It stops a non-Windows host from overwriting a Windows host’s DNS name. It uses a DHCID record.
40. An unauthorized server does not service clients. A scope that is not activated does not provide service. A relay is required when the router does not forward the broadcast. Any two.
41. No. The discussion lists address conflicts and does not give the causes.
42. Shorten the lease, or enlarge the pool (the superscope handout is the case where the current pool is nearly depleted). Also keep about 20% of the pool free.
43. The lab asks. It does not answer.
44. No. The scope wizard has a WINS page, and the lab asks what WINS is and how it differs from DNS, without defining it.
