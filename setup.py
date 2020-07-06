from setuptools import setup

setup(
    name='Pydemic',
    version='0.1.7',
    packages=['pydemic',],
    long_description=open('README.md').read(),
    install_requires=['arcade'],
    entry_points={
        "console_scripts": [
            "pydemic=pydemic.game:main",
        ],},
    package_data={'pydemic': ['data/*.png', 'data/*.mp3']}
)