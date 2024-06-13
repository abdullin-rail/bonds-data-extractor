import json
from decimal import Decimal

from pika import BlockingConnection, ConnectionParameters

from utils.json_encoder import DecimalEncoder
from variables import RABBITMQ_HOST, RABBITMQ_PORT


class RabbitMQProducer:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name

    def __enter__(self):
        self.connection = BlockingConnection(ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def send_message(self, data):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(data, cls=DecimalEncoder)
        )

