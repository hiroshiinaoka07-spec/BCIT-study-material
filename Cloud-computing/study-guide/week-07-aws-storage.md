# Week 7 — AWS Storage Services: S3, EBS & EFS

## Learning Objectives

By the end of this week you should be able to:

1. **Match a workload to the right storage type**: **object** (S3), **block** (EBS) or **shared file** (EFS).
2. **Choose an S3 storage class** based on how often the data is accessed, how fast it has to come back, and whether it can live in a single Availability Zone.
3. **Pick an EBS volume type** for a workload, and explain how **snapshots**, **Elastic Volumes** and **Multi-Attach** work.

---

## Key Concepts & Deep Dive

### 1. Why cloud storage? Who secures what?

The world is projected to generate **~175 ZB** of data by 2025 (up from 33 ZB in 2018), and nearly half of it will live in the cloud. The drivers: **AI training data, mobile devices, IoT sensors, and streaming services**. On-premises answers — direct-attached storage, **NAS**, **SANs** — work, but they're complex and expensive to run at that scale.

**Shared Responsibility Model applied to storage:**

| AWS — security **of** the cloud | You — security **in** the cloud |
| ------------------------------- | ------------------------------- |
| The hardware, data centers, and infrastructure behind S3/EBS/EFS | **Encryption** settings, **access controls** (IAM, bucket policies), **backup policies** |

### 2. The three storage types at a glance

| | **S3** | **EBS** | **EFS** |
| - | ------ | ------- | ------- |
| Storage type | **Object** | **Block** | **File** (shared) |
| What it looks like | Buckets of objects, reached by console/CLI/SDK/REST API | A **disk** attached to an EC2 instance — format it with any file system | A network file system mounted over **NFS 4.0/4.1** |
| Who can use it at once | Anyone/anything you grant access to | **One instance** (except io2 **Multi-Attach**, same AZ) | **Many** EC2 instances *and* on-prem Linux servers |
| Scope / redundancy | Multi-AZ (most classes) | Replicated **within one AZ** | Regional file system = **multi-AZ** |
| Durability | **11 nines** (99.999999999%) | **0.1–0.2% AFR** (annual failure rate) | **11 nines** |
| Scales | Unlimited total; **5 TB max per object** | Resize with **Elastic Volumes** (no downtime) | **Automatically**, up and down, to petabytes |
| Typical use | Website assets, data lakes, backups, event-driven apps | **Boot volumes**, databases | Shared content across servers |

> **Memory hook:** *S3 = a giant bucket of files you fetch by name. EBS = a hard drive for one server. EFS = a shared network drive for many servers.*

---

### 3. Amazon S3 (Simple Storage Service)

- **Object storage**, accessed via the **console, CLI, SDKs or REST APIs**.
- **No cap** on total storage; each object can be up to **5 TB**.
- **Durability: 11 nines** — copies spread automatically across **multiple AZs**.
- **Availability: 99.99%** (S3 Standard), backed by an **SLA** (a contract that sets the level of service).

⚠️ **Not every class is multi-AZ.** **S3 One Zone-IA** and **S3 Express One Zone** keep data in **one AZ** — cheaper, but less redundant.

**Security**

| Layer | Options |
| ----- | ------- |
| In transit | **SSL/TLS** |
| At rest | **Server-side** or **client-side** encryption (Week 2: SSE-S3 or SSE-KMS) |
| Access | **IAM roles**, **bucket policies** |
| Compliance | **Object Lock** → **WORM** (write-once-read-many) |

**Use cases**

| Use case | How S3 fits |
| -------- | ----------- |
| Primary storage for cloud apps | Website assets, mobile backends, gaming content, file distribution |
| Data lakes & analytics | Feeds **Athena, Redshift, EMR** |
| Backup & disaster recovery | **Lifecycle policies** move old backups to cheaper tiers or delete them |
| Serverless / event-driven | An upload **triggers Lambda**; integrates with API Gateway, **SNS**, **SQS** |

#### S3 storage classes — the exam favourite

| Class | Access pattern | AZs | Availability | Retrieval | Pick it for |
| ----- | -------------- | --- | ------------ | --------- | ----------- |
| **S3 Standard** (default) | Frequent | **≥ 3** | 99.99% | ms, low latency, high throughput | Cloud-native apps, dynamic websites, content delivery, analytics |
| **S3 Intelligent-Tiering** | **Unpredictable / changing** | Multi | Same as Standard | ms | You don't know the access pattern. Auto-moves data between **5 tiers** (Frequent, Infrequent, Archive Instant, Archive\*, Deep Archive\*). \*opt-in |
| **S3 Express One Zone** | Ultra-fast, hot | **1** | — | **Sub-ms** | Real-time analytics, ML training, compute right next to the data (Local Zones/Outposts) |
| **S3 Standard-IA** | Infrequent, needs fast access | Multi | **99.9%** | ms + **retrieval fee** | Backups, DR, old datasets |
| **S3 One Zone-IA** | Infrequent, re-creatable | **1** | **99.5%** | ms + retrieval fee | Cheapest IA, no cross-AZ redundancy |
| **S3 Glacier Instant Retrieval** | Archive, rarely accessed, needed on demand | Multi | — | **Milliseconds** | Archived media, medical imaging, compliance records |
| **S3 Glacier Flexible Retrieval** (formerly "Glacier") | Archive, accessed occasionally | Multi | — | **Minutes (expedited) → hours (bulk)** | Backups/archives that aren't time-sensitive |
| **S3 Glacier Deep Archive** | Almost never | Multi | — | **12–48 hours** | Legal and regulatory records kept for years — **cheapest** |

Rule of thumb: **the colder the data, the cheaper it is to store and the slower or costlier it is to retrieve.**

**Special cases**

| Need | Feature |
| ---- | ------- |
| Data must stay **on-premises** | **S3 on Outposts** — same S3 API, stored on the Outposts rack |
| Data must stay **inside a jurisdiction** | **Directory buckets in Dedicated Local Zones** (Express One Zone, One Zone-IA) |
| **Fast uploads across long distances** | **S3 Transfer Acceleration** — routes uploads through **CloudFront edge locations** |

#### Creating a bucket (console walkthrough, Figures 10-1 & 10-2)

1. Search **S3** → **Create bucket**.
2. **Region:** the one closest to you (lower latency) — for this course, `us-west-2`.
3. **Bucket type:** **General purpose** (multi-AZ default).
4. **Bucket name.**
5. **Object ownership:** **ACLs disabled — "Bucket owner enforced"** (recommended; your account owns every object).
6. **Block all public access** (recommended).
7. **Versioning:** Disable (no old versions kept).
8. **Encryption:** **Amazon S3 managed keys** (SSE-S3).
9. **Create bucket** → open it → **Upload** files/folders.

Since you've done Week 5, you can do the same from the CLI. The command below is the standard `aws s3` syntax; it isn't in the chapter notes:

```bash
aws s3 mb s3://my-unique-bucket-name --region us-west-2   # make bucket
aws s3 cp report.pdf s3://my-unique-bucket-name/          # upload
aws s3 ls s3://my-unique-bucket-name                      # list
```

---

### 4. Amazon EBS (Elastic Block Store)

- **The main boot storage for EC2.** Durable, high-performance **block** storage.
- **Replicated automatically within its AZ**, so a hardware failure doesn't lose data. **AFR 0.1–0.2%**.
- **Consistently low latency.** **Elastic Volumes** let you change **size, performance and type on the fly — no stop, no downtime**.
- Attached to an instance it behaves like a **native block device**: format it with any file system the OS supports. Data **persists** across reboots and detaches (Week 3: EBS = persistent, instance store = ephemeral).

#### Volume types

| Type | Media | Built for | Key numbers |
| ---- | ----- | --------- | ----------- |
| **gp2 / gp3** — General Purpose | SSD | **Boot volumes**, dev environments, most apps | gp3 baseline **3,000 IOPS + 125 MiB/s** at any size; up to **80,000 IOPS / 2,000 MiB/s** for extra cost |
| **io1 / io2 / io2 Block Express** — Provisioned IOPS | SSD | **Mission-critical databases** | Up to **256,000 IOPS, 4,000 MB/s**, **sub-ms** latency, **64 TB** |
| **st1** — Throughput Optimized | HDD | **Big data, data warehouses** — MB/s matters more than IOPS | — |
| **sc1** — Cold | HDD | **Infrequently accessed** data, moderate throughput | Cheapest |

> **Memory hook:** *SSD types are measured in IOPS (many small reads/writes). HDD types are measured in throughput (big sequential reads).*

#### Security
**AES-256** encryption **at rest and in transit**, with keys managed in **AWS KMS** (Week 2: encryption is chosen when the volume is created).

#### Snapshots
- **Point-in-time backups**, **incremental** — only **changed blocks** are stored, which saves time and money.
- Use them to: **create new volumes**, **copy across AZs or regions**, **share with other accounts**, and enable **fast restores**.
- Advanced: **snapshot locking** (compliance), **cross-region copy**, **archiving**, automation with **Data Lifecycle Manager**.
- Week 3 link: **snapshot → AMI** is how you clone a configured server.

#### Multi-Attach (io2 Block Express only)
- One volume attached to **multiple EC2 instances** at once, **all in the same AZ**.
- For high-availability, mission-critical apps that share one data set instead of keeping copies.
- ⚠️ The **application** must handle multiple servers writing safely — EBS doesn't do that for you.

---

### 5. Amazon EFS (Elastic File System)

- **Plug-and-play shared file storage**. It can also be mounted by **on-premises** servers.
- **Elastic**: grows to **petabytes** and shrinks again **automatically**, with no interruptions.
- Uses **NFS 4.0 and 4.1** — **many EC2 instances (and on-prem Linux servers) read/write the same files at the same time**.
- **Lifecycle tiering**: rarely-used files move **automatically** to **Infrequent Access** or **Archive** classes (like S3 tiers).
- **Access points**: multiple entry points into one file system, each with its **own root directory** and enforced **POSIX user/group permissions**. Use them to isolate different apps sharing one EFS.
- **Regional** file system: data stored **across multiple AZs**, **11 nines durability**, up to **99.99% availability**; throughput and IOPS **scale automatically**.

> **Not covered in the notes yet:** the chapter intro also lists **FSx** (shared file storage), **Storage Gateway** (bridges on-prem and cloud) and **AWS Backup** (data protection), but `chapter10-week7` stops in the middle of the EFS section. Add the rest of the chapter to the notes before the exam.

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `chapter10-week7` | Data-growth drivers, shared responsibility for storage, S3 durability/availability, **storage classes**, bucket-creation steps (Figures 10-1/10-2), **EBS volume types**, snapshots, Multi-Attach, EFS features |
| `chapter 7.md` (Week 3) | EBS vs **instance store**, creating an AMI from an EBS snapshot |
| `study-guide/week-02-iam-security.md` | KMS, SSE-S3 vs SSE-KMS, the EC2 → S3 **IAM role** scenario (`transcripts/6.2 …`) |
| `study-guide/week-05-aws-cli-bash.md` | CLI basics for scripting S3 and EBS work |

---

## Practical Takeaways — Why This Matters

- **Storage class choice is a bill you pay every month.** Leaving years of logs in S3 Standard instead of Glacier Deep Archive can multiply storage costs. **Lifecycle policies** automate the move.
- **"Block all public access" is the default for a reason.** Public buckets are one of the most common causes of cloud data leaks. That configuration is *your* side of the shared responsibility model.
- **Snapshots are your EBS safety net.** They're incremental and cheap, so snapshot before risky changes and automate it with Data Lifecycle Manager.
- **Shared data across servers → EFS, not EBS.** Trying to share one EBS volume (without io2 Multi-Attach and a cluster-aware app) is a classic design mistake.

---

## Knowledge Check

**Q1 (Multiple choice).** A web app's EC2 instances in **three Availability Zones** all need to read and write the **same set of files** at the same time. Which service fits best?

- A) Amazon EBS gp3
- B) Amazon EFS
- C) S3 Glacier Deep Archive
- D) EBS io2 Block Express with Multi-Attach

**Q2 (Multiple choice).** Which S3 storage class stores data in a **single Availability Zone**?

- A) S3 Standard
- B) S3 Standard-IA
- C) S3 One Zone-IA
- D) S3 Glacier Instant Retrieval

**Q3 (Fill in the blank).**
- S3 is designed for ________ nines of durability, and a single object can be up to ________ TB.
- EBS snapshots are ________, meaning only ________ blocks are stored after the first snapshot.
- EFS uses the ________ protocol, versions 4.0 and 4.1.

**Q4 (What does this setting handle?).** During bucket creation you choose **Object ownership → "Bucket owner enforced"** and **"Block all public access"**. What does each setting do, and which side of the Shared Responsibility Model owns these decisions?

**Q5 (Scenario).** A clinic must keep patient imaging for **10 years**. Images older than **30 days** are opened rarely, but when a doctor asks for one it must load **immediately**. Its main PostgreSQL database on EC2 needs **very high, guaranteed IOPS**. Which S3 class and which EBS volume type would you use, and how would you move images to the cheaper class automatically?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

**Q1 — B) Amazon EFS.** EFS is shared file storage over NFS that many instances can mount at once, and a regional file system spans multiple AZs. **A** attaches to one instance. **C** is archival object storage with 12–48 h retrieval. **D** is tempting, but Multi-Attach only works for instances **in the same AZ**, and the app must handle concurrent writes itself.

**Q2 — C) S3 One Zone-IA.** It's the cheaper IA option with **99.5%** availability and no cross-AZ redundancy. S3 Express One Zone is also single-AZ but isn't an option here. The others are multi-AZ.

**Q3** — **11** (99.999999999%); **5** TB. **Incremental**; **changed**. **NFS** (Network File System).

**Q4** — **Bucket owner enforced** disables ACLs, so **your account owns every object** in the bucket, and access is managed only through policies (IAM / bucket policies). That's simpler and harder to get wrong. **Block all public access** stops anyone from making the bucket or its objects public. Both are **your** responsibility, *security in the cloud*: AWS secures the infrastructure, but you configure access controls and encryption.

**Q5** — **S3 Glacier Instant Retrieval** for images older than 30 days: archive-level storage cost, but **millisecond** access, and the notes name **medical imaging** as an example use case. Use an S3 **lifecycle policy** to move objects from S3 Standard to Glacier Instant Retrieval after 30 days automatically. (Deep Archive would be cheaper, but its 12–48 h retrieval fails the "immediately" requirement.) For the database, use **Provisioned IOPS SSD (io1/io2/io2 Block Express)**: it's built for mission-critical databases, with up to 256,000 IOPS and sub-ms latency. gp3 tops out at 80,000 IOPS and isn't intended for that tier.

</details>
