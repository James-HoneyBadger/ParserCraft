#!/usr/bin/env python3
"""
Setup script for ParserCraft - Custom Language Construction Framework
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="parsercraft",
    version="3.0.0",
    author="James HoneyBadger",
    description=("ParserCraft - Create custom programming languages "
                 "without writing a compiler"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/James-HoneyBadger/ParserCraft",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    license="MIT",
    python_requires=">=3.7",
    install_requires=[
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "ide": [
            "tkinter",  # Usually included with Python
        ],
    },
    entry_points={
        "console_scripts": [
            "parsercraft=parsercraft.cli:main",
            "parsercraft-ide=parsercraft.launch_ide:main",
            "codex=codex.codex:main",
        ],
    },
    include_package_data=True,
    package_data={
        "parsercraft": ["*.json", "*.yaml"],
    },
)
