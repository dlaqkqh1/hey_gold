import redshift_connector
from discord_bot.config.environment import RedshiftConnect


class RedshiftSession:
    @classmethod
    def redshift_conn(cls):
        conn = redshift_connector.connect(
            host=RedshiftConnect.HOST,
            database=RedshiftConnect.DATABASE,
            user=RedshiftConnect.USERNAME,
            password=RedshiftConnect.PASSWORD,
            port=RedshiftConnect.PORT
        )

        return conn.cursor()


