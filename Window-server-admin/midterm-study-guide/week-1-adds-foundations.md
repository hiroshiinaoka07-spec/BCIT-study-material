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
