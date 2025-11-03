# OBD2_sensors.py: Write OBD2 sensor data. No need to edit.
import _setup
firehose, s3, records = _setup.ex_vars
for idx, row in records.iterrows(): 

    # Create a payload string that ends with a newline
    payload = ' '.join(str(value) for value in row) 
    payload = payload + "\n"

    # Send the payload string to Firehose stream
    res = firehose.put_record(
        DeliveryStreamName = 'gps-delivery-stream',
        Record = {'Data': payload})
