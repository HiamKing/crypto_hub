import os

KAFKA_BOOTSTRAP_SERVERS = "localhost:19092,localhost:29092,localhost:39092"


SPARK_APP_NAME = "binance_data_streamer"
SPARK_MASTER = "local[*]"
SPARK_CONFIG = {
    "spark.jars.packages": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.mongodb.spark:mongo-spark-connector_2.12:10.2.0",
    "spark.mongodb.write.connection.uri": "mongodb://admin:admin@mongo:27017",
    "spark.mongodb.write.database": "crypto_hub",
    "spark.sql.caseSensitive": "true"
}

# Add Hadoop conf
os.environ['HADOOP_CONF_DIR'] = f"{os.path.dirname(os.path.realpath(__file__))}/../../../utils/hadoop_conf"
