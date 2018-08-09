# scapy extensions

The extension functions snippets on various settings in scapy

## IPOption implementation

* Remarks

The realization of these IP options is based on RFC 791. 
But support for these IP options from ISP is by no means guaranteed. 
Especially, lssr and ssrr options are the most interesting ones but are generally forbidden by ISP's routers.
I don't write the implementation on security options since I think it is of no use (correct me if I am wrong).
For details on IP headers and settings, see my [blog](https://refraction-ray.github.io/IP%E5%8D%8F%E8%AE%AE%E7%AC%94%E8%AE%B0/) (in Chinese).

* Usage example: 
~~~PYTHON
IP(dst='some.ip1', options=IPOption(lsrr('some.ip2','some.ip3')))/ICMP()
IP(dst=some.ip, ttl=64,IPOption(record_route(9))/ICMP() 
IP(dst=some.ip, src=fake.ip, IPOption(timestamp(3,2,'stamp.ip.1','stamp.ip.2'))/ICMP()
~~~