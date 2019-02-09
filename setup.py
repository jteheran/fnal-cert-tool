import os
from distutils.core import setup
from distutils.sysconfig import get_python_lib

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "FNALCertTool",
    version = "0.0.1",
    author = "Jeny Teheran",
    author_email = "jteheran@fnal.gov",
    description = ("A utility to request and manage certificates."),
    data_files = [('/usr/bin/')],
    packages=['fnalcert_tool'],
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python"
        "Operating System :: POSIX :: Linux"
    ],
)

