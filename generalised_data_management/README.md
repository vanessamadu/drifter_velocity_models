# Requirements

This set of packages has the following requirements:
- pandas
- h5py
- os
- logging
- pytest (for testing)
- numpy (for testing)

## Data Manager Classes
### CSV Data Manager Class
`CSVManager`: A **class** for managing CSV files.
#### Class Attributes
- `file_path` (str): The path to the CSV file
- `delimiter` (str): The delimiter used in this CSV file
- `has_header` (bool): Flag indicating if the CSV file has a header row
- `column_names` (list): List of column names, populated from header row if `has_header` is `True`.
- `data` (dataframe): The data from the CSV file
- `read_only` (bool): Flag indicating if the CSV file is in read-only mode.
- `error_handling` (str): How the CSV class should handle errors ('raise', 'log', 'skip', etc...)
- `encoding` (str): The character encoding used in the CSV file
- `line_endings` (str): The line ending characters used in the CSV file.
- `metadata` (dict): Additional metadata about the CSV file.
- `datetime_format` (str): The format for date and time columns in the CSV file.
- `archive_status` (bool): Flag indicating if the data is archived

#### Class Methods
- `read()`: Reads data from the CSV file into the `data` attribute. 
- `write()`: Writes data to the CSV file using the current state of the CSV object. 
- `row_filter()`: Filters rows based on specified conditions. 
- `col_filter()`: Filters columns to only those specified
- `aggregate()`: Aggregates data based on specified conditions. 
- `validate()`: Validates the data against user-defined validation rules.
- `info()`: Displays information (metadata) about the CSV file and its configuration.

#### Method Documentation
##### read()
`read(self)`: Reads data from the CSV file into the `data` attribute.
Raises: 
- `IOError`: If the file cannot be read.
- `ValueError`: If there are issues with the file structure/encoding error.

### HDF5 Data Manager Class

`HDF5Manager`: A **class** for managing Hierarchical Data Format Version 5 (HDF5)  files.

#### Class Attributes 
- `file_path` (str): The path to the HDF5 file
- `mode` (str): The mode in which the HDF5 file is opened ('r' for read, 'w' for write)
- `data` (h5py.File): The HDF5 file object.
- `read_only` (bool): Flag indicating if the HDF5 file is in read-only mode.
- `archive_status` (bool): Flag indicating if the data is archived

#### Class Methods
- `read()`: Reads data from the HDF5 file into the `data` attribute. 
- `write()`: Writes data to the HDF5 file using the current state of the HDF5 object. 
- `get_dataset(name)`: Retrieves a dataset from the HDF5 file.
- `info()`: Displays information (metadata) about the HDF5 file and its configuration.

#### Method Documentation
##### Validation Methods
###### __check_file_path()
`__check_file_path(self)`: Checks if file path is valid.
Raises:
- `ValueError`: 
    - If file path is not a string.
    - If file path is empty.
    - If file path contains invalid characters.
- `FileNotFoundError`: If file path does not exist.

###### __check_mode()
`__check_mode(self)`: Checks if mode is valid.
Raises:
 - `ValueError`: If mode is not 'r', 'w', or 'a'.

###### __check_group_path()
`__check_group_path(self,group_path)`: Checks if group path is valid.
Parameters:
    - `group_path` (str): The group path to be checked.

Raises:
- `ValueError`: 
    - If group path is not a string.
    - If group path is empty.
    - If group path contains invalid characters.

###### __check_dataset_name()
`__check_dataset_name(self,dataset_name)`: Checks if dataset name is valid.
Parameters:
    - `dataset_name` (str): The dataset name to be checked.

Raises:
- `ValueError`: 
    - If dataset name is not a string.
    - If dataset name is empty.
    - If dataset name contains invalid characters.

###### __check_init()
`__check_init(self)`: Checks if file path and mode are valid.

Raises:
See [`__check_file_path`](#__check_file_path) and [`__check_mode`](#__check_mode) methods.

    
##### Instance Methods
###### read()
`read(self)`:Reads `h5py.File` object into the `data` attribute. A object that is iterable similarly to a dictionary.
Raises:
- `FileNotFoundError`: If file does not exist.
- `OSError`: If file is not readable.
- `ValueError`: If file has already been read.

###### write()
`write(self, group_path, dataset_name, dataset)`: Writes new data sets to a specific group of an `h5py.File` object in the `data` attribute.
Parameters:
- `dataset_name` (str): The name of the new dataset
- `dataset` (any type): The new dataset
- `group_path` (str): Path to the new dataset destination.
- `overwrite` (bool): If `True`, overwrite existing dataset with the same name. Default is `False`.
                If `False` and dataset name already exists, raise `ValueError`.
- `new_group` (bool): If True, create a new subgroup if the group path does not exist. Default is       `False`. If `False` and group path does not exist, raise `KeyError`.
Raises:
- `ValueError`:
    - If `self.mode` is not 'a' or 'w'.
    - If the `self.data` is empty.
    - If the dataset name already exists in the group.
    - If `dataset_name` is not a valid dataset name.
    - If `dataset` is empty or `None`.
    - If `group_path` is not a valid group path.
- `KeyError`: If `group_path` does not exist.
- `PermissionError`: If file is in read-only mode.

## Testing
The methods in Data Manager class have (successfully) undergone tests given in `test_data_handling.py` PyTest test suite to verify that they behave as expected under the following circumstances:
### read() Method
- `data` attribute is populated after `read()`.
- `data` attribute was empty before `read()`.
- `data` attribute is populated with an `h5py.File` object after `read()`.
- attempting to read a non-existent file will raise a `FileNotFoundError` and logs an exception as an "ERROR" with the message "File not found."
- attempting to read a non-HDF5 file will raise a `OSError` and logs an exception as an "ERROR" with the message "File not readable."
- attempting to read a file if the `data` attribute has already been populated raises a `ValueError` and logs an exception as an "ERROR" with the message "File has already been read."

