# Week 5 Quiz — AWS CLI v2 & Bash

Sources: `aws-cli.md`, `aws-cli-exercise.md`, [GitLab: aws-cli-exercise-start](https://gitlab.com/cit_3640/aws-cli-exercise-start).

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** Why not install the AWS CLI from Debian's apt repo without checking?

- A) apt cannot install CLI tools
- B) Distro packages are often CLI v1 or an old v2; this course requires a current v2
- C) apt always installs to `~/.aws`
- D) The official installer does not work on Debian

**2.** `aws login` stores the region you type in:

- A) `~/.ssh/config`
- B) IAM user tags
- C) `~/.aws/config`
- D) `/etc/aws/region`

**3.** `--query` uses:

- A) jq
- B) SQL
- C) JMESPath
- D) grep

**4.** `import-key-pair` uses `fileb://` because:

- A) The private key must be uploaded
- B) The file is read as raw binary with no extra encoding
- C) `file://` only works inside S3
- D) It enables MFA on the key

**5.** Inside a VM you authenticate with:

- A) `aws login --remote`
- B) `aws login --profile remote`
- C) root user credentials
- D) `aws configure sso` only

---

## Short Answer

**6.** Label each token:

```bash
aws ec2 describe-key-pairs --output yaml
```

List the four valid `--output` values.

**7.** What does `set -euo pipefail` do, piece by piece? Why does the import script still survive `if aws ec2 describe-key-pairs … &>/dev/null` when the key is missing?

**8.** Explain this query in four parts. What does it print?

```bash
aws ec2 describe-key-pairs \
  --query 'KeyPairs | sort_by(@, &CreateTime) | [-1].KeyName' \
  --output text
```

**9.** The notes show `./script ~/.ssh/aws` as the example invocation. What is wrong with that path, and what should you pass?

---

## Hands-on / Scenario

**10.** Rewrite the Debian AMI lookup so a script stores **only the newest ImageId** and writes `debian_ami=ami-…` via a heredoc. Keep owner `136693071363`.

**11.** Complete the three TODOs from GitLab `create-instance` (run-instances, public IP, heredoc). Use variables already in that script (`$debian_ami`, `$key_name`, `$subnet_id`, `$security_group_id`, `$region`).

**12.** `create-vpc` must produce a **public** subnet. List the CLI calls that (a) enable public IPv4 on the subnet and (b) send `0.0.0.0/0` to the internet. What file do later scripts `source`?

---

## Answer Key

**1. B.** Official install: `curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash` → `~/.local/bin`. Confirm with `aws --version` (`aws-cli/2.x`). Fedora 44 is the notes' exception with a recent package.

**2. C.** Plain-text INI. Short-term credentials also land under `~/.aws/`. Sign in as the **IAM user, never root**.

**3. C.** JMESPath. `jq` is a separate tool (Week 7 `backup-info` uses it on `s3api` JSON).

**4. B.** `file://` applies normal CLI encoding; `fileb://` is raw binary — required for `--public-key-material`. Never upload the private key.

**5. A.** `--remote` is for environments without a local browser hand-off. `--profile` selects a named credential set; it is not a substitute.

**6.** `aws` = base; `ec2` = top-level service; `describe-key-pairs` = operation; `--output yaml` = option. Outputs: `json` (default), `yaml`, `text`, `table`.

**7.** `-e` exit on error; `-u` unset variables are errors; `-o pipefail` a pipeline fails if any stage fails. Commands in an `if` test do **not** trigger `-e`; a missing key makes `describe-key-pairs` fail, the `if` is false, and the script continues into `import-key-pair`. `&>/dev/null` discards stdout and stderr so only the exit code is used.

**8.** Take `KeyPairs` → sort by `CreateTime` ascending → last element (`[-1]`) = newest → `.KeyName` as plain text. `[0].KeyName` after the same sort would be the **oldest**.

**9.** `~/.ssh/aws` is the **private** key. Pass `~/.ssh/aws.pub`. The script already prefixes `fileb://`.

**10.**

```bash
#!/usr/bin/env bash
set -euo pipefail

debian_ami=$(aws ec2 describe-images \
  --owners 136693071363 \
  --filters \
    "Name=name,Values=debian-13-amd64-*" \
    "Name=architecture,Values=x86_64" \
    "Name=root-device-type,Values=ebs" \
    "Name=free-tier-eligible,Values=true" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --output text)

cat > ami_data <<EOF
debian_ami=${debian_ami}
EOF
```

Unquoted `EOF` expands `${debian_ami}`. Verify the owner ID on the Debian wiki, do not scrape it blindly.

**11.**

```bash
instance_id=$(aws ec2 run-instances \
  --image-id "$debian_ami" \
  --instance-type t3.micro \
  --key-name "$key_name" \
  --subnet-id "$subnet_id" \
  --security-group-ids "$security_group_id" \
  --user-data file://cloud-init.yaml \
  --query 'Instances[0].InstanceId' \
  --output text \
  --region "$region")

public_ip=$(aws ec2 describe-instances \
  --instance-ids "$instance_id" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text \
  --region "$region")

cat > instance_data <<EOF
instance_id=$instance_id
public_ip=$public_ip
security_group_id=$security_group_id
EOF
```

`--user-data` uses **`file://`** (text YAML), not `fileb://`. `aws ec2 wait instance-running` should run before you query the public IP. Key name is **`bcitkey`** — Week 7 EFS lab reuses it.

**12.** (a) `aws ec2 modify-subnet-attribute --map-public-ip-on-launch`. (b) `aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id "$igw_id"` on the route table associated with that subnet (after `create-internet-gateway` + `attach-internet-gateway`). Later scripts `source ./infrastructure_data` for `vpc_id`, `subnet_id`, etc.
