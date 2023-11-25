# Requirements

This set of packages has the following requirements:
- pandas
- h5py

## Data Manager Classes
### CSV Data Manager Class
`CSVManager`: A **class** for managing CSV files.
#### Class Attributes
- `file_path (str):` The path to the CSV file
- `delimiter (str):` The delimiter used in this CSV file
- `has_header (bool):` Flag indicating if the CSV file has a header row
- `column_names (list):` List of column names, populated from header row if `has_header` is True.
- `data (dataframe):` The data from the CSV file
- `read_only (bool):` Flag indicating if the CSV file is in read-only mode.
- `error_handling (str):` How the CSV class should handle errors ('raise', 'log', 'skip', etc...)
- `encoding (str):` The character encoding used in the CSV file
- `line_endings (str):` The line ending characters used in the CSV file.
- `metadata (dict):` Additional metadata about the CSV file.
- `datetime_format (str):` The format for date and time columns in the CSV file.
- `archive_status (bool):` Flag indicating if the data is archived