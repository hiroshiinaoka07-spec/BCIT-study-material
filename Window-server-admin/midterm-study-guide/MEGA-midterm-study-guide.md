# ACIT 3420 — Midterm essentials

Only the bullets on [`../Midterm.pdf`](../Midterm.pdf), in the same order.

## 1. Active Directory Domain Services (ADDS)

**What is ADDS?** Active Directory Domain Services is a directory that stores identities (users, computers, groups), authenticates them with Kerberos, and authorizes what they can access.

**Why a network needs it.** One account works everywhere in the domain, administration (passwords, policy) is centralized, and every domain controller holds a copy so sign-in still works if one DC is down.

## 2. ADDS Database Partitions

The database file `ntds.dit` is split into four partitions.

**Schema** defines every object type and attribute, and it replicates to every DC in the forest.

**Configuration** holds the forest map (sites, services, which DCs exist), and it replicates to every DC in the forest.

**Domain** holds that domain’s users, computers, groups, and OUs, and it replicates only to DCs in that domain.

**Application** holds app data such as DNS zones, and it replicates only to the DCs you choose.

## 3. ADDS Physical and Logical Components

**Physical components** are the domain controllers, the sites they sit in, and the replication paths between them.

**Site** is a group of IP subnets linked at high speed, so clients use a nearby DC and replication follows the real network.

**Replication** inside a site is fast and uncompressed; between sites it is scheduled, compressed, and passes through one bridgehead DC per site, with the KCC building those connections automatically.

**OU** is a container inside a domain, used to delegate admin rights and link Group Policy.

**Domain** is the security and replication boundary that holds one shared directory of accounts.

**Tree** is domains that share one contiguous DNS name, such as `adatum.com` and `van.adatum.com`.

**Forest** is one or more trees that share one schema, one configuration, and one Global Catalog; the first domain is the forest root.

## 4. FSMO Roles (Flexible Single Master Operations)

**Definition.** Any writable DC can accept most changes, but five operations would conflict if two DCs did them at once, so each is assigned to exactly one DC.

**Schema Master** (one per forest) is the only DC that can change the schema.

**Domain Naming Master** (one per forest) is the only DC that can add or remove domains.

**PDC Emulator** (one per domain) is the time source and handles password changes and account lockouts.

**RID Master** (one per domain) gives each DC a pool of relative IDs so new objects get unique SIDs.

**Infrastructure Master** (one per domain) updates references to objects that live in other domains.

**How they are distributed.** A forest has those 2 forest roles plus the 3 domain roles in every domain, and by default they start on the first DC.

## 5. Global Catalog (GC)

The Global Catalog keeps a full copy of its own domain plus a partial copy of every object in the other domains, so one search can find an account anywhere in the forest and a logon can check Universal group membership.

## 6. IGDLA Model

Put each person in a Global group (who they are, members from that domain only), put that Global group in a Domain Local group on the resource (what they can use, in that resource’s domain), and grant the permission to the Domain Local group, so adding or removing someone is one membership change.

## 7. Hyper-V and Hypervisors

**What is Hyper-V?** Hyper-V is Windows Server’s hypervisor: software that sits on the hardware and runs many virtual machines on one physical server.

**Type 1 (bare-metal)** runs directly on the hardware, so it is fast and is used for production servers (Hyper-V, VMware ESXi).

**Type 2 (hosted)** runs as an application on a normal operating system, so it is easy to install on a PC and is used for labs and testing (VMware Workstation, VirtualBox).

## 8. Hyper-V Virtual Switches

**External** lets VMs talk to each other, to the host, and to the physical network, and it needs a physical NIC; use it when users must reach the VM.

**Internal** lets VMs talk to each other and to the host, and it stays off the physical network; use it when the host must manage the VMs.

**Private** lets only the VMs on that host talk to each other; use it for a fully isolated lab.

## 9. Checkpoints in Hyper-V

A checkpoint is a point-in-time snapshot of a VM that you roll back to.

**Usage.** Take one before a change such as an update or a new install, and delete it after the change checks out; deleting merges the checkpoint back into the VM’s disk.

**Standard** (the default) saves the disk and the memory, so the VM returns still running, with open apps as they were.

**Production** saves the disk through VSS, so the VM returns as if it had been shut down cleanly.

## 10. iSCSI Storage Server and Storage Pool

**iSCSI** carries SCSI disk commands over TCP/IP so a server gets block-level disks across a normal Ethernet network, which is how a lower-cost SAN is built; the storage side is the target and the server side is the initiator.

**Storage pool** groups many physical disks into one unit, then you create a virtual disk (a resiliency layout, thin or fixed) and a volume on top of it; in virtualization you add disks as you grow and give VMs space that is consumed only as they use it, with mirror or parity protection and no hardware RAID card.

## 11. RAID (Redundant Array of Independent Disks)

**RAID 0** stripes data across at least 2 disks for the fastest reads and writes and keeps all of the space, and losing one disk loses everything.

**RAID 1** writes the same data to at least 2 disks so one disk can fail, and only half of the raw space is usable.

**RAID 5** stripes data plus parity across at least 3 disks, survives one disk failure, and keeps the space of all but one disk; parity math slows writes.

**RAID 10** mirrors disks in pairs and then stripes those pairs, needs at least 4 disks, survives one failure in each pair, keeps half the space, and gives both speed and redundancy at the highest cost per usable gigabyte.

## 12. Enterprise Storage Solutions (DAS, NAS, SAN)

**DAS** is disks inside one server or cabled only to it, block-level, cheap and simple, and that one server is the only machine that can use them.

**NAS** is shared folders on the network (SMB or NFS), easy for many users to share files, and too slow for databases such as SQL or Exchange.

**SAN** is a storage network that many servers see as local block disks (LUNs) over Fibre Channel or iSCSI, the fastest and most redundant option, and the most expensive to buy and run.

## 13. Storage Layout and Disk Requirements

**Planning.** Choose speed with no protection, a mirror when a copy matters more than space, or parity when you want a balance of space and protection, then put a volume on that layout.

**RAID minimum disks.** RAID 0 needs 2, RAID 1 needs 2, RAID 5 needs 3, and RAID 10 needs 4.

**Storage Spaces minimum disks.** Simple needs 1, two-way mirror needs 2, parity needs 3, three-way mirror needs 5, and dual parity needs 7.

## 14. Security Identifier (SID)

**What is a SID?** A Security Identifier is the unique ID Windows gives every user, computer, and security group, and access checks use that ID.

**Why it matters.** Permissions stay with the SID, so renaming an account keeps its access, deleting it and creating the same name does not, and the RID Master exists so two DCs never issue the same SID.
