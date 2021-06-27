"""
metadata
"""

from setuptools import setup, find_packages

# open REAMD.md for long description.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="koncert",
    version="0.0.1",
    author="Jiwon Park",
    author_email="park@jiwon.me",
    description="scraper for NICE Checkplus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiwonMe/KONCERT",
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.8",
)
