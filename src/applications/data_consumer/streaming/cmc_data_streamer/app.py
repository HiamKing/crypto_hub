from .data_streamer import CMCDataStreamer


def main():
    data_collector = CMCDataStreamer()
    data_collector.start()


main()
