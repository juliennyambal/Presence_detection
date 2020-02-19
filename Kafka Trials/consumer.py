# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:24:12 2020

@author: julien.nyambal
"""

import pandas as pd
import json
import threading
import uuid

from pathlib import Path
from kafka import KafkaProducer, KafkaConsumer
from time import sleep


KAFKA_HOST = 'localhost:9092'
df_test = pd.read_csv('datatest.txt')
# In the real world, the messages would not come with the target/outcome of
# our actions. Here we will keep it and assume that at some point in the
# future we can collect the outcome and monitor how our algorithm is doing
# df_test.drop('income_bracket', axis=1, inplace=True)
df_test['json'] = df_test.apply(lambda x: x.to_json(), axis=1)
messages = df_test.json.tolist()


def start_producing():
	producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)
	for i in range(200):
		message_id = str(uuid.uuid4())
		message = {'request_id': message_id, 'data': json.loads(messages[i])}

		producer.send('app_messages', json.dumps(message).encode('utf-8'))
		producer.flush()

		print("\033[1;31;40m -- PRODUCER: Sent message with id {}".format(message_id))
		sleep(2)


def start_consuming():
	consumer = KafkaConsumer('occupancy', bootstrap_servers=KAFKA_HOST)
	print(consumer)
	for msg in consumer:
		message = json.loads(msg.value)
		if 'data' in message:
			request_id = message['request_id']
			print("\033[1;32;40m ** CONSUMER: Received prediction {} for request id {}".format(message['data'], request_id))


start_consuming()