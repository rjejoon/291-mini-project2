import os
from setuptools import Extension, setup
from Cython.Build import cythonize
# from pipenv.project import Project
# from pipenv.utils import convert_deps_to_pip


# pfile = Project(chdir=False).parsed_pipfile
# requirements = convert_deps_to_pip(pfile['packages'], r=False)
# test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

extensions = [
        Extension('mini_project2.phase1.extractTermsFrom', [os.path.join('mini_project2','phase1', 'extractTermsFrom.pyx')]),
        Extension('mini_project2.phase1.serializeDocumentsFrom', [os.path.join('mini_project2','phase1', 'serializeDocumentsFrom.pyx')])
        ]

setup(
    name='291_mini_project2',
    version='0.1.0',
    description='CMPUT 291 mini project 2',
    author='Jejoon Ryu, Moe Numasawa, Junhyeon Cho',
    author_email='jejoon@ualberta.ca, numasawa@ualberta.ca, junhyeon@ualberta.ca',
    # install_requires=requirements,
    ext_modules = cythonize(extensions),
)
