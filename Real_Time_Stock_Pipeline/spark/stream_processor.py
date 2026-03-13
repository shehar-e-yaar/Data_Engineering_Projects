from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StringType, DoubleType, LongType

schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType()) \
    .add("volume", LongType()) \
    .add("timestamp", StringType())

spark = SparkSession.builder \
    .appName("StockMarketStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "stock_prices") \
    .option("startingOffsets", "earliest") \
    .load()

json_df = raw_df.selectExpr("CAST(value AS STRING) as json_value")

parsed_df = json_df.select(
    from_json(col("json_value"), schema).alias("data")
).select(
    col("data.symbol").alias("symbol"),
    col("data.price").alias("price"),
    col("data.volume").alias("volume"),
    to_timestamp(col("data.timestamp")).alias("event_time")
)

def write_to_postgres(batch_df, batch_id):
    print(f"=== Batch {batch_id} ===")
    count = batch_df.count()
    print(f"Rows in batch: {count}")

    if count == 0:
        return

    batch_df.show(truncate=False)

    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/stock_db") \
        .option("dbtable", "stock_prices") \
        .option("user", "stock_user") \
        .option("password", "stock_pass") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    print("Batch written successfully.")

query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()