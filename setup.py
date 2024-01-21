import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="root2hdf5",
    version="0.1.0",
    author="Geoffrey Gilles",
    description="Lightweight ROOT to HDF5 file converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-geof/root2hdf5",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "root2hdf5=src:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.9.13",
    test_suite="tests", 
)
