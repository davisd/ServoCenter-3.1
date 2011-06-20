from distutils.core import setup

setup(
    name='ServoCenter-3.1',
    version='0.1.0',
    author='David Davis',
    author_email='davisd@davisd.com',
    py_modules=['servocenter',],
    url='http://www.davisd.com/projects/servocenter-3.1/',
    license='LICENSE',
    requires=['serial'],
    description='ServoCenter-3.1 is a python module for interacting with ' \
    'the ServoCenter 3.1 USB controller board by Yost Engineering, Inc.',
    long_description=open('README').read(),
)
