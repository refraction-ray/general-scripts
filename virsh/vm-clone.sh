#! /bin/bash

base="base1"
vmname=$1

# extra things to note when preparing base1: netplan config should avoid match on mac address which would disable nic in cloned machines with different macs

opts="abrt-data,bash-history,blkid-tab,ca-certificates,crash-data,cron-spool,customize,dhcp-client-state,dhcp-server-state,dovecot-data,firewall-rules,flag-reconfiguration,fs-uuids,kerberos-data,logfiles,lvm-uuids,machine-id,mail-spool,net-hostname,net-hwaddr,pacct-log,package-manager-cache,pam-data,puppet-data-log,rh-subscription-manager,rhn-systemid,rpm-db,samba-db-log,script,smolt-uuid,sssd-db-log,tmp-files,udev-persistent-net,user-account,utmp,yum-uuid"

virt-clone -o ${base} -n ${vmname} --auto-clone
virt-sysprep -d ${vmname} --hostname ${vmname} --keep-user-accounts ubuntu --enable ${opts}
