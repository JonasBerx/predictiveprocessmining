from estimate_start_times import *
from estimate_start_times.concurrency_oracle import HeuristicsConcurrencyOracle
from estimate_start_times.config import DEFAULT_CSV_IDS
from estimate_start_times.estimator import StartTimeEstimator
from estimate_start_times.utils import read_csv_log, write_csv_log
import pandas as pd
import time

configuration = config.Configuration(
    log_ids=DEFAULT_CSV_IDS,  # Custom the column IDs with this parameter
    consider_start_times=True  # Consider real parallelism if the start times are available
)
# Read event log
event_log = read_csv_log(
    log_path="data/Claims_Management_Simplified.csv",
    config=configuration,
    sort_by_end_time=True  # Sort log by end time (warning this might alter the order of the events sharing end time)
)

# TODO Got to play around a little - some results give me 1667 as a year??

def run_estimation(event_log_path, configuration, output_log_path):
    print("\nProcessing event log {}".format(event_log_path))
    # Read event log
    event_log = read_csv_log(event_log_path, configuration)
    # Instantiate desired concurrency oracle
    concurrency_oracle = HeuristicsConcurrencyOracle(event_log, configuration)
    # concurrency_oracle = AlphaConcurrencyOracle(event_log, configuration)
    # concurrency_oracle = NoConcurrencyOracle(event_log, configuration)
    # Add enablement times to the event log
    concurrency_oracle.add_enabled_times(event_log)
    # Export
    write_csv_log(event_log, output_log_path)


def timestamp_to_string(dates: pd.Series) -> pd.Series:
    return (dates.apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S.%f')).apply(lambda x: x[:-3]) +
            dates.apply(lambda x: x.strftime("%z")).apply(lambda x: x[:-2]) +
            ":" +
            dates.apply(lambda x: x.strftime("%z")).apply(lambda x: x[-2:]))


run_estimation("data/Claims_Management_Simplified.csv", configuration,
               "data/results/Claims_Management_Simplified.csv")
