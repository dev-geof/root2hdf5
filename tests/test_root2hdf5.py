import unittest
import os
import h5py
import numpy as np
from src.root2hdf5 import root2hdf5


class TestRoot2HDF5Converter(unittest.TestCase):
    def test_conversion(self):
        # Define paths
        input_root_file = "tests/test.root"
        output_hdf5_file = "tests/test_output.h5"
        tree_name = "Tree"

        # Run the conversion
        root2hdf5(input_root_file, output_hdf5_file, tree_name)

        # Check if the HDF5 file is created
        self.assertTrue(os.path.exists(output_hdf5_file))

        # Check if the HDF5 file contains the correct dataset
        with h5py.File(output_hdf5_file, "r") as file:
            self.assertTrue(tree_name in file.keys())
            dataset = file[tree_name]
            self.assertIsInstance(dataset, h5py.Dataset)

            # Compare some values to ensure conversion correctness
            expected_data = np.array(
                [(1, 2.5, 3.5), (2, 3.5, 4.5), (3, 4.5, 5.5)],
                dtype=[("Branch1", "<i4"), ("Branch2", "<f4"), ("Branch3", "<f8")],
            )
            np.testing.assert_array_equal(dataset[:], expected_data)

        # Clean up - remove the created HDF5 file
        os.remove(output_hdf5_file)


if __name__ == "__main__":
    unittest.main()
