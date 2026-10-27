# Week 6 Quiz — In-Class Test Review (Weeks 1–5)

No new flipped reading this week. This set mixes fundamentals, IAM, EC2, VPC, and the CLI.

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** Combining an on-premises data center with AWS is:

- A) Private cloud
- B) Community cloud
- C) Hybrid cloud
- D) IaaS only

**2.** Least privilege is applied when you:

- A) Attach `AdministratorAccess` to every user
- B) Give each identity only the permissions it needs
- C) Share the root user through a password manager
- D) Disable MFA so people can log in faster

**3.** Reserved Instances are:

- A) A specific physical machine reserved for you
- B) A billing discount on matching On-Demand usage, 1- or 3-year term
- C) Unused capacity reclaimed with two minutes' notice
- D) Required in order to use an Elastic IP

**4.** Which firewall is stateful?

- A) NACL
- B) Route table
- C) Security group
- D) Internet gateway

**5.** After `aws login`, you work as:

- A) The AWS account root user
- B) Your IAM user, with short-term credentials under `~/.aws/`
- C) An IAM role named `bcitkey`
- D) A federated Google account by default

---

## Short Answer

**6.** Classify each: EC2, Vercel, Google Docs. Then classify: AWS alone; AWS + your data center.

**7.** Write the trust-policy `Principal` for an EC2 instance role, and one reason you would not paste access keys onto the instance.

**8.** A `/28` subnet in AWS: total addresses, reserved, usable. Why might a tiny subnet still be a bad idea for a public web tier?

**9.** Difference between `file://` and `fileb://`. Which does `--user-data` for cloud-init YAML use, and which does `--public-key-material` use?

---

## Hands-on / Scenario

**10.** You must bootstrap nginx on Debian at launch, then prove it works from your laptop. Write (a) the first line of user data, (b) the SSH command, (c) the curl command, (d) the on-instance debug command.

**11.** Design a two-AZ VPC `10.0.0.0/16` with one public and one private subnet. Give CIDRs, what makes the public subnet public, and where a database should live.

**12.** A classmate's import script dies with "already exists" for `bcitkey`. They want to change `key_name` in the script. Why should they **not**, if they still have to run the Week 7 EFS lab?

---

## Answer Key

**1. C.** AWS is public; plus on-prem = hybrid. On-prem alone is not automatically a private cloud.

**2. B.** Groups are how you apply that efficiently to many people; roles are how services get it.

**3. B.** Not a particular host. Spot is the reclaimable one. Dedicated hosts are for socket-licensed software.

**4. C.** Return traffic is allowed automatically. NACLs need explicit return rules. Route tables and IGWs are not firewalls.

**5. B.** Course warning: never `aws login` as root. Region `us-west-2` in `~/.aws/config`.

**6.** EC2 = IaaS; Vercel = PaaS; Google Docs = SaaS. AWS alone = public; AWS + DC = hybrid.

**7.** `"Principal": { "Service": "ec2.amazonaws.com" }`. Keys on disk leak, do not rotate themselves, and violate least privilege if they are user keys with broad rights.

**8.** 16 total, 5 reserved, **11 usable**. A public web tier that scales will run out of IPs; `/24` is the lab's typical subnet size.

**9.** `file://` = read + normal encoding (cloud-init `--user-data file://cloud-init.yaml`). `fileb://` = raw binary (`--public-key-material fileb://~/.ssh/aws.pub`).

**10.**
- (a) `#cloud-config`
- (b) `ssh -i ~/.ssh/aws admin@<ip>`
- (c) `curl http://<ip>`
- (d) `cloud-init status --long`

**11.** Example: public `10.0.1.0/24` in `us-west-2a`, private `10.0.2.0/24` in `us-west-2b`. Public = IGW + `0.0.0.0/0 → IGW` on that subnet's route table + public IPs. Database in the **private** subnet (no IGW route); SG allows the app SG only, not `0.0.0.0/0`.

**12.** Week 7 `create-ec2` hard-codes `--key-name bcitkey`. Renaming in the import script means the EFS instances cannot SSH with the key they expect. Delete the existing pair in AWS if you need to re-import, or keep the name and skip re-import.
