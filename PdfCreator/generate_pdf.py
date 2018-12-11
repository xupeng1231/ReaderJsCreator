import sys
from PyPDF2 import PdfFileWriter,PdfFileReader
import os
import random
import time
from collections import Counter
from PyPDF2.pdf import *
from PyPDF2.rutils import R, RPools
from mutate_config import MutateCls

InputDir = r"G:\pycharm-projects\ReaderJsCreator\PdfCreator\inputs"

def set_mutate_ratios(context):
    cls_counts = {}
    for cls_str in context["record_counts"]:
        cls = eval(cls_str)
        for m_cls in MutateCls.Mutate_cls:
            if issubclass(cls, m_cls):
                if m_cls not in cls_counts:
                    cls_counts[m_cls] = context["record_counts"][cls_str]
                else:
                    cls_counts[m_cls] += context["record_counts"][cls_str]
                break

    context["mutate_clss"]=[]
    for cls in MutateCls.Mutate_cls:
        context["mutate_ratios"][cls] = MutateCls.Cls_mutate_ratio[cls]()
        context["mutate_clss"].append(cls)

    return

def convert_set_list(context):
    for k in context["interesting_values"]:
        if isinstance(context["interesting_values"][k],set):
            context["interesting_values"][k]=list(context["interesting_values"][k])

def generate(samples, output_dir, num=5):
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
        context={
            "interesting_values": {
                "num": set(),
                "name_str": set(),
                "byte_str": set(),
                "text_str": set(),
                "float": set(),
                "dict_item": {},
            },
            "record_switch": True,
            "record_counts": {},

            "mutate_switch": False,
            "mutate_ratios": {},
            "mutate_clss":[],
            "mutated_stacks": [],
            "mutated_cls_list":[],

            "wrote_stacks": [],
        }
        devnull = StringIO()
        output.write(devnull, context)
        del devnull

        # pre handle context
        set_mutate_ratios(context)
        convert_set_list(context)

        context["record_switch"] = False
        context["mutate_switch"] = True
        outfilename = "{}_{:01d}_{:08x}.pdf".format(time.strftime("%m_%d_%H_%M_%S"), len(outpages), random.getrandbits(32), )
        outfilename = os.path.join(output_dir, outfilename)
        outfile = file(outfilename, "wb")
        output.write(outfile, context)
        outfile.close()
        # print outfilename
        # print Counter(context["mutated_cls_list"]),

def main():
    # random.seed(1)
    usage = "Usage: python generate_pdf.py <sample_dir> <output_dir> <num>"
    if len(sys.argv) != 4:
        print usage
        exit(1)
    sample_dir = sys.argv[1]
    output_dir = sys.argv[2]
    num_str = sys.argv[3]
    if not num_str.isalnum():
        print "3rd arg is not a num"
        exit(1)
    if not os.path.isdir(sample_dir):
        print "%s is not a dir" % sample_dir
        exit(1)
    if not os.path.isdir(output_dir):
        print "%s is not a dir" % output_dir
        exit(1)
    num =int(num_str)
    sample_filename_list = [c for c in os.listdir(sample_dir) if c.endswith(".pdf")]
    if len(sample_filename_list) == 0:
        print "%s sample_dir is empty!" % sample_dir
        exit(1)
    sample_num = R.select(RPools.sample_num_pool)
    samples = [os.path.join(sample_dir, c) for c in random.sample(sample_filename_list, min(sample_num,len(sample_filename_list)))]
    generate(samples, output_dir, num)

if __name__ == "__main__":
    main()
    # # search_pdf()
    # prehandle_pdf()