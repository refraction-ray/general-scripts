## Relevant scripts for latex

### tex_decomment.py

A script to strip all comments from source .tex file with considerations on some subtle cases, implemented with ply module, which is the python version of lex.

Usage: `python3 tex_decomment.py input.tex [-e encoding] -o output.tex`

Test on python3.6 and macOS.

### insert_bbl.py

Replace the `\bibliography`include line with the real content from `.bbl` file such that one can write the papers with his or her own literature management but share the single tex file with others.

Usage: `python3 insert_bbl.py [the file name without extentions]`.

Note the `.bbl` file share the same name with `.tex` file automatically.