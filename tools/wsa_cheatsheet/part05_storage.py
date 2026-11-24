"""Part 5: IPv4/IPv6 (SG-22).  Part 6: Storage (SG-23 to SG-25)."""


def part5(s):
    s.part("PART 5 — IPv4 AND IPv6 ADDRESSING (SG-22)")
    s.src("IPv4 and IPv6 lecture slides (p1–p25); \"How to Configure Static IP Address on Windows Server 2022\" lab; \"How to Set an IPv4 Address with PowerShell\" lab; Week 7 discussion prompts.")

    s.h2("SG-22  IPv4 / IPv6; private vs public addresses")
    s.h3("IPv4 essentials")
    s.bullets([
        "**32-bit** address in dotted decimal (4 octets). Part of the address is the **network ID** (shared by everything on the subnet) and the rest is the **host ID** (unique per device). The **subnet mask** or **CIDR prefix** marks the boundary.",
        "**Default gateway** = the router interface that connects the local subnet to other networks. Packets for remote subnets go to it.",
        "**Subnetting** \"steals\" host bits to make more, smaller networks (e.g. one Class B with more than 65,000 hosts split into 254 subnets of 254 hosts each).",
        "**CIDR** (Classless Inter-Domain Routing) replaced wasteful classes with any prefix length (`/26`) and enables **route summarization (supernetting)**.",
        "**NAT** (with masquerading) hides a whole private address space behind one public IP and slowed IPv4 exhaustion.",
    ])
    s.table(["Class", "First octet", "Default mask", "Private range (RFC 1918)"], [
        ["A", "1–126", "255.0.0.0 (/8)", "**10.0.0.0 – 10.255.255.255** (10.0.0.0/8)"],
        ["B", "128–191", "255.255.0.0 (/16)", "**172.16.0.0 – 172.31.255.255** (172.16.0.0/12)"],
        ["C", "192–223", "255.255.255.0 (/24)", "**192.168.0.0 – 192.168.255.255** (192.168.0.0/16)"],
        ["D / E", "224–239 / 240–255", "—", "Multicast / experimental"],
        ["Special", "127.0.0.0/8", "—", "**Loopback** (127.0.0.1); **169.254.0.0/16 = APIPA** (no DHCP server answered); 0.0.0.0 = this host / default route"],
    ], widths=(0.8, 1.4, 1.6, 3.7))
    s.p("**Private IPs** (RFC 1918) are free to use inside any organization, **aren't routed on the Internet**, and need NAT to get out (the lab uses 192.168.239.0/24 and 172.16.x.0/24). **Public IPs** are globally unique, assigned by an ISP or registry (ARIN), and Internet-routable (e.g. the DMZ in the course topology uses 133.12.10.x).")
    s.h3("Subnetting quick math")
    s.table(["Prefix", "Mask", "Block size", "Usable hosts", "Prefix", "Mask", "Block size", "Usable hosts"], [
        ["/24", "255.255.255.0", "256", "254", "/28", ".240", "16", "14"],
        ["/25", ".128", "128", "126", "/29", ".248", "8", "6"],
        ["/26", ".192", "64", "62", "/30", ".252", "4", "2"],
        ["/27", ".224", "32", "30", "/16", "255.255.0.0", "65,536", "65,534"],
    ], widths=(0.6, 1.2, 0.9, 1.05, 0.6, 1.2, 0.9, 1.05), size=8)
    s.box("key", [
        "**Usable hosts = 2^(host bits) − 2** (network ID + broadcast). **Lab CIDR task: is 192.168.1.55/26 a usable host address?** /26 means blocks of 64: .0–.63, .64–.127, … 55 falls in **.0–.63**, so network = 192.168.1.0, broadcast = 192.168.1.63, usable range .1–.62. **Yes, .55 is a valid host.**",
    ])
    s.h3("IPv6 essentials")
    s.bullets([
        "**128-bit** address, 8 groups of 4 hex digits: `2001:0db8:0000:0000:0000:ff00:0042:8329` → `2001:db8::ff00:42:8329` (drop leading zeros; use `::` **once** for consecutive zero groups). Usually a /64 network prefix + 64-bit interface ID.",
        "**Benefits (slide p14):** a huge address space (every device can have a globally unique address, so no NAT is needed), **more efficient routing** (hierarchical, no router fragmentation, simpler header), **autoconfiguration**, **better security** (scanning a /64 is impractical; IPsec is built in).",
        "**No broadcast** in IPv6. ARP is replaced by Neighbor Discovery (ICMPv6).",
    ])
    s.table(["IPv6 address type", "Prefix / example", "IPv4 equivalent"], [
        ["**Unicast**: one-to-one", "—", "Unicast"],
        ["  Global unicast", "**2000::/3** (2001:…, 2600:…)", "Public address"],
        ["  Link-local", "**FE80::/10** (always FE80::/64 on a link); every IPv6 interface has one; **not routable**", "169.254.x.x (APIPA)"],
        ["  Unique local", "**FC00::/7** (in practice FD00::/8): private but unique, so merging networks causes no collisions", "RFC 1918 private (replaces the deprecated site-local FEC0::/10)"],
        ["  Loopback / unspecified", "**::1** / **::**", "127.0.0.1 / 0.0.0.0"],
        ["**Multicast**: one-to-many", "**FF00::/8** (FF02::1 all nodes, FF02::2 all routers)", "224.0.0.0/4 (also replaces broadcast)"],
        ["**Anycast**: one-to-nearest-of-many", "Same format as unicast, assigned to several interfaces; the nearest (fewest router hops) receives it", "Used for locating services or the nearest router"],
    ], widths=(2.0, 3.6, 1.9), first_col_bold=False)
    s.table(["Autoconfiguration (slide p17)", "How it works"], [
        ["**Stateless (SLAAC)**", "The host builds its address from the prefix in the router's **Router Advertisement** plus its own interface ID. Native IPv6, no server needed."],
        ["**Stateful (DHCPv6)**", "A DHCPv6 server assigns addresses and options (UDP 546/547)."],
        ["**Both**", "The RA supplies the prefix *and* tells hosts to use DHCPv6 for additional options (such as DNS)."],
    ], widths=(2.0, 5.5))
    s.table(["Transition technology", "What it does"], [
        ["**Dual stack**", "Run IPv4 and IPv6 side by side (Windows' default)."],
        ["**6to4**", "Puts IPv6 inside IPv4 across the IPv4 Internet with no explicit tunnel. The **IPv4 address is embedded** in the IPv6 prefix (2002:WWXX:YYZZ::/48). Needs a **public IPv4 address**. Both ends run IPv4 and IPv6; a router can do it for its clients."],
        ["**ISATAP**", "Intra-Site Automatic Tunnel Addressing Protocol: treats the IPv4 intranet as one IPv6 link. Interface ID = `::0:5EFE:w.x.y.z` (the IPv4 address) with a link-local (FE80::/64), site or global prefix."],
        ["**Teredo**", "IPv6 inside **UDP** (port 3544) for NAT traversal (NAT-T), so it **works behind one or more IPv4 NATs**. Prefix 2001::/32."],
    ], widths=(1.6, 5.9))
    s.h3("Configure a static IP (lab handouts)")
    s.p("**GUI:** Server Manager → Local Server → click the Ethernet link → adapter → Properties → **Internet Protocol Version 4 (TCP/IPv4)** → Use the following IP address / DNS server addresses. (Or `ncpa.cpl`.)")
    s.code("""Get-NetAdapter                                   # note the ifIndex / Name
Get-NetIPAddress -AddressFamily IPv4             # 169.254.x.x = APIPA (no DHCP answer)
New-NetIPAddress -InterfaceIndex 4 -IPAddress 192.168.239.20 -PrefixLength 24 -DefaultGateway 192.168.239.254
#   or -InterfaceAlias "Ethernet0"
Set-DnsClientServerAddress -InterfaceIndex 4 -ServerAddresses 192.168.239.1
Get-NetIPConfiguration                           # summary: IP, gateway, DNS
Remove-NetIPAddress -InterfaceIndex 4 -IPAddress 192.168.239.20 ; Remove-NetRoute -InterfaceIndex 4
Set-NetIPInterface -InterfaceIndex 4 -Dhcp Enabled ; Set-DnsClientServerAddress -InterfaceIndex 4 -ResetServerAddresses
Disable-NetAdapterBinding -Name Ethernet0 -ComponentID ms_tcpip6   # disable IPv6 (DNS lab removed IPv6)
netsh interface ipv4 set address "Ethernet0" static 192.168.239.20 255.255.255.0 192.168.239.254
ipconfig /all ;  ipconfig /release ; ipconfig /renew ; ping -6 ::1 ; tracert ; pathping ; Test-NetConnection 192.168.239.1 -Port 445""",
           title="PowerShell / netsh")
    s.box("trouble", [
        "- **169.254.x.x address:** no DHCP server reached (DHCP is down, the scope isn't activated or authorized, or there's no relay across routers). Check with `ipconfig /all`.",
        "- **`New-NetIPAddress` fails with \"Instance already exists\" / \"DefaultGateway already exists\":** remove the old IP and route first (`Remove-NetIPAddress`, `Remove-NetRoute`).",
        "- **IPv6 `::1`** in `nslookup` or `ping localhost` output is simply the IPv6 loopback, not an error.",
    ])
    s.h3("Week 7 discussion: model answers")
    s.tag("model")
    s.qa([
        ["IPv4 vs IPv6?", "32-bit vs 128-bit; dotted decimal vs hex; IPv4 has broadcast + ARP, IPv6 uses multicast + Neighbor Discovery; IPv4 uses DHCP or manual config, IPv6 has SLAAC/DHCPv6; IPv4 relies on NAT, IPv6 is end-to-end; IPv6 has a simpler fixed header, no router fragmentation and built-in IPsec support."],
        ["What is CIDR and what are its benefits?", "A prefix-length notation (`/n`) independent of classes. It allocates exactly the needed size (less waste), summarizes routes (smaller routing tables) and slowed IPv4 exhaustion."],
        ["Types of IPv6 addresses?", "Unicast (global, link-local, unique local, loopback), multicast and anycast. No broadcast."],
        ["Why IPv6?", "IPv4 is exhausted. IPv6 brings a huge address space, no NAT, autoconfiguration, better routing efficiency and security. It's needed for IoT and mobile growth and is already required by many ISPs and governments."],
    ], title=None)


def part6(s):
    s.part("PART 6 — SERVER STORAGE (SG-23 to SG-25)")
    s.src("Server Storage lecture slides (disks, file systems, RAID, DAS/NAS/SAN, FC, iSCSI, Storage Spaces, SMB/NFS); Storage Pool handout; Block vs File Level Storage article (TechRepublic); iSCSI IQN handout; CHAP handout; iSCSI / Storage Pool lab + videos (thin-provisioning demo); diskpart handout; Week 6 discussion prompts.")

    s.h3("Disks, partitions, volumes and file systems (foundation for SG-23 to SG-25)")
    s.table(["", "MBR (Master Boot Record)", "GPT (GUID Partition Table)"], [
        ["Partitions", "**4 primary**, or 3 primary + 1 extended (with logical drives)", "**128** partitions (Windows)"],
        ["Max disk size", "**2 TB**", "**18 EB** (effectively unlimited)"],
        ["Resilience", "One boot record, a **single point of failure**", "Primary + **backup** partition table, CRC protected"],
        ["Boot", "BIOS", "**UEFI** (needed for Gen 2 VMs and Secure Boot)"],
    ], widths=(1.3, 3.1, 3.1))
    s.table(["", "Basic disk", "Dynamic disk (legacy, deprecated)"], [
        ["Structure", "Partitions (primary, extended, logical)", "Volumes stored in an LDM database"],
        ["Volume types", "Simple partitions only", "**Simple, Spanned (up to 32 disks), Striped (RAID 0), Mirrored (RAID 1), RAID 5**"],
        ["Use today", "**Default and recommended**", "Replaced by **Storage Spaces**; converting back to basic requires deleting the volumes"],
    ], widths=(1.3, 3.1, 3.1))
    s.table(["File system", "Max file / volume", "Key features"], [
        ["FAT32", "4 GB file / 32 GB (Windows format limit; 2 TB in theory)", "Compatible with everything (USB, UEFI system partition); no security"],
        ["exFAT", "16 EB / 128 PB", "Flash drives and SD cards; large files; no ACLs or journaling"],
        ["**NTFS**", "16 TB to 8 PB (depends on cluster size)", "**ACL permissions, auditing, journaling (metadata log), EFS encryption, compression, quotas, BitLocker**, hard links, shadow copies; bootable"],
        ["**ReFS**", "35 PB in practice (2^78 bytes per slide)", "**Checksums / integrity streams, allocate-on-write, scrubbing, auto-repair with Storage Spaces mirror/parity**, block cloning, huge volumes. **No boot, EFS, quotas or compression.** Best for Hyper-V VHDX, S2D and backup targets"],
    ], widths=(1.0, 2.0, 4.5))
    s.code("""fsutil fsinfo volumeinfo c:      # file system name + supported features (ACLs, EFS, compression, USN journal)
fsutil fsinfo sectorinfo c:      # LogicalBytesPerSector 512, PhysicalBytesPerSector..., alignment, TRIM
fsutil fsinfo ntfsinfo c:        # bytes per cluster (allocation unit)
Format-Volume -DriveLetter E -FileSystem ReFS -NewFileSystemLabel Data   # slide p07""", title="Storage slide p07")
    s.table(["Disk type (slide p08)", "Performance", "Note"], [
        ["EIDE / PATA", "Slowest", "Legacy desktop"],
        ["SATA", "~150 IOPS", "Cheap capacity"],
        ["SCSI", "~210 IOPS", "Legacy server"],
        ["SAS", "Faster (10K/15K RPM)", "Enterprise, dual-ported"],
        ["SSD / NVMe", "Up to ~1.5 million IOPS", "Fastest and most expensive. **As performance goes up, so does cost.**"],
    ], widths=(2.0, 2.0, 3.5))

    # ---------------- SG-23 ----------------
    s.h2("SG-23  Storage pools; media types; parity vs two-way vs three-way mirror")
    s.p("**Storage Spaces** pools physical disks (JBOD, **without hardware RAID**) into a **storage pool**. From the pool you carve **virtual disks (storage spaces)** with a chosen **resiliency** and **provisioning** type, then create **volumes** on them. Tool: Server Manager → File and Storage Services → **Volumes → Storage Pools**. Unclaimed blank disks appear in the **Primordial** pool.")
    s.bullets([
        "**Disk requirements:** blank (**not initialized or partitioned**), at least 4 GB, bus type **SAS, SATA, SCSI, NVMe** (USB works on standalone servers but isn't recommended). **iSCSI and Fibre Channel LUNs and hardware-RAID volumes aren't supported** for pooling.",
        "**Media types:** HDD, SSD, SCM (storage-class memory) / NVMe, or Unspecified. Mixing SSD and HDD lets you build **storage tiers** (hot data on SSD) and an SSD **write-back cache**. Set it with `Set-PhysicalDisk -MediaType SSD`.",
        "**Drive allocation** for each disk when creating the pool: **Automatic**, **Manual** (used only when you pick it explicitly), or **Hot Spare** (stands by to replace a failed disk).",
        "**Enclosure awareness:** keeps the data copies in separate JBOD enclosures so a whole enclosure can fail (needs SES-capable enclosures).",
        "**Provisioning:** **Thin** (space is consumed only as data is written, so you can over-commit; demo: a 60 GB disk used only 7.56 MB) vs **Fixed** (all capacity is reserved immediately; better performance and needed for tiers).",
        "After pooling, **the disks disappear from Disk Management** because the pool owns them. The new *virtual disk* appears there instead, and you initialize and format it.",
    ])
    s.table(["Resiliency type", "Like RAID", "Copies / parity", "Min disks", "Tolerates", "Capacity efficiency", "Best for"], [
        ["**Simple**", "RAID 0", "Striped, no redundancy", "**1**", "0 failures", "100%", "Temp or scratch data, max speed"],
        ["**Two-way mirror**", "RAID 1 / 10", "2 copies", "**2**", "1 disk", "50%", "General purpose, VMs"],
        ["**Three-way mirror**", "—", "3 copies", "**5**", "**2 disks**", "33%", "Critical data, highest performance + resilience"],
        ["**Parity (single)**", "RAID 5", "Data + parity, striped", "**3**", "1 disk", "(n−1)/n, e.g. 67% with 3", "Archives, backups, sequential I/O (slow random writes)"],
        ["**Dual parity**", "RAID 6", "Data + 2 parity", "**7**", "2 disks", "≈ (n−2)/n", "Large archival volumes"],
    ], widths=(1.15, 0.7, 1.25, 0.65, 0.8, 1.25, 1.7), size=8)
    s.box("trap", [
        "- **Two-way mirror needs 2 disks, but a three-way mirror needs 5** in a standalone Storage Spaces pool (not 3). **Parity needs 3, dual parity needs 7.** These numbers come straight from the lecture.",
        "- \"Mirror\" in Storage Spaces = copies of data; \"Parity\" = calculated recovery information. Mirror is faster; parity is more space-efficient.",
    ])
    s.h3("Storage pool lab: steps (CA-VAN-SVR7, 5 × 10 GB SCSI disks)")
    s.steps([
        "Add 5 new SCSI virtual disks of 10 GB to Svr7 in VMware. **Don't bring them online or initialize them** (they must be blank to show in Primordial).",
        "Server Manager → File and Storage Services → Storage Pools → **Primordial** → TASKS → **New Storage Pool** → name `Pool1` → tick the disks → Allocation **Automatic** (or set one as **Hot Spare**).",
        "**New Virtual Disk** → pool → name → (enclosure awareness) → layout **Mirror** → **Three-way mirror** (needs 5 disks) → provisioning **Thin** or **Fixed** → size.",
        "**New Volume** wizard → drive letter → file system **ReFS** or **NTFS** → label.",
    ])
    s.code("""Get-PhysicalDisk -CanPool $true
New-StoragePool -FriendlyName Pool1 -StorageSubSystemFriendlyName "Windows Storage*" -PhysicalDisks (Get-PhysicalDisk -CanPool $true)
New-VirtualDisk -StoragePoolFriendlyName Pool1 -FriendlyName VD1 -ResiliencySettingName Mirror -NumberOfDataCopies 3 -ProvisioningType Thin -Size 20GB
#   Parity:  -ResiliencySettingName Parity     Dual parity: -ResiliencySettingName Parity -PhysicalDiskRedundancy 2
Get-VirtualDisk VD1 | Get-Disk | Initialize-Disk -PartitionStyle GPT -PassThru |
  New-Partition -AssignDriveLetter -UseMaximumSize | Format-Volume -FileSystem ReFS -NewFileSystemLabel Data
Set-PhysicalDisk -FriendlyName PhysicalDisk5 -Usage HotSpare
Get-StoragePool ; Get-VirtualDisk ; Repair-VirtualDisk VD1 ; Get-StorageJob""", title="Storage Spaces in PowerShell")
    s.tag("extra", "PowerShell equivalents of the lab GUI steps.")
    s.qa([
        ["Minimum disks for a parity virtual disk?", "**3**."],
        ["Define simple, mirror and parity.", "Simple = striping with no redundancy. Mirror = 2 or 3 full copies on different disks. Parity = data striped with parity information so one (or two, for dual parity) disk can fail."],
        ["Why didn't the new disks appear in Primordial?", "They were initialized or partitioned (or under 4 GB). Clean them (`Clear-Disk` or diskpart `clean`) so they're blank."],
        ["Why did the disks vanish from Disk Management?", "The storage pool claimed them. Windows now shows only the virtual disk created from the pool."],
        ["Thin vs fixed provisioning?", "Thin allocates on write (efficient, can over-commit, so monitor free pool space). Fixed reserves everything now (predictable, needed for tiering)."],
        ["What is a hot spare?", "A pool disk held in reserve that Storage Spaces uses automatically to rebuild after a disk fails."],
    ], title="Storage pool lab: Questions & Answers")

    # ---------------- SG-24 ----------------
    s.h2("SG-24  Block-level vs file-level storage (DAS / NAS / SAN)")
    s.table(["", "Block-level storage", "File-level storage"], [
        ["Presented as", "Raw volumes or **LUNs**; the server sees a local disk, formats it with its own file system (NTFS/ReFS/VMFS) and manages files itself", "A **share** of files and folders; the storage device owns the file system"],
        ["Protocols", "**iSCSI** (TCP 3260), **Fibre Channel**, FCoE, SAS", "**SMB/CIFS** (TCP 445), **NFS** (2049)"],
        ["Typical device", "**SAN**, iSCSI target, DAS", "**NAS**, Windows file server"],
        ["Use cases (article)", "**Databases** (SQL, especially clustered), **Exchange** (supports only block-level storage), **VMware VMFS / Hyper-V CSV**, **boot from SAN**", "File shares, home folders, archives, backups, media, \"a place to dump raw files\""],
        ["Pros", "Fast, flexible, low latency; any OS or file system; can boot servers", "**Simple, cheaper**, easy to share among many users, permissions managed by the NAS"],
        ["Cons", "**More complex to manage**: allocate storage per server, manage RAID protection, track performance, run the iSCSI/FC network", "Slower for random I/O; not supported for SQL or Exchange databases"],
        ["Backup", "Looks like a local disk, so OS-native or 3rd-party tools (DPM) work normally", "Share-level backup or NAS snapshots"],
    ], widths=(1.2, 3.2, 3.1), size=8)
    s.table(["Architecture", "What it is", "Pros", "Cons"], [
        ["**DAS** (Direct-Attached)", "Disks inside or cabled directly to one server (SATA/SAS/USB)", "Easy, cheap, fast", "**Isolated**: can't be shared, so capacity is stranded; one server = a single point of failure"],
        ["**NAS** (Network-Attached)", "A file-level appliance on the LAN (SMB/NFS/CIFS)", "Simple, shareable, inexpensive", "Slower (uses LAN bandwidth); not for SQL or Exchange"],
        ["**SAN** (Storage Area Network)", "A dedicated network of block storage (FC or iSCSI) presenting **LUNs**", "High performance and availability, clustering, centralized", "**Expensive**, complex, needs specialized skills"],
        ["**S2D** (Storage Spaces Direct)", "Hyper-converged: the local disks of 2–16 cluster nodes pooled over the network (Datacenter edition)", "No SAN needed, scales out", "Needs Datacenter, RDMA NICs and certified hardware"],
    ], widths=(1.4, 2.3, 1.8, 2.0), size=8)
    s.h3("Fibre Channel and iSCSI")
    s.table(["Fibre Channel term", "Meaning"], [
        ["Node / port", "Any FC device (server HBA, storage port)"],
        ["**WWN** (World Wide Name)", "A 64-bit unique ID for an FC node or port, like a MAC address"],
        ["**HBA**", "Host Bus Adapter, the FC card in the server"],
        ["Fabric", "The FC switch network"],
        ["Topologies", "**Point-to-point** (2 devices), **Arbitrated loop** (FC-AL ring, up to 126 devices, shared bandwidth), **Switched fabric** (FC switches; most common and scalable)"],
        ["**FCoE**", "Fibre Channel over (lossless, DCB) Ethernet, so the LAN and SAN share one converged network"],
        ["Speeds", "8 / 16 / **32** / 64 Gbps"],
    ], widths=(2.0, 5.5))
    s.table(["iSCSI term", "Meaning"], [
        ["**iSCSI**", "SCSI commands carried over **TCP/IP, port 3260**: block storage over the ordinary Ethernet network (a cheap SAN)"],
        ["**Target**", "The storage side that **offers** LUNs (Windows: **iSCSI Target Server** role service, backed by VHDX files)"],
        ["**Initiator**", "The client side that **connects** to the target and uses the LUN as a local disk (built-in *iSCSI Initiator*, `iscsicpl.exe`)"],
        ["**IQN**", "iSCSI Qualified Name: `iqn.yyyy-mm.reverse-domain:unique-name`, e.g. `iqn.1991-05.com.microsoft:ca-van-client1.adatum.com`. Find it under iSCSI Initiator → **Configuration** tab (Linux: `cat /etc/iscsi/initiatorname.iscsi`)"],
        ["**CHAP / Mutual CHAP**", "Authentication with a shared secret (12–16 characters). CHAP = the target authenticates the initiator. **Mutual (reverse) CHAP = both authenticate each other (more secure)**. Set the initiator secret on the Configuration tab"],
        ["**iSNS**", "Internet Storage Name Service: a DNS-like discovery and registration service for iSCSI targets and initiators"],
        ["**MPIO vs MCS**", "Multipath I/O (several network paths, failover and load balance, works for FC too) vs Multiple Connections per Session (iSCSI-only). Use MPIO for redundancy"],
        ["Other target features", "Diskless network boot of many servers from differencing VHDs, CHAP, VHDX-based LUNs, clustering"],
    ], widths=(1.6, 5.9))
    s.h3("iSCSI lab: steps")
    s.steps([
        "On Svr7: Add Roles → File and Storage Services → File and iSCSI Services → **iSCSI Target Server** (+ *iSCSI Target Storage Provider (VDS and VSS hardware providers)*).",
        "File and Storage Services → **iSCSI** → TASKS → **New iSCSI Virtual Disk** → location (volume) → name → size (fixed or dynamic VHDX) → **New iSCSI target** → name → **Access servers**: add the initiator by **IQN**, DNS name, IP or MAC (Client1 = 192.168.239.20) → (optional) **CHAP / reverse CHAP** → Create.",
        "On Client1: open **iSCSI Initiator** (say Yes to start the MSiSCSI service) → Targets → **Quick Connect** to the target IP (192.168.239.7) → Connected.",
        "Disk Management on Client1 → new disk → **Online → Initialize (GPT) → New Simple Volume → format**. It now behaves like a local disk.",
    ])
    s.code("""Install-WindowsFeature FS-iSCSITarget-Server -IncludeManagementTools
New-IscsiVirtualDisk -Path E:\\iSCSIVirtualDisks\\LUN1.vhdx -SizeBytes 10GB
New-IscsiServerTarget -TargetName Target1 -InitiatorIds "IQN:iqn.1991-05.com.microsoft:ca-van-client1.adatum.com"
Add-IscsiVirtualDiskTargetMapping -TargetName Target1 -Path E:\\iSCSIVirtualDisks\\LUN1.vhdx
# --- initiator ---
Start-Service MSiSCSI ; Set-Service MSiSCSI -StartupType Automatic
New-IscsiTargetPortal -TargetPortalAddress 192.168.239.7
Get-IscsiTarget | Connect-IscsiTarget -IsPersistent $true      # add -AuthenticationType ONEWAYCHAP -ChapSecret ...
Get-Disk | Where PartitionStyle -eq RAW | Initialize-Disk -PartitionStyle GPT -PassThru | New-Partition -UseMaximumSize -AssignDriveLetter | Format-Volume""",
           title="iSCSI in PowerShell")
    s.tag("extra", "PowerShell equivalents.")
    s.qa([
        ["Challenge: what's the more secure authentication option?", "**Mutual CHAP** (reverse CHAP): the initiator also verifies the target, which prevents a rogue target."],
        ["Challenge: default iSCSI port?", "**TCP 3260**."],
        ["What is an IQN and where do you find it?", "The unique iSCSI name of an initiator or target (`iqn.1991-05.com.microsoft:<fqdn>`). iSCSI Initiator → Configuration tab."],
        ["Is iSCSI block or file storage?", "**Block**. The client formats the LUN with its own file system."],
        ["Can two non-clustered servers use the same iSCSI LUN at once?", "No. Without a cluster file system (CSV) they corrupt NTFS. Share files with SMB instead."],
    ], title="iSCSI lab: Questions & Answers")

    # ---------------- SG-25 ----------------
    s.h2("SG-25  RAID 0 / 1 / 5 (and 6, 10)")
    s.table(["RAID", "Technique", "Min disks", "Fault tolerance", "Usable capacity", "Performance", "Use"], [
        ["**0**", "**Striping**, no parity", "2", "**None**: one failure loses everything", "100% (n × size)", "Fastest read and write", "Temp, scratch, video editing"],
        ["**1**", "**Mirroring**", "2", "1 disk", "**50%**", "Good read, normal write", "OS / boot volumes, small critical data"],
        ["**5**", "**Striping with distributed parity**", "**3**", "1 disk", "(n − 1) × size", "Good read, **slower write** (parity calculation)", "File servers, general data"],
        ["6", "Striping with **dual** parity", "4", "2 disks", "(n − 2) × size", "Slower write than RAID 5", "Large arrays, archives"],
        ["10 (1+0)", "Mirror pairs, then stripe", "4", "1 per mirror pair", "50%", "Fast read and write", "Databases, VMs"],
    ], widths=(0.6, 1.35, 0.6, 1.3, 1.1, 1.25, 1.3), size=8)
    s.box("key", [
        "**Capacity examples, 4 × 2 TB disks:** RAID 0 = 8 TB · RAID 1 (2 disks) = 2 TB · **RAID 5 = 6 TB** · RAID 6 = 4 TB · RAID 10 = 4 TB.",
        "**RAID is NOT a backup** (lecture): it protects against disk failure, not deletion, ransomware, corruption or site loss. Use the 3-2-1 backup rule.",
        "Hardware RAID (controller with cache and battery) is faster and OS-independent. Software RAID is done in Windows: dynamic disks or **Storage Spaces** (simple ≈ RAID 0, two-way mirror ≈ RAID 1, parity ≈ RAID 5).",
    ])
    s.h3("Diskpart (handout)")
    s.code("""diskpart
list disk
select disk 4
online disk
attributes disk clear readonly
clean                                  # wipes partition info (makes the disk blank for a storage pool)
convert gpt                            # or: convert mbr | convert dynamic | convert basic
create partition primary size=5120     # MB; omit size for the whole disk
select partition 1
active                                 # MBR system partition only
format fs=ntfs label=test quick        # or fs=refs
assign letter=Z
list volume
exit""")
    s.h3("Week 6 discussion: model answers")
    s.tag("model")
    s.qa([
        ["Partition vs volume?", "A partition is a contiguous section of **one** physical (basic) disk. A volume is a logical storage unit with a file system and drive letter or mount point. It can be a single partition or span several disks (dynamic or Storage Spaces)."],
        ["Sector vs allocation unit (cluster)?", "A **sector** is the smallest physical unit the disk reads or writes (512 bytes, or 4 KB on Advanced Format / 512e). An **allocation unit (cluster)** is the smallest space the *file system* allocates to a file (NTFS default **4 KB**; 64 KB is common for Hyper-V and SQL). A 1-byte file still uses one cluster."],
        ["What is a file system?", "The structure and rules an OS uses to name, store, find and secure files on a volume (FAT32, exFAT, NTFS, ReFS, ext4, XFS)."],
        ["Basic vs dynamic disk?", "Basic = partitions, the standard and recommended choice. Dynamic = LDM volumes (spanned, striped, mirrored, RAID 5), now deprecated in favour of Storage Spaces."],
        ["Storage pool vs storage space?", "A pool is the collection of physical disks. A storage space (virtual disk) is a logical disk carved from the pool with its own resiliency and provisioning."],
        ["File vs block storage?", "See SG-24: file = shares over SMB/NFS (NAS); block = raw LUNs over iSCSI/FC (SAN), formatted by the host."],
        ["Thin vs thick vs fixed provisioning?", "Thin: allocate on write, can over-commit. **Thick / fixed**: all space reserved at creation (VMware *thick lazy-zeroed* zeroes blocks on first write; *eager-zeroed* zeroes everything up front, which is needed for FT/clustering). Hyper-V equivalents: dynamic VHDX vs fixed VHDX."],
    ], title=None)
