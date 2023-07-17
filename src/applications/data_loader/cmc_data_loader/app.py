from .data_loader import CMCDataLoader


def main():
    data_collector = CMCDataLoader()
    data_collector.start()


main()
