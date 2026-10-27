# AWS CLI exercise

## Create an EC2 instance using the AWS CLI Part 1

### Get Debian AMI ID

This will return several AMI IDs along with the name and creation date.

**Tasks:**
Convert the code snippet below to a Bash script that will: 
- only get the most recent AMI ID. Just a single ID, without name and creation date
- store the value(the AMI ID) in a variable using command substitution
- write the value to a file using a heredoc

```bash
aws ec2 describe-images \
    --owners 136693071363 \
    --filters \
        "Name=name,Values=debian-13-amd64-*" \
        "Name=architecture,Values=x86_64" \
        "Name=root-device-type,Values=ebs" \
        "Name=free-tier-eligible,Values=true" \
    --query 'sort_by(Images, &CreationDate)[*].[ImageId,Name,CreationDate]' \
    --output text
```

The file produced by your heredoc should look a little like:
```
debian_ami=ami-0b3c68efb8f9567ef
```

In addition to the AWS CLI command information, this command requires that you look up the account ID `--owners 136693071363`. For Debian this is available in the Debian Wiki under [Cloud AmazonEC2Image](https://wiki.debian.org/Cloud/AmazonEC2Image)

You can programmatically access this information, but this is one of those things that is better verified by hand. Fortunately most Linux distros publish this information somewhere in there documentation.

**Reference:**
- [Did you forget about command substitution?](https://www.golinuxcloud.com/bash-command-substitution/)
- [Did you forget about heredocs?](https://linuxize.com/post/bash-heredoc/)
### Import an SSH key into your AWS account

This script takes the path to a public key as an argument and will import that public key into your AWS account under the name "bcitkey".

```bash
#!/usr/bin/env bash

set -euo pipefail

# Function to handle errors
err() {
  local error_message="$*"
  echo -e "\033[1;31m ERROR:\033[0m ${error_message}" >&2
  exit 1
}

# Define variables
key_name="bcitkey"
public_key_file=""

# Check arguments
if [[ $# -ne 1 ]]; then
  err "Script requires the path to the public key file you would like to import."
fi

# Check if the public key file is a regular file
if [[ ! -f "$1" ]]; then
  err "Path to public key for import is incorrect; file does not exist."
else
  public_key_file="$1"
fi

# Check if key already exists to prevent duplicate errors
if aws ec2 describe-key-pairs --key-names "$key_name" &>/dev/null; then
  err "Key pair '$key_name' already exists in AWS. Delete it first or use a different name."
fi

echo "Importing public key into AWS account..."
aws ec2 import-key-pair \
  --key-name "$key_name" \
  --public-key-material fileb://"$public_key_file" > key_data

echo "Key imported successfully. Details saved to 'key_data'."
```