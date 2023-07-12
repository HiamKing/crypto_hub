from .data_consumer import CMCDataConsumer


def main():
    data_collector = CMCDataConsumer()
    data_collector.start()


main()
