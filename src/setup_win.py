import sys
from cx_Freeze import setup, Executable

BASE = None
#if sys.platform == "win32":
#    BASE = "Win32GUI"

BUILD_EXE_OPTIONS = {
    "packages": ["cv2", "nnabla"],
    "includes": [],
    "excludes": ["tkinte"],
    "include_files": [],
    "include_msvcr": True
}


setup(
    name="ilwork",
    version="0.0.0",
    description="ilwork",
    author="@MizunagiKB",
    url="",
    options={
        "build_exe": BUILD_EXE_OPTIONS
    },
    executables=[Executable("ilwork.py", base=BASE)]
)
