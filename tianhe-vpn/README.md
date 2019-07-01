## Tianhe2 VPN setup

By default, the IPSec VPN provided by Tianhe2 HPC is terrible on mac, since once your connect to the VPN, all your normal networks turn off, and you are disconnected from the Internet world. 

`thvpn.sh` provide an automatic way to setup and connect to the VPN while at the same time, we can still be connected to the whole Internet. This is done by maintaining some route table items.