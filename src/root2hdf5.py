import uproot
import h5py
import argparse
import numpy as np
from tqdm import tqdm


def convert_vector_branch(branch):
    """
    Convert a vector branch to a format suitable for HDF5 storage.

    Parameters:
    - branch (array-like): The vector branch to be converted.

    Returns:
    - np.ndarray: An array suitable for HDF5 storage.

    Notes:
    This function is designed to handle vector branches in ROOT files, where each entry in the branch
    is a vector (list or array) of elements. The function flattens the nested arrays and stores them
    as a structured array, allowing it to be stored in HDF5 datasets.

    Example:
    If the input vector branch looks like:
    [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]

    The output would be:
    array([(1, 2, 3), (4, 5, 6), (7, 8, 9)], dtype=[('f0', '<f8'), ('f1', '<f8'), ('f2', '<f8')])
    """
    flattened_branch = np.array(branch).flatten()
    dtype = [(f"f{i}", "<f8") for i in range(len(flattened_branch))]
    return np.array([tuple(x) for x in flattened_branch], dtype=dtype)


def root2hdf5(input_root_file: str, output_hdf5_file: str, tree_name: str) -> None:
    """
    Convert a CERN ROOT file into HDF5 format.

    Parameters:
    - input_root_file (str): The name of the input ROOT file.
    - output_hdf5_file (str): The name of the output HDF5 file.
    - tree_name (str): The name of the ROOT tree to be processed.

    Raises:
    - ValueError: If the specified tree does not exist in the ROOT file or if the output dataset
      already exists in the HDF5 file.

    Notes:
    This function reads a ROOT file, extracts the specified tree, and converts its branches into
    an HDF5 dataset. Numeric branches are directly converted, while vector branches are transformed
    into arrays suitable for HDF5 storage.

    Example:
    ```python
    root2hdf5("input.root", "output.h5", "my_tree")
    ```

    In this example, the function reads the "my_tree" from "input.root" and saves it as an HDF5 dataset
    in "output.h5".
    """
    try:
        # Open ROOT file
        root_file = uproot.open(input_root_file)

        # Check if the specified tree exists without version suffix
        matching_tree_name = None
        for key in root_file.keys():
            if key.split(";")[0] == tree_name:
                matching_tree_name = key
                break

        if matching_tree_name is None:
            available_trees = [key.split(";")[0] for key in root_file.keys()]
            raise ValueError(
                f"Tree '{tree_name}' does not exist in the ROOT file. Available trees: {available_trees}"
            )

        # Find the latest version suffix for the specified tree name
        latest_version_suffix = 0
        for key in root_file.keys():
            if key.startswith(f"{tree_name};"):
                version_suffix = int(key.split(";")[1])
                latest_version_suffix = max(latest_version_suffix, version_suffix)

        # Rebuild the complete tree name with the latest version suffix
        complete_tree_name = f"{tree_name};{latest_version_suffix}"

        # Extract the tree from the root file
        tree = root_file[complete_tree_name]

        # Get the list of branch names in the tree
        branch_names = tree.keys()

        # Initialize a dictionary to store arrays for each branch
        branch_data = {}

        # Loop over branches, extract data, and save as individual arrays
        for branch_name in tqdm(branch_names):
            # Extract the array for the current branch
            branch_array = tree[branch_name].array(library="np")

            # Check if the array has a numeric dtype
            if np.issubdtype(branch_array.dtype, np.number):
                branch_data[branch_name] = np.array(branch_array)
            elif isinstance(
                branch_array[0], (list, np.ndarray)
            ):  # Check if it's a vector branch
                branch_data[branch_name] = convert_vector_branch(branch_array)
            else:
                print(
                    f"Skipping branch '{branch_name}' with unsupported type: {branch_array.dtype}"
                )

        # Combine the arrays into a structured array
        data = np.array(
            list(zip(*branch_data.values())),
            dtype=[(name, arr.dtype) for name, arr in branch_data.items()],
        )

        # Create an HDF5 file
        with h5py.File(output_hdf5_file, "w") as file:
            # Check if the output file already exists
            if tree_name in file.keys():
                raise ValueError(
                    f"Dataset '{tree_name}' already exists in the HDF5 file. Please choose a different output file or dataset name."
                )

            # Create a compound dataset
            dataset = file.create_dataset(
                tree_name, shape=(len(data),), dtype=data.dtype
            )

            # Write the data to the dataset
            dataset[:] = data

    except Exception as e:
        print(f"Error:{str(e)}")


def main():
    """
    Entry point for the ROOT to HDF5 conversion script.

    Parses command-line arguments and invokes the root2hdf5 function.
    """
    parser = argparse.ArgumentParser(description="ROOT to HDF5 file converter")
    parser.add_argument(
        "-i",
        action="store",
        dest="input_root_file",
        default="input.root",
        help="Name of the input ROOT file",
    )
    parser.add_argument(
        "-o",
        action="store",
        dest="output_hdf5_file",
        default="output.h5",
        help="Name of the output HDF5 file",
    )
    parser.add_argument(
        "-t",
        action="store",
        dest="tree_name",
        default="tree",
        help="Name of the ROOT tree to be processed",
    )

    args = vars(parser.parse_args())
    root2hdf5(**args)


if __name__ == "__main__":
    main()
