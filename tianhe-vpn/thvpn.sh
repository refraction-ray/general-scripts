#! /bin/bash

vpndev="VPN (Cisco IPSec) 2"
normif=en0

scutil --nc start "$vpndev"
sleep 2;
status=`scutil --nc show "$vpndev"|head -n 1|awk '{print $2}'`
echo $status
if [ "$status" == "(Connected)" ]; then
	gtip=`netstat -nr|grep de|grep $normif|head -n 1|awk '{print $2}'`
	sudo route delete default
	sudo route delete default -ifscope $normif
	sudo route add default $gtip
	thip=`netstat -nr|grep 172|grep UH|awk '{print $1}'`
	sudo route -n add -net 172.0/8 $thip || sudo route change -net 172.0/8 $thip
	netstat -nr|grep de|awk '{print $2}'
	echo "VPN setup success"
else
	scutil --nc stop "$vpndev"
	echo "failed to start VPN, please try again"
fi