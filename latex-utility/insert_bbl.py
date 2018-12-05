"""
python3 is required
"""
import sys

def main(path):
	ref = ""
	with open(path+".bbl","r") as bblfile:
		ref = bblfile.read()
	text = []
	subflag = False
	with open(path+".tex","r") as texfile:
		for line in texfile:
			if line.startswith("\\bibliographystyle"):
				line = "%"+line
			elif line.startswith("\\bibliography"):
				subflag = True
				line = "%"+line
				line += ref
			text.append(line)
	text = "".join(text)
	if subflag is True:
		with open(path+".tex","w") as texfile:
			texfile.write(text)
	else:
		print("No substitution is needed")

if __name__ == "__main__":
	main(sys.argv[1])