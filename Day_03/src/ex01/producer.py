import redis
import json
import random
import string
import logging

def generate_random_number():
    random_digits = ''.join(random.choices(string.digits, k=10))
    return random_digits


def generate_message(sender, receiver, amount):
    # message = {
    #     'from': generate_random_number(),
    #     'to': generate_random_number(),
    #     'amount': generate_random_number(),
    # }
    message = {
        'metadata': {
            'from': sender,
            'to': receiver
        },
        'amount': amount,
    }
    return message


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    redis = redis.Redis(host='localhost', port=6379, db=0)

    # for i in range(5):
    #     message=generate_message()
    # redis.publish('pubsub',json.dumps(message))
    message = generate_message('1111111111', '4815162342', 100)
    redis.publish('channel-1', json.dumps(message))
    logger.info('Send message ' + str(message))

    message = generate_message('3333333333', '4444444444', 200)
    redis.publish('channel-1', json.dumps(message))
    logger.info('Send message ' + str(message))

    message = generate_message('4815162342', '3133780085', 300)
    redis.publish('channel-1', json.dumps(message))
    logger.info('Send message ' + str(message))

    message = generate_message('4815162342', '3133780085', 400)
    redis.publish('channel-1', json.dumps(message))
    logger.info('Send message ' + str(message))

    message = generate_message('4815162342', '3133780085', -500)
    redis.publish('channel-1', json.dumps(message))
    logger.info('Send message ' + str(message))
