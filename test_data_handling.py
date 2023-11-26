# Description: Test file for data_handling.py

from data_handling import HDF5Manager
import pytest
import h5py

# HDF5Manager Tests
class HDF5_Read_Tests:
    # Setup test files
    @pytest.fixture
    def set_up_existing_file(self):
        file_path = 'existing_file.h5'
        with h5py.File(file_path,'w') as file:
            group = file.create_group('/test_group')
            group.create_dataset('test_dataset', data=[1,2,3])
        return file_path