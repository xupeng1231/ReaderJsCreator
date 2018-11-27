def main():
    in_file_path = "a.txt"
    out_file_path = "aa.txt"
    with open(in_file_path,"rt") as inf:
        s=inf.read()
    lines=s.split('\n')
    class_name=None
    with open(out_file_path,"wt") as outf:
        outf.write('\n#rawnotes "{}"\n'.format(s.replace("\n","\\n")))
        for line in lines:
            line = line.strip()
            if len(line)<=0:
                continue
            if line.startswith("#"):
                outf.write(line+"\n")
                continue
            if class_name is None:
                class_name=line
                continue
            parts = line.split(" ")
            if len(parts) < 2:
                outf.write("# ****{}****\n\n".format(line))
                continue
            if parts[0][0]=='-':
                parts[0] = parts[0][1:]
                outf.write("# ****{}****\n".format(line))
            attr_name = parts[0]
            attr_type = parts[1]
            if attr_type.startswith("array") and attr_type.find("-")>0:
                # array-type-len-minlen-maxlen
                type_parts=attr_type.split("-")
                type_parts = [p.strip(" ") for p in type_parts]
                attr_type_new = "array"
                if len(type_parts)>1 and len(type_parts[1])>0:
                    attr_type_new+=" type="+type_parts[1]
                if len(type_parts)>2 and len(type_parts[2])>0:
                    attr_type_new+=" len="+type_parts[2]
                if len(type_parts)>3 and len(type_parts[3])>0:
                    attr_type_new+=" minlen="+type_parts[3]
                if len(type_parts)>4 and len(type_parts[4])>0:
                    attr_type_new+=" maxlen="+type_parts[4]
                attr_type=attr_type_new
            elif attr_type.startswith("int") and attr_type.find("-")>0:
                # int-min-max-best
                type_parts=attr_type.split("-")
                type_parts = [p.strip(" ") for p in type_parts]
                attr_type_new = "int"
                if len(type_parts)>1 and len(type_parts[1])>0:
                    attr_type_new+=" min="+type_parts[1]
                if len(type_parts)>2 and len(type_parts[2])>0:
                    attr_type_new+=" max="+type_parts[2]
                if len(type_parts)>3 and len(type_parts[3])>0:
                    attr_type_new+=" best="+type_parts[3]
                attr_type=attr_type_new
            if len(parts) > 2:
                generate_constant = True
            else:
                generate_constant = False
            if attr_name and attr_type:
                if not generate_constant:
                    out_str = "<{}>.{}=<{}>;\n".format(class_name,attr_name,attr_type)
                    out_str += "<new {}>=<{}>.{};\n".format(attr_type if attr_type != "string" else "JString",class_name,attr_name)
                else:
                    out_str = "<{}>.{}=<{}>;\n".format(class_name, attr_name, "{}_{}_{}".format(attr_type,class_name,attr_name))
                    out_str += "<new {}>=<{}>.{};\n".format(attr_type if attr_type != "string" else "JString", class_name, attr_name)
                    for part in parts[2:]:
                        out_str += "<{}>={}\n".format("{}_{}_{}".format(attr_type,class_name,attr_name), part if attr_type!="string"else "\"{}\"".format(part))
                outf.write(out_str+"\n")



if __name__ == "__main__":
    main()