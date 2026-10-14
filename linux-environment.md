# Setting up a Linux environment for 3640

We are going to be installing tools in a Linux environment and writing Bash scripts this term. To do this you need a local Linux development environment on your system.

You will be responsible for maintaining the Linux environment. I recommend making regular updates on your system as the term progresses.

Don't worry about the Linux distro you chose. Since, Debian is the only distro most of you have experience with, Debian is a good choice. If you want to experiment with a different distro that is great, however you may want to save that for outside of class.

You can create your Linux environment using one of the three methods listed below.

## Switch to Linux

Honestly, in a lot of ways this will be the easiest option. 

If you are running Linux on your laptop already and you wish to isolate the environment you are going to use in this class from you own system I recommend using [distrobox](https://distrobox.it)

[CIT distrobox resources](https://gitlab.com/cit-debian/cit-container-resources)
## Create a Linux VM with Virtualbox

Or similar Virtualization/emulation tool.

You don't need a GUI for this, so a headless VM is probably the best option.

## WSL

Important to know if you chose this option.

WSL will create its own file system. So you will have two file systems, your existing Windows system, and your WSL file system. Microsoft recommends working from the WSL file system when you are using WSL. You can still access Windows GUI tools like the file explore. `explorer.exe .` will open the explorer in your working directory.

There are two reasons you don't want to work in your Windows file system:
1. Working in your Windows environment can result in permission errors.
2. According to the WSL Docs your WSL system will perform better. I haven't tested this, but I would assume that the difference is relatively small. The first reason however is really important.

You can tell you are in your Windows environment if your prompt path includes `/mnt/c`. You don't want to see this. You can configure WSL to start in the home of your WSL environment, or simply run the `cd` command by itself. Just type `cd` and press return.

## Reference

1. [WSL Docs](https://learn.microsoft.com/en-us/windows/wsl/)
2. [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
3. [WSL File storage and performance across file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems#file-storage-and-performance-across-file-systems)

## Optional: Enable Systemd in WSL 2

For testing purposes, it is useful to be able to run `systemd` in WSL 2.  This can be done by following the steps below. Edit the file `/etc/wsl.conf` form WSL2 terminal and add the following lines:

```
[boot]
systemd=true
```
## Reference

1. [Systemd support lands in WSL](https://ubuntu.com/blog/ubuntu-wsl-enable-systemd)
