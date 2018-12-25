from grammar import *
import random

js_whole_need_pre = '''
console.show();
function GetVariable(fuzzervars, var_type) { if(fuzzervars[var_type]) { return fuzzervars[var_type]; } else { return null; }}
function SetVariable(fuzzervars, var_name, var_type) { fuzzervars[var_type] = var_name; }
fuzzervars={};
iii=7;
'''
js_after='''
console.println("AAAAA");
'''
if __name__=="__main__":
    random.seed(3)
    jsgrammar = Grammar()
    err = jsgrammar.parse_from_file("jsgrammar\\rootline.txt")
    s = jsgrammar._generate_code(5000, prerun=True)
    s = js_whole_need_pre+s+js_after
    with open("outjs.txt","wt") as of:
        of.write(s)
    print err