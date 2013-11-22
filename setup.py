from setuptools import setup, find_packages

try:
    desc_file = open("README.rst")
    description = desc_file.read()
    desc_file.close()
except:
    description = ""


setup(
    name="wunderpy",
    version="0.2.1",
    author="bsmt",
    author_email="bsmt@bsmt.me",
    url="https://github.com/bsmt/wunderpy",
    license="MIT",
    description="An experimental wrapper for the Wunderlist 2 API",
    long_description=description,
    classifiers=['Development Status :: 4 - Beta',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python',
                'Topic :: Utilities',
                'Topic :: Documentation'
                ],
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests>=1.1.0"],
    entry_points={'console_scripts': ['wunderlist = wunderpy.cli.main:main']}
)
