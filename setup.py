from setuptools import setup, find_packages
setup(
    name="wunderpy",
    version="0.2",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["requests>=1.1.0"],
    url="https://github.com/bsmt/wunderpy"
)