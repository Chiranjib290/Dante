import sys
import os
from cx_Freeze import setup, Executable

# files = ["favicon.ico",]

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'python310.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'python3.dll'),
            "favicon.ico",
            "configfiles/",
            "configfiles/forbidden_path.info",
            "logo/",
            "logs/",
            "images/",
            "themes/",
        ],
    },
}

target = Executable(
    script="dante_main_app_glbl.py",
    base="Win32GUI",
    icon="favicon.ico",
    copyright="©PricewaterhouseCoopers International Limited. All rights reserved."
)

setup(
    name= "DPE Automation tool",
    version="4.5.0",
    description="Tool that helps to complete DPE works",
    author = "Shouvik Das",
    options = options,
    executables = [target,]
)