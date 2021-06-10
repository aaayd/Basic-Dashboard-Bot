#!/usr/bin/env python
import subprocess
from discord.ext import commands, ipc
from discord import Intents
from discord.flags import Intents

class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        
        self.ipc = ipc.Server(self,secret_key = "ipcSecret123")

        self.COGS = {
            "cogs" : [
                "ipc_routes"
            ],
        }

    async def on_ready(self):
        print(f"Bot is ready")
        
    async def on_ipc_ready(self):
        process = subprocess.Popen(f'python website.py')
        print(f"IPC Server is ready")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)


bot = Bot(command_prefix = '?', intents = Intents.all())
TOKEN = "TOKEN"

for key, cogs in bot.COGS.items():
    for cog in cogs:

        string = f'Bot.{key}.{cog}'

        bot.load_extension(string)

if __name__ == "__main__":
    bot.ipc.start()
    bot.run(TOKEN)