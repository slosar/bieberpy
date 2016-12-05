#!/usr/bin/env python
import distutils
from distutils.core import setup

description = "Reader for Signal Hound .bbr files"

setup(name="bieberpy", 
      version="0.1.0",
      description=description,
      url="https://github.com/slosar/bieberpy",
      author="Anze Slosar",
      py_modules=['bieberpy'],
      package_dir={'': 'py'})


