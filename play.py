import json
import logging
import os

from kafka import KafkaConsumer

import k8scontroller

bootstrap_servers = os.environ.get('KAFKA_SERVERS', 'localhost:9092').split(',')
topic = os.environ.get('KAFKA_TOPIC', 'events')

TEST_TYPE = 'test'
EVENT_TYPE = 'event'
QUERIES_TYPE = 'queries'

UPDATE_ACTION = 'update'
IGNORE_ACTION = 'ignore'


def main():
    consumer = KafkaConsumer(topic, group_id='k8scontroller-eventpartser', bootstrap_servers=bootstrap_servers,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    for message in consumer:
        message = json.loads(message.value)
        type_ = message['type']
        action = message['action']
        data = json.load(message['data'])
        if action == UPDATE_ACTION and type_ == EVENT_TYPE:
            try:
                if data['tracking']:
                    k8scontroller.apply_deployment(data['code'], data['keywords'])
                    logging.info('Created event partser for event: %s' % data['code'])
            except KeyError:
                logging.info('Message received was not formatted correctly. Message:\n %s' % data)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    logging.info('Checking Kubernetes connection...')
    logging.info('Kubernetes current pods ips: %s' % k8scontroller.get_pod_ips())

    logging.info('Kafka servers: %s' % ','.join(bootstrap_servers))
    logging.info('Start tracking changes')
    # main()
