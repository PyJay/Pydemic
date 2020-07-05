from setuptools import setup

setup(
    name='Epydemic',
    version='0.1.1',
    packages=['epydemic',],
    long_description=open('README.md').read(),
    install_requires=['arcade'],
    entry_points={
        "console_scripts": [
            "epydemic=epydemic.game:main",
        ],},
    package_data={'epydemic': ['data/*.png', 'data/*.mp3']}
)