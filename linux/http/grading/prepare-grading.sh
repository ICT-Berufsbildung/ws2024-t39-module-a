#!/bin/bash
mkdir --mode=700 /root/.ssh
chown root:root /root/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF7u8pFB94emoZVKK45/HI6/4tyABMIIFxelb+ii7DmP root@WSC2024_MOD_A" > /root/.ssh/authorized_keys
chown root:root /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

# Install required packages unattended
export DEBIAN_FRONTEND=noninteractive
apt-get -qqy update
apt-get install -qqy \
  -o DPkg::options::="--force-confdef" \
  -o DPkg::options::="--force-confold" \
  python3-pip

pip3 install nornir nornir_utils nornir_paramiko