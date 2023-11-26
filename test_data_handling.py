# Description: Test file for data_handling.py

from data_handling import HDF5Manager
import pytest
import h5py
import os
import logging

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
    
    # Define test methods

    def test_data_attribute_is_populated_after_read(self, set_up_existing_file):
        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path)
        manager.read()
        # Verify
        assert manager.data is not None

    def test_data_attribute_is_empty_before_read(self, set_up_existing_file):
        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path)
        # Verify
        assert manager.data is None

    def test_data_contains_h5py_File_object(self, set_up_existing_file):
        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path)
        manager.read()
        # Verify
        assert isinstance(manager.data, h5py.File)

    def test_read_nonexistent_file_raises_FileNotFoundError_and_logs_exception(self,caplog,set_up_nonexistent_file):
        # Set up
        file_path = set_up_nonexistent_file
        # Exercise
        manager = HDF5Manager(file_path)
        # Verify
        with pytest.raises(FileNotFoundError):
            manager.read()
        assert "File not found." in caplog.text
        assert caplog.records.levelname == "ERROR"

    def test_read_non_hdf5_file_raises_OSError_and_logs_exception(self,caplog,setup_non_hdf5_file):
        # Set up
        file_path = setup_non_hdf5_file
        # Exercise
        manager = HDF5Manager(file_path)
        # Verify
        with pytest.raises(OSError):
            manager.read()
        assert "File is not a valid HDF5 file." in caplog.text
        assert caplog.records.levelname == "ERROR"

    def test_read_no_permission_file_raises_IOError_and_logs_exception(self,caplog,setup_no_permissions_file):
        # Set up
        file_path = setup_no_permissions_file
        # Exercise
        manager = HDF5Manager(file_path)
        # Verify
        with pytest.raises(IOError):
            manager.read()
        assert "File is not readable." in caplog.text
        assert caplog.records.levelname == "ERROR"

    def test_read_existing_file_with_read_only_mode_raises_ValueError_and_logs_exception(self,caplog,set_up_existing_file):
        # Set up
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path, mode='r')
        manager.read()
        # Verify
        with pytest.raises(ValueError):
            manager.read()
        assert "File has already been read." in caplog.text
        assert caplog.records.levelname == "ERROR"
