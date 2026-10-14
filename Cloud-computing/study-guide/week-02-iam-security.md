# Week 2 — Securing Your AWS Account with IAM

## Learning Objectives

By the end of this week you should be able to:

1. **Lock down an AWS account**: protect the root user and replace it with an IAM admin user for daily work.
2. **Choose the right IAM identity** (user, group, or role) for a person, a team, or an application, applying the *principle of least privilege*.
3. **Explain the supporting security tools**: authentication methods, KMS encryption, credential reports, and AWS Artifact.

---

## Key Concepts & Deep Dive

### 1. Authentication vs. authorization

`chapter 5` frames IAM around two questions:

- **Authentication** — *Who are you?* (getting past the wall)
- **Authorization** — *What are you allowed to do?* (what you can touch once inside)

IAM = **I**dentity and **A**ccess **M**anagement handles both.

### 2. Protect the root user first

The **root user** is the identity created with your AWS account (your email + password). It can do *anything*, including launching resources in every region and authorizing unlimited spending. If it's compromised, an attacker could delete your data or run up huge bills (the chapter's example: a rogue crypto-mining operation).

Root lockdown checklist:

- [ ] Strong, randomly generated password (use a password manager)
- [ ] **MFA enabled**
- [ ] **Delete all root access keys**
- [ ] Stop using root for day-to-day work — create an IAM admin user instead

The 6.1 lesson video makes the same point: even an IAM user with `AdministratorAccess` can't do a few root-only tasks, **like closing the account** — which is why root still exists, but should be locked away.

### 3. The three ways to authenticate

| Credential | Used for | Key facts |
| ---------- | -------- | --------- |
| **Password** (+ MFA) | AWS Management Console | Enforce complexity with an account-wide **password policy** (min length, upper/lower, number, symbol) |
| **Access keys** (Access Key ID + Secret Access Key) | CLI and programmatic/API access | **No MFA option**; the secret is shown **only once**; never email or commit it |
| **SSH key pair** | Logging in to EC2 Linux instances | AWS keeps the public key; you keep the private key. Downloaded only once |

**MFA** = something you *know* (password) + something you *have* (an authenticator app or a YubiKey-style device producing a short-lived code).

An SSH login from the chapter:

```bash
ssh -i keyname.pem ec2-user@<public_ip_address_of_instance>
```

> Note: `ec2-user` is the default user on **Amazon Linux**. On the **Debian** AMIs this course uses, it's `admin` (see `aws-ec2.md`, Week 3).

### 4. Users, groups, and roles

```
           ┌─────────────┐   attach policies   ┌──────────────────────┐
 People →  │  IAM User   │ ◄────────────────── │  Policies             │
           └─────┬───────┘                     │  (AWS managed or      │
                 │ member of                   │   customer managed)   │
           ┌─────▼───────┐ ◄────────────────── │                       │
           │  IAM Group  │                     │                       │
           └─────────────┘                     │                       │
 Apps /    ┌─────────────┐ ◄────────────────── │                       │
 services →│  IAM Role   │  assumed by a       └──────────────────────┘
           └─────────────┘  trusted entity
```

- **IAM user** — an individual identity (usually a person). Exercise 5.2 creates "Steve" with only `AmazonEC2FullAccess`.
- **IAM group** — a collection of users that share permissions (e.g. `EC2-admins`, `S3-admins`). Add a new hire to the group and they inherit everything; change the group and every member updates. **This is the most efficient way to manage many users.**
- **IAM role** — permissions that a **trusted entity** can *assume*. Roles are mainly for **applications and services**, not people. Trusted entities include:
  - an AWS service (e.g. an **EC2 instance**)
  - a **federated identity** (e.g. Google sign-in, Amazon Cognito)
  - another AWS account

**Least privilege**: give each identity only the permissions it needs. The 6.1 video shows this in practice — it opens the **Policies** page, where AWS-managed and customer-managed policies are listed, to show that not everyone needs admin.

To replace root for daily administration, the right managed policy is **`AdministratorAccess`**.

### 5. Roles in action — the lesson 6.2 scenario

The 6.2 video sets up a very common real-world pattern:

> "We have an application running on EC2, and we need to grant access to that application to be able to work with an S3 bucket."

The **wrong** way: put access keys in a config file on the server (they can leak, and they never expire on their own).

The **right** way: create an **IAM role** whose trusted entity is EC2, attach a policy granting access to the bucket, and attach the role to the instance. The app then gets temporary credentials automatically.

For reference (this goes a little beyond the chapter), a role has two parts:

**Trust policy** — *who* can assume the role:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ec2.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

**Permissions policy** — *what* the role can do (least privilege: one bucket only):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject"],
    "Resource": "arn:aws:s3:::example-demo-bucket/*"
  }]
}
```

### 6. Federation

**Federation** lets users sign in with an *existing* identity system instead of new IAM users:

- **SAML 2.0** and **Microsoft Active Directory** are the standards named in the chapter (enabling single sign-on, SSO).
- **AWS Single Sign-On** (now IAM Identity Center) handles federated access; **AWS Microsoft AD** handles AD-based workloads like SharePoint and SQL Server.

### 7. Monitoring, encryption, and compliance

- **Credential report** — a downloadable **CSV** listing every IAM user: last login, whether MFA is on, active access keys, and when keys were last rotated. Download it regularly.
- **AWS KMS (Key Management Service)** — manages encryption keys using a **customer master key (CMK)**. It works with EBS, RDS, DynamoDB, and S3.
  - EBS volumes are encrypted **when created** (you can't simply flip encryption on for an existing volume).
  - S3 server-side options: **SSE-S3** (S3-managed keys) or **SSE-KMS** (KMS-managed keys).
  - To protect data **in transit from your office**, use **client-side encryption** (encrypt before uploading, with a KMS CMK or a client-side master key).
- **AWS Artifact** — downloadable compliance documents ("artifacts"): **PCI DSS** (credit cards), **SOC 1/2/3** reports (helpful for Sarbanes–Oxley), FedRAMP, the Government of Canada Partner Package, and more.

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `chapter 5` | The full chapter: root protection, Exercises 5.1–5.3 (password policy, IAM user, IAM group), roles, federation, KMS, Artifact, and ~20 review questions at the end |
| `transcripts/6.1 Create IAM users [1_anp33394]/transcript.md` | Why to stop using root; creating an admin user; browsing AWS-managed vs customer-managed policies |
| `transcripts/6.2 Create IAM role with S3 permissions [1_9sl6sq6n]/transcript.md` | What roles are and who can assume them; the EC2 → S3 access scenario |
| `transcripts/*/frames/` | Screenshots of the IAM dashboard (users, groups, roles, policies) |

> The two lesson videos in the repo are only 1-minute clips, so the transcripts cover just the introductions. `chapter 5` is the main source this week.

---

## Practical Takeaways — Why This Matters

- **Leaked credentials are the #1 cloud breach story.** Locking root and never hard-coding access keys prevents most of those disasters.
- **Groups scale; individual permissions don't.** On a real team you'll manage dozens of people — groups keep that sane and auditable.
- **Roles are how AWS services talk to each other securely.** Every later topic (EC2 reading S3, Lambda writing to a database) relies on roles.
- **You'll use your IAM user for the CLI in Week 5.** `aws login` authenticates as the IAM user you create now, so set it up correctly.

---

## Knowledge Check

**Q1 (Multiple choice).** What is the *most efficient* way to manage permissions for a team of 15 people who all need the same S3 access?

- A) Attach the S3 policy to each IAM user individually
- B) Create an IAM role and give each person its password
- C) Put the users in an IAM group with the S3 policy attached
- D) Share the root user's credentials with the team

**Q2 (Multiple choice).** Which of the following best describes an IAM role?

- A) A set of IAM users who share a password
- B) Permissions that a trusted entity (like an EC2 instance) can assume
- C) A second account that backs up the root user
- D) A CSV report of user activity

**Q3 (Fill in the blank).** A developer needs to run AWS CLI commands from their laptop using long-term credentials. They need an ________ and a ________. Unlike console logins, this type of credential has no ________ option, and the secret part is shown only ________.

**Q4 (Code reading).** Break down this command piece by piece. What is each part, and would it work on a Debian EC2 instance?

```bash
ssh -i mykey.pem ec2-user@54.7.35.103
```

**Q5 (Scenario).** A Python application running on an EC2 instance needs to upload reports to a single S3 bucket. A teammate suggests pasting your access keys into the app's config file. What should you do instead, which IAM component would you create, and how would you apply least privilege?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

**Q1 — C) An IAM group.** Attach the policy once to the group; members inherit it and future changes apply to everyone. Option A works but doesn't scale. Option B misunderstands roles (they aren't shared logins). Option D is the worst possible security practice.

**Q2 — B).** A role defines permissions that a **trusted entity** — an AWS service, a federated identity, or another account — can assume. It's mainly for applications and services rather than people.

**Q3** — **access key ID**; **secret access key**; **MFA**; **once** (at creation — download or copy it immediately).

**Q4** —
- `ssh` — the Secure Shell client
- `-i mykey.pem` — the private key file (identity) to authenticate with
- `ec2-user` — the login username
- `@54.7.35.103` — the instance's public IP address

It works on **Amazon Linux**, whose default user is `ec2-user`. On a **Debian** AMI the default user is **`admin`**, so you'd use `ssh -i mykey.pem admin@54.7.35.103`.

**Q5** — Don't put access keys on the server. Create an **IAM role** with **EC2 as the trusted entity**, attach a **permissions policy** that allows only the needed actions (e.g. `s3:PutObject`) on **only that bucket**, and attach the role to the instance. The application then receives temporary credentials automatically, so there are no long-lived keys to leak. This is exactly the scenario from lesson 6.2.

</details>
