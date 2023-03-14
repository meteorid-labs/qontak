from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in qontak/__init__.py
from qontak import __version__ as version

setup(
	name="qontak",
	version=version,
	description="Qontak Integration",
	author="Meteor Inovasi Digital",
	author_email="info@meteor.id",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
