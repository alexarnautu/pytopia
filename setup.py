import setuptools

version = "1.0.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytopia",
    version="1.0.0",
    author="Alexandru Arnautu",
    author_email="alex.arnautu96@gmail.com",
    description="Wrapper for Cryptopia API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexarnautu/pytopia/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)