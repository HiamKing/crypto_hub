import os

CONSUMER_KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092",
    "group.id": "binance_data_loader",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
}

SPARK_APP_NAME = "binance_data_loader"
SPARK_MASTER = "local[*]"
SPARK_CONFIG = {
    "spark.jars.packages": "org.apache.spark:spark-avro_2.12:3.4.1,org.mongodb.spark:mongo-spark-connector_2.12:10.2.0",
    "spark.mongodb.write.connection.uri": "mongodb://admin:admin@mongo:27017",
    "spark.mongodb.write.database": "crypto_hub",
}

# Add Hadoop conf
os.environ['HADOOP_CONF_DIR'] = f"{os.path.dirname(os.path.realpath(__file__))}/.." + '/hadoop_conf'
