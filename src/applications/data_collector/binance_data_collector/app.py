from .data_collector import BinanceDataCollector


def main():
    data_collector = BinanceDataCollector()
    data_collector.start()


main()
