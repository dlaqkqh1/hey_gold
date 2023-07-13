import discord
from discord_bot.config.environment import DiscordBotConnect
from discord_bot.util.spark_util import SparkDataLoader
from pyspark.sql import SparkSession
from discord_bot.util import kafka_util as ku



TOKEN = DiscordBotConnect.TOKEN
CHANNEL_ID = DiscordBotConnect.CHANNEL_ID

spark = SparkSession \
    .builder \
    .appName("hey gold bot") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .master("local[*]") \
    .getOrCreate()


spark_loader = SparkDataLoader()
gold_data = spark_loader.load_data('dlaqkqh1.gold_prices', spark)
gold_data.createOrReplaceTempView("gold_data")

silver_data = spark_loader.load_data('dlaqkqh1.silver_prices', spark)
silver_data.createOrReplaceTempView("silver_data")

ku.create_topic("localhost:9092", 'hey_kafka', 4)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong {0.author.mention}'.format(message))
        else:
            answer = self.get_answer(message.content)
            await message.channel.send(answer)

    def get_max_gold_price(self):
        d = spark.sql("""SELECT left(date, 4) AS year, MAX(usd_pm) as max_price
                         FROM gold_data 
                         GROUP BY LEFT(date, 4)
                         ORDER BY 1 DESC""")
        pandas_d = d.toPandas()
        output = pandas_d.to_string(index=False)
        return output

    def get_max_silver_price(self):
        d = spark.sql("""SELECT left(date, 4) AS year, MAX(usd) as max_price
                         FROM silver_data 
                         GROUP BY LEFT(date, 4)
                         ORDER BY 1 DESC""")
        pandas_d = d.toPandas()
        output = pandas_d.to_string(index=False)
        return output

    def put_data_to_topic(self, text):
        print(text)
        ku.send_data_to_topic("localhost:9092", 'hey_kafka', text)
        return text + " 전송"

    def put_data_to_s3(self):
        ku.upload_data_to_s3()
        return"s3에 데이터 전송"

    def get_answer(self, text):
        try:
            command, option = text.split(' ', 1)
        except:
            return "알 수 없는 명령입니다."

        hi_answer_dict = {
            '안녕': '안녕하세요. 헤이골드입니다.'
        }

        gold_answer_dict = {
            '연도별최대': f'연도별 최대 금값 입니다. \n ```{self.get_max_gold_price()}```'
        }

        silver_answer_dict = {
            '연도별최대': f'연도별 최대 은값 입니다. \n ```{self.get_max_silver_price()}```'
        }

        kafka_answer_dict = {
            'answer': self.put_data_to_topic,
            's3': self.put_data_to_s3
        }

        if command == '안녕':
            if option not in hi_answer_dict.keys():
                return f"{option}은 알 수 없는 명령입니다."
            return hi_answer_dict[option]

        elif command == '헤이골드':
            if option not in gold_answer_dict.keys():
                return f"{option}은 알 수 없는 명령입니다."
            return gold_answer_dict[option]

        elif command == '헤이실버':
            if option not in silver_answer_dict.keys():
                return f"{option}은 알 수 없는 명령입니다."
            return silver_answer_dict[option]

        elif command == '헤이카프카':
            if option == 's3':
                return kafka_answer_dict['s3']()
            return kafka_answer_dict['answer'](option)

        return command + "은(는) 없는 명령입니다."


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
