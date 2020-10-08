import discord
from discord.ext import commands, tasks

import json
import os

if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 

token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def loadcog(ctx, cog):
    bot.load_extension(f"cogs.{cog}")

@bot.command()
async def unloadcog(ctx, cog):
    bot.unload_extension(f"cogs.{cog}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)