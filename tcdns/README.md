# tcDNS

This is a shell script to detect and evaluate the 'pureness' of specified DNS server.

It supports both ipv4 and ipv6 evaluation, i.e. the specified DNS server can be using ipv6 or ipv4 address,  meanwhile the query parts are also evaluated both in A and AAAA response.

## Usage
Learn how to use by `./tcdns.sh -h`.

 If you are permission denied, try `chmod +x tcdns.sh`  first.

## Note
This script depends on the availability of API from ipinfo.io, the internet connection may not be good. Anyone can update it with reliable ip whois APIs easily.
