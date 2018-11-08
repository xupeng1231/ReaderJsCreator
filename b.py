def main():
    infile_path = "b.txt"
    outfile_path = "bb.txt"
    with open(infile_path,"rt") as inf:
        s = inf.read()
    lines = s.split("\n")
    with open(outfile_path,"wt") as outf:
        class_name=None
        for line in lines:
            line = line.strip()
            if len(line)<=0:
                continue
            if class_name is None:
                class_name = line
                continue
            parts = line.split(" ")
            if parts[0][0]=="-":
                outf.write("****{}****\n".format(line))
                parts[0]=parts[0][1:]
                if parts[0][0]=="-":
                    outf.write("\n")
                    continue
            fun_name=parts[0]
            ret_type=None
            if len(parts)>1:
                ret_type=parts[1]
            args=None
            if len(parts)>2:
                args=parts[2:]

            if ret_type is None or ret_type=="-":
                ret_str=""
            else:
                ret_str="<new {}>=".format(ret_type if "string"!=ret_type else "JString")

            if args is None:
                arg_str=""
            else:
                arg_str=",".join(["<{}>".format(c) for c in args])

            invocation_str = "{}<{}>.{}({});\n".format(ret_str, class_name, fun_name, arg_str)
            outf.write(invocation_str + "\n")



if __name__=="__main__":
    main()