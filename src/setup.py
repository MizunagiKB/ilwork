import sys
from cx_Freeze import setup, Executable

base = None
# if sys.platform == "win32":
#    base = "Win32GUI"

BUILD_EXE_OPTIONS = {
    "packages": ["cv2", "nnabla"],
    "includes": [],
    "excludes": ["tkinter"],
    "include_files": [("lang/ilwork_ja-JP.qm", "lang/ilwork_ja-JP.qm")],
    "include_msvcr": True,
}


setup(
    name="ilwork",
    version="0.0.0",
    description="ilwork",
    author="@MizunagiKB",
    url="",
    options={"build_exe": BUILD_EXE_OPTIONS},
    executables=[Executable("ilwork.py", base=base)],
)
