#!/bin/bash
vmname=${1}
disks=($(virsh dumpxml ${vmname}|grep -A 3 disk|grep source|awk -F "'" '{print $2}'))

virsh shutdown ${vmname}
virsh undefine ${vmname}
for d in ${disks[@]}; do
    rm -f ${d}
done
