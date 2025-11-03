from kafka import KafkaConsumer
import sys
host='localhost:9092' if len(sys.argv)<=1 else sys.argv[1]
print("host="+host)
#consumer = KafkaConsumer(bootstrap_servers=host)
consumer = KafkaConsumer(bootstrap_servers=host, auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000, group_id='log-begining')
consumer.subscribe(['AuditLogEvent','DataProcessingRequest','MachineMetaData','OperatorLogEvent','StateChangedEvent','MachineEvent','RecipeChangedEvent','LotChangedEvent','ProductionResultEvent','ItemRegisterEvent','ItemTransferEvent','ItemParameterChangedEvent','UnitMetaData','EquipmentValueChangedEvent','TraceableProductionData','MeasurementMonitoringSubscription','MeasurementMonitoringUnsubscription','MachineMessageEvent','MachineMessageClearEvent','MachineMessageMappingsEvent','TraceableProductionMeasurement','MachineMessageData'])
#for msg in consumer:
#    print (msg)	
isNotEnd = True
while isNotEnd:
    raw_messages = consumer.poll(timeout_ms=20000, max_records=1000000)
    if len(raw_messages)==0: 
        isNotEnd=False
    for topic_partition, messages in raw_messages.items():
        for msg in messages:
            #application_message = json.loads(message.value.decode())
            print (msg)
