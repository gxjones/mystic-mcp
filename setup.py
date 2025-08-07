"""Setup script for mystic-mcp package."""

import os

from setuptools import find_packages, setup

# Read the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="mystic-mcp",
    version="0.1.0",
    author="Grant Jones",
    author_email="grant@gxjones.com",
    description="A Python package for MCP integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gxjones/mystic-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "mystic-mcp=mystic_mcp.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
