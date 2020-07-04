from setuptools import setup

setup(
    name='Quorontine',
    version='0.1dev',
    packages=['quorontine',],
    long_description=open('README.txt').read(),
    entry_points={
        "console_scripts": [
            "qorontine=qorontine.game:main",
        ],
)