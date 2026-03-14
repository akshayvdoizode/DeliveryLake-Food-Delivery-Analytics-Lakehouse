class MinIOConnector:

    def __init__(self, spark, bucket="deliverylake"):
        self.spark = spark
        self.bucket = bucket

    def path(self, layer, table):
        return f"s3a://{self.bucket}/{layer}/{table}"

    def write(self, df, layer, table, fmt="delta", mode="overwrite"):
        path = self.path(layer, table)

        (
            df.write
            .format(fmt)
            .mode(mode)
            .save(path)
        )

    def read(self, layer, table, fmt="delta"):
        path = self.path(layer, table)

        return (
            self.spark.read
            .format(fmt)
            .load(path)
        )