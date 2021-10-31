from setuptools import setup

APP = ["ilwork.py"]
DATA_FILES = []
OPTIONS = {"includes": ["cv2.config", "cv2.config-3.8"], "packages": ["cv2"]}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
