from setuptools import setup

setup(
    name='Qorona',
    version='0.1dev',
    packages=['qorona',],
    long_description=open('README.md').read(),
    install_requires=['arcade'],
    entry_points={
        "console_scripts": [
            "qorona=qorona.game:main",
        ],},
    package_data={'qorona': ['data/*.png', 'data/*.mp3,]}
)