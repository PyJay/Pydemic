from setuptools import setup

setup(
    name='Quorontine',
    version='0.1dev',
    packages=['qorontine',],
    long_description=open('README.md').read(),
    install_requires=['arcade'],
    entry_points={
        "console_scripts": [
            "qorontine=qorontine.game:main",
        ],}
)