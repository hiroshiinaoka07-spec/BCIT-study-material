# Week 4: Server Storage — RAID, DAS/NAS/SAN, iSCSI & Storage Pools

> **Midterm topics covered** (`Midterm.pdf` p.2): *iSCSI Storage Server and Storage Pool* · *RAID (0, 1, 5, 10)* · *Enterprise Storage Solutions (DAS, NAS, SAN)* · *Storage Layout and Disk Requirements*
> **Sources:** `ACIT3420 Server Storage.pdf` (Module 7, 45 slides), `Storage Pool.pdf`, `How to identify the iSCSI software initiator node name.pdf`, `Block Level Storage vs File Level Storage.pdf` (TechRepublic), SAN intro video ([`transcripts/Intro to Storage Area Network…/transcript.md`](<../../transcripts/Intro to Storage Area Network SAN Technologies (Network  Complete Video Course - Sample Video)/transcript.md>))

## Learning Objectives

By the end of this week you should be able to:

1. **State the minimum disks, benefits and drawbacks** of RAID 0, 1, 5 and 10, and of each Storage Spaces layout.
2. **Compare DAS, NAS and SAN** (block-level vs file-level access) and pick the right one for a workload.
3. **Explain iSCSI** — targets, initiators, IQNs, port 3260 — and how **storage pools** turn physical disks into virtual disks.

---

## 1. RAID (Redundant Array of Independent Disks)

**What RAID does (slide 9):** combines multiple disks into **one logical unit** for **fault tolerance** (via **mirroring** or **parity**) and/or **performance** (spreading I/O across disks). **RAID does not replace backups.**

| Level | How it works (slide diagram) | **Min disks** | Fault tolerance | Usable capacity | Benefit | Drawback |
|---|---|---|---|---|---|---|
| **RAID 0** — striping | *"Striped set without parity or mirroring."* A1 on Disk 0, A2 on Disk 1, A3 on Disk 0… | **2** | **None** — lose one disk, lose everything | 100% | **Fastest** reads/writes | Zero redundancy |
| **RAID 1** — mirroring | *"Mirrored drives."* A1–A4 written identically to Disk 0 and Disk 1 | **2** | Survives **1** disk failure | **50%** | Simple, full redundancy | Half the raw space is lost |
| **RAID 5** — striping + distributed parity | *"Block level striped set with parity distributed across all disks."* Parity (Ap, Bp, Cp, Dp) rotates across disks | **3** | Survives **1** disk failure | (n − 1) disks | Good balance of space, speed and protection | Parity calc slows writes; a 2nd failure during rebuild = data loss |
| **RAID 10 (1+0)** — mirror, then stripe | *"Each pair of disks is mirrored, then the mirrored disks are striped."* | **4** | Survives **1 disk per mirrored pair** | **50%** | **Speed of striping + safety of mirroring** | Most expensive per usable GB |

> *Optional (on the slides, not in the midterm list):* **RAID 6** — like RAID 5 but with **two** parity blocks per stripe, so it survives **2** failures (min 4 disks).

**Windows dynamic-disk equivalents (slide 3):**

| Dynamic volume | Equivalent | Note |
|---|---|---|
| **Striped** | **RAID 0** | 2+ disks, can't be mirrored or spanned |
| **Mirrored** | **RAID 1** | Can't be spanned |
| **Spanned** | (no RAID) | Extends one volume across up to **32** disks, no redundancy |
| **Simple** | — | Free space on one disk |

---

## 2. Enterprise storage solutions: DAS vs NAS vs SAN

| | **DAS** (Direct-Attached) | **NAS** (Network-Attached) | **SAN** (Storage Area Network) |
|---|---|---|---|
| What it is | Disks **inside** the server or cabled straight to it (external array, USB) | A **file-level** storage device on the LAN that provides **shared folders** | An enterprise network of storage that servers see **as if it were locally attached** |
| Access level | **Block** | **File** | **Block** (via **LUNs**) |
| Protocols | SCSI/SATA/SAS to the disk | **SMB/CIFS, NFS** over Ethernet | **Fibre Channel, FCoE, iSCSI** |
| Advantages | **Easiest to deploy and maintain**, **inexpensive** (no switches/routers), managed in Disk Management | **Relatively inexpensive centralized** storage, easy to configure | **Multiple servers** at once, **fastest/most robust**, **easily expandable**, **highest redundancy** (redundant switches, UPS, drives) |
| Disadvantages | **Isolated** to one server, less flexible, limited scalability | **Slower access**; not suitable for **SQL, Exchange** | **Most expensive**; needs **specialized skills** (LUN setup, vendor-specific tools) |
| Summary (slide 27) | **Least complex, low setup cost** | **Best in specific situations**, complements DAS/SAN | **Highest performance, most features** |

**Block-level vs file-level (slide 28, TechRepublic, SAN video):**

- **Block-level:** the server gets a **raw volume (LUN)** and formats it itself (**NTFS** on Windows, VMFS on VMware) — "a blank hard drive you can do anything with". **High performing**, more complex to manage. Used for **databases (esp. clustered), Exchange (only block is supported), VMware VMFS, server boot**.
- **File-level:** you browse a share like `\\server\share`; the device owns the file system. **Simple and cheaper**, "nothing beats it when all you need is a place to dump files". Still uses block storage on the back end.

**SAN transport options (slides 22–26, SAN video):**

| Option | Cabling | Server needs | Cost / performance |
|---|---|---|---|
| **Fibre Channel** | Separate fibre network; FC switch fabric | **HBA** + NIC (two connections: LAN + SAN) | Highest performance (**32 Gbps**), most expensive, high training cost |
| **FCoE** | Ethernet to an FCoE switch, then FC to storage | Just Ethernet | FC benefits, cheaper; one network topology |
| **iSCSI** | **Plain Ethernet / TCP/IP** | Software initiator (or optional HBA) | **Much cheaper**, slightly lower performance; typical for **small–medium** deployments |

FC terms: **Node** (any device on the SAN), **WWN** (World Wide Name, unique ID), **Fabric** (all the switching hardware). Layouts: arbitrated loop, point-to-point, switched fabric.

---

## 3. iSCSI storage server

**iSCSI** carries **SCSI commands inside TCP/IP packets**, giving **block-level** access to storage over a normal Ethernet network, on **TCP port 3260**.

| Component | Role |
|---|---|
| **iSCSI target** | Runs on the storage device and listens for requests. In Windows: the **iSCSI Target Server** role service (File and Storage Services) — serves **virtual hard disks** as LUNs, supports **CHAP** authentication, diskless/network boot, app storage, lab environments |
| **iSCSI initiator** | The client side. **Installed by default** since Server 2008/Vista; just **start the service** and connect to a target. *Server Manager → Tools → iSCSI Initiator → Configuration* |
| **IQN** | **iSCSI Qualified Name** — globally unique ID for initiators and targets |
| **IP network** | Ordinary Ethernet (optionally dedicated switches/HBAs) |

**IQN format** (IQN handout):

```text
iqn.yyyy-mm.backward-naming-authority:unique-device-name
iqn.1991-05.com.microsoft:example          ← Windows initiator
```

- `yyyy-mm` = when the naming authority acquired its domain; `com.microsoft` = reversed domain name.
- An IQN is a **logical name, not tied to an IP address**. You use it on the target to say **which initiator may see which LUN**.

**Making iSCSI production-ready:**

- **MPIO** (Multipath I/O) / **MCS**: one connection makes storage *available* but not *highly available*. If a NIC or switch fails, the server loses its disk. MPIO (built in since Server 2008) adds redundant paths and more throughput.
- **iSNS** (Internet Storage Name Service): automatic **discovery and management** of iSCSI devices — name service, discovery domains/login control, state-change notification, database mapping. Installed via Server Manager or PowerShell.
- Considerations before deploying: network speed, high availability, security, staff skills, vendor support.

---

## 4. Storage pools and Storage Spaces

**Concept (slide 33, `Storage Pool.pdf`):**

```
Physical disks (any size/type: SAS, SATA, SCSI, NVMe, USB — "JBOD")
   └─► Storage POOL       — aggregates disks into one manageable unit
         └─► Virtual disk  = "storage space"  — choose layout, provisioning, size
               └─► Volume  — formatted (NTFS/ReFS), used like any disk
```

- Benefits: **storage aggregation**, **elastic capacity** (add disks later as needs grow), **delegated administration**.
- When creating a virtual disk you choose: **resiliency type** (simple, mirror, parity), **provisioning type** (**thin** = grows on demand, or **fixed** = reserved up front), and **size**.
- Disks must be **blank and unformatted** — no existing volumes.
- In virtualization environments, pools let a Hyper-V host or an **iSCSI Target Server** carve out VHDX-backed space from cheap disks with RAID-like protection, without a hardware RAID controller.

---

## 5. Storage layout and disk requirements

### Storage Spaces layouts (slides 34–35) — **memorise the minimums**

| Layout | RAID analogue | Copies / protection | **Min disks** |
|---|---|---|---|
| **Simple** | RAID 0 | One copy, **no resiliency** | **1** |
| **Two-way mirror** | RAID 1 | 2 copies, survives **1** failure | **2** |
| **Parity** | RAID 5 | Data + parity, survives **1** failure | **3** |
| **Three-way mirror** | — | 3 copies, survives **2 simultaneous** failures | **5** |
| **Dual parity** | (RAID 6-like) | Survives **2** failures | **7** |

Creating a pool itself needs only **1** physical disk. Only **three** layouts give real fault tolerance (simple doesn't).

### Hardware RAID minimums (quick recall)

| RAID 0 | RAID 1 | RAID 5 | RAID 10 |
|---|---|---|---|
| **2** | **2** | **3** | **4** |

### Other planning choices (slides 2–8)

| Decision | Rule from the slides |
|---|---|
| **Partition table** | **MBR**: ≤ 2 TB, max 4 primary partitions, single point of failure. **GPT**: up to **128** partitions, up to **18 EB**. *MBR < 2 TB, GPT > 2 TB* |
| **Disk type** | **Basic** (default, simple volumes only) vs **Dynamic** (simple, spanned, striped, mirrored; changes without reboot) |
| **File system** | **FAT/FAT32/exFAT** (basic, flash). **NTFS** (ACLs, encryption, journaling, auditing). **ReFS** (checksums/integrity streams, huge volumes, **storage pooling**, disk scrubbing, corruption resiliency) |
| **Drive type** | Performance and cost rise together: EIDE → SATA (~150 IOPS) → SCSI (~210 IOPS) → SAS → **SSD** (~1.5 M IOPS) |

```powershell
fsutil fsinfo volumeinfo c:                     # file system + supported features (NTFS: ACLs, EFS, quotas…)
fsutil fsinfo sectorinfo c:                     # sector size and alignment
Format-Volume -DriveLetter E -FileSystem ReFS   # format a volume as ReFS (slide 7)
```

**Matching storage to workloads** (slide 29 scenarios): transactional databases and Exchange → **SAN/block**; user home folders and branch shares → **NAS/file**; VM storage → SAN or a resilient storage pool; tiered app storage → mix.

---

## Module Tour

| Where | What to look at |
|---|---|
| `Midterm.pdf` **p.2** headings 2–5 | The tested wording |
| `ACIT3420 Server Storage.pdf` slides 2–8 | Basic/dynamic disks, volume types, MBR vs GPT, FAT/NTFS/ReFS, `fsutil`, disk types |
| **slides 9–14** | **RAID overview and the RAID 0 / 1 / 5 / 6 / 1+0 diagrams** (image-only slides — open the PDF) |
| **slides 15–29** | **DAS, NAS, SAN**, Fibre Channel, FCoE, comparison, block vs file, scenarios |
| **slides 30–32, 36–39** | **iSCSI** SAN, Target Server, Initiator, considerations, iSNS, MPIO |
| **slides 33–35** | **Storage pools**, minimum disks, **Storage Spaces layouts** |
| `Storage Pool.pdf` | Pool → virtual disk → volume; resiliency + thin/fixed provisioning |
| `How to identify the iSCSI software initiator node name.pdf` p.1 | IQN format and where to find it in Windows |
| `Block Level Storage vs File Level Storage.pdf` pp.1–2 | Block vs file use cases |
| SAN intro video (5 min) | DAS → NAS → FC → FCoE → iSCSI, with the cost/performance trade-offs |

## Practical Takeaways

- **RAID protects against disk failure, not deletion or corruption.** You still need backups — the slides say it outright.
- **Minimum-disk questions are free marks.** RAID 0/1/5/10 = 2/2/3/4. Storage Spaces simple/2-way/parity/3-way/dual parity = 1/2/3/5/7.
- **Block vs file decides the platform.** If the app (SQL, Exchange, VM hosts) needs a "real disk", it's SAN/iSCSI. If users need a share, NAS/SMB is cheaper and simpler.
- **iSCSI without MPIO is a single point of failure.** One switch outage takes every server's disk offline.

---

## Knowledge Check: Week 4

**1. (Multiple choice)** Which storage solution provides **block-level** access to **centralized** storage that multiple servers can use at once?
- A) DAS
- B) NAS
- C) SAN
- D) A spanned volume

**2. (Multiple choice)** Which RAID level stripes data with **parity distributed across all disks** and requires a minimum of **three** disks?
- A) RAID 0
- B) RAID 1
- C) RAID 5
- D) RAID 10

**3. (Fill in the blank)** iSCSI communicates over TCP port `______`. The component that runs on the storage device is the iSCSI ______, and the client side is the iSCSI ______. Both are identified by an ______ such as `iqn.1991-05.com.microsoft:example`.

**4. (What does it handle?)** In a Storage Spaces virtual disk wizard you choose **Three-way mirror** with **thin** provisioning. What do those two settings mean, and what's the minimum number of physical disks?

**5. (Scenario)** A small company wants shared, fault-tolerant **block-level** storage for two Hyper-V hosts, but can't afford Fibre Channel. They have a Windows Server with five blank SATA disks. Using only the guide, which technologies would you combine, what layout would you choose to survive **two** simultaneous disk failures, and what would you add so a single switch failure doesn't take the storage offline?

<details>
<summary><b>Answer key with explanations (click to expand)</b></summary>

1. **C, SAN.** It presents LUNs to servers as if locally attached (block-level) and is shared. **DAS** is block-level but isolated to one server; **NAS** is shared but **file-level**.
2. **C, RAID 5.** RAID 0 has no parity (2 disks), RAID 1 is mirroring (2 disks), RAID 10 is mirrored pairs striped (4 disks).
3. **3260**, **target**, **initiator**, **IQN** (iSCSI Qualified Name).
4. **Three-way mirror** keeps **three copies** of the data and survives **two simultaneous** disk failures. **Thin** provisioning means space is allocated from the pool **as it's used** rather than reserved up front (fixed). Minimum **5** physical disks.
5. Put the five disks in a **storage pool**, create a **three-way mirror** virtual disk (needs exactly the 5 disks it has, survives 2 failures), and publish it to the hosts with the **iSCSI Target Server** role — iSCSI gives block-level SAN access over ordinary **Ethernet/TCP/IP** at much lower cost than Fibre Channel. Connect each host with the built-in **iSCSI Initiator**, and add **MPIO** with redundant network paths so one switch or NIC failure doesn't cut off the storage.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What is the **minimum number of disks** for **RAID 10**?

- A) 2
- B) 4
- C) 3
- D) 5

**2.** Which RAID level provides **no fault tolerance**, so losing one disk loses everything?

- A) RAID 1
- B) RAID 5
- C) RAID 10
- D) RAID 0

**3.** Which protocols does a **NAS** use to provide shared folders?

- A) SMB/CIFS and NFS over Ethernet
- B) Fibre Channel and FCoE
- C) iSCSI only
- D) SAS and SATA cabled directly to the server

**4.** What is the minimum number of physical disks for a **dual parity** Storage Spaces virtual disk?

- A) 3
- B) 5
- C) 7
- D) 4

**5.** What is an **IQN**?

- A) The IP address of the iSCSI target
- B) The World Wide Name of a Fibre Channel node
- C) The number of a LUN on a SAN
- D) A globally unique logical name for an iSCSI initiator or target, not tied to an IP address

**6.** Which command shows the **file system and supported features** (ACLs, EFS, quotas) of drive C:?

- A) `fsutil fsinfo volumeinfo c:`
- B) `fsutil fsinfo sectorinfo c:`
- C) `Format-Volume -DriveLetter C -FileSystem ReFS`
- D) `systeminfo.exe`

**7.** You are initializing a new **4 TB** data disk and want a single partition that uses the whole disk. Which partition table do you choose?

- A) MBR
- B) GPT
- C) Dynamic spanned
- D) FAT32

**8.** Where in Windows Server do you configure the **iSCSI initiator** and find its IQN?

- A) Server Manager → Add Roles and Features → iSCSI Target Server
- B) Disk Management → New Spanned Volume
- C) Server Manager → Tools → iSCSI Initiator → Configuration
- D) The iSNS server console

**9.** Which Windows **dynamic volume** type is the equivalent of **RAID 1**?

- A) Mirrored
- B) Striped
- C) Spanned
- D) Simple

**10.** Which file system offers **checksums/integrity streams**, **storage pooling** and **disk scrubbing**?

- A) FAT32
- B) exFAT
- C) NTFS
- D) ReFS

**11.** A consultant proposes storing the company's **Exchange** databases on a NAS share. Why does the guide say this is a poor choice?

- A) NAS is block-level storage and costs more than a SAN.
- B) NAS is file-level and slower, and isn't suitable for Exchange or SQL, which need block-level storage.
- C) A NAS can only be used by one server at a time.
- D) A NAS requires Fibre Channel HBAs in every server.

**12.** A **RAID 5** array has four disks. One disk fails, and a **second disk fails** while the array is rebuilding. What happens?

- A) The array keeps running because parity covers two failures.
- B) The array keeps running in degraded mode with no data loss.
- C) Data is lost, because RAID 5 survives only one disk failure.
- D) The array automatically converts itself to RAID 1.

**13.** A small office has **one server** that needs more disk capacity. They want the **cheapest, easiest** option with no extra switches, managed in Disk Management. Which solution fits?

- A) A Fibre Channel SAN
- B) A NAS
- C) An iSCSI SAN with MPIO
- D) DAS

**14.** Three servers connect to an iSCSI target through a **single switch**. The switch fails and **every server loses its disk**. What should have been deployed to prevent this?

- A) **MPIO** with redundant network paths
- B) An **iSNS** server
- C) **CHAP** authentication on the target
- D) **Thin** provisioning on the virtual disk

**15.** When creating a new storage pool, one physical disk can't be added. It still holds an **NTFS volume** with old data on it. Why?

- A) A pool needs at least three disks before any can be added.
- B) Disks added to a pool must be blank and unformatted, with no existing volumes.
- C) Storage pools don't support SATA disks.
- D) All disks in a pool must be the same size.

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** RAID 10 mirrors pairs and then stripes them, so it needs **4** disks. 2 is the minimum for RAID 0 and RAID 1, and 3 is RAID 5.
2. **D.** **RAID 0** is striping without parity or mirroring, so one failed disk loses the whole set. RAID 1, 5 and 10 all survive at least one failure.
3. **A.** NAS is file-level storage using **SMB/CIFS and NFS** over Ethernet. Fibre Channel, FCoE and iSCSI are SAN transports, and SAS/SATA is DAS.
4. **C.** Dual parity needs **7** disks. 3 is parity, 5 is three-way mirror; memorise 1/2/3/5/7 for simple/two-way/parity/three-way/dual parity.
5. **D.** An IQN (iSCSI Qualified Name) is a globally unique **logical** name for initiators and targets, used to decide which initiator sees which LUN. It is not an IP address, and WWN is the Fibre Channel equivalent term.
6. **A.** `fsutil fsinfo volumeinfo` shows the file system and its features. `sectorinfo` shows sector size and alignment instead.
7. **B.** **GPT** is for disks over 2 TB (up to 128 partitions, 18 EB). MBR is limited to 2 TB. Spanned is a volume type and FAT32 is a file system, not partition tables.
8. **C.** The initiator is installed by default and configured at **Server Manager → Tools → iSCSI Initiator → Configuration**. The iSCSI Target Server role is the storage side, not the client.
9. **A.** **Mirrored** = RAID 1. Striped = RAID 0, and spanned has no RAID equivalent or redundancy.
10. **D.** **ReFS** adds checksums/integrity streams, storage pooling, disk scrubbing and corruption resiliency. NTFS is the tempting choice, but its listed features are ACLs, encryption, journaling and auditing.
11. **B.** NAS is file-level with slower access and is not suitable for SQL or Exchange; Exchange supports only block storage. A NAS is shared and relatively inexpensive, so A, C and D are false.
12. **C.** RAID 5 survives **one** failure; a second failure during the rebuild means data loss. Surviving two failures needs RAID 6 or dual parity.
13. **D.** **DAS** is the easiest to deploy, inexpensive (no switches or routers) and managed in Disk Management. Its drawback, isolation to one server, doesn't matter here. NAS and SAN add network devices and cost.
14. **A.** **MPIO** adds redundant paths so one NIC or switch failure doesn't cut off the storage. iSNS is the tempting distractor, but it handles discovery and management, not redundancy.
15. **B.** Pool disks must be **blank and unformatted**. A pool can be created from a single disk, accepts SATA and other types, and mixes disk sizes.

</details>
