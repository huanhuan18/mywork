## 版本对应：
PyQt5==5.15.1
PyInstaller==3.4
pyinstaller-hooks-contrib==2020.11

报错：
### 1.
  File "e:\git_repositories\pyqt_tmp\tiaoseqi\lib\site-packages\PyInstaller\building\api.py", line 273, in assemble
    pylib_name = os.path.basename(bindepend.get_python_library_path())
  File "D:\Software\work\python37\lib\ntpath.py", line 214, in basename
    return split(p)[1]
  File "D:\Software\work\python37\lib\ntpath.py", line 183, in split
    p = os.fspath(p)
TypeError: expected str, bytes or os.PathLike object, not NoneType
### 1.solution（https://www.jianshu.com/p/71b1c4aaf06d）
修改venv/Lib/site-packages/PyInstaller/depend/bindepend.py文件，到函数get_python_library_path里面，在if is_unix:上方添加
if is_win and 'VERSION.dll' in dlls:
        pydll = 'python%d%d.dll' % sys.version_info[:2]
        if pydll in PYDYLIB_NAMES:
            filename = getfullnameof(pydll)
            return filename