import os, re, sys, time, subprocess


def judgeMem(mystr):
    restr = re.search("\d+(\.\d+)?", mystr)
    return restr.group()


def clearCache(deviceNum):
    aa = os.popen("adb -s {} shell free -h".format(deviceNum))
    bb = aa.read().split()[7]
    cc = judgeMem(bb)
    if cc > str(6.0):
        subprocess.call("adb -s {} shell echo 3 > /proc/sys/vm/drop_caches".format(deviceNum),shell=True)
        return
    else:
        return


def main():
    a = os.popen("adb devices")
    b = a.read().split()
    if sys.argv[1] in b:
        myDevice = sys.argv[1]
        i = 1
        while i < 480:
            time.sleep(60)
            clearCache(myDevice)
            i += 1
    else:
        print("please enter deviceNum!")
        
        
if __name__ == "__main__":
    main()
