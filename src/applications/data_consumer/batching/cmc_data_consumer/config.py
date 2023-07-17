KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092",
    "group.id": "cmc_batch_data_consumer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
}

FE_KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092",
    "client.id": "cmc_batch_data_consumer"
}

HADOOP_URL = "http://localhost:9870"
HADOOP_USER = "root"
