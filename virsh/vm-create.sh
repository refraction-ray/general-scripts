#!/bin/bash
no=$1
prefix=${2:-test}
pubkey=""
osimg="ubuntu-18.04-server-cloudimg-amd64.img"

cat << END > meta-data
instance-id: ${prefix}${no}
local-hostname: ${prefix}${no}
END

cat << END > user-data
#cloud-config
users:
- name: ubuntu
  groups: sudo
  shell: /bin/bash
  ssh_authorized_keys:
  - ${pubkey}
  sudo:  ALL=(ALL) NOPASSWD:ALL
END

cp ${osimg} ${prefix}${no}.qcow2
genisoimage -o config${prefix}${no}.iso -V cidata -r -J meta-data user-data
virt-install -n ${prefix}${no} -r 2048 --vcpus=2 --disk ${prefix}${no}.qcow2 --import --disk path=config${prefix}${no}.iso,device=cdrom  --network network=default,mac=52:54:00:77:39:$(printf "%02x" $no) --noautoconsole
