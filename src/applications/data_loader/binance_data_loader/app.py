from .data_loader import BinanceDataLoader


def main():
    data_collector = BinanceDataLoader()
    data_collector.start()


main()
