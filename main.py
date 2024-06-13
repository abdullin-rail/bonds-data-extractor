"""
Bonds data analyzer
"""
from message_broker.producer import RabbitMQProducer
from services.moex import MoexService
from variables import RABBITMQ_QUEUE_NAME


def extract_data_and_publish():
    service = MoexService()

    boards = service.get_boards()
    assert len(boards) > 0

    all_bonds = []
    for board in boards:
        bonds = service.get_bonds(board_id=board)
        all_bonds.append(bonds)

    with RabbitMQProducer(queue_name=RABBITMQ_QUEUE_NAME) as producer:
        producer.send_message(all_bonds)


if __name__ == "__main__":
    extract_data_and_publish()