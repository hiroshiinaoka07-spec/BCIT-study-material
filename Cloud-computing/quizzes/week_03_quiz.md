# Week 3 Quiz — EC2 & cloud-init

Sources: `chapter 7.md` (skip managed/container/serverless sections), `aws-ec2.md`.

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** AMIs are:

- A) Global; one AMI ID works in every region
- B) Region-specific templates that become the instance boot volume
- C) The firewall rules attached to an instance
- D) Billing discounts applied to running instances

**2.** Which storage survives an instance **stop**?

- A) Instance store only
- B) EBS only
- C) Both, because both are network-attached
- D) Neither; you must snapshot first

**3.** Spot instances can be reclaimed with:

- A) No notice
- B) Two minutes' notice
- C) One hour's notice
- D) Only at the end of a 1-year term

**4.** The first line of a YAML cloud-init user-data file must be:

- A) `#!/bin/bash`
- B) `#cloud-config`
- C) `cloud-init:`
- D) `---yaml`

**5.** Community AMIs are risky because:

- A) They always cost extra on top of EC2
- B) There are 100,000+ images, some unverified, and **you** are responsible for their security
- C) They cannot run Linux
- D) They only work with dedicated hosts

---

## Short Answer

**6.** Map the four on-prem steps (install OS, pick CPU/RAM, buy disks, lock the server room) to the four EC2 parts you choose at launch.

**7.** Give one good workload for On-Demand, one for Reserved, and one for Spot, and state the risk/cost trade-off in a phrase each.

**8.** What is an Elastic IP, when does it cost money while unused, and how does it hide an instance failure?

**9.** In the lab `#cloud-config`, what do `users`, `packages`, `write_files`, and `runcmd` each do? Why does `runcmd` include `chown -R web:web /var/www/html`?

---

## Hands-on / Scenario

**10.** Complete this `write_files` block so nginx serves the lab HTML as `web:web` with mode `0644`. Call out the two YAML pitfalls that cause most cloud-init failures.

```yaml
write_files:
  - path:
    owner:
    permissions:
    content:
```

**11.** You terminate an instance. A new one gets the same public IP. SSH prints `REMOTE HOST IDENTIFICATION HAS CHANGED`. What command from `aws-ec2.md` fixes it, and why is the warning there?

**12.** `curl http://<public-ip>` hangs until timeout after you launched with the lab cloud-config. List the checks in a sensible order.

---

## Answer Key

**1. B.** AMIs are region-specific. Copy/create in the target region if you need the same image elsewhere. Firewall = security group; discounts = Reserved/Spot.

**2. B.** EBS is persistent and network-attached. Instance store is physically on the host and is **ephemeral** (gone on stop/hibernate/terminate). It is faster but not for data you must keep.

**3. B.** Up to ~90% off unused capacity; AWS can reclaim with **two minutes' notice**. Fine for CI/batch; not for the uninterruptible base of a prod app.

**4. B.** Without `#cloud-config` as line 1, cloud-init will not treat the file as YAML config. `#!/bin/bash` marks a shell script (the other valid user-data form).

**5. B.** Quick Start ≈ popular Free-Tier images; Marketplace = vendor software + EC2 cost; My AMIs = snapshots of *your* instances.

**6.** OS+stack → **AMI**; CPU/RAM/NIC → **instance type**; disks → **EBS** (or instance store); physical security → **key pair + security group**.

**7.** On-Demand: short uninterruptible burst (one-day sale) — no commitment, highest hourly cost. Reserved: always-on base — 1/3-year billing discount, not a specific machine. Spot: CI/big-data — cheapest, can vanish in two minutes.

**8.** A static public IPv4 allocated to **your account** until you release it. Unused Elastic IPs are billed, so release them. Remap the same address onto a replacement instance (or put it in DNS) to hide a failure.

**9.** `users` creates `web` and installs your public key. `packages` installs nginx. `write_files` drops `index.html`. `runcmd` runs late in boot (`mkdir`/`chmod`/`systemctl`). The `chown` covers the case where files were written before the `web` user existed.

**10.**

```yaml
write_files:
  - path: /var/www/html/index.html
    owner: web:web
    permissions: "0644"
    content: |
      <!DOCTYPE html>
      ...
```

Pitfalls: `permissions` must be a **quoted string**; `content: |` needs consistent indentation (no tabs). Most failures are YAML, diagnosed with `cloud-init status --long` on the instance.

**11.** `ssh-keygen -R <host>`. `~/.ssh/known_hosts` still has the **old** instance's host key. The new VM at that IP has a different key, so SSH warns about a possible MITM. Removing the stale entry lets you accept the new key.

**12.**
1. Security group: inbound **HTTP/80** from `0.0.0.0/0`? A hang (vs connection refused) usually means a firewall drop.
2. Confirm you are curling the current public IPv4 (auto-assigned IPs change on stop/start).
3. SSH as `admin` and run `cloud-init status --long`.
4. `systemctl status nginx`.
5. Check `/var/www/html/index.html` owner/mode.
