import os
from dotenv import load_dotenv

load_dotenv()


class RedshiftConnect:
    # Redshift 접속 정보
    HOST = os.getenv('REDSHIFT_HOST', '')
    USERNAME = os.getenv('REDSHIFT_USERNAME', '')
    PASSWORD = os.getenv('REDSHIFT_PASSWORD', '')
    DATABASE = os.getenv('REDSHIFT_DATABASE', '')
    PORT = os.getenv('REDSHIFT_PORT', '')


class DiscordBotConnect:
    # Discord Bot 접속 정보
    TOKEN = os.getenv('DISCORD_CHAT_BOT_TOKEN')
    CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')


class AWSS3Connect:
    # Discord Bot 접속 정보
    ACCESS_ID = os.getenv('AWS_S3_ACCESS_ID')
    ACCESS_KEY = os.getenv('AWS_S3_ACCESS_KEY')
    REGION = os.getenv('AWS_REGION')
    PATH = os.getenv('LOCAL_S3_DATA_FOLDER_PATH')