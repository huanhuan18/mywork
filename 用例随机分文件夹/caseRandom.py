import os
import random
from shutil import copyfile


class RandomFile():
    def __init__(self, path):
        self.path = path

    def filerandom(self):
        filelist = []
        allfile = os.listdir(self.path)
        for file in allfile:
            if file.endswith(".txt"):
                if os.path.exists(file + ".cpat"):
                    filelist.append(file)
        random.shuffle(filelist)
        return filelist


path = r""
def allot(n):
    filelist = RandomFile(path).filerandom()
    if len(filelist) < n:
        os.makedirs(os.path.join(path, str(i)))
    else:
        os.makedirs(os.path.join(path, str(i)))
    for i in range(0, n + 1):
        for file in filelist:
            p = filelist.index(file)
            if p % n == i:
                copyfile(os.path.join(path, file), os.path.join(path, str(i), file))
                copyfile(os.path.join(path, file+".cpat"), os.path.join(path, str(i), file+".cpat"))
                copyfile(os.path.join(path, file+".ini"), os.path.join(path, str(i), file+".ini"))


if __name__ == "__main__":
    allot(35)