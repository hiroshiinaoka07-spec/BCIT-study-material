# Week 3: Virtualization with Hyper-V — Hypervisors, Virtual Switches & Checkpoints

> **Midterm topics covered:** *Hyper-V and Hypervisors* and *Hyper-V Virtual Switches* (`Midterm.pdf` p.1) · *Checkpoints in Hyper-V* (`Midterm.pdf` p.2, first heading)
> **Sources:** `Module 5 Hyper-V.pdf` (23 slides), `Lecture Video.mp4` (Johnny's 45-min Hyper-V lecture → [`transcripts/Lecture Video/transcript.md`](<../../transcripts/Lecture Video/transcript.md>)), `Hyper-V Snapshots vs Snapshot Explained.pdf` (Altaro article)

## Learning Objectives

By the end of this week you should be able to:

1. **Explain what Hyper-V is**, compare **Type 1 (bare-metal)** and **Type 2 (hosted)** hypervisors, and give use cases for each.
2. **Choose the right virtual switch** (External, Internal, Private) for a scenario by knowing exactly who can talk to whom on each.
3. **Describe checkpoints** — Standard vs Production, the `.avhdx` files they create — and explain **why a checkpoint is not a backup**.

---

## 1. Why virtualize? What is Hyper-V?

**Why (lecture, 2:53–4:07):** modern hardware is huge (100+ cores, Server 2022 supports up to 64 TB RAM). One OS per physical server **wastes resources**. Running **multiple VMs on one host** saves money, improves efficiency, keeps services separated, and gives you safe, self-contained test systems.

**What Hyper-V is (slides 3–4):**

- The **hardware virtualization role** in Windows Server 2019/2022 (hypervisor-based virtualization for x64 since **Server 2008**).
- The **hypervisor sits between the hardware and the operating system** and **controls access to hardware**. Hardware drivers live in the **host OS**.
- Guest VMs **don't know** they run on virtualized hardware. Pick the wrong virtual hardware/profile and the guest OS can have problems.
- **Guest OSes:** Windows Server 2008 SP2+, Windows Vista SP2+, **Linux**, **FreeBSD**.

### Type 1 vs Type 2 hypervisors

| | **Type 1 (bare-metal)** | **Type 2 (hosted)** |
|---|---|---|
| Runs on | **Directly on the hardware** | **On top of a host OS**, as an application |
| Performance / overhead | Best performance, least overhead | Extra layer (host OS) → more overhead |
| Typical use | **Production servers, data centers** | **Desktops, labs, testing**, learning |
| Course examples | Hyper-V (slide 3: hypervisor between hardware and OS), VMware ESXi (in the lab VM list) | VMware Workstation, VirtualBox (what you run the course lab in) |

> ⚠ **Instructor nuance (lecture, 10:36–11:02):** Johnny says *"Hyper-V is the role, and also you can directly download the Hyper-V ISO and install above the hardware… so Hyper-V is type 2, and also Hyper-V is type 1."* His point: Hyper-V can be **enabled as a role inside Windows Server** *or* **installed bare-metal from the Hyper-V Server ISO**. On the exam, if asked which type Hyper-V is, **Type 1** matches slide 3's architecture — but be ready to explain his "both deployment styles" framing.

**Lab gotcha (lecture, 1:24–1:52):** Hyper-V conflicts with other hypervisors. With **WSL / Virtual Machine Platform** on, or with **VirtualBox**, you can't run Hyper-V nested in **VMware Workstation**. That's why most students can't finish the lab.

### Prerequisites (slides 8–9)

- Run **`systeminfo.exe`** to verify hardware support (VM Monitor Mode Extensions, virtualization enabled in BIOS, Data Execution Prevention).
- Host resources: **memory 8 GB+ (test)**, **storage SAN (enterprise) / S2D (test)**, **network 1 Gb (test) / 10 Gb (enterprise)**.
- **Nested virtualization** (a Hyper-V VM that is itself a Hyper-V host): ≥ **4 GB static memory**, same build on host and guest, useful for dev/test only.

---

## 2. Hyper-V virtual switches

Created in **Hyper-V Manager → Virtual Switch Manager** (slide 12, lecture 32:01).

![Virtual Switch Manager: External / Internal / Private](<../../transcripts/Lecture Video/frames/frame_0047.jpg>)

| Switch | VM ↔ VM (same host) | VM ↔ **Host** | VM ↔ physical network / other hosts | Needs a physical NIC? |
|---|---|---|---|---|
| **External** | ✅ | ✅ | ✅ | **Yes** — binds to one physical adapter |
| **Internal** | ✅ | ✅ | ❌ | No |
| **Private** | ✅ | ❌ | ❌ | No |

**Memory hook:** *External = everywhere. Internal = inside this box (host included). Private = VMs only, not even the host.*

**Use cases**

| Switch | When to use it |
|---|---|
| **External** | VMs need the LAN/internet, e.g. a VM file server users connect to |
| **Internal** | Host must manage/test VMs, but VMs stay off the real network |
| **Private** | Fully isolated lab: e.g. a test DC + client that must never touch production |

**Configuration details from the lecture demo (33:31–35:42):**

- **One physical NIC → one External switch.** Give it a meaningful name (he used `Internet`).
- After creating an External switch, Windows shows a new **`vEthernet (Internet)`** adapter. The **IP is copied from the physical NIC to the virtual adapter**.
- On the **physical NIC**, **IPv4 becomes unchecked** and **Hyper-V Extensible Virtual Switch** is bound instead. **This is normal — don't re-enable IPv4 or assign an IP to the physical adapter.**

![vEthernet adapter properties after creating the External switch](<../../transcripts/Lecture Video/frames/frame_0050.jpg>)

- Switches can also **configure VLANs**, and **capture** and **filter** traffic (slide 12). VLAN config isn't required for this course.

---

## 3. Checkpoints

**Definition (slide 20):** a checkpoint is a **snapshot of a VM at a particular point in time** that you can roll back to. "Checkpoint" is Hyper-V's name for a snapshot.

| | **Standard checkpoint** | **Production checkpoint** |
|---|---|---|
| Captures | Disk **and memory/running state** | Disk data only, via **VSS** inside the guest |
| Consistency (slide 6 wording) | **Application-consistent** | **Data-consistent** |
| On rollback | VM returns **running**, apps open exactly as they were | VM boots as if **from an offline state**; anything unsaved is gone |
| Default | **Yes** (lecture 42:41) | — |

**Lecture example (17:05–19:00):** open Notepad, type text **without saving**, take a checkpoint, then roll back.
- **Standard:** Notepad is still open **with the unsaved text**.
- **Production:** Notepad is gone; only what was **saved to disk** exists.

**How it works on disk:**

- A checkpoint creates a **differencing disk** — an **`.avhd` / `.avhdx`** file — for each `.vhd(x)`. All new writes go there, like a database log.
- **Deleting** a checkpoint **merges** its `.avhdx` back into the previous checkpoint/parent (slide 20).
- **Pass-through disks can't be checkpointed** — they're outside the hypervisor's control (Altaro).

**Checkpoint ≠ backup** (slide 20 and lecture 19:46 — "make sure remember"):

| Hyper-V checkpoint | VSS snapshot / backup |
|---|---|
| Rollback point for the **whole VM** (disk + memory + config) | **Disk only**, meant for backup apps to copy out |
| Lives **on the same storage** as the VM; depends on the parent disk | Copied **off** to long-term storage |
| You can build **chains and trees** of them | One snapshot at a time |
| **Aging checkpoints hurt performance and eat space** — a runaway `.avhdx` can fill the volume and stop the VM | VSS cleans up after itself |

**When Johnny says to take one (19:06–19:46):** before **Windows updates**, before **installing new applications**, before **removing a service** — any time you modify the system.

---

## 4. Supporting details you'll need (slides 10–23)

**Virtual disk formats and types**

| Format | Notes |
|---|---|
| `.vhd` | Old format, **~2 TB max**. Use only for Server 2008/2008 R2 compatibility |
| `.vhdx` | **Default choice**, larger than 2 TB (lecture: "file server → VHDX, not VHD") |
| `.vhds` | VHD Set (shared) file VMs connect to |
| `.avhdx` | Differencing/**checkpoint** disk where changes are stored |

| Type | Use |
|---|---|
| **Fixed-size** | **Production** — full size is reserved up front, so hosts can't overcommit |
| **Dynamically expanding** | **Test** — grows as used. Lecture warning: 3 VMs × 200 GB on < 400 GB free will eventually fill the disk |
| **Pass-through** | **Don't use** — maps a physical disk directly; very hard to move |
| **Differencing** | Stores only changes vs a parent (like a linked clone). Breaks if the parent is modified or removed; layers hurt performance. **Run Sysprep** before cloning this way |

**Generation 1 vs Generation 2**

| Gen 1 | Gen 2 |
|---|---|
| BIOS, IDE boot | **UEFI**, boot from virtual **SCSI** disk/DVD, **PXE** on the standard adapter |
| Supports 32-bit/old OSes (e.g. XP 32-bit) | **64-bit only** |
| — | **Secure Boot**, **hot add** memory/NIC, **vTPM / shielded VMs** |

**Other commands and features from the slides**

```powershell
Set-VMProcessor -VMName VM1 -EnableHostResourceProtection $true   # stop one VM hogging host CPU
Update-VMVersion "VMName"                                          # upgrade VM configuration version
Enter-PSSession -VMName VM1                                        # PowerShell Direct: no network needed
Invoke-Command -VMName VM1 -ScriptBlock { Get-Service }            # run a command inside the VM
```

- **PowerShell Direct:** host → VM only, **no network connectivity needed**, run PowerShell **as administrator**, supply **guest credentials**; host and guest must both run Windows Server 2022+ or Windows 10 (slide 22).
- **VM states:** Off, Starting, Running, Paused, Saved.
- **Import options:** Register in-place / Restore (keep the **existing unique ID**) vs **Copy** (create a **new unique ID**).
- **Best practices (slide 18):** Dynamic **Memory** (not dynamic disks!), avoid differencing disks, multiple synthetic NICs, each VM's files on a separate volume, **don't store VMs in the default location**.

---

## Module Tour

| Where | What to look at |
|---|---|
| `Midterm.pdf` **p.1** *Hyper-V and Hypervisors*, *Hyper-V Virtual Switches*; **p.2** *Checkpoints in Hyper-V* | The tested wording |
| `Module 5 Hyper-V.pdf` slides 3–4 | What Hyper-V is, hypervisor placement |
| slides 5–7 | New features (host resource protection, nested virtualization, shielded VMs, Standard vs Production checkpoints, DDA) |
| slides 10–11 | Disk formats and types |
| **slide 12** | **Virtual switch types** |
| slides 14–15 | Generation 2, hot add |
| **slide 20** | **Managing checkpoints** |
| slide 22 | PowerShell Direct |
| `Lecture Video` **10:36** | "Hyper-V is type 1 and type 2" |
| `Lecture Video` **17:05–19:54** | Standard vs Production checkpoint demo explanation; checkpoint vs backup |
| `Lecture Video` **32:01–35:45** | **Virtual Switch Manager demo** (frames `0046`–`0051`) |
| `Lecture Video` **38:19–39:24** | Gen 1 vs Gen 2 |
| `Hyper-V Snapshots vs Snapshot Explained.pdf` pp.3–5 | Hyper-V snapshot vs VSS snapshot differences |

## Practical Takeaways

- **Pick the switch by blast radius.** Private for anything risky (malware tests, a rogue DHCP server), External only for VMs that genuinely need the network.
- **Checkpoint before every change, delete it after you've verified.** Old checkpoints silently grow and can stop the VM when the volume fills.
- **Use Production checkpoints for servers running databases/AD** you'd roll back, since they're data-consistent; Standard is handy for quick lab rollbacks.
- **Fixed-size VHDX in production.** Dynamic disks let you overcommit storage without noticing until it's full.

---

## Knowledge Check: Week 3

**1. (Multiple choice)** Which statement best describes a **Type 1** hypervisor?
- A) It runs as an application on top of a desktop OS such as Windows 10
- B) It runs directly on the hardware and controls hardware access for the VMs
- C) It can only run Linux guests
- D) It requires a Type 2 hypervisor underneath it

**2. (Multiple choice)** Which virtual switch lets VMs talk to **each other and to the host**, but **not** to the physical network?
- A) External
- B) Internal
- C) Private
- D) Pass-through

**3. (Fill in the blank)** When you take a checkpoint, Hyper-V creates a differencing disk with the extension `________`. A ________ checkpoint uses VSS and is data-consistent, while a ________ checkpoint also saves memory and is application-consistent.

**4. (What does it handle?)** What does this command do, and what is its key requirement compared with normal remoting?
```powershell
Enter-PSSession -VMName DC1
```

**5. (Scenario)** You need to build a test lab on one Hyper-V host: a test DC and a client that must be **completely isolated** from both the production LAN **and** the Hyper-V host itself. Before installing a risky update on the DC you want a quick rollback point. Which switch type and which protection do you use, and why isn't that protection enough on its own for production?

<details>
<summary><b>Answer key with explanations (click to expand)</b></summary>

1. **B.** Type 1 (bare-metal) sits directly on the hardware — matching slide 3, "the hypervisor is installed between the hardware and the operating system". **A** describes Type 2 (e.g. VMware Workstation, VirtualBox).
2. **B, Internal.** External also reaches the physical network; Private excludes the host. "Pass-through" is a disk type, not a switch.
3. **`.avhdx`** (or `.avhd`). **Production** = VSS, data-consistent. **Standard** = includes memory/running state, application-consistent (and is the default).
4. It opens an interactive **PowerShell Direct** session from the **host into VM `DC1`**. It needs **no network connectivity** between host and VM (no IP, no virtual switch), but it only works **host → VM**, PowerShell must run **as administrator**, and you must supply **guest credentials**.
5. Use a **Private** switch — the only type that blocks VM ↔ host traffic as well as the physical network. Take a **checkpoint** before the update so you can roll back instantly. It's not enough on its own because **checkpoints are not backups**: they live on the same storage, depend on the parent disk, and aging `.avhdx` files degrade performance and can fill the volume. Production needs real backups too.

</details>
