from discord_bot.config.environment import RedshiftConnect
from pyspark.sql import SparkSession


class SparkDataLoader:
    def __init__(self):
        host = RedshiftConnect.HOST
        database = RedshiftConnect.DATABASE
        user = RedshiftConnect.USERNAME
        password = RedshiftConnect.PASSWORD
        port = RedshiftConnect.PORT
        self.url = f"jdbc:redshift://{host}:{port}/{database}?user={user}&password={password}"

    def load_data(self, table, spark: SparkSession):
        redshift_data = spark.read \
            .format("jdbc") \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .option("url", self.url) \
            .option("dbtable", table) \
            .load()

        return redshift_data
