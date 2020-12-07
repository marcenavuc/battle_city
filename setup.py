from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="battle_city",
    version="0.0.1",
    author="Mark Averchenko",
    author_email="markenavuk@bk.ru",
    description="Sample game battle city python implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcenavuc/battle_city",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6, <3.7",
)
