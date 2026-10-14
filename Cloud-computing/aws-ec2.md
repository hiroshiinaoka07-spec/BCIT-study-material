# AWS EC2 lab resources

## SSH key review

Create an SSH key pair
```bash
ssh-keygen -f .ssh/aws -C "aws lab key"
```

Connect to a server
```bash
ssh -i .ssh/aws admin@<ip-address> # admin is the default user on AWS Debian AMIs
```

Remove a host from your `~/.ssh/known_hosts` file
```bash
ssh-keygen -R <host> # host name, ip address...
```

## cloud-init review

> `Cloud-init` is the _industry standard_ multi-distribution method for cross-platform cloud instance initialization. It is supported across all major public cloud providers, provisioning systems for private cloud infrastructure, and bare-metal installations.
> - [cloud-init documentation](https://docs.cloud-init.io/en/latest/)

cloud-init is a service that runs on most Linux distros. It is generally installed and the service is running on default cloud images.

Most cloud service providers allow you to pass data in the form of Bash scripts or YAML files to make initial configuration of an image.
### Writing out files using cloud-init

The docs contain a section on [Writing out arbitrary files](https://docs.cloud-init.io/en/latest/reference/examples.html#writing-out-arbitrary-files). Take a look at this section for the lab.
### Starter file for cloud-init lab component

Copy the file below into your Linux dev environment and make the following additions to the file.
- Add the public ssh key content that created to connect to your servers.
- to the `write_files` module add the following:
	- path `/var/www/html/index.html`
	- owner web:web
	- permissions "0644"
	- content The HTML document below (Look at the multi-line examples in the link to the docs provided above)


```yaml
#cloud-config

users:
  - name: web
    shell: /bin/bash
    ssh_authorized_keys:
      - "ssh-ed25519... your ssh key"

packages:
  - nginx

write_files:

runcmd:
# Ensure the web user owns the web content.
  - mkdir -p /var/www/html
  - chown -R web:web /var/www/html
  - chmod 0755 /var/www
  - chmod 0755 /var/www/html
  
  # Enable nginx at boot and restart it.
  - systemctl enable nginx
  - systemctl restart nginx
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hello from nginx</title>
</head>
<body>
  <h1>Hello from nginx!</h1>
  <p>This page is being served by nginx on Debian 13.</p>
</body>
</html>
```
### Trouble shooting cloud-init errors

Most of the time cloud init errors are YAML formatting errors, or other problems with your yaml file. You can generally diagnose these by connecting to your server via SSH and running the command:
```bash
cloud-init status --long
```

### Test your server with `curl`

To test your server use the curl command below. Replace the example IP address with the IP address of your server.
```bash
curl http://52.89.72.172
```
## AWS EC2 features

**Amazon Machine Images (AMIs)**

Preconfigured templates for your instances that package the components you need for your server (including the operating system and additional software).

**Instance types**

Various configurations of CPU, memory, storage, networking capacity, and graphics hardware for your instances.

**Amazon EBS volumes**

Persistent storage volumes for your data using Amazon Elastic Block Store (Amazon EBS).

**Instance store volumes**

Storage volumes for temporary data that is deleted when you stop, hibernate, or terminate your instance.

**Key pairs**

Secure login information for your instances. AWS stores the public key and you store the private key in a secure place.

**Security groups**

A virtual firewall that allows you to specify the protocols, ports, and source IP ranges that can reach your instances, and the destination IP ranges to which your instances can connect.

### AWS Elastic IP address

> An _Elastic IP address_ is a static IPv4 address designed for dynamic cloud computing. An Elastic IP address is allocated to your AWS account, and is yours until you release it. By using an Elastic IP address, you can mask the failure of an instance or software by rapidly remapping the address to another instance in your account. Alternatively, you can specify the Elastic IP address in a DNS record for your domain, so that your domain points to your instance. For more information, see the documentation for your domain registrar.
> 
> An Elastic IP address is a public IPv4 address, which is reachable from the internet. If you need to connect to an instance that does not have a public IPv4 address, you can associate an Elastic IP address with your instance to enable communication with the internet.
> - [Elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)

## Reference:
- [AWS EC2 Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [cloud-init](https://cloud-init.io)