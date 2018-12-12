import pykd
import os
import time
import shutil
import sys
import datetime
from subprocess import Popen,call
import traceback

def log(log_str):
    with open("confirm.log", "at") as log:
        log.write(log_str)
        log.write("\n\n")

# !py windbg.py file_name base_dir

# this script run most 20 seconds
enter_time = time.time()
expire_time = enter_time + 20

base_dir = sys.argv[2]
confirm_dir = os.path.join(base_dir, "confirms")
crash_dir = os.path.join(base_dir, "crashes")
if not os.path.exists(confirm_dir):
    log("Warning:confirms dir({}) not exists, will create it.".format(confirm_dir))
    os.makedirs(confirm_dir)
if not os.path.exists(crash_dir):
    log("Error: crash folder({}) not exists, exit.".format(crash_dir))
    os._exit(0)


e = pykd.dbgCommand

def save_sample(who_find):
    # log
    try:
        log( str(who_find)+" confirmed!!!"+"#"*64+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    except:
        traceback.print_exc()
        pass

    sample_file = sys.argv[1]
    # save the crash sample to confirm folder
    try:
        Popen("copy "+os.path.join(crash_dir, sample_file)+" "+os.path.join(confirm_dir, sample_file), shell=True)
    except:
        traceback.print_exc()

    # save a log file about this crash sample
    try:
        logf=open(os.path.join(confirm_dir,"log_"+sample_file+".txt"),"wt")
        logf.write("*"*40+".lastevent"+"*"*40+"\n"*2)
        logf.write(e(".lastevent")+"\n"*4)
        logf.write("*"*40+"r"+"*"*40+"\n"*2)
        logf.write(e("r")+"\n"*4)
        logf.write("*"*40+"u "+"*"*40+"\n"*2)
        logf.write(e("u")+"\n"*4)
        logf.write("*"*40+"ub"+"*"*40+"\n"*2)
        logf.write(e("ub eip")+"\n"*4)
        logf.write("*"*40+"callstack"+"*"*40+"\n"*2)
        logf.write(e("kv")+"\n"*4)
        logf.write("*" * 40 + "lm" + "*" * 40 + "\n" * 2)
        logf.write(e("lm") + "\n" * 4)
        logf.close()
    except:
        traceback.print_exc()
        log( "ERROE:crashlog create error!")

while True:
    # check if expiration time arrived.
    if time.time() > expire_time:
        break

    try:
        # only fuzz 1 process
        if 1!=pykd.getCurrentProcessId():
            e("g")
            continue

        # sxd some breakpoint, and go;
        res_g=e("sxd cpr;sxd ld;sxd ct;sxd et;g")

        # get some information
        lastevent=e(".lastevent")
        r=e("r")
        kl2=e("k L2")

        # see if any crash
        # if break at verifier!VerifierStopMessage, maybe a page heap crash occur.
        if kl2.find("verifier!VerifierStopMessage")>=0:
            save_sample(lastevent)
            time.sleep(2)
            break
        # filter some normal breakpoint, otherwise will be treated as a crash.
        if lastevent.find("Break instruction exception") > 0 or lastevent.find("Exit process") > 0 or r.find("ntdll!KiFastSystemCallRet") > 0:
            continue
        else:
            save_sample(lastevent)
            time.sleep(2)
            break
    except:
        pass