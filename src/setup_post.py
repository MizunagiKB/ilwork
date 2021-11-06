import platform
import sys
import os
import shutil
import cv2
import nnabla
import nnabla_ext


def copy_module(src_path: str, dst_path: str, module_name: str):
    try:
        shutil.rmtree(os.path.join(dst_path, module_name))
    except FileNotFoundError:
        pass
    shutil.copytree(src_path, os.path.join(dst_path, module_name))


def main():

    if platform.system() == "Darwin":
        os_version, _, os_machine = platform.mac_ver()
        dst_path = "build/exe.macosx-{:s}-{:s}-{:d}.{:d}/lib".format(
            os_version, os_machine, sys.version_info.major, sys.version_info.minor
        )
    elif platform.system() == "Windows":
        dst_path = "build/exe.win-{:s}-{:d}.{:d}/lib".format(
            platform.machine().lower(), sys.version_info.major, sys.version_info.minor
        )
    else:
        return

    copy_module(cv2.__path__[0], dst_path, "cv2")
    copy_module(nnabla.__path__[0], dst_path, "nnabla")
    copy_module(nnabla_ext.__path__[0], dst_path, "nnabla_ext")


if __name__ == "__main__":
    main()
