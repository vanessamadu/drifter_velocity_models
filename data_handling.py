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
