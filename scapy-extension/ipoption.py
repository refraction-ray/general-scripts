'''
python3: scapy, ipaddress is required
functions return IP options in scapy construction
'''

from scapy.all import sr1, IP, IPOption,ICMP
import ipaddress as ipa

def record_route(hop=1):
	if hop >= 10:
		raise Exception('exceed the max length of ip header')
	length = chr(hop*4+3)
	option_head = b'\x07'+length.encode()+b'\x04'
	route_data = "".join(['\x00']*4*hop)
	option = option_head+('%s'%route_data).encode()
	return option

def lsrr(*source_route_table):
	hop = len(source_route_table)
	if hop >= 10:
		raise Exception('exceed the max length of ip header')
	length = chr(hop*4+3)
	option_head = b'\x83'+length.encode()+b'\x04'
	option = option_head
	for ip in source_route_table:
		ip = ipa.v4_int_to_packed(int(ipa.IPv4Address(ip)))
		option = option + ip
	return option

def ssrr(*source_route_table):
	hop = len(source_route_table)
	if hop >= 10:
		raise Exception('exceed the max length of ip header')
	length = chr(hop*4+3)
	option_head = b'\x89'+length.encode()+b'\x04'
	option = option_head
	for ip in source_route_table:
		ip = ipa.v4_int_to_packed(int(ipa.IPv4Address(ip)))
		option = option + ip
	return option

def timestamp(flag=0,hop=1,*specified_route):
	if flag == 0:
		if hop >= 10:
			raise Exception('exceed the max length of ip header')
		length = chr (hop*4+4)
		option_head = b'\x44'+length.encode()+b'\x05\x00'
		route_data = "".join(['\x00']*4*hop)
		option = option_head+('%s'%route_data).encode()
		return option
	if flag == 1:
		if hop >= 5:
			raise Exception('exceed the max length of ip header')
		length = chr (hop*8+4)
		option_head = b'\x44'+length.encode()+b'\x05\x01'
		route_data = "".join(['\x00']*8*hop)
		option = option_head+('%s'%route_data).encode()
		return option
	if flag==3:
		hop_check = len(specified_route)
		if hop_check != hop:
			raise Exception('the number of routes is not consistent with hops')
		if hop >= 5:
			raise Exception('exceed the max length of ip header')
		length = chr (hop*8+4)
		option_head = b'\x44'+length.encode()+b'\x05\x03'
		option = option_head
		for ip in specified_route:
			ip = ipa.v4_int_to_packed(int(ipa.IPv4Address(ip)))
			option = option + ip + b'\x00\x00\x00\x00'		
		return option
	raise Exception('no such flag, flag must be set as 0,1,3 in timastamp option')

def streamid(byte_id):
	return b'\x88\x04'+byte_id
