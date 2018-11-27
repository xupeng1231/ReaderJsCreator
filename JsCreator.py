from grammar import *
import random

if __name__=="__main__":
    random.seed(2)
    jsgrammar = Grammar()
    err = jsgrammar.parse_from_file("js_line.txt")
    s=jsgrammar._generate_code(100)
    with open("outjs.txt","wt") as of:
        of.write(s)
    print err