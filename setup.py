import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="Flight radar package",
    version="1.0.0",
    author="l.remkowicz",
    author_email="l.remkowicz@gmail.com",
    description="An package responsible for getting flights data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    url="https://github.com/LukaszRemkowicz/flight_radar",
    packages=find_packages(exclude=["docs", "tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        'Natural Language :: English',
    ],
    cmdclass={'test': PyTest},
    setup_requires=["setuptools>=38.6.0", "pytest"],
    entry_points={"console_scripts": ["pm_core=pm_core"]},
)
