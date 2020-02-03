# coding=utf-8

from setuptools import setup  # , find_packages

setup(
    name='GStruct',
    version='0.1.200203',
    description=(
        '"GStruct" is a pythonic "struct" type framework similar to Golang struct, '
        'with self-created "interface" for it.'
    ),
    long_description=open('README.rst').read(),
    author='DJun',
    author_email='djunxp@gmail.com',
    maintainer='DJun',
    maintainer_email='djunxp@gmail.com',
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
        'jsonpath-rw',
    ],
)
