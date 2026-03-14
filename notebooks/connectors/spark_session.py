from pyspark.sql import SparkSession


def get_spark_session():

    spark = (
        SparkSession.builder
        .appName("DeliveryLake")

        # JDBC + S3 + Delta dependencies
        .config(
            "spark.jars.packages",
            ",".join([
                "org.postgresql:postgresql:42.7.3",
                "org.apache.hadoop:hadoop-aws:3.3.4",
                "io.delta:delta-spark_2.12:3.1.0"
            ])
        )

        # Delta configs
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension"
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )

        # MinIO config
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark