from setuptools import setup
from setuptools import find_packages
import logather

setup(
    name='logather',
    version=logather.__version__,
    description='Public HTTP log gatherer tool',
    url='https://github.com/mtnalonso/logather',
    author='Martin Alonso Vilar',
    author_email='mtnalonso@protonmail.com',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        'requests',
        'pysocks',
        'beautifulsoup4',
    ]
)
