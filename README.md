# Lightweight ROOT to HDF5 File Converter

## Introduction

The `root2hdf5` tool provides a streamlined solution for converting CERN ROOT files into HDF5 format. This lightweight implementation specifically targets ROOT files containing `TTree` structures, seamlessly transforming them into organized HDF5 compound datasets.

## Getting the Code

To get started you can clone the `root2hdf5` repository from GitHub using the following command:
```bash
git clone https://github.com/dev-geof/root2hdf5.git
```

## Installation

To install `root2hdf5` and its dependencies you can use the following command:
```bash
python -m pip install -e . -r requirements.txt
```
Pre-built `root2hdf5` can also be installed from PyPI via:
```bash
pip install root2hdf5
```

## Usage

### Script Invocation

```bash
root2hdf5 -i input_root_file -o output_hdf5_file -t tree_name
```

### Parameters

- **input_root_file** (str): The name of the input ROOT file.
- **output_hdf5_file** (str): The name of the output HDF5 file.
- **tree_name** (str): The name of the ROOT tree to be processed.

## License

`root2hdf5` is distributed under the [MIT License](LICENSE), granting users the freedom to use, modify, and distribute the code. Contributions, bug reports, and suggestions for improvements are warmly welcomed.

