# Description: Test file for data_handling.py

from data_handling import HDF5Manager
import pytest
import h5py
import os

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
    
    @pytest.fixture
    def set_up_nonexistent_file(self):
        return 'nonexistent_file.h5'
    
    @pytest.fixture
    def setup_non_hdf5_file(self):
        non_hdf5_file_path = 'non_hdf5_file.txt'
        with open(non_hdf5_file_path,'w') as file:
            file.write('This is not an HDF5 file.')
        return non_hdf5_file_path
    
    @pytest.fixture
    def setup_no_permissions_file(self):
        no_permission_file_path = 'no_permission_file.h5'
        with h5py.File(no_permission_file_path,'w') as file:
            # Create dummy file content to test if file is readable
            group = file.create_group('/test_group')
        # Change file permissions to read-only
        os.chmod(no_permission_file_path, 0o400)
        return no_permission_file_path
