# Week 4 Quiz — VPC Networking

Sources: `chpater10` (VPC section only), `aws-vpc.md`, `assets/vpc-3640.png`.

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** Allowed VPC IPv4 CIDR sizes are:

- A) `/8` through `/24`
- B) `/16` through `/28`
- C) `/16` through `/32`
- D) Any RFC 1918 prefix

**2.** A subnet lives in:

- A) Every AZ in the region
- B) Exactly one Availability Zone
- C) The region, same as the VPC
- D) An edge location

**3.** Which CIDR is **forbidden** for a VPC?

- A) `10.0.0.0/16`
- B) `172.31.0.0/16`
- C) `192.168.0.0/20`
- D) `127.0.0.0/8`

**4.** Default security group inbound vs default NACL inbound:

- A) SG allow-all, NACL deny-all
- B) SG deny-all, NACL allow-all
- C) Both deny-all
- D) Both allow-all

**5.** Direct Connect is:

- A) An encrypted tunnel over the public internet
- B) A point-to-point link between exactly two VPCs
- C) A dedicated private link that bypasses the internet
- D) Another name for an internet gateway

---

## Short Answer

**6.** State the **three** conditions that must all be true for an instance to be reachable from the internet.

**7.** How many addresses does `10.0.1.0/24` contain, how many does AWS reserve per subnet, and how many are usable?

**8.** In the course lab, why does adding `0.0.0.0/0 → bcit-demo-igw` to the **main** route table make `bcit-demo-sub-pb` public, while `bcit-demo-sub-pr` stays private?

**9.** Contrast VPC peering, VPN, and Direct Connect on *what they connect* and *whether traffic uses the public internet*.

---

## Hands-on / Scenario

**10.** Fill in the lab table from memory.

| Resource | Name | Key setting |
| -------- | ---- | ----------- |
| VPC | | CIDR + DNS hostnames |
| Public subnet | | AZ + CIDR + auto-assign public IPv4 |
| Private subnet | | AZ + CIDR |
| Custom route table | | Associated with which subnet? |
| IGW | | Attached to? |
| Public EC2 SG | | Allowed protocol |
| Private EC2 SG | | Allowed protocol |

**11.** From `bcit-demo-pb` you can `ping` `bcit-demo-pr`'s private IP, but `ssh admin@10.0.2.x` times out. Why, and what inbound rule should you add (source **not** `0.0.0.0/0`)?

**12.** Two instances in the **same** subnet must not talk on TCP 3306. Why can't a NACL do this, and what can?

---

## Answer Key

**1. B.** `/16` (65,536 addresses) is the largest VPC; `/28` (16 addresses) is the smallest VPC or subnet. `/8` is both too big and a forbidden range (`0.0.0.0/8`).

**2. B.** Subnets are AZ-scoped. High availability means **multiple subnets in multiple AZs**. The VPC itself is regional.

**3. D.** Loopback. Also forbidden: `0.0.0.0/8`, `169.254.0.0/16` (link-local), `224.0.0.0/4` (multicast). The others are RFC 1918 examples from the notes.

**4. B.** New SGs allow **nothing inbound** (all outbound). Default NACLs allow all in and out. SGs are **stateful**; NACLs are **stateless**.

**5. C.** VPN is encrypted **over the internet** (virtual private gateway ↔ customer gateway). Peering is private AWS-network, two VPCs only. IGW is how a *public subnet* reaches the internet.

**6.** (1) IGW attached to the VPC. (2) Subnet route table has `0.0.0.0/0 → IGW` (that is the definition of a public subnet). (3) Instance has a public IP (auto-assign or Elastic IP).

**7.** 256 total; AWS reserves **5** (first four + last); **251** usable.

**8.** The main route table applies to any subnet **without** an explicit association — `sub-pb`. `sub-pr` is explicitly associated with `bcit-demo-rt`, which has only the local `10.0.0.0/16` route. If you added the IGW route to `bcit-demo-rt` instead, `sub-pr` would become public (instances would still need a public IP to be reachable).

**9.**
- **Peering:** exactly two VPCs, private over AWS's network, no internet.
- **VPN:** your router (customer gateway) to a virtual private gateway, **AES tunnel over the public internet**, up to 10 per VPC.
- **Direct Connect:** dedicated 1/10 Gbps (or hosted 50–500 Mbps) private link; predictable latency; more expensive; does **not** by itself provide internet access.

**10.**

| Resource | Name | Key setting |
| -------- | ---- | ----------- |
| VPC | `bcit-demo-vpc` | `10.0.0.0/16`, Enable DNS hostnames |
| Public subnet | `bcit-demo-sub-pb` | `us-west-2a`, `10.0.1.0/24`, auto-assign public IPv4 |
| Private subnet | `bcit-demo-sub-pr` | `us-west-2b`, `10.0.2.0/24` |
| Custom RT | `bcit-demo-rt` | Associated with **`bcit-demo-sub-pr`** |
| IGW | `bcit-demo-igw` | Attached to `bcit-demo-vpc`; `0.0.0.0/0` on the **main** RT |
| Public EC2 SG | (on `bcit-demo-pb`) | **SSH** from anywhere |
| Private EC2 SG | (on `bcit-demo-pr`) | **ICMP** from anywhere |

**11.** Local VPC routing allows the ping. The private instance's SG allows **ICMP only**, so TCP/22 is dropped (timeout). Add SSH from `10.0.1.0/24` or from the public instance's SG. Jump through the public host (`ssh -J admin@<public-ip> admin@10.0.2.x`) so the private key never has to live on the jump box's disk if you use agent forwarding — at minimum, do not open port 22 to the world on the private instance.

**12.** NACLs filter at the **subnet boundary**. Traffic between two ENIs in the same subnet never hits the NACL. Use **security groups** (instance-level, can deny 3306 between those two).
