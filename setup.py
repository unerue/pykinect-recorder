from setuptools import find_packages, setup
from numpy.distutils.misc_util import Configuration
from distutils.command.clean import clean as Clean
from distutils.command.sdist import sdist
import os
import shutil


setup(
    name='pykinect recorder',
    version='0.2',
    author='Kyungsu',
    author_email='unerue@me.com',
    maintainer='Kyungsu',
    maintainer_email='unerue@me.com',
    keywords="azure, kinect, deep-learning, computer-vision",
    url="https://github.com/unerue/pykinect-recorder",
    description='PyKinect Recorder with Pyside6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pykinect = pykinect_recorder.main.cli.command:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.8.1'
)
    

