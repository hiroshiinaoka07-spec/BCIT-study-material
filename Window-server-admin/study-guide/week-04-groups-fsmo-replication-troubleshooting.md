# Week 4: Groups & Nesting, FSMO Roles, Replication & DC Removal

> ACIT 3420 Windows Server Administration, Module 3–4 (part 2)
> Sources: `ACIT3420 Domain Controller (1).pdf` (slides 36–45), `Local Domain groups, Global groups and Universal groups (1).pdf` (SS64), `Repadmin Tool (1).pdf`, `Forced Removal of a Domain Controller from Active Directory (1).pdf`, the lab video *Group Nesting*.

## Learning Objectives

By the end of this week you should be able to:

1. **Decide** whether one group can be nested in another, within a domain and **across domains**, and apply **AGDLP / IGDLA**.
2. **Name** the five FSMO roles, their scope, and the console that manages each.
3. **Diagnose** replication with `repadmin`, and **force-remove** a dead DC (ADUC, Sites and Services, `ntdsutil` metadata cleanup).

---

## 1. Group types

| | **Security group** | **Distribution group** |
|---|---|---|
| SID? | **Yes** (it's a security principal) | **No**, not security enabled |
| Can be given permissions? | **Yes** | **No** |
| Email list? | Yes (can be mail-enabled) | Yes; that's its only job |

You can **convert** either type into the other. Members **inherit** the rights and permissions assigned to the group.

> Group membership is evaluated at **logon**. After changing membership, the user must **log off and on**. Permission changes made directly on ACLs or user accounts apply **immediately**.

---

## 2. Group scopes

| Scope | Stored in | **Can contain** | **Can be granted access to** |
|---|---|---|---|
| **Local** (machine) | Local **SAM** | Users, computers, Global/Universal groups, Domain Local groups (same domain) | **That one computer only**. Still works if the network is down |
| **Domain Local** | AD | Users, computers, **Global & Universal groups from any domain** in the forest/trusted domains, Domain Local groups **from the same domain** | Resources **in its own domain only** |
| **Global** | AD | Users, computers, Global groups **from the same domain only** | Resources in **any domain** (own domain + trusting domains) |
| **Universal** | AD (membership in the **GC**) | Users, computers, Global and Universal groups **from any domain in the forest**. **No Domain Local** | **Any resource in the forest** |

### Memory hooks

- **Global = "who"**, the people, grouped by role/department. **Members: same domain only. Used: anywhere.**
- **Domain Local = "what"**, the resource access. **Members: from anywhere. Used: own domain only.**
- **Universal = forest-wide** both ways, but every membership change replicates to **every GC**. Keep membership **static** by nesting Global groups instead of users.
- **Domain Local groups can't go inside anything** except other Domain Local groups in the same domain.

### Nesting rules (SS64)

**Same domain:**
- Global → can nest in **Domain Local, Universal, and other Global** groups.
- Universal → can nest in **Domain Local and other Universal** groups.
- Domain Local → **cannot** nest in Global or Universal.

**Different domain:**
- Domain Local accepts **anything except Domain Local groups from another domain**.
- Global groups **cannot be nested across domains**, and a user from domain A cannot join a Global group in domain B.
- Universal accepts users, computers and Global groups **from any domain**, and can nest in Universal or Domain Local groups **in any domain**.
- Cross-domain group use requires a **trust** (automatic inside a forest).

### Quick nesting matrix: can the **row** go inside the **column**?

| ↓ member / container → | Global (same dom) | Global (other dom) | Universal (any) | DL (same dom) | DL (other dom) |
|---|---|---|---|---|---|
| **Global** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Universal** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Domain Local** | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 3. Best practice: AGDLP / IGDLA

```
Identities (users/computers)
   └─► Global group  (by ROLE:  "Sales", "Auditors")
         └─► Domain Local group  (by RESOURCE: "ACL_Sales_Read")
               └─► Assigned permission on the resource (share/NTFS/printer)
```

- **IGDLA** (slides): **I**dentities → **G**lobal → **D**omain **L**ocal → **A**ccess.
- **AGDLP** (classic): **A**ccounts → **G**lobal → **D**omain **L**ocal → **P**ermissions.
- **AGUDLP** for multi-domain forests: put a **U**niversal group between Global and Domain Local.

**Why separate people and resources?** The SS64 example: 25 accountants need *Crest*, *Intranet* and *Account_Balances*.
- **Flat:** add 25 people to 3 groups = **75** memberships to maintain. A new hire means remembering all 3.
- **Nested:** 25 people in `Accounting` (Global), and `Accounting` in `res_CREST`, `res_INTRANET`, `res_ACCOUNT_BALANCES` (Domain Local) = **28**. A new hire goes into one group.
- **Bonus:** temporarily cut access by removing `Accounting` from `res_CREST`. No need to touch users or ACLs.
- **Why it's safe:** you *can't* put a Domain Local group into a Global group, so you can't accidentally nest a resource group inside a people group. Otherwise a colour-printer group nested in the HR group would hand HR files to everyone in it.

**Who can modify groups:** members of **Account Operators**, **Domain Admins**, **Enterprise Admins**, or anyone delegated the authority.

---

## 4. The slide 41 questions (likely exam material)

Groups:
- `Adatum.com → Downtown` OU: **ACIT Global** (G), **ACIT Local** (DL), **ACIT Universal** (U), **ACIT Students** (U), **ACIT Faculty Global** (G)
- `Bby.Adatum.com → BBY` OU: **CIT Global** (G), **CIT Local** (DL), **CIT Universal** (U)

| # | Question | Answer | Why |
|---|---|---|---|
| 1 | ACIT Faculty Global → ACIT Global | ✅ **Yes** | Global into Global, **same domain** |
| 2 | ACIT Universal → ACIT Global | ❌ **No** | Global groups only take users, computers and Global groups from the same domain |
| 3 | ACIT Local → ACIT Faculty Global | ❌ **No** | Domain Local can't nest in Global |
| 4 | ACIT Global → ACIT Universal | ✅ **Yes** | Global can nest in Universal |
| 5 | ACIT Universal → ACIT Local | ✅ **Yes** | Universal can nest in Domain Local |
| 6 | CIT Global → ACIT Global | ❌ **No** | Global groups **can't be nested across domains** |
| 7 | CIT Local → ACIT Local | ❌ **No** | Domain Local doesn't accept Domain Local groups **from another domain** |
| 8 | ACIT Universal → CIT Universal | ✅ **Yes** | Universal into Universal, any domain in the forest |
| 9 | ACIT Universal → CIT Local | ✅ **Yes** | Domain Local accepts Universal groups from any domain (**shown in the lab video**) |
| 10 | ACIT Global → CIT Universal | ✅ **Yes** | Universal accepts Global groups from any domain in the forest |

### Group Nesting lab walkthrough (video)

On **ACIT3420Sub-DC** (`BBY.Adatum.com`), in ADUC:

1. `BBY` OU → **CIT Local** → Properties → **Members** → **Add…**
2. Click **Locations…** and change *From this location* from `BBY.Adatum.com` to **`Adatum.com`**.
3. Type `acit` → **Check Names** → *Multiple Names Found* (ACIT Faculty, ACIT Global, ACIT Students, ACIT Universal).
4. Add **ACIT Universal**, then repeat for **ACIT Global**.
5. Result: CIT Local's members are `ACIT Global` and `ACIT Universal`, both from `Adatum.com/Downtown`.

![CIT Local members after nesting](<../../transcripts/Group Nesting/dense/t033.jpg>)

---

## 5. FSMO / Operations Master roles

AD is **multi-master** (write on any DC), but five jobs must be done by **one DC only**: the **Flexible Single Master Operations** roles.

| Role | Scope | What it does | Managed in |
|---|---|---|---|
| **Schema Master** | **Forest** (1 per forest) | Only DC that can **change the schema** | **AD Schema** snap-in (`regsvr32 schmmgmt.dll` first) |
| **Domain Naming Master** | **Forest** | **Adds/removes domains** in the forest (needed when creating `Van` / `Indy`) | **AD Domains and Trusts** |
| **PDC Emulator** | **Domain** (1 per domain) | Time sync source, **password changes / account lockout**, GPO editing, legacy PDC | **AD Users and Computers** → Operations Masters |
| **RID Master** | **Domain** | Hands out pools of **Relative IDs** so DCs can create SIDs for new objects | **ADUC** |
| **Infrastructure Master** | **Domain** | Updates **cross-domain object references** (e.g. a group member from another domain) | **ADUC** |

> **2 forest + 3 domain = 5.** A forest with 3 domains has 2 + (3×3) = **11** role holders.
> Check holders with: `netdom query fsmo`
> **Transfer** a role (old holder online) vs **seize** it (old holder dead, done with `ntdsutil`).

---

## 6. Replication

- **Within a site:** fast, uncompressed, change-notification based (seconds).
- **Between sites:** compressed, on a **schedule**, through **bridgehead servers** (one per site), over site links.
- The **KCC (Knowledge Consistency Checker)** builds the replication topology automatically (`<automatically generated>` connections in Sites and Services) and recalculates it every **15 minutes**.
- To trigger it manually: **AD Sites and Services → NTDS Settings → connection → Replicate Now**.
- Replication problems lead to authentication problems, which lead to failures accessing resources.

---

## 7. `repadmin`: the replication troubleshooting tool

- Built in since **Windows Server 2008 / 2008 R2**. Available wherever the **AD DS or AD LDS** role or **RSAT AD DS tools** are installed.
- Run it from an **elevated** Command Prompt as a **domain admin**.

> ⚠ The handout says "run `ntdsutil` … to start repadmin". In practice you just type `repadmin …` directly. Know that the handout says it, in case it shows up on the test.

| Command | Use |
|---|---|
| `repadmin /replsum` | **First command to run.** Summary of every DC's replication status: **Source DSA** and **Destination DSA** sections, attempts, fails, error %. **RODCs appear only under Destination**, because they don't replicate outbound |
| `repadmin /showrepl *` | **Detailed** per-partner results and the likely cause of each failure |
| `repadmin /queue` | Shows the **inbound replication queue**. Items waiting is normal; items stuck indefinitely or a very long queue means a problem |
| `repadmin /kcc` | Forces the **KCC** to recalculate this DC's inbound topology now (normally every 15 min) |
| `repadmin /replicate <dest> <source> <NC>` | **Forces replication** of a partition between DCs |
| `repadmin /syncall <DSA> [<NC>] [flags]` | Syncs a DC with **all its partners**. Default NC = **configuration** partition. Flags: `/a` abort if a server is unavailable, `/h` help, `/i` iterate indefinitely, `/s` do not synchronise, `/q` quiet |
| `repadmin /prp` | Manages the **Password Replication Policy for RODCs**. Run it against a **writable** DC. `add`, `delete`, `move`, `view`. **Can't** edit the **Deny** list |
| `repadmin /showattr` | Shows an object's attributes now. Uses **LDAP 389** for writable partitions and **3268** for read-only/GC |
| `repadmin /showobjmeta` | Attribute **change history**: version number, originating DC, timestamp, GUID, **USNs** |

**Fix example from the handout** (a Kerberos error in `/showrepl`): stop the **Kerberos Key Distribution Center** service → restart **Active Directory Domain Services** → **Replicate Now** in Sites and Services → check the logs → restart the KDC.

---

## 8. Forced removal of a dead DC

**Scenario:** the DC is dead, there's no backup, and it won't come back. If it is even partly online, **try a normal demote first**. A forced removal leaves **orphaned metadata** that must be cleaned up.

### Method 1: Active Directory Users and Computers
1. **Domain Controllers** OU → right-click the DC → **Delete** → Yes.
2. Check **"Delete this Domain Controller anyway. It is permanently offline and can no longer be removed using the removal wizard"** → **Delete**.
3. If it was a **GC**, confirm with Yes.
4. If it held **FSMO roles**, click OK to **transfer them to another DC** (unless you already seized them).

### Method 2: AD Sites and Services
1. Sites → … → the server → right-click **NTDS Settings** → **Delete** → Yes → accept the warnings → **Delete**.
2. Confirm the GC/FSMO prompts as above.
3. Then delete the **server object** itself.

### Method 3: `ntdsutil` metadata cleanup
```text
ntdsutil
metadata cleanup
connections
connect to server <working DC in the same domain>
quit
select operation target
list domains
select domain <#>
list sites
select site <#>
list servers in site
select server <#>          <- the dead DC
quit
remove selected server     -> confirm Yes
quit
quit
```

**Afterwards, always:** clean up **DNS** (A, NS and SRV records of the dead DC; scavenging is slow) and check **Sites and Services** for leftovers. Microsoft says the GUI methods clean metadata automatically, but records still get left in DNS and Sites.

---

## Repository Tour

| File | What to look at |
|---|---|
| `Window-server-admin/ACIT3420 Domain Controller (1).pdf` | Slides 36–45: FSMO, group types/scopes, IGDLA, **the 10 questions**, replication, summary |
| `Window-server-admin/Local Domain groups, Global groups and Universal groups (1).pdf` | Nesting rules, the "separate people and resources" example, membership/permission tables |
| `Window-server-admin/Repadmin Tool (1).pdf` | All the `repadmin` switches |
| `Window-server-admin/Forced Removal of a Domain Controller from Active Directory (1).pdf` | The three removal methods |
| `Window-server-admin/group-nesting-notes.md` | Group Nesting lab notes |
| `transcripts/Group Nesting/dense/` | Lab screenshots: `t017` (ACIT groups), `t025` (Multiple Names Found), `t033` (final members) |

## Practical Takeaways

- **AGDLP keeps permissions maintainable.** Onboarding becomes "add the user to one Global group" instead of editing ACLs.
- **Universal groups cost GC replication.** Nest groups in them, not users.
- **FSMO placement matters when a DC dies.** Know which roles you'd need to seize: losing the PDC Emulator breaks time sync and password changes.
- **`repadmin /replsum` first, `/showrepl` second** is the standard replication triage.
- A dead DC that isn't cleaned out leaves stale DNS/SRV records, so clients keep trying to authenticate against a server that doesn't exist.

---

## Knowledge Check: Week 4

**1. (Multiple choice)** Which group scope can contain members from **any domain in the forest** but can only be **assigned permissions in its own domain**?
- A) Global
- B) Universal
- C) Domain Local
- D) Machine Local

**2. (Multiple choice)** Which FSMO role must be online to **add a new child domain** like `Van.Adatum.com` to the forest?
- A) PDC Emulator
- B) RID Master
- C) Infrastructure Master
- D) Domain Naming Master

**3. (Fill in the blank)** The first `repadmin` command to run when debugging replication is `repadmin /________`. To see detailed per-partner failures, use `repadmin /________ *`. Read-only DCs appear only in the ________ DSA section.

**4. (What does it do?)** What does this `ntdsutil` sequence accomplish, and what must you do afterwards?
```text
metadata cleanup
connections
connect to server CA-VAN-SVR1
quit
select operation target
... select server 1
quit
remove selected server
```

**5. (Scenario)** The `Van.Adatum.com` file server has a share that the **Adatum.com** ACIT faculty need to read. Using AGDLP, which groups do you create or use, in which domains, and how do you nest them? Could you instead put the Adatum `ACIT Faculty Global` group directly into a Van **Global** group?

<details>
<summary><b>Answer key (click to expand)</b></summary>

1. **C, Domain Local.** It accepts users and Global/Universal groups from any domain, but can only grant access to resources in its own domain. (Global is the opposite: same-domain members, usable anywhere.)
2. **D, Domain Naming Master.** It's the forest-wide role that adds and removes domains. The other three are per-domain roles.
3. **`replsum`**, **`showrepl`**, **Destination**. RODCs never replicate outbound, so they never appear as a source.
4. It **force-removes the metadata of a dead DC** (server 1 in the selected domain and site), connecting through a working DC (`CA-VAN-SVR1`). Afterwards, **delete the dead DC's DNS records** (A, NS, SRV) and check **AD Sites and Services** for a leftover server object. Transfer or seize any FSMO roles it held.
5. **Faculty users → `ACIT Faculty Global`** (Global, **Adatum.com**) → a **Domain Local** group in **Van.Adatum.com**, e.g. `ACL_VanShare_Read` → assign **Read** on the share and NTFS to that Domain Local group. **No**, you couldn't use a Van Global group: Global groups only accept members from their **own** domain, and Global groups can't be nested across domains. (A Universal group in between, AGUDLP, would also work.)

</details>

---

## Multiple-Choice Quiz (15 Questions)

One correct answer per question. Try all 15 before opening the key.

**1.** How does a **distribution group** differ from a **security group**?

- A) It has no SID and can't be assigned permissions; it is only used as an email list.
- B) It can be assigned permissions but can't be used as an email list.
- C) It can never be converted into a security group.
- D) It is stored in the local SAM instead of AD.

**2.** Which FSMO role is the **time sync source** and handles **password changes and account lockout**?

- A) RID Master
- B) Infrastructure Master
- C) PDC Emulator
- D) Schema Master

**3.** How many FSMO role holders are there in a forest with **three domains**?

- A) 5
- B) 11
- C) 15
- D) 9

**4.** How often does the **KCC** automatically recalculate the replication topology?

- A) Every 5 minutes
- B) Every 60 minutes
- C) Once every 24 hours
- D) Every 15 minutes

**5.** Where is **Universal group membership** held, which is why every membership change creates forest-wide replication?

- A) In each computer's local SAM
- B) Only on the PDC Emulator
- C) In the Global Catalog
- D) In SYSVOL

**6.** Which command lists the DCs that currently hold the **FSMO roles**?

- A) `netdom query fsmo`
- B) `repadmin /replsum`
- C) `repadmin /kcc`
- D) `ntdsutil` → `metadata cleanup`

**7.** Which console do you use to manage the **Domain Naming Master** role?

- A) Active Directory Users and Computers
- B) Active Directory Sites and Services
- C) Active Directory Schema snap-in
- D) Active Directory Domains and Trusts

**8.** You suspect inbound replication on a DC is **stuck**. Which command shows its inbound replication queue?

- A) `repadmin /showobjmeta`
- B) `repadmin /queue`
- C) `repadmin /prp`
- D) `repadmin /syncall`

**9.** You just changed a site link and don't want to wait for the next automatic topology check. Which command forces the KCC to recalculate this DC's inbound topology **now**?

- A) `repadmin /replsum`
- B) `repadmin /showattr`
- C) `repadmin /queue`
- D) `repadmin /kcc`

**10.** Which command shows an object's attribute **change history**: version number, originating DC, timestamp and USNs?

- A) `repadmin /showobjmeta`
- B) `repadmin /showattr`
- C) `repadmin /showrepl *`
- D) `repadmin /replicate`

**11.** A user is added to a **security group** that has Read on a share, and the share's ACL is correct. The user, still logged on, still can't open the share. Why?

- A) The group must be converted to Universal first.
- B) ACL changes take 15 minutes to replicate.
- C) Group membership is evaluated at logon, so the user must log off and back on.
- D) Security groups can't be granted share permissions.

**12.** Can **ACIT Local** (Domain Local, `Adatum.com`) be nested inside **ACIT Universal** (Universal, `Adatum.com`)?

- A) Yes, Universal groups accept any group from any domain in the forest.
- B) No, Universal groups can't contain Domain Local groups.
- C) Yes, because both groups are in the same domain.
- D) No, but it would work if the groups were in different domains.

**13.** The DC holding the **PDC Emulator** role has died permanently and there is no backup. Users report time sync and password change problems. What do you do with the role?

- A) **Seize** it onto another DC using `ntdsutil`.
- B) **Transfer** it from the dead DC in ADUC → Operations Masters.
- C) Wait for the KCC to move it automatically.
- D) Run `repadmin /syncall` so the role replicates to another DC.

**14.** You force-removed a dead DC through ADUC, but clients keep trying to authenticate against it. What step was most likely missed?

- A) Raising the domain functional level
- B) Running `repadmin /prp` against a writable DC
- C) Converting the dead DC's groups to distribution groups
- D) Cleaning up its **DNS** A, NS and SRV records and checking Sites and Services for leftovers

**15.** An admin adds **500 users directly** to a Universal group, and GC replication traffic spikes every time someone joins or leaves. What does the guide recommend?

- A) Convert the Universal group to a Domain Local group.
- B) Make only one DC in the forest a Global Catalog.
- C) Put the users in Global groups and nest those Global groups in the Universal group, so its membership stays static.
- D) Convert the Universal group to a distribution group.

<details>
<summary><strong>Multiple-Choice Answer Key (click to expand)</strong></summary>

1. **A.** A distribution group is **not security enabled**: no SID, no permissions, email only. Either type can be converted into the other, and both are AD groups, not SAM groups.
2. **C.** The **PDC Emulator** handles time sync, password changes and account lockout. The RID Master hands out RID pools, and the Infrastructure Master updates cross-domain references.
3. **B.** 2 forest-wide roles + 3 per-domain roles × 3 domains = **11**. 5 is the count for a single-domain forest.
4. **D.** The KCC recalculates every **15 minutes**. You can force it sooner with `repadmin /kcc`.
5. **C.** Universal group membership is stored in the **Global Catalog**, so every change replicates to every GC. The local SAM holds only machine-local groups.
6. **A.** `netdom query fsmo` lists the role holders. `repadmin /replsum` summarises replication health, not role ownership.
7. **D.** The Domain Naming Master is managed in **AD Domains and Trusts**. ADUC manages the three domain roles, and the Schema snap-in manages the Schema Master.
8. **B.** `repadmin /queue` shows the inbound queue; items waiting is normal, but items stuck indefinitely or a very long queue means a problem. `/syncall` forces a sync rather than showing the queue.
9. **D.** `repadmin /kcc` forces the KCC to recalculate now instead of waiting up to 15 minutes. `/queue` only displays pending inbound items.
10. **A.** `/showobjmeta` shows the change history (version, originating DC, timestamp, GUID, USNs). `/showattr` shows the attributes' current values, which is the tempting distractor.
11. **C.** Membership is evaluated at **logon**, so the user must log off and on. Changes made directly on ACLs apply immediately, so B is wrong.
12. **B.** Universal groups contain users, computers, Global and Universal groups, but **no Domain Local groups**. Domain Local groups can only go inside other Domain Local groups in the same domain.
13. **A.** When the old holder is dead, you **seize** the role with `ntdsutil`. A transfer needs the old holder online, and roles don't move by replication or the KCC.
14. **D.** Even when the GUI cleans up metadata, records are left in **DNS** and **Sites and Services**, so clients keep finding the dead DC through stale SRV records. Clean them up after every forced removal.
15. **C.** Keep Universal membership **static** by nesting Global groups instead of adding users directly (AGUDLP). Converting to Domain Local or distribution would break the group's purpose, and fewer GCs would slow logons and searches.

</details>
