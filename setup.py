import sys
from cx_Freeze import setup, Executable
import gooey
import os
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = (os.path.join(gooey_root, 'languages'), 'gooey/languages')
gooey_images = (os.path.join(gooey_root, 'images'), 'gooey/images')

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["win32com.client"],
    "excludes": [],
    "include_files": [
        gooey_languages,
        gooey_images,
        'img']}

setup(
    name="slpcopy",
    version="0.1",
    description="blorppppp's *.slp copy tool. Copies all *.slp files from thumbdrives onto your machine.",
    options={
        "build_exe": build_exe_options},
    executables=[
        Executable(
            "slpcopy.py",
            icon="icon.ico",
            base='Win32GUI')])
