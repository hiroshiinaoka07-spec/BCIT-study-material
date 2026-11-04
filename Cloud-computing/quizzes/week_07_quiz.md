# Week 7 Quiz — S3, EBS, EFS & Storage CLI Labs

Sources: `chapter10-week7`, `aws-storage-services.md`, [GitLab: aws-cli-efs-exercise](https://gitlab.com/cit_3640/aws-cli-efs-exercise), [GitLab: aws-cli-s3-exercise](https://gitlab.com/cit_3640/aws-cli-s3-exercise).

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** Under the Shared Responsibility Model for storage, **you** own:

- A) Data-center physical security
- B) Hardware that hosts EBS
- C) Encryption settings, IAM/bucket policies, backup policies
- D) Automatic replication of EBS inside its AZ

**2.** Which S3 class is **single-AZ**?

- A) S3 Standard
- B) S3 Standard-IA
- C) S3 Glacier Instant Retrieval
- D) S3 One Zone-IA

**3.** gp3 baseline performance (any size, no extra pay) is:

- A) 256,000 IOPS / 4,000 MB/s
- B) 3,000 IOPS / 125 MiB/s
- C) 80,000 IOPS / 2,000 MiB/s
- D) Depends on volume size, like gp2 burst

**4.** EFS speaks:

- A) iSCSI
- B) NFS 4.0/4.1
- C) SMB only
- D) The S3 REST API

**5.** Multi-Attach is available on:

- A) Any EBS type
- B) gp3
- C) io2 Block Express, instances in the **same AZ**, app must coordinate writes
- D) st1, for data warehouses

---

## Short Answer

**6.** One-line memory hook: S3 vs EBS vs EFS. Then pick a service for (a) a boot volume, (b) a public website's images, (c) three web servers sharing uploads.

**7.** Fill in: S3 durability is ________ nines; max object size is ________ TB; EBS durability is quoted as AFR ________; EFS regional durability is ________ nines.

**8.** When do you pick Intelligent-Tiering vs Standard-IA vs Glacier Instant Retrieval vs Glacier Deep Archive?

**9.** What is an EFS **mount target**, which TCP port must its SG allow, and from whom (lab vs production)?

---

## Hands-on / Scenario

**10.** Put the EFS lab scripts in order and state what each writes to disk. Why does `create-efs` loop on `LifeCycleState` before you are allowed to run the next script?

**11.** The lab `cloud-init` fstab line is:

```text
$EFS_DNS:/  /mnt/efs  nfs4  defaults,_netdev,nfsvers=4.1  0  0
```

What is `$EFS_DNS` in terms of `EFS_ID` and region? What does `_netdev` do? After instance A writes `/mnt/efs/shared.txt`, what must be true on instance B?

**12.** Complete the four S3-lab TODOs. Why does `create-bucket` need `LocationConstraint` in `us-west-2`? Why does `backup-info` require `jq`? How does `delete-bucket` avoid deleting the wrong bucket?

---

## Answer Key

**1. C.** AWS = security *of* the cloud (hardware, replication, facilities). You = security *in* the cloud.

**2. D.** Also single-AZ: S3 Express One Zone. Standard / Standard-IA / Glacier Instant Retrieval are multi-AZ. One Zone-IA availability is 99.5%.

**3. B.** 80k IOPS / 2,000 MiB/s is the gp3 **max you can pay extra for**. 256k / 4,000 MB/s is io2 Block Express.

**4. B.** POSIX shared file system. Many EC2 **and** on-prem Linux clients. iSCSI would be block (that is closer to EBS). S3 is object APIs, not a mount-by-default POSIX FS.

**5. C.** Not gp3/st1. Same-AZ only. EBS will not serialize writers for you.

**6.** *S3 = bucket of objects by key. EBS = a disk for one server. EFS = a network drive for many servers.* (a) EBS gp2/gp3 (b) S3 (c) EFS — not EBS unless io2 Multi-Attach + a cluster-aware app, and that still cannot span AZs.

**7.** 11; 5 TB; 0.1–0.2%; 11.

**8.** Intelligent-Tiering: unknown/changing access; auto-moves across tiers. Standard-IA: you *know* it is infrequent but need millisecond access (retrieval fee). Glacier Instant Retrieval: archive that must open **immediately** (medical imaging). Deep Archive: almost never, 12–48 h, cheapest (long legal hold).

**9.** A mount target is an ENI in a **subnet** that NFS clients connect to. SG ingress **TCP 2049**. Lab: from the **EC2 security group** (`--source-group`), not `0.0.0.0/0`. Production: same idea — NFS only from the instance SG/CIDR that must mount.

**10.** `create-efs` → `efs_data` (`REGION`, `EFS_ID`); `create-mount-target` → `mount_data` (VPC, subnet, both SGs, mount target ID); `create-ec2` → `instance_<id>_data`. AWS will not create a mount target until the filesystem is **available**; the wait loop (up to ~150 s) is that dependency.

**11.** `${EFS_ID}.efs.${REGION}.amazonaws.com`. `_netdev` delays the mount until the network is up. Instance B, launched with the same filesystem/mount target, must see the **same** `shared.txt` — proof that EFS is shared, not local EBS.

**12.**

```bash
# create-bucket
aws s3api create-bucket \
  --bucket "$bucket_name" \
  --region "$region" \
  --create-bucket-configuration LocationConstraint="$region"

# backup
aws s3 sync "$source_dir" "s3://$BUCKET_NAME/backups/" --region "$AWS_REGION"

# backup-info
objects_json=$(aws s3api list-objects-v2 \
  --bucket "$BUCKET_NAME" \
  --prefix "$backup_prefix" \
  --region "$AWS_REGION" \
  --output json)

# backup-restore
aws s3 sync "s3://$BUCKET_NAME/backups/" "$destination_dir" --region "$AWS_REGION"
```

`us-east-1` is the only region that omits `LocationConstraint`; every other region, including **`us-west-2`**, requires it. `list-objects-v2` returns JSON; `jq` counts objects, sums `Size`, and finds `max_by(.LastModified)`. `delete-bucket` makes you **retype the bucket name**, then `aws s3 rb --force` empties and deletes it.
