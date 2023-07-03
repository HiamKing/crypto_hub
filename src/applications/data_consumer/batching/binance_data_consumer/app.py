from .data_consumer import BinanceDataConsumer


def main():
    data_collector = BinanceDataConsumer()
    data_collector.start()


main()
