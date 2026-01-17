# Debian ZFS on root bootstrap

This project is a set of ansible playbooks to automate the installation of a
Debian system with an encrypted ZFS on root system.


## Assumptions on the setup

- ⚠️ The disk(s) can be erased. ⚠️
- You want encryption.
- The system supports UEFI.
- You want Debian Trixie (will not work _before_ Trixie. Might work on later versions).
- You have ansible >2.10 installed on your system.
- You have a wired connection on your machine.


## Installation

### Preparing the system

The first step is to setup a live environment in which we will be able to start
the installation.

You will need to disable SecureBoot for the installation.
We will re-enable it later.

You will need to start by getting a
[Debian live CD](https://cdimage.debian.org/cdimage/release/current-live/amd64/iso-hybrid/)
and boot your system with it.

You will then need to install an ssh server an set it up:

```bash
sudo passwd  # Note the password, you will need it later
sudo apt update
sudo apt install openssh-server
# Allow root to login with password
sed -i 's/^#\{0,1\}PermitRootLogin\ .*$/PermitRootLogin\ yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

And gather the connection information:

```
ip addr show scope global | grep inet
```

### Preparing the inventory

⚠️⚠️⚠️

This is the most critical part of the setup and later steps _**will wipe**_ disks. Be careful with what you set here. You have been warned.

⚠️⚠️⚠️


Copy the example inventory file [./inventory.example.yml](./inventory.example.yml)
 and fill in the fields according to the inline documentation.


### Starting the installation

⚠️⚠️⚠️ This will wipe the disks you have selected and you will **loose all data** on them. You have been warned.

In order to install the system, run:

```
ansible-playbook --diff playbooks/provision.yml --extra-vars="debian_zfs_root_hosts=${TARGET_SERVER_IP_ADDRESS_HERE}"
```

Once it is done, you can safely reboot your computer, and will be able to log
in remotely!

### Post cleanup

- You should re-enable UEFI secure boot
- Note that if you have decided to use a mirrored setup, the efi partitions are
not replicated and you should setup that up yourself.
