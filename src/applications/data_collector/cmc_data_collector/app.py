import time
from .data_collector import CMCPostsDataCollector, CMCNewsDataCollector
from .constants import SYMBOL_LIST, CRAWL_INTERVAL


def main():
    post_data_collectors = []
    news_data_collectors = []
    for symbol in SYMBOL_LIST[:1]:
        post_data_collectors.append(CMCPostsDataCollector(symbol))
        news_data_collectors.append(CMCNewsDataCollector(symbol))

    try:
        while True:
            for data_collector in post_data_collectors:
                data_collector.start()
            for data_collector in news_data_collectors:
                data_collector.start()
            time.sleep(CRAWL_INTERVAL)
    except Exception as e:
        print(e)
    finally:
        for data_collector in post_data_collectors:
            data_collector.stop()


main()
