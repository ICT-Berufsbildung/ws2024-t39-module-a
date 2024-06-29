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
  guest_os_type        = "debian12_64Guest"
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
  tools_sync_time = true
  export {
    force = true
    output_directory = "./output-artifacts"
  }
}
# ha-prx01
build {
  name = "ha-prx01"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "ha-prx01"
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
    source = "http/resolv.dmz.conf"
    destination = "/etc/resolv.conf"
  }

}
# ha-prx02
build {
  name = "ha-prx02"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "ha-prx02"
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
    source = "http/resolv.dmz.conf"
    destination = "/etc/resolv.conf"
  }
}
# web01
build {
  name = "web01"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "web01"
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
    source = "http/resolv.dmz.conf"
    destination = "/etc/resolv.conf"
  }
}
# web02
build {
  name = "web02"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "web02"
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
    source = "http/resolv.dmz.conf"
    destination = "/etc/resolv.conf"
  }
}
# mailsrv
build {
  name = "mail"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "mail"
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
    inline = ["hostnamectl set-hostname mail"]
  }
  provisioner "file" {
    source = "http/mailsrv/interfaces"
    destination = "/etc/network/interfaces"
  }
  provisioner "file" {
    source = "http/resolv.dmz.conf"
    destination = "/etc/resolv.conf"
  }
}
# int-srv01
build {
  name = "int-srv01"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "int-srv01"
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
    source = "http/resolv.int.conf"
    destination = "/etc/resolv.conf"
  }
}
# jamie-ws01
build {
  name = "jamie-ws01"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "jamie-ws01"
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
  provisioner "file" {
    source = "http/resolv.int.conf"
    destination = "/etc/resolv.conf"
  }
}
#fw01
build {
  name = "fw01"
  sources = ["source.vsphere-iso.base"]
  source "source.vsphere-iso.base" {
    vm_name = "fw01"
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
    source = "http/resolv.dmz.conf"
    destination = "/etc/resolv.conf"
  }

  provisioner "shell" {
    script = "http/grading/prepare-grading.sh"
  }

  provisioner "file" {
    source = "http/fw/id_ed25519"
    destination = "/root/.ssh/id_ed25519"
  }

  provisioner "shell" {
    inline = [
      "chmod 600 /root/.ssh/id_ed25519"
    ]
  }

  provisioner "file" {
    source = "http/grading/wsc_grading.zip"
    destination = "/usr/local/share/wsc_grading.zip"
  }

  provisioner "file" {
    source = "http/grading/grading.sh"
    destination = "/usr/local/bin/grading"
  }
}
