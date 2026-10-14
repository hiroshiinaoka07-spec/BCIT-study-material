# Group Nesting — Notes (ACIT3420)

> Source: `Group Nesting.mp4` (2:25, silent screen recording). Notes are written from what is shown on screen.
> Screenshots: `transcripts/Group Nesting/dense/` (one every 4 s).

## What the demo shows

A **Domain Local** group in a **child domain** (`BBY.Adatum.com`) gets **Global** and **Universal** groups from the **parent domain** (`Adatum.com`) as members. That's group nesting across domains in the same forest.

## Lab environment

| VM (VMware tab) | Role | Domain | Server name |
|---|---|---|---|
| `ACIT3420-DC` | Forest root DC (AD DS, DHCP, DNS, File and Storage) | `Adatum.com` | `CA-VAN-SVR1` |
| `ACIT3420Sub-DC` | Child domain DC | `BBY.Adatum.com` | `CA-BBY-S…` (cut off on screen) |
| `ACIT3420-Client` | Client | — | — |

Logged in as `ADATUM\administrator`.

## Groups that already exist

**Parent domain `Adatum.com`, OU `Downtown`:**

| Group | Scope |
|---|---|
| ACIT Universal | Security Group – Universal |
| ACIT Students | Security Group – Universal |
| ACIT Local | Security Group – Domain Local |
| ACIT Global | Security Group – Global |
| ACIT Faculty Global | Security Group – Global |

**Child domain `BBY.Adatum.com`, OU `BBY`:**

| Group | Scope |
|---|---|
| CIT Global | Security Group – Global |
| CIT Local | Security Group – Domain Local |
| CIT Universal | Security Group – Universal |

## Steps

1. **(0:00–0:40) Parent DC (`ACIT3420-DC`).** Sign in. Server Manager shows 3 stopped services flagged red (Sync Host, Downloaded Maps Manager, Google Update). These are unrelated "Automatic (Delayed Start)" noise; after a refresh the tiles go green.
2. **(~1:05) Parent DC.** Open **Tools → Active Directory Users and Computers**, then `Adatum.com → Downtown` to show the ACIT groups listed above.
3. **(~1:15) Switch to `ACIT3420Sub-DC`.** In ADUC, open `BBY.Adatum.com → BBY`.
4. **(~1:25) `CIT Local` → Properties → Members tab → Add…**
   - **From this location:** `Adatum.com`. Click **Locations…** to switch from the local `BBY.Adatum.com` domain to the parent domain.
   - Type `acit` and click **Check Names**. The **Multiple Names Found** dialog lists ACIT Faculty, ACIT Global, ACIT Students and ACIT Universal (all in `Adatum.com/Downtown`).
   - Select **ACIT Universal** and click OK.
5. **(~1:50) Add again.** Same process, this time selecting **ACIT Global**.
6. **(~2:10) Result.** `CIT Local` members:
   - `ACIT Global`, from `Adatum.com/Downtown`
   - `ACIT Universal`, from `Adatum.com/Downtown`

   Click Apply, then OK.

The ACIT Domain Local and ACIT Students groups were not added. The demo only uses the Global and Universal groups.

## Key concept: what can be nested where

| Group scope | Can contain | Can be a member of | Where it can be used for permissions |
|---|---|---|---|
| **Domain Local** | Users, **Global** and **Universal** groups from **any domain in the forest**, and other Domain Local groups from the **same** domain | Domain Local groups in the same domain | **Only its own domain** |
| **Global** | Users and Global groups from the **same domain only** | Global groups (same domain), Universal groups, Domain Local groups (any domain) | **Any domain** in the forest or trusting domains |
| **Universal** | Users, Global and Universal groups from **any domain in the forest** | Universal groups, Domain Local groups (any domain) | **Any domain** in the forest |

That's why the demo works: a Domain Local group (`CIT Local`) **can** accept Global and Universal groups from another domain (`Adatum.com`). It wouldn't work the other way round. `CIT Global` couldn't take `ACIT Global` as a member, because Global groups only accept members from their own domain.

### AGDLP (Microsoft's recommended strategy)

**A**ccounts go into **G**lobal groups, Global groups go into **D**omain **L**ocal groups, and you assign **P**ermissions to the Domain Local group.

- Global group = *who* (organised by role or department, e.g. ACIT Faculty).
- Domain Local group = *access to what* (e.g. access to a share in BBY).
- In multi-domain forests this becomes **AGUDLP**: Accounts → Global → **Universal** → Domain Local → Permissions.

## Exam-style takeaways

- Change the **Locations…** in the object picker to browse groups in another domain.
- Domain Local groups are the only scope that accepts Global groups from **other** domains.
- Global groups only take members from their **own** domain.
- Universal group membership is stored in the **Global Catalog**, so keep Universal membership stable (nest Global groups in it rather than individual users).
