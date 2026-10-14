# Second DC, Child Domain (Subdomain) and Domain Tree — Notes (ACIT3420)

> Source: `How to configure Second Domain SubDomain and Domain Tree.mp4` (44:57, silent screen recording, Windows Server 2022).
> Notes are written from on-screen content. Screenshots: `transcripts/How to configure Second Domain SubDomain and Domain Tree/dense/` (one every 15 s; frame `tNNN` ≈ (NNN−1)×15 s).

## What gets built

The video starts with one DC in the `Adatum.com` forest and ends with **three domains in one forest**:

```
Forest: Adatum.com
├── Tree 1: Adatum.com            (forest root)  DC1 + DC2
│     └── Van.Adatum.com          (child domain) SubDC
└── Tree 2: Indy.com              (tree domain)  DomainTree
```

| VM tab | Computer name | IP | Ends up as |
|---|---|---|---|
| ACIT3420-DC1 | Ca-Van-Svr1 | 192.168.239.1 | Existing forest root DC (Adatum.com) |
| ACIT3420-DC2 | Ca-Van-Svr2 | 192.168.239.2 | **Additional DC** in Adatum.com |
| ACIT3420-SubDC | Ca-Van-Svr3 | 192.168.239.3 | First DC of **child domain** `Van.Adatum.com` (NetBIOS name `VAN`) |
| ACIT3420-DomainTree | Us-Indy-Svr1 (renamed from Ca-Van-Svr4) | 192.168.239.4 | First DC of **tree domain** `Indy.com` (NetBIOS name `INDY`) |
| (client) | Ca-Van-Client3 | 192.168.239.20 | Computer in Adatum.com |

Network for all VMs: VMware **Custom (VMnet9)**, subnet `192.168.239.0/24`, mask `255.255.255.0`, gateway `192.168.239.254`. Each adapter is renamed to **"Vmnet 9"**.

The three `Add a new …` choices on the **Deployment Configuration** page are the heart of this lab:

| Wizard option | Used for | Domain type field |
|---|---|---|
| Add a domain controller to an existing domain | DC2 (redundancy in the same domain) | — |
| Add a new domain to an existing forest | SubDC | **Child Domain**: parent `Adatum.com`, new name `Van`, giving `Van.Adatum.com` |
| Add a new domain to an existing forest | DomainTree | **Tree Domain**: forest `Adatum.com`, new name `Indy.com` |
| Add a new forest | (not used) | — |

---

## Part 1: Add a second DC to Adatum.com (0:00–14:00, VM `ACIT3420-DC2`)

### Prep the server
1. Server Manager → Local Server: computer name **Ca-Van-Svr2**, WORKGROUP.
2. Network Connections: rename `Ethernet0` to **Vmnet 9**.
3. IPv4 properties (static):
   - IP `192.168.239.2`, mask `255.255.255.0`, gateway `192.168.239.254`
   - **Preferred DNS `192.168.239.1`** (DC1, which hosts the Adatum.com zone)
4. Test with `ping adatum` from an admin Command Prompt.

> The new server must use the **existing DC's DNS** before promotion, or it can't locate the domain.

### Install the role
5. Manage → **Add Roles and Features** → **Active Directory Domain Services** → *Add Features* (keep "Include management tools" checked). This pulls in Group Policy Management, RSAT AD DS and AD LDS tools, the AD PowerShell module, Active Directory Administrative Center, and the snap-ins.
6. When it finishes: notification flag → **Promote this server to a domain controller**.

### AD DS Configuration Wizard
| Page | Setting |
|---|---|
| Deployment Configuration | **Add a domain controller to an existing domain**. Domain `Adatum.com`. Credentials **Change… → `Adatum\Administrator`** |
| Domain Controller Options | ☑ DNS server, ☑ Global Catalog, ☐ RODC. Site `Default-First-Site-Name`. Set the **DSRM** password |
| Paths | Defaults: `C:\Windows\NTDS` (database and logs), `C:\Windows\SYSVOL` |
| Prerequisites Check | Passes with 2 warnings (see "Common warnings" below). Click **Install**; the server auto-reboots |

Install progress: *Checking domain upgrade status → Changing domain membership → Securing … → Configuring the DNS Server service*.

### After reboot
7. Server Manager now shows **Domain: Adatum.com**, with AD DS and DNS roles.
8. On DC2, change the DNS client settings so it also points at itself (alternate `192.168.239.2`).
9. From SubDC, `ping adatum.com` resolves to **192.168.239.2**, so DC2 is now registered as a DC for the domain.
10. Replication test: in ADUC on DC1, `Adatum.com → BCIT → CIT` holds users *Lei Zhang* and *Lisa Tim*. The presenter **deletes Lisa Tim on DC1** to show the change replicating to DC2.
11. ADUC → **Domain Controllers** now lists **CA-VAN-SVR1** and **CA-VAN-SVR2** (both GC).
12. DNS Manager on DC2 → `Adatum.com → _tcp` shows SRV records for **both** DCs:

| SRV record | Port | Purpose |
|---|---|---|
| `_ldap` | **389** | LDAP / locating DCs |
| `_kerberos` | **88** | Kerberos authentication |
| `_kpasswd` | **464** | Kerberos password change |
| `_gc` | **3268** | Global Catalog |

---

## Part 2: Create the child domain `Van.Adatum.com` (9:00–21:00, VM `ACIT3420-SubDC`)

### Prep
1. Computer name **Ca-Van-Svr3**, WORKGROUP (was on DHCP).
2. Rename the adapter to **Vmnet 9**, static IP `192.168.239.3` / `255.255.255.0` / gw `192.168.239.254`, **Preferred DNS `192.168.239.1`**.
3. `ping adatum.com` succeeds (reply from 192.168.239.2).
4. Add Roles and Features → AD DS. The info page reminds you to *install at least two DCs per domain* and that *AD DS requires a DNS server on the network*.
5. **Promote this server to a domain controller.**

### Wizard
| Page | Setting |
|---|---|
| Deployment Configuration | **Add a new domain to an existing forest**. Domain type **Child Domain**. Parent domain **`Adatum.com`**. New domain name **`Van`**. Credentials `Adatum\Administrator` |
| Domain Controller Options | Domain functional level **Windows Server 2016**. ☑ DNS, ☑ GC, ☐ RODC. Site `Default-First-Site-Name`. DSRM password |
| Additional Options | NetBIOS name **`VAN`** |
| Review Options | "Configure this server as the first Active Directory domain controller in a **new child domain**… child domain of **Adatum.com**". There's a **View script** button, which shows the equivalent PowerShell |

Install progress: *Checking forest upgrade status → Waiting for DNS installation → **Replicating the schema directory partition** → Securing … → Configuring DNS Server service*. The server reboots.

### Results
- Sign in as **`VAN\Administrator`**. Server Manager shows Domain **Van.Adatum.com**.
- ADUC on SubDC: `Van.Adatum.com → Domain Controllers` = **CA-VAN-SVR3** (GC).
- ADUC on DC2 (Adatum.com) still lists only SVR1 and SVR2. **Each domain has its own Domain Controllers container**; the child's DC doesn't appear in the parent's.
- DNS on DC2: the Adatum.com zone now contains a **`Van` delegation**. Promoting a child domain **automatically creates the DNS delegation** in the parent zone, so names in the child domain resolve from the parent.

---

## Part 3: Create the tree domain `Indy.com` (20:00–43:00, VM `ACIT3420-DomainTree`)

### Prep
1. System Properties → rename **Ca-Van-Svr4 → `Us-Indy-Svr1`** (stays in WORKGROUP), then reboot.
2. VMware VM Settings: Network Adapter **Custom (VMnet9)**. Specs: 2 GB RAM, 4 CPUs, 120 GB NVMe.
3. Rename the adapter to **Vmnet 9**, static IP `192.168.239.4` / `255.255.255.0` / gw `192.168.239.254` (DNS must point at an Adatum DC so it can find the forest).
4. Test with `ping adatum.com`.
5. Add Roles and Features → AD DS → **Promote this server to a domain controller**.

### Wizard
| Page | Setting |
|---|---|
| Deployment Configuration | **Add a new domain to an existing forest**. Domain type **Tree Domain**. Fields become **Forest name = `Adatum.com`** and **New domain name = `Indy.com`**. Credentials `Adatum\Administrator` |
| Domain Controller Options | Functional level Windows Server 2016. ☑ DNS, ☑ GC, ☐ RODC. DSRM password |
| DNS Options | Warning: *"A delegation for this DNS server cannot be created because the authoritative parent zone cannot be found…"*. ☐ **Create DNS delegation** (greyed out) |
| Additional Options | NetBIOS name **`INDY`** |
| Prerequisites Check, then Install | Auto-reboot (the "Applying computer settings" screen took about 4 minutes) |

> **Gotcha in the video:** at first the presenter typed `Indy.com` into the **Forest name** box. The forest name must be the **existing** forest (`Adatum.com`); `Indy.com` goes in **New domain name**.

### Verify
- **AD Sites and Services** (on DC2): `Sites → Default-First-Site-Name → Servers` lists **CA-VAN-SVR1, CA-VAN-SVR2, CA-VAN-SVR3, US-INDY-SVR1**. All four DCs from all three domains are in the **same forest and site**.
- **NTDS Settings** under CA-VAN-SVR1 shows `<automatically generated>` connections (created by the KCC) **from** SVR2, SVR3 and US-INDY-SVR1.
  - The connection from **US-INDY-SVR1** replicates only **Schema** and **Configuration**. Those partitions are **forest-wide**; the domain partition is replicated only among DCs of the **same** domain.
- Sign-in on Us-Indy-Svr1 defaults to `INDY\Administrator`. The presenter used **Other user** and logged in as `ADATUM\Administrator`, which works because of the automatic **two-way transitive trust** between trees in a forest.
  - `whoami /all` returns `adatum\administrator`, and `hostname` returns `Us-Indy-Svr1`.
- Server Manager on Us-Indy-Svr1: Domain **Indy.com**, AD DS and DNS roles.

### Problem: DC2 can't resolve indy.com

On DC2:

```
C:\> ping indy.com
Ping request could not find host indy.com. Please check the name and try again.
```

The presenter asks: *"Could you tell me why I can not ping indy.com domain? How to fix the problem?"*

**Why:** `Indy.com` is a **separate DNS namespace**. Unlike the child domain (where the wizard created a `Van` delegation inside `Adatum.com`), there's **no parent zone** for `indy.com` on the Adatum DNS servers, which is why the wizard warned that the delegation couldn't be created. Adatum's DNS has no idea where `indy.com` lives.

The other direction works: Us-Indy-Svr1 **can** `ping adatum.com` (reply from 192.168.239.2), because its DNS client points at an Adatum DC.

**Fix: Conditional Forwarder on the Adatum DNS server (DC2)**
1. DNS Manager → CA-VAN-SVR2 → right-click **Conditional Forwarders** → **New Conditional Forwarder…**
2. DNS Domain: **`Indy.com`**
3. IP addresses of the master servers: the Indy DNS server, i.e. **`192.168.239.4`** (Us-Indy-Svr1). The value wasn't readable on screen, but that's the Indy DC's IP.
4. "Store this conditional forwarder in Active Directory…" was left **unchecked**, so it lives on DC2 only. Check it and choose *All DNS servers in this forest* to make it apply to DC1 and the others too.
5. Timeout: **5 seconds**.

Conditional Forwarders now lists `Indy.com`, and `ping indy.com` from Adatum should resolve. For full two-way resolution without relying on DNS client settings, create the mirror forwarder on Us-Indy-Svr1 for `Adatum.com → 192.168.239.1 / .2`.

---

## Common warnings during promotion (both normal)

1. **"Allow cryptography algorithms compatible with Windows NT 4.0"**: Server 2022 DCs block weak legacy crypto by default (KB 942564). It's informational.
2. **"A delegation for this DNS server cannot be created because the authoritative parent zone cannot be found…"**: shown for DC2 and for the tree root. It's harmless for an additional DC. For a **new tree** it means you must sort out name resolution yourself (a conditional forwarder, stub zone, or manual delegation).

Post-reboot event noise seen: NETLOGON **5774** and **5719**, GroupPolicy **1058**, DNS Client **1014**. These are typical while DNS and replication settle right after promotion.

---

## Concepts to know

| Term | Meaning |
|---|---|
| **Additional DC** | A second DC in the **same domain**, for fault tolerance and load sharing. Microsoft recommends at least 2 per domain |
| **Child domain** | A new domain that **shares the parent's DNS namespace** (`Van.Adatum.com` under `Adatum.com`). Same tree. Gets an automatic two-way transitive parent–child trust and an automatic DNS delegation |
| **Tree domain** | A new domain with a **different (contiguous-root) namespace** (`Indy.com`) in the **same forest**. Gets an automatic two-way transitive **tree-root trust**. **No** automatic DNS delegation |
| **Forest** | One or more trees sharing a common **schema**, **configuration**, **Global Catalog** and trust. The first domain (`Adatum.com`) is the **forest root** |
| **Forest-wide partitions** | Schema and Configuration, which replicate to every DC in the forest. The **domain partition** only replicates within its own domain |
| **Global Catalog** | Partial copy of every object in the forest. Port **3268** |
| **DSRM password** | Directory Services Restore Mode password, used for offline AD recovery. Set separately on each DC |
| **NetBIOS domain name** | Short pre-Windows 2000 name (`ADATUM`, `VAN`, `INDY`), used in `DOMAIN\user` logons |
| **Conditional forwarder** | A DNS rule saying "send queries for *this* domain to *these* DNS servers". It's the usual way to resolve another tree's or another forest's namespace |
| **KCC** | Knowledge Consistency Checker, which creates the `<automatically generated>` replication connections |

## Checklist for promoting any new DC
1. Set a static IP. Set **preferred DNS to an existing DC**.
2. Rename the computer if needed (do this **before** promotion).
3. Test with `ping <domain>` to confirm DNS can find the domain.
4. Add the AD DS role, then **Promote this server to a domain controller**.
5. Choose the deployment type (existing domain / new child / new tree / new forest).
6. Supply **Enterprise Admin** credentials (`Adatum\Administrator`) when adding a domain to the forest.
7. DNS and GC on, set the DSRM password, check the NetBIOS name, Install, let it reboot.
8. Verify in ADUC, AD Sites and Services and DNS Manager, then test name resolution **both ways**.
