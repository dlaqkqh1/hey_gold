import os
import discord
from discord_bot.config.environment import DiscordBotConnect
from discord_bot.util.spark_util import SparkDataLoader
from datetime import datetime
from pyspark.sql import SparkSession
import pandas as pd

TOKEN = DiscordBotConnect.TOKEN
CHANNEL_ID = DiscordBotConnect.CHANNEL_ID

spark = SparkSession \
    .builder \
    .appName("hey gold bot") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()


spark_loader = SparkDataLoader()
gold_data = spark_loader.load_data('dlaqkqh1.gold_prices', spark)
gold_data.createOrReplaceTempView("gold_data")


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
        d = spark.sql("""SELECT left(date, 4) AS year, MAX(usd_pm) as max_price($)
                         FROM gold_data 
                         GROUP BY LEFT(date, 4)
                         ORDER BY 1 DESC""")
        pandas_d = d.toPandas()
        output = pandas_d.to_string(index=False)
        return output

    def get_answer(self, text):
        trim_text = text.replace(" ", "")

        answer_dict = {
            '안녕': '안녕하세요. 헤이골드입니다.',
            '연별': f'연도별 최대 금값 입니다. \n ```{self.get_max_gold_price()}```'
        }

        if trim_text == '' or None:
            return "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."
        elif trim_text in answer_dict.keys():
            return answer_dict[trim_text]
        else:
            for key in answer_dict.keys():
                if key.find(trim_text) != -1:
                    return "연관 단어 [" + key + "]에 대한 답변입니다.\n" + answer_dict[key]

            for key in answer_dict.keys():
                if answer_dict[key].find(text[1:]) != -1:
                    return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n" + answer_dict[key]

        return text + "은(는) 없는 질문입니다."


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
