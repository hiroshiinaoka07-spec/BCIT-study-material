# Week 2: Identity & Permissions — FSMO Roles, the IGDLA Model & SIDs

> **Midterm topics covered:** *FSMO Roles* and *IGDLA Model* (`Midterm.pdf` p.1) · *Security Identifier (SID)* (`Midterm.pdf` p.2, last heading)
> **Sources:** `ACIT3420 Domain Controller (1).pdf` slides 36–45, SS64 *Local Domain groups, Global groups and Universal groups*, lab video *Group Nesting* (via [`../study-guide/week-04-…`](../study-guide/week-04-groups-fsmo-replication-troubleshooting.md) and [`../group-nesting-notes.md`](../group-nesting-notes.md)), Hyper-V lecture video (Sysprep remark)

## Learning Objectives

By the end of this week you should be able to:

1. **Name the five FSMO roles**, their scope (forest vs domain), what each does, and how they're distributed across a forest.
2. **Apply IGDLA** (Identity → Global → Domain Local → Access) and decide whether one group scope can be nested in another, including **across domains**.
3. **Explain what a SID is** and why it, not the account name, is what Windows uses for security and identity.

---

## 1. FSMO roles (Flexible Single Master Operations)

**Definition:** AD is **multi-master** (any writable DC accepts changes), but five operations would conflict if two DCs did them at once. Each of these is assigned to **exactly one DC** — that DC is the *operations master* for the role.

| Role | Scope | What it does | Managed in |
|---|---|---|---|
| **Schema Master** | **Forest** (1 per forest) | The only DC that can **change the schema** | **AD Schema** snap-in (`regsvr32 schmmgmt.dll` first) |
| **Domain Naming Master** | **Forest** | **Adds/removes domains** in the forest | **AD Domains and Trusts** |
| **PDC Emulator** | **Domain** (1 per domain) | **Time sync** source, **password changes**, **account lockout**, GPO editing, legacy PDC | **AD Users and Computers** → Operations Masters |
| **RID Master** | **Domain** | Hands out **pools of Relative IDs** so each DC can build **SIDs** for new objects | **ADUC** |
| **Infrastructure Master** | **Domain** | Updates **cross-domain object references** (e.g. a group member from another domain) | **ADUC** |

### How they're distributed

- **2 forest-wide + 3 per domain.** A forest with 3 domains has 2 + (3 × 3) = **11** role assignments.
- By default all roles land on the **first DC** (forest root → all 5; first DC of each new domain → its 3 domain roles).
- If **every DC is a GC**, Infrastructure Master placement stops mattering (Week 1 trade-off table).

```cmd
netdom query fsmo        :: list the current role holders
```

| Situation | Action |
|---|---|
| Old holder is **online** (planned maintenance) | **Transfer** the role (GUI consoles above) |
| Old holder is **dead** and won't return | **Seize** the role with `ntdsutil`, then clean up the dead DC's metadata |

> **Memory hook:** *"Schema, Naming — the forest's two. PDC, RID, Infrastructure — every domain's three."*

---

## 2. The IGDLA model

```
Identity (users / computers)
   └─► Global group         — WHO   (by role:     "ACIT Faculty Global")
         └─► Domain Local group  — WHAT  (by resource: "ACL_VanShare_Read")
               └─► Access    — the permission on the share / NTFS / printer
```

- **IGDLA** (slide wording): **I**dentities → **G**lobal → **D**omain **L**ocal → **A**ccess.
- Same idea as Microsoft's **AGDLP** (Accounts → Global → Domain Local → Permissions). In multi-domain forests, **AGUDLP** inserts a **Universal** group in the middle.

### Group scopes (you need these to apply IGDLA)

| Scope | Can contain | Can be granted access to |
|---|---|---|
| **Global** | Users, computers, Global groups **from the same domain only** | Resources in **any** domain |
| **Domain Local** | Users, computers, **Global & Universal groups from any domain**, Domain Local groups from the **same** domain | Resources in **its own domain only** |
| **Universal** | Users, computers, Global & Universal groups **from any domain** (no Domain Local) | **Any** resource in the forest. Membership stored in the **GC** |

**Group types:** **Security** groups have a **SID** and can be given permissions. **Distribution** groups have **no SID** and are email-only. Either can be converted to the other.

### Nesting matrix — can the **row** go inside the **column**?

| member ↓ / container → | Global (same dom) | Global (other dom) | Universal | DL (same dom) | DL (other dom) |
|---|---|---|---|---|---|
| **Global** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Universal** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Domain Local** | ❌ | ❌ | ❌ | ✅ | ❌ |

### Why IGDLA is "structured and scalable"

SS64 example: 25 accountants need 3 resources.

| Approach | Memberships to maintain | New hire |
|---|---|---|
| Flat (users straight onto each resource group) | 25 × 3 = **75** | Remember all 3 groups |
| **IGDLA** (25 users → `Accounting` Global → 3 resource DL groups) | 25 + 3 = **28** | Add to **one** group |

- **Revoke** a whole team's access by removing one Global group from one DL group — no ACL edits.
- **Safe by design:** a Domain Local group *can't* go inside a Global group, so you can't accidentally nest a resource group inside a people group.
- Group membership is evaluated **at logon**, so users must **log off and on** after a membership change.

### Lab walkthrough (Group Nesting video)

On the child DC (`BBY.Adatum.com`) → ADUC → `BBY` OU → **CIT Local** → Properties → **Members → Add… → Locations…** → change to **`Adatum.com`** → type `acit` → **Check Names** → add **ACIT Universal** and **ACIT Global**. This works because a **Domain Local** group accepts Global and Universal groups from **another domain**.

### Slide 41 questions (likely exam material)

`Adatum.com`: ACIT Global (G), ACIT Faculty Global (G), ACIT Local (DL), ACIT Universal (U). `Bby.Adatum.com`: CIT Global (G), CIT Local (DL), CIT Universal (U).

| # | Nest… → into… | Answer | Rule |
|---|---|---|---|
| 1 | ACIT Faculty Global → ACIT Global | ✅ | G → G, same domain |
| 2 | ACIT Universal → ACIT Global | ❌ | Global only takes same-domain users/computers/Globals |
| 3 | ACIT Local → ACIT Faculty Global | ❌ | DL can't go inside Global |
| 4 | ACIT Global → ACIT Universal | ✅ | G → U |
| 5 | ACIT Universal → ACIT Local | ✅ | U → DL |
| 6 | CIT Global → ACIT Global | ❌ | Global can't nest **across domains** |
| 7 | CIT Local → ACIT Local | ❌ | DL won't accept a DL from **another domain** |
| 8 | ACIT Universal → CIT Universal | ✅ | U → U, any domain |
| 9 | ACIT Universal → CIT Local | ✅ | DL accepts U from any domain (shown in the lab) |
| 10 | ACIT Global → CIT Universal | ✅ | U accepts G from any domain |

---

## 3. Security Identifier (SID)

> ⚠ **Coverage note:** no course file has a dedicated SID section. Everything below is what the course files *do* say about SIDs, plus the one-line definition the midterm asks for.

**What is a SID?** A **unique identifier** given to every **security principal** — users, computers and **security** groups. Windows uses the SID, **not the name**, to decide who someone is and what they can access.

**How the course material ties SIDs to the rest of the midterm:**

| Where it shows up | What the course says |
|---|---|
| **RID Master** (FSMO) | Hands each DC a **pool of RIDs** so it can create **SIDs** for new objects. Domain SID + unique RID = the object's SID. This is why **only one DC per domain** may hand out RID pools: two DCs issuing the same RID would create duplicate SIDs |
| **Security vs Distribution groups** | **Security groups have a SID** (so they can be put on ACLs). **Distribution groups have no SID**, so they can't be granted permissions |
| **Permissions / IGDLA** | Permissions are granted to the group's SID; users get access through the SIDs of the groups they belong to, collected **at logon** (hence "log off and on" after membership changes) |
| **Cloning VMs** (Hyper-V lecture, ~29:47) | Before cloning a Windows instance (e.g. from a differencing disk / linked clone), **run Sysprep** — it generalizes the image so the copies don't share the same machine identity (SID) |
| **DC cloning** | The supported process (`Cloneable Domain Controllers` group + `New-ADDCCloneConfigFile`) exists so a copied DC gets its own identity |

**Why it matters for security and identity management:**

- **Renaming is safe.** Rename a user and their permissions survive, because ACLs store the SID.
- **Deleting is permanent.** Delete a user and recreate one with the same name → it gets a **new SID**, so it does **not** get the old permissions back.
- **Duplicate SIDs = identity confusion**, which is why RID allocation is a single-master role and why cloned machines are generalized.

---

## Module Tour

| Where | What to look at |
|---|---|
| `Midterm.pdf` **p.1** *FSMO Roles*, *IGDLA Model*; **p.2** *Security Identifier (SID)* | The exact wording tested |
| `ACIT3420 Domain Controller (1).pdf` slides 36–45 | FSMO, group types/scopes, IGDLA, **slide 41's 10 questions** (content in [`../study-guide/week-04-…`](../study-guide/week-04-groups-fsmo-replication-troubleshooting.md) §1–5) |
| [`../group-nesting-notes.md`](../group-nesting-notes.md) | Step-by-step of the cross-domain nesting demo |
| `transcripts/Group Nesting/dense/t025.jpg`, `t033.jpg` | *Multiple Names Found* dialog; final CIT Local members |
| `transcripts/Lecture Video/transcript.md` ~29:30–29:50 | Sysprep before cloning |

## Practical Takeaways

- **Know your FSMO holders before something breaks.** Losing the PDC Emulator breaks time sync and password changes; losing the RID Master eventually stops new object creation.
- **IGDLA turns onboarding into one click.** New hire → one Global group. Access audits read "who's in this DL group?"
- **Think in SIDs.** "I recreated the account but they still can't get in" is a SID problem — the old ACL entries point at a SID that no longer exists.

---

## Knowledge Check: Week 2

**1. (Multiple choice)** Which pair of FSMO roles exists **once per forest**?
- A) PDC Emulator and RID Master
- B) Schema Master and Domain Naming Master
- C) Infrastructure Master and PDC Emulator
- D) RID Master and Schema Master

**2. (Multiple choice)** Following IGDLA, where do you assign the actual NTFS permission on a file share?
- A) Directly to each user account
- B) To the Global group
- C) To the Domain Local group
- D) To the Universal group only

**3. (Fill in the blank)** The FSMO role that hands out pools of ______ so DCs can create unique ______ for new objects is the ______ Master.

**4. (What does it handle?)** What does `netdom query fsmo` tell you, and when would you **seize** rather than **transfer** a role?

**5. (Scenario)** An admin deletes the user `jsmith` by mistake, recreates `jsmith` with the same name and password, and adds them back to the `Sales` Global group. `jsmith` can open the Sales share (granted via `Sales` → `ACL_Sales_Read`) but **not** a personal folder whose NTFS permissions listed `jsmith` directly. Explain why using the guide's SID concepts, and say what IGDLA practice would have avoided the problem.

<details>
<summary><b>Answer key with explanations (click to expand)</b></summary>

1. **B.** Schema Master and Domain Naming Master are forest-wide. PDC Emulator, RID Master and Infrastructure Master exist **once per domain**.
2. **C.** IGDLA = Identity → Global → **Domain Local → Access**. The permission (Access) goes on the Domain Local group; people go in the Global group; the Global group goes in the Domain Local group.
3. **RIDs (Relative IDs)**, **SIDs**, **RID** Master.
4. It lists which DC holds each of the **five FSMO roles**. **Transfer** when the current holder is online (planned move). **Seize** with `ntdsutil` only when the holder is **permanently dead** — then do metadata cleanup so it never comes back.
5. The recreated account has a **new SID**. The personal folder's ACL stores the **old SID**, so the new `jsmith` doesn't match it. The Sales share works because access is granted to the `ACL_Sales_Read` group's SID, and the new `jsmith` is a member again via `Sales`. **IGDLA** avoids this by **never putting user accounts directly on ACLs** — grant to Domain Local groups, so re-adding a user to the right Global group restores everything.

</details>
