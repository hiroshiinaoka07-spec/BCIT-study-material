# Week 2 Quiz — IAM & Account Security

Sources: `chapter 5`, transcripts `6.1 Create IAM users`, `6.2 Create IAM role with S3 permissions`.

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** Authentication answers which question?

- A) What are you allowed to do?
- B) Who are you?
- C) Which region should you use?
- D) How is data encrypted at rest?

**2.** Which root-user lockdown step is **not** on the course checklist?

- A) Strong randomly generated password
- B) MFA enabled
- C) Delete all root access keys
- D) Share the root password with the IAM admin via a password manager

**3.** Why do access keys have no MFA option?

- A) They are only used by the root user
- B) They authenticate programmatic/CLI access with a key ID + secret, not an interactive login
- C) MFA is built into the secret access key
- D) SSH key pairs already provide MFA

**4.** The most efficient way to give 20 developers the same S3 permissions is to:

- A) Attach the policy to each user
- B) Put them in an IAM group and attach the policy to the group
- C) Create 20 IAM roles, one per person
- D) Use the root user

**5.** AWS Artifact is used to:

- A) Rotate access keys
- B) Encrypt EBS volumes after they are created
- C) Download compliance documents such as PCI DSS and SOC reports
- D) Assume a role from EC2

---

## Short Answer

**6.** Distinguish **IAM user**, **IAM group**, and **IAM role** in one sentence each. Who is a role *for*?

**7.** Name the three authentication methods in Chapter 5, what each is used for, and which secret is shown only once.

**8.** What does a **credential report** contain, what format is it, and when would you download one?

**9.** For data at rest on S3, contrast **SSE-S3**, **SSE-KMS**, and **client-side encryption**. Which one is required if data must be encrypted *before it leaves your office*?

---

## Hands-on / Scenario

**10.** Break down this command. Would it work on the Debian AMIs this course uses? If not, fix it.

```bash
ssh -i ~/.ssh/aws.pem ec2-user@54.188.10.22
```

**11.** A teammate wants to put your access key ID and secret into `/opt/app/config.yml` on an EC2 instance so the app can write to one S3 bucket. Using lesson 6.2, describe the correct IAM design. Include the two policies a role needs and a least-privilege `Resource`.

**12.** You are creating the IAM admin that replaces root for daily work. Which managed policy do you attach, and which root-only task does the 6.1 video say even that admin still cannot do?

---

## Answer Key

**1. B.** Authentication = *who are you?*; authorization = *what are you allowed to do?*

**2. D.** Sharing root credentials is the opposite of lockdown. The checklist is: strong password, MFA, delete root access keys, stop using root daily.

**3. B.** Access keys are long-lived ID + secret for CLI/API. There is no interactive MFA step. The secret is shown only at creation.

**4. B.** Groups scale: attach once, members inherit, later changes apply to everyone. Roles are assumed by trusted entities (services, federation, other accounts), not used as shared people-logins.

**5. C.** Artifact hosts compliance "artifacts." Credential reports (A) and KMS (B) are different tools. EBS encryption is chosen at volume creation, not flipped later.

**6.**
- **User** — an identity for a person (or a specific long-lived principal).
- **Group** — a collection of users that share policies.
- **Role** — permissions a **trusted entity can assume**; mainly for applications and AWS services, not daily human logins.

**7.** Password (+ MFA) for the console; access keys for CLI/API (secret shown **once**); SSH key pair for EC2 Linux (private key downloaded **once**; AWS keeps the public key).

**8.** CSV of every IAM user: last login, MFA on/off, active access keys, last key rotation. Download regularly for audits and to find stale keys / users without MFA.

**9.** SSE-S3 = S3-managed keys on the server. SSE-KMS = server-side with a KMS CMK. Client-side = you encrypt before upload (KMS CMK or a client master key). **Client-side** is what the chapter recommends for protecting data in transit from the office.

**10.** `-i` = private key; `ec2-user` = default on **Amazon Linux**; `@54.188.10.22` = public IP. On **Debian** AMIs the user is **`admin`**:

```bash
ssh -i ~/.ssh/aws admin@54.188.10.22
```

(Course keys are typically ed25519 without a `.pem` suffix; the username is the part that is definitely wrong.)

**11.** Do not put long-lived keys on the instance. Create an **IAM role** with:
- **Trust policy**: `Principal: { Service: ec2.amazonaws.com }`, `Action: sts:AssumeRole`.
- **Permissions policy**: e.g. `s3:PutObject` (and `s3:GetObject` if needed) on `arn:aws:s3:::that-bucket/*` only.
Attach the role to the instance. The app receives temporary credentials automatically.

**12.** Attach **`AdministratorAccess`**. Even that user cannot **close the AWS account** — a root-only task, which is why root is locked away rather than deleted.
