# ACIT 3420 Windows Server Administration — Midterm Study Guide

Built strictly from [`../Midterm.pdf`](../Midterm.pdf) (the 2-page topic list) and the course files that cover those topics. Every heading in `Midterm.pdf` maps to exactly one week below.

## Curriculum Outline

| Week | File | `Midterm.pdf` topics |
|---|---|---|
| **1** | [week-1-adds-foundations.md](week-1-adds-foundations.md) | ADDS (what & why) · Database Partitions · Physical and Logical Components (sites, replication topology, domains/trees/forests/OUs) · Global Catalog |
| **2** | [week-2-fsmo-igdla-sid.md](week-2-fsmo-igdla-sid.md) | FSMO Roles · IGDLA Model · Security Identifier (SID) |
| **3** | [week-3-hyper-v.md](week-3-hyper-v.md) | Hyper-V and Hypervisors (Type 1 vs 2) · Hyper-V Virtual Switches · Checkpoints |
| **4** | [week-4-server-storage.md](week-4-server-storage.md) | iSCSI Storage Server and Storage Pool · RAID 0/1/5/10 · DAS vs NAS vs SAN · Storage Layout and Disk Requirements |

Each week has: Learning Objectives → Key Concepts & Deep Dive → Module Tour (exact slides/timestamps) → Practical Takeaways → 5-question Knowledge Check with a collapsible answer key.

**Source files used:** `Module 5 Hyper-V.pdf`, `Lecture Video.mp4` (Hyper-V lecture, transcribed to `transcripts/Lecture Video/`), `Hyper-V Snapshots vs Snapshot Explained.pdf`, `ACIT3420 Server Storage.pdf`, `Storage Pool.pdf`, `How to identify the iSCSI software initiator node name.pdf`, `Block Level Storage vs File Level Storage.pdf`, the SAN intro video, plus the AD material already summarised in [`../study-guide/`](../study-guide/README.md) and the two lab notes.

---

## Last-minute cheat sheet

**AD DS** = directory that **stores identities**, **authenticates** (Kerberos) and **authorizes**. Multi-master; every DC has a copy.

**Partitions** (`ntds.dit`): **Schema + Configuration → every DC in the forest** · **Domain → its own domain only** · **Application** (DNS) → where configured.

**Logical:** OU (delegation, GPO) → Domain (security/replication boundary) → Tree (contiguous namespace) → Forest (shared schema, config, GC). **Physical:** DCs, **sites** (fast-linked subnets), **bridgeheads**, KCC-built connections (every 15 min).

**GC:** partial copy of every forest object; **forest-wide search + Universal group check at logon**; port **3268** (LDAP 389).

**FSMO:** forest → **Schema Master**, **Domain Naming Master**. Domain → **PDC Emulator** (time, passwords, lockout), **RID Master** (RID pools → SIDs), **Infrastructure Master** (cross-domain refs). `netdom query fsmo`. Transfer if alive, seize (`ntdsutil`) if dead.

**IGDLA:** Identity → **Global** (who, same-domain members) → **Domain Local** (what, members from anywhere) → **Access**. DL can't go in G or U. G can't cross domains.

**SID:** unique ID of a security principal; permissions are stored against SIDs. RID Master makes them unique. Security groups have one, distribution groups don't. Sysprep before cloning.

**Hypervisors:** **Type 1** = bare-metal (Hyper-V, ESXi) · **Type 2** = hosted on an OS (Workstation, VirtualBox).

**Switches:** **External** = VMs + host + network (needs physical NIC) · **Internal** = VMs + host · **Private** = VMs only.

**Checkpoints:** **Standard** (default, saves memory, application-consistent) vs **Production** (VSS, data-consistent). Creates **`.avhdx`**; deleting **merges**. **Not a backup.**

**RAID min disks:** 0 → **2** · 1 → **2** · 5 → **3** · 10 → **4**. RAID ≠ backup.

**Storage Spaces min disks:** simple **1** · two-way mirror **2** · parity **3** · three-way mirror **5** · dual parity **7**. Pool → virtual disk (resiliency + thin/fixed) → volume.

**DAS** (block, one server, cheap) · **NAS** (file, SMB/NFS, shared, slower) · **SAN** (block, LUNs, shared, fastest, most expensive).

**iSCSI:** SCSI over TCP/IP, port **3260**, **target** (storage) ↔ **initiator** (client), **IQN** `iqn.1991-05.com.microsoft:name`. Add **MPIO** for HA, **iSNS** for discovery.
