import uproot
import h5py
import argparse
import numpy as np
from tqdm import tqdm


def root2hdf5(input_root_file: str, output_hdf5_file: str, tree_name: str) -> None:
    """
    Convert a CERN ROOT file into HDF5 format.

    Parameters:
    - input_root_file (str): The name of the input ROOT file.
    - output_hdf5_file (str): The name of the output HDF5 file.
    - tree_name (str): The name of the tree to be processed.
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
            raise ValueError(
                f"Tree '{tree_name}' does not exist in the ROOT file. Available trees: {list(root_file.keys())}"
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
            branch_data[branch_name] = np.array(tree[branch_name].array(library="np"))

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
