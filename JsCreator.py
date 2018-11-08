from grammar import *

if __name__=="__main__":
    jsgrammar = Grammar()
    err = jsgrammar.parse_from_file("js_line.txt")
    print err