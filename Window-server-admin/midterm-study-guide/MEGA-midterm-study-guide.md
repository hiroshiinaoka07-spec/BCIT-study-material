# ACIT 3420 — Midterm essentials

Every bullet from [`../Midterm.pdf`](../Midterm.pdf), in the same order, with the facts that bullet asks for.

## Active Directory Domain Services (ADDS)

**What is ADDS?** Active Directory Domain Services is a directory database of objects (users, computers, groups) and their attributes. It stores identities, authenticates them with Kerberos on a domain controller, and authorizes access from group membership and permissions.

**Why a network needs domain services.** Without a domain, every server keeps its own local accounts. With AD DS, one account works at any DC in the domain, password policy and Group Policy are set in one place, and every DC holds a synchronized copy. AD is multi-master: you can write changes on any writable DC.

## ADDS Database Partitions

The database is one file, `ntds.dit`, split into four partitions. The exam fact is what each holds and who receives a copy.

**Schema** defines every object class and attribute, and it replicates to every DC in the forest.

**Configuration** holds the forest topology (sites, services, which DCs exist), and it replicates to every DC in the forest.

**Domain** holds that domain’s users, computers, groups, and OUs, and it replicates only to DCs in that domain.

**Application** holds app data such as DNS zones, and it replicates only to the DCs you choose.

## ADDS Physical and Logical Components

**Physical components.** A domain controller hosts the database and Kerberos. A site is a group of IP subnets linked at high speed. A bridgehead is the DC in a site that replicates with other sites. Site links and connection objects are the paths that replication uses.

**Sites.** A site follows the physical network, not the org chart: one site can hold several domains, and one domain can span several sites. Clients log on to a DC in their own site.

**Replication topology.** Inside a site, replication is frequent and uncompressed, DC to DC. Between sites it runs on a schedule, is compressed, and passes through bridgehead servers. The KCC builds those connections automatically and recalculates them every 15 minutes.

**Organizational unit (OU).** An OU is a container inside a domain, used to delegate admin rights and to link Group Policy.

**Domain.** A domain is an administration, security, and replication boundary with its own directory of accounts. A child domain does not inherit the parent’s permissions or policies.

**Tree.** A tree is domains that share one contiguous DNS namespace, such as `adatum.com` and `van.adatum.com`.

**Forest.** A forest is one or more trees that share one schema, one configuration partition, and one Global Catalog. The first domain is the forest root. Trusts between parent and child, and between trees in the forest, are automatic, two-way, and transitive.

## FSMO Roles (Flexible Single Master Operations)

**Definition.** Most AD writes can happen on any DC, but five operations would conflict if two DCs did them at once, so each is owned by exactly one DC.

**Schema Master** (one per forest) is the only DC that can change the schema.

**Domain Naming Master** (one per forest) is the only DC that can add or remove domains.

**PDC Emulator** (one per domain) is the time source and handles password changes, account lockouts, and Group Policy edits.

**RID Master** (one per domain) hands each DC a pool of relative IDs. An object’s SID is the domain SID plus a RID from that pool.

**Infrastructure Master** (one per domain) updates references to objects that live in another domain, such as a group member from that domain.

**How they are distributed.** Every forest has the 2 forest roles, and every domain has the 3 domain roles, so 3 domains means 2 + 9 = 11 role holders. By default the first DC in the forest holds all five, and the first DC of each new domain holds that domain’s three. Move a role with a transfer while the old holder is online; seize it with `ntdsutil` only when that DC is dead.

## Global Catalog (GC)

**Searches across domains.** A GC holds a full copy of its own domain plus a partial copy of every object in every other domain, so you can find an account anywhere in the forest without querying every domain. It answers on port 3268 (normal LDAP is 389).

**Logons across domains.** At logon the DC must read Universal group membership, and that membership is stored in the GC. A site with no reachable GC can fail logons. Making every DC a GC removes that dependency and costs more replication and disk space.

## IGDLA Model

**Identity → Global group → Domain Local group → Access.** Put users in a Global group that names the role (who). Put that Global group into a Domain Local group that names the resource (what). Grant the permission on the share, NTFS folder, or printer to the Domain Local group.

**Why it scales.** A new person is added to one Global group and inherits every resource that group already reaches. Removing that one Global group from a Domain Local group removes the whole team from that resource, with no edit to the ACL.

**Scopes that make the chain work.** A Global group holds members from its own domain only and can be granted access in any domain. A Domain Local group can hold Global groups from any domain and can be granted access only in its own domain. A Domain Local group cannot be placed inside a Global group.

## Hyper-V and Hypervisors

**What is Hyper-V?** Hyper-V is Windows Server’s hardware virtualization role. The hypervisor sits between the hardware and the operating systems and controls access to that hardware, so one physical server runs many virtual machines.

**Type 1 (bare-metal)** runs directly on the hardware. It has the least overhead and the strongest isolation, so it is used for production servers and data centers. Hyper-V and VMware ESXi are Type 1.

**Type 2 (hosted)** runs as an application on a normal operating system. The extra OS layer costs performance, and it is used on desktops for labs and testing because it needs no dedicated server. VMware Workstation and VirtualBox are Type 2.

## Hyper-V Virtual Switches

**External** connects VMs to each other, to the host, and to the physical network. It must bind to a physical NIC. Use it when people on the real network must reach the VM.

**Internal** connects VMs to each other and to the host, and it has no path to the physical network. Use it when the host must manage or test the VMs and those VMs must stay off the LAN.

**Private** connects only the VMs on that host, not the host and not the physical network. Use it for a fully isolated lab.

## Checkpoints in Hyper-V

**Definition.** A checkpoint (Hyper-V’s name for a snapshot) is a saved point in time for a VM that you can roll back to. It creates a differencing disk, `.avhdx`, and new writes go there until you delete the checkpoint, which merges that disk back.

**Usage.** Take one before a Windows update, a new application, or removing a service, and delete it after the change checks out. It lives on the same storage as the VM, so it is a rollback tool; a backup is a separate copy stored elsewhere. Old checkpoints also slow the VM and fill the volume.

**Standard** (the default) saves the disk and the running memory, so a rollback returns the VM still running, including unsaved work in open apps. The slides call this application-consistent.

**Production** saves disk data through VSS inside the guest, so a rollback boots the VM as if it had been shut down, and unsaved work is gone. The slides call this data-consistent.

## iSCSI Storage Server and Storage Pool

**iSCSI protocol.** iSCSI carries SCSI commands inside TCP/IP on port 3260, so a server gets block-level disks over ordinary Ethernet. That is how a SAN is built without Fibre Channel. The storage device is the iSCSI target; the server is the iSCSI initiator. Each side is named by an IQN (`iqn.1991-05.com.microsoft:name`), and the target uses that name to decide which initiator may see which LUN.

**Role in enterprise storage.** One path makes the disk available; MPIO adds extra paths so a failed NIC or switch does not take the disk offline. iSNS is the directory that discovers and tracks iSCSI devices.

**Storage pools.** A pool groups physical disks of any type into one unit. From the pool you create a virtual disk (simple, mirror, or parity; thin or fixed) and then a volume. Disks in the pool must be blank. In virtualization this lets a Hyper-V host or an iSCSI target grow by adding disks, hand VMs space that is consumed only as they write, and get RAID-like protection without a hardware RAID controller.

## RAID (Redundant Array of Independent Disks)

RAID joins disks into one logical unit for speed (striping), fault tolerance (mirroring or parity), or both. It does not replace backups.

**RAID 0** stripes data across at least 2 disks, keeps 100% of the space, and is the fastest. It has no fault tolerance: one failed disk loses everything.

**RAID 1** writes the same data to at least 2 disks, survives one failure, and can use only 50% of the raw space. It is simple and fully redundant, and half the disks are copies.

**RAID 5** stripes data and distributed parity across at least 3 disks, survives one failure, and keeps the space of n − 1 disks. Writes are slower because of the parity math, and a second failure while a disk is rebuilding loses the data.

**RAID 10** mirrors disks in pairs, then stripes those pairs. It needs at least 4 disks, survives one failure in each pair, keeps 50% of the space, and gives striping speed plus mirror safety at the highest cost per usable gigabyte.

## Enterprise Storage Solutions

**DAS (Direct-Attached Storage)** is disks inside one server or cabled only to it (SATA, SAS, SCSI, USB). Access is block-level. It is the cheapest and easiest to run, and only that one server can use the disks, so it fits a single server on a small budget.

**NAS (Network-Attached Storage)** is a device on the LAN that shares folders over SMB/CIFS or NFS. Access is file-level: you open `\\server\share` and the device owns the file system. It is inexpensive shared storage for home folders and branch file shares, and it is too slow for SQL or Exchange.

**SAN (Storage Area Network)** is a storage network that many servers see as local disks, called LUNs, over Fibre Channel, FCoE, or iSCSI. Access is block-level: the server formats the LUN itself. It is the fastest, most expandable, and most redundant option, and it costs the most in hardware and skill. Use it for databases, Exchange, and storage shared by many servers.

**The difference that decides the choice.** Block storage (DAS and SAN) is a raw disk the server formats. File storage (NAS) is a share. Block is what databases and Exchange require; file is what you use when people only need a place to put files.

## Storage Layout and Disk Requirements

**Planning a configuration.** Use MBR at 2 TB or below (4 primary partitions); use GPT above 2 TB (up to 128 partitions). A basic disk holds simple volumes. A dynamic disk can be simple, spanned, striped (RAID 0), or mirrored (RAID 1). Format with NTFS for permissions and encryption, or ReFS when you want integrity checks and storage pools. Then pick a layout: striping for speed, a mirror when a second copy matters more than space, or parity for a balance of space and protection.

**RAID minimum disks.** RAID 0 needs 2, RAID 1 needs 2, RAID 5 needs 3, and RAID 10 needs 4.

**Storage Spaces minimum disks (enterprise layouts).** Simple needs 1 and has no protection. Two-way mirror needs 2 and survives 1 failure. Parity needs 3 and survives 1 failure. Three-way mirror needs 5 and survives 2 failures. Dual parity needs 7 and survives 2 failures.

## Security Identifier (SID)

**What is a SID?** A Security Identifier is the unique ID Windows assigns to every security principal: a user, a computer, or a security group. Access checks use the SID. A security group has a SID, so it can sit on an ACL; a distribution group has none, so it cannot be granted permissions. The value is the domain SID plus a RID from the RID Master.

**Why it matters.** Permissions are stored on the SID, so renaming an account keeps its access, and deleting an account then creating the same name does not, because the new account gets a new SID. Two objects must never share a SID, which is why only one DC per domain issues RIDs, and why a cloned Windows machine is generalized with Sysprep before it is copied.
