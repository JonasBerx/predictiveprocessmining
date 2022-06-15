"""
This script contains all the preprocessing scripts for the Claims_Management_Simplified.csv file

The preprocessing steps go as follows:

  1. Calculate Activity Processing Time ->
      How long does it take to finish each activity in a process flow

  2. Calculate Total Process Time (Start) ->
      Cumulative sum of the durations of the activities,
        relative to the start_time of each activity.
      (Note: The last number of each process is the cumsum until
        the starttime of the last activity.)

  3. Calculate Total Process Time (End) ->
      Cumulative sum of the durations of the activities, relative to the end_time of each activity.
      (Note: This is the actual total cumulative time the process takes)

  4. Calculate Waiting Time Between Activities -> Obvious :)

  5. Calculate Case Variants ->
      Find out the different flows inside the dataset and assign a unique identifier to each flow,
      then assign that identifier to each case within that flow.
"""
import pandas as pd
import numpy as np
import hashlib

def custom_hash(obj):
    return int.from_bytes(hashlib.sha256(obj.encode('utf-8')).digest()[:4], 'little')


def write_to_csv():
    frame = transform_data()
    frame.to_csv('./data/results/data.csv', sep=',', encoding='utf-8')
    print(frame.dtypes)


def transform_data():
    # Only select columns we actually use here.
    columns = ["case_id", "start_time", "end_time", "Activity"]
    df = pd.read_csv('./data/conform_SLA.csv')[columns]
    # Convert start_time and end_time to datetime types
    df.start_time = pd.to_datetime(df.start_time)
    df.end_time = pd.to_datetime(df.end_time)
    # print(df)

    # startTime = time.time()
    df = calc_case_variants(df)
    # endTime = time.time()
    # print(str(endTime - startTime) + " sec")

    # startTime = time.time()
    df = calc_activity_process_time(df)
    # endTime = time.time()
    # print(str(endTime - startTime) + " sec")

    # startTime = time.time()
    df = df.groupby(df.case_id).apply(calc_total_process_time_start)
    # endTime = time.time()
    # print(str(endTime - startTime) + " sec")

    # startTime = time.time()
    df = df.groupby(df.case_id).apply(calc_total_process_time_end)
    # endTime = time.time()
    # print(str(endTime - startTime) + " sec")

    # startTime = time.time()
    df = df.groupby(df.case_id).apply(calc_waiting_time_between)
    # endTime = time.time()
    # print(str(endTime - startTime) + " sec")

    return df


def calc_activity_process_time(frame):
    """
      Takes a data frame with start_time and end_time column;
      Add new colum with processing time.
    """
    # 1. Calculate difference in date time of row
    diff = (frame.end_time - frame.start_time) / np.timedelta64(1, 'm')

    # 2. In case there is no time. set to 0
    diff[diff.isna()] = pd.Timedelta(0)

    # 3. Populate frame with new column
    frame['processing_time'] = diff

    return frame


def calc_total_process_time_start(frame):
    """
    Takes a data frame with a start_time column;
    Add new colum with cummulative sum for start_time for each case_id.
    """
    # 1. create the difference array from start_time
    r1 = frame.start_time.diff()

    # 2. fill the first value (NaT) with zero
    r1[r1.isna()] = pd.Timedelta(0)

    # 3. convert to seconds and use cumsum -> new column
    frame["relative_start_time"] = np.cumsum(r1.dt.total_seconds().values / 60)
    return frame


def calc_total_process_time_end(frame):
    """
    Takes a data frame with a relative_start_time and processing_time column;
    Add new colum with cummulative sum for relative_start_time + processing_time for each case_id.
    """
    # 1. calculate cumulative end_time based on processing time and relative start time.
    cprt = frame.relative_start_time + frame.processing_time
    # 2. Create new column with resulted values
    frame["relative_end_time"] = cprt

    return frame


def calc_waiting_time_between(frame):
    wtt = frame.relative_start_time - frame.relative_end_time.shift(1)

    wtt[wtt.isna()] = 0.0

    frame["waiting_time"] = wtt

    return frame


def calc_case_variants(frame):
    """
    This method takes a Pandas Dataframe and returns the same frame with a case variant identifier
        - Perform equivalent of GROUP_CONCAT to combine all the flows of each case
        - Remove duplicates and reindex
        - Collect all case_id's that follow the case_variant flow
        - Adding case_variant id to the original dataframe
    """
    # Case variant collection through hashing
    ddf = frame.groupby('case_id')['Activity'].transform(
        lambda x: custom_hash(",".join(list(x))))
    # ddf = frame.rename(columns={'Activity': 'a_list'})
    # ddf = frame.sort_values('a_list', ascending=False)
    frame['case_variant'] = ddf
    frame['case_variant'] = frame['case_variant'].astype('string')
    # LEAVE THIS CODE HERE JUST IN CASE

    # Case variant collection
    # ddf = frame.groupby('case_id')['Activity'].apply(
    #     lambda x: ",".join(list(x))).reset_index()
    # ddf = ddf.rename(columns={'Activity': 'a_list'})
    # ddf = ddf.groupby(ddf.a_list).agg(lambda col: col.tolist()).reset_index()
    # ddf['len'] = ddf.case_id.map(len)
    # ddf = ddf.sort_values('len', ascending=False)
    # ddf = ddf.reset_index()
    #
    # Add case variant index to original dataframe
    # frame['case_variant'] = -1
    #
    # for jndex, s in ddf.iterrows():
    #     frame.loc[frame.case_id.isin(s.case_id),
    #               'case_variant'] = ddf.loc[jndex].name

    return frame


write_to_csv()
