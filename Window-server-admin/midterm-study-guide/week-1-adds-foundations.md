# Week 1: AD DS Foundations — Partitions, Structure & the Global Catalog

> **Midterm topics covered** (`Midterm.pdf` p.1, first four headings): *Active Directory Domain Services (ADDS)* · *ADDS Database Partitions* · *ADDS Physical and Logical Components* · *Global Catalog (GC)*
> **Sources:** `ACIT3420 Domain Controller (1).pdf` slides 3–35 (via [`../study-guide/week-03-…`](../study-guide/week-03-active-directory-and-domain-controllers.md)), lab video *How to configure Second Domain SubDomain and Domain Tree* ([`../second-dc-subdomain-domain-tree-notes.md`](../second-dc-subdomain-domain-tree-notes.md))

## Learning Objectives

By the end of this week you should be able to:

1. **Define** AD DS and **explain why** a networked environment needs centralized domain services instead of per-machine accounts.
2. **Name the four database partitions** and state exactly **where each one replicates**.
3. **Distinguish** logical components (OU, domain, tree, forest) from physical components (DC, site, replication topology), and **explain the Global Catalog's role** in logon and forest-wide search.

---

## 1. What is AD DS, and why do we need it?

**Active Directory Domain Services** is a specialised database called a **directory**. It has three jobs:

| Job | Question it answers | How |
|---|---|---|
| **Store identities** | *What exists?* | Users, computers, groups, services stored as **objects** with **attributes** |
| **Authentication** | *Who are you?* | **Kerberos**, issued by the KDC running on every DC |
| **Authorization** | *What can you access?* | Group membership + permissions on network resources |

**Why a network needs it (the "why" half of the midterm question):**

- **One account, everywhere.** Without a domain, every server has its own local SAM accounts. With AD DS, **any DC can authenticate any sign-in anywhere in the domain** (the slides' example: log on at BBY *or* DTC campus).
- **Central administration.** The domain is the **administrative center**, e.g. for password policy and Group Policy.
- **Redundancy.** **Every DC holds a copy** of the domain database, continually synchronised. It's **multi-master**: you can write on any DC (except an RODC).
- **Scalability.** Domains, trees and forests let one organisation grow to many divisions without losing a single directory.

**Key vocabulary**

| Term | Meaning |
|---|---|
| **Domain controller (DC)** | Server with the AD DS role, holding a **writable** copy of AD |
| **Member server** | Domain-joined server **without** AD DS |
| **Object / attribute** | A resource (user, computer, printer…) / a property of it (first name, phone) |
| **Container vs leaf** | Container objects hold others (**Domain, OU**). Leaf objects don't (**users, computers, groups**) |
| **Schema** | Defines **every object class and attribute** AD can store. Apps like Exchange *extend* it |

---

## 2. ADDS database partitions

The database is one file, **`ntds.dit`**, logically split into **partitions** (also called *naming contexts*). The exam question is really *"what's in it, and who gets a copy?"*

| Partition | Contains | Replicates to |
|---|---|---|
| **Schema** | Definitions of object classes and attributes | **Every DC in the forest** |
| **Configuration** | Forest topology: sites, services, which DCs exist | **Every DC in the forest** |
| **Domain** | Users, computers, groups, OUs of **one** domain | **Only DCs in that domain** |
| **Application** | App data, e.g. DNS zones (`DomainDnsZones`, `ForestDnsZones`) | **DCs you choose** |

> **Memory hook:** *Schema and Configuration are the forest's "rules and map", so everyone needs them. Domain data is private to its domain.*
>
> **Seen in the lab:** in AD Sites and Services, the connection from `US-INDY-SVR1` (Indy.com) to `CA-VAN-SVR1` (Adatum.com) replicates only **Schema; Configuration**, because they're different domains.

**Files in `C:\Windows\NTDS`:**

| File | Purpose |
|---|---|
| `ntds.dit` | The AD database (all partitions) |
| `EDB*.log` | Transaction logs |
| `EDB.chk` | Checkpoint: which log entries are already written to the database |
| `Edbres00001.jrs`, `Edbres00002.jrs` | 2 × 10 MB **reserve logs** so AD can finish transactions if the **disk fills up** |

**SYSVOL** (`C:\Windows\SYSVOL`) holds Group Policy and logon scripts, replicated between DCs.

**Viewing the Schema partition** (the snap-in is hidden by default):

```cmd
regsvr32 schmmgmt.dll
mmc
:: File > Add/Remove Snap-in > Active Directory Schema
```

---

## 3. Logical components (what admins design)

| Component | What it is | Key fact |
|---|---|---|
| **OU** | Container **inside** a domain | Used to **delegate admin rights** and **link GPOs** |
| **Domain** | Admin, security and **replication boundary** sharing one directory database | Where accounts are created |
| **Tree** | Domains with a **common root and contiguous DNS namespace** | `adatum.com` → `van.adatum.com` |
| **Forest** | One or more trees sharing **one schema, configuration and Global Catalog** | First domain = **forest root** |

```
                ┌──────────────── FOREST: Adatum.com ────────────────┐
  Tree 1                                          Tree 2
  Adatum.com  (forest root)                       Indy.com  (tree root)
     └── Van.Adatum.com  (child domain)
```

Rules to remember:

- Parent ↔ child and tree ↔ tree trusts inside a forest are **automatic, two-way and transitive**.
- **Unlike OUs, child domains do NOT inherit** permissions or policies from the parent. Each domain is a separate security entity.
- **Child vs tree** = a namespace decision. A child gets an **automatic DNS delegation**; a tree doesn't, so you need a **conditional forwarder** (the lab's "why can't I ping `indy.com`?" problem).

---

## 4. Physical components (what follows the real network)

| Component | What it is |
|---|---|
| **Domain controller** | Hosts `ntds.dit` and SYSVOL, runs Kerberos/KDC |
| **Site** | A group of **IP subnets connected at high speed** |
| **Bridgehead server** | The **one DC per site** chosen to exchange replication with other sites |
| **Site link / connection objects** | The paths replication travels over |

**What a site does:**

- Reflects the **physical network**, *not* the domain structure. One site can hold several domains; one domain can span several sites.
- Lets clients find the **closest DC** for logon.
- Controls **replication**: AD replicates efficiently when it knows where DCs are.
- Contains only **two object types: servers and configuration objects**.

### Replication topology

| | Within a site (intra-site) | Between sites (inter-site) |
|---|---|---|
| Speed | Seconds, change-notification based | On a **schedule** |
| Compression | Uncompressed | **Compressed** |
| Path | DC ↔ DC | Through **bridgehead servers** over **site links** |

- The **KCC (Knowledge Consistency Checker)** builds the topology automatically. You see its work as `<automatically generated>` connections under **NTDS Settings** in AD Sites and Services. It recalculates every **15 minutes**.
- Manual trigger: **AD Sites and Services → server → NTDS Settings → right-click connection → Replicate Now**.

```cmd
repadmin /replsum        :: first look: per-DC success/fail summary
repadmin /showrepl *     :: detail per partner
repadmin /kcc            :: force the KCC to recalculate now
netdom query fsmo        :: (Week 2) who holds the FSMO roles
```

> **Seen in the lab:** all four DCs (three domains!) sit in **`Default-First-Site-Name`**, which proves a site is independent of domain boundaries.

---

## 5. Global Catalog (GC)

**What it holds:** a **full** copy of its own domain **plus a partial attribute set of every object in every other domain** in the forest.

**What it's used for (the midterm wording: "searches and logins across domains"):**

| Use | Why the GC is needed |
|---|---|
| **Forest-wide search** | Find a user in `Indy.com` while you're in `Adatum.com` without querying every domain |
| **Logon** | At logon the DC checks **Universal group membership**, which is stored only in the GC |

- Port **3268** (normal LDAP is **389**). DNS SRV record: `_gc._tcp`.
- In the lab every DC was promoted with **☑ Global Catalog** (the default).

**Slide exam question: "Can we set all DCs as GC?"**

| Benefits | Drawbacks |
|---|---|
| Faster logons and searches, a local GC in every site | More **replication traffic** |
| No dependence on a WAN link to reach a GC | More **disk space** on every DC |
| If **all** DCs are GCs, Infrastructure Master placement stops mattering | Bigger impact when Universal group membership changes |

---

## Module Tour

| Where | What to look at |
|---|---|
| `Midterm.pdf` **p.1**, headings 1–3 and *Global Catalog* | The exact topic wording you'll be tested on |
| `ACIT3420 Domain Controller (1).pdf` slides 3–35 | AD DS definition, partitions, trees/forests, sites, GC (the PDF itself isn't in this folder; the content is in [`../study-guide/week-03-…`](../study-guide/week-03-active-directory-and-domain-controllers.md) §1–4) |
| [`../second-dc-subdomain-domain-tree-notes.md`](../second-dc-subdomain-domain-tree-notes.md) Part 3 "Verify" | The Sites and Services view: Schema/Configuration-only connection, KCC connections |
| `transcripts/How to configure Second Domain SubDomain and Domain Tree/dense/t127.jpg` | Sites and Services screenshot showing all DCs in one site |

## Practical Takeaways

- **Partitions explain replication traffic.** Adding a new domain doesn't flood other domains with user objects; only Schema and Configuration go forest-wide.
- **Sites are about bandwidth, domains are about administration.** Design sites from your WAN map, not your org chart.
- **The GC is a logon dependency.** In a multi-domain forest, a branch office with no reachable GC can have logon problems, which is why "make every DC a GC" is a common real-world choice.

---

## Knowledge Check: Week 1

**1. (Multiple choice)** Which statement about AD DS partitions is correct?
- A) The Domain partition replicates to every DC in the forest
- B) The Schema and Configuration partitions replicate to every DC in the forest
- C) The Application partition always replicates to every DC in the domain
- D) Each partition is stored in its own separate `.dit` file

**2. (Multiple choice)** An administrator wants to control how often AD replicates across a slow WAN link between Vancouver and Burnaby. Which component do they configure?
- A) An Organizational Unit
- B) A child domain
- C) A site (and its site link)
- D) The Schema partition

**3. (Fill in the blank)** The Global Catalog listens on port `______`, while standard LDAP uses port `______`. The GC holds a ______ copy of objects from other domains.

**4. (What does it handle?)** In AD Sites and Services you see a connection named `<automatically generated>` under a DC's **NTDS Settings**. What created it, and how often is it recalculated?

**5. (Scenario)** Users in `Indy.com` report slow logons whenever the WAN link to the head office is congested. The only Global Catalog is a DC in head office. Based on the guide, what's the likely cause and what would you change?

<details>
<summary><b>Answer key with explanations (click to expand)</b></summary>

1. **B.** Schema and Configuration are forest-wide. **A** is wrong: the Domain partition stays inside its own domain. **C** is wrong: Application partitions replicate to the DCs *you choose*. **D** is wrong: all partitions live in the single `ntds.dit`.
2. **C.** Sites map to the **physical network**, and inter-site replication runs on a **schedule** over site links through **bridgehead** servers. OUs and domains are logical structures and don't control replication timing.
3. **3268**, **389**, **partial** (a partial attribute set). It holds a *full* copy of its own domain only.
4. The **KCC (Knowledge Consistency Checker)** created it. It builds the replication topology automatically and recalculates every **15 minutes**. You can force it with `repadmin /kcc`.
5. At logon the DC must check **Universal group membership**, which only the **GC** holds. With the only GC across a congested WAN, every logon waits on that link. **Fix:** make a DC in the Indy site a **Global Catalog** (the "can we set all DCs as GC?" trade-off: faster logons in exchange for more replication and disk use).

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Which protocol does AD DS use to **authenticate** users, issued by the KDC running on every DC?

- A) LDAP
- B) DNS
- C) Kerberos
- D) SMB

**2.** Which file in `C:\Windows\NTDS` is the actual AD database that holds all the partitions?

- A) `ntds.dit`
- B) `EDB.chk`
- C) `EDB*.log`
- D) `Edbres00001.jrs`

**3.** What is the purpose of the two 10 MB **reserve log** files (`Edbres00001.jrs` and `Edbres00002.jrs`)?

- A) They record which log entries have already been written to the database
- B) They store Group Policy and logon scripts for replication
- C) They hold a backup copy of the Schema partition
- D) They let AD finish its transactions if the disk fills up

**4.** Which statement correctly describes a **tree** in AD DS?

- A) A container inside a domain used to link GPOs
- B) One or more domains sharing a common root and a contiguous DNS namespace
- C) A group of IP subnets connected at high speed
- D) The single domain that holds the Schema Master

**5.** A **site** in AD DS contains only two types of objects. Which two?

- A) Servers and configuration objects
- B) Users and computers
- C) OUs and GPOs
- D) Domains and trusts

**6.** The helpdesk should be able to reset passwords for Sales staff only, and the Sales computers need their own Group Policy. Which logical component should you create?

- A) A child domain
- B) A new site
- C) An Organizational Unit (OU)
- D) An application partition

**7.** You want to look at the Schema partition, but the Active Directory Schema snap-in isn't listed in `mmc`. What do you run first?

- A) `repadmin /kcc`
- B) `netdom query fsmo`
- C) `repadmin /showrepl *`
- D) `regsvr32 schmmgmt.dll`

**8.** You want a quick **first look** at replication health: a per-DC summary of successes and failures. Which command do you run?

- A) `repadmin /kcc`
- B) `repadmin /replsum`
- C) `netdom query fsmo`
- D) `regsvr32 schmmgmt.dll`

**9.** DNS zones such as `DomainDnsZones` and `ForestDnsZones` are stored in which partition?

- A) Application
- B) Configuration
- C) Domain
- D) Schema

**10.** A domain-joined server hosts file shares but does **not** have the AD DS role installed. What is it called?

- A) A bridgehead server
- B) A domain controller
- C) A Global Catalog server
- D) A member server

**11.** You add `Indy.com` to the `Adatum.com` forest as a **new tree**. From an Adatum DC, `ping indy.com` fails, although adding a child domain such as `Van.Adatum.com` earlier caused no such problem. What fixes it?

- A) Making the Adatum DC a Global Catalog
- B) Creating a conditional forwarder for `indy.com` in DNS
- C) Moving the Indy DC into a new site
- D) Running `repadmin /kcc` on the Indy DC

**12.** An admin sets a password policy on `Adatum.com` and expects the child domain `Van.Adatum.com` to pick it up automatically. It doesn't. Why?

- A) The trust between parent and child is one-way
- B) Policies only replicate between sites on a schedule
- C) Child domains do not inherit policies or permissions from the parent, because each domain is a separate security entity
- D) The Domain partition only replicates to DCs you choose

**13.** DC1 is in the Vancouver site and DC2 is in the Burnaby site. You've just made a change on DC1 and don't want to wait for the replication schedule. What do you do?

- A) In AD Sites and Services, open the server's **NTDS Settings**, right-click the connection and choose **Replicate Now**
- B) Run `repadmin /kcc` to force the change across
- C) Run `repadmin /replsum` to push the change
- D) Move DC2 into the Vancouver site's OU

**14.** In the lab, four DCs from **three different domains** all sit in `Default-First-Site-Name`. A classmate says this is misconfigured because every domain needs its own site. What's the correct response?

- A) They're right: a site can only contain DCs from one domain
- B) They're right: each domain must have its own bridgehead server
- C) It's fine: sites reflect the physical network, not the domain structure, so one site can hold several domains
- D) It's fine, but only because all four DCs are Global Catalogs

**15.** Your manager wants every DC in a multi-site, multi-domain forest made a Global Catalog. According to the guide, what is the main cost of doing this?

- A) Logons become slower because every DC must query the others
- B) The Infrastructure Master stops working
- C) Universal groups can no longer be created
- D) More replication traffic and more disk space used on every DC

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** **Kerberos** handles authentication, issued by the KDC on every DC. **LDAP** (port 389) is how you query the directory, not how users prove who they are.
2. **A.** **`ntds.dit`** is the single database file containing all partitions. `EDB.chk` is only the checkpoint file that tracks which log entries have been written.
3. **D.** The **reserve logs** give AD room to finish transactions if the disk fills up. Tracking which log entries are committed is the job of `EDB.chk` (option A).
4. **B.** A **tree** is domains with a common root and a **contiguous DNS namespace**, e.g. `adatum.com` → `van.adatum.com`. Option A describes an OU.
5. **A.** A site contains only **servers and configuration objects**. Users and computers live in the Domain partition, organised by OUs, not in sites.
6. **C.** **OUs** are used to **delegate admin rights** and **link GPOs** inside a domain. A child domain would be far heavier and would not inherit the parent's settings anyway.
7. **D.** The Schema snap-in is hidden by default, so you register it with **`regsvr32 schmmgmt.dll`** and then add it in `mmc`. `repadmin /kcc` only recalculates the replication topology.
8. **B.** **`repadmin /replsum`** is the first-look per-DC success/fail summary. `repadmin /kcc` forces the KCC to rebuild connections; it doesn't report health.
9. **A.** DNS zones live in **Application** partitions, which replicate to the DCs you choose. Configuration holds forest topology (sites, services, DCs), not DNS zones.
10. **D.** A **member server** is domain-joined but has no AD DS role. A domain controller, by definition, holds a writable copy of AD.
11. **B.** A child domain gets an **automatic DNS delegation**, but a new tree doesn't, so you need a **conditional forwarder**. The GC deals with search and logon, not DNS name resolution.
12. **C.** Unlike OUs, **child domains do not inherit** permissions or policies; each domain is its own security entity. Option A is wrong because parent ↔ child trusts are **two-way and transitive**.
13. **A.** **Replicate Now** on the connection under **NTDS Settings** triggers replication manually. `repadmin /kcc` only recalculates the topology and doesn't push the change.
14. **C.** Sites reflect the **physical network**, not domains: one site can hold several domains and one domain can span several sites. The lab setup proves exactly this.
15. **D.** Making every DC a GC means **more replication traffic** and **more disk space** on every DC. Option A is backwards: a local GC makes logons **faster**, and it also makes Infrastructure Master placement stop mattering rather than breaking it.

</details>
