# Week 7 — AWS Storage Services: S3, EBS & EFS

## Learning Objectives

By the end of this week you should be able to:

1. **Match a workload to the right storage type**: **object** (S3), **block** (EBS) or **shared file** (EFS).
2. **Choose an S3 storage class** based on how often the data is accessed, how fast it has to come back, and whether it can live in a single Availability Zone.
3. **Pick an EBS volume type** for a workload, and explain how **snapshots**, **Elastic Volumes** and **Multi-Attach** work.
4. **Provision EFS from the CLI** (filesystem → mount target + NFS SG → EC2 + cloud-init mount) and **script an S3 backup/restore** (`s3api` + `s3 sync`).

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

### 6. Matching workloads (`aws-storage-services.md`)

The lab notes add concrete "when do I pick this?" examples on top of the chapter:

| Service | Pick it when… | Course examples |
| ------- | ------------- | --------------- |
| **S3** | Unstructured objects fetched by key, over the internet or APIs | Website images/videos; database backups with lifecycle policies; data lakes feeding Athena |
| **EBS** | One EC2 instance needs a disk (boot volume, database, or provisioned IOPS) | MySQL/PostgreSQL data; OS + app files; financial transaction systems on io1/io2 |
| **EFS** | Many servers must read/write the **same POSIX files at once** | Shared uploads for a web fleet; CMS content; scientific datasets mounted from EC2 and on-prem Linux |

---

### 7. GitLab lab 1 — `aws-cli-efs-exercise` (demo)

Repo: [gitlab.com/cit_3640/aws-cli-efs-exercise](https://gitlab.com/cit_3640/aws-cli-efs-exercise)

Uses the **default VPC** (so you can ignore the Week 4 custom VPC) and the **`bcitkey`** key pair from Week 5. Default Debian user is still **`admin`**.

Order matters: **the filesystem must be `available` before you create a mount target**, and a mount target needs a **subnet + security group**.

```
create-efs  →  wait until LifeCycleState=available  →  efs_data
     ↓
create-mount-target  →  default VPC + subnet, two SGs, mount target  →  mount_data
     ↓
create-ec2  →  Debian AMI + cloud-init nfs mount  →  instance_<id>_data
     ↓
SSH, df -h, write /mnt/efs/shared.txt, launch a second instance, confirm the file is there
```

**`create-efs`** creates an encrypted, general-purpose, bursting filesystem:

```bash
aws efs create-file-system \
  --creation-token "efs-lab-$(date +%s)" \
  --encrypted \
  --performance-mode generalPurpose \
  --throughput-mode bursting \
  --tags Key=Name,Value=bcit-lab-efs \
  --query 'FileSystemId' --output text
```

Then it polls `aws efs describe-file-systems --query 'FileSystems[0].LifeCycleState'` until the state is `available` (or errors out after ~150 s) and writes `REGION` / `EFS_ID` to `efs_data`.

**`create-mount-target`** discovers the default VPC (`Name=isDefault,Values=true`) and one available subnet, then creates **two** security groups:

| SG | Ingress |
| -- | ------- |
| EC2 SG (`efs-lab-ec2-…`) | TCP **22** and **80** from `0.0.0.0/0` (lab only — restrict SSH in production) |
| EFS SG (`efs-lab-storage-…`) | TCP **2049** (NFS) from the **EC2 security group**, not from the internet |

```bash
aws efs create-mount-target \
  --file-system-id "$EFS_ID" \
  --subnet-id "$SUBNET_ID" \
  --security-groups "$EFS_SG" \
  --query MountTargetId --output text
```

Poll `describe-mount-targets` until `LifeCycleState=available`.

**`create-ec2`** looks up the latest Debian 13 AMI (same owner `136693071363` as Week 5), renders cloud-init by substituting the EFS DNS name:

```text
${EFS_ID}.efs.${REGION}.amazonaws.com
```

then launches with `--user-data file://cloud-init-rendered.yaml` and `aws ec2 wait instance-running`.

**`cloud-init.yaml`** installs `nfs-common`, writes a mount script, and appends fstab:

```text
$EFS_DNS:/  /mnt/efs  nfs4  defaults,_netdev,nfsvers=4.1  0  0
```

`_netdev` waits for the network before mounting. After SSH:

```bash
df -h
echo "Created on instance A" | sudo tee /mnt/efs/shared.txt
```

Run `create-ec2` again. The second instance must see the same `shared.txt` — that is the whole point of EFS.

**Cleanup (console):** delete the EFS (mount target goes with it), the **two tagged lab SGs** (never the Default SG), and both EC2 instances.

---

### 8. GitLab lab 2 — `aws-cli-s3-exercise` (Sourcehut submit)

Repo: [gitlab.com/cit_3640/aws-cli-s3-exercise](https://gitlab.com/cit_3640/aws-cli-s3-exercise)

Two CLI surfaces:

| Command family | Level | Used for |
| -------------- | ----- | -------- |
| `aws s3` | High-level | `sync`, `cp`, `ls`, `rb --force` |
| `aws s3api` | Low-level, 1:1 with the API | `create-bucket`, `head-bucket`, `list-objects-v2` |

`backup-info` needs **`jq`** (`sudo apt install jq` on Debian).

**TODOs to complete:**

`create-bucket` — buckets outside `us-east-1` need a **LocationConstraint**:

```bash
aws s3api create-bucket \
  --bucket "$bucket_name" \
  --region "$region" \
  --create-bucket-configuration LocationConstraint="$region"
```

Idempotency guard already in the script: `aws s3api head-bucket --bucket "$bucket_name"` (succeeds → bucket exists → exit 1).

`backup` — sync a local directory to the `backups/` prefix:

```bash
aws s3 sync "$source_dir" "s3://$BUCKET_NAME/backups/" --region "$AWS_REGION"
```

`backup-info` — list objects as JSON, then parse with `jq`:

```bash
objects_json=$(aws s3api list-objects-v2 \
  --bucket "$BUCKET_NAME" \
  --prefix "$backup_prefix" \
  --region "$AWS_REGION" \
  --output json)
```

`backup-restore` — reverse of backup:

```bash
aws s3 sync "s3://$BUCKET_NAME/backups/" "$destination_dir" --region "$AWS_REGION"
```

`delete-bucket` is already complete: confirms by retyping the name, then `aws s3 rb "s3://$BUCKET_NAME" --force` (empties and deletes) and removes local `bucket_info`.

**Deliverable:** your own Sourcehut repo of the completed scripts, submitted on D2L.

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `chapter10-week7` | Data-growth drivers, shared responsibility for storage, S3 durability/availability, **storage classes**, bucket-creation steps (Figures 10-1/10-2), **EBS volume types**, snapshots, Multi-Attach, EFS features |
| `aws-storage-services.md` | One-page S3 vs EBS vs EFS comparison plus concrete use-case examples; diagrams in `assets/aws-s3.jpeg`, `aws-ebs.jpeg`, `aws-efs.jpeg` |
| [GitLab: aws-cli-efs-exercise](https://gitlab.com/cit_3640/aws-cli-efs-exercise) | Encrypted EFS, mount target, NFS port 2049 SG, cloud-init `nfs-common` + fstab, two instances sharing `/mnt/efs` |
| [GitLab: aws-cli-s3-exercise](https://gitlab.com/cit_3640/aws-cli-s3-exercise) | `s3` vs `s3api`, `LocationConstraint`, `s3 sync` backup/restore, `head-bucket`, `jq`, `s3 rb --force` |
| `chapter 7.md` (Week 3) | EBS vs **instance store**, creating an AMI from an EBS snapshot |
| `study-guide/week-02-iam-security.md` | KMS, SSE-S3 vs SSE-KMS, the EC2 → S3 **IAM role** scenario (`transcripts/6.2 …`) |
| `study-guide/week-05-aws-cli-bash.md` | CLI basics; `bcitkey` and Debian AMI lookup reused here |

---

## Practical Takeaways — Why This Matters

- **Storage class choice is a bill you pay every month.** Leaving years of logs in S3 Standard instead of Glacier Deep Archive can multiply storage costs. **Lifecycle policies** automate the move.
- **"Block all public access" is the default for a reason.** Public buckets are one of the most common causes of cloud data leaks. That configuration is *your* side of the shared responsibility model.
- **Snapshots are your EBS safety net.** They're incremental and cheap, so snapshot before risky changes and automate it with Data Lifecycle Manager.
- **Shared data across servers → EFS, not EBS.** Trying to share one EBS volume (without io2 Multi-Attach and a cluster-aware app) is a classic design mistake.
- **NFS is not open to the internet.** The EFS lab SG allows port **2049** only from the EC2 security group. Opening 2049 to `0.0.0.0/0` is a common, dangerous mix-up with the SSH/HTTP rules.
- **`s3 sync` is incremental.** Re-running `backup` after you change one test file only uploads the delta — same idea as EBS snapshots storing changed blocks.

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

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** Under the Shared Responsibility Model for storage, which task belongs to **you**, the customer?

- A) Maintaining the hardware behind S3
- B) Securing the data centers that host EBS volumes
- C) Configuring bucket policies and encryption settings
- D) Replicating EBS volumes within their Availability Zone

**2.** A team stores files in S3 but has no idea how often each file will be read, and the pattern keeps changing. Which storage class moves data between access tiers automatically?

- A) S3 Intelligent-Tiering
- B) S3 Standard-IA
- C) S3 Glacier Flexible Retrieval
- D) S3 One Zone-IA

**3.** What does an **EFS access point** provide?

- A) A way to mount EFS from on-premises servers only
- B) A separate copy of the file system in each Availability Zone
- C) A lifecycle rule that moves rarely used files to Infrequent Access
- D) An entry point into the file system with its own root directory and enforced POSIX user/group permissions

**4.** How does the guide describe the durability of **EBS**?

- A) 11 nines (99.999999999%)
- B) An annual failure rate (AFR) of 0.1–0.2%
- C) 99.99% availability, backed by an SLA
- D) 99.5% availability

**5.** Users on another continent upload large files to your S3 bucket, and the uploads are slow because of the distance. Which feature speeds them up?

- A) S3 Express One Zone
- B) S3 Object Lock
- C) S3 on Outposts
- D) S3 Transfer Acceleration

**6.** Which command uploads `report.pdf` to an existing bucket?

- A) `aws s3 mb s3://my-unique-bucket-name/report.pdf`
- B) `aws s3 ls s3://my-unique-bucket-name report.pdf`
- C) `aws s3 cp report.pdf s3://my-unique-bucket-name/`
- D) `aws s3 upload report.pdf my-unique-bucket-name`

**7.** A data warehouse reads large files sequentially. **Throughput (MB/s) matters more than IOPS**, and HDD pricing is preferred. Which EBS volume type fits?

- A) st1
- B) sc1
- C) io2
- D) gp3

**8.** You create a **50 GiB gp3** volume and don't pay for any extra performance. What baseline do you get?

- A) 80,000 IOPS and 2,000 MiB/s
- B) 3,000 IOPS and 125 MiB/s
- C) 256,000 IOPS and 4,000 MB/s
- D) It depends on the volume size, so 50 GiB gets less than larger volumes

**9.** You snapshot a 100 GiB EBS volume. Later, 2 GiB worth of blocks change and you take a second snapshot. What does the second snapshot store?

- A) A full new copy of all 100 GiB
- B) Only the roughly 2 GiB of blocks that changed
- C) Nothing, because snapshots only record the first state of a volume
- D) 102 GiB: the full volume plus the changes

**10.** A law firm must keep closed case records for **seven years**. They are almost never opened, and waiting up to two days for one is acceptable. Which S3 class is the cheapest fit?

- A) S3 Standard-IA
- B) S3 Glacier Instant Retrieval
- C) S3 Intelligent-Tiering
- D) S3 Glacier Deep Archive

**11.** A production EC2 instance's gp2 volume needs to become gp3 and grow larger, but the server **can't be stopped**. What should you use?

- A) Take a snapshot, then restore it to a new gp3 volume
- B) Stop the instance and replace the volume
- C) Elastic Volumes
- D) Multi-Attach

**12.** Two EC2 instances in the **same Availability Zone** run a mission-critical, cluster-aware application that must share **one block-storage data set**. Which option fits?

- A) gp3 with Multi-Attach
- B) io2 Block Express with Multi-Attach, with the application coordinating writes
- C) st1 with Multi-Attach
- D) Any EBS type, since EBS is replicated within the AZ

**13.** A hospital's policy says some data must **stay on-premises**, but developers want to use the normal S3 API. Which option fits?

- A) S3 on Outposts
- B) S3 One Zone-IA
- C) S3 Transfer Acceleration
- D) S3 Glacier Deep Archive

**14.** Every time a user uploads a photo to a bucket, a thumbnail should be generated automatically without running a server. What does the guide say S3 can trigger for this?

- A) An EFS mount
- B) An EBS snapshot
- C) A Glacier restore
- D) A Lambda function

**15.** An ML training job needs **sub-millisecond** access to hot data, with compute placed right next to it. Which S3 class fits?

- A) S3 Standard
- B) S3 Glacier Instant Retrieval
- C) S3 Express One Zone
- D) S3 Intelligent-Tiering

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** You own security **in** the cloud: encryption settings, access controls such as bucket policies, and backup policies. Hardware, data centers and EBS replication are AWS's side, security **of** the cloud.
2. **A.** **Intelligent-Tiering** is for unpredictable or changing access patterns and moves data between its tiers automatically. Standard-IA assumes you already know the data is infrequently accessed.
3. **D.** Access points give apps sharing one EFS their own root directory and enforced POSIX permissions, which isolates them. Lifecycle tiering (option C) is a separate EFS feature.
4. **B.** EBS durability is given as a **0.1–0.2% AFR**. 11 nines is the figure for **S3 and EFS**, which is the tempting mix-up.
5. **D.** **Transfer Acceleration** routes uploads through CloudFront edge locations to speed up long-distance transfers. Express One Zone is about sub-millisecond access in a single AZ, not upload distance.
6. **C.** `aws s3 cp` copies (uploads) a file to the bucket. `mb` makes a bucket and `ls` lists one; `aws s3 upload` isn't the command the guide shows.
7. **A.** **st1** (Throughput Optimized HDD) is built for big data and data warehouses. **sc1** is also HDD, but it's for infrequently accessed data.
8. **B.** gp3 gives a baseline of **3,000 IOPS and 125 MiB/s at any size**. 80,000 IOPS and 2,000 MiB/s is the maximum you can pay extra for.
9. **B.** Snapshots are **incremental**, so after the first one only **changed blocks** are stored. That's what makes them cheap and quick.
10. **D.** **Glacier Deep Archive** is the cheapest class, built for legal and regulatory records kept for years, and its 12–48 hour retrieval fits the two-day window. Glacier Instant Retrieval gives millisecond access the firm doesn't need, at a higher storage cost.
11. **C.** **Elastic Volumes** change size, performance and type on the fly with no stop and no downtime. Snapshot-and-restore works, but it means swapping volumes instead of changing the live one.
12. **B.** Multi-Attach is only for **io2 Block Express**, all instances must be **in the same AZ**, and the **application** must handle multiple servers writing safely. gp3 and st1 don't support it.
13. **A.** **S3 on Outposts** keeps the data on the Outposts rack on-premises while using the same S3 API. One Zone-IA still stores data in an AWS Availability Zone.
14. **D.** In event-driven designs, an S3 upload **triggers Lambda**. That's the serverless use case the guide lists, along with integrations with API Gateway, SNS and SQS.
15. **C.** **S3 Express One Zone** offers sub-millisecond access for real-time analytics and ML training, with compute placed next to the data. S3 Standard returns data in milliseconds, not sub-milliseconds.

</details>
