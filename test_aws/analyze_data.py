# analyze_data.py: Analyze written sensor data. EDIT HERE.
import _setup, _run_deps, pandas as pd
firehose, s3, records = _setup.ex_vars

# List the objects that have been written to the S3 bucket
objects = s3.____(Bucket='adelramezani-vehicle-data')['Contents']

# Create list for collecting dataframes from read files.
dfs = []

# For every object, load it from S3
for obj in objects:
    data_file = s3.____(Bucket='adelramezani-vehicle-data', ____=obj['Key'])

    # Load it into a dataframe, specifying a delimiter and column names
    dfs.append(pd.read_csv(data_file['Body'], 
                           delimiter = " ", 
                           names=["record_id", "timestamp", "vin", "lon", "lat", "speed"]))

# Concatenate the resulting dataframes.
data = pd.concat(dfs)
print(data.groupby(['vin'])['speed'].max())