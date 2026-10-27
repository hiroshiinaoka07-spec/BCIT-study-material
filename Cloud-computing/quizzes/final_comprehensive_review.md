# Final Comprehensive Review — CIT 3640 (Weeks 1–7)

Materials in this repo stop at storage. Weeks 9–13 (ALB/ASG, Route 53, DynamoDB, OpenTofu) are on the schedule but not yet in the notes — do not treat them as covered here.

Midterm (Week 8): Tue Oct 27, 14:00–15:00, DTC-825, 1 hour.

**Scope note:** Chapter 5 / IAM theory is **not** on the midterm. Week 5 Bash **is** — command substitution `$( )`, heredocs, and the `if` statements in the CLI lab scripts. See [`week_05_quiz.md`](week_05_quiz.md) and the expanded Week 5 study guide.

---

## 1. Core concepts by module

### Cloud fundamentals (Week 1)

| Idea | Exam line |
| ---- | --------- |
| NIST cloud | On-demand access to a **shared pool**, rapidly provisioned and released |
| Deployment | Public / private / community / **hybrid** (on-prem + AWS). On-prem ≠ private cloud |
| Service | IaaS (EC2) → PaaS (Vercel) → SaaS (Google Docs). Most AWS = IaaS |
| Region vs AZ | Region = geography (`us-west-2`); AZ = isolated DCs inside it (`us-west-2a`). ≥ 3 AZs/region |
| Multitenancy | Shared hardware, logical isolation (IAM, virt, net isolation, encryption) |
| IaC | Declare **desired state** (Terraform/OpenTofu later); CLI scripts are the first step |
| Workstation | Debian; WSL → stay off `/mnt/c`; `cd`; `explorer.exe .`; optional systemd in `/etc/wsl.conf` |

Course region: **`us-west-2`**. Accounts: AWS + **Sourcehut**. Eval: 15 / 15 / 30 / 40.

### IAM (Week 2) — not on this midterm

Skip for the midterm. Kept here for the final exam later.

- AuthN = who; AuthZ = what. Root = account email; lock it (password, MFA, **delete root access keys**), daily admin = IAM user + **`AdministratorAccess`**. Root-only example: **close the account**.
- Identities: user (person), group (shared policies — scales), role (assumed by a trusted entity).
- Credentials: console password + MFA; access keys (no MFA, secret **once**); SSH key pair (private **once**).
- Role = **trust policy** (`sts:AssumeRole`, e.g. `ec2.amazonaws.com`) + **permissions policy**. EC2→S3: role, not keys on disk.
- KMS CMKs; EBS encrypted **at create**; SSE-S3 vs SSE-KMS; client-side if data must be encrypted before it leaves the office.
- Credential report = CSV. Artifact = PCI DSS / SOC / FedRAMP docs.

### Compute (Week 3)

| Piece | Remember |
| ----- | -------- |
| AMI | Region-specific boot template. Course: official Debian, owner `136693071363`, user **`admin`** |
| Instance type | Family letter: T/M general, C compute, R/X memory, P/G GPU, H/I/D storage |
| EBS vs instance store | Persistent vs ephemeral; instance store faster, no encrypt, dies on stop |
| Pricing | On-Demand (no commit) / Reserved (1–3 yr **billing** discount) / Spot (cheap, **2 min** reclaim) |
| Elastic IP | Static public IPv4 on the **account**; remap to hide failure; unused = billed |
| Isolation | Dedicated instance = your hardware; dedicated host = placement + socket licences |

cloud-init: first line `#cloud-config`. Lab keys: `users` / `packages` / `write_files` (`"0644"`, `content: \|`) / `runcmd`. Debug: `cloud-init status --long`. Test: `curl http://<ip>`. Host-key clash: `ssh-keygen -R <host>`.

### VPC (Week 4)

- VPC = regional isolated network. Default VPC every region: **`172.31.0.0/16`**. Custom lab: `10.0.0.0/16`.
- CIDR: `/16`–`/28`. RFC 1918. Forbidden: `0.0.0.0/8`, `127.0.0.0/8`, `169.254.0.0/16`, `224.0.0.0/4`.
- Subnet = **one AZ**, subset of VPC CIDR. AWS reserves **5** addresses (`/24` → 251 usable).
- Public subnet = IGW + `0.0.0.0/0 → IGW` + instance public IP.
- Lab trick: IGW route on the **main** RT (`sub-pb` has no explicit association); `sub-pr` associated with `bcit-demo-rt` (local only).
- SG: instance, deny inbound default, **stateful**. NACL: subnet, allow-all default, **stateless**, cannot filter same-subnet traffic.
- Peering = two VPCs, no overlap. VPN = over internet (VGW ↔ CGW). Direct Connect = dedicated private link.

### CLI + Bash (Week 5) — high yield for the midterm

- CLI **v2** from the official installer; `aws login` (or `--remote` in a VM); not root; `us-west-2`.
- Anatomy: `aws <service> <operation> [options]`. `--output json|yaml|text|table`. `--query` = **JMESPath**.
- `fileb://` for key material; `file://` for cloud-init YAML.
- Strict mode `set -euo pipefail`; `err` → stderr.

**Command substitution** — capture stdout into a variable (AMI ID, instance ID, public IP):

```bash
debian_ami=$(aws ec2 describe-images … --query 'sort_by(Images, &CreationDate)[-1].ImageId' --output text)
```

`--output text` so the variable is a bare ID, not JSON quotes.

**Heredoc** — write a `KEY=value` file the next script can `source`. Unquoted `EOF` **expands** variables; `<<'EOF'` does not (wrong for these labs):

```bash
cat > instance_data <<EOF
instance_id=$instance_id
public_ip=$public_ip
security_group_id=$security_group_id
EOF
```

**`if` in the lab scripts** — true when the command exits 0:

| `if` | Then-branch when |
| ---- | ---------------- |
| `[[ $# -ne 1 ]]` | You did not pass exactly one argument |
| `[[ ! -f "$1" ]]` | Path missing / not a regular file |
| `aws ec2 describe-key-pairs --key-names "$key_name" &>/dev/null` | Key **already exists** (CLI success). Missing key → non-zero → skip `then` and import. `set -e` does not abort `if` tests |
| `[[ ! -f "infrastructure_data" ]]` | You have not run `create-vpc` yet |
| `[[ -z "$az" \|\| "$az" == "None" ]]` | Empty, or AWS printed `None` |

GitLab `aws-cli-exercise-start`: `create-vpc` heredoc → `infrastructure_data`; you complete `run-instances` / public IP (`$( )`) / heredoc `instance_data`. Key name **`bcitkey`**.

### Storage (Week 7)

| | S3 | EBS | EFS |
| - | -- | --- | --- |
| Type | Object | Block | Shared file (NFS) |
| Scope | Multi-AZ (most classes) | One AZ | Regional (multi-AZ) |
| Durability | 11 nines | 0.1–0.2% AFR | 11 nines |
| Concurrent clients | Any principal you allow | One instance (except io2 Multi-Attach, same AZ) | Many EC2 + on-prem Linux |

S3 classes (cold → cheaper, slower/costlier retrieve): Standard → Intelligent-Tiering → Standard-IA → One Zone-IA → Glacier Instant / Flexible / Deep Archive. Express One Zone = sub-ms, single AZ.

EBS types: gp2/gp3 (boot), io1/io2 (mission-critical DB), st1 (throughput HDD), sc1 (cold HDD). Elastic Volumes = change size/type live. Snapshots = incremental. Encryption AES-256/KMS at create.

EFS: NFS 2049, mount targets, access points (per-app root + POSIX), lifecycle IA/Archive.

CLI labs: EFS on **default VPC**; S3 `s3` vs `s3api`; `LocationConstraint=us-west-2`; `s3 sync`; `s3 rb --force`; submit S3 scripts to **Sourcehut**.

---

## 2. Architectural patterns (high yield)

```
Internet
   │
   ▼
 IGW ── public subnet (AZ-a) ── EC2 web  (+ SG :80, :22)
   │
   └── private subnet (AZ-b) ── EC2/db  (SG :3306 from web SG only; no 0.0.0.0/0)

Shared files across the web fleet     → EFS (mount targets + NFS SG)
User uploads / backups / static assets → S3 (block public access; lifecycle)
Boot + database disks                 → EBS gp3 / io2
EC2 talking to S3                     → IAM instance role, not access keys
Rebuildable servers                   → AMI + cloud-init (cattle, not pets)
HA inside a region                    → copies in ≥ 2 AZs
```

Three "why can't I reach it?" checks, in order: **SG inbound** → **public IP** → **IGW route**.

---

## 3. Command sheet

```bash
# Auth / environment
aws login                          # IAM user; --remote inside a VM
aws --version                      # must be 2.x
ssh-keygen -f ~/.ssh/aws -C "aws lab key"
ssh -i ~/.ssh/aws admin@<ip>
ssh-keygen -R <host>
cloud-init status --long
curl http://<ip>
explorer.exe .
# /etc/wsl.conf → [boot] systemd=true

# EC2 / keys / AMI
aws ec2 describe-key-pairs --query 'KeyPairs | sort_by(@, &CreateTime) | [-1].KeyName' --output text
aws ec2 import-key-pair --key-name bcitkey --public-key-material fileb://~/.ssh/aws.pub
aws ec2 describe-images --owners 136693071363 \
  --filters "Name=name,Values=debian-13-amd64-*" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' --output text
aws ec2 run-instances --image-id "$ami" --instance-type t3.micro --key-name bcitkey \
  --subnet-id "$subnet" --security-group-ids "$sg" --user-data file://cloud-init.yaml \
  --query 'Instances[0].InstanceId' --output text
aws ec2 wait instance-running --instance-ids "$id"
aws ec2 describe-instances --instance-ids "$id" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text

# Command substitution + heredoc (Week 5 exercise / create-instance)
debian_ami=$(aws ec2 describe-images … --query 'sort_by(Images, &CreationDate)[-1].ImageId' --output text)
instance_id=$(aws ec2 run-instances … --query 'Instances[0].InstanceId' --output text)
public_ip=$(aws ec2 describe-instances … --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
cat > instance_data <<EOF
instance_id=$instance_id
public_ip=$public_ip
security_group_id=$security_group_id
EOF
# unquoted EOF expands $vars; <<'EOF' would write the dollar signs literally
source ./infrastructure_data   # later script loads KEY=value lines as variables

# Lab ifs (true = exit 0)
# [[ $# -ne 1 ]]                         → not exactly one argument
# [[ ! -f "$1" ]]                        → path is not a regular file
# aws ec2 describe-key-pairs … &>/dev/null → key already exists (success)
# [[ ! -f "infrastructure_data" ]]       → forgot create-vpc
# [[ -z "$az" || "$az" == "None" ]]      → empty / no AZ
# set -e does NOT abort a command used as an if condition

# VPC (public subnet)
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 modify-vpc-attribute --vpc-id "$vpc" --enable-dns-hostnames
aws ec2 modify-subnet-attribute --subnet-id "$sub" --map-public-ip-on-launch
aws ec2 create-route --route-table-id "$rt" --destination-cidr-block 0.0.0.0/0 --gateway-id "$igw"

# EFS
aws efs create-file-system --encrypted --performance-mode generalPurpose --throughput-mode bursting
aws efs create-mount-target --file-system-id "$fs" --subnet-id "$sub" --security-groups "$efs_sg"
# NFS SG: TCP 2049 from the EC2 SG, not 0.0.0.0/0
# DNS: ${EFS_ID}.efs.us-west-2.amazonaws.com

# S3
aws s3api create-bucket --bucket "$b" --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2
aws s3api head-bucket --bucket "$b"
aws s3 sync ./dir "s3://$b/backups/"
aws s3 sync "s3://$b/backups/" ./restore
aws s3api list-objects-v2 --bucket "$b" --prefix backups/ --output json
aws s3 rb "s3://$b" --force
```

Bash patterns: `set -euo pipefail`; `$(cmd)` substitution; `cat > file <<EOF … EOF`; `source ./data_file`.

---

## 4. High-yield trap list

1. Debian user is **`admin`**, not `ec2-user`.
2. `/mnt/c` + SSH keys = permission denied.
3. `#cloud-config` missing → YAML never runs; failures are usually indentation.
4. Auto-assigned public IP **changes on stop/start**; Elastic IP does not.
5. Unused Elastic IPs still bill.
6. SG default inbound = **deny**; NACL default = **allow**.
7. NACL cannot stop two instances in the **same subnet** from talking.
8. Overlapping CIDRs block peering.
9. Distro `aws` package is often v1.
10. Pass `.pub` to `import-key-pair`, never the private key.
11. `file://` vs `fileb://` mix-up.
12. `us-west-2` create-bucket needs **LocationConstraint**.
13. EFS filesystem must be **available** before a mount target.
14. NFS **2049** from the instance SG, not the internet.
15. EBS encryption is not a post-create toggle.
16. Multi-Attach ≠ EFS, and it does not span AZs.
17. Glacier Deep Archive is not "immediate."
18. One Zone-IA / Express One Zone are **not** multi-AZ.
19. `bcitkey` is reused in the EFS lab — do not rename it.
20. Clean up: instances, EFS, extra SGs (not Default), buckets, EIPs.

---

## 5. Mock exam (25 questions)

One best answer unless the prompt says otherwise. Do the whole set before the key.

For **this midterm**, skip **3, 15, 21** (Chapter 5 / IAM). Still do **8, 12, 13** and anything with `$( )` / heredocs / `if`.

**1.** Which service model matches "you manage the OS, runtime, and application on a rented VM"?

- A) SaaS
- B) PaaS
- C) IaaS
- D) Community cloud

**2.** `us-west-2b` is a(n) ________ inside region ________. A VPC you create lives at which of those two levels?

**3.** An IAM role's trust policy contains `"Action": "sts:AssumeRole"` and `"Principal": { "Service": "ec2.amazonaws.com" }`. What does this allow, and what does it **not** grant by itself?

**4.** Which pricing model is a 3-year **billing discount** automatically applied to matching running instances, not a reservation of a particular host?

- A) Spot
- B) On-Demand
- C) Dedicated host
- D) Reserved

**5.** You need persistent, encryptable disks for a PostgreSQL data directory on one EC2 instance. Choose the storage service and a volume type, and say why instance store is wrong.

**6.** How many usable IPs does subnet `10.0.3.0/28` have in AWS?

- A) 16
- B) 14
- C) 11
- D) 6

**7.** Which pair is correct?

- A) SG = subnet / NACL = instance
- B) SG = stateful instance firewall / NACL = stateless subnet firewall
- C) Both are stateful
- D) Both default to deny inbound

**8.** Read the query. What is printed?

```bash
aws ec2 describe-key-pairs \
  --query 'KeyPairs | sort_by(@, &CreateTime) | [0].KeyName' \
  --output text
```

**9.** Why is this launch still unreachable from the internet?

- Subnet route: `0.0.0.0/0 → igw`
- SG: TCP 22 from `0.0.0.0/0`
- Instance: private IP only

**10.** A clinic archives MRI files after 30 days. Retrieval must be **immediate**. Cheapest fitting S3 class?

- A) S3 Standard
- B) S3 Glacier Flexible Retrieval
- C) S3 Glacier Instant Retrieval
- D) S3 Glacier Deep Archive

**11.** Two Debian instances in **different AZs** must append to the same log files. Which storage, and why not io2 Multi-Attach?

**12.** Complete:

```yaml
#________

packages:
  - nginx

write_files:
  - path: /var/www/html/index.html
    permissions: ______
    content: __
      <h1>ok</h1>
```

**13.** `create-bucket` in this course region. Fill the missing flag family.

```bash
aws s3api create-bucket --bucket my-bucket --region us-west-2 \
  --____________________________________
```

**14.** Which inbound rule belongs on the **EFS** security group in the GitLab lab?

- A) TCP 22 from `0.0.0.0/0`
- B) TCP 80 from `0.0.0.0/0`
- C) TCP 2049 from the EC2 security group
- D) TCP 2049 from `0.0.0.0/0`

**15.** Name two root-lockdown steps and the managed policy on the replacement daily-admin IAM user.

**16.** A company must keep data **on-premises** but wants the S3 API. Which S3 option?

- A) S3 One Zone-IA
- B) S3 Transfer Acceleration
- C) S3 on Outposts
- D) Directory buckets in a commercial Region

**17.** True or false? Justify: "If the servers are in our building, we have a private cloud."

**18.** You stop and start an instance that had an auto-assigned public IPv4. SSH to the old address times out. Why, and what address type would have survived?

**19.** Write the `s3 sync` backup line from the GitLab lab (`$source_dir` → bucket prefix `backups/`).

**20.** Which EBS feature lets you grow a gp2 volume and convert it to gp3 **without stopping** the instance?

- A) Multi-Attach
- B) Instance store
- C) Elastic Volumes
- D) Snapshot lock

**21.** Federation in Chapter 5 is mainly about:

- A) Copying AMIs between regions
- B) Signing in with an existing identity system (SAML/AD) instead of new IAM users
- C) Peering two VPCs
- D) Encrypting EBS

**22.** The Week 4 private instance SG allows ICMP from anywhere. From the public instance, ping works and SSH does not. State the missing rule with a **restricted** source.

**23.** Why does the EFS `create-efs` script poll for up to 30 attempts before writing `efs_data` and exiting 0?

**24.** Pick the class: frequent, low-latency, multi-AZ object storage for a dynamic website.

- A) S3 Standard
- B) S3 One Zone-IA
- C) sc1
- D) EFS Archive

**25.** Scenario (write a short architecture). Public web app, PostgreSQL that must not be on the internet, shared user-upload directory across three web nodes in two AZs, static images on a CDN-friendly store, web nodes need to read those images without long-lived keys. Name VPC placement, three storage services, and the IAM mechanism.

---

## Mock exam answer key

**1. C.** EC2 is the course IaaS example. PaaS = you bring code; SaaS = you just use the app.

**2.** Availability Zone; `us-west-2`. VPC = **region** level; subnets = AZ level.

**3.** Allows the **EC2 service** to assume the role (instances with that role get temporary creds). It grants **no S3 (or other) permissions** — those come from the separate permissions policy.

**4. D.** Spot can vanish in two minutes. Dedicated host is about placement/licences.

**5.** **EBS io2** (or io1) if you need provisioned IOPS; **gp3** if "good enough" general DB. Instance store is ephemeral and unencrypted — a stop loses the database.

**6. C.** 16 − 5 reserved = 11.

**7. B.** SG deny-inbound default; NACL allow-all default. Option D is therefore false.

**8.** Name of the **oldest** key pair (`[0]` after ascending `CreateTime`). Newest would be `[-1]`.

**9.** Missing a **public IP** (auto-assign or Elastic IP). IGW + default route are not enough.

**10. C.** Millisecond archive; notes cite medical imaging. Deep Archive is 12–48 h. Flexible Retrieval is minutes–hours.

**11.** **EFS** (regional, NFS, many clients, multi-AZ). Multi-Attach is same-AZ only and is block storage that the app must cluster-lock.

**12.** First line `#cloud-config`. `permissions: "0644"` (quoted). `content: |` (literal block).

**13.** `--create-bucket-configuration LocationConstraint=us-west-2` (required outside `us-east-1`).

**14. C.** 22/80 belong on the **EC2** SG. Opening 2049 to the world is the classic lab mistake.

**15.** Any two of: strong password, MFA, delete root access keys, stop using root daily. Policy: **`AdministratorAccess`**.

**16. C.** Outposts keeps objects on the on-prem rack with the S3 API.

**17.** **False.** On-premises only means you run local infrastructure. Private cloud = dedicated cloud-style pool for one org; it might even be hosted off-site.

**18.** Auto-assigned public IPv4 is released on stop. Use an **Elastic IP** if the address must stick (and release it later so you are not billed).

**19.**

```bash
aws s3 sync "$source_dir" "s3://$BUCKET_NAME/backups/" --region "$AWS_REGION"
```

**20. C.** Elastic Volumes change size, IOPS, and type live. Multi-Attach is sharing io2, not resizing.

**21. B.** SAML 2.0 / AD / IAM Identity Center. Not AMI copy, peering, or KMS.

**22.** Inbound **TCP 22** on the private SG, source = `10.0.1.0/24` or the public instance's SG. Then SSH via jump host; do not use `0.0.0.0/0` on the private node.

**23.** A mount target cannot be created until the filesystem **LifeCycleState is `available`**. The loop is that wait (error/timeout if it never becomes available).

**24. A.** Standard is the default frequent-access multi-AZ class. One Zone-IA is cheap infrequent single-AZ. sc1 is cold **EBS HDD**.

**25.** Public subnets (two AZs) + IGW for web EC2; PostgreSQL in **private** subnets, SG from web SG only. Shared uploads → **EFS**. Images → **S3** (block public access unless a deliberate CloudFront/public-read design). DB/boot → **EBS**. Web instances get an **IAM role** with `s3:GetObject` on that bucket; no access keys on disk.
