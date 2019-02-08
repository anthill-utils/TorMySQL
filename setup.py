# -*- coding: utf-8 -*-
# 14-8-8
# create by: snower

from setuptools import setup


setup(
    name='anthill-tormysql',
    version='0.4.0',
    packages=['tormysql', 'tormysql.platform'],
    install_requires=[
        'tornado>=5.0',
        'anthill-PyMySQL>=0.9.999',
        'greenlet>=0.4.2',
    ],
    author='snower, mosquito',
    author_email='sujian199@gmail.com, me@mosquito.su',
    url='https://github.com/snower/TorMySQL',
    license='MIT',
    keywords=[
        "tornado", "mysql"
    ],
    description='Tornado asynchronous MySQL Driver',
    long_description=open("README.rst").read(),
    zip_safe=False,
)
