terraform {
  required_providers {
    proxmox = {
      source = "telmate/proxmox"
      version = "~> 2.9"
    }
  }
}

provider "proxmox" {
    pm_api_url = var.controller-api
    #pm_api_token_id = var.PM_API_TOKEN_ID
    #ppm_api_token_secret = var.PM_API_TOKEN_SECRET

    pm_user = var.PM_USER
    pm_password = var.PM_API_TOKEN_SECRET
    pm_parallel = 1
}

resource "proxmox_vm_qemu" "k8-controller" {
    name = "${cluster-hostname}-controller"
    target_node = var.controller-host

    clone = "rocky-linux-template-${ var.controller-host }"
    desc = "${jsonencode({ "groups": ["${cluster-hostname}-controller"] })}"
    
    pool = var.pool
    bootdisk = "scsi0"

    full_clone = true
    cores = 4
    memory = 4096
    agent = 1

    ciuser = var.CI_User
    cipassword = var.CI_Passwd

    # this is the ssh key that will be used to access the VM
    sshkeys = <<EOF
    ${var.VM_sshkeys}
    EOF

    provisioner "remote-exec" {
      connection {
        type     = "ssh"
        user     = "${self.ciuser}"
        private_key = "${file("~/.ssh/id_ed25519")}"
        host     = "${self.default_ipv4_address}"
      }
      inline = [
        "sudo hostnamectl set-hostname --static ${self.name}",
        "sudo hostnamectl set-hostname ${self.name}",
        "sudo dhclient -H ${self.name}"
      ]
    }
}

resource "proxmox_vm_qemu" "k8-node" {
    count = var.number-of-nodes
    name = "${cluster-hostname}-${count.index}"
    target_node = var.node-host
    desc = "${jsonencode({ "groups": ["${cluster-hostname}_node"] })}"

    clone = "rocky-linux-template-${ var.node-host }"
    
    pool = var.pool
    bootdisk = "scsi0"

    full_clone = true
    cores = 4
    memory = 4096
    agent = 1

    ciuser = var.CI_User
    cipassword = var.CI_Passwd

    # this is the ssh key that will be used to access the VM
    sshkeys = <<EOF
    ${var.VM_sshkeys}
    EOF

    provisioner "remote-exec" {
      connection {
        type     = "ssh"
        user     = "${self.ciuser}"
        private_key = "${file("~/.ssh/id_ed25519")}"
        host     = "${self.default_ipv4_address}"
      }
      inline = [
        "sudo hostnamectl set-hostname --static ${self.name}",
        "sudo hostnamectl set-hostname ${self.name}", 
        "sudo dhclient -H ${self.name}"
      ]
    }
}