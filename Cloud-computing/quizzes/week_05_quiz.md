# Week 5 Quiz — CLI labs: `if`, `$( )`, heredocs

Sources: `aws-cli.md`, `aws-cli-exercise.md`, [GitLab: aws-cli-exercise-start](https://gitlab.com/cit_3640/aws-cli-exercise-start).

**Midterm focus (not Chapter 5):** command substitution, heredocs, and the `if` statements in the lab scripts.

Attempt all questions before opening the answer key.

---

## Multiple Choice

**1.** After this runs, what is in `settings`?

```bash
latest="bcit-demo"
cat > settings <<EOF
latest_key=${latest}
EOF
```

- A) `latest_key=${latest}`
- B) `latest_key=bcit-demo`
- C) `latest_key=`
- D) Nothing; `cat` prints to the terminal

**2.** Same body, but the delimiter is quoted. What is in `settings`?

```bash
latest="bcit-demo"
cat > settings <<'EOF'
latest_key=${latest}
EOF
```

- A) `latest_key=bcit-demo`
- B) `latest_key=${latest}`
- C) A Bash error: quoted EOF is illegal
- D) `latest_key=`

**3.** What does `debian_ami=$(aws ec2 describe-images … --query 'sort_by(Images, &CreationDate)[-1].ImageId' --output text)` store?

- A) A YAML table of every Debian AMI
- B) The newest ImageId as a bare string, e.g. `ami-0b3c68efb8f9567ef`
- C) The newest ImageId still wrapped in JSON quotes
- D) The contents of `ami_data`

**4.** You run the import script as `./script` (no arguments). Which `if` fires, and what happens?

```bash
if [[ $# -ne 1 ]]; then
  err "Script requires the path to the public key file you would like to import."
fi
if [[ ! -f "$1" ]]; then
  err "Path to public key for import is incorrect; file does not exist."
fi
```

- A) The file check, because `$1` is empty
- B) The `$# -ne 1` check; `err` prints to stderr and the script exits 1. The file check never runs
- C) Neither; `set -e` aborts first
- D) Both, and both error messages print

**5.** `bcitkey` already exists. What does this do?

```bash
if aws ec2 describe-key-pairs --key-names "$key_name" &>/dev/null; then
  err "Key pair '$key_name' already exists in AWS. …"
fi
```

- A) `describe-key-pairs` succeeds (exit 0), `if` is true, `err` runs, no import
- B) `describe-key-pairs` succeeds, so `set -e` kills the script with a raw AWS error
- C) `&>/dev/null` makes the command fail, so the script imports a duplicate
- D) The `if` only looks at stdout, which was discarded, so it always imports

---

## Short Answer

**6.** In one sentence each: what is command substitution, what is a heredoc, and why do the labs use them *together*?

**7.** Translate each test into English.

```bash
[[ $# -ne 1 ]]
[[ ! -f "$1" ]]
[[ -z "$availability_zone" || "$availability_zone" == "None" ]]
[[ ! -f "infrastructure_data" ]]
```

**8.** Why `&>/dev/null` on the `describe-key-pairs` `if`? Why does a *missing* key **not** abort the script even with `set -e`?

**9.** The starter `--query` is `'sort_by(Images, &CreationDate)[*].[ImageId,Name,CreationDate]'`. What do you change for the exercise, and why would leaving the table in the substitution break `run-instances --image-id "$debian_ami"`?

---

## Hands-on / Scenario

**10.** Write the AMI exercise: newest ID only, command substitution, heredoc file that looks like `debian_ami=ami-…`. Owner `136693071363`.

**11.** Trace this run and state which `if` (if any) stops it:

```bash
./script /tmp/does-not-exist.pub
```

Assume the script is the import-key script from `aws-cli-exercise.md`.

**12.** Complete the `create-instance` heredoc and the two substitutions it depends on. Then say what `source ./instance_data` would give a later script.

```bash
instance_id=$(     )     # run-instances
public_ip=$(       )     # describe-instances
cat > instance_data <<EOF
# three KEY=value lines
EOF
```

---

## Answer Key

**1. B.** Unquoted `EOF` expands `${latest}`. `cat > settings` writes a file, not the terminal.

**2. B.** Quoted `'EOF'` is literal — no expansion. That is the wrong form for lab data files you later `source`.

**3. B.** `[-1].ImageId` plus `--output text` → one bare ID. The starter query's `[*].[ImageId,Name,CreationDate]` is the table you are supposed to get rid of.

**4. B.** `$#` is 0, so `-ne 1` is true. `err` calls `exit 1`. The `-f` test is never reached.

**5. A.** `if cmd` is true on exit 0. Existing key → describe succeeds → `then`/`err`. `set -e` does not apply to commands in `if` tests. `&>/dev/null` hides output only.

**6.** Command substitution `$(cmd)` captures stdout into a variable. A heredoc (`cat > file <<EOF … EOF`) writes a multi-line file, expanding variables if the delimiter is unquoted. Labs capture IDs with `$(aws …)` then persist them with a heredoc so the next script can `source` the file.

**7.**
- Not exactly one argument.
- `$1` is missing or not a regular file.
- AZ string is empty, or AWS printed `None`.
- `infrastructure_data` is not a file in the current directory (you forgot `create-vpc`).

**8.** You only want the exit code: success = key exists, failure = safe to import. The JSON and the "not found" error would clutter the terminal. `set -e` ignores failures in `if`/`while` tests, which is how a missing key is allowed to continue into `import-key-pair`.

**9.** Change it to `'sort_by(Images, &CreationDate)[-1].ImageId'` (drop `[*].[…]`). Leaving the table means `$debian_ami` holds several columns/rows; `--image-id` expects a single ID and will error.

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

**11.** `$#` is 1, so the argument-count `if` passes. `[[ ! -f "$1" ]]` is true (file does not exist) → `err` about the path → exit 1. AWS is never called.

**12.**

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

`source ./instance_data` sets those three variables in the current shell (same pattern as `source ./infrastructure_data` after `create-vpc`).
