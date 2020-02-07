# coding=utf-8

from setuptools import setup  # , find_packages

from gstruct.__init__ import __version__, __author__, __author_email__

setup(
    name='GStruct',
    version=__version__,
    description=(
        '"GStruct" is a pythonic "struct" type framework similar to Golang struct, '
        'with self-created "interface" for it.'
    ),
    long_description=open('README.rst').read(),
    author=__author__,
    author_email=__author_email__,
    maintainer=__author__,
    maintainer_email=__author_email__,
    license='MIT License',
    # packages=find_packages(),
    packages=[
        'gstruct',
    ],
    platforms=["all"],
    url='https://github.com/djun/gstruct',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
    ],
)
