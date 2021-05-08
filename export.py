import sys
from cx_Freeze import setup, Executable


build_exe_options = {
    "include_files": ["icon.ico"],
    "packages": ["pyscreenshot","PIL","sys","pydirectinput","time","os","multiprocessing"],
    "includes": ["Autogambler"] # <-- Include easy_gui

}

base = None
if sys.platform == "win32":
	base = None#"Win32GUI"

setup(  name = "Autogambler",
        version = "0.1",
        description = "Python 3 Autogambler for Chromerivals",
        options = {"build_exe": build_exe_options},
        executables = [Executable(script="main.py", base=base, icon='icon.ico')])



#kein screenshot im build => https://stackoverflow.com/questions/57859801/after-converting-to-exe-pyscreenshot-doesnt-take-screenshots