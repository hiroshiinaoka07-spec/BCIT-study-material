# ACIT 3420 Windows Server Administration: Weeks 3–4 Study Guide

Module 3–4: **Installing and Configuring Domain Controllers** (Lei "Johnny" Zhang)

| Week | File | Covers |
|---|---|---|
| **3** | [week-03-active-directory-and-domain-controllers.md](week-03-active-directory-and-domain-controllers.md) | AD DS terms, partitions and `ntds.dit`, OUs/domains/trees/forests, sites, GC, functional levels, deploying an additional DC, child domain and tree domain, DNS SRV records and conditional forwarders, IFM, RODC, cloning, AD DS vs Azure AD |
| **4** | [week-04-groups-fsmo-replication-troubleshooting.md](week-04-groups-fsmo-replication-troubleshooting.md) | Group types and scopes, nesting rules, AGDLP/IGDLA, **the 10 slide questions answered**, FSMO roles, replication and KCC, `repadmin`, forced DC removal / `ntdsutil` metadata cleanup |

Lab notes: [`../second-dc-subdomain-domain-tree-notes.md`](../second-dc-subdomain-domain-tree-notes.md), [`../group-nesting-notes.md`](../group-nesting-notes.md)

---

## Last-minute cheat sheet

**AD DS** = directory that **stores identities**, does **authentication** (Kerberos) and **authorization**. Multi-master; at least 2 DCs per domain.

**Structure:** OU (inside a domain; delegation and GPOs) → **Domain** (security, admin and replication boundary) → **Tree** (contiguous namespace, shared root) → **Forest** (shared schema, configuration and GC; first domain = forest root). Children **don't inherit** the parent's policies. Trusts within a forest are **two-way transitive**.

**Physical:** **Site** = well-connected IP subnets; used for replication and finding the closest DC; one **bridgehead** per site. Contains only **servers and configuration objects**.

**Partitions** (all in `ntds.dit`): **Schema** and **Configuration** go forest-wide; **Domain** stays in its own domain; **Application** (DNS zones) goes where configured.
Files in `C:\Windows\NTDS`: `ntds.dit`, `EDB*.log` (transaction logs), `EDB.chk` (checkpoint), `Edbres0000x.jrs` (2 × 10 MB reserve for a full disk). SYSVOL is at `C:\Windows\SYSVOL`.

**Schema snap-in:** `regsvr32 schmmgmt.dll` → `mmc` → add *Active Directory Schema*.

**GC:** partial copy of all forest objects; used for logon, forest-wide search and Universal group membership; port **3268**.

**Ports:** LDAP **389** · Kerberos **88** · kpasswd **464** · GC **3268**

**Promotion:** install the role → *Promote this server*. The three options:
- *Add a DC to an existing domain*
- *Add a new domain to an existing forest* → **Child** (Parent + New name) or **Tree** (Forest name + New name)
- *Add a new forest*

Before promoting: **static IP + DNS pointing at an existing DC**. Set a DSRM password. Use Enterprise Admin credentials for new domains.

**Child vs tree DNS:** a child gets an **automatic delegation**. A tree has no parent zone, so **set up a conditional forwarder** (e.g. `Indy.com → 192.168.239.4` on the Adatum DNS).

**Upgrade path:** only 2008 R2 SP1, 2012 and 2012 R2 → 2019. **IFM** = `ntdsutil` media, so a new DC doesn't replicate the full database over the WAN. **RODC** = read-only, for insecure sites, PRP-cached passwords. **Cloning** = Server 2012+, virtual DCs.

**Group types:** Security (SID, permissions) vs Distribution (email only, no SID). They can be converted either way.

**Group scopes:**
- **Global:** members from the **same domain**; usable **anywhere**
- **Domain Local:** members from **anywhere**; usable only in its **own domain**
- **Universal:** members from **any domain** (no DL); usable **forest-wide**; stored in the GC, so keep membership static
- **Local:** SAM; this machine only

**Nesting:** G→G (same domain) ✅ · G→U ✅ · G→DL ✅ · U→U ✅ · U→DL ✅ · U→G ❌ · DL→G/U ❌ · G across domains ❌ · DL from another domain into DL ❌

**AGDLP / IGDLA:** Accounts → Global → Domain Local → Permissions (add Universal in between for multi-domain).

**FSMO (5):** forest-wide: **Schema Master** (Schema snap-in), **Domain Naming Master** (Domains and Trusts). Domain-wide: **PDC Emulator** (time, passwords, lockout), **RID Master** (RID pools), **Infrastructure Master** (cross-domain references); all three in ADUC. Check with `netdom query fsmo`.

**repadmin:** `/replsum` (first; RODCs only under Destination) · `/showrepl *` (detail) · `/queue` · `/kcc` (KCC runs every 15 min) · `/replicate` · `/syncall` (`/a /h /i /s /q`; default NC = configuration) · `/prp` (RODC password policy; run on a writable DC; can't edit the Deny list) · `/showattr` (389/3268) · `/showobjmeta` (versions, USNs)

**Dead DC removal:** try a demote first. Then use ADUC (Delete → *"Delete this DC anyway…"* → GC/FSMO prompts) **or** Sites and Services (delete NTDS Settings, then the server) **or** `ntdsutil` → `metadata cleanup` → connections → select operation target → `remove selected server`. **Then clean up DNS.**

**Azure:** AD DS = on-prem, Kerberos/NTLM, GPO. Azure AD = cloud, OAuth/OIDC, Intune MDM, no GPO. Azure AD DS = managed domain in Azure with Kerberos/NTLM/GPO, but **no schema extensions and no Domain/Enterprise Admin**.
