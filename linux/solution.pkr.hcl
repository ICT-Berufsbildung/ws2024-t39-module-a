packer {
  required_plugins {
    vsphere = {
      version = "~> 1"
      source  = "github.com/hashicorp/vsphere"
    }
  }
}

source "vsphere-iso" "base" {

  CPUs         = 2
  RAM          = 1024
  boot_command = [
    "<esc><wait>",
    "auto url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg interface=ens192<wait>", "<enter><wait>"
  ]
  disk_controller_type = ["pvscsi"]
  guest_os_type        = "debian11Guest"
  host                 = "esxi.lab.chrusuchopf.ch"
  datastore            = "local"
  insecure_connection  = true
  cdrom_type           = "sata"
  iso_paths            = [
    "[lab-storage] ISO/debian-12.5.0-amd64-BD-1.iso", "[lab-storage] ISO/debian-12.5.0-amd64-BD-2.iso",
    "[lab-storage] ISO/debian-12.5.0-amd64-BD-3.iso", "[lab-storage] ISO/debian-12.5.0-amd64-BD-4.iso",
    "[lab-storage] ISO/debian-12.5.0-amd64-BD-5.iso"
  ]
  password             = "Skill$39!"
  ssh_password         = "Skill39"
  ssh_username         = "root"
  storage {
    disk_size             = 32768
    disk_thin_provisioned = true
  }
  username       = "root"
  vcenter_server = "10.20.41.10"
  http_directory = "http"
  http_port_min  = 5100
  http_port_max  = 5150

}
# ha-prx01
build {
  name = "ha-prx01-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "ha-prx01-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "DMZ"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname ha-prx01"]
  }
  provisioner "file" {
    source = "http/ha-prx/interfaces01"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "solution/ha-prx/"
    destination = "/opt"
  }
  provisioner "shell" {
    inline = ["ansible-playbook /opt/ansible/solve.yml -i 'localhost,'"]
  }

}
# ha-prx02
build {
  name = "ha-prx02-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "ha-prx02-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "DMZ"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname ha-prx02"]
  }
  provisioner "file" {
    source = "http/ha-prx/interfaces02"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "solution/ha-prx/"
    destination = "/opt"
  }
  provisioner "shell" {
    inline = ["ansible-playbook /opt/ansible/solve.yml -i 'localhost,'"]
  }
}
# web01
build {
  name = "web01-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "web01-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "DMZ"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname web01"]
  }
  provisioner "file" {
    source = "http/web/interfaces01"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "http/web/wwwroot"
    destination = "/opt"
  }
  provisioner "file" {
    source = "solution/web/"
    destination = "/opt"
  }
  provisioner "shell" {
    inline = ["ansible-playbook /opt/ansible/solve.yml -i 'localhost,'"]
  }
}
# web02
build {
  name = "web02-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "web02-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "DMZ"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname web02"]
  }
  provisioner "file" {
    source = "http/web/interfaces02"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "http/web/wwwroot"
    destination = "/opt"
  }
  provisioner "file" {
    source = "solution/web/"
    destination = "/opt"
  }
  provisioner "shell" {
    inline = ["ansible-playbook /opt/ansible/solve.yml -i 'localhost,'"]
  }
}

# mailsrv
build {
  name = "mailsrv-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "mailsrv-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "DMZ"
    }
    storage {
      disk_size             = 16384
      disk_thin_provisioned = true
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname mailsrv"]
  }
  provisioner "file" {
    source = "http/mailsrv/interfaces"
    destination = "/etc/network/interfaces"
  }
}
# int-srv01
build {
  name = "int-srv01-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "int-srv01-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "Internal"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname int-srv01"]
  }
  provisioner "file" {
    source = "http/int-srv01/interfaces"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "solution/int-srv01/"
    destination = "/opt"
  }
  provisioner "shell" {
    inline = ["ansible-playbook /opt/ansible/solve.yml -i 'localhost,'"]
  }
}
# jamie-ws01
build {
  name = "jamie-ws01-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "jamie-ws01-SOLVED"
    network_adapters {
      network_card = "vmxnet3"
      network = "Internal"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname jamie-ws01"]
  }
  provisioner "file" {
    source = "http/jamie-ws01/interfaces"
    destination = "/etc/network/interfaces"
  }
}
#fw01
build {
  name = "fw01-SOLVED"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "fw01-SOLVED"
    network_adapters{
      network_card = "vmxnet3"
      network = "Internet"
    }
     network_adapters{
      network_card = "vmxnet3"
      network = "Internal"
    }
    network_adapters{
      network_card = "vmxnet3"
      network = "DMZ"
    }
  }
  provisioner "shell" {
    inline = ["hostnamectl set-hostname fw01"]
  }
  provisioner "file" {
    source = "http/firewall/interfaces"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "solution/firewall/"
    destination = "/opt"
  }
  provisioner "shell" {
    inline = ["ansible-playbook /opt/ansible/solve.yml -i 'localhost,'"]
  }
}