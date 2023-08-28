from os.path import join, dirname
import os
import sys
import asyncio
import time

from dotenv import load_dotenv
import discord
from mctools import PINGClient


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
MC_SERVER_ADDRESS = os.environ.get("MC_SERVER_ADDRESS")

if TOKEN is None:
    print(".envファイルにTOKENを設定して下さい")
    sys.exit(1)
if MC_SERVER_ADDRESS is None:
    print(".envファイルにMC_SERVER_ADDRESSを設定して下さい")
    sys.exit(1)
    

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)


while True:
    ping = PINGClient(MC_SERVER_ADDRESS)
    try:
        stats = ping.get_stats()
        numplayers = stats["players"]["online"]
        game = discord.Game(f"{numplayers}人がオンライン")
        status = discord.Status.online
    except:
        game = discord.Game("サーバーはオフライン")
        status = discord.Status.idle
    asyncio.run(client.change_presence(status=status, activity=game))
    time.sleep(1)