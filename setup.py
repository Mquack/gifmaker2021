import sys
from cx_Freeze import setup, Executable

#Currently not working. The exe is created and the app launches like it should but no gif is created.
#Apparently a lot of modules are missing...

#setup script for cx_freeze, -> python3 setup.py build


build_exe_options = {"packages": ["os"]}
# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

includefiles = ["vis_gust_small_icon.ico", "vis_gust_text.png"]
packages = ["os"]
setup(
    name = "guifoo",
    version = "0.1",
    description = "My GUI application!",
    options = {'build_exe': {'packages':packages, 'include_files':includefiles}},
    executables = [Executable("gifMaker.py", base=base)]
)
