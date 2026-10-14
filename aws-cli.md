# Getting started with the AWS CLI


> [!warning] AWS CLI v1 and v2
> There are two version of the AWS CLI and the top level command for both is `aws`. We are going to be using version 2.
> If you install The AWS CLI using your distros package manager double check that you are installing version 2. Many distros only have version 1 in their package repositories.
> The notes below are specific to version 2.
> 

> The AWS Command Line Interface (AWS CLI) is an open source tool that enables you to interact with AWS services using commands in your command-line shell. With minimal configuration, the AWS CLI enables you to start running commands that implement functionality equivalent to that provided by the browser-based AWS Management Console from the command prompt in your terminal program.
> - AWS Command Line Interface

The AWS CLI can be used to create and discover resources. 

While you can use the AWS CLI to provision complex infrastructure in your AWS environment. Where I find it really shines is in running common tasks that can be scripted for convenience. This includes things, like adding an SSH key to your AWS account, or checking to see what the name of the most recently added keypair is.

```bash
aws ec2 describe-key-pairs \
  --query 'KeyPairs | sort_by(@, &CreateTime) | [-1].KeyName' \
  --output text
```
## Installing 

Before installing from a package manager double check that your distros package is:
- version 2, not version 1
- A relatively recent release (The current version is 2.37.4)

Fedora 44 has a relatively recent version. For other distros I recommend installing manually.

### manual installation

Use `curl` to download and run the install script
```bash
curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash
```

This will install to `$HOME/.local/bin`. If this directory isn't already in your PATH you will need to add it to your PATH.

To test that you have installed the `aws` tool, run the command:
```bash
aws --version
```

**Reference:**
- [AWS CLI install instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Installing command completion (optional)

The aws-cli package includes a very useful command completion feature. This feature is not automatically installed so you need to configure it manually. To enable tab completion for bash either use the built-in command `complete`:
```bash
complete -C aws_completer aws
```

Or add `bin/aws_bash_completer` file under `/etc/bash_completion.d`, `/usr/local/etc/bash_completion.d` or any other `bash_completion.d` location.
## Configuration and set up

After installing the AWS CLI we can set up authentication and some configuration.

The AWS CLI stores credential and configuration information in the  `~/.aws` directory. Configuration is stored in an INI style format and can be kept in "profiles". Profiles allow you to create separate credentials and configuration for different accounts, or activities. 

If you don't need to create separate profiles you can use the default profile. If you are in a group that is planning to use AWS for ISSP project for example, you may want a separate profile.

Like most of the things we have done with AWS there are a few ways that we could authenticate and configure the AWS CLI.

Most of the methods have theirown pros and cons. For now at least we are going to use the simplest method.

### Console session as short-term credentials

Simply open up a terminal and run the command
```bash
aws login
```

If you are working in a VM run the command:
```bash
aws login --remote
```

This will open your default browser, if it isn't already open, and require you to login using the web console, just like we have been doing in class. If you already logged-in this will still work, it just means that you have already completed a step.

> [!warning] Don't login as the root user
> Login using the IAM user we created in week 1.

This will prompt you for an AWS Region
```
AWS Region [us-east-1]: 
```

Set the value to `us-west-2`. This will be stored in `~/.aws/config`. This is just a plain text file, so you can always edit it later.

This will also create short term credentials that will be store in `~/.aws/`. In general you don't need to manually do anything with the credential files created by AWS.

The big advantage of this that it is pretty easy. You don't have to create new credentials, and you are creating resources using the permissions you set up with your IAM user. 

Another nice thing about this is that at least initially I think it is a good idea to keep the web console open. That way you can look at your account and see which resources you are creating.

#### Next login

In the future when you type:
```bash
aws login
```

You will still login through a web console using your AWS IAM User, this will create new short term credentials, but you won't have to configure anything.

The downside is that you still have to login using the web console. 

Later we might look at long-term credentials or using an IAM Identity Center User. This is a separate user from the IAM User we created in week 1. 

**Reference:**
- [Setting up the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
- [Configuration and credential file settings in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

## Learning to use the AWS CLI

AWS CLI commands take the format:
```
# base command, top-level command, sub-command,       options
  aws           ec2                describe-key-pairs --output text
```

The general aws command structure is:

- base command `aws`
- top-level command, this usually corresponds to an aws service, eg `ec2`
- sub-command, this specifies an operation to perform, eg `describe-key-pair`
- aws cli options, `--output text`

Generally the sub-commands use the same language as the web console.

For example:
- `create-key-pair` Will create a new SSH key pair.
- `import-key-pair` Will import a local keypair.
- `delete-key-pair` Will (you probably guessed this one), delete a keypair.

Let's look at a more concrete example.

In the third week you had to import an SSH key pair that you created in your local Linux environment. Let's first find that key pair, then delete it, then add a new key.

To find the key you imported in week 3
Run the following command
```bash
aws ec2 describe-key-pairs --output yaml # the default output is JSON
```

You should see something that looks like:
```
KeyPairs:
- CreateTime: '2026-09-20T22:28:04.792000+00:00'
  KeyFingerprint: XJxIQX+JEMBZNlq3TIdtrcp0twH4onuYL+5BVSuALCI=
  KeyName: bcit-demo
  KeyPairId: key-03ae06856396559ae
  KeyType: ed25519
  Tags: []
```

We can then use this data to delete that key. The name and ID are both good choices for identifying the key we want to delete.

The command below will search for the "KeyName" value and only returns the ID
```bash
aws ec2 describe-key-pairs \
  --key-names "bcit-demo" \
  --query 'KeyPairs[0].KeyPairId' \
  --output text
```

If I wanted to print all of the keys names I could use this command:
```bash
aws ec2 describe-key-pairs   --query 'KeyPairs[*].KeyName' --output text
```

Notice in both cases we are querying nested data. 'describe-key-pairs' returns a YAML mapping.  

We can delete the key with the command:
```bash
aws ec2 delete-key-pair --key-name "bcit-demo"
```

This will return either an error or info about the key we are deleting.

```
{
    "Return": true,
    "KeyPairId": "key-03ae06856396559ae"
}
```

Try running the 'describe-key-pairs' command above again.

Finally let's import another key. This can be the same key you created last week. If you had to look up the command to create an SSH key pair, or you had difficulty with that part last week it may not be a bad idea to create a new local key pair.

The command below assumes that you created a key "aws" in `~/.ssh`.
```bash
aws ec2 import-key-pair --key-name "bcit-demo" --public-key-material fileb://~/.ssh/aws.pub
```

a note on "fileb"
AWS CLI has two related URI prefixes:
- `file://` — reads a file and applies the CLI's normal parameter encoding/handling.
- `fileb://` — reads the file **as raw binary data**, without any encoding.

#### Import a key in a reusable script

All of that is great, but it does require you to look up or remember aws commands. The real advantage of the AWS CLI is that you can store these commands in simple Bash scripts to reuse as needed.

The script below will take the path to your public key and store that in the variable "public_key_file". It does what the command above does, but before that it checks that the key file exists. So you would run this script like so:

```bash
./script ~/.ssh/aws
```

The script below will also write out data to a "key_data" file that will be created in the directory where this script is run.

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
### Getting help

AWS provides an online [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/) that is a handy tool for working with the AWS CLI. This shows you top-level commands, sub-commands, and their options as well as examples of the sub-commands.

Getting help in the command line. This shows you the same info as what can be found in the web at the URL above.

```bash
aws help
aws ec2 help
```
