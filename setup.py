from setuptools import setup
from Cython.Build import cythonize
import os


setup(
    ext_modules = cythonize(os.path.join('mini_project2', 'phase1', '*.pyx'), annotate=True)
)
