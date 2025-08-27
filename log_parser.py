from io import StringIO
import logging
import pandas as pd

# can be set to INFO to see the completed tasks also
logging.basicConfig(level=logging.WARNING)

# time thresholds 
WARNING_TRESHOLD_MINUTES = 5
ERROR_TRESHOLD_MINUTES = 10
WARNING_TRESHOLD = WARNING_TRESHOLD_MINUTES * 60  # convert to seconds
ERROR_TRESHOLD = ERROR_TRESHOLD_MINUTES * 60  # convert to seconds

def parse_log_file(file_path):
    try:
        # read log file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # read file content into a pandas dataframe using StringIO to avooid creating a temporary file
        dataframe = pd.read_csv(StringIO(content), header=None, names=['time', 'description', 'type', 'pid'])
        
        # convert pid column to integer
        dataframe['pid'] = dataframe['pid'].astype(int)

        # convert time column to datetime object
        dataframe['time'] = pd.to_datetime(dataframe['time'], format='%H:%M:%S')

        return dataframe
    except FileNotFoundError:
        print(f"Log file not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None
def calc_job_durations(df):
    # group log entries by PID 
    grouped_jobs = df.groupby('pid')
    
    # store the results in a list of dicts
    jobs_summary = []
    
    for pid, group in grouped_jobs:

        #  remove spaces and use uppercase for 'type' column
        group = group.copy()
        group['type'] = group['type'].astype(str).str.strip().str.upper()

        # find 'START' and 'END' entries
        start_time_entry = group[group['type'] == 'START']
        end_time_entry = group[group['type'] == 'END']

        #  if job has both start and end times record it
        if not start_time_entry.empty and not end_time_entry.empty:

            # get start and end times using iloc for pandas dataframe
            start_time = start_time_entry['time'].iloc[0]
            end_time = end_time_entry['time'].iloc[0]
            description = start_time_entry['description'].iloc[0]
            
            # calculate time difference in seconds
            duration = (end_time - start_time).total_seconds()
            
            # append job summary to the list
            jobs_summary.append({
                'pid': pid,
                'description': description,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration
            })
    
    return pd.DataFrame(jobs_summary)

def generate_report(summary_df):

    # check if there are any completed jobs
    if summary_df.empty:
        print("No completed jobs found.")
        return
    # log the report
    logging.info("Job Report:")
    # iterate through each job and log its status based on duration
    for _, row in summary_df.iterrows():
        pid = row['pid']
        description = row['description']
        duration = row['duration']

        # log messages based on duration thresholds
        if duration > ERROR_TRESHOLD:
            logging.error(f"Job {pid} ({description}) took longer than 10 minutes ({duration:.0f} seconds)")
        elif duration > WARNING_TRESHOLD:
            logging.warning(f"Job {pid} ({description}) took longer than 5 minutes ({duration:.0f} seconds)")
        else:
            logging.info(f"Job {pid} ({description}) took {duration:.0f} seconds - OK")

def main():
    logging.info("Starting log parsing and report generation...")

    # specify log file path
    log_file_path = 'logs.log'
    logging.info(f"Parsing log file: {log_file_path}")
    
    # parse log file
    log_df = parse_log_file(log_file_path)
    if log_df is None:
        return
    
    # calculate job durations
    job_summary = calc_job_durations(log_df)

    # generate report
    generate_report(job_summary)    
    
    logging.info("Report generation completed.")

if __name__ == "__main__":
    main()