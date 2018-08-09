#! /bin/bash
while getopts "46thvs:" arg 
do
		case $arg in
			s)
				sflag=x
				dnsip=$OPTARG
				;;
			4)
				v4flag=x
				;;
			6)
				v6flag=x
				;;
			t)
				tflag=x
				;;
			h)
				hflag=x
				;;
			v)
				echo "tcdns v0.0.1" 
				echo "author: refraction-ray"
				exit 0
				;;
			?)  
				echo "unkonw argument"
				exit 1
				;;
		esac
done

if [ x$hflag = xx ]
then
	echo "tcdns: DNS test tool. Test/Check your DNS server now."
	echo "Usage: ./tcdns.sh -s [DNS server ip] <options>"
	echo "Options:"
	echo "  -4:  check  A record queries (default)"
	echo "  -6:  check  AAAA record queries (can set with -4 at the same time)"
	echo "  -t:  use tcp connection for the DNS queries"
	echo "  -v:  show the version info"
	echo "  -h:  show the help info"
	exit 0
fi

if [ x$sflag = x ]
then 
	echo "No DNS server specified, use the option -s [DNS ip]"
	exit 1
fi

available=`dig +short @$dnsip baidu.com|grep '^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$'`
if [ -z "$available" ]
then
	echo "The server is not an available DNS server"
	exit 1
fi

address=(youtube.com www.google.com twitter.com facebook.com instagram.com tumblr.com pornhub.com medium.com nytimes.com www.dropbox-dns.com)
inc=(Google Google Twitter Facebook Amazon Yahoo Viking Cloudflare Fastly Dropbox)

dnstest(){
i=0
score=0
for add in ${address[@]}
do
	ip=`dig +short $3 @$dnsip ${add} $1|head -1|grep $2`
	if [ -n "$ip" ]
	then
		url="ipinfo.io/"$ip"/org"
		org=`curl -s $url|grep ${inc[$i]}`
		if [ -n "$org" ]
		then
			score=`expr $score + 1`
		fi	
	fi
i=`expr $i + 1`
done
echo "The settings and score of the DNS server (max: 10 for A and 6 for AAAA):"
echo $1$3
echo $score	
}

echo "Please wait for the results, it may take some time"

if [ x$tflag = x ]
then
	if ( [ x$v4flag = x ] && [ x$v6flag = x ] ) || [ x$v4flag = xx ]
	then
		dnstest A '^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$' 
	fi
	if [ x$v6flag = xx ]
	then
		dnstest AAAA '^[0-9a-fA-F:]\{3,40\}$'
	fi
fi

if [ x$tflag = xx ]
then
	if ( [ x$v4flag = x ] && [ x$v6flag = x ] ) || [ x$v4flag = xx ]
	then
		dnstest A '^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$' +tcp
	fi
	if [ x$v6flag = xx ]
	then
		dnstest AAAA '^[0-9a-fA-F:]\{3,40\}$' +tcp
	fi
fi