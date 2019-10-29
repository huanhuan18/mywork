import os, sys
import logging

logging.basicConfig(level=logging.DEBUG,format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",filename="logging.log",filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

the_params = sys.argv[1].split(",")
logging.info(the_params)

# 获取设备号
a = os.popen("adb devices")
b = a.read()
deviceNum = b.split()[4]
logging.info("deviceNum is {}".format(deviceNum))