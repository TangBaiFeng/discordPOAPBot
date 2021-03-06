from dotenv import load_dotenv, find_dotenv
import discord
from discord.ext import tasks
import os
import logging
import requests

logging.basicConfig(level=logging.INFO)
load_dotenv(find_dotenv())
BOT_TOKEN = os.getenv('BOT_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(619359579058470923)  # channel ID goes here

        await channel.send(x.count)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient()
client.run(BOT_TOKEN)
