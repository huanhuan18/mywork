import os, shutil

path = r'D:\11111111'
alldir = os.listdir(path)

i = 1
for dir in alldir:
    if os.path.isdir(os.path.join(path, dir)):
        os.rename(os.path.join(path, dir), os.path.join(path, str(i)))
        i += 1