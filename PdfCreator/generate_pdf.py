from PyPDF2 import PdfFileWriter,PdfFileReader
import sys
import os
import random
import time
from tools import *

InputDir = r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\inputs"
class RPools:
    sample_num_pool = [1]*10 + [2]*40 + [3]*40 + [4]*10
    output_numpage_pool = [2]*10 + [3]*15 + [4]*20 + [5]*25 + [6]*15 + [7]*10 + [8]*5

class R:
    def select(arr):
        assert isinstance(arr,list)
        return random.choice(arr)
    select = staticmethod(select)

def generate(samples, num=1):
    inputs = [PdfFileReader(c) for c in samples]
    outputs = [PdfFileWriter() for c in range(num)]

    input_pages = []
    for input in inputs:
        numpages=input.getNumPages()
        if numpages <=5:
            input_pages.extend([input.getPage(c) for c in range(numpages)])
        else:
            for iii in range(5):
                input_pages.append(input.getPage(random.choice(range(numpages))))

    for output in outputs:
        outpage_num = random.choice(RPools.output_numpage_pool)
        outpages = random.sample(input_pages, min(outpage_num, len(input_pages)))
        for outpage in outpages:
            output.addPage(outpage)

        outfilename = "{}_{:01d}_{:08x}.pdf".format(time.strftime("%m_%d_%H_%M_%S"), len(outpages), random.getrandbits(32),)
        outfilename=os.path.join(InputDir,outfilename)

        outfile = file(outfilename, "wb")
        output.write(outfile)
        outfile.close()

def main():
    usage = "Usage: python generate_pdf.py <sample_dir>"
    sys.argv.append(r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\samples")
    if len(sys.argv) != 2:
        print usage
        exit(1)
    sample_dir = sys.argv[1]
    if not os.path.isdir(sample_dir):
        print "%s is not a dir" % sample_dir
        exit(1)
    sample_filename_list = [c for c in os.listdir(sample_dir) if c.endswith(".pdf")]
    if len(sample_filename_list) == 0:
        print "%s sample_dir is empty!" % sample_dir
        exit(1)
    for iii in range(50):
        sample_num = R.select(RPools.sample_num_pool)
        samples = [os.path.join(sample_dir, c) for c in random.sample(sample_filename_list, min(sample_num,len(sample_filename_list)))]
        generate(samples, 5)

if __name__ == "__main__":
    main()
    # # search_pdf()
    # prehandle_pdf()