def main():
    infile_path = "b.txt"
    outfile_path = "bb.txt"
    with open(infile_path, "rt") as inf:
        s = inf.read()
    lines = s.split("\n")
    with open(outfile_path, "wt") as outf:
        outf.write('\n#rawnotes "{}"\n'.format(s.replace("\n", "\\n")))
        class_name = None
        for line in lines:
            line = line.strip()
            if len(line)<=0:
                continue
            if line.startswith("#"):
                outf.write(line+"\n")
                continue
            if class_name is None:
                class_name = line
                continue
            parts = line.split(" ")
            if parts[0][0] == "-":
                outf.write("# ****{}****\n".format(line))
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
            if args is not None:
                for i in range(len(args)):
                    arg = args[i]
                    if arg.startswith("array") and arg.find("-") > 0:
                        # array-type-len-minlen-maxlen
                        arg_parts = arg.split("-")
                        arg_parts = [p.strip(" ") for p in arg_parts]
                        arg_new = "array"
                        if len(arg_parts) > 1 and len(arg_parts[1]) > 0:
                            arg_new += " type=" + arg_parts[1]
                        if len(arg_parts) > 2 and len(arg_parts[2]) > 0:
                            arg_new += " len=" + arg_parts[2]
                        if len(arg_parts) > 3 and len(arg_parts[3]) > 0:
                            arg_new += " minlen=" + arg_parts[3]
                        if len(arg_parts) > 4 and len(arg_parts[4]) > 0:
                            arg_new += " maxlen=" + arg_parts[4]
                        args[i] = arg_new
                    elif arg.startswith("int") and arg.find("-") > 0:
                        # int-min-max-best
                        arg_parts = arg.split("-")
                        arg_parts = [p.strip(" ") for p in arg_parts]
                        arg_new = "int"
                        if len(arg_parts) > 1 and len(arg_parts[1]) > 0:
                            arg_new += " min=" + arg_parts[1]
                        if len(arg_parts) > 2 and len(arg_parts[2]) > 0:
                            arg_new += " max=" + arg_parts[2]
                        if len(arg_parts) > 3 and len(arg_parts[3]) > 0:
                            arg_new += " best=" + arg_parts[3]
                        args[i]=arg_new
                    elif arg.find("-") >= 0:
                        args[i] = arg.replace("-", " ")


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