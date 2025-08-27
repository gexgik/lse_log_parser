# Log Parser

This project provides a Python script to parse log files, calculate job durations, and generate reports based on configurable time thresholds.

## Features

- Parses log files with columns: time, description, type, and pid.
- Calculates the duration of jobs based on 'START' and 'END' log entries.
- Generates a report with warnings and errors if job durations exceed specified thresholds.
- Uses pandas for efficient data processing.

## Usage

1. **Prepare your log file**  
   Ensure your log file (`logs.log` by default) has entries in the following format (comma-separated):  
   ```
   HH:MM:SS,Description,Type,PID
   ```

2. **Run the script**  
   Execute the script using Python 3:
   ```sh
   python log_parser.py
   ```

3. **View the report**  
   The script will output warnings and errors to the console based on job durations.

## Configuration

- **Thresholds**  
  You can adjust the warning and error thresholds (in minutes) at the top of log_parser.py:
  ```python
  WARNING_TRESHOLD_MINUTES = 5
  ERROR_TRESHOLD_MINUTES = 10
  ```

- **Log Level**  
  Change the logging level to `INFO` to see all completed tasks:
  ```python
  logging.basicConfig(level=logging.INFO)
  ```

## Dependencies

- Python 3.x
- pandas

Install dependencies with:
```sh
pip install pandas
```

## Project Structure

- log_parser.py: Main script for parsing logs and generating reports.

## Example

Sample log file entry:
```
12:00:00,Job A,START,1001
12:07:00,Job A,END,1001
```

## License

MIT License
