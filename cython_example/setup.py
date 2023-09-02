# from distutils.core import Extension, setup
# from Cython.Build import cythonize
# try:
#     from setuptools import setup
#     from setuptools import Extension
# except ImportError:
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import requests
from bs4 import BeautifulSoup

# define an extension that will be cythonized and compiled
ext = Extension(name="cutil", sources=["util.py"])
setup(ext_modules=cythonize(ext))
