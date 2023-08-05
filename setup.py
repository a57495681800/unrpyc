#!/usr/bin/python3
from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='unrpyc',
    version='1.1.8.1',
    description='Tool to decompile Ren\'Py compiled .rpyc script files.',
    long_description=readme(),
    url='https://github.com/a57495681800/unrpyc',
    py_modules=['unrpyc', 'deobfuscate'],
    packages=find_packages(),
    install_requires=[
        # 在这里添加你的项目依赖的其他 Python 包
    ],
    entry_points={
        'console_scripts': [
            'unrpyc = unrpyc:main',
        ],
    },
    zip_safe=False,
)