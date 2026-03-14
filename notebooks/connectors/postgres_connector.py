JDBC_URL = "jdbc:postgresql://postgres:5432/food_delivery"

DB_PROPS = {
    "user": "retail_user",
    "password": "retail_pass",
    "driver": "org.postgresql.Driver"
}

class PostgresConnector:
    def __init__(self, spark, host="postgres", port=5432, db="food_delivery",
                 user="retail_user", password="retail_pass"):
        self.spark = spark
        self.jdbc_url = f"jdbc:postgresql://{host}:{port}/{db}"

        self.properties = {
            "user": user,
            "password": password,
            "driver": "org.postgresql.Driver"
        }
    def read_table(self, table):
        return (
            self.spark.read
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("dbtable", table)
            .options(**self.properties)
            .load()
        )

    def read_query(self, query):
        print("query", query)
        return (
            self.spark.read
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("query", query)
            .options(**self.properties)
            .load()
        )

    def read_parallel(self, table, partition_column, lower, upper, num_partitions=8):
        return (
            self.spark.read
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("dbtable", table)
            .option("partitionColumn", partition_column)
            .option("lowerBound", lower)
            .option("upperBound", upper)
            .option("numPartitions", num_partitions)
            .options(**self.properties)
            .load()
        )

    def write_table(self, df, table, mode="append"):
        (
            df.write
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("dbtable", table)
            .options(**self.properties)
            .mode(mode)
            .save()
        )