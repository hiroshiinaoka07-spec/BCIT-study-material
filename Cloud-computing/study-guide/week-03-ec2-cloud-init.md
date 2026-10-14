# Week 3 — Compute with EC2 & Bootstrapping Servers with cloud-init

> **Reading scope:** In `chapter 7.md`, skip *Simplified Deployments Through Managed Services* and *Deploying Container and Serverless Workloads* (containers come in term 4), per `README.md`.

## Learning Objectives

By the end of this week you should be able to:

1. **Assemble an EC2 instance** from its parts — AMI, instance type, storage, key pair, security group — and justify each choice.
2. **Pick the right pricing model** (On-Demand, Reserved, Spot) for a workload.
3. **Bootstrap a web server automatically** with a `#cloud-config` file, then connect, debug, and test it from your Linux environment.

---

## Key Concepts & Deep Dive

### 1. An EC2 instance is a virtual version of a physical server

`chapter 7.md` maps each on-prem step to an EC2 concept:

| On-premises | EC2 equivalent |
| ----------- | -------------- |
| Install an OS + software stack | Choose an **AMI** (Amazon Machine Image) |
| Pick CPU, RAM, network card | Choose an **instance type** |
| Buy and install hard drives | Attach **EBS** volumes (or use instance store) |
| Lock the server room door | **Key pair** + **security group** |

### 2. AMIs — the starting image

An AMI is a template that becomes your instance's boot drive. AMIs are **region-specific**. There are four collections:

- **Quick Start** — ~3 dozen popular, mostly Free Tier-eligible images.
- **My AMIs** — your own (made from an EBS **snapshot** of a configured instance, so you can clone a server you spent a week setting up).
- **AWS Marketplace** — vendor software, billed as *software cost + EC2 cost*.
- **Community AMIs** — 100,000+ images, some unverified. **You're responsible for their security.**

The course uses official **Debian** AMIs, published by account `136693071363` (verified on the Debian wiki — you'll query it with the CLI in Week 5).

### 3. Instance types and families

The name tells you a lot, e.g. `t2.micro` (1 vCPU, 1 GB RAM) vs `c5d.18xlarge` (72 vCPUs, 144 GB).

| Family | Examples | Best for |
| ------ | -------- | -------- |
| General purpose | T2, T3, M5 | Most workloads, web servers |
| Compute optimized | C5, C4 | CPU-heavy processing |
| Memory optimized | R5, X1 | Large in-memory datasets |
| Accelerated computing | P3, G3 | GPUs, ML, graphics |
| Storage optimized | H1, I3, D2 | High-throughput disk I/O |

A **vCPU** is AWS's (somewhat vague) unit of compute power. The right *family* can let you use fewer vCPUs and save money.

Isolation options for compliance: a **dedicated instance** runs on hardware reserved for your account; a **dedicated host** also gives you control over instance placement (useful for per-socket software licences).

### 4. Storage: EBS vs. instance store

| | **EBS** | **Instance store** |
| - | ------- | ------------------ |
| Location | Network-attached (low latency) | Physically attached to the host |
| Survives stop/crash? | ✅ Yes, persistent | ❌ No, ephemeral |
| Encryption | ✅ Yes | ❌ No |
| Flexibility | Detach, reattach, snapshot, turn into an AMI | Tied to that host |
| Speed | Fast | **Faster** |

Rule of thumb: **EBS for anything you want to keep**; instance store for scratch data in fast-moving processing jobs.

### 5. Pricing models

```
Cost:  On-Demand ($$$) ─── Reserved ($$) ─── Spot ($)
Risk:  none                1–3 yr commit     can be reclaimed with 2 min notice
```

- **On-Demand** — pay per hour, no commitment. Best for short, uninterruptible bursts (e.g. a one-day sale).
- **Reserved** — 1- or 3-year commitment (All / Partial / No Upfront). It's a **billing discount** automatically applied to matching instances, not a specific machine. Best for the always-on base of an app.
- **Spot** — up to **90% off** unused capacity, but AWS can reclaim it with **two minutes' notice**. Best for big-data jobs and CI/test environments.

**Elastic IP** — a static public IPv4 address that belongs to your account until you release it. You can remap it to a replacement instance to hide a failure. (Release unused Elastic IPs; they cost money.)

### 6. SSH workflow from your Linux environment

From `aws-ec2.md`:

```bash
# 1. Create a key pair (private: ~/.ssh/aws, public: ~/.ssh/aws.pub)
ssh-keygen -f .ssh/aws -C "aws lab key"

# 2. Connect — "admin" is the default user on Debian AMIs
ssh -i .ssh/aws admin@<ip-address>

# 3. Remove an old host entry if a new server reuses an IP
ssh-keygen -R <host>
```

### 7. cloud-init — configure the server on first boot

**cloud-init** is the industry-standard tool that runs on first boot of cloud images. You pass it **user data** (a Bash script or a YAML `#cloud-config` file) when launching the instance.

The lab's starter file from `aws-ec2.md`:

```yaml
#cloud-config

users:
  - name: web
    shell: /bin/bash
    ssh_authorized_keys:
      - "ssh-ed25519... your ssh key"

packages:
  - nginx

write_files:

runcmd:
# Ensure the web user owns the web content.
  - mkdir -p /var/www/html
  - chown -R web:web /var/www/html
  - chmod 0755 /var/www
  - chmod 0755 /var/www/html

  # Enable nginx at boot and restart it.
  - systemctl enable nginx
  - systemctl restart nginx
```

What each top-level key does:

- `#cloud-config` — **must be the first line**, or cloud-init won't treat the file as YAML config.
- `users` — creates a `web` user and installs your public key so you can `ssh web@<ip>`.
- `packages` — installs nginx with the distro's package manager.
- `write_files` — **your task**: write `/var/www/html/index.html` with owner `web:web` and permissions `"0644"` (see the quiz).
- `runcmd` — shell commands run near the end of boot. The `chown` line also guarantees correct ownership even if files were written before the `web` user existed.

Debug and test:

```bash
cloud-init status --long        # on the server: shows errors (usually YAML indentation)
curl http://52.89.72.172        # from your machine: should return your HTML
```

> Most cloud-init failures are **YAML formatting errors** — wrong indentation, tabs instead of spaces, or a missing `|` for multi-line content.

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `chapter 7.md` | AMIs, instance types (Table 7.1), EBS vs instance store, pricing models, Exercise 7.2 (Apache via user data), review questions |
| `aws-ec2.md` | SSH key review, the cloud-init lab starter file and HTML page, troubleshooting, `curl` testing, EC2 feature glossary, Elastic IPs |

---

## Practical Takeaways — Why This Matters

- **Cattle, not pets.** If a server can be rebuilt from an AMI + cloud-init file, a failure is a two-minute relaunch instead of a weekend of rebuilding.
- **Pricing literacy saves real money.** A Reserved base with On-Demand burst capacity is a standard production pattern; Spot is how teams run cheap CI.
- **cloud-init is a gateway to IaC.** Your `#cloud-config` file *is* infrastructure as code — version-control it like any other code.
- **Persistent vs ephemeral storage mistakes lose data.** Know which one your instance uses before writing anything important to it.

---

## Knowledge Check

**Q1 (Multiple choice).** Your web app has a steady base load all year, plus occasional spikes. Which pricing combination makes the most sense?

- A) Spot for the base, Reserved for the spikes
- B) Reserved for the base, On-Demand for the spikes
- C) On-Demand for everything
- D) Dedicated hosts for everything

**Q2 (Multiple choice).** Which statement about instance store volumes is TRUE?

- A) Their data survives an instance stop
- B) They can be encrypted with KMS
- C) They're physically attached to the host, so reads and writes are faster
- D) They can be converted into an AMI

**Q3 (Fill in the code).** Complete the `write_files` section of the lab's cloud-config so it writes the HTML page to `/var/www/html/index.html`, owned by `web:web`, with permissions `0644`. Show the structure, not the whole HTML.

```yaml
write_files:
  - path: ____________
    owner: ____________
    permissions: ____________
    content: ____
      <!DOCTYPE html>
      ...
```

**Q4 (Code reading).** You terminate an instance and launch a new one that happens to get the *same* public IP. When you SSH in, you get a scary `REMOTE HOST IDENTIFICATION HAS CHANGED` warning. Which command from `aws-ec2.md` fixes this, and why does the warning appear?

**Q5 (Scenario).** You launched a Debian instance with your cloud-config, but `curl http://<ip>` hangs and eventually times out. List the checks you'd do, in order, and which file or tool you'd use for each.

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

**Q1 — B).** Reserved instances discount always-running capacity; On-Demand handles uninterruptible, short-lived spikes. Spot (option A) is wrong for the base because it can be reclaimed with two minutes' notice.

**Q2 — C).** Instance store is directly attached, so it's faster — but it's **ephemeral**, can't be encrypted, and can't be turned into an AMI (all EBS features).

**Q3** —

```yaml
write_files:
  - path: /var/www/html/index.html
    owner: web:web
    permissions: "0644"
    content: |
      <!DOCTYPE html>
      <html lang="en">
      ...
      </html>
```

Key details: `permissions` must be a **quoted string** (`"0644"`); `content: |` is YAML's multi-line literal block; every HTML line must be **indented consistently** under `content`.

**Q4** — `ssh-keygen -R <host>` (e.g. `ssh-keygen -R 52.89.72.172`). SSH saved the *old* server's host key in `~/.ssh/known_hosts`. The new server at the same IP has a different key, so SSH warns of a possible man-in-the-middle attack. Removing the stale entry lets you accept the new key.

**Q5** — A reasonable order:

1. **Security group** (EC2 console): is there an inbound rule for **HTTP, port 80** from `0.0.0.0/0`? A timeout (instead of "connection refused") usually means a firewall is dropping traffic. Chapter 7's Exercise 7.2 adds exactly this rule.
2. **Correct IP / public IP assigned**: are you curling the instance's current public IPv4?
3. **SSH in** (`ssh -i .ssh/aws admin@<ip>`) and run **`cloud-init status --long`** to look for YAML or module errors.
4. **Check nginx** on the server: `systemctl status nginx` — did the package install and the `runcmd` restart succeed?
5. **Check the file**: does `/var/www/html/index.html` exist with the right owner and permissions?

</details>
