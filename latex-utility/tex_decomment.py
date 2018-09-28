'''
script to strip all comments in .tex files before distribution, only test on macOS.
it is worth noting that latexpand command utility can do the task perfectly.

usage: python3 tex_decomment.py input.tex [-e encoding] -o output.tex

inspired by https://gist.github.com/amerberg/a273ca1e579ab573b499,
make some modifications to improve the logic.
'''

from ply import lex
import argparse

def strip_comments(source):
    tokens = (
                'PERCENT', 'BEGINCOMMENT', 'ENDCOMMENT', 'BACKSLASH',
                'CHAR', 'BEGINVERBATIM', 'ENDVERBATIM', 'NEWLINE', 'ESCPCT', 'ENDDOCUMENT'
             )
    states = (
                ('linecomment', 'exclusive'), # start with %, ignore all char between % and \n
                ('commentenv', 'exclusive'), # start with \begin{comment}, a comment line even without %
                ('verbatim', 'exclusive'),  # start with \begin{verbatim}, not a comment line even with %
                ('documentend', 'exclusive') # ignore all stuff after \end{document}
            )

    # in general we use lexer.lineno to maintain the column, which is irrelvant to number of line at all

    #Deal with escaped backslashes, so we don't think they're escaping %.
    def t_BACKSLASH(t):
        r"\\\\"
        t.lexer.lineno += 1
        return t

    #Escaped percent signs
    def t_ESCPCT(t):
        r"\\%"
        t.lexer.lineno += 1
        return t

    #One-line comments
    def t_PERCENT(t):
        r"%"
        t.lexer.begin("linecomment")
        if t.lexer.lineno > 0: # if the comment is not a whole line, the ending \n should be kept
            t.value = '\n'
            return t

    # End document env enter
    def t_ENDDOCUMENT(t):
        r"\\end\s*{\s*document\s*}"
        t.lexer.begin("documentend")
        return t

    #Comment environment, as defined by verbatim package       
    def t_BEGINCOMMENT(t):
        r"\\begin\s*{\s*comment\s*}"
        t.lexer.begin("commentenv")
        pass

    #Verbatim environment (different treatment of comments within)   
    def t_BEGINVERBATIM(t):
        r"\\begin\s*{\s*verbatim\s*}"
        t.lexer.begin("verbatim")
        return t

    #Any other character in initial state we leave alone    
    def t_CHAR(t):
        r"."
        t.lexer.lineno += 1
        return t

    def t_NEWLINE(t):
        r"\n"
        t.lexer.lineno = 0
        return t

    #End comment environment    
    def t_commentenv_ENDCOMMENT(t):
        r"\\end\s*{\s*comment\s*}"
        #Anything after \end{comment} on a line is ignored!
        t.lexer.begin('linecomment')
        pass

    #Ignore comments of comment environment    
    def t_commentenv_CHAR(t):
        r"."
        pass

    def t_commentenv_NEWLINE(t):
        r"\n"
        pass

    #Ignore all things after \end{document}    
    def t_documentend_CHAR(t):
        r"."
        pass

    def t_documentend_NEWLINE(t):
        r"\n"
        pass

    #End of verbatim environment    
    def t_verbatim_ENDVERBATIM(t):
        r"\\end\s*{\s*verbatim\s*}"
        t.lexer.begin('INITIAL')
        return t

    #Leave contents of verbatim environment alone
    def t_verbatim_CHAR(t):
        r"."
        return t

    def t_verbatim_NEWLINE(t):
        r"\n"
        return t

    #End a % comment when we get to a new line
    def t_linecomment_ENDCOMMENT(t):
        r"\n"
        t.lexer.begin("INITIAL")
        pass
        #Newline at the end of a line comment is stripped.

    #Ignore anything after a % on a line        
    def t_linecomment_CHAR(t):
        r"."
        pass

    def t_ANY_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
       
    lexer = lex.lex()
    lexer.input(source)
    
    # the comment part has already be dropped when parsing by pass claim in the above functions
    # so the remaining part is what we want

    return "".join([tok.value for tok in lexer])

def main():
    parser = argparse.ArgumentParser(description = 'strip all comments from tex file appropriately')
    parser.add_argument('filename', help = 'the file to strip comments from')
    parser.add_argument('-o', dest = 'output', help = 'the file without comments to')
    parser.add_argument('-e', dest = 'encoding', default = 'utf-8', help = 'the encoding of the file')
    
    args = parser.parse_args()
    
    with open(args.filename, encoding=args.encoding) as f:
        source = f.read()
    with open(args.output, 'w', encoding=args.encoding) as f:
        f.write(strip_comments(source))

if __name__ == '__main__':
    main()