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

### How to read the SRV screenshot

Open DNS Manager on **CA-VAN-SVR1**. Under Forward Lookup Zones, open **`_msdcs.Adatum.com`**. The rows in that zone are SRV records. An SRV record answers one question: which computer offers this service, and on which port?

The slide says an SRV record holds the service, the target port, the priority, and a normal host (A) record. Domain controllers create these rows themselves.

One line on the screenshot looks like this:

`[0][100][3268] CA-VAN-Svr2.Adatum.com`

Read it from the right. The name at the end is the server. The last number inside the brackets is the port. The folder the row sits in is either **tcp** or **udp**.

Four names are on that screenshot:

- **`_gc`**, folder tcp, port **3268**. Most of these point at CA-VAN-Svr1 or CA-VAN-Svr2. One points at `CA-BBY-Svr2.BBY.Adatum.com`, a server in the BBY site. The lab says clients use DNS to find a global catalog. This is that row.
- **`_kerberos`**, folders tcp and udp, port **88**. Hosts are the two VAN servers.
- **`_kpasswd`**, folders tcp and udp, port **464**. Same two VAN servers.
- **`_ldap`**, folder tcp, port **389**. Same two VAN servers.

The benefits slide gives the reason these rows exist:

- A domain controller registers them itself, by service and by site.
- A computer looks for a domain controller in its own site first.
- Only if that fails does it try a domain controller across the WAN. That keeps traffic off the WAN link.

### The mail-record screenshots (alnorthamerica.com)

Two slides show the same zone before and after a fix.

**Before.** The only MX record is `10 mail.alnorthamerica.com.` The name `mail` is an A record at **72.10.34.68**. That same address is also used by the zone name itself, the `*` wildcard, `ftp`, and `www`.

**After.** The `mail` A record is gone. In its place are five MX records, all with TTL **43200**:

- preference 1: `ASPMX.L.GOOGLE.COM.`
- preference 5: `ALT1.ASPMX.L.GOOGLE.COM.` and `ALT2.ASPMX.L.GOOGLE.COM.`
- preference 10: `ALT3.ASPMX.L.GOOGLE.COM.` and `ALT4.ASPMX.L.GOOGLE.COM.`

A TXT record that starts with `google-site-verification=` is on both screenshots. The second slide asks which tools can identify the problem. It does not name any tools.

### Forwarder, conditional forwarder, and stub zone

This is one of the discussion questions. The three are different ways to send a query somewhere else.

If your DNS server does not know a name, the default is to start at the root and walk down until it finds the server that does. A forwarder replaces that walk.

**Forwarder.** Use this for names outside your network. You pick another DNS server and send those queries there. The slide’s reason: you control where the queries go, and that makes resolution faster and more predictable for your computers.

**Conditional forwarder.** Use this for one domain name only. That name can even be in a different top-level domain. Every query for that one name takes the single path you chose.

**Stub zone.** Use this when the other name sits under a domain you already know, which the slide calls a delegation below a delegation. The stub holds only three kinds of records: SOA, NS, and glue host (A). It is not authoritative. The lab says this saves bandwidth because the whole zone is not copied.

**Root hints** are the list your server uses to find the root servers when it does that default walk. A root server can answer for the root zone. For anything else it tells you which servers are authoritative for the right top-level domain. You need root hints when your server is authoritative only for its own lower part of the namespace and still has to find other zones.

**Zone delegation** is a subdomain that keeps the parent’s suffix, stored as its own zone on another server. The slide says this spreads the query load.

### Split DNS

Most organizations keep internal DNS and external DNS apart, for security.

1. Computers inside the firewall send every query to the AD-integrated DNS servers on the domain controllers.
2. Those servers answer with the internal addresses. People inside still have to be able to resolve the company’s own public names, such as mail and web.
3. A separate DNS server in the perimeter network answers people on the Internet. It holds only the records that must be visible from outside, such as mail and web.

The internal zone cannot be reached from outside the firewall. Internal names and addresses stay unpublished.

### Secondary zone lab

The primary is the domain controller **CA-VAN-SVR1** (192.168.239.1), zone `adatum.com`. The secondary is **CA-VAN-SVR4**.

1. Install the DNS role on Svr4.
2. On Svr4: Forward Lookup Zones → New Zone → Secondary → zone name `adatum.com` → master IP 192.168.239.1.
3. The zone says **“Zone not loaded by DNS server.”** The lab asks you why. The next step is the fix: the primary has not been told it may send the zone.
4. On the primary: zone Properties → Zone Transfers → Allow zone transfers → Only to the following servers → add Svr4’s IP. Then Notify, and add that same IP.
5. Refresh DNS Manager on Svr4. The zone should be there.
6. The lab asks whether you can add a record on the secondary. The zone notes call a secondary read-only, so the answer they are aiming at is no. You add records on the primary.

### Advanced tab

Three options are already turned on:

- **Round robin.** If one name has several A records, the server rotates which address it hands out first. That spreads the load.
- **Netmask ordering.** If several addresses exist, prefer the one on the client’s own subnet.
- **Secure cache against pollution.** Ignore extra records stuffed into a referral when those records are not for the name that was asked.

You can also turn **recursion** on or off on this tab. The Linux handout is the place that says an authoritative server should not recurse.

**Debug logging** writes a detailed file of DNS packets. It is for troubleshooting. The slide warns that it costs processing and disk.

### TTL, aging, and scavenging

**TTL** is how long a resolver may keep a record in cache.

**Aging** applies to dynamic records. You can also turn it on for static ones. A dynamic record has a timestamp.

Two timers follow:

- **No-refresh interval.** The timestamp cannot be updated. Other changes are still allowed, such as a new IP or a new port. This cuts replication traffic and stops records from being deleted too soon.
- **Refresh interval.** Anything can change, including the timestamp.

**Scavenging** deletes records that were not refreshed after both intervals have passed. The slide’s default for that total is **14 days**. Scavenging is off until you configure it. It needs several settings, and it can look like it runs at random.

### How you protect DNS

The security slide’s goal: stop false records from being added, and stop clients from being sent to the wrong address.

- **DNSSEC** proves the records are really from that zone, and it can prove a name really does not exist. It does not provide confidentiality or availability.
- **Socket pool** randomizes the source port of a query so an attacker has a harder time guessing it. Command on the slide: `dnscmd /Config /SocketPoolSize`, value 0 to 10,000.
- **Cache locking** stops someone from replacing a cached record while its TTL is still running. Commands on the slide: `dnscmd /Conifg /CatcheLockingPercent 100` and `Set-DnsServerCache -LockingPercent`. 100 means the record stays locked for the whole TTL. The dnscmd spelling on the slide is missing letters; that is how the slide prints it.
- **Secure cache against pollution** is the Advanced-tab option above. It is on by default.
- **Secure dynamic updates** are listed with AD-integrated zones.
- **Zone transfers** should be allowed only to the servers you name. The mistakes article says an open transfer lets an outsider download the whole zone. The lab uses “Only to the following servers.”
- **Least privilege:** only people who need to administer DNS should be able to. AD-integrated zones can also use ACLs.
- **Split DNS** keeps internal names off the Internet. That section is above.

**DNSSEC lab, the short version.** Signing the zone and telling clients to check the signature are two separate jobs.

Sign `adatum.com` in DNS Manager: DNSSEC → Sign the Zone → Customize zone signing parameters. The Key Master is the domain controller. Add a Key Signing Key and a Zone Signing Key, both with the defaults. Choose **nsce3** (that is the spelling in the lab) with the defaults. Turn on distribution of trust anchors, then check that DNSKEY records showed up under Trust Points. You can unsign the zone later.

Clients do not check signatures until a GPO says so. Create a GPO and open Computer Configuration → Policies → Windows Settings → Name Resolution Policy. A rule can match a suffix (the lab’s example is `microsoft.com`, which also covers its child domains), a prefix (the lab’s example is `www`), one exact FQDN, an IPv4 or IPv6 subnet (used for reverse lookups), or Any (everything else). On the DNSSEC tab, enable DNSSEC for the rule and require clients to check that the name and address were validated. The lab also notes IPsec can be required between the client and the DNS server. On the client, run `gpupdate /force`, then `gpresult /r`, and confirm the GPO applied.

### Who is allowed to change DNS

Only the people who actually need to administer DNS should be able to. That is the least-privilege slide. On an AD-integrated zone you can also delegate a zone and set ACLs.

### Adatum namespace worksheet

The lab’s rules:

- Everything hangs under **adatum.com**.
- The internal network uses a different domain from the external one.
- Sales, Human Resources, and Production each get their own subdomain.
- A host name says what the computer does: file, db, www, mail, or wk for a workstation.
- The web, FTP, and email servers on the perimeter stay in **adatum.com**.

The figure on the worksheet already uses these names:

- Outside: `www.adatum.com`, `ftp.adatum.com`, `mail.adatum.com`
- Internal parent: `int.adatum.com`
- Human Resources: `hr.int.adatum.com`, for example `file1.hr.int.adatum.com`
- Sales: `sl.int.adatum.com`, for example `db.sl.int.adatum.com`
- Production: `pr.int.adatum.com`, for example `wk2.pr.int.adatum.com`

### Nine DNS mistakes

1. **Lonely island.** A domain controller uses only itself for DNS (`127.0.0.1` or its own IP). With AD-integrated DNS it can become an island and replication fails. The first DC has to point at itself until a second DC exists. After that, point each DC at another DC.
2. **DNS is too far from users.** The article wants answers in under 25 ms, and says under 50 ms is acceptable. If a site has no domain controller, a caching DNS server on the file and print server is enough.
3. **AD zones stored as files.** For internal DNS, store the zone in AD.
4. **Secure updates only, while Linux or Mac machines also exist.** Those machines cannot register. Let DHCP register them, or allow nonsecure updates on that zone. The article’s point is that more registered names make machines easier to find. Secure-only is fine when every machine is domain-joined Windows.
5. **No reverse zone.** Build the `in-addr.arpa` zone so PTR records can turn an IP back into a name.
6. **Forwarding to a far-away DNS server.** A Tokyo DC that forwards to Dallas gets slow answers, and the answers are often not local to Tokyo.
7. **A forwarding loop.** A forwards to B and B forwards to A. DNS queries have no memory of who already asked, so the two servers bounce the same question until the link fills up. Forward one way only.
8. **Aging and scavenging left off.** Old dynamic records stay forever, including PCs that were shut down years ago. Turn scavenging on.
9. **Zone transfers.** Allow them to your own servers. Do not allow them to the outside world, because that hands someone the whole zone.

### Linux DNS handout

The handout installs BIND, whose service name is `named`, on **Ca-Van-Ns1** at **192.168.239.10**.

The config file is `/etc/named.conf`. Zone files go in `/var/named`. The example zone file is `Adatum.com.db`.

It listens on port 53 at 127.0.0.1 and at 192.168.239.10. Recursion and DNSSEC validation are turned on for this resolver. The file’s own comment says an authoritative server should not recurse, and a public recursive server must limit who can query it or it gets used in an amplification attack.

The root-hints zone in that file is `zone "." IN { type hint; file "named.ca"; };`. The Adatum zone is `type master; file "Adatum.com.db";`.

Open the firewall for 53/udp and 53/tcp, reload the firewall, then `systemctl restart named`. `netstat` then shows TCP 53 on 192.168.239.10 and on 127.0.0.1, and also TCP 953 on 127.0.0.1.

A Windows DNS server can be a secondary of a Unix primary. That is on the Windows zone-type slide.

The Windows lab names **nslookup** as the troubleshooting tool and does not give a command list. The DNSSEC lab uses `gpupdate /force` and `gpresult /r`.

### Week 9 discussion, in one pass

**What is DNS, and why do you need it?** It turns a name into an IP, on port 53 TCP and UDP. Clients also use it to find domain controllers, global catalog servers, and mail servers. If DNS is wrong, those services cannot be found.

**Four zone types.** Primary: the writable file, and the only place you edit. Secondary: a read-only copy for load and fault tolerance. Stub: SOA, NS, and glue A only, not authoritative. AD-integrated: stored in AD on domain controllers, multi-master, secure dynamic updates.

**The records.** A and AAAA are host to IP. PTR is IP to name. CNAME is an alias. MX is the mail server. SRV is a service plus a port, which is how a PC finds a domain controller. NS says who is authoritative. SOA is the one record that describes the zone. TXT/SPF is the text record the slide groups with email spoofing.

**How you protect it.** DNSSEC, socket pool, cache locking, secure cache against pollution, secure dynamic updates, zone transfers limited to named servers, least privilege, and split DNS.

**Forwarder vs conditional forwarder vs stub.** A forwarder handles names outside your network. A conditional forwarder handles one domain, even one in another top-level domain, and sends all of those queries down one path. A stub is for a name underneath a domain you already have. It keeps only SOA, NS, and glue A, and it does not copy the whole zone.

---

## Part 2 — Week 10, Module 9: DHCP

DHCP hands out IP settings automatically: address, subnet mask, default gateway, DNS servers, and the DNS domain name. The Microsoft DHCP service also supports IPv6.

Doing it by hand means typing every address. A typo, a wrong gateway, or a wrong DNS server breaks the machine, and every time a computer moves you have to edit it again. DHCP does that from one place.

Routers, switches, and printers normally keep a static address. The lease article says a printer left on DHCP can come back with a different address after a long shutdown, and then every PC that was pointed at the old address breaks. Leave those addresses outside the DHCP pool.

The deploy lab asks whether a client has to join the domain before it can use DHCP. The lab does not answer that.

### Getting an address: DORA

All four messages on the generation slide are broadcasts.

1. **DHCPDISCOVER.** The client broadcasts: is there a DHCP server?
2. **DHCPOFFER.** Every server that has a free address broadcasts an offer.
3. **DHCPREQUEST.** The client broadcasts which offer it accepts.
4. **DHCPACK.** The chosen server broadcasts that the lease is the client’s.

The lab tests this with `ipconfig /release` and `ipconfig /renew`. The scope wizard can also add a delay between the server hearing DISCOVER and sending OFFER.

### Keeping the address: 50%, 87.5%, 100%

The lease article calls the halfway point **T1** and the later point **T2**.

Think of an 8-day lease.

- At **50%** (day 4) the client sends DHCPREQUEST to try to keep the same address. The server answers with DHCPACK. If that works, both timers reset and the 8 days start over. The article’s example: the client reaches the server on day 5, so a fresh 8-day lease begins that day.
- If the 50% attempt fails, the client tries again at **87.5%**. The article calls this rebinding: it will take an answer from any DHCP server that is up.
- At **100%** the lease is over. The client starts from the beginning with DHCPDISCOVER.

If the computer boots while the lease is still valid, it checks that same lease instead of asking for a brand-new one.

A 1-hour guest lease tries to renew at 30 minutes. In the article’s coffee-shop math, a renewal at 35 minutes resets the clock, so the address stays reserved for about 95 minutes total.

### How long the lease should be

- Wired office: **8 days**. Machines stay put, and a shorter lease only adds DHCP traffic. The scope wizard’s default is also 8 days.
- Home: **24 hours** (1440 minutes, 86400 seconds) is the usual router default. 8 days is also fine, because a home does not gain and lose devices all day.
- Wireless: **about 24 hours**. Phones leave, and a long lease holds their addresses.
- Office guest network: **about 8 hours**, one work day.
- Café or hotspot: **about 1 hour**.

Keep about **20%** of the pool free. Count the devices, add 20%, and if it does not fit, make the pool bigger or the lease shorter.

The café in the article has 400 visitors a day, each staying 30 to 60 minutes, and only 200 addresses (192.168.0.10 through 192.168.0.210). A 24-hour lease means the first 200 guests hold every address for the rest of the day. A 1-hour lease gives them back. The article says that same pool can then serve on the order of 130 guests an hour.

Leave room outside the pool for static devices. The article’s pattern is a pool from .10 to .200, with printers and similar devices at .201 and above.

When you run DHCP and DNS together, the article says to turn on DNS scavenging so dynamic DNS records do not live forever.

### Install, then authorize

The DHCP server needs a static IP. In the lab that server is **CA-VAN-SVR1**, 192.168.239.1.

Install it from Server Manager → Add Roles and Features → DHCP Server, or with `Add-WindowsFeature DHCP`.

After install, in this order:

1. Create the DHCP security groups. The lab asks what **DHCP Administrators** and **DHCP Users** are. It does not define them.
2. Restart the DHCP Server service.
3. Authorize the server in Active Directory. Do this logged on as **Adatum\Administrator**.

If you are not that account, “use the following user’s credentials” is greyed out and you get **error 20079**. Sign in as the domain administrator and authorize it yourself. Before you retire a DHCP server, unauthorize it. The lab says `netsh` can list authorized servers. It does not print the command.

What authorization actually checks: when the service starts, the server asks a domain controller whether its own IP is on the authorized list. If it is, it serves clients. If it is not, it does not.

That only stops a rogue **domain-joined Windows** DHCP server. It does not stop a rogue access point or some other device that is not in the domain. The lab says to limit those with port security. The security slide also says to unplug unused network jacks and to require authenticated Layer 2 connections.

### A scope

A scope is the pool for one subnet. Nothing is handed out until you create one, and nothing is handed out if you leave it inactive. The last page of the wizard is Activate Scope, and the lab says you have to choose Yes.

A scope must have a start and end address, a subnet mask, and a lease duration.

It can also have exclusions, a delay between DISCOVER and OFFER, a reservation (one address pinned to one MAC), and options.

The wizard order in the lab:

1. A meaningful name and a description.
2. Start address, end address, and mask. You can use the whole subnet (1–254) and then exclude the servers. The policy lab’s office range is 192.168.239.100–200, mask 255.255.255.0.
3. Exclusions and delay.
4. Lease duration. The default shown is 8 days. The lab asks what you would use for wireless, and why. The lease article’s answer is about 24 hours.
5. Configure options: Yes.
6. Router, then DNS domain and DNS servers. The next page is WINS. The lab asks what WINS is and how it differs from DNS. It does not answer.
7. Activate the scope.

The relay lab also needs one scope per remote subnet: Houston 172.16.30.0/24, Mexico 172.16.40.0/24, Portland 172.16.50.0/24. The DHCP server is still 192.168.239.1.

On a client, run `ipconfig /release`, `ipconfig /renew`, and `ipconfig /all`. Then look under Address Leases in DHCP Manager and confirm the lease is there.

**Options** are the extra settings inside the lease. The slide says you can set them at four levels: the whole server, one scope, a class, or one reservation. The common scope options it names are the router (default gateway), the DNS domain name, and the DNS servers. It does not give option numbers, and it does not say which level wins.

**Exclusion** means those addresses are kept out of the pool. Use that for member servers, and for the static routers, switches, and printers in the lease article.

**Reservation** means one address is tied to one MAC address. That is the allocation slide.

### Relay agent

DHCPDISCOVER is a broadcast. A router that is not RFC 1542 compliant does not forward broadcasts, so clients on another subnet never hear the server.

A relay agent sits on the clients’ subnet, hears the broadcast, and sends it on to the DHCP server. The slide marks that forwarded path as unicast. On the picture, Subnet A has the DHCP server, Subnet B has the clients and the relay, and the router between them does not pass the broadcast.

In the lab you install the Remote Access role with the Routing role service, enable Routing and Remote Access as a LAN router, add the DHCP Relay Agent routing protocol, put 192.168.239.1 in the relay’s properties, and add the network interface that faces the clients.

You need a relay whenever the server and the clients are on different subnets and the router will not forward the DHCP broadcast. That is how one server in the lab serves Houston, Mexico, and Portland, with one scope per subnet.

### Policies

A policy can give different addresses, options, or lease times based on vendor class, user class, MAC address, FQDN, or relay-agent information. Vendor class comes from the hardware maker. User class is one you define.

The lab:

1. IPv4 → Define User Classes → Add → name **Sales**, data `sales`. You can define vendor classes for IPv4 and IPv6. You cannot define a user class for IPv6.
2. On the office scope (192.168.239.100–200), new policy **sales**, condition User Class equals Sales, address range 192.168.239.190–200, lease **8 hours**.
3. On the client: `ipconfig /setclassid "Ethernet" sales`, then release and renew.
4. The follow-up is a **Finance** class whose addresses are 192.168.239.100–150.

The lab’s own puzzle: the client can get an address in the right range and still get a 1-hour lease instead of 8 hours. The only hint written in the lab is “DHCP relay agent.” It does not explain further.

### Superscope

A superscope is a group of scopes, called member scopes, so one DHCP server can hand out addresses from more than one scope on a single physical network. The handout calls that network a **multinet**: more than one IP subnet on the same wire.

Use one when:

- the current pool is almost empty and you add a second subnet on the same wire
- the first scope already used the whole classful network, so you need another range on that same segment
- you are slowly moving clients from an old subnet to a new one
- the clients are behind a relay, and the far network is itself a multinet
- two DHCP servers on the same segment each own a different logical network

The module slide also mentions multicast scopes. The superscope handout does not define them.

### Two DHCP servers

The slides show three designs.

**Cluster.** Two cluster members, and the DHCP database sits on shared storage. You have to build the cluster.

**Split scope.** Two servers divide one subnet so their ranges do not overlap. The slide’s example is server A with 192.168.0.1–150 and server B with 192.168.0.151–254. The delay is **500 milliseconds**, so one server usually answers first. The steps are: install DHCP on the second server, right-click the scope, Advanced → Split-Scope, name the second server, then set the percentage and the delay.

**Failover.** Two servers serve the same scopes. The relationship name has to be unique. The slide’s example is `Svr1-Svr2`, and then it asks “Any problem?” The two modes are **hot standby** and **load sharing**. The slide does not give a percentage for either mode.

Four failover settings are on the slide:

- **MCLT** (Maximum Client Lead Time): when the partner takes over the scope.
- **Auto state switchover interval**: how long contact can be lost before the partner is treated as down.
- **Shared secret**: a password that checks the failover messages.
- **TCP 647**: the firewall rules created when you install DHCP, named Microsoft-Windows-DHCP-Failover-TCP-In and TCP-Out.

### The database

The file is **Dhcp.mdb**. It holds the scopes, leases, reservations, and the rest of the configuration. It lives in `%systemroot%\System32\DHCP`.

It backs itself up every 60 minutes. You can also back it up manually. **Reconcile** repairs inconsistencies. To move the service, export the data to a file on the old server and import that file on the new one. The slide says PowerShell or NetShell can do that. It does not show the commands.

### Security, then the discussion questions

- Unplug unused jacks. Require authenticated Layer 2 connections.
- Turn on the DHCP audit log: Event Viewer → Applications and Services Logs → Microsoft → Windows → DHCP-Server.
- **Name protection** stops a non-Windows computer from overwriting a Windows computer’s DNS name when both want the same name. It records the original machine with a **DHCID** record.
- Authorization, covered above. Port security covers the devices authorization does not stop.

The troubleshooting slide lists five problems and does not print the fixes. These facts from the rest of the module are the ones that match some of them:

- A client gets no address if the server is not authorized, if the scope was never activated, or if the clients are on another subnet and there is no relay.
- A damaged database can be restored from the 60-minute backup, repaired with Reconcile, or replaced by importing an export from the other server.
- An empty pool is the lease article’s problem: shorten the lease or make the pool bigger, and keep about 20% free. A superscope is the handout’s answer when the current pool is almost gone.
- Address conflicts, and a client getting an address from the wrong scope, are on the list. The module does not give the causes.

---

## Check yourself

Answer, then read the line under the question.

**DNS**

1. What port does DNS use?
   Port 53, both TCP and UDP, on Windows and Linux.

2. What is `computer1.sales.contoso.com` made of?
   Host `computer1`, domain `sales` under `contoso`, top-level domain `com`. That is the hierarchy slide.

3. Primary, secondary, stub, AD-integrated: one line each.
   Primary is the writable copy. Secondary is a read-only copy. Stub holds only SOA, NS, and glue A, and is not authoritative. AD-integrated is stored in AD, only on a domain controller, and any of those domain controllers can accept a change.

4. A new secondary says “Zone not loaded.” What do you change, and where?
   On the primary, allow zone transfers only to the secondary’s IP, and notify that same IP. Then refresh the secondary. You add records on the primary, not on the secondary.

5. What is on the SRV screenshot, in plain words?
   In `_msdcs.Adatum.com`, `_gc` is tcp port 3268, `_kerberos` is tcp and udp port 88, `_kpasswd` is tcp and udp port 464, and `_ldap` is tcp port 389. The name at the end of the row is the server, usually CA-VAN-Svr1 or CA-VAN-Svr2. Clients use the records for their own site before they cross the WAN.

6. Forwarder, conditional forwarder, or stub?
   Forwarder: names outside your network. Conditional forwarder: one domain, sent down one path. Stub: a name under a domain you already have; only SOA, NS, and glue A.

7. What does split DNS keep off the Internet?
   The internal zone. The external server publishes only what outside clients must see, such as mail and web.

8. What does DNSSEC prove, and what does it not prove?
   That the records are authentic, and that a missing name is really missing. It does not provide confidentiality or availability.

9. No-refresh, refresh, scavenging.
   No-refresh: the timestamp stays put. Refresh: the timestamp may be updated. Scavenging deletes the record after both have passed. The slide’s total is 14 days, and scavenging is off until you turn it on.

10. The lonely-island mistake.
    A domain controller that uses only itself for DNS can fail replication. After the second domain controller exists, point each one at the other.

**DHCP**

11. Write DORA, and say how those packets are sent.
    Discover, Offer, Request, Ack. The generation slide says all four are broadcasts.

12. What happens at 50%, 87.5%, and 100% of an 8-day lease?
    Day 4: the client asks to keep the address (DHCPREQUEST, then DHCPACK). If that fails, at 87.5% it asks any DHCP server. At 100% it starts over with DISCOVER.

13. Wireless devices are filling an 8-day pool. What lease do you use?
    About 24 hours, so addresses come back when the devices leave.

14. Why does the café’s 24-hour lease fail?
    200 addresses and 400 visitors. The first 200 guests hold every address all day.

15. A scope will not hand out addresses. What two lab facts explain that?
    The server was not authorized (error 20079 if you were not Adatum\Administrator), or the scope was not activated.

16. When do you need a relay?
    Clients and the DHCP server are on different subnets, and the router does not forward DHCP broadcasts.

17. What is a superscope for?
    Several scopes on one physical network that has more than one IP subnet. One case is a pool that is almost empty. Another is moving clients from an old range to a new one.

18. Split scope versus failover.
    Split scope divides one subnet, for example .1–150 and .151–254, with a 500 ms delay. Failover lets two servers serve the same scopes, either hot standby or load sharing. MCLT is when the partner takes the scope. The switchover interval is when the partner is considered down. The shared secret checks the messages. TCP 647 is the firewall rule.

19. Where is the DHCP database, and how often is it backed up?
    `%systemroot%\System32\DHCP\Dhcp.mdb`, every 60 minutes. Reconcile repairs inconsistencies.

20. What is name protection?
    It stops a non-Windows computer from taking a Windows computer’s DNS name. It uses a DHCID record.
