import os
from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize

# with open("README.md", "r") as fh:
    # long_description = fh.read()

extensions = [
        Extension('mini_project2.phase1.extractTermsFrom', [os.path.join('mini_project2','phase1', 'extractTermsFrom.pyx')]),
        Extension('mini_project2.phase1.serializeDocumentsFrom', [os.path.join('mini_project2','phase1', 'serializeDocumentsFrom.pyx')])
        ]

setup(
    name='mini_project2',
    version='0.0.1',
    author='Jejoon Ryu, Moe Numasawa, Junhyeon Cho',
    author_email='jejoon@ualberta.ca, numasawa@ualberta.ca, junhyeon@ualberta.ca',
    description='CMPUT 291 F20 mini project 2',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    license="MIT License",
    packages=find_packages(),
    install_requires=[
        "cython",
        "pymongo",
        "motor"
    ],
    ext_modules = cythonize(extensions),
    url='https://github.com/rjejoon/291_mini_project2',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.5',
)
