# https://koalatea.io/python-redis-pubsub/
import argparse
import redis
import json
import io
import logging
import time

start_time = time.time()
duration = 10


def perform(bytes):
    message = json.load(io.BytesIO(bytes))

    sender = message['metadata']['from']
    receiver = message['metadata']['to']
    amount = message['amount']

    if not receiver in bad_guys and not sender in bad_guys:
        logging.info('Ignore message ' + str(message))
        return

    if amount >= 0 and receiver in bad_guys:
        message['metadata']['from'], message['metadata']['to'] = message['metadata']['to'], message['metadata']['from']
        logging.info('Swap message ' + str(message))

    logging.info('Bad guy ' + str(message))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='bad_guys', help='List of bad guys', type=str, required=True)
    args = parser.parse_args()
    bad_guys = args.bad_guys.split(',')

    redis = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = redis.pubsub()
    pubsub.subscribe('channel-1')

    while time.time() - start_time < duration:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            logger.info('Received message ' + str(message))
            perform(message['data'])
