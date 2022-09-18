import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Pomodoro timer",
      version= "1.0",
      description="Pomodoro techique for effective time management",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])