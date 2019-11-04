import os
import sys
import socket
import getpass
import subprocess
import sqlDeal

name = socket.gethostname()
ip = socket.gethostbyname(name)
user = getpass.getuser()
userip = user + "@" + ip

server_case_path = r""
server_result_path = r""
server_backup_path = r""


class AdbRun():
    def __init__(self, cmd, deviceNum):
        self.cmd = cmd
        self.deviceNum = deviceNum

    def adbrun(self):
        cmd = self.cmd
        pipe = subprocess.Popen("adb -s {} shell".format(self.deviceNum), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        code = pipe.communicate("\n".join(cmd))
        return code

class Run():
    def __init__(self, caseType, deviceNum):
        self.caseType = caseType
        self.deviceNum = deviceNum

    def run(self):
        caseType = self.caseType.decode()
        deviceNum = self.deviceNum.decode()

        if caseType in ["game", "benchmark", "application"]:
            print("deviceNum is {}".format(deviceNum))
            print("caseType is {}".format(caseType))

            os.system("adb remount")
            os.system("adb -s {} shell".format(deviceNum))
            os.system("rm -rf /data/log/android_logs")
            os.system("rm -rf /data/tombstones")

            # 获取版本号
            version = os.listdir(os.path.join(server_case_path, caseType))[0]
            # 获取Android路径
            AndroidCasePath = "/data/keyFrameRun" + version
            # 插入数据库
            record = sqlDeal.insertTask(caseType)
            # 将用例push到手机
            cmd = ["adb -s {} push {} {}".format(deviceNum, server_case_path, AndroidCasePath)]
            subprocess.call(cmd)
            print("run {},importing case mow,please wait...".format(caseType))

            adbs = ["sh "]
            caserun = AdbRun(adbs, deviceNum)
            caserun.adbrun()

            # 创建结果路径
            result_path = os.path.join(server_result_path, version, "{}".format(caseType))
            if os.path.exists(result_path):
                pass
            else:
                os.makedirs(result_path)
            cmd = ["adb -s {} pull {} {}".format(deviceNum, AndroidCasePath, result_path)]
            subprocess.call(cmd)

            # 创建备份路径
            backup_path = os.path.join(server_backup_path, version, "{}".format(caseType))
            if os.path.exists(backup_path):
                pass
            else:
                os.makedirs(backup_path)
            cmd = ["adb -s {} pull {} {}".format(deviceNum, AndroidCasePath, backup_path)]
            subprocess.call(cmd)