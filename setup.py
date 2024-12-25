from setuptools import setup, find_packages

setup(
    name="ezarduino",
    version="1.0.0",
    packages=find_packages(),
    description="A basic Arduino connector library.",
    author="Crate",
    author_email="crate.arg@proton.me",
    url='https://github.com/cr4t3/arduino-py',
    install_requires=[
        "pyserial>=3.5"
    ]
)