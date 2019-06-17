"""
python3 is required, shift between bbl inserted tex and external bibliography tex
"""
import sys

def main(path):
	ref = ""
	with open(path+".bbl","r") as bblfile:
		ref = bblfile.read()
	text = []
	subflag = False
	blioflag = False
	bblstart = "\\begin{thebibliography}" 
	bblend = "\\end{thebibliography}" 
	with open(path+".tex","r") as texfile:
		for line in texfile:
			if line.startswith("\\bibliographystyle") and not blioflag:
				line = "%"+line
			elif line.startswith("\\bibliography") and not blioflag:
				subflag = True
				line = "%"+line
				line += ref
			elif line.startswith("%\\bibliography") and not blioflag:
				subflag = True
				line = line[1:]
			elif line.startswith("%\\bibliographystyle") and not blioflag:
				subflag = True
				line = line[1:]
			elif line.startswith(bblstart) and not blioflag:
				subflag = True
				blioflag = True
				line = ""
			elif blioflag and not line.startswith(bblend):
				line = ""
			elif blioflag and line.startswith(bblend):
				blioflag = False
				line = ""
			text.append(line)
	text = "".join(text)
	if subflag is True:
		with open(path+".tex","w") as texfile:
			texfile.write(text)
	else:
		print("nothing changed")
		

if __name__ == "__main__":
	main(sys.argv[1])