from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
        Extension('mini_project2.phase1.extractTermsFrom', ['mini_project2/phase1/extractTermsFrom.pyx'],
            language='c++',
            extra_compile_args=['-std=c++11', '-mmacosx-version-min=10.9', '-D_hypot=hypot', '-stdlib=libc++'])


        ]

setup(
    ext_modules = cythonize(extensions, annotate=True)
)
