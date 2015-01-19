from setuptools import setup, find_packages
import io
import codecs
import os
import sys

import soccersimulator

setup(
    name='soccer-simulator',
    version='0.9.2014',
    url='https://github.com/baskiotisn/soccersimulator/',
    license='GPL',
    author='Nicolas Baskiotis',
    install_requires=['numpy',
                    'pyglet',
                    ],
    author_email='nicolas.baskiotis@lip6.fr',
    description='Soccer Simulator and MDP for 2I013 UPMC project',
    packages=find_packages()    
)
