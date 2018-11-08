def main():
    in_file_path = "a.txt"
    out_file_path = "aa.txt"
    with open(in_file_path,"rt") as inf:
        s=inf.read()
    lines=s.split('\n')
    class_name=None
    with open(out_file_path,"wt") as outf:
        for line in lines:
            line = line.strip()
            if len(line)<=0:
                continue
            if class_name is None:
                class_name=line
                continue
            parts = line.split(" ")
            if len(parts) < 2:
                outf.write("****{}****\n\n".format(line))
                continue
            if parts[0][0]=='-':
                parts[0] = parts[0][1:]
                outf.write("****{}****\n".format(line))
            attr_name = parts[0]
            attr_type = parts[1]
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
                        out_str += "<{}>={};\n".format("{}_{}_{}".format(attr_type,class_name,attr_name), part if attr_type!="string"else "\"{}\"".format(part))
                outf.write(out_str+"\n")



if __name__ == "__main__":
    main()