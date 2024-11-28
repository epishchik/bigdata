from onetl.connection import SparkHDFS
from onetl.file import FileDFReader
from onetl.file.format import CSV
from prefect import flow, task
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import IntegerType


@task(name="Create Spark Session")
def create_spark_session(app_name: str = "spark-with-yarn") -> SparkSession:
    spark = (
        SparkSession.builder.master("yarn")
        .appName(app_name)
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
        .enableHiveSupport()
        .getOrCreate()
    )

    return spark


@task(name="Create HDFS Connection")
def create_hdfs_connection(
    spark: SparkSession,
    host: str = "team-30-nn",
    port: int = 9000,
    cluster: str = "test",
) -> SparkHDFS:
    hdfs = SparkHDFS(host=host, port=port, spark=spark, cluster=cluster)

    if not hdfs.check():
        raise ConnectionError("HDFS connection failed")

    return hdfs


@task(name="Read CSV from HDFS")
def read_csv_from_hdfs(
    hdfs: SparkHDFS,
    source_path: str = "/tmp",
    files: list[str] = ["california_housing.csv"],
) -> DataFrame:
    reader = FileDFReader(
        connection=hdfs, format=CSV(delimiter=",", header=True), source_path=source_path
    )

    df = reader.run(files)
    return df


@task(name="Transform Data Types")
def transform_columns_to_integer(df: DataFrame) -> DataFrame:
    integer_columns = ["MedHouseValue", "MedInc", "HouseAge", "AveRooms", "Population"]

    for col in integer_columns:
        df = df.withColumn(f"{col}Int", df[col].cast(IntegerType()))

    return df


@task(name="Repartition Data")
def repartition_data(
    df: DataFrame, num_partitions: int = 90, partition_column: str = "MedHouseValue"
) -> DataFrame:
    return df.repartition(num_partitions, partition_column)


@task(name="Write Parquet Data")
def write_parquet(df: DataFrame, output_path: str = "/tmp/california_housing_prefect"):
    df.write.parquet(output_path)


@task(name="Save as Hive Table")
def save_as_hive_table(
    df: DataFrame,
    table_name: str = "california_housing_prefect_table",
    partition_column: str = "MedHouseValue",
):
    df.write.saveAsTable(table_name, partitionBy=partition_column)


@flow(name="California Housing Data Processing")
def california_housing_flow():
    spark = create_spark_session()
    hdfs = create_hdfs_connection(spark)

    df = read_csv_from_hdfs(hdfs)
    df = transform_columns_to_integer(df)
    df = repartition_data(df)

    write_parquet(df)
    save_as_hive_table(df)


if __name__ == "__main__":
    california_housing_flow()
