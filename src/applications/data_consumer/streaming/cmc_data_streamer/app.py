from .data_streamer import CMCDataStreamer
from .config import SPARK_APP_NAME, SPARK_CONFIG, SPARK_MASTER


def main():
    data_collector = CMCDataStreamer(SPARK_APP_NAME, SPARK_MASTER, SPARK_CONFIG)
    data_collector.start()


main()
