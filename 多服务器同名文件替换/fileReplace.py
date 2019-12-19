# -*- coding: utf-8 -*-
import os, shutil
import openpyxl
import string

src_casename = ["a222", "a555"]
src_casepath = r"F:\AppStore\Bin"

wb1 = openpyxl.load_workbook(r"I:\disk_operation\2227\B11.xlsx")
sheet = wb1.active

alldata = {}

for column in string.ascii_uppercase[0: 18]:      # A到S大写循环
    for row in range(1, sheet.max_row + 1):
        server = sheet[column + "1"].value
        case = sheet[column + str(row)].value
        alldata.setdefault(server, [])  # if "server" exists,pass  else add key named "result"
        alldata[server].append(case)


def searchPath(casename, srcpath):
    """查找文件的完整路径"""
    for path, dirs, files in os.walk(srcpath):
        if casename in files:
            return path

for case in src_casename:
    if os.path.exists(os.path.join(src_casepath, case + ".txt")):
        for server, casename in alldata.items():
            if case in casename:
                src_path = r"\\{}\home\model\workshop".format("10.141.95.57")
                os.chdir(src_path)
                dst_path = searchPath(case, src_path)
                src_file = os.path.join(dst_path, case + ".txt")
                dst_file = os.path.join(src_casepath, case +".txt")
                try:
                    os.remove(src_file)
                    shutil.copy(dst_file, dst_path)
                except Exception as e:
                    print(e)
                else:
                    # os.path.basename()获得路径的最后一个目录
                    print("已替换{}服务器{}文件夹下的{}".format(server, os.path.basename(dst_path), case))
    else:
        print("要替换的文件没准备好！！")