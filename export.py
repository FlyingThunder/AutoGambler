import sys
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["pyscreenshot","PIL","sys","pydirectinput","time","os","multiprocessing"]#,
    #"includes": ["QtOutput", "Settings", "BrowseFileSystem"] # <-- Include easy_gui
}

base = None
if sys.platform == "win32":
	base = None#"Win32GUI"

setup(  name = "Autogambler",
        version = "0.1",
        description = "Python 3 Autogambler for Chromerivals",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])