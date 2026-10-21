# ACIT 3420 Windows Server Administration — Mega Midterm Study Guide

Every topic from [`../Midterm.pdf`](../Midterm.pdf), in the **same order** as the PDF. Practice questions with answers are at the end.

## Contents

1. **Active Directory Domain Services (ADDS)**
2. **ADDS Database Partitions**
3. **ADDS Physical and Logical Components**
4. **FSMO Roles (Flexible Single Master Operations)**
5. **Global Catalog (GC)**
6. **IGDLA Model**
7. **Hyper-V and Hypervisors**
8. **Hyper-V Virtual Switches**
9. **Checkpoints in Hyper-V**
10. **iSCSI Storage Server and Storage Pool**
11. **RAID (Redundant Array of Independent Disks)**
12. **Enterprise Storage Solutions (DAS, NAS, SAN)**
13. **Storage Layout and Disk Requirements**
14. **Security Identifier (SID)**

---

## **1. Active Directory Domain Services (ADDS)**

> *Midterm: Definition: What is ADDS? · Why do we need domain services in a networked environment?*

### **What is AD DS?**

**Active Directory Domain Services** is a specialised database called a **directory**. It has three jobs:

| Job | Question it answers | How |
|---|---|---|
| **Store identities** | *What exists?* | Users, computers, groups, services stored as **objects** with **attributes** |
| **Authentication** | *Who are you?* | **Kerberos**, issued by the KDC running on every DC |
| **Authorization** | *What can you access?* | Group membership + permissions on network resources |

### **Why a network needs it**

- **One account, everywhere.** Without a domain, every server has its own local SAM accounts. With AD DS, **any DC can authenticate any sign-in anywhere in the domain** (slide example: log on at BBY *or* DTC campus).
- **Central administration.** The domain is the **administrative center**, e.g. for password policy and Group Policy.
- **Redundancy.** **Every DC holds a copy** of the domain database, continually synchronised. It's **multi-master**: you can write on any DC (except an RODC).
- **Scalability.** Domains, trees and forests let one organisation grow to many divisions while keeping a single directory.

### **Key vocabulary**

| Term | Meaning |
|---|---|
| **Domain controller (DC)** | Server with the AD DS role, holding a **writable** copy of AD |
| **Member server** | Domain-joined server **without** AD DS |
| **Object / attribute** | A resource (user, computer, printer…) / a property of it (first name, phone) |
| **Container vs leaf** | Container objects hold others (**Domain, OU**). Leaf objects don't (**users, computers, groups**) |
| **Schema** | Defines **every object class and attribute** AD can store. Apps like Exchange *extend* it |

---

## **2. ADDS Database Partitions**

> *Midterm: Overview of Schema, Configuration, Domain, and Application partitions.*

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

### **Files in `C:\Windows\NTDS`**

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

## **3. ADDS Physical and Logical Components**

> *Midterm: Physical components · Sites, replication topology · Logical components: Domains, trees, forests, organizational units (OUs).*

### **Physical components (what follows the real network)**

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

### **Replication topology**

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
```

> **Seen in the lab:** all four DCs (three domains!) sit in **`Default-First-Site-Name`**, which proves a site is independent of domain boundaries.

### **Logical components (what admins design)**

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

> **Takeaway:** *Sites are about bandwidth, domains are about administration.* Design sites from your WAN map, not your org chart.

---

## **4. FSMO Roles (Flexible Single Master Operations)**

> *Midterm: Definition, types of FSMO roles, their functions, and how they are distributed.*

### **Definition**

AD is **multi-master** (any writable DC accepts changes), but five operations would conflict if two DCs did them at once. Each of these is assigned to **exactly one DC**, which is the *operations master* for that role.

### **The five roles**

| Role | Scope | What it does | Managed in |
|---|---|---|---|
| **Schema Master** | **Forest** (1 per forest) | The only DC that can **change the schema** | **AD Schema** snap-in (`regsvr32 schmmgmt.dll` first) |
| **Domain Naming Master** | **Forest** | **Adds/removes domains** in the forest | **AD Domains and Trusts** |
| **PDC Emulator** | **Domain** (1 per domain) | **Time sync** source, **password changes**, **account lockout**, GPO editing, legacy PDC | **AD Users and Computers** → Operations Masters |
| **RID Master** | **Domain** | Hands out **pools of Relative IDs** so each DC can build **SIDs** for new objects | **ADUC** |
| **Infrastructure Master** | **Domain** | Updates **cross-domain object references** (e.g. a group member from another domain) | **ADUC** |

> **Memory hook:** *"Schema, Naming — the forest's two. PDC, RID, Infrastructure — every domain's three."*

### **How they're distributed**

- **2 forest-wide + 3 per domain.** A forest with 3 domains has 2 + (3 × 3) = **11** role assignments.
- By default all roles land on the **first DC** (forest root → all 5; first DC of each new domain → its 3 domain roles).
- If **every DC is a GC**, Infrastructure Master placement stops mattering (see the Global Catalog trade-off table below).

```cmd
netdom query fsmo        :: list the current role holders
```

| Situation | Action |
|---|---|
| Old holder is **online** (planned maintenance) | **Transfer** the role (GUI consoles above) |
| Old holder is **dead** and won't return | **Seize** the role with `ntdsutil`, then clean up the dead DC's metadata |

> **Takeaway:** losing the PDC Emulator breaks time sync and password changes; losing the RID Master eventually stops new object creation.

---

## **5. Global Catalog (GC)**

> *Midterm: Role of the Global Catalog in facilitating searches and logins across domains.*

**What it holds:** a **full** copy of its own domain **plus a partial attribute set of every object in every other domain** in the forest.

### **What it's used for**

| Use | Why the GC is needed |
|---|---|
| **Forest-wide search** | Find a user in `Indy.com` while you're in `Adatum.com` without querying every domain |
| **Logon** | At logon the DC checks **Universal group membership**, which is stored only in the GC |

- Port **3268** (normal LDAP is **389**). DNS SRV record: `_gc._tcp`.
- In the lab every DC was promoted with **☑ Global Catalog** (the default).

### **Slide exam question: "Can we set all DCs as GC?"**

| Benefits | Drawbacks |
|---|---|
| Faster logons and searches, a local GC in every site | More **replication traffic** |
| No dependence on a WAN link to reach a GC | More **disk space** on every DC |
| If **all** DCs are GCs, Infrastructure Master placement stops mattering | Bigger impact when Universal group membership changes |

> **Takeaway:** the GC is a logon dependency. A branch office with no reachable GC can have logon problems, which is why "make every DC a GC" is a common real-world choice.

---

## **6. IGDLA Model**

> *Midterm: Identity → Global Group → Domain Local Group → Access · Used for structured and scalable permission assignment.*

```
Identity (users / computers)
   └─► Global group         — WHO   (by role:     "ACIT Faculty Global")
         └─► Domain Local group  — WHAT  (by resource: "ACL_VanShare_Read")
               └─► Access    — the permission on the share / NTFS / printer
```

- **IGDLA:** **I**dentities → **G**lobal → **D**omain **L**ocal → **A**ccess.
- Same idea as Microsoft's **AGDLP** (Accounts → Global → Domain Local → Permissions). In multi-domain forests, **AGUDLP** inserts a **Universal** group in the middle.

### **Group scopes (you need these to apply IGDLA)**

| Scope | Can contain | Can be granted access to |
|---|---|---|
| **Global** | Users, computers, Global groups **from the same domain only** | Resources in **any** domain |
| **Domain Local** | Users, computers, **Global & Universal groups from any domain**, Domain Local groups from the **same** domain | Resources in **its own domain only** |
| **Universal** | Users, computers, Global & Universal groups **from any domain** (no Domain Local) | **Any** resource in the forest. Membership stored in the **GC** |

**Group types:** **Security** groups have a **SID** and can be given permissions. **Distribution** groups have **no SID** and are email-only. Either can be converted to the other.

### **Nesting matrix: can the row go inside the column?**

| member ↓ / container → | Global (same dom) | Global (other dom) | Universal | DL (same dom) | DL (other dom) |
|---|---|---|---|---|---|
| **Global** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Universal** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Domain Local** | ❌ | ❌ | ❌ | ✅ | ❌ |

### **Why IGDLA is "structured and scalable"**

SS64 example: 25 accountants need 3 resources.

| Approach | Memberships to maintain | New hire |
|---|---|---|
| Flat (users straight onto each resource group) | 25 × 3 = **75** | Remember all 3 groups |
| **IGDLA** (25 users → `Accounting` Global → 3 resource DL groups) | 25 + 3 = **28** | Add to **one** group |

- **Revoke** a whole team's access by removing one Global group from one DL group, with no ACL edits.
- **Safe by design:** a Domain Local group *can't* go inside a Global group, so you can't accidentally nest a resource group inside a people group.
- Group membership is evaluated **at logon**, so users must **log off and on** after a membership change.

### **Lab walkthrough (Group Nesting video)**

On the child DC (`BBY.Adatum.com`) → ADUC → `BBY` OU → **CIT Local** → Properties → **Members → Add… → Locations…** → change to **`Adatum.com`** → type `acit` → **Check Names** → add **ACIT Universal** and **ACIT Global**. This works because a **Domain Local** group accepts Global and Universal groups from **another domain**.

### **Slide 41 questions (likely exam material)**

`Adatum.com`: ACIT Global (G), ACIT Faculty Global (G), ACIT Local (DL), ACIT Universal (U). `Bby.Adatum.com`: CIT Global (G), CIT Local (DL), CIT Universal (U).

| # | Nest… → into… | Answer | Rule |
|---|---|---|---|
| 1 | ACIT Faculty Global → ACIT Global | ✅ | G → G, same domain |
| 2 | ACIT Universal → ACIT Global | ❌ | Global only takes same-domain users/computers/Globals |
| 3 | ACIT Local → ACIT Faculty Global | ❌ | DL can't go inside Global |
| 4 | ACIT Global → ACIT Universal | ✅ | G → U |
| 5 | ACIT Universal → ACIT Local | ✅ | U → DL |
| 6 | CIT Global → ACIT Global | ❌ | Global can't nest **across domains** |
| 7 | CIT Local → ACIT Local | ❌ | DL won't accept a DL from **another domain** |
| 8 | ACIT Universal → CIT Universal | ✅ | U → U, any domain |
| 9 | ACIT Universal → CIT Local | ✅ | DL accepts U from any domain (shown in the lab) |
| 10 | ACIT Global → CIT Universal | ✅ | U accepts G from any domain |

---

## **7. Hyper-V and Hypervisors**

> *Midterm: What is Hyper-V? · Hypervisor types: Type 1 (bare-metal) vs. Type 2 (hosted) · Use cases and advantages of each.*

### **Why virtualize?**

Modern hardware is huge (100+ cores, Server 2022 supports up to 64 TB RAM). One OS per physical server **wastes resources**. Running **multiple VMs on one host** saves money, improves efficiency, keeps services separated, and gives you safe, self-contained test systems.

### **What is Hyper-V?**

- The **hardware virtualization role** in Windows Server 2019/2022 (hypervisor-based virtualization for x64 since **Server 2008**).
- The **hypervisor sits between the hardware and the operating system** and **controls access to hardware**. Hardware drivers live in the **host OS**.
- Guest VMs **don't know** they run on virtualized hardware. Pick the wrong virtual hardware/profile and the guest OS can have problems.
- **Guest OSes:** Windows Server 2008 SP2+, Windows Vista SP2+, **Linux**, **FreeBSD**.

### **Type 1 vs Type 2 hypervisors**

| | **Type 1 (bare-metal)** | **Type 2 (hosted)** |
|---|---|---|
| Runs on | **Directly on the hardware** | **On top of a host OS**, as an application |
| Performance / overhead | Best performance, least overhead | Extra layer (host OS) → more overhead |
| Typical use | **Production servers, data centers** | **Desktops, labs, testing**, learning |
| Advantages | Speed, efficiency, stronger isolation, scales to many VMs | Easy to install on an existing PC, no dedicated server needed |
| Examples | Hyper-V, VMware ESXi | VMware Workstation, VirtualBox |

> ⚠ **Instructor nuance (lecture, 10:36):** Johnny says Hyper-V is *"type 2, and also type 1"* because it can be **enabled as a role inside Windows Server** *or* **installed bare-metal from the Hyper-V Server ISO**. On the exam, if asked which type Hyper-V is, **Type 1** matches slide 3's architecture, but be ready to explain his "both deployment styles" framing.

**Lab gotcha:** Hyper-V conflicts with other hypervisors. With **WSL / Virtual Machine Platform** on, or with **VirtualBox**, you can't run Hyper-V nested in **VMware Workstation**.

### **Prerequisites**

- Run **`systeminfo.exe`** to verify hardware support (VM Monitor Mode Extensions, virtualization enabled in BIOS, Data Execution Prevention).
- Host resources: **memory 8 GB+ (test)**, **storage SAN (enterprise) / S2D (test)**, **network 1 Gb (test) / 10 Gb (enterprise)**.
- **Nested virtualization** (a Hyper-V VM that is itself a Hyper-V host): ≥ **4 GB static memory**, same build on host and guest, useful for dev/test only.

### **Supporting details: virtual disks and VM generations**

| Format | Notes |
|---|---|
| `.vhd` | Old format, **~2 TB max**. Use only for Server 2008/2008 R2 compatibility |
| `.vhdx` | **Default choice**, larger than 2 TB |
| `.vhds` | VHD Set (shared) file VMs connect to |
| `.avhdx` | Differencing/**checkpoint** disk where changes are stored |

| Disk type | Use |
|---|---|
| **Fixed-size** | **Production**: full size is reserved up front, so hosts can't overcommit |
| **Dynamically expanding** | **Test**: grows as used. 3 VMs × 200 GB on < 400 GB free will eventually fill the disk |
| **Pass-through** | **Don't use**: maps a physical disk directly; very hard to move |
| **Differencing** | Stores only changes vs a parent (like a linked clone). Breaks if the parent is modified or removed. **Run Sysprep** before cloning this way |

| Gen 1 | Gen 2 |
|---|---|
| BIOS, IDE boot | **UEFI**, boot from virtual **SCSI** disk/DVD, **PXE** on the standard adapter |
| Supports 32-bit/old OSes | **64-bit only** |
| — | **Secure Boot**, **hot add** memory/NIC, **vTPM / shielded VMs** |

```powershell
Set-VMProcessor -VMName VM1 -EnableHostResourceProtection $true   # stop one VM hogging host CPU
Update-VMVersion "VMName"                                          # upgrade VM configuration version
Enter-PSSession -VMName VM1                                        # PowerShell Direct: no network needed
Invoke-Command -VMName VM1 -ScriptBlock { Get-Service }            # run a command inside the VM
```

- **PowerShell Direct:** host → VM only, **no network connectivity needed**, run PowerShell **as administrator**, supply **guest credentials**.
- **VM states:** Off, Starting, Running, Paused, Saved.
- **Import options:** Register in-place / Restore (keep the **existing unique ID**) vs **Copy** (create a **new unique ID**).
- **Best practices:** Dynamic **Memory** (not dynamic disks!), avoid differencing disks, multiple synthetic NICs, each VM's files on a separate volume, **don't store VMs in the default location**.

---

## **8. Hyper-V Virtual Switches**

> *Midterm: Types of virtual switches: Internal, External, Private · Differences and appropriate use cases.*

Created in **Hyper-V Manager → Virtual Switch Manager**.

![Virtual Switch Manager: External / Internal / Private](<../../transcripts/Lecture Video/frames/frame_0047.jpg>)

| Switch | VM ↔ VM (same host) | VM ↔ **Host** | VM ↔ physical network / other hosts | Needs a physical NIC? |
|---|---|---|---|---|
| **External** | ✅ | ✅ | ✅ | **Yes**, binds to one physical adapter |
| **Internal** | ✅ | ✅ | ❌ | No |
| **Private** | ✅ | ❌ | ❌ | No |

> **Memory hook:** *External = everywhere. Internal = inside this box (host included). Private = VMs only, not even the host.*

### **Use cases**

| Switch | When to use it |
|---|---|
| **External** | VMs need the LAN/internet, e.g. a VM file server users connect to |
| **Internal** | Host must manage/test VMs, but VMs stay off the real network |
| **Private** | Fully isolated lab: e.g. a test DC + client that must never touch production |

### **Configuration details from the lecture demo**

- **One physical NIC → one External switch.** Give it a meaningful name (he used `Internet`).
- After creating an External switch, Windows shows a new **`vEthernet (Internet)`** adapter. The **IP is copied from the physical NIC to the virtual adapter**.
- On the **physical NIC**, **IPv4 becomes unchecked** and **Hyper-V Extensible Virtual Switch** is bound instead. **This is normal: don't re-enable IPv4 or assign an IP to the physical adapter.**

![vEthernet adapter properties after creating the External switch](<../../transcripts/Lecture Video/frames/frame_0050.jpg>)

- Switches can also **configure VLANs**, and **capture** and **filter** traffic.

> **Takeaway:** pick the switch by blast radius. Private for anything risky, External only for VMs that genuinely need the network.

---

## **9. Checkpoints in Hyper-V**

> *Midterm: Definition and usage of checkpoints (snapshots) in virtual machine management.*

**Definition:** a checkpoint is a **snapshot of a VM at a particular point in time** that you can roll back to. "Checkpoint" is Hyper-V's name for a snapshot.

### **Standard vs Production**

| | **Standard checkpoint** | **Production checkpoint** |
|---|---|---|
| Captures | Disk **and memory/running state** | Disk data only, via **VSS** inside the guest |
| Consistency (slide wording) | **Application-consistent** | **Data-consistent** |
| On rollback | VM returns **running**, apps open exactly as they were | VM boots as if **from an offline state**; anything unsaved is gone |
| Default | **Yes** | — |

**Lecture example:** open Notepad, type text **without saving**, take a checkpoint, then roll back.
- **Standard:** Notepad is still open **with the unsaved text**.
- **Production:** Notepad is gone; only what was **saved to disk** exists.

### **How it works on disk**

- A checkpoint creates a **differencing disk**, an **`.avhd` / `.avhdx`** file, for each `.vhd(x)`. All new writes go there, like a database log.
- **Deleting** a checkpoint **merges** its `.avhdx` back into the previous checkpoint/parent.
- **Pass-through disks can't be checkpointed**: they're outside the hypervisor's control.

### **Checkpoint ≠ backup** ("make sure remember")

| Hyper-V checkpoint | VSS snapshot / backup |
|---|---|
| Rollback point for the **whole VM** (disk + memory + config) | **Disk only**, meant for backup apps to copy out |
| Lives **on the same storage** as the VM; depends on the parent disk | Copied **off** to long-term storage |
| You can build **chains and trees** of them | One snapshot at a time |
| **Aging checkpoints hurt performance and eat space**; a runaway `.avhdx` can fill the volume and stop the VM | VSS cleans up after itself |

### **When to take one**

Before **Windows updates**, before **installing new applications**, before **removing a service**: any time you modify the system. Delete it once you've verified the change.

---

## **10. iSCSI Storage Server and Storage Pool**

> *Midterm: Understanding iSCSI protocol and its role in enterprise storage · Storage pools and their benefits in virtualization environments.*

### **iSCSI protocol**

**iSCSI** carries **SCSI commands inside TCP/IP packets**, giving **block-level** access to storage over a normal Ethernet network, on **TCP port 3260**. Its role in enterprise storage: it builds a **SAN over ordinary Ethernet**, much cheaper than Fibre Channel, typical for **small–medium** deployments.

| Component | Role |
|---|---|
| **iSCSI target** | Runs on the storage device and listens for requests. In Windows: the **iSCSI Target Server** role service (File and Storage Services). Serves **virtual hard disks** as LUNs, supports **CHAP** authentication, diskless/network boot, app storage, lab environments |
| **iSCSI initiator** | The client side. **Installed by default** since Server 2008/Vista; just **start the service** and connect to a target. *Server Manager → Tools → iSCSI Initiator → Configuration* |
| **IQN** | **iSCSI Qualified Name**: globally unique ID for initiators and targets |
| **IP network** | Ordinary Ethernet (optionally dedicated switches/HBAs) |

**IQN format:**

```text
iqn.yyyy-mm.backward-naming-authority:unique-device-name
iqn.1991-05.com.microsoft:example          ← Windows initiator
```

- `yyyy-mm` = when the naming authority acquired its domain; `com.microsoft` = reversed domain name.
- An IQN is a **logical name, not tied to an IP address**. You use it on the target to say **which initiator may see which LUN**.

### **Making iSCSI production-ready**

- **MPIO** (Multipath I/O) / **MCS**: one connection makes storage *available* but not *highly available*. If a NIC or switch fails, the server loses its disk. MPIO (built in since Server 2008) adds redundant paths and more throughput.
- **iSNS** (Internet Storage Name Service): automatic **discovery and management** of iSCSI devices (name service, discovery domains/login control, state-change notification, database mapping).
- Considerations before deploying: network speed, high availability, security, staff skills, vendor support.

### **Storage pools (Storage Spaces)**

```
Physical disks (any size/type: SAS, SATA, SCSI, NVMe, USB — "JBOD")
   └─► Storage POOL       — aggregates disks into one manageable unit
         └─► Virtual disk  = "storage space"  — choose layout, provisioning, size
               └─► Volume  — formatted (NTFS/ReFS), used like any disk
```

- When creating a virtual disk you choose: **resiliency type** (simple, mirror, parity), **provisioning type** (**thin** = grows on demand, or **fixed** = reserved up front), and **size**.
- Disks must be **blank and unformatted**, with no existing volumes. Creating a pool needs only **1** physical disk.

### **Benefits of storage pools (especially in virtualization)**

- **Storage aggregation:** many cheap disks become one manageable unit.
- **Elastic capacity:** add disks later as needs grow.
- **Delegated administration.**
- **RAID-like resiliency without a hardware RAID controller.**
- **Thin provisioning** lets a Hyper-V host give VMs space that's only consumed as they use it.
- A Hyper-V host or an **iSCSI Target Server** can carve VHDX-backed space out of the pool and share it with other hosts.

> **Takeaway:** iSCSI without MPIO is a single point of failure. One switch outage takes every server's disk offline.

---

## **11. RAID (Redundant Array of Independent Disks)**

> *Midterm: Overview of RAID levels (0, 1, 5, 10) · Benefits, drawbacks, and required number of disks for each level.*

**What RAID does:** combines multiple disks into **one logical unit** for **fault tolerance** (via **mirroring** or **parity**) and/or **performance** (spreading I/O across disks). **RAID does not replace backups.**

| Level | How it works | **Min disks** | Fault tolerance | Usable capacity | Benefit | Drawback |
|---|---|---|---|---|---|---|
| **RAID 0**: striping | *"Striped set without parity or mirroring."* A1 on Disk 0, A2 on Disk 1, A3 on Disk 0… | **2** | **None**: lose one disk, lose everything | 100% | **Fastest** reads/writes | Zero redundancy |
| **RAID 1**: mirroring | *"Mirrored drives."* A1–A4 written identically to Disk 0 and Disk 1 | **2** | Survives **1** disk failure | **50%** | Simple, full redundancy | Half the raw space is lost |
| **RAID 5**: striping + distributed parity | *"Block level striped set with parity distributed across all disks."* Parity (Ap, Bp, Cp, Dp) rotates across disks | **3** | Survives **1** disk failure | (n − 1) disks | Good balance of space, speed and protection | Parity calc slows writes; a 2nd failure during rebuild = data loss |
| **RAID 10 (1+0)**: mirror, then stripe | *"Each pair of disks is mirrored, then the mirrored disks are striped."* | **4** | Survives **1 disk per mirrored pair** | **50%** | **Speed of striping + safety of mirroring** | Most expensive per usable GB |

> *Optional (on the slides, not in the midterm list):* **RAID 6** is like RAID 5 but with **two** parity blocks per stripe, so it survives **2** failures (min 4 disks).

**Windows dynamic-disk equivalents:**

| Dynamic volume | Equivalent | Note |
|---|---|---|
| **Striped** | **RAID 0** | 2+ disks, can't be mirrored or spanned |
| **Mirrored** | **RAID 1** | Can't be spanned |
| **Spanned** | (no RAID) | Extends one volume across up to **32** disks, no redundancy |
| **Simple** | — | Free space on one disk |

---

## **12. Enterprise Storage Solutions (DAS, NAS, SAN)**

> *Midterm: Comparison of DAS, NAS, and SAN · Use cases, advantages, and differences between them.*

| | **DAS** (Direct-Attached) | **NAS** (Network-Attached) | **SAN** (Storage Area Network) |
|---|---|---|---|
| What it is | Disks **inside** the server or cabled straight to it (external array, USB) | A **file-level** storage device on the LAN that provides **shared folders** | An enterprise network of storage that servers see **as if it were locally attached** |
| Access level | **Block** | **File** | **Block** (via **LUNs**) |
| Protocols | SCSI/SATA/SAS to the disk | **SMB/CIFS, NFS** over Ethernet | **Fibre Channel, FCoE, iSCSI** |
| Advantages | **Easiest to deploy and maintain**, **inexpensive** (no switches/routers), managed in Disk Management | **Relatively inexpensive centralized** storage, easy to configure | **Multiple servers** at once, **fastest/most robust**, **easily expandable**, **highest redundancy** |
| Disadvantages | **Isolated** to one server, less flexible, limited scalability | **Slower access**; not suitable for **SQL, Exchange** | **Most expensive**; needs **specialized skills** (LUN setup, vendor-specific tools) |
| Summary | **Least complex, low setup cost** | **Best in specific situations**, complements DAS/SAN | **Highest performance, most features** |

### **Block-level vs file-level**

- **Block-level:** the server gets a **raw volume (LUN)** and formats it itself (**NTFS** on Windows, VMFS on VMware), like "a blank hard drive you can do anything with". **High performing**, more complex to manage. Used for **databases (esp. clustered), Exchange (only block is supported), VMware VMFS, server boot**.
- **File-level:** you browse a share like `\\server\share`; the device owns the file system. **Simple and cheaper**: "nothing beats it when all you need is a place to dump files". Still uses block storage on the back end.

### **SAN transport options**

| Option | Cabling | Server needs | Cost / performance |
|---|---|---|---|
| **Fibre Channel** | Separate fibre network; FC switch fabric | **HBA** + NIC (two connections: LAN + SAN) | Highest performance (**32 Gbps**), most expensive, high training cost |
| **FCoE** | Ethernet to an FCoE switch, then FC to storage | Just Ethernet | FC benefits, cheaper; one network topology |
| **iSCSI** | **Plain Ethernet / TCP/IP** | Software initiator (or optional HBA) | **Much cheaper**, slightly lower performance; typical for **small–medium** deployments |

FC terms: **Node** (any device on the SAN), **WWN** (World Wide Name, unique ID), **Fabric** (all the switching hardware). Layouts: arbitrated loop, point-to-point, switched fabric.

### **Use cases (matching storage to workloads)**

Transactional databases and Exchange → **SAN/block** · user home folders and branch shares → **NAS/file** · single server, low budget → **DAS** · VM storage → SAN or a resilient storage pool · tiered app storage → mix.

---

## **13. Storage Layout and Disk Requirements**

> *Midterm: Planning storage configurations · Minimum disk requirements for different RAID levels and enterprise needs.*

### **Storage Spaces layouts: memorise the minimums**

| Layout | RAID analogue | Copies / protection | **Min disks** |
|---|---|---|---|
| **Simple** | RAID 0 | One copy, **no resiliency** | **1** |
| **Two-way mirror** | RAID 1 | 2 copies, survives **1** failure | **2** |
| **Parity** | RAID 5 | Data + parity, survives **1** failure | **3** |
| **Three-way mirror** | — | 3 copies, survives **2 simultaneous** failures | **5** |
| **Dual parity** | (RAID 6-like) | Survives **2** failures | **7** |

Only **three** layouts give real fault tolerance (simple doesn't).

### **Hardware RAID minimums (quick recall)**

| RAID 0 | RAID 1 | RAID 5 | RAID 10 |
|---|---|---|---|
| **2** | **2** | **3** | **4** |

### **Other planning choices**

| Decision | Rule from the slides |
|---|---|
| **Partition table** | **MBR**: ≤ 2 TB, max 4 primary partitions, single point of failure. **GPT**: up to **128** partitions, up to **18 EB**. *MBR < 2 TB, GPT > 2 TB* |
| **Disk type** | **Basic** (default, simple volumes only) vs **Dynamic** (simple, spanned, striped, mirrored; changes without reboot) |
| **File system** | **FAT/FAT32/exFAT** (basic, flash). **NTFS** (ACLs, encryption, journaling, auditing). **ReFS** (checksums/integrity streams, huge volumes, **storage pooling**, disk scrubbing, corruption resiliency) |
| **Drive type** | Performance and cost rise together: EIDE → SATA (~150 IOPS) → SCSI (~210 IOPS) → SAS → **SSD** (~1.5 M IOPS) |

```powershell
fsutil fsinfo volumeinfo c:                     # file system + supported features (NTFS: ACLs, EFS, quotas…)
fsutil fsinfo sectorinfo c:                     # sector size and alignment
Format-Volume -DriveLetter E -FileSystem ReFS   # format a volume as ReFS
```

> **Takeaway:** minimum-disk questions are free marks. RAID 0/1/5/10 = 2/2/3/4. Storage Spaces simple/2-way/parity/3-way/dual parity = 1/2/3/5/7.

---

## **14. Security Identifier (SID)**

> *Midterm: What is a SID? · Why is it important for security and identity management in Windows environments.*

> ⚠ **Coverage note:** no course file has a dedicated SID section. Everything below is what the course files *do* say about SIDs, plus the core definition.

### **What is a SID?**

A **unique identifier** given to every **security principal**: users, computers and **security** groups. Windows uses the SID, **not the name**, to decide who someone is and what they can access.

### **Where SIDs show up in the rest of the course**

| Where | What the course says |
|---|---|
| **RID Master** (FSMO) | Hands each DC a **pool of RIDs** so it can create **SIDs** for new objects. Domain SID + unique RID = the object's SID. Only **one DC per domain** may hand out RID pools, because two DCs issuing the same RID would create duplicate SIDs |
| **Security vs Distribution groups** | **Security groups have a SID** (so they can be put on ACLs). **Distribution groups have no SID**, so they can't be granted permissions |
| **Permissions / IGDLA** | Permissions are granted to the group's SID; users get access through the SIDs of the groups they belong to, collected **at logon** (hence "log off and on" after membership changes) |
| **Cloning VMs** (Hyper-V lecture) | Before cloning a Windows instance (e.g. from a differencing disk), **run Sysprep**. It generalizes the image so the copies don't share the same machine identity (SID) |
| **DC cloning** | The supported process (`Cloneable Domain Controllers` group + `New-ADDCCloneConfigFile`) exists so a copied DC gets its own identity |

### **Why it matters for security and identity management**

- **Renaming is safe.** Rename a user and their permissions survive, because ACLs store the SID.
- **Deleting is permanent.** Delete a user and recreate one with the same name → it gets a **new SID**, so it does **not** get the old permissions back.
- **Duplicate SIDs = identity confusion**, which is why RID allocation is a single-master role and why cloned machines are generalized.

---

## **Last-Minute Cheat Sheet**

**ADDS** = directory that **stores identities**, **authenticates** (Kerberos) and **authorizes**. Multi-master; every DC has a copy.

**Partitions** (`ntds.dit`): **Schema + Configuration → every DC in the forest** · **Domain → its own domain only** · **Application** (DNS) → where configured.

**Physical:** DCs, **sites** (fast-linked subnets), **bridgeheads**, KCC-built connections (every 15 min). **Logical:** OU (delegation, GPO) → Domain (security/replication boundary) → Tree (contiguous namespace) → Forest (shared schema, config, GC).

**FSMO:** forest → **Schema Master**, **Domain Naming Master**. Domain → **PDC Emulator** (time, passwords, lockout), **RID Master** (RID pools → SIDs), **Infrastructure Master** (cross-domain refs). `netdom query fsmo`. Transfer if alive, seize (`ntdsutil`) if dead.

**GC:** partial copy of every forest object; **forest-wide search + Universal group check at logon**; port **3268** (LDAP 389).

**IGDLA:** Identity → **Global** (who, same-domain members) → **Domain Local** (what, members from anywhere) → **Access**. DL can't go in G or U. G can't cross domains.

**Hypervisors:** **Type 1** = bare-metal (Hyper-V, ESXi) · **Type 2** = hosted on an OS (Workstation, VirtualBox).

**Switches:** **External** = VMs + host + network (needs physical NIC) · **Internal** = VMs + host · **Private** = VMs only.

**Checkpoints:** **Standard** (default, saves memory, application-consistent) vs **Production** (VSS, data-consistent). Creates **`.avhdx`**; deleting **merges**. **Not a backup.**

**iSCSI:** SCSI over TCP/IP, port **3260**, **target** (storage) ↔ **initiator** (client), **IQN** `iqn.1991-05.com.microsoft:name`. Add **MPIO** for HA, **iSNS** for discovery. **Pool** → virtual disk (resiliency + thin/fixed) → volume.

**RAID min disks:** 0 → **2** · 1 → **2** · 5 → **3** · 10 → **4**. RAID ≠ backup.

**DAS** (block, one server, cheap) · **NAS** (file, SMB/NFS, shared, slower) · **SAN** (block, LUNs, shared, fastest, most expensive).

**Storage Spaces min disks:** simple **1** · two-way mirror **2** · parity **3** · three-way mirror **5** · dual parity **7**. MBR ≤ 2 TB, GPT > 2 TB.

**SID:** unique ID of a security principal; permissions are stored against SIDs. RID Master makes them unique. Security groups have one, distribution groups don't. Sysprep before cloning.

---

## **Practice Questions**

**1. (ADDS Partitions)** Which statement about AD DS partitions is correct?
- A) The Domain partition replicates to every DC in the forest
- B) The Schema and Configuration partitions replicate to every DC in the forest
- C) The Application partition always replicates to every DC in the domain
- D) Each partition is stored in its own separate `.dit` file

**2. (Physical Components)** An administrator wants to control how often AD replicates across a slow WAN link between Vancouver and Burnaby. Which component do they configure?
- A) An Organizational Unit
- B) A child domain
- C) A site (and its site link)
- D) The Schema partition

**3. (Replication Topology)** In AD Sites and Services you see a connection named `<automatically generated>` under a DC's **NTDS Settings**. What created it, and how often is it recalculated?

**4. (FSMO)** Which pair of FSMO roles exists **once per forest**?
- A) PDC Emulator and RID Master
- B) Schema Master and Domain Naming Master
- C) Infrastructure Master and PDC Emulator
- D) RID Master and Schema Master

**5. (FSMO)** What does `netdom query fsmo` tell you, and when would you **seize** rather than **transfer** a role?

**6. (Global Catalog)** The Global Catalog listens on port `______`, while standard LDAP uses port `______`. The GC holds a ______ copy of objects from other domains.

**7. (Global Catalog)** Users in `Indy.com` report slow logons whenever the WAN link to head office is congested. The only Global Catalog is a DC in head office. What's the likely cause and what would you change?

**8. (IGDLA)** Following IGDLA, where do you assign the actual NTFS permission on a file share?
- A) Directly to each user account
- B) To the Global group
- C) To the Domain Local group
- D) To the Universal group only

**9. (Hypervisors)** Which statement best describes a **Type 1** hypervisor?
- A) It runs as an application on top of a desktop OS such as Windows 10
- B) It runs directly on the hardware and controls hardware access for the VMs
- C) It can only run Linux guests
- D) It requires a Type 2 hypervisor underneath it

**10. (Hyper-V)** What does `Enter-PSSession -VMName DC1` do, and what is its key requirement compared with normal remoting?

**11. (Virtual Switches)** Which virtual switch lets VMs talk to **each other and to the host**, but **not** to the physical network?
- A) External
- B) Internal
- C) Private
- D) Pass-through

**12. (Checkpoints)** When you take a checkpoint, Hyper-V creates a differencing disk with the extension `________`. A ________ checkpoint uses VSS and is data-consistent, while a ________ checkpoint also saves memory and is application-consistent.

**13. (Switches + Checkpoints)** You need a test DC and client on one Hyper-V host, **completely isolated** from both the production LAN **and** the host itself. Before a risky update on the DC you want a quick rollback point. Which switch type and which protection do you use, and why isn't that protection enough on its own for production?

**14. (iSCSI)** iSCSI communicates over TCP port `______`. The component on the storage device is the iSCSI ______, and the client side is the iSCSI ______. Both are identified by an ______ such as `iqn.1991-05.com.microsoft:example`.

**15. (RAID)** Which RAID level stripes data with **parity distributed across all disks** and requires a minimum of **three** disks?
- A) RAID 0
- B) RAID 1
- C) RAID 5
- D) RAID 10

**16. (DAS/NAS/SAN)** Which storage solution provides **block-level** access to **centralized** storage that multiple servers can use at once?
- A) DAS
- B) NAS
- C) SAN
- D) A spanned volume

**17. (Storage Layout)** In a Storage Spaces virtual disk wizard you choose **Three-way mirror** with **thin** provisioning. What do those two settings mean, and what's the minimum number of physical disks?

**18. (Storage Pool + iSCSI)** A small company wants shared, fault-tolerant **block-level** storage for two Hyper-V hosts but can't afford Fibre Channel. They have a Windows Server with five blank SATA disks. Which technologies would you combine, what layout survives **two** simultaneous disk failures, and what would you add so a single switch failure doesn't take the storage offline?

**19. (SID)** The FSMO role that hands out pools of ______ so DCs can create unique ______ for new objects is the ______ Master.

**20. (SID)** An admin deletes user `jsmith` by mistake, recreates `jsmith` with the same name and password, and adds them back to the `Sales` Global group. `jsmith` can open the Sales share (granted via `Sales` → `ACL_Sales_Read`) but **not** a personal folder whose NTFS permissions listed `jsmith` directly. Explain why, and say what IGDLA practice would have avoided the problem.

<details>
<summary><b>Answer key with explanations (click to expand)</b></summary>

1. **B.** Schema and Configuration are forest-wide. The Domain partition stays inside its own domain, Application partitions replicate to the DCs *you choose*, and all partitions live in the single `ntds.dit`.
2. **C.** Sites map to the **physical network**, and inter-site replication runs on a **schedule** over site links through **bridgehead** servers.
3. The **KCC (Knowledge Consistency Checker)**. It builds the replication topology automatically and recalculates every **15 minutes**. Force it with `repadmin /kcc`.
4. **B.** Schema Master and Domain Naming Master are forest-wide. The other three exist **once per domain**.
5. It lists which DC holds each of the **five FSMO roles**. **Transfer** when the holder is online (planned move). **Seize** with `ntdsutil` only when the holder is **permanently dead**, then do metadata cleanup.
6. **3268**, **389**, **partial** (a partial attribute set). It holds a *full* copy of its own domain only.
7. At logon the DC must check **Universal group membership**, which only the **GC** holds. With the only GC across a congested WAN, every logon waits on that link. **Fix:** make a DC in the Indy site a **Global Catalog**.
8. **C.** Identity → Global → **Domain Local → Access**. People go in the Global group, the Global group goes in the Domain Local group, and the permission goes on the Domain Local group.
9. **B.** Type 1 sits directly on the hardware. **A** describes Type 2 (VMware Workstation, VirtualBox).
10. It opens a **PowerShell Direct** session from the **host into VM `DC1`**. It needs **no network connectivity**, but only works **host → VM**, PowerShell must run **as administrator**, and you must supply **guest credentials**.
11. **B, Internal.** External also reaches the physical network; Private excludes the host. Pass-through is a disk type.
12. **`.avhdx`** (or `.avhd`). **Production** = VSS, data-consistent. **Standard** = includes memory, application-consistent (the default).
13. A **Private** switch (the only type that blocks VM ↔ host traffic) plus a **checkpoint** before the update. Not enough alone because **checkpoints are not backups**: they live on the same storage, depend on the parent disk, and aging `.avhdx` files degrade performance and can fill the volume.
14. **3260**, **target**, **initiator**, **IQN** (iSCSI Qualified Name).
15. **C, RAID 5.** RAID 0 has no parity, RAID 1 is mirroring, RAID 10 is mirrored pairs striped (4 disks).
16. **C, SAN.** Presents LUNs as if locally attached (block-level) and is shared. DAS is block-level but isolated to one server; NAS is shared but file-level.
17. **Three-way mirror** keeps **three copies** and survives **two simultaneous** failures. **Thin** provisioning allocates space from the pool **as it's used** rather than reserving it up front. Minimum **5** disks.
18. Put the five disks in a **storage pool**, create a **three-way mirror** virtual disk (needs 5 disks, survives 2 failures), and publish it with the **iSCSI Target Server** role (block-level SAN over ordinary Ethernet). Connect each host with the built-in **iSCSI Initiator**, and add **MPIO** with redundant network paths.
19. **RIDs (Relative IDs)**, **SIDs**, **RID** Master.
20. The recreated account has a **new SID**. The personal folder's ACL stores the **old SID**, so it doesn't match. The Sales share works because access is granted to the `ACL_Sales_Read` group's SID and the new `jsmith` is a member again via `Sales`. **IGDLA** avoids this by **never putting user accounts directly on ACLs**.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Which Hyper-V virtual disk format is the default choice and supports disks larger than 2 TB?

- A) `.vhd`
- B) `.avhdx`
- C) `.vhdx`
- D) `.vhds`

**2.** Which feature is available on a **Generation 2** VM but not on a Generation 1 VM?

- A) Secure Boot
- B) Booting from a virtual IDE disk
- C) Support for 32-bit guest operating systems
- D) BIOS-based startup

**3.** Which AD DS logical component is the **administrative, security and replication boundary** that shares one directory database?

- A) Organizational Unit
- B) Site
- C) Forest
- D) Domain

**4.** A **NAS** device gives clients access to storage using which protocols, and at which level?

- A) Fibre Channel and FCoE, at block level
- B) SMB/CIFS and NFS, at file level
- C) iSCSI, at block level
- D) SAS and SATA, directly to the disk

**5.** Which RAID level provides **no fault tolerance**, so losing one disk loses everything?

- A) RAID 0
- B) RAID 1
- C) RAID 5
- D) RAID 10

**6.** Which FSMO role is the domain's **time sync** source and also handles **password changes** and **account lockout**?

- A) Schema Master
- B) RID Master
- C) Infrastructure Master
- D) PDC Emulator

**7.** One VM on a Hyper-V host keeps consuming so much CPU that the other VMs slow down. Which command limits this?

- A) `Update-VMVersion "VM1"`
- B) `Enter-PSSession -VMName VM1`
- C) `Set-VMProcessor -VMName VM1 -EnableHostResourceProtection $true`
- D) `Invoke-Command -VMName VM1 -ScriptBlock { Get-Service }`

**8.** You're setting up a new 6 TB data disk that will need more than four partitions. Which partition table do you choose?

- A) MBR
- B) GPT
- C) Dynamic
- D) ReFS

**9.** What is the minimum number of physical disks for a **dual parity** Storage Spaces virtual disk?

- A) 3
- B) 4
- C) 5
- D) 7

**10.** Which group scope can contain Global and Universal groups **from any domain**, but can only be granted access to resources in **its own domain**?

- A) Domain Local
- B) Global
- C) Universal
- D) Distribution

**11.** After creating an **External** virtual switch named `Internet`, a colleague notices that **IPv4 is unchecked** on the physical NIC and wants to re-enable it and assign the old IP. What should you tell them?

- A) Re-enable IPv4, because the External switch needs an IP on the physical NIC to reach the LAN
- B) Delete the switch and create an Internal switch instead
- C) Leave it: this is normal, because the IP has moved to the `vEthernet (Internet)` adapter and the physical NIC is now bound to the Hyper-V Extensible Virtual Switch
- D) Leave it, but only until the VMs are converted to Generation 1

**12.** You open Notepad in a VM, type text without saving, take a **Production** checkpoint, and later roll back to it. What do you see?

- A) Notepad is open with the unsaved text, exactly as it was
- B) Notepad is gone; the VM starts as if from an offline state and only what was saved to disk exists
- C) The rollback fails because Production checkpoints can't capture a running VM
- D) Notepad is open, but the text is replaced by the last saved version

**13.** A test host has less than 400 GB free. An admin creates three VMs, each with a **200 GB dynamically expanding** disk. Everything works at first. What is the risk, and what disk type does the guide recommend for production?

- A) No risk, because dynamically expanding disks can never exceed free space; use pass-through disks in production
- B) The VMs will fail to boot immediately; use differencing disks in production
- C) The disks will be converted to `.vhd` and capped at 2 TB; use `.vhds` in production
- D) As the VMs use their space, the host disk will eventually fill up; use fixed-size disks in production

**14.** On an iSCSI Target Server, you need to make sure that only the SQL server can see the database LUN. What do you use to identify which client may connect?

- A) The initiator's IQN
- B) The SQL server's IP address only, because IQNs change with the IP
- C) The target's TCP port number
- D) A Distribution group containing the SQL server's computer account

**15.** An admin creates a group called `Finance Staff` and tries to add it to the NTFS permissions on a Finance folder, but the group can't be used there. The group was created as a **Distribution** group. What's the cause and fix?

- A) Distribution groups must be Universal; change the scope to Universal
- B) The folder is on a different domain; move the folder
- C) Distribution groups have no SID, so they can't be granted permissions; convert it to a Security group
- D) The RID Master is offline; seize it with `ntdsutil`

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** **`.vhdx`** is the default and supports disks larger than 2 TB. `.vhd` is the old format, capped at about 2 TB and kept only for Server 2008/2008 R2 compatibility.
2. **A.** **Secure Boot** is a Generation 2 feature, along with UEFI, SCSI boot and vTPM. IDE boot, BIOS and 32-bit support are all Generation 1 traits.
3. **D.** A **domain** is the admin, security and **replication boundary** sharing one directory database. An OU is a container *inside* a domain, and a site reflects the physical network.
4. **B.** NAS is **file-level** storage reached over **SMB/CIFS and NFS**. Fibre Channel, FCoE and iSCSI are SAN transports, which give block-level access.
5. **A.** **RAID 0** is striping with no parity or mirroring, so one failed disk loses everything. RAID 1, 5 and 10 each survive at least one disk failure.
6. **D.** The **PDC Emulator** handles time sync, password changes and account lockout. The RID Master hands out RID pools so DCs can create SIDs.
7. **C.** **`Set-VMProcessor ... -EnableHostResourceProtection $true`** stops one VM hogging host CPU. `Enter-PSSession -VMName` opens a PowerShell Direct session and doesn't limit resources.
8. **B.** **GPT** supports up to **128** partitions and disks well beyond 2 TB. **MBR** is limited to 2 TB and 4 primary partitions; Dynamic is a disk type and ReFS is a file system, not partition tables.
9. **D.** **Dual parity** needs at least **7** disks. 3 is the minimum for single parity and 5 is for a three-way mirror.
10. **A.** A **Domain Local** group accepts Global and Universal groups from any domain but can only be granted access in its own domain. A Universal group can be granted access to any resource in the forest.
11. **C.** Unchecked IPv4 on the physical NIC is **normal**. The IP is copied to the **`vEthernet (Internet)`** adapter, and the physical NIC is bound to the **Hyper-V Extensible Virtual Switch**. Re-enabling IPv4 or giving the physical adapter an IP is exactly what the guide says not to do.
12. **B.** A **Production** checkpoint uses VSS and is **data-consistent**, so the VM comes back as if from an **offline state** and unsaved work is gone. Option A describes a **Standard** checkpoint, which also saves memory.
13. **D.** Dynamically expanding disks grow as they're used, so 3 × 200 GB on under 400 GB free will **eventually fill the disk**. The guide recommends **fixed-size** disks for production and says not to use pass-through disks.
14. **A.** An **IQN** is a logical name, **not tied to an IP address**, and you use it on the target to say **which initiator may see which LUN**. Port 3260 identifies the iSCSI service, not a particular client.
15. **C.** **Distribution** groups have **no SID**, so they can't be put on ACLs; converting the group to a **Security** group gives it one. Group types can be converted either way, so this is a quick fix.

</details>
