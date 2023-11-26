# DATA HANDLING LIBRARIES
import pandas as pd ## CSV
import h5py         ## HDF5

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

    def read(self):
        '''
        Read data from HDF5 file into `data` attribute as an h5py.File object.

        Raises:
            FileNotFoundError: If file does not exist.
            IOError: If file is not readable.
            OSError: If file is not a valid HDF5 file. 
            ValueError: If file is not in read-only mode/file has already been read.
        '''
        # Check if file is in read-only mode or has already been read
        if self.data is not None:
            raise ValueError("File has already been read.") # raise new specific exception
        try:
            with h5py.File(self.file_path, mode=self.mode) as file:
                self.data = file
        except FileNotFoundError as fnfe:
            print("File not found.") # handle the exception that was raised
            raise fnfe               # re-raise last exception caught
        except IOError as ioe:
            print("File is not readable.")
            raise ioe
        except OSError as ose:
            print("File is not a valid HDF5 file.")
            raise ose

    def write(self):
        pass

    def get_dataset(name):
        pass

    def info():
        pass