# K8-Proxmox-Setup

 :warning:

 ***This is a work in progress, there is a good chance this is broken and will not be fixed. Please use for example purposes only***

 :warning:

Created by @xn4p4lm

***Note***: I'm making this public, because I think it's cool tool!

---

## Requirements

First to use this project you will need the following software: 

Proxmox Environment: 
- Proxmox version 7.0 (may work on later versions)
- [x86/64 Generic Cloud / OpenStack image of Rocky Linux 7](https://rockylinux.org/alternative-images) setup as a template in proxmox

Software: 
- Terraform v1.2.2
- Ansible 2.11.6 
- Python 3.9.13

pip Modules: 
- simple-term-menu

You can validate your by running `./checkEnvironment.sh`

> Other version of the above software may work, but cannot guarantee this will work as intended 

---

## Using this automation

First you will need to copy `variables.tf.example` to `variables.tf` and fill all variables by replacing `{}` with the appropriate variable in this format `" "`

For example: `"{desired hostname}"` would become `"kubernetes"`

Again, there is no gaurentee that it will work without modification or tweakin

---

## To Do

- Currently this does not setup a networking layer, as such you will need to configure this manually using your desired flavor