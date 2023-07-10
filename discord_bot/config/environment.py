import os


class RedshiftConnect:
    # Redshift 접속 정보
    HOST = os.getenv('REDSHIFT_HOST')
    USERNAME = os.getenv('REDSHIFT_USERNAME')
    PASSWORD = os.getenv('REDSHIFT_PASSWORD')
    DATABASE = os.getenv('REDSHIFT_DATABASE')
    PORT = os.getenv('REDSHIFT_PORT')


class DiscordBotConnect:
    # Discord Bot 접속 정보
    TOKEN = os.getenv('DISCORD_CHAT_BOT_TOKEN')
    CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
