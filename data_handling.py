# DATA HANDLING LIBRARIES
import pandas as pd ## CSV
import h5py         ## HDF5
# ERROR HANDLING LIBRARIES
import logging
import os
# DATA MANAGER CLASSES

class CSVManager:
    def __init__(self,file_path,delimiter,has_header,read_only,
                 error_handling,encoding,line_endings, datetime_format,
                 archive_status):
        self.file_path = file_path
        self.delimiter = delimiter
        self.has_header = has_header
        self.column_names = None
        self.data = None
        self.read_only = read_only
        self.error_handling = error_handling
        self.encoding = encoding
        self.line_endings = line_endings
        self.metadata = {}
        self.datetime_format = datetime_format
        self.archive_status = archive_status

    def read(self):
        pass

    def write(self):
        pass

    def row_filter(self):
        pass

    def col_filter(self):
        pass

    def aggregate(self):
        pass

    def validate(self):
        pass

    def info(self):
        pass

class HDF5Manager:
    def __init__(self,file_path,mode,read_only,archive_status):
        self.file_path = file_path
        self.mode = mode
        self.data = None
        self.read_only = read_only
        self.archive_status = archive_status

    # VALIDATION METHODS

    def __check_file_path(self):
        '''
        Checks if file path is valid.

        Raises:
            - ValueError: 
                - If file path is not a string.
                - If file path is empty.
                - If file path contains invalid characters.
            - FileNotFoundError: If file path does not exist.
        '''
        if not isinstance(self.file_path, str):
            logging.error("File path must be a string.")
            raise ValueError("File path must be a string.")
        if not self.file_path:
            logging.error("File path cannot be empty.")
            raise ValueError("File path cannot be empty.")
        invalid_chars = set('<>:\"/\\|?* ')
        if any(char in invalid_chars for char in self.file_path):
            logging.error("File path contains invalid characters.")
            raise ValueError("File path contains invalid characters.")
        if not os.path.exists(self.file_path):
            logging.error("File not found.")
            raise FileNotFoundError("File not found.")

    def __check_mode(self):
        '''
        Checks if mode is valid.

        Raises:
            - ValueError: If mode is not 'r', 'w', or 'a'.
        '''
        if self.mode not in ['r','w','a']:
            logging.error("Mode must be 'r', 'w', or 'a'.")
            raise ValueError("Mode must be 'r', 'w', or 'a'.")
    
    def __check_group_path(self,group_path):
        '''
        Checks if group path is valid.

        Parameters:
            - `group_path` (str): The group path to be checked.

        Raises:
            - ValueError: 
                - If group path is not a string.
                - If group path is empty.
                - If group path contains invalid characters.
        '''
        if not isinstance(group_path, str):
            logging.error("Group path must be a string.")
            raise ValueError("Group path must be a string.")
        if not group_path:
            logging.error("Group path cannot be empty.")
            raise ValueError("Group path cannot be empty.")
        invalid_chars = set('<>:\"\\|?* ')
        if any(char in invalid_chars for char in group_path):
            logging.error("Group path contains invalid characters.")
            raise ValueError("Group path contains invalid characters.")

    def __check_dataset_name(self,dataset_name):
        '''
        Checks if dataset name is valid.

        Parameters:
            - `dataset_name` (str): The dataset name to be checked.

        Raises:
            - ValueError: 
                - If dataset name is not a string.
                - If dataset name is empty.
                - If dataset name contains invalid characters.
        '''
        if not isinstance(dataset_name, str):
            logging.error("Dataset name must be a string.")
            raise ValueError("Dataset name must be a string.")
        if not dataset_name:
            logging.error("Dataset name cannot be empty.")
            raise ValueError("Dataset name cannot be empty.")
        invalid_chars = set('<>:\"/\\|?* ')
        if any(char in invalid_chars for char in dataset_name):
            logging.error("Dataset name contains invalid characters.")
            raise ValueError("Dataset name contains invalid characters.")
    
    ## init checks
    def __check_init(self):
        '''
        Checks if file path and mode are valid.

        Raises:
        See `__check_file_path` and `__check_mode` methods.
        '''
        self.__check_file_path(self.file_path)
        self.__check_mode(self.mode)

    # INSTANCE METHODS
    def read(self):
        '''
        Read data from HDF5 file into `data` attribute as an h5py.File object.

        Raises:
            FileNotFoundError: If file does not exist.
            OSError: If file is not readable.
            ValueError: If file has already been read.
        '''
        # Check if file is in read-only mode or has already been read
        if self.data is not None:
            logging.error("File has already been read.")
            raise ValueError("File has already been read.")
        try:
            with h5py.File(self.file_path, mode=self.mode) as file:
                self.data = file
        except FileNotFoundError as fnfe:
            logging.error("File not found.")
            raise fnfe              
        except OSError as ose:
            logging.error("File not readable.")
            raise ose
    def write(self):
        pass

    def get_dataset(name):
        pass

    def info():
        pass