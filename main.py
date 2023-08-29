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
MC_SERVER_PORT = os.environ.get("MC_SERVER_PORT")

if TOKEN is None:
    print(".envファイルにTOKENを設定して下さい")
    sys.exit(1)


class MyClient(discord.Client):
    async def on_ready(self):
        if MC_SERVER_ADDRESS is None:
            print(".envファイルにMC_SERVER_ADDRESSを設定して下さい")
            sys.exit(1)
        print(f"Logged on as {self.user}")
        while True:
            if MC_SERVER_PORT is None:
                ping = PINGClient(MC_SERVER_ADDRESS)
            else:
                ping = PINGClient(MC_SERVER_ADDRESS, port=int(MC_SERVER_PORT))
            try:
                stats = ping.get_stats()
                numplayers = stats["players"]["online"]
                activity = discord.Game(f"{numplayers}人がMinecraft")
                status = discord.Status.online
            except:
                activity = discord.CustomActivity(name="サーバーはオフライン")
                status = discord.Status.idle
            await client.change_presence(status=status, activity=activity)
            await asyncio.sleep(1)


intents = discord.Intents.default()
intents.message_content = False

client = MyClient(intents=intents)
client.run(TOKEN)
