import discord
from discord.ext import commands

import json
import os

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot is ready.")
 
bot.run("token")