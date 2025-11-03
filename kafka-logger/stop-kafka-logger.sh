kill $(lslocks | grep logger.lock | awk '{print $2}')
kill $(lsof | grep kafka-messages.log | awk '{print $1}')
