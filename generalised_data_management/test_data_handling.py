# Description: Test file for data_handling.py

from data_handling import HDF5Manager
import pytest
import h5py
import numpy as np

# HDF5Manager Tests

class TestHDF5ManagerRead:
    # Setup test files
    @pytest.fixture
    def set_up_existing_file(self):

        """Create an HDF5 file and return its path."""

        file_path = 'existing_file.h5'
        with h5py.File(file_path,'w') as file:
            group = file.create_group('/test_group')
            group.create_dataset('test_dataset', data=[1,2,3])
        return file_path
    
    @pytest.fixture
    def set_up_nonexistent_file(self):

        """Return the path of a nonexistent file."""

        return 'nonexistent_file.h5'
    
    @pytest.fixture
    def setup_non_hdf5_file(self):

        """Create a non-HDF5 file and return its path."""

        non_hdf5_file_path = 'non_hdf5_file.txt'
        with open(non_hdf5_file_path,'w') as file:
            file.write('This is not an HDF5 file.')
        return non_hdf5_file_path

    # Define test methods
    def test_data_attribute_is_populated_after_read(self, set_up_existing_file):

        """Test that reading an existing file populates the data attribute."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        manager.read()
        # Verify
        assert manager.data is not None

    def test_data_attribute_is_empty_before_read(self, set_up_existing_file):

        """Test that the data attribute is empty before reading."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        # Verify
        assert manager.data is None

    def test_data_contains_h5py_File_object(self, set_up_existing_file):

        """Test that the data attribute contains an h5py.File object after reading."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        manager.read()
        # Verify
        assert isinstance(manager.data, h5py.File)

    def test_read_nonexistent_file_raises_FileNotFoundError_and_logs_exception(self,caplog,set_up_nonexistent_file):
        
        """Test that reading a nonexistent file raises FileNotFoundError and logs the exception."""

        # Set up
        file_path = set_up_nonexistent_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        # Verify
        with pytest.raises(FileNotFoundError):
            manager.read()
        assert "File not found." in caplog.text
        assert "ERROR" in caplog.text

    def test_read_non_hdf5_file_raises_OSError_and_logs_exception(self,caplog,setup_non_hdf5_file):

        """Test that reading a non-HDF5 file raises OSError and logs the exception."""

        # Set up
        file_path = setup_non_hdf5_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        # Verify
        with pytest.raises(OSError):
            manager.read()
        assert "File not readable" in caplog.text
        assert "ERROR" in caplog.text

    def test_re_read_existing_file_raises_ValueError_and_logs_exception(self,caplog,set_up_existing_file):
        
        """Test that reading an existing file with read-only mode raises ValueError 
        and logs the exception."""
        
        # Set up
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        manager.read()
        # Verify
        with pytest.raises(ValueError,match="File has already been read."):
            manager.read()
        assert "File has already been read." in caplog.text
        assert "ERROR" in caplog.text
