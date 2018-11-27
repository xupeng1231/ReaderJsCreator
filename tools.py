from PyPDF2 import PdfFileWriter,PdfFileReader
import os
import shutil


def test():
    output = PdfFileWriter()
    input1 = PdfFileReader(open("0.pdf", "rb"))

    # print how many pages input1 has:
    print "document1.pdf has %d pages." % input1.getNumPages()

    # add page 1 from input1 to output document, unchanged
    output.addPage(input1.getPage(0))

    output.addJS("console.show();")

    # finally, write "output" to document-output.pdf
    outputStream = file("PyPDF2-output.pdf", "wb")
    output.write(outputStream)

def search_pdf():
    crc32s=[]
    dirs=["c:","f:","g:","i:"]
    num=0
    for dir_path in dirs:
        try:
            files=os.listdir(dir_path)
        except:
            continue
        files=[os.path.join(dir_path, f) for f in files]
        for f in files:
            if os.path.isfile(f) and f.endswith(".pdf"):
                try:
                    shutil.copy(f,r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\samples")
                    num+=1
                except:
                    pass
            if os.path.isdir(f):
                dirs.append(f)
        if num > 200:
            break
def prehandle_pd():
    files = os.listdir(r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\samples")
    files=[os.path.join(r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\samples", c) for c in files if c.endswith(".pdf")]
    index = 0
    for f in files:
        try:
            pdf=PdfFileReader(f)
            pdf.getPage(0)
        except Exception as e:
            print e
            shutil.move(f, os.path.join(r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\samples","bad_"+str(index)+".pdf"))
            index+=1
            continue
        shutil.move(f, os.path.join(r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\samples", "good_" + str(index)+".pdf"))
        index += 1

