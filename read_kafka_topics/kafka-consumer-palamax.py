#start-kafka-logger.sh
#flock -n logger.lock python3 kafka-consumer-palamax.py >> $(date +"%Y%m%dT%H%M%S")-kafka-messages.log &

#stop-kafka-logger.sh
#kill $(lslocks | grep logger.lock | awk '{print $2}')
#kill $(lsof | grep kafka-messages.log | awk '{print $1}')

#tail -f 20241017T100924-kafka-messages-T131959.log

from kafka import KafkaConsumer
import sys
host='localhost:9092' if len(sys.argv)<=1 else sys.argv[1]
print("host="+host)
consumer = KafkaConsumer(bootstrap_servers=host,group_id='kafka-logger',fetch_min_bytes=1,fetch_max_wait_ms=0,enable_auto_commit=True)
consumer.subscribe(['AuditLogEvent','DataProcessingRequest','MachineMetaData','OperatorLogEvent','StateChangedEvent','MachineEvent','RecipeChangedEvent','LotChangedEvent','ProductionResultEvent','ItemRegisterEvent','ItemTransferEvent','ItemParameterChangedEvent','UnitMetaData','EquipmentValueChangedEvent','TraceableProductionData','MeasurementMonitoringSubscription','MeasurementMonitoringUnsubscription','MachineMessageEvent','MachineMessageClearEvent','MachineMessageMappingsEvent','TraceableProductionMeasurement','MachineMessageData'])
#for msg in consumer:
#    print (msg)	
while True:
    raw_messages = consumer.poll(timeout_ms=1000) #, max_records=500
    for topic_partition, messages in raw_messages.items():
        for msg in messages:
            #application_message = json.loads(message.value.decode())
            print (msg)
