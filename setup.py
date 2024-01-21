import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="root2hdf5",
    version="0.1.3",
    author="Geoffrey Gilles",
    description="Lightweight ROOT to HDF5 file converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-geof/root2hdf5",
    packages=setuptools.find_packages(),
    install_requires=[
        'uproot==5.0.4',
        'h5py==3.8.0',
        'numpy==1.24.2',
        'tqdm==4.62.3',
    ],
    entry_points={
        "console_scripts": [
            "root2hdf5=src.root2hdf5:main",
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
