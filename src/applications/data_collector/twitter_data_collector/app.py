from .data_collector import TwitterDataCollector


def main():
    data_collector = TwitterDataCollector()
    data_collector.start()


main()
