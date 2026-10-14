# Week 3: Active Directory Fundamentals & Deploying Domain Controllers

> ACIT 3420 Windows Server Administration, Module 3–4 (part 1)
> Sources: `ACIT3420 Domain Controller (1).pdf` (slides 1–35), `Difference between Active Directory Domain Services (1).pdf`, the lab video *How to configure Second Domain SubDomain and Domain Tree*.

## Learning Objectives

By the end of this week you should be able to:

1. **Define** AD DS terminology: object, attribute, schema, partition, OU, domain, tree, forest, site, Global Catalog, functional level.
2. **Deploy** a domain controller three ways: as an additional DC, as a child domain, and as a tree domain. Know which wizard option and fields each one uses.
3. **Troubleshoot** the DNS side of AD: SRV records, delegation vs conditional forwarders, and why a new tree can't be pinged.

---

## 1. What is AD DS?

**Active Directory Domain Services** is a specialised database called a **directory**. It does three things:

| Job | Meaning |
|---|---|
| **Stores identities** | Users, computers, services |
| **Authentication** | *Who are you?* Checks the logon (Kerberos, using the KDC on each DC) |
| **Authorization** | *What can you access?* Network resources |

Facts about the **domain** (from the slides):

- AD DS needs **one or more domain controllers**.
- **Every DC holds a copy** of the domain database, continually synchronised (*multi-master*: you can write on any DC except an RODC).
- The domain is where user, computer and group accounts are created.
- The domain is a **replication boundary**: the domain partition only replicates to DCs of the same domain.
- The domain is an **administrative center**, e.g. for password policy.
- **Any DC can authenticate any sign-in anywhere in the domain** (e.g. you can log on at BBY or DTC campus).

### Key vocabulary

| Term | Definition |
|---|---|
| **Domain controller (DC)** | Server with the AD DS role, holding a **writable** copy of AD |
| **Member server** | Server joined to the domain but **without** AD DS installed |
| **Domain** | Container holding all network resources grouped in it; each resource is an **object** |
| **Object** | Represents a logical or physical resource (user, computer, printer…) |
| **Attribute** | A property stored on an object (e.g. first name, phone). Different object classes have different attributes |
| **Container object** | Can hold other objects: **Domain, OU** |
| **Leaf object** | Cannot hold other objects: **Users, Computers, Groups, Applications, Network resources** |
| **Schema** | Defines **all object classes and attributes** AD can store. Applications like Exchange *extend* the schema |

**Enabling the Schema snap-in** (it's hidden by default):

```cmd
regsvr32 schmmgmt.dll
mmc
:: File > Add/Remove Snap-in > Active Directory Schema
```

---

## 2. The AD database: partitions and files

The database is a single file, **`ntds.dit`**, logically split into **partitions** (also called naming contexts):

| Partition | Contains | Replicates to |
|---|---|---|
| **Schema** | Class and attribute definitions | **Every DC in the forest** |
| **Configuration** | Forest topology: sites, services, DCs | **Every DC in the forest** |
| **Domain** | Users, computers, groups, OUs of *one* domain | **Only DCs in that domain** |
| **Application** | App data, e.g. `DomainDnsZones`, `ForestDnsZones` | DCs you choose |

> **Seen in the lab:** in AD Sites and Services, the automatic connection from `US-INDY-SVR1` (Indy.com) to `CA-VAN-SVR1` (Adatum.com) replicates only **Schema; Configuration**. They're different domains, so no domain partition is shared.

**Files in `%systemroot%\NTDS` (default `C:\Windows\NTDS`):**

| File | Purpose |
|---|---|
| `ntds.dit` | **Main AD database**, holding all partitions and objects |
| `EDB*.log` | Transaction logs |
| `EDB.chk` | Checkpoint file (which log entries have been written to the database) |
| `Edbres00001.jrs`, `Edbres00002.jrs` | **Reserve logs**, 10 MB each, so AD can keep processing transactions if the **disk runs out of space** |

**SYSVOL** (`C:\Windows\SYSVOL`) holds Group Policy and logon scripts and is replicated between DCs.

---

## 3. Logical vs physical structure

### Logical (what admins design)

| Component | What it is |
|---|---|
| **OU** | Container *inside* a domain for organising objects and **delegating admin rights** / linking GPOs |
| **Domain** | Administrative and security boundary sharing one directory database |
| **Domain tree** | Domains in a hierarchy sharing a **common root and contiguous DNS namespace** |
| **Forest** | One or more trees sharing a common AD DS: **schema, configuration, Global Catalog** |

**Domain tree facts:**

- The first domain you create is the **root of a tree** *and* the **forest root domain**.
- **Two-way transitive trusts** exist between parent and child domains.
- All domains in a tree use the **same schema** and the **same Global Catalog**.
- Each domain is a **separate security entity** with its own GPOs, permissions and user accounts.
- **Unlike OUs, child domains do NOT inherit permissions or policies from the parent.**

```
                   ┌────────────── FOREST ──────────────┐
  Tree 1                                        Tree 2
  adatum.com  (forest root)                     fabrikam.com (tree root)
     ├── ca.adatum.com   (child)
     ├── us.adatum.com   (child)
     └── uk.adatum.com   (child)
```

Trees in the same forest have the **same two-way trusts** between them as parent and child domains do.

### Physical (follows the real network)

| Component | What it is |
|---|---|
| **Domain controller** | Hosts `ntds.dit` and SYSVOL; runs Kerberos/KDC |
| **Site** | A group of **IP subnets connected at high speed**. A TCP/IP-based container linked to subnets |
| **Bridgehead server** | The **one DC per site** chosen to exchange replication with other sites |

**What a site does:**

- Reflects the **physical network**. It is *not* tied to the domain structure: one site can hold several domains, and one domain can span several sites.
- Is used for **DC replication** (efficient when AD knows where DCs are).
- Lets clients find the **closest DC**.
- Contains only **two object types: servers and configuration objects**.
- Creates **redundant replication paths** between DCs.

> **Seen in the lab:** all four DCs (`CA-VAN-SVR1`, `CA-VAN-SVR2`, `CA-VAN-SVR3`, `US-INDY-SVR1`) sit in **`Default-First-Site-Name`**, even though they belong to three different domains.

---

## 4. Global Catalog (GC)

- Holds a **full copy of its own domain** plus a **partial attribute set of every other domain** in the forest.
- Used for **logon** (looking up Universal group membership), **forest-wide searches**, and **Universal group membership**.
- Port **3268** (LDAP is **389**).

**Exam question from the slides: "Can we set all DCs as GC?"**

| Benefits | Drawbacks |
|---|---|
| Faster logons and searches; every site has a local GC | More **replication traffic** (partial copy of every domain) |
| No dependency on a WAN link to reach a GC | More **disk/storage** on each DC |
| If **all** DCs are GCs, Infrastructure Master placement stops mattering | Larger impact when Universal group membership changes |

In the lab, every DC was promoted with **☑ Global Catalog** (it's the default).

---

## 5. Functional levels

- They give **backwards compatibility** when DCs run different Windows Server versions.
- Set the level to the **oldest** Windows Server version running on your DCs. Newer features stay disabled so all DCs interoperate.
- **Benefit** of raising it: new AD features are unlocked.
- **Drawback** of raising it: you can no longer add DCs running older versions, and raising is generally **one-way**.
- In the lab, the child and tree domains used **Windows Server 2016** domain functional level on Windows Server 2022.

---

## 6. Deploying a DC: the workflow

Deployment is always **two phases**:

1. **Install the role**: Server Manager → Manage → **Add Roles and Features** → **Active Directory Domain Services** (keep *Include management tools* checked).
2. **Promote**: notification flag → **Promote this server to a domain controller** (the AD DS Configuration Wizard).

**Before promoting**, on every new server:

- [ ] Rename the computer (do it **before** promotion)
- [ ] Set a **static IP**
- [ ] Set **Preferred DNS = an existing DC** (e.g. `192.168.239.1`)
- [ ] Test with `ping adatum.com`. If DNS can't find the domain, the promotion will fail

### The three Deployment Configuration options

| Option | Use when | Extra fields |
|---|---|---|
| **Add a domain controller to an existing domain** | Redundancy or load in the same domain | Domain name |
| **Add a new domain to an existing forest** | New child or tree domain | **Domain type**: *Child Domain* (Parent domain name + New domain name) or *Tree Domain* (Forest name + New domain name) |
| **Add a new forest** | Very first DC | Root domain name |

Remaining wizard pages: **Domain Controller Options** (functional level, ☑ DNS, ☑ GC, ☐ RODC, Site, **DSRM password**) → **DNS Options** (delegation) → **Additional Options** (NetBIOS name) → **Paths** (`C:\Windows\NTDS`, `C:\Windows\SYSVOL`) → **Review Options** (*View script* shows the PowerShell) → **Prerequisites Check** → **Install** (auto-reboot).

### Lab topology (VMnet9, `192.168.239.0/24`, gateway `.254`)

| VM | Computer | IP | Role | Wizard choice |
|---|---|---|---|---|
| ACIT3420-DC1 | Ca-Van-Svr1 | .1 | Forest root DC, `Adatum.com` | (already built) |
| ACIT3420-DC2 | Ca-Van-Svr2 | .2 | Additional DC, `Adatum.com` | *Add a DC to an existing domain* |
| ACIT3420-SubDC | Ca-Van-Svr3 | .3 | **Child** `Van.Adatum.com` (NetBIOS `VAN`) | *New domain → Child Domain*, Parent `Adatum.com`, New `Van` |
| ACIT3420-DomainTree | Us-Indy-Svr1 | .4 | **Tree** `Indy.com` (NetBIOS `INDY`) | *New domain → Tree Domain*, Forest `Adatum.com`, New `Indy.com` |

Credentials for every promotion: **`Adatum\Administrator`**. Adding a domain to the forest needs **Enterprise Admin** rights.

> **Gotcha seen in the video:** for a Tree Domain, the presenter first typed `Indy.com` in **Forest name**. The forest name must be the **existing forest** (`Adatum.com`).

### PowerShell equivalents (the preferred method on Server Core)

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools

# Additional DC in an existing domain
Install-ADDSDomainController -DomainName "Adatum.com" -InstallDns -Credential (Get-Credential)

# Child domain  -> Van.Adatum.com
Install-ADDSDomain -DomainType ChildDomain -ParentDomainName "Adatum.com" -NewDomainName "Van" -InstallDns -Credential (Get-Credential)

# Tree domain   -> Indy.com in the Adatum.com forest
Install-ADDSDomain -DomainType TreeDomain -ParentDomainName "Adatum.com" -NewDomainName "Indy.com" -InstallDns -Credential (Get-Credential)

# Brand-new forest
Install-ADDSForest -DomainName "Adatum.com" -InstallDns
```

### Normal warnings during promotion

1. *"Allow cryptography algorithms compatible with Windows NT 4.0"*: Server 2022 blocks weak crypto by default (KB 942564). Informational only.
2. *"A delegation for this DNS server cannot be created because the authoritative parent zone cannot be found…"*: harmless for an additional DC. **For a tree domain it means you must fix name resolution yourself.**

Post-reboot event noise seen in the lab: NETLOGON 5774/5719, GroupPolicy 1058, DNS Client 1014. These clear once DNS settles.

### Verifying a promotion

| Where | What you should see |
|---|---|
| Server Manager → Local Server | Domain = new domain; AD DS + DNS roles |
| ADUC → Domain Controllers | The new DC (type *GC*). **Each domain has its own** Domain Controllers container |
| AD Sites and Services | All forest DCs under the site, with `<automatically generated>` NTDS connections (built by the **KCC**) |
| DNS Manager → `_tcp` | SRV records for each DC |
| Logon screen | `VAN\Administrator`, `INDY\Administrator`, or `ADATUM\Administrator` (works thanks to the forest trust) |

---

## 7. DNS and AD

AD **cannot work without DNS**. Clients find DCs using **SRV records** registered in `_tcp` / `_msdcs`:

| SRV record | Port | Used for |
|---|---|---|
| `_ldap._tcp` | **389** | Locating DCs / LDAP |
| `_kerberos._tcp` | **88** | Kerberos authentication |
| `_kpasswd._tcp` | **464** | Kerberos password change |
| `_gc._tcp` | **3268** | Global Catalog |

**SRV registration failure:** if these records are missing, clients can't find a DC (join and logon failures). Fixes: point the DC's DNS at a correct server, then restart **Netlogon** (`net stop netlogon && net start netlogon`) or run `ipconfig /registerdns` and `dcdiag /test:dns`.

### Child vs tree domain DNS: the lab's troubleshooting question

> *"Could you tell me why I can not ping indy.com domain? How to fix the problem?"*

| | Child (`Van.Adatum.com`) | Tree (`Indy.com`) |
|---|---|---|
| Namespace | Inside `Adatum.com` | **Separate** namespace |
| DNS delegation | **Created automatically** (a `Van` delegation appears in the Adatum.com zone) | **Cannot** be created; there's no parent zone |
| Can Adatum DNS resolve it? | Yes | **No** (`Ping request could not find host indy.com`) |

**Fix:** on the Adatum DNS server, open DNS Manager → right-click **Conditional Forwarders** → **New Conditional Forwarder** → DNS Domain `Indy.com`, master server `192.168.239.4`. Optionally check *Store this conditional forwarder in Active Directory → All DNS servers in this forest* so DC1 gets it too. Add the mirror forwarder on the Indy DNS server for `Adatum.com`. Alternatives: a **stub zone**, or a secondary zone.

---

## 8. Other deployment options

| Option | Key facts |
|---|---|
| **Server Core** | Install AD DS with **PowerShell** (the preferred method). The same two phases: install the role, then promote |
| **Upgrading** | You can upgrade **2008 R2 SP1, 2012, 2012 R2** DCs to 2019; **nothing earlier**. Or add a new DC and retire the old one |
| **Install from Media (IFM)** | `ntdsutil` creates install media with a **copy of the AD database**, so a remote-site DC doesn't have to replicate the whole database over the WAN. Example: `ntdsutil "activate instance ntds" ifm "create sysvol full C:\IFM" quit quit` |
| **RODC** (Server 2008+) | **Read-only** full copy of the domain database for sites with **poor physical security** and slow WAN links. No outbound replication, and passwords are cached only per the **Password Replication Policy (PRP)** |
| **DC cloning** (Server 2012+) | Safely copy a **virtualised** DC to deploy quickly or rebuild a test lab. Add the source DC to the **Cloneable Domain Controllers** group, then run `New-ADDCCloneConfigFile` and export/copy the VM |

**Restricting domain users from joining computers:** by default any authenticated user can join **10** computers (`ms-DS-MachineAccountQuota`). Set it to **0** with ADSI Edit, or limit the **"Add workstations to domain"** user right in the Default Domain Controllers Policy GPO.

**Best practices (summary slide):**

- **Availability:** at least **two DCs per domain**.
- **Security:** use an **RODC** or **BitLocker** where physical security is weak.

---

## 9. AD DS vs Azure AD vs Azure AD DS

| | **AD DS** | **Azure AD** (now Entra ID) | **Azure AD DS** |
|---|---|---|---|
| Where | **On-premises**; you manage the DCs | **Cloud**, multitenant; Microsoft manages it | **Managed** AD DS domain in Azure |
| Protocols | LDAP, **Kerberos, NTLM** | **OAuth / OpenID Connect**, works over the internet | **Kerberos, NTLM**, LDAP |
| Management | **Group Policy** | **MDM (Intune)**; no Group Policy | Group Policy |
| Devices | Domain-joined computers | Azure AD-joined/registered (BYOD), SSO, Windows Hello | Azure server VMs (lift-and-shift legacy apps) |
| Domain/Enterprise Admin? | ✓ | — | ✕ |
| Schema extensions | ✓ | — | ✕ |
| Forest trusts | ✓ | — | One-way outbound only |
| Geo-distributed | ✓ | — | ✕ |

- **Managed domain:** Microsoft creates and runs the DCs (Azure AD DS). There are no forests, sites or replication links for you to design.
- **Self-managed domain:** you build DCs on Azure VMs with traditional tools and manage them yourself. You *can* extend the schema and create forest trusts.

---

## Repository Tour

| File | What to look at |
|---|---|
| `Window-server-admin/ACIT3420 Domain Controller (1).pdf` | Slides 3–35: terminology, partitions, trees and forests, sites, GC, deployment options |
| `Window-server-admin/Difference between Active Directory Domain Services (1).pdf` | AD DS vs Azure AD vs Azure AD DS tables |
| `Window-server-admin/second-dc-subdomain-domain-tree-notes.md` | Full step-by-step of the 45-minute lab |
| `transcripts/How to configure Second Domain SubDomain and Domain Tree/dense/` | Screenshots. Frame `tNNN` ≈ (NNN−1)×15 s. Useful ones: `t017` (DC2 wizard), `t067` (Child Domain), `t106` (Tree Domain), `t127` (Sites and Services), `t162` (failed ping), `t168` (conditional forwarder) |

![Child domain wizard](<../../transcripts/How to configure Second Domain SubDomain and Domain Tree/dense/t067.jpg>)

## Practical Takeaways

- **DNS first, always.** Most failed promotions and logons are a DNS problem: wrong preferred DNS, or missing SRV records.
- **Child vs tree** is a namespace decision. Use a child domain for a sub-division of the same organisation. Use a tree for an acquired company that keeps its own name (e.g. `Indy.com`). Trees need manual DNS forwarding.
- **Two DCs per domain** is the minimum for production. Losing your only DC means losing the domain.

---

## Knowledge Check: Week 3

**1. (Multiple choice)** Which AD partition replicates to **every DC in the forest**?
- A) Domain partition only
- B) Schema and Configuration partitions
- C) Application partition only
- D) None; every partition stays within its domain

**2. (Multiple choice)** You create `Van.Adatum.com` from the existing `Adatum.com` forest. In the AD DS Configuration Wizard, which deployment option and domain type do you choose?
- A) Add a new forest; Tree Domain
- B) Add a domain controller to an existing domain; Child Domain
- C) Add a new domain to an existing forest; Child Domain
- D) Add a new domain to an existing forest; Tree Domain

**3. (Fill in the blank)** The main AD DS database file is `________`, stored by default in `%systemroot%\________`. The two 10 MB `.jrs` files exist so AD can keep working when ________.

**4. (What does it handle?)** In DNS Manager under `Adatum.com → _tcp`, you see `_gc  [0][100][3268] ca-van-svr2.adatum.com.` What is this record for, and what would break if it disappeared?

**5. (Scenario)** After promoting `Us-Indy-Svr1` as the tree domain `Indy.com`, `ping indy.com` from DC2 (`Adatum.com`) fails with *"could not find host"*, but `ping adatum.com` from Us-Indy-Svr1 works. Why, and what exactly do you configure, and where?

<details>
<summary><b>Answer key (click to expand)</b></summary>

1. **B.** Schema and Configuration are forest-wide. The domain partition only replicates within its own domain. That's why the Indy→Adatum connection in Sites and Services showed only *Schema; Configuration*.
2. **C.** *Add a new domain to an existing forest*, type **Child Domain**, Parent `Adatum.com`, New domain name `Van`. Tree Domain is for a separate namespace like `Indy.com`.
3. **`ntds.dit`**, in **`NTDS`** (`C:\Windows\NTDS`). The reserve logs (`Edbres00001.jrs`, `Edbres00002.jrs`) let AD finish transactions **if the disk runs out of space**.
4. It's the **Global Catalog SRV record** (port **3268**). Clients use it to find a GC server. Without it, clients couldn't find a GC, so **forest-wide searches and Universal group lookups at logon would fail**. To fix it, restart Netlogon or check the DC's DNS settings so it re-registers.
5. `Indy.com` is a **separate DNS namespace**. With a child domain, the wizard creates a delegation in the parent zone automatically. For a tree there's **no parent zone**, which is why the wizard warned that it couldn't create the delegation, so Adatum's DNS doesn't know where `indy.com` lives. Indy can resolve Adatum because its DNS client points at an Adatum DC. **Fix:** on DC2, open DNS Manager → **Conditional Forwarders → New** → DNS domain `Indy.com`, master IP `192.168.239.4`. Optionally store it in AD for all DNS servers in the forest.

</details>
