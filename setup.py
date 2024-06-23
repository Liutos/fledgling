# -*- coding: utf8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fledgling",
    version="0.0.1",
    author="Liutos",
    author_email="mat.liutos@gmail.com",
    description="Client of nest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Liutos/fledgling",
    project_urls={
        "Bug Tracker": "https://github.com/Liutos/fledgling/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    scripts=[
        "bin/fledgling",
    ],
    include_package_data=True,
    install_requires=[
        "PyInquirer",
        "click",
        "colored",
        "cryptography",
        "jieba",
        "python-daemon",
        "requests",
        "tabulate",
        "wcwidth",
        "xdg",
    ],
)
