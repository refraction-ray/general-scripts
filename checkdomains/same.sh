#! /bin/bash
a=`dig +tcp @8.8.8.8 $1|grep reset`
if [ -n "$a"  ]
then
	rst=1
	echo "in the rst list"
else
	rst=0
	echo "not in the rst list"
fi
b=`dig @8.8.8.8 $1|grep "Query time"|sed -e 's/^.*:[[:space:]]\([0-9]*\)[[:space:]].*$/\1/'`

if [ $b -lt 10 ] 
then
	poison=1
	echo "in the poison list"
else
	poison=0
	echo "might not in the poison list"
fi
if [ $rst = $poison ]
then 
	echo "results are consistent"
else
	echo "warning: inconsitent results in this domain"
fi