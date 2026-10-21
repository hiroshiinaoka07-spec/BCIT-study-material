# Week 1 — Cloud Fundamentals & Your Linux Workstation

## Learning Objectives

By the end of this week you should be able to:

1. **Define cloud computing** and explain why organizations adopt it (flexibility, security, efficiency, cost).
2. **Classify** a service by deployment model (public / private / community / hybrid) and service model (IaaS / PaaS / SaaS).
3. **Set up and correctly use** a Linux development environment for the rest of the course.

---

## Key Concepts & Deep Dive

### 1. What "the cloud" actually is

The course anchors everything on the NIST definition (`wk01.md`):

> Cloud computing is a model for enabling ubiquitous, convenient, **on-demand network access** to a **shared pool of configurable computing resources** … that can be **rapidly provisioned and released** with minimal management effort.

Unpack the bolded parts — they're the whole idea:

- **On-demand** → you create resources when you need them, not after a hardware purchase order.
- **Shared pool** → many customers share the provider's hardware (see *multitenancy* below).
- **Rapidly provisioned and released** → you pay for what you use (consumption-based pricing), then turn it off.

### 2. The three building blocks

| Component | What it is | AWS example (coming later) |
| --------- | ---------- | -------------------------- |
| **Servers** | Physical machines in a data center, usually running many VMs (each a *Virtual Private Server*) | EC2 (Week 3) |
| **Networking** | Connects storage, apps, and workloads across servers/data centers; includes load balancers and switches | VPC (Week 4) |
| **Storage** | Persistent, scalable data reachable over the network | EBS, S3 |

### 3. Deployment models — *who owns and shares the infrastructure*

- **Public cloud** — run by a third party (AWS, GCP, Azure), shared on demand.
- **Private cloud** — dedicated to one organization. ⚠️ Two traps from the notes:
  - *On-premises ≠ private cloud.* On-prem just means you run your own local infrastructure.
  - *A private cloud doesn't have to be on-premises.*
- **Community cloud** — organizations with similar needs pool infrastructure.
- **Hybrid cloud** — public + private combined. **Your on-prem data center + AWS = hybrid.**

### 4. Service models — *how much the provider manages for you*

Think of it as a ladder of control vs. convenience:

```
More control  ◄──────────────────────────────►  More managed
   IaaS                    PaaS                     SaaS
 (AWS EC2)               (Vercel)              (Google Docs)
 You manage the OS,     You bring the code;    You just use
 runtime, and app       platform runs it       the application
```

Most AWS services are IaaS — which is why this course has you managing Linux servers yourself.

### 5. Regions, Availability Zones, and related terms

- **Region** — a geographic area of infrastructure, e.g. `us-west-2` (Oregon), `ca-central-1` (Canada). The course uses **`us-west-2`**.
- **Availability Zone (AZ)** — an isolated location *inside* a region with one or more data centers, e.g. `us-west-2a`, `us-west-2b`. Every AWS region has **at least three AZs**, so you can design for high availability.
- **Multitenancy** — many customers (tenants) share physical hardware but are *logically isolated* via access controls, virtualization, network isolation, and encryption.
- **Infrastructure as Code (IaC)** — define the *desired state* of infrastructure in code instead of clicking through consoles (e.g. Terraform / OpenTofu, which you'll touch later this term).

### 6. Your Linux environment

You need a Linux system for Bash scripting and installing tools. Three options (`linux-environment.md`):

1. **Run Linux natively** (optionally isolate course work with `distrobox`).
2. **A VM** (VirtualBox or similar) — headless is fine; no GUI needed.
3. **WSL** on Windows — the most common choice, with one crucial rule:

> **Work in the WSL file system, not the Windows one.** If your prompt path contains `/mnt/c`, you're in Windows — expect permission errors.

Fix it by typing `cd` on its own to jump to your WSL home directory. You can still open Windows Explorer on your current folder with:

```bash
explorer.exe .
```

Optional: enable `systemd` in WSL 2 by adding this to `/etc/wsl.conf`:

```ini
[boot]
systemd=true
```

Debian is the recommended distro since it's what most of the class already knows.

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `README.md` | The week-by-week reading schedule (flipped material) for the whole term |
| `wk01.md` | Course evaluation (Participation 15%, Test 15%, Midterm 30%, Final 40%), cloud definitions, deployment/service models, regions & AZs, IaC |
| `linux-environment.md` | The three ways to set up Linux, the WSL `/mnt/c` warning, optional systemd |

---

## Practical Takeaways — Why This Matters

- **Vocabulary is the exam.** The Cloud Practitioner-style questions in later chapters assume you can instantly classify IaaS vs PaaS vs SaaS and public vs hybrid.
- **AZs are how real systems survive outages.** A single data center can fail; spreading across AZs is the basic high-availability pattern you'll build in Week 4.
- **IaC is the industry direction.** Clicking in the console is fine for learning, but teams version-control their infrastructure. The CLI scripting in Week 5 is your first step there.
- **A broken dev environment costs you every week.** Fix the WSL file-system habit now and you'll avoid mysterious permission errors with SSH keys later (SSH refuses keys with loose permissions, which is common under `/mnt/c`).

---

## Knowledge Check

**Q1 (Multiple choice).** AWS EC2 lets you rent virtual machines where you manage the operating system and software yourself. Which service model is this?

- A) SaaS
- B) PaaS
- C) IaaS
- D) FaaS

**Q2 (Multiple choice).** A company keeps its payroll database in its own on-premises data center but runs its public website on AWS. Which deployment model is this?

- A) Private cloud
- B) Hybrid cloud
- C) Community cloud
- D) Public cloud

**Q3 (Code reading).** You open your WSL terminal and see this prompt:

```
user@laptop:/mnt/c/Users/user/projects$
```

What does the `/mnt/c` tell you, why is it a problem for this course, and what single command fixes it?

**Q4 (Fill in the blank).** In the identifier `us-west-2b`, `us-west-2` is the ________ and `us-west-2b` is a(n) ________. Every AWS region contains at least ________ of these.

**Q5 (Scenario).** Your team's web application runs on one server in `us-west-2a`. Last month a power issue took that data center offline for two hours. Using only concepts from this week, how would you redesign the deployment to reduce the risk of this happening again, and why does it work?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

**Q1 — C) IaaS.** You get infrastructure (compute, storage, networking) and manage everything above it. The notes call out EC2 as the IaaS example and note that most AWS services are IaaS.

**Q2 — B) Hybrid cloud.** Combining your own infrastructure with a public cloud is hybrid. It is *not* "private cloud" just because part of it is on-premises — the notes explicitly warn that on-prem ≠ private cloud.

**Q3** — `/mnt/c` means you're working inside the **Windows file system** mounted into WSL. This causes **permission errors** (and slightly worse performance). Run **`cd`** with no arguments to go to your WSL home directory.

**Q4** — **Region**; **Availability Zone**; **three**.

**Q5** — Run copies of the application in **multiple Availability Zones** (e.g. `us-west-2a` and `us-west-2b`) within the region. AZs are isolated locations with separate data centers, so a failure in one AZ doesn't take down the other. This is exactly why AWS guarantees at least three AZs per region. (You'll learn the networking side — subnets per AZ — in Week 4.)

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** According to the NIST definition used in this course, cloud computing provides on-demand network access to what?

- A) Dedicated physical servers owned by each customer
- B) A shared pool of configurable computing resources
- C) A single data center located in each customer's country
- D) Software installed on each user's local workstation

**2.** Which statement best describes **multitenancy**?

- A) Each customer gets their own physical server that no one else uses
- B) An application is split across several AWS regions
- C) Infrastructure is defined as code instead of through a console
- D) Many customers share physical hardware but are logically isolated from each other

**3.** What is an **Availability Zone**?

- A) An isolated location inside a region with one or more data centers
- B) A geographic area such as `us-west-2` that contains several regions
- C) A separate AWS account created for each region
- D) The physical server that hosts a single virtual machine

**4.** On the service-model ladder from the guide, which model gives **you** the most control (and the most to manage)?

- A) SaaS
- B) PaaS
- C) IaaS
- D) All three give the same level of control

**5.** You're in your WSL home directory and want to browse the current folder in Windows Explorer. Which command does the guide recommend?

- A) `explorer.exe .`
- B) `cd /mnt/c`
- C) `cd`
- D) `systemctl start explorer`

**6.** You want to enable `systemd` in WSL 2. Which change matches the guide?

- A) Add `systemd=true` to `~/.bashrc`
- B) Add this to `/etc/systemd.conf`:

  ```ini
  [wsl]
  systemd=enabled
  ```

- C) Add this to `/etc/wsl.conf`:

  ```ini
  [boot]
  systemd=true
  ```

- D) Run `explorer.exe systemd` from the WSL prompt

**7.** Which of these identifiers names a **region** rather than an Availability Zone?

- A) `us-west-2a`
- B) `ca-central-1`
- C) `us-west-2b`
- D) `us-west-2c`

**8.** With a service like **Vercel**, you bring your code and the platform runs it for you. Which service model is this?

- A) IaaS
- B) SaaS
- C) Community cloud
- D) PaaS

**9.** Load balancers and switches belong to which of the three cloud building blocks?

- A) Servers
- B) Storage
- C) Networking
- D) Multitenancy

**10.** Several hospitals with the same regulatory requirements agree to pool their infrastructure and share it among themselves. Which deployment model is this?

- A) Community cloud
- B) Public cloud
- C) Hybrid cloud
- D) Private cloud

**11.** A colleague says: "All our servers are in our own building, so by definition we have a private cloud." Which response matches the guide?

- A) Correct — on-premises and private cloud mean the same thing
- B) Correct — a private cloud must always be on-premises
- C) Incorrect — anything in your own building is a hybrid cloud
- D) Incorrect — on-premises just means running your own local infrastructure; it isn't automatically a private cloud

**12.** A student keeps their SSH private key under `/mnt/c/Users/student/keys/` in WSL, and SSH refuses to use the key. What is the most likely reason, according to the guide?

- A) SSH keys only work on native Linux, not in WSL
- B) Files under `/mnt/c` commonly have loose permissions, and SSH refuses keys with loose permissions
- C) The key must be stored in `/etc/wsl.conf`
- D) `systemd` is not enabled, so SSH cannot read the key

**13.** A startup wants to test an idea for one week and then shut everything down, without buying any hardware. Which part of the cloud definition makes this possible?

- A) Multitenancy
- B) The community cloud model
- C) Resources can be rapidly provisioned and released, and you pay only for what you use
- D) Every region has at least three Availability Zones

**14.** Your team sets up servers by clicking through the AWS console, and every environment ends up slightly different. You want the infrastructure to be reviewable and version-controlled. What approach does the guide point to?

- A) Infrastructure as Code, such as Terraform / OpenTofu, which defines the desired state in code
- B) Moving everything to a SaaS product
- C) Switching to a hybrid cloud
- D) Running all servers in a single Availability Zone

**15.** You're on a Windows laptop and need a Linux environment for this course. Which setup best follows the guide's advice?

- A) WSL, keeping all course files under `/mnt/c` so Windows can see them
- B) WSL with Debian, keeping course files in the WSL file system (your WSL home directory)
- C) A VirtualBox VM, which must have a full desktop GUI installed
- D) Native Linux only, because WSL and VMs are not supported

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** NIST describes on-demand network access to a **shared pool of configurable computing resources**. Option A is the opposite of "shared pool"; resources are shared, not dedicated per customer.
2. **D.** Multitenancy means many tenants share physical hardware while being **logically isolated** through access controls, virtualization, network isolation, and encryption. Option A describes the absence of multitenancy.
3. **A.** An AZ is an isolated location **inside** a region with one or more data centers. Option B reverses the relationship: a region contains AZs, not the other way around.
4. **C.** IaaS sits at the "more control" end: you manage the OS, runtime, and app. SaaS (option A) is the most managed — you just use the application.
5. **A.** `explorer.exe .` opens Windows Explorer on the current folder. Option B would move you into the Windows file system, which is exactly what the guide tells you to avoid.
6. **C.** The guide adds a `[boot]` section with `systemd=true` to `/etc/wsl.conf`. Options A and B use the wrong files and wrong settings.
7. **B.** `ca-central-1` is a region (Canada). The others end in a letter, which marks an Availability Zone within `us-west-2`.
8. **D.** You bring the code and the platform runs it — that is **PaaS**, with Vercel as the guide's example. IaaS (option A) would have you managing the OS yourself.
9. **C.** The guide lists load balancers and switches under **Networking**, which connects storage, apps, and workloads. Servers (option A) are the machines that run VMs.
10. **A.** Organizations with similar needs pooling infrastructure is a **community cloud**. It isn't private (option D) because more than one organization shares it.
11. **D.** The guide explicitly warns that **on-prem ≠ private cloud**, and that a private cloud doesn't have to be on-premises. That rules out options A and B.
12. **B.** The guide notes that SSH refuses keys with loose permissions, which is common under `/mnt/c`. Option A is wrong — SSH works fine from the WSL file system.
13. **C.** "Rapidly provisioned and released" with consumption-based pricing lets you spin up, use, and turn off resources without a hardware purchase. Multitenancy (option A) is how providers share hardware, not why you can stop paying.
14. **A.** IaC defines the **desired state** of infrastructure in code, so it can be reviewed and version-controlled. A hybrid cloud (option C) is about where infrastructure lives, not how it's defined.
15. **B.** WSL is the most common choice, Debian is the recommended distro, and you must **work in the WSL file system**. Option A causes permission errors; option C is wrong because a headless VM is fine.

</details>
