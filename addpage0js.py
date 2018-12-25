from PyPDF2.generic import DictionaryObject, NameObject, ArrayObject, createStringObject, IndirectObject, NumberObject
from PyPDF2 import PdfFileWriter,PdfFileReader
import uuid
from StringIO import StringIO
import sys
import re
import zlib

def obj_insertline(obj, line):
    left_arrow_offset = obj.index("<<")
    return obj[:left_arrow_offset+2]+'\n'+line+obj[left_arrow_offset+2:]

def addpage0js(pdf_string, js_string, outpath):
    writer = PdfFileWriter()
    reader = PdfFileReader(StringIO(pdf_string))
    pagenum =reader.getNumPages()
    for i in range(pagenum):
        writer.addPage(reader.getPage(i))
    del reader
    tmp_stringio=StringIO()
    writer.write(tmp_stringio)
    pdf_string = tmp_stringio.getvalue()
    del writer,tmp_stringio

    xref = re.findall("startxref\n(\d+)\n%%EOF\n", pdf_string)
    trailer = re.findall(r'trailer\n<<\n/Size\s(\d+)\n/Root\s(\d+)\s0\sR\n/Info\s(\d+)', pdf_string)
    # with open('tmp.pdf', 'wb') as tmp_fd:
    #     tmp_fd.write(pdf_string)
    assert len(xref) == 1
    xref_offset = int(xref[-1])
    obj_num = int(trailer[-1][0])
    root_obj_index = int(trailer[-1][1])
    info_obj_index = int(trailer[-1][2])
    print xref_offset, obj_num, root_obj_index, info_obj_index
    xref_lines = pdf_string[xref_offset:].splitlines()
    splits = []
    for i in range(2, obj_num+2):
        splits.append(int(xref_lines[i].split(" ")[0]))
    splits.append(xref_offset)

    objs = []
    for i in range(len(splits)-1):
        objs.append(pdf_string[splits[i]:splits[i+1]])

    # get page0 index
    pages_obj_index = int(re.findall('/Pages\s(\d+)\s0\sR', objs[root_obj_index])[-1])
    page0_index =int(re.findall('/Kids \[\s?(\d+)\s+0\s+R', objs[pages_obj_index])[-1])
    print pages_obj_index, page0_index

    js_compressed_source = zlib.compress(js_string)

    # generate new page0 object and javascript object
    js_obj_index = obj_num
    js_source_obj_index = obj_num+1
    page0_update_obj = obj_insertline(objs[page0_index], '/AA<</O {} 0 R>>'.format(js_obj_index))
    js_obj = "{} 0 obj\n<<\n/S /JavaScript\n/JS {}\n>>\nendobj\n".format(js_obj_index, "{} 0 R".format(js_source_obj_index))
    js_source_obj = '{} 0 obj\n<</Filter [/FlateDecode]/Length {}>>\nstream\n{}\nendstream\nendobj\n'.format(
        js_source_obj_index, len(js_compressed_source),js_compressed_source)

    # write new pdf file
    outfileio=StringIO()
    outfileio.write(pdf_string)

    page0_update_obj_offset = outfileio.tell()
    outfileio.write(page0_update_obj)
    js_obj_offset = outfileio.tell()
    outfileio.write(js_obj)
    js_source_obj_offset = outfileio.tell()
    outfileio.write(js_source_obj)


    new_xref_offset = outfileio.tell()
    outfileio.write("xref\n0 1\n0000000000 65535 f\n")
    outfileio.write('{} 1\n{:010d} 00000 n\n'.format(page0_index, page0_update_obj_offset))
    outfileio.write('{} 1\n{:010d} 00000 n\n'.format(js_obj_index, js_obj_offset))
    outfileio.write('{} 1\n{:010d} 00000 n\n'.format(js_source_obj_index, js_source_obj_offset))

    new_obj_num = obj_num+2
    outfileio.write('trailer\n')
    trailer = DictionaryObject()
    trailer.update({
        NameObject("/Size"): NumberObject(new_obj_num),
        NameObject("/Root"): IndirectObject(root_obj_index, 0, None),
        NameObject("/Info"): IndirectObject(info_obj_index, 0, None),
        NameObject("/Prev"): NumberObject(xref_offset)
    })
    trailer.writeToStream(outfileio, None)

    outfileio.write("\nstartxref\n%s\n%%%%EOF\n" % new_xref_offset)

    with open(outpath, 'wb') as outfile_fd:
        outfile_fd.write(outfileio.getvalue())



if __name__ == "__main__":
    if len(sys.argv)!=3:
        print "Usage: python addpage0js.py pdffile jsfile"
    pdffile = sys.argv[1]
    jsfile = sys.argv[2]
    with open(pdffile,'rb') as pdf_fd:
        pdf_string = pdf_fd.read()
    with open(jsfile,'rb') as js_fd:
        js_string = js_fd.read()
    addpage0js(pdf_string, js_string, "temp.pdf")

