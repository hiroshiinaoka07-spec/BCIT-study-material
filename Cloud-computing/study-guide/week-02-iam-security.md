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

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** In IAM, which question does **authorization** answer?

- A) Who are you?
- B) Which region are you working in?
- C) What are you allowed to do?
- D) How long is your password?

**2.** Even an IAM user with `AdministratorAccess` cannot do a few root-only tasks. Which example does the 6.1 lesson video give?

- A) Closing the AWS account
- B) Creating IAM groups
- C) Attaching policies to users
- D) Launching EC2 instances

**3.** Which statement about the **SSH key pair** used to log in to EC2 Linux instances is correct?

- A) AWS keeps both keys, so you can download the private key again at any time
- B) It is used to sign in to the AWS Management Console
- C) It is the same thing as an access key ID and secret access key
- D) AWS keeps the public key, you keep the private key, and you can download it only once

**4.** What is the AWS **root user**?

- A) The first IAM user you create and give `AdministratorAccess`
- B) The identity created with your AWS account (your email and password), which can do anything
- C) A role that EC2 instances assume
- D) The default Linux user on Amazon Linux instances

**5.** **MFA** combines which two factors?

- A) Two different passwords
- B) Something you know (a password) and something you have (an authenticator app or YubiKey-style device)
- C) An access key ID and a secret access key
- D) A public key and a private key

**6.** Read this role policy. What does it control?

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

- A) It gives EC2 instances full access to S3
- B) It lets any IAM user in the account assume the role
- C) It lets the role launch new EC2 instances
- D) It is a trust policy that allows the EC2 service to assume the role

**7.** A role has this permissions policy attached. Which action does it allow?

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

- A) Uploading a file to `example-demo-bucket`
- B) Deleting objects in `example-demo-bucket`
- C) Reading objects from any bucket in the account
- D) Creating a new S3 bucket

**8.** You are creating an IAM admin user to replace the root user for daily administration. Which managed policy should you attach?

- A) `AmazonEC2FullAccess`
- B) `AmazonS3FullAccess`
- C) `AdministratorAccess`
- D) `ReadOnlyAccess`

**9.** You want S3 to encrypt objects on the server side using keys managed by AWS KMS. Which option is this?

- A) SSE-S3
- B) Client-side encryption
- C) A credential report
- D) SSE-KMS

**10.** You want every IAM user's console password to require a minimum length plus uppercase, lowercase, a number, and a symbol. What should you configure?

- A) An account-wide password policy
- B) MFA on the root user
- C) A credential report
- D) A KMS customer master key

**11.** An auditor asks you to encrypt an EBS volume that was created without encryption. Which statement matches the guide?

- A) You can switch on an encryption setting for the existing volume with no other changes
- B) You apply SSE-S3 to the volume
- C) EBS volumes are encrypted when they are created, so you can't simply flip encryption on for an existing volume
- D) EBS volumes cannot be encrypted at all

**12.** A company wants employees to sign in to AWS with their existing Microsoft Active Directory accounts instead of creating new IAM users. What should it use?

- A) One IAM group per department, with a new IAM user for every employee
- B) Federation (for example SAML 2.0 / Active Directory) through AWS Single Sign-On (IAM Identity Center)
- C) The root user's credentials, shared through a password manager
- D) Separate access keys for each employee

**13.** Your office uploads sensitive files to S3, and the data must be protected **while in transit from the office**. Which approach does the guide recommend?

- A) Client-side encryption — encrypt the data before uploading, using a KMS CMK or a client-side master key
- B) SSE-S3
- C) SSE-KMS alone
- D) Downloading a credential report after each upload

**14.** During a security review you need to find which IAM users have no MFA and which have access keys that haven't been rotated in a long time. What is the quickest tool?

- A) AWS Artifact
- B) The IAM **Policies** page
- C) An IAM role's trust policy
- D) The IAM credential report

**15.** Your company processes credit card payments, and an auditor wants AWS's **PCI DSS** compliance documentation. Where do you get it?

- A) AWS KMS
- B) The IAM credential report
- C) AWS Artifact
- D) AWS Single Sign-On

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **C.** Authorization is *what are you allowed to do* once inside. Option A, "Who are you?", is authentication.
2. **A.** The 6.1 video points out that closing the account is a root-only task, which is why root still exists but should be locked away. Admin users can do the other three.
3. **D.** AWS keeps the public key and you keep the private key, which can be downloaded only once. Option A is the tempting mistake — if you lose the private key, AWS can't give it back.
4. **B.** The root user is created with the account and can do anything, including authorizing unlimited spending. Option A describes the IAM admin user you create to *replace* root for daily work.
5. **B.** MFA is something you **know** plus something you **have**. Option C is the two parts of an access key, which has no MFA option.
6. **D.** A `Principal` plus `sts:AssumeRole` makes this a **trust policy**: it defines *who* can assume the role (the EC2 service). It grants no S3 permissions itself, so option A is wrong — that's the job of the permissions policy.
7. **A.** `s3:PutObject` on `example-demo-bucket/*` allows uploads to that bucket. Option C is wrong because the `Resource` limits access to one bucket only, and deleting (B) isn't in the action list.
8. **C.** The guide names `AdministratorAccess` as the policy for replacing root in daily administration. `AmazonEC2FullAccess` (option A) is what the limited user "Steve" gets in Exercise 5.2.
9. **D.** SSE-KMS uses KMS-managed keys. SSE-S3 (option A) is server-side encryption with S3-managed keys.
10. **A.** Complexity rules are enforced with an account-wide **password policy**. MFA (option B) adds a second factor but doesn't control password complexity.
11. **C.** The guide states that EBS volumes are encrypted **when created**. Option D is wrong — EBS does support encryption; it just has to be chosen at creation.
12. **B.** Federation lets users sign in with an existing identity system; SAML 2.0 and Active Directory are the standards the guide names. Option A works but ignores the existing directory and creates many new identities to manage.
13. **A.** For data in transit from the office, the guide recommends **client-side encryption** before upload. SSE-S3 and SSE-KMS (options B and C) encrypt on the server side, after the data arrives.
14. **D.** The credential report is a CSV showing each user's last login, MFA status, active access keys, and key rotation dates. AWS Artifact (option A) is for compliance documents, not user activity.
15. **C.** AWS Artifact provides downloadable compliance documents such as PCI DSS and SOC reports. KMS (option A) manages encryption keys.

</details>
