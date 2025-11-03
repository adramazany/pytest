# _setup.py: Create clients, load data, etc. No need to edit.
import boto3, pandas as pd,os

# Load Data
data_url = "vehicles.csv"
records = pd.read_csv(data_url).head(100)

# Create firehose client
AWS_KEY_ID = os.environ['AWS_KEY_ID']
AWS_SECRET = os.environ['AWS_SECRET']
firehose = boto3.client('firehose', 
    aws_access_key_id=AWS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET, 
    region_name='eu-central-1')#, 
    #endpoint_url="http://localhost:4573")

# Create s3 client
s3 = boto3.client('s3', 
    aws_access_key_id=AWS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET, 
    region_name='eu-central-1'#, 
    #endpoint_url="http://localhost:4572")
    
    
# Prep variables for export
ex_vars = [firehose, s3, records]
