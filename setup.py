from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
        Extension('mini_project2.phase1.extractTermsFrom', ['mini_project2/phase1/extractTermsFrom.pyx']),
        Extension('mini_project2.phase1.serializeDocumentsFrom', ['mini_project2/phase1/serializeDocumentsFrom.pyx'])
        ]

setup(
    ext_modules = cythonize(extensions)
)
