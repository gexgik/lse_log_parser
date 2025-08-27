import unittest
import pandas as pd
from io import StringIO
from log_parser import parse_log_file, calc_job_durations

class TestLogParser(unittest.TestCase):
    def setUp(self):
        # sample log as a string
        self.sample_log = (
            "12:00:00,Job A,START,1001\n"
            "12:05:00,Job A,END,1001\n"
            "13:00:00,Job B,START,1002\n"
            "13:12:00,Job B,END,1002\n"
        )
        # load the log into a pandas DataFrame
        self.df = pd.read_csv(
            StringIO(self.sample_log),
            header=None,
            names=['time', 'description', 'type', 'pid']
        )
        # convert 'pid' to integer and 'time' to datetime for consistency with main code
        self.df['pid'] = self.df['pid'].astype(int)
        self.df['time'] = pd.to_datetime(self.df['time'], format='%H:%M:%S')

    def test_calc_job_durations(self):
        # test if calc_job_durations returns correct number of jobs and durations
        summary = calc_job_durations(self.df)
        self.assertEqual(len(summary), 2)  # assert two jobs
        self.assertIn('duration', summary.columns)  # 'duration' column should exist
        # check if durations are as expected (in seconds)
        self.assertAlmostEqual(summary.loc[summary['pid'] == 1001, 'duration'].values[0], 300)
        self.assertAlmostEqual(summary.loc[summary['pid'] == 1002, 'duration'].values[0], 720)

    def test_parse_log_file(self):
        # write the sample log to a temporary file
        with open('test_logs.log', 'w') as f:
            f.write(self.sample_log)
        # parse the file 
        df = parse_log_file('test_logs.log')
        self.assertIsNotNone(df)  # dataFrame should not be None
        self.assertEqual(len(df), 4)  # should have 4 rows
        self.assertListEqual(list(df.columns), ['time', 'description', 'type', 'pid'])  # correct columns

if __name__ == '__main__':
    unittest.main()
