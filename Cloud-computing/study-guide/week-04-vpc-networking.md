# Week 4 — Networking with VPCs

> **Reading scope:** Only the **Virtual Private Cloud** section of `chpater10` (Ch 10, The Core Networking Services). Route 53 and CloudFront are not assigned this week.

## Learning Objectives

By the end of this week you should be able to:

1. **Design a VPC address plan**: pick a valid CIDR block and carve it into subnets across Availability Zones.
2. **Explain what makes a subnet public or private** (internet gateway + route table + public IP).
3. **Build the course's two-subnet VPC lab** and control traffic with security groups and NACLs.

---

## Key Concepts & Deep Dive

### 1. What a VPC is

A **VPC (Virtual Private Cloud)** is your own logically isolated network inside AWS — "a tool that allows you to create your own network" (`aws-vpc.md`).

- A VPC lives at the **Region** level (e.g. `us-west-2`).
- AWS creates a **default VPC in every region** (CIDR `172.31.0.0/16`) with internet access, so you could launch EC2 without ever touching networking.
- A **non-default VPC** you create is **fully isolated** until you explicitly connect it to something.

Why bother? Security. You put public-facing pieces (web servers) in public subnets and sensitive pieces (**databases**) in private subnets that the internet can't reach.

### 2. CIDR blocks — sizing the network

CIDR notation `a.b.c.d/n` means "the first *n* bits are fixed." Number of addresses = **2^(32 − n)**.

| CIDR | Addresses | Note |
| ---- | --------- | ---- |
| `/16` | 65,536 | **Largest** allowed VPC |
| `/20` | 4,096 | |
| `/24` | 256 | Typical subnet in this lab |
| `/28` | 16 | **Smallest** allowed VPC/subnet |

> A *smaller* prefix number = a *bigger* network. `/16` is bigger than `/24`.

Use the private ranges from **RFC 1918**:

| Range | Example VPC CIDR |
| ----- | ---------------- |
| `10.0.0.0/8` | `10.0.0.0/16` |
| `172.16.0.0/12` | `172.31.0.0/16` |
| `192.168.0.0/16` | `192.168.0.0/20` |

You **can't** use `0.0.0.0/8`, `127.0.0.0/8` (loopback), `169.254.0.0/16` (link-local), or `224.0.0.0/4` (multicast).

Beyond the notes, a useful fact: AWS reserves **5 addresses in every subnet** (the first four and the last), so a `/24` gives you 251 usable IPs.

### 3. Subnets

- A VPC needs **one or more** subnets.
- Each subnet's CIDR must be a **subset** of the VPC's CIDR.
- Each subnet lives in **exactly one Availability Zone**. To be highly available, spread subnets (and instances) across AZs.

### 4. Getting to the internet

Three things must all be true for an instance to be reachable from the internet:

```
 ┌───────────── VPC 10.0.0.0/16 ─────────────────────────┐
 │                                                       │
 │  Public subnet 10.0.1.0/24 (us-west-2a)               │
 │   ┌───────────┐   route 0.0.0.0/0 → igw     ┌──────┐  │      ┌──────────┐
 │   │ EC2       │ ───────────────────────────►│ IGW  │──┼─────►│ Internet │
 │   │ public IP │                             └──────┘  │      └──────────┘
 │   └───────────┘                                       │
 │                                                       │
 │  Private subnet 10.0.2.0/24 (us-west-2b)              │
 │   ┌───────────┐   route table: local only             │
 │   │ EC2       │   (no route to the IGW)               │
 │   │ private IP│                                       │
 │   └───────────┘                                       │
 └───────────────────────────────────────────────────────┘
```

1. An **internet gateway (IGW)** attached to the VPC.
2. A **route table** associated with the subnet that has a default route **`0.0.0.0/0 → IGW`**. A subnet with this route is called a **public subnet**.
3. The instance has a **public IP** (auto-assigned, or an Elastic IP). Auto-assigned public IPs are lost when the instance stops; Elastic IPs persist until you release them.

### 5. Firewalls: security groups vs. NACLs

| | **Security group** | **Network ACL (NACL)** |
| - | ------------------ | ---------------------- |
| Applies to | **Instance** level | **Subnet** level |
| Default inbound | **Nothing allowed** | Allow all |
| Default outbound | Allow all | Allow all |
| Return traffic | Automatically allowed (stateful) | Must be allowed explicitly |
| Traffic between instances in the same subnet | Can restrict | **Can't** restrict |

Every instance needs **at least one** security group, and every VPC gets a default security group and a default NACL.

### 6. Connecting a VPC to other networks

- **VPC peering** — private, point-to-point link between **exactly two** VPCs (same or different regions) over AWS's network.
- **VPN** — encrypted (AES-128/256) tunnel **over the public internet** between a *virtual private gateway* (AWS side) and a *customer gateway* (your router). Up to 10 per VPC.
- **Direct Connect** — a **dedicated private link** (1 or 10 Gbps, or 50–500 Mbps hosted) that bypasses the internet for predictable latency. More expensive, and it doesn't provide internet access.

### 7. The course lab, step by step (`aws-vpc.md`)

| Resource | Name | Settings |
| -------- | ---- | -------- |
| VPC | `bcit-demo-vpc` | `10.0.0.0/16`, then **Enable DNS hostnames** |
| Public subnet | `bcit-demo-sub-pb` | `us-west-2a`, `10.0.1.0/24`, **Enable auto-assign public IPv4** |
| Private subnet | `bcit-demo-sub-pr` | `us-west-2b`, `10.0.2.0/24` |
| Route table | `bcit-demo-rt` | Explicitly associate with **`bcit-demo-sub-pr`** |
| Internet gateway | `bcit-demo-igw` | Attach to `bcit-demo-vpc` |
| Main route table | (auto-created) | Add route **`0.0.0.0/0 → bcit-demo-igw`** |
| Public EC2 | `bcit-demo-pb` | Debian, in `sub-pb`, SG allows **SSH from anywhere** |
| Private EC2 | `bcit-demo-pr` | Debian, in `sub-pr`, SG allows **ICMP from anywhere** |

Why this works: the **main** route table applies to any subnet *without* an explicit association — that's `sub-pb`, so it gets the internet route. `sub-pr` is explicitly tied to `bcit-demo-rt`, which only has the built-in **local** route (`10.0.0.0/16`), so it stays private but can still talk to the rest of the VPC.

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `chpater10` | VPC section: CIDRs, subnets, internet gateways, security groups, NACLs, peering, VPN, Direct Connect, and the VPC review questions (first ~7) |
| `aws-vpc.md` | Plain-language VPC intro, RFC 1918 table, forbidden CIDRs, the full step-by-step lab build |

> `aws-vpc.md` references a diagram at `./assets/vpc-3640.png` that isn't in the repo. The ASCII diagram above shows the same layout.

---

## Practical Takeaways — Why This Matters

- **This is the standard production layout.** Public subnet for load balancers / web servers, private subnet for databases and internal services — you'll see it at every company that uses AWS.
- **Plan CIDRs before you build.** Overlapping CIDRs block VPC peering and VPNs later, and changing a VPC's CIDR after the fact is painful.
- **Most "my server is unreachable" bugs are networking.** Missing IGW route, no public IP, or a security group without the right inbound rule — check these three first.
- **Defence in depth.** Security groups (instance) plus NACLs (subnet) give you two independent layers of firewall.

---

## Knowledge Check

**Q1 (Multiple choice).** Which of these is a valid CIDR block for a VPC?

- A) `10.0.0.0/8`
- B) `10.0.0.0/15`
- C) `10.0.0.0/28`
- D) `10.0.0.0/29`

**Q2 (Multiple choice).** Which pair of statements is correct?

- A) Security groups work at the subnet level; NACLs work at the instance level
- B) Security groups work at the instance level; NACLs work at the subnet level
- C) Both work only at the VPC level
- D) Both work only at the instance level

**Q3 (Code reading / "what does this handle?").** In the lab, two things make `bcit-demo-sub-pb` a working public subnet, and one thing keeps `bcit-demo-sub-pr` private. Identify all three from the lab steps.

**Q4 (Fill in the blank).** The subnet `10.0.1.0/24` contains ________ IP addresses in total. It must fit inside the VPC CIDR `10.0.0.0/16`, which contains ________ addresses. A subnet can span ________ Availability Zone(s).

**Q5 (Scenario).** After building the lab, you SSH into `bcit-demo-pb` and can successfully `ping` the private IP of `bcit-demo-pr`, but `ssh admin@10.0.2.x` from `bcit-demo-pb` times out. Why does ping work but SSH doesn't, and what would you change to allow it securely?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

**Q1 — C) `10.0.0.0/28`.** Allowed sizes are `/16` to `/28`. `/8` and `/15` are too large; `/29` is too small.

**Q2 — B).** Security groups are attached to instances; NACLs are attached to subnets. (Also remember: security groups deny all inbound by default, while the default NACL allows everything.)

**Q3** —
- **Public subnet:** (1) the **main route table** has the route **`0.0.0.0/0 → bcit-demo-igw`** (with the IGW attached to the VPC), and `sub-pb` uses the main table because it has no explicit association; (2) **auto-assign public IPv4** is enabled on `sub-pb`, so instances get a public IP.
- **Private subnet:** `sub-pr` is **explicitly associated with `bcit-demo-rt`**, which has no route to the internet gateway (only the local VPC route).

**Q4** — **256**; **65,536**; **one** (a subnet lives in exactly one AZ).

**Q5** — Traffic between the subnets works thanks to the VPC's **local route**, but `bcit-demo-pr`'s **security group only allows ICMP** (ping) inbound. SSH (TCP port 22) is dropped, so it times out. Fix it by adding an inbound rule to the private instance's security group for **SSH (port 22)** with the source limited to the **public subnet `10.0.1.0/24`** (or the public instance's security group) — not `0.0.0.0/0`. Then connect *through* the public instance as a jump host, e.g. `ssh -J admin@<public-ip> admin@10.0.2.x`, so your private key never has to be copied onto the server.

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** What CIDR block does AWS use for the **default VPC** it creates in every region?

- A) `10.0.0.0/16`
- B) `172.31.0.0/16`
- C) `192.168.0.0/16`
- D) `172.16.0.0/12`

**2.** At what level does a VPC exist?

- A) Availability Zone
- B) Global (across all regions)
- C) Region
- D) Edge location

**3.** How many IP addresses does a `/20` block contain in total?

- A) 1,024
- B) 2,048
- C) 8,192
- D) 4,096

**4.** You create a subnet with the CIDR `10.0.3.0/28`. How many IP addresses can you actually assign to instances in it?

- A) 11
- B) 14
- C) 16
- D) 12

**5.** Which of these CIDR blocks can you **not** use for a VPC?

- A) `10.0.0.0/16`
- B) `192.168.0.0/20`
- C) `172.31.0.0/16`
- D) `169.254.0.0/16`

**6.** Your VPC uses `10.0.0.0/16`. Which of these is a valid CIDR for a subnet inside it?

- A) `10.1.0.0/24`
- B) `10.0.5.0/24`
- C) `192.168.1.0/24`
- D) `10.0.0.0/8`

**7.** You launch an instance with a brand-new security group and add no rules. What inbound traffic does that security group allow?

- A) Nothing
- B) All traffic
- C) SSH only
- D) Only traffic from the same subnet

**8.** Which firewall is **stateful**, meaning return traffic for an allowed request is automatically allowed?

- A) Network ACL
- B) Route table
- C) Security group
- D) Internet gateway

**9.** An instance sits in a subnet whose route table has `0.0.0.0/0 → igw`, and its security group allows SSH from `0.0.0.0/0`. However, the instance only has a **private IP**, and you can't reach it from home. What fixes this?

- A) Add an inbound rule to the subnet's default NACL
- B) Add a second route `10.0.0.0/16 → igw`
- C) Associate an Elastic IP with the instance
- D) Create a VPN connection to the VPC

**10.** You launched `bcit-demo-pb` with an auto-assigned public IP and saved that IP. After you **stop and start** the instance, `ssh` to the saved IP times out. What is the most likely cause?

- A) Auto-assigned public IPs are lost when an instance stops, so it now has a different one
- B) Stopping an instance deletes its security group rules
- C) The main route table loses its `0.0.0.0/0` route when instances stop
- D) The instance was moved to a different Availability Zone

**11.** A company wants a **dedicated private link** from its data centre to AWS that **bypasses the public internet** for predictable latency. Cost is not a concern. Which option fits?

- A) VPC peering
- B) VPN
- C) Internet gateway
- D) Direct Connect

**12.** VPC A uses `10.0.0.0/16`. You're creating VPC B and plan to **peer** it with VPC A later. Which CIDR should VPC B use?

- A) `10.0.0.0/16`
- B) `10.0.128.0/20`
- C) `172.16.0.0/16`
- D) `10.0.0.0/8`

**13.** In the course lab, a teammate adds the route `0.0.0.0/0 → bcit-demo-igw` to **`bcit-demo-rt`**. What is the effect?

- A) Nothing, because private subnets can't have routes to an internet gateway
- B) `bcit-demo-sub-pr` becomes a public subnet, though its instances still need a public IP to be reachable from the internet
- C) `bcit-demo-sub-pb` loses its internet access
- D) The VPC's local route `10.0.0.0/16` is replaced

**14.** In an AWS VPN connection, what is the **AWS-side** endpoint called?

- A) Virtual private gateway
- B) Customer gateway
- C) Internet gateway
- D) Direct Connect location

**15.** Two instances in the **same subnet** must not be able to talk to each other on port 3306. Where do you enforce this?

- A) A deny rule in the subnet's network ACL
- B) The instances' security groups
- C) Removing the local route from the subnet's route table
- D) Moving the internet gateway route to a different route table

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **B.** The default VPC in every region uses `172.31.0.0/16`. `172.16.0.0/12` is the RFC 1918 range that contains it, not the VPC's own CIDR.
2. **C.** A VPC lives at the **Region** level (for example `us-west-2`). Its subnets are the parts that sit in individual Availability Zones.
3. **D.** 2^(32 − 20) = 2^12 = **4,096**. 2,048 would be a `/21` and 8,192 a `/19`.
4. **A.** A `/28` has 2^4 = 16 addresses, and AWS reserves **5 in every subnet** (the first four and the last), leaving **11**. 14 is the answer you'd get by reserving only the network and broadcast addresses, which isn't how AWS works.
5. **D.** `169.254.0.0/16` is the **link-local** range, which the guide lists as forbidden. The other three are RFC 1918 private ranges used as examples in the guide.
6. **B.** `10.0.5.0/24` is a **subset** of `10.0.0.0/16`. `10.1.0.0/24` and `192.168.1.0/24` fall outside the VPC's range, and `10.0.0.0/8` is larger than the VPC itself.
7. **A.** A security group allows **nothing inbound** by default (outbound is allowed). "All traffic" is the default for a NACL, which is the usual mix-up.
8. **C.** Security groups are stateful, so return traffic is allowed automatically. NACLs are stateless: return traffic must be allowed explicitly.
9. **C.** All three conditions must be true: an IGW, a `0.0.0.0/0 → IGW` route, and a **public IP**. The first two are already in place, so the instance needs a public IP such as an Elastic IP. The default NACL already allows all traffic, so option A changes nothing.
10. **A.** Auto-assigned public IPs are released when the instance stops, and a new one is assigned when it starts. An **Elastic IP** persists until you release it, so use one when the address must stay the same.
11. **D.** **Direct Connect** is a dedicated private link that bypasses the internet for predictable latency, and it's the more expensive option. A VPN is encrypted but still runs **over the public internet**.
12. **C.** Overlapping CIDRs block VPC peering. `172.16.0.0/16` doesn't overlap `10.0.0.0/16`, while `10.0.0.0/16`, `10.0.128.0/20` and `10.0.0.0/8` all overlap it. (`/8` is also too large for a VPC.)
13. **B.** A subnet whose route table has `0.0.0.0/0 → IGW` is by definition a public subnet, so `sub-pr` would now be public. Its instances still need a public IP to be reachable, and `sub-pr` doesn't auto-assign one. `sub-pb` uses the main route table, which isn't affected.
14. **A.** The **virtual private gateway** is the AWS side of the VPN tunnel. The **customer gateway** is your router on the other end.
15. **B.** NACLs work at the subnet boundary, so they **can't** restrict traffic between instances in the same subnet. Security groups work at the instance level and can. Route tables decide where traffic goes, not which ports are allowed, so they aren't the tool for this.

</details>
