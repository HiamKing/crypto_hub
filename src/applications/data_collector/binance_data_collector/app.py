import time
from .data_collector import BinanceDataCollector
from .constants import SYMBOL_LIST, CRAWL_INTERVAL


def main():
    data_collectors = []
    for symbol in SYMBOL_LIST:
        data_collectors.append(BinanceDataCollector(symbol))

    try:
        while True:
            for data_collector in data_collectors:
                data_collector.start()
            time.sleep(CRAWL_INTERVAL)
    except Exception as e:
        print(e)
    finally:
        for data_collector in data_collectors:
            data_collector.stop()


main()
