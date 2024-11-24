from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType

from onetl.file.format import CSV
from onetl.file import FileDFReader
from onetl.connection import SparkHDFS

# create spark session with yarn as execution engine
spark = SparkSession.builder \
   .master("yarn") \
   .appName("spark-with-yarn") \
   .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
   .enableHiveSupport() \
   .getOrCreate()

# create connection hdfs
hdfs = SparkHDFS(host="team-30-nn", port=9000, spark=spark, cluster="test")

# check connection status
print(hdfs.check())

# create file reader
reader = FileDFReader(connection=hdfs, format=CSV(delimiter=",", header=True), source_path="/tmp")

# run reader to get the file
df = reader.run(["california_housing.csv"])

print(df.head())

# get current number of partitions
print(f"Current number of partitions: {df.rdd.getNumPartitions()}")

# do data transformations, we will convert columns to integer type

df = df.withColumn("MedHouseValueInt", df["MedHouseValue"].cast(IntegerType()))
df = df.withColumn("MedIncInt", df["MedInc"].cast(IntegerType()))
df = df.withColumn("HouseAgeInt", df["HouseAge"].cast(IntegerType()))
df = df.withColumn("AveRoomsInt", df["AveRooms"].cast(IntegerType()))
df = df.withColumn("PopulationInt", df["Population"].cast(IntegerType()))

print(f"df after integer transformation:\n{df.head()}")

# repartition data
df = df.repartition(90, "MedHouseValue")

print(f"Num partitions after repartition: {df.rdd.getNumPartitions()}")

# save paritioned data as parquet
df.write.parquet("/tmp/california_housing")

# save table
df.write.saveAsTable("california_housing_table", partitionBy="MedHouseValue")