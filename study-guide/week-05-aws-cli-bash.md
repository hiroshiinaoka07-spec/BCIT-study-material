# Week 5 — Automating AWS with the CLI & Bash

## Learning Objectives

By the end of this week you should be able to:

1. **Install and authenticate AWS CLI v2** in your Linux environment as your IAM user.
2. **Read and write CLI commands** — including `--query` filters and `--output` formats — to find, create, and delete resources.
3. **Write safe, reusable Bash scripts** around AWS CLI commands (strict mode, argument checks, error handling, command substitution, heredocs).

---

## Key Concepts & Deep Dive

### 1. Why the CLI?

Anything you click in the console, you can do from the terminal. Where the CLI really shines (per `aws-cli.md`) is **scripting common tasks** — importing SSH keys, finding the latest key pair or AMI — so you never have to click through them again. It's your first real step toward Infrastructure as Code.

### 2. Installing — make sure it's version 2

⚠️ v1 and v2 both use the `aws` command. **This course uses v2**, and many distro package repositories (including Debian's) only ship v1 or an old v2.

```bash
curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash   # installs to ~/.local/bin
aws --version                                                    # confirm it says aws-cli/2.x
```

If `aws` isn't found, add `$HOME/.local/bin` to your `PATH`.

Optional tab completion:

```bash
complete -C aws_completer aws
```

### 3. Authenticating with `aws login`

```bash
aws login            # opens your browser
aws login --remote   # use this inside a VM
```

- Sign in as your **IAM user from Week 2 — never root.**
- When prompted for a region, enter **`us-west-2`**. It's stored in the plain-text file **`~/.aws/config`**.
- You get **short-term credentials**, stored under `~/.aws/` — no long-lived access keys to leak.
- Future sessions: just run `aws login` again; no reconfiguration.

**Profiles** let you keep separate credentials/config for different accounts or projects (e.g. a group ISSP account). For now, the default profile is fine.

### 4. Anatomy of a command

```
aws   ec2          describe-key-pairs   --output text
 │     │                  │                  │
base  top-level        sub-command         options
      (service)        (operation)
```

Sub-commands mirror console language: `create-key-pair`, `import-key-pair`, `delete-key-pair`, `describe-…`.

Help is built in:

```bash
aws help
aws ec2 help
```

### 5. Filtering output with `--query` and `--output`

`--output` controls the format: `json` (default), `yaml`, `text`, `table`.
`--query` uses **JMESPath** to pull out exactly what you need — essential for scripts.

```bash
# Everything about your key pairs, as YAML
aws ec2 describe-key-pairs --output yaml

# Just the ID of the key named "bcit-demo"
aws ec2 describe-key-pairs \
  --key-names "bcit-demo" \
  --query 'KeyPairs[0].KeyPairId' \
  --output text

# All key names
aws ec2 describe-key-pairs --query 'KeyPairs[*].KeyName' --output text

# Name of the MOST RECENT key pair
aws ec2 describe-key-pairs \
  --query 'KeyPairs | sort_by(@, &CreateTime) | [-1].KeyName' \
  --output text
```

JMESPath cheat sheet for these examples:

| Expression | Meaning |
| ---------- | ------- |
| `KeyPairs[0]` | First item in the list |
| `KeyPairs[*].KeyName` | `KeyName` of every item |
| `sort_by(@, &CreateTime)` | Sort the current list (`@`) by `CreateTime` |
| `[-1]` | Last item (after sorting ascending = newest) |
| `\|` | Pipe the result into the next expression |

### 6. `file://` vs `fileb://`

```bash
aws ec2 import-key-pair --key-name "bcit-demo" \
  --public-key-material fileb://~/.ssh/aws.pub
```

- `file://` — reads the file and applies the CLI's normal parameter encoding.
- `fileb://` — reads the file as **raw binary**, with no encoding. Required here for the key material.

### 7. A production-quality Bash script

The key-import script from `aws-cli.md` / `aws-cli-exercise.md` shows the patterns you should reuse in every script:

```bash
#!/usr/bin/env bash

set -euo pipefail

# Function to handle errors
err() {
  local error_message="$*"
  echo -e "\033[1;31m ERROR:\033[0m ${error_message}" >&2
  exit 1
}

key_name="bcitkey"
public_key_file=""

if [[ $# -ne 1 ]]; then
  err "Script requires the path to the public key file you would like to import."
fi

if [[ ! -f "$1" ]]; then
  err "Path to public key for import is incorrect; file does not exist."
else
  public_key_file="$1"
fi

if aws ec2 describe-key-pairs --key-names "$key_name" &>/dev/null; then
  err "Key pair '$key_name' already exists in AWS. Delete it first or use a different name."
fi

echo "Importing public key into AWS account..."
aws ec2 import-key-pair \
  --key-name "$key_name" \
  --public-key-material fileb://"$public_key_file" > key_data

echo "Key imported successfully. Details saved to 'key_data'."
```

Pattern by pattern:

| Line | Pattern | Why |
| ---- | ------- | --- |
| `#!/usr/bin/env bash` | Portable shebang | Finds `bash` wherever it's installed |
| `set -euo pipefail` | **Strict mode** | `-e` exit on any error; `-u` error on unset variables; `-o pipefail` a pipeline fails if *any* part fails |
| `err() { … >&2; exit 1; }` | Error helper | Red "ERROR" message to **stderr**, then stop |
| `[[ $# -ne 1 ]]` | Argument check | Exactly one argument required |
| `[[ ! -f "$1" ]]` | File check | Fail early with a clear message |
| `if aws … &>/dev/null` | Idempotency guard | Silences all output; uses only the exit code to see if the key already exists |
| `> key_data` | Redirect | Saves AWS's JSON response for later use |

Run it with:

```bash
./script ~/.ssh/aws.pub
```

> Note: `aws-cli.md` shows the example as `./script ~/.ssh/aws`. Since the script imports a **public** key, pass the `.pub` file — never upload your private key.

### 8. Two Bash tools for the exercise

```bash
# Command substitution — capture a command's output in a variable
latest=$(aws ec2 describe-key-pairs --query 'KeyPairs[-1].KeyName' --output text)

# Heredoc — write multi-line text to a file, with variables expanded
cat > settings <<EOF
latest_key=${latest}
EOF
```

---

## Repository Tour

| File | What to look for |
| ---- | ---------------- |
| `aws-cli.md` | v1 vs v2 warning, install, completion, `aws login`, `~/.aws` config, command structure, key pair describe/delete/import, `file://` vs `fileb://`, the import script, getting help |
| `aws-cli-exercise.md` | Exercise: turn the Debian AMI lookup into a script (latest ID only → variable → heredoc file); the key-import script |
| `aws-ec2.md` | Where the SSH key you're importing was created (Week 3) |

---

## Practical Takeaways — Why This Matters

- **Repeatability beats memory.** A 20-line script that's been tested is more reliable than remembering a dozen console clicks during an outage.
- **Strict mode prevents silent disasters.** Without `set -e`, a failed command can let the script keep going and create (or delete) the wrong things.
- **Idempotency is a core DevOps idea.** Checking "does this already exist?" before creating it means you can safely run a script twice — the same idea Terraform/OpenTofu is built on.
- **`--query` makes AWS composable.** Pulling out a single ID lets you chain commands: find the AMI → launch an instance → tag it, all in one script.

---

## Knowledge Check

**Q1 (Multiple choice).** Why does the course warn against installing the AWS CLI with your distro's package manager?

- A) Package managers can't install command-line tools
- B) The packaged version is often v1 or an outdated v2
- C) The packaged version only works with the root user
- D) It installs the CLI to `~/.aws`

**Q2 (Multiple choice).** You run `aws login` and choose `us-west-2`. Where is that region setting saved?

- A) `~/.ssh/config`
- B) `/etc/aws/region`
- C) `~/.aws/config`
- D) In your IAM user's settings in the AWS console

**Q3 (Code reading).** What exactly does this command print? Explain each part of the query.

```bash
aws ec2 describe-key-pairs \
  --query 'KeyPairs | sort_by(@, &CreateTime) | [-1].KeyName' \
  --output text
```

**Q4 (Fill in the blank).** In the key-import script:
- `set -euo pipefail`: `-e` makes the script ________ when a command fails; `-u` makes using an ________ variable an error; `pipefail` makes a pipeline fail if ________ command in it fails.
- In `if aws ec2 describe-key-pairs --key-names "$key_name" &>/dev/null`, the `&>/dev/null` discards both ________ and ________, so the `if` only looks at the command's ________.

**Q5 (Scenario).** This is the exercise from `aws-cli-exercise.md`. Starting from the Debian AMI lookup command, write a Bash script that (1) gets **only the most recent** AMI ID, (2) stores it in a variable with command substitution, and (3) writes `debian_ami=<id>` to a file using a heredoc. Which part of the original command do you change, and why?

<details>
<summary><strong>Answer Key (click to expand)</strong></summary>

**Q1 — B).** Many distros (Debian included) only have v1, or an old v2, in their repos. The notes recommend the official install script; Fedora 44 is the exception with a recent package.

**Q2 — C) `~/.aws/config`.** It's a plain-text INI-style file you can edit later. Short-term credentials are also stored under `~/.aws/`.

**Q3** — It prints the **name of the most recently created key pair** as plain text.
- `KeyPairs` — take the list of key pairs
- `| sort_by(@, &CreateTime)` — sort that list (`@`) by creation time, oldest → newest
- `| [-1]` — take the last element (the newest)
- `.KeyName` — return only its name
- `--output text` — no JSON quotes, so it's easy to use in a script

**Q4** — **exit**; **unset** (undefined); **any**. Then: **stdout**; **stderr**; **exit code** (success means the key exists, which triggers the error).

**Q5** — Change the **`--query`** so it sorts by date and takes only the last element's ID, instead of returning every `[ImageId,Name,CreationDate]` row:

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

- `sort_by(Images, &CreationDate)` sorts oldest → newest, and `[-1].ImageId` picks just the newest ID.
- `$( … )` is command substitution: it captures the output into `debian_ami`.
- `cat > ami_data <<EOF … EOF` is the heredoc; `${debian_ami}` is expanded because the `EOF` delimiter isn't quoted.
- `--owners 136693071363` stays: it's Debian's official account ID, which the notes say to verify by hand on the Debian wiki.

</details>
