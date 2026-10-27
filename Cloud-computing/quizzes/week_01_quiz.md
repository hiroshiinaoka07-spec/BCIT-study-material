# Week 1 Quiz — Cloud Fundamentals & Linux Workstation

Sources: `wk01.md`, `linux-environment.md`, `README.md`.

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** An organization runs every workload on AWS and has no on-premises data center. Which deployment model is this?

- A) Hybrid cloud
- B) Private cloud
- C) Public cloud
- D) Community cloud

**2.** Which statement about a **private cloud** is correct?

- A) It must be on-premises
- B) On-premises infrastructure is automatically a private cloud
- C) All resources are dedicated to one organization; it may or may not be on-premises
- D) It is the same thing as combining an on-prem data center with AWS

**3.** Google Docs is an example of which service model?

- A) IaaS
- B) PaaS
- C) SaaS
- D) VPS

**4.** Why does AWS guarantee **at least three Availability Zones** in each region?

- A) So every customer gets a dedicated data center
- B) So you can design applications that survive the failure of one AZ
- C) So CIDR blocks can be larger than `/16`
- D) So the root user can be locked down

**5.** Which of the following is **not** a reason `wk01.md` gives for organizations adopting the cloud?

- A) Flexibility of access and integrated services
- B) Provider security teams
- C) Ability to create resources quickly
- D) Guaranteed lower cost than on-premises for every workload

---

## Short Answer

**6.** Unpack the NIST definition: name the three ideas highlighted in the course notes (on-demand access, shared pool, rapid provision/release) and give a one-line meaning for each.

**7.** In the identifier `ca-central-1a`, what is the region code, what is the AZ, and which of the two does a VPC live in?

**8.** You need a Linux environment for this course. List the three options in `linux-environment.md` and the one WSL rule that, if ignored, causes SSH-key permission errors.

**9.** What three accounts/environments does `wk01.md` say you need this term, and what is the course evaluation breakdown?

---

## Hands-on / Scenario

**10.** Your WSL prompt is:

```text
hiro@laptop:/mnt/c/Users/hiro/BCIT-study-material$
```

You try `chmod 600 ~/.ssh/aws` on a key that actually lives under `/mnt/c/...`, and `ssh -i` still refuses the key. What is happening, what single command gets you onto the WSL filesystem, and how do you open the current folder in Windows Explorer once you are there?

**11.** A hospital consortium wants shared infrastructure that none of them will offer to the general public, and they will hire a third party to operate it. Which deployment model is this, and how is it different from a public cloud?

**12.** You are asked to explain **multitenancy** to someone who thinks "shared hardware" means "other customers can read my disk." Write a four-sentence explanation that includes *how* isolation is enforced.

---

## Answer Key

**1. C.** AWS as a third-party provider offering shared on-demand resources is a public cloud. Hybrid requires combining public with private/on-prem. Private is dedicated to one org.

**2. C.** The notes are explicit: on-prem ≠ private cloud, and a private cloud does not have to be on-premises. D describes hybrid.

**3. C.** SaaS delivers the full application; you just use it. Vercel is the course's PaaS example; EC2 is IaaS.

**4. B.** Multiple isolated AZs inside a region are how you design for high availability. A single AZ failure should not take the application down.

**5. D.** Cost is *often* lower depending on needs — not guaranteed for every workload. Pricing models also vary by service.

**6.**
- **On-demand network access** — create resources when you need them, without a hardware PO.
- **Shared pool of configurable resources** — many customers share provider hardware (multitenancy).
- **Rapidly provisioned and released** — consumption-based pricing; turn it off when finished.

**7.** Region = `ca-central-1` (Canada). AZ = `ca-central-1a`. A VPC lives at the **region** level; its subnets sit in AZs.

**8.** Native Linux (optionally Distrobox), a headless VM, or WSL. Work in the **WSL filesystem**, not `/mnt/c` — Windows mounts commonly have loose permissions, and SSH refuses keys that are group/world-readable.

**9.** Linux environment, AWS account, Sourcehut account. Evaluation: Participation 15%, Test 15%, Midterm 30%, Final 40%.

**10.** `/mnt/c` is the Windows filesystem mounted into WSL. `chmod` there often does not stick, so SSH still sees a too-open key. Run `cd` (no arguments) to jump to the WSL home. From a WSL path, `explorer.exe .` opens Explorer on that folder.

**11.** **Community cloud** — organizations with similar needs pool infrastructure, operated by one of them or a third party. A public cloud is run by a provider (AWS, Azure, GCP) and offered to any customer, not a closed consortium.

**12.** Multitenancy means many customers share physical servers, storage, and networks while remaining **logically isolated**. The provider tracks each tenant's identity, config, permissions, and limits. Isolation is enforced with access controls, virtualization, network isolation, and encryption. One tenant must not be able to read another's data even though they share hardware.
