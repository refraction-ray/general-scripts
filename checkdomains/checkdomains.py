'''
python3
main script to check the domain status in blacklist
'''
from re import sub,search
from subprocess import check_output
with open("GFWlist.txt") as ls:
	total = 0
	rst = 0
	poison = 0
	for line in ls.readlines():
		domain = sub(r".*--.*|^@@.*|.*##.*|^\[.*|!.*|http://|https://|[\s]*|^\^https.*","",line)
		domain = sub(r"^\.(.*)$|^[|]{1,2}(.*)$","\\1",domain)
		if bool(search(r"^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*\.[a-z]+$",domain)):
			stdout = check_output(["./same.sh",domain]).decode('utf-8').split("\n")
			total = total+1
			if stdout[0].startswith("in"):
				rst = rst+1
			if stdout[1].startswith("in"):
				poison = poison+1
			if stdout[2].startswith('warning'):
				print(domain)
			# if total%100 == 0:
				# print('%s domains have been checked and %s have rst issue %s have poison issue'%(total,rst,poison))
	print('%s domains have been checked and %s have rst issue %s have poison issue'%(total,rst,poison))