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

class TestHDF5ManagerWrite:
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
    
    # group path fixtures
    @pytest.fixture
    def set_up_group_path_with_invalid_characters(self):

        """Return an invalid group path with invalid characters."""

        return '/invalid_group_path?'
    
    @pytest.fixture
    def set_up_empty_group_path(self):

        """Return an empty group path."""

        return ''
    
    @pytest.fixture
    def set_up_group_path_with_invalid_type(self):

        """Return a group path with invalid type."""

        return 1
    
    @pytest.fixture
    def set_up_non_existent_group_path(self):

        """Return a group path that does not exist."""

        return '/non_existent_group_path'
    
    # dataset fixtures

    @pytest.fixture
    def set_up_dataset_name_with_invalid_characters(self):

        """Return a dataset name with invalid characters."""

        return 'invalid_dataset_name?'
    
    @pytest.fixture
    def set_up_empty_dataset_name(self):

        """Return an empty dataset name."""

        return ''
    
    @pytest.fixture
    def set_up_dataset_name_with_invalid_type(self):

        """Return a dataset name with invalid type."""

        return 1
    
    # Define test methods

    def test_data_attribute_updated_after_write(self, set_up_existing_file):

        """Test that the data attribute is updated after writing."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        manager.write('/test_group','new_dataset', data = [5,6,7])
        # Verify
        assert 'new_dataset' in manager.data['/test_group']
        assert np.array_equal(manager.data['/test_group']['new_dataset'], [5, 6, 7])

    def test_data_attribute_was_not_none_before_write(self, set_up_existing_file):

        """Test that the data attribute was not None before writing."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        # Verify
        assert manager.data is not None

    ## overwrite tests

    def test_overwrite_when_overwrite_false_raises_ValueError_and_logs_exception(self,caplog,set_up_existing_file):

        """Test that writing a dataset with the same name as an existing dataset 
        when overwrite is False raises ValueError and logs the exception."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        # Verify
        with pytest.raises(ValueError,match="Dataset name already exists in group."):
            manager.write('/test_group','test_dataset', data = [1,2,3])
        assert "Dataset name already exists in group." in caplog.text
        assert "ERROR" in caplog.text

    def test_overwrite_when_overwrite_true_overwrites_existing_dataset(self, set_up_existing_file):

        """Test that writing a dataset with the same name as an existing dataset 
        when overwrite is True overwrites the existing dataset."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        manager.write('/test_group','test_dataset', data = [5,6,7], overwrite = True)
        assert np.array_equal(manager.data['/test_group']['test_dataset'], [5, 6, 7])

    ## group path tests

    def test_invalid_group_path_name(self, set_up_existing_file, set_up_group_path_with_invalid_characters, set_up_empty_group_path, set_up_group_path_with_invalid_type,caplog):

        """Test that writing to a group path with invalid characters raises ValueError."""

        # Setup
        file_path = set_up_existing_file
        invalid_char_group_path = set_up_group_path_with_invalid_characters
        invalid_type_group_path = set_up_group_path_with_invalid_type
        empty_group_path = set_up_empty_group_path
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        # Verify
        with pytest.raises(ValueError,match="Group path contains invalid characters."):
            manager.write(invalid_char_group_path,'new_dataset', data = [5,6,7])
            assert "Invalid characters in group path." in caplog.text
        with pytest.raises(ValueError,match="Group path must be a string."):
            manager.write(invalid_type_group_path,'new_dataset', data = [5,6,7])
            assert "Invalid group path type." in caplog.text
        with pytest.raises(ValueError,match="Group path cannot be empty."):
            manager.write(empty_group_path,'new_dataset', data = [5,6,7])
            assert "Group path cannot be empty." in caplog.text
    
    def test_write_to_non_existent_group_path_new_group_false_raises_KeyError_and_logs_exception(self,caplog,set_up_existing_file,set_up_non_existent_group_path):

        """Test that writing to a non-existent group path when new_group is False 
        raises KeyError and logs the exception."""

        # Setup
        file_path = set_up_existing_file
        non_existent_group_path = set_up_non_existent_group_path
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        # Verify
        with pytest.raises(KeyError,match="Group path does not exist."):
            manager.write(non_existent_group_path,'new_dataset', data = [5,6,7])
        assert "Group path does not exist." in caplog.text
        assert "ERROR" in caplog.text

    def test_write_to_non_existent_group_path_new_group_true_creates_new_group(self, set_up_existing_file, set_up_non_existent_group_path):

        """Test that writing to a non-existent group path when new_group is True 
        creates a new group."""

        # Setup
        file_path = set_up_existing_file
        non_existent_group_path = set_up_non_existent_group_path
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        manager.write(non_existent_group_path,'new_dataset', data = [5,6,7], new_group = True)
        # Verify
        assert 'new_dataset' in manager.data['/non_existent_group_path']
        assert np.array_equal(manager.data['/non_existent_group_path']['new_dataset'], [5, 6, 7])

    ## dataset tests

    def test_invalid_dataset_name(self, set_up_existing_file, set_up_dataset_name_with_invalid_characters, set_up_empty_dataset_name, set_up_dataset_name_with_invalid_type,caplog):

        """ Test that writing to a dataset with invalid name raises ValueError"""
        
        # Setup
        file_path = set_up_existing_file
        invalid_char_dataset_name = set_up_dataset_name_with_invalid_characters
        invalid_type_dataset_name = set_up_dataset_name_with_invalid_type
        empty_dataset_name = set_up_empty_dataset_name
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        # Verify
        with pytest.raises(ValueError,match="Dataset name contains invalid characters."):
            manager.write('/test_group',invalid_char_dataset_name, data = [5,6,7])
            assert "Invalid characters in dataset name." in caplog.text
        with pytest.raises(ValueError,match="Dataset name must be a string."):
            manager.write('/test_group',invalid_type_dataset_name, data = [5,6,7])
            assert "Invalid dataset name type." in caplog.text
        with pytest.raises(ValueError,match="Dataset name cannot be empty."):
            manager.write('/test_group',empty_dataset_name, data = [5,6,7])
            assert "Dataset name cannot be empty." in caplog.text

    def test_write_an_empty_or_none_dataset_raises_ValueError_and_logs_exception(self,caplog,set_up_existing_file):

        """Test that writing an empty or None dataset raises ValueError and logs the exception."""

        # Setup
        file_path = set_up_existing_file
        empty_dataset = []
        none_dataset = None
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'w',read_only = False,archive_status = False)
        manager.read()
        # Verify
        with pytest.raises(ValueError,match="Dataset cannot be empty."):
            manager.write('/test_group','new_dataset', data = empty_dataset)
            assert "Dataset cannot be empty." in caplog.text
        with pytest.raises(ValueError,match="Dataset cannot be empty."):
            manager.write('/test_group','new_dataset', data = none_dataset)
            assert "Dataset cannot be empty." in caplog.text

    ## other tests

    def test_writing_with_insufficient_permissions_raises_PermissionError_and_logs_exception(self,caplog,set_up_existing_file):

        """Test that writing with insufficient permissions raises PermissionError and logs the exception."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = False,archive_status = False)
        # Verify
        with pytest.raises(PermissionError):
            manager.write('/test_group','new_dataset', data = [5,6,7])
        assert "Insufficient permissions." in caplog.text
        assert "ERROR" in caplog.text

    def test_write_to_non_readable_mode_raises_ValueError_and_logs_exception(self,caplog,set_up_existing_file):

        """Test that writing to a file with non-readable mode raises ValueError and logs the exception."""

        # Setup
        file_path = set_up_existing_file
        # Exercise
        manager = HDF5Manager(file_path = file_path,mode = 'r',read_only = True,archive_status = False)
        # Verify
        with pytest.raises(ValueError, match = 'File is not in append or write mode.'):
            manager.write('/test_group','new_dataset', data = [5,6,7])
        assert "File not writable." in caplog.text
        assert "ERROR" in caplog.text
    


        