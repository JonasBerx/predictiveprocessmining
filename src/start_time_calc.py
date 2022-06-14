from estimate_start_times import *
from estimate_start_times.concurrency_oracle import HeuristicsConcurrencyOracle
from estimate_start_times.config import DEFAULT_CSV_IDS
from estimate_start_times.utils import read_csv_log

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
# Instantiate desired concurrency oracle
concurrency_oracle = HeuristicsConcurrencyOracle(event_log, configuration)
# concurrency_oracle = AlphaConcurrencyOracle(event_log, configuration)
# concurrency_oracle = NoConcurrencyOracle(event_log, configuration)
# Add enablement times to the event log
concurrency_oracle.add_enabled_times(event_log)
