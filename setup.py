#!/usr/bin/env python3
"""
VAPT Automation Engine - Setup Configuration
"""

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vapt-automation-engine",
    version="1.0.0",
    author="VAPT Team",
    author_email="alvinseahsq@gmail.com",
    description="Comprehensive penetration testing automation platform for nVAPT and AVAPT assessments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alvinnnnn/vapt-automation-engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Proprietary License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: Security",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "vapt=vapt.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "vapt": [
            "templates/*.html",
            "templates/*.jinja2",
            "config/*.yaml",
            "config/*.yml",
        ],
    },
    zip_safe=False,
)
