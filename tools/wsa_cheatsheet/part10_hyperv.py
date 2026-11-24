"""Part 10: Virtualization & Hyper-V (SG-36, SG-37).  Part 11: VPN (SG-38)."""


def part10(s):
    s.part("PART 10 — VIRTUALIZATION AND HYPER-V (SG-36, SG-37)")
    s.src("Hyper-V lecture slides + Hyper-V lecture video; Nested Virtualization handout; Hyper-V Snapshots vs VSS Snapshots article (Altaro); Hyper-V lab; VMware network video; Lab 1A/1B; Week 1–2 and Week 5 discussion prompts.")

    # ---------------- SG-36 ----------------
    s.h2("SG-36  Virtualization: Type I vs Type II hypervisors")
    s.p("**Virtualization** runs several isolated virtual machines (each with its own OS) on one physical host. A **hypervisor** (Virtual Machine Monitor) shares out CPU, RAM, storage and network. Why virtualize (lecture): hardware is very powerful (hosts support up to 48–64 TB of RAM), so consolidation cuts hardware, power, cooling and space costs and improves efficiency, isolation, provisioning speed, testing (checkpoints) and HA/DR. VMware is the market leader; V2V tools convert between platforms.")
    s.table(["", "Type I: bare-metal (native)", "Type II: hosted"], [
        ["Runs on", "**Directly on the hardware**; the hypervisor *is* the lowest layer", "**On top of a host OS** (Windows, macOS, Linux) as an application"],
        ["Examples", "**Microsoft Hyper-V** (Hyper-V Server and the Hyper-V role), **VMware ESXi**, Citrix XenServer / XCP-ng, KVM, Proxmox", "**VMware Workstation / Player / Fusion** (used in this course's labs), **Oracle VirtualBox**, Parallels"],
        ["Performance", "Near-native, low overhead", "Extra overhead from the host OS"],
        ["Security / stability", "Smaller attack surface; host OS problems can't crash the VMs", "A host OS crash, reboot or malware affects every VM"],
        ["Use", "Production data centers, cloud, servers", "Desktops, labs, development and test, students"],
        ["Management", "Remote consoles (Hyper-V Manager, vCenter, WAC)", "A local GUI app"],
    ], widths=(1.2, 3.3, 3.0))
    s.box("trap", [
        "**Hyper-V is a Type 1 hypervisor, even when you add it as a role on Windows Server or enable it on Windows 10/11.** Once installed, the hypervisor loads *beneath* Windows, and the original Windows install becomes the privileged **parent (root) partition**. The instructor said Hyper-V \"is type 2 and also type 1\", meaning it *looks* hosted because you install it inside Windows. For a strict definition question, answer **Type 1**.",
        "Microsoft's free **Hyper-V Server** (no GUI, sconfig-style menu) is Type 1. The last free release was **2019**, even though the slide is titled 2022.",
    ])
    s.h3("What's new in Hyper-V (lecture)")
    s.table(["Host features (2016+)", "VM features (2016+)"], [
        ["**Host resource protection**: stops a VM from hogging host resources (`Set-VMProcessor -EnableHostResourceProtection $true`)\nHyper-V Manager improvements (alternate credentials, connect by IP, WS-MAN)\n**Nested virtualization**\n**Rolling Hyper-V cluster upgrade**\n**Shielded VMs** + HGS\n**VM start order priority**: e.g. start the back-end database before the front-end web tier\n**Storage QoS** (min/max IOPS per VM)\n**PowerShell Direct**",
         "**Discrete Device Assignment (DDA)**: pass a PCIe device (GPU, NVMe) straight to a VM\n**Hot add/remove of NICs and memory** (Gen 2; changing the CPU count needs a shutdown)\n**Integration services delivered through Windows Update**\n**Virtual TPM** (Windows 11 needs TPM 2.0; Windows 10 needs 1.2+)\n**Linux Secure Boot** (checks driver signatures)\nUp to **12 TB RAM / 240 vCPUs** per VM\n**Production checkpoints** (the default)\n2019: 2-node clusters with a file-share witness, S2D up to 4 PB, ReFS dedup, smaller Core image (5 GB → 1.58 GB), Linux shielded VMs"],
    ], widths=(3.75, 3.75), first_col_bold=False)
    s.h3("Requirements and installation")
    s.bullets([
        "**64-bit CPU with SLAT** (Intel EPT / AMD RVI), **VM Monitor Mode Extensions** (Intel VT-x / AMD-V) **enabled in BIOS/UEFI**, **hardware DEP** (Intel XD / AMD NX), and at least **4 GB RAM** (the lecture recommends 8 GB+). Check with `systeminfo.exe`: the *Hyper-V Requirements* section must show **Yes** four times, or \"A hypervisor has been detected\".",
        "**Conflicts:** VMware Workstation or VirtualBox can't use VT-x while Hyper-V, WSL2, *Virtual Machine Platform*, Windows Sandbox or VBS / Memory Integrity holds it (Module 2A p27 shows the *Windows Features* list). Newer VMware versions run on top of the Windows Hypervisor Platform, but more slowly.",
        "Install: Server Manager → Add Roles → **Hyper-V** → create virtual switches (pick the NIC) → **migration** settings → **default stores** for VHDX and config files (change them from C:) → restart. PowerShell: `Install-WindowsFeature Hyper-V -IncludeManagementTools -Restart`. Windows 10/11: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`.",
    ])
    s.h3("Nested virtualization (handout)")
    s.code("""Set-VMProcessor -VMName "Windows Server 2016" -ExposeVirtualizationExtensions $true   # VM must be OFF
Get-VMProcessor -VMName "Windows Server 2016" | fl          # ExposeVirtualizationExtensions : True
Get-VMNetworkAdapter -VMName "Windows Server 2016" | Set-VMNetworkAdapter -MacAddressSpoofing On
Set-VMMemory -VMName "Windows Server 2016" -DynamicMemoryEnabled $false -StartupBytes 4GB""")
    s.p("Nested rules: the VM gets **at least 4 GB of static memory (no dynamic memory)**, the host and guest run the **same build** (2016+/Win10+), Intel VT-x (AMD supported from 2022/Windows 11), and MAC spoofing or NAT for the inner VMs' networking. In **VMware** (the course labs), tick **Virtualize Intel VT-x/EPT or AMD-V/RVI** in the VM's processor settings.", size=9)
    s.h3("VM generations, disks and files")
    s.table(["", "Generation 1", "Generation 2"], [
        ["Firmware", "BIOS", "**UEFI** (Secure Boot, vTPM)"],
        ["Boot disk", "**IDE** controller", "**SCSI** (VHDX); boot disk up to 64 TB"],
        ["Guest OS", "32-bit or 64-bit, older OSes", "**64-bit only** (Windows 8 / 2012+, modern Linux)"],
        ["PXE boot", "Legacy NIC only", "**Standard (synthetic) NIC**"],
        ["Features", "Compatibility (e.g. Azure Gen 1 images)", "Faster boot, Secure Boot, **Shielded VM**, hot add NIC/memory, larger disks"],
        ["Change later?", "**No.** The generation can't be changed after creation", "—"],
    ], widths=(1.3, 3.0, 3.2))
    s.table(["Disk format / type", "Facts"], [
        ["**VHD**", "Max **2 TB** (2,040 GB), 512-byte sectors. Use only for 2008/2008 R2 or Gen 1 compatibility"],
        ["**VHDX**", "Max **64 TB**, 4 KB sectors, **log-based corruption protection** (power loss), TRIM, larger blocks. **The default; use it** (the instructor's advice)"],
        ["**VHDS** (VHD Set)", "Shared virtual disk for **guest clusters** (2016+)"],
        ["**AVHDX**", "Differencing file created by a **checkpoint**"],
        ["**Fixed size**", "All space allocated at creation; best performance; **use in production** (the instructor prefers it to avoid over-committing storage)"],
        ["**Dynamically expanding**", "Grows as data is written; saves space; good for **test**; risk of filling the volume"],
        ["**Differencing**", "Child disk that records changes against a read-only **parent**. Fast for labs, but **avoid many layers**; if the parent changes, the child is **invalid** (it can be re-linked with *Inspect Disk / Reconnect*)"],
        ["**Pass-through**", "A VM uses a physical disk directly. **Don't use it**: no checkpoints and hard to move (the instructor's advice)"],
    ], widths=(1.7, 5.8))
    s.code("""New-VHD -Path D:\\VMs\\VM1.vhdx -SizeBytes 60GB -Dynamic      # -Fixed | -ParentPath base.vhdx -Differencing
Convert-VHD -Path old.vhd -DestinationPath new.vhdx ; Resize-VHD -Path VM1.vhdx -SizeBytes 80GB ; Optimize-VHD -Path VM1.vhdx -Mode Full
New-VM -Name CA-VAN-VM1 -Generation 2 -MemoryStartupBytes 2GB -NewVHDPath D:\\VMs\\CA-VAN-VM1.vhdx -NewVHDSizeBytes 60GB -SwitchName External
Set-VMMemory CA-VAN-VM1 -DynamicMemoryEnabled $true -MinimumBytes 512MB -StartupBytes 2GB -MaximumBytes 4GB -Buffer 20
Add-VMDvdDrive -VMName CA-VAN-VM1 -Path D:\\ISO\\WS2022.iso ; Set-VMFirmware CA-VAN-VM1 -FirstBootDevice (Get-VMDvdDrive CA-VAN-VM1)
Start-VM CA-VAN-VM1 ; Get-VM | Select Name, State, Version, Generation ; Update-VMVersion -Name CA-VAN-VM1""", title="Hyper-V PowerShell")
    s.bullets([
        "**Configuration files:** older versions used **XML**; 2016+ uses binary **.VMCX** (configuration) + **.VMRS** (runtime state) (+ .VMGS guest state). **Configuration version 8.0+** is needed for the 2016+ features (9.0 = 2019, 10.0 = 2022). `Update-VMVersion \"VMName\"` is **one-way**: the VM can't then run on an older host.",
        "**Dynamic memory:** Startup RAM (allocated at boot, and must be enough for the OS to start), Minimum, Maximum, Buffer %, Weight. **Smart Paging** uses disk temporarily when a VM restarts and can't get its startup RAM.",
        "**VM states:** Off, Starting, **Running, Paused** (CPU frozen, RAM kept), **Saved** (RAM written to disk, like hibernate), Stopping. **Resource metering** (`Enable-VMResourceMetering`, `Measure-VM`) supports chargeback.",
        "**Import types:** **Register in place** (use the files where they are, same ID), **Restore** (copy to the default folders, **same ID**), **Copy** (copy with a **new unique ID**, for cloning). You can export a whole VM or a single checkpoint (`Export-VM`, `Export-VMSnapshot`).",
        "**Best practices:** fixed VHDX in production; avoid differencing chains; dynamic memory where it fits; several synthetic NICs; **separate volumes** for VM files and the host OS; keep integration services current; don't snapshot DCs with standard checkpoints.",
    ])
    s.h3("Checkpoints (snapshots)")
    s.table(["", "Standard checkpoint", "Production checkpoint (default since 2016)"], [
        ["Captures", "**Disk + memory + device state**: the running VM exactly as it was", "**Disk only**, made with **VSS** inside Windows guests (fsfreeze for Linux)"],
        ["Restore result", "VM resumes **running**, open apps included (instructor demo: **unsaved Notepad text was still there**). The instructor calls this *application-consistent* (application *state* is kept)", "VM boots **as if after a clean shutdown**; data on disk is **consistent** (instructor: *data-consistent*)"],
        ["Good for", "Lab or test rollback of a running state", "**Production workloads, DCs, SQL, Exchange** (supported by Microsoft)"],
    ], widths=(1.2, 3.1, 3.2))
    s.bullets([
        "**A checkpoint is NOT a backup** (instructor). It lives on the same storage as the VM and depends on the parent VHDX, and long chains of **.AVHDX** differencing files hurt performance. Delete it once it's no longer needed; deleting **merges** it back into the parent.",
        "Take one **before updates, software installs or removals**, then delete it once the change is verified.",
        "**Hyper-V snapshot vs VSS snapshot (Altaro article):** a Hyper-V checkpoint is a VM-level rollback point made with differencing disks. A **VSS (Volume Shadow Copy Service)** snapshot is a short-lived, **volume-level** copy-on-write shadow copy that **backup software** uses: a *requester* asks, *writers* (SQL, AD, the **Hyper-V VSS writer**) quiesce their data, and a *provider* creates the shadow copy. Production checkpoints and host-level backups of running VMs both use VSS, through the *Backup (volume shadow copy)* integration service.",
    ])
    s.code("""Set-VM -Name VM1 -CheckpointType Production      # Production | ProductionOnly | Standard | Disabled
Checkpoint-VM -Name VM1 -SnapshotName "Before KB update"
Get-VMSnapshot VM1 ; Restore-VMSnapshot -Name "Before KB update" -VMName VM1 -Confirm:$false ; Remove-VMSnapshot -VMName VM1 -Name *""")
    s.h3("Remote access to VMs")
    s.bullets([
        "**PowerShell Direct:** `Enter-PSSession -VMName VM1` / `Invoke-Command -VMName VM1 -ScriptBlock { Get-Service }` / `Copy-Item -ToSession`. **Host → its own VMs only; no network needed**; 2016+/Windows 10 host and guest; needs Hyper-V admin rights on the host **plus guest credentials**.",
        "**Enhanced Session Mode** (2012 R2+): VMConnect over RDP through the VMBus, giving clipboard, local drives, USB, audio and resizable screens without a network. `Set-VMHost -EnableEnhancedSessionMode $true`.",
        "Normal remoting between machines: `Enter-PSSession -ComputerName DC2` (needs the network, WinRM 5985 and the firewall).",
    ])
    s.h3("Shielded VMs and Host Guardian Service")
    s.bullets([
        "A **shielded VM** = **Gen 2 + vTPM + BitLocker**-encrypted disks (+ Secure Boot). Hyper-V admins can't see the console or inspect, debug or copy the VM's data. A **copied VHDX won't run on another host**.",
        "**HGS (Host Guardian Service)** is a separate, hardened 3-node cluster (its own AD forest) that provides **attestation** (is this host healthy and authorized?) and **key protection** (it releases the keys that unlock the VM only to guarded hosts). Attestation modes: **TPM-trusted** (hardware-rooted, strongest), **Host key** (2019+), **Admin-trusted** (AD group membership, deprecated in 2019).",
    ])
    s.h3("Hyper-V lab (CA-VAN-SVR6): Questions & Answers")
    s.qa([
        ["What does Svr6 need before you add the Hyper-V role?", "Domain-joined member server, a CPU with SLAT and VT-x/AMD-V exposed by VMware (*Virtualize Intel VT-x/EPT*), at least 4 GB RAM, and DEP. Check with `systeminfo`."],
        ["Steps?", "Add Roles → Hyper-V → create a virtual switch on the right NIC → migration (leave off) → default stores (change the location) → restart → Virtual Switch Manager → **External** switch bound to the correct Ethernet or Wi-Fi adapter → New VM *CA-Van-Vm1*, **Gen 2**, dynamic memory, connect the switch, VHDX location, ISO (copied into the VM with VMware Tools) → install → join the domain → `hostname` / `whoami`."],
        ["What is startup memory?", "The RAM given to the VM when it boots. It must be enough for the OS to start. With dynamic memory, Hyper-V can reclaim memory down to the *Minimum* and grow it up to the *Maximum* afterwards."],
        ["Why Gen 2?", "UEFI and Secure Boot, SCSI boot, faster, hot add of NICs and memory, and required for shielded VMs and vTPM."],
        ["After creating the External switch, the host's NIC shows IPv4 unticked and only *Hyper-V Extensible Virtual Switch* bound. Is that broken?", "**No, that's normal.** The physical NIC becomes a switch uplink, and the host's IP moves to the new **vEthernet (External)** adapter."],
    ])

    # ---------------- SG-37 ----------------
    s.h2("SG-37  Hyper-V virtual switches")
    s.table(["Switch type", "VM ↔ VM (same host)", "VM ↔ host", "VM ↔ physical network / other hosts", "Notes"], [
        ["**External**", "Yes", "Yes (if *Allow management OS to share this adapter* is on)", "**Yes**", "**Bound to one physical NIC (one External switch per NIC)**; the host IP moves to a vEthernet adapter. Use for production and Internet access"],
        ["**Internal**", "Yes", "**Yes**", "No", "Isolated lab with the host; the host gets a vEthernet adapter (add NAT for Internet: `New-NetNat`)"],
        ["**Private**", "Yes", "**No**", "No", "**VMs only**, no physical adapter needed; most isolated (e.g. a cluster heartbeat or malware lab)"],
    ], widths=(1.0, 1.0, 1.5, 1.5, 2.5), size=8)
    s.box("memory", "**External = everyone. Internal = VMs + host. Private = VMs only.** The default (NAT) switch on Windows 10/11 client Hyper-V is a built-in internal switch with NAT and DHCP.")
    s.bullets([
        "**Switch features:** VLAN ID (802.1Q tagging, for the VM or the management OS), **extensions** (capture, filtering, forwarding, e.g. NDIS capture or WFP), port mirroring, **DHCP Guard** / **Router Guard** (block rogue DHCP or RA from VMs), **MAC address spoofing** (needed for nested virtualization and some appliances), bandwidth management, SR-IOV, **Switch Embedded Teaming (SET)**.",
        "**Virtual NICs:** **synthetic** (network adapter, fast, needs integration services) vs **legacy** (emulated, Gen 1 only, used to PXE boot Gen 1).",
    ])
    s.code("""Get-NetAdapter
New-VMSwitch -Name "External" -NetAdapterName "Ethernet0" -AllowManagementOS $true
New-VMSwitch -Name "Internal" -SwitchType Internal
New-VMSwitch -Name "Private"  -SwitchType Private
Connect-VMNetworkAdapter -VMName CA-VAN-VM1 -SwitchName "External"
Set-VMNetworkAdapterVlan -VMName CA-VAN-VM1 -Access -VlanId 10
Set-VMNetworkAdapter -VMName CA-VAN-VM1 -DhcpGuard On -RouterGuard On ; Get-VMSwitch""", title="Virtual switch PowerShell")
    s.h3("Type 2 comparison: VMware Workstation networking (course labs)")
    s.table(["VMware mode", "Behaviour", "Hyper-V equivalent"], [
        ["**Bridged** (VMnet0)", "The VM joins the **host's physical LAN** with its own IP from the LAN's DHCP. Bridge VMnet0 to a **specific NIC**, not *Automatic* (VMware network video)", "External"],
        ["**NAT** (VMnet8)", "The VM shares the host's IP for outbound Internet. Host ↔ VM works; others reach the VM **only through port forwarding**", "Internal + NAT / Default Switch"],
        ["**Host-only** (VMnet1, the custom **VMnet9** used for the lab domain)", "A private network with the host, no Internet. In the **Virtual Network Editor**, untick *Use local DHCP service* (the lab's Windows DHCP serves it) and *Connect a host virtual adapter* as instructed", "Internal / Private"],
    ], widths=(1.8, 4.2, 1.5))
    s.box("trouble", [
        "- **VMs can't ping each other:** Windows Firewall blocks ICMPv4 echo. Allow *File and Printer Sharing (Echo Request – ICMPv4-In)* or add the `netsh` rule from Part 1. Also check that both VMs are on the **same VMnet**.",
        "- **A clone conflicts with its source:** same SID and name. Sysprep first. A **linked clone** depends on the parent, so never delete or move the base VM.",
    ])
    s.h3("Week 5 discussion: model answers")
    s.tag("model")
    s.qa([
        ["Production vs standard checkpoints?", "Production = VSS-based, disk only, the guest restarts clean, **supported for production apps** (the default). Standard = disk + memory state, the VM resumes exactly where it was, which risks inconsistency for DCs and databases."],
        ["What is the Host Guardian Service?", "A Windows Server role (Datacenter) that **attests** Hyper-V hosts and **releases keys** only to healthy guarded hosts so they can run shielded VMs (TPM, host-key or admin-trusted attestation)."],
        ["What is live migration?", "Moving a **running** VM from one Hyper-V host to another with **no noticeable downtime**: memory pages copy iteratively, then a brief final switchover. Variants: clustered (shared storage / CSV), **shared-nothing** (2012+, moves storage too), storage live migration. Needs compatible CPUs (or *processor compatibility mode*), a migration network and Kerberos or CredSSP authentication. Compare **Quick migration** (save, move, restore, so there's a short outage) and **Hyper-V Replica** (asynchronous DR copy)."],
        ["Benefits of a hypervisor?", "Consolidation and lower cost (hardware, power, space), isolation, fast provisioning from templates, checkpoints for safe changes, live migration and HA, DR replication, legacy OS support, dev/test labs."],
        ["External vs internal vs private switch?", "See SG-37: External = VMs + host + physical network; Internal = VMs + host; Private = VMs only."],
        ["What is a shielded VM?", "A Gen 2 VM with vTPM and BitLocker that only runs on HGS-attested guarded hosts, protecting it from compromised or malicious fabric admins and from disk theft."],
    ], title=None)


def part11(s):
    s.part("PART 11 — REMOTE ACCESS AND VPN (SG-38)")
    s.tag("supp", "No VPN lecture or lab was in the course folder. The course only mentions site-to-site (S2S) VPN in the network topology, the Azure Network Adapter point-to-site VPN (2019), and RRAS (used for the DHCP relay).")
    s.h2("SG-38  VPN protocols and ports")
    s.p("A **VPN (Virtual Private Network)** builds an encrypted **tunnel** across an untrusted network (the Internet). **Remote-access (point-to-site / client-to-site)** VPN connects individual users. **Site-to-site** VPN joins whole networks, e.g. a branch, or on-premises to Azure through a VPN gateway. On Windows Server the VPN server is **RRAS**: the **Remote Access** role, role service **DirectAccess and VPN (RAS)** (+ Routing, Web Application Proxy).")
    s.table(["Protocol", "Ports / IP protocols to open", "Encryption / authentication", "Notes"], [
        ["**PPTP**", "**TCP 1723** + **GRE (IP protocol 47)**", "MPPE, MS-CHAPv2", "Oldest and fastest to set up, but **insecure (MS-CHAPv2 is crackable). Avoid it.** GRE often blocked by NAT"],
        ["**L2TP/IPsec**", "**UDP 500** (IKE), **UDP 4500** (NAT-T), **UDP 1701** (L2TP, inside IPsec), **ESP (IP protocol 50)**", "IPsec (AES), with a computer **certificate or pre-shared key** + user authentication", "Strong; double encapsulation means some overhead. NAT traversal needs 4500"],
        ["**SSTP**", "**TCP 443** (HTTPS)", "SSL/TLS; needs a **server certificate** trusted by clients", "**Passes almost any firewall or proxy** (looks like HTTPS). Microsoft-proprietary"],
        ["**IKEv2** (IPsec)", "**UDP 500, UDP 4500** (+ ESP 50)", "IPsec with certificates or EAP", "**VPN Reconnect**: survives network changes (Wi-Fi ↔ LTE), so it's best for mobile. The preferred protocol for **Always On VPN**"],
        ["OpenVPN (not built into RRAS)", "UDP 1194 (or TCP 443)", "TLS / OpenSSL", "Open source, third-party"],
        ["WireGuard (not built in)", "UDP 51820", "ChaCha20, Curve25519", "Modern and fast, third-party"],
    ], widths=(1.2, 2.2, 2.0, 2.1), size=8)
    s.table(["Authentication / support service", "Port", "Notes"], [
        ["**RADIUS** through **NPS** (Network Policy Server)", "**UDP 1812** (auth), **1813** (accounting); legacy 1645/1646", "Centralizes VPN, Wi-Fi and 802.1X authentication and policy (conditions, constraints)"],
        ["PAP / CHAP / **MS-CHAPv2** / **EAP** (EAP-TLS, PEAP)", "—", "PAP = cleartext (never use). MS-CHAPv2 = password. **EAP-TLS = certificates (strongest)**"],
        ["IP address assignment", "—", "From the internal DHCP server (RRAS leases blocks of 10) or a **static pool**"],
        ["DirectAccess (legacy)", "IP-HTTPS TCP 443, IPv6, IPsec", "Always-on, automatic, domain-joined Enterprise clients only. **Replaced by Always On VPN**"],
    ], widths=(2.6, 2.4, 2.5), size=8)
    s.h3("Deploy a VPN server (RRAS)")
    s.steps([
        "Two NICs: Internet / DMZ (e.g. 133.12.10.x) and internal (192.168.239.x). Install the role: `Install-WindowsFeature RemoteAccess, DirectAccess-VPN, Routing -IncludeManagementTools`.",
        "Open **Routing and Remote Access** → right-click server → **Configure and Enable** → **Remote access (dial-up or VPN)** → VPN → choose the **Internet-facing** interface (this applies static packet filters) → IP assignment (**DHCP** or a range) → authentication: RRAS itself (Windows) or **RADIUS/NPS** → Finish. Or in PowerShell: `Install-RemoteAccess -VpnType Vpn`.",
        "Install a **certificate** for SSTP or IKEv2 (CN = the public FQDN, e.g. `vpn.adatum.com`).",
        "Grant users access: user Properties → **Dial-in** → *Network Access Permission*: **Allow access** or **Control access through NPS Network Policy** (recommended; create an NPS policy for a *VPN Users* group).",
        "Open the protocol's ports on the edge firewall (table above), publish a DNS name, then test from a client.",
    ])
    s.code("""Add-VpnConnection -Name "Adatum VPN" -ServerAddress vpn.adatum.com -TunnelType Ikev2 -AuthenticationMethod Eap -SplitTunneling
#   -TunnelType Pptp | L2tp (-L2tpPsk "key") | Sstp | Ikev2 | Automatic
rasdial "Adatum VPN" user P@ssw0rd ; rasdial "Adatum VPN" /disconnect
Get-RemoteAccess ; Get-VpnServerConfiguration ; Get-RemoteAccessConnectionStatistics""")
    s.box("trap", [
        "- **PPTP = TCP 1723 + GRE 47.** **L2TP/IPsec = UDP 500 + 4500 + 1701 + ESP 50.** **SSTP = TCP 443.** **IKEv2 = UDP 500 + 4500.** **RADIUS = UDP 1812/1813.**",
        "- The protocol that \"works through hotel firewalls\" is **SSTP** (443). The one that \"reconnects automatically when the network changes\" is **IKEv2**. The one to avoid is **PPTP**.",
        "- **Split tunneling** sends only corporate traffic through the VPN (less load, less control). **Force tunneling** sends everything through it (more security and inspection).",
    ])
    s.p("**Site-to-site to Azure (course topology):** an on-premises VPN device or RRAS ↔ Azure **VPN Gateway** + **Local Network Gateway**, IKEv2/IPsec with a pre-shared key. **Azure Network Adapter** (2019, through WAC) creates a **point-to-site** VPN from one server into an Azure VNet.", size=9)
