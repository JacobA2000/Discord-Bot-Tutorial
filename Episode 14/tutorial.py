import discord
from discord.ext import commands, tasks

import json
import os
import re

if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "!", "noPing": [], "bannedWords": []}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 

token = configData["Token"]
prefix = configData["Prefix"]
bannedWords = configData["bannedWords"]

bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def loadcog(ctx, cog):
    bot.load_extension(f"cogs.{cog}")

@bot.command()
async def unloadcog(ctx, cog):
    bot.unload_extension(f"cogs.{cog}")

@bot.command()
@commands.has_permissions(administrator=True)
async def addbannedword(ctx, word):
    if word.lower() in bannedWords:
        await ctx.send("Already banned")
    else:
        bannedWords.append(word.lower())

        with open("./config.json", "r+") as f:
            data = json.load(f)
            data["bannedWords"] = bannedWords
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

        await ctx.message.delete()
        await ctx.send("Word added to banned words.")

@bot.command()
@commands.has_permissions(administrator=True)
async def removebannedword(ctx, word):
    if word.lower() in bannedWords:
        bannedWords.remove(word.lower())

        with open("./config.json", "r+") as f:
            data = json.load(f)
            data["bannedWords"] = bannedWords
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

        await ctx.message.delete()
        await ctx.send("Word remove from banned words.")
    else:
        await ctx.send("Word isn't banned.")

def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None

@bot.event
async def on_message(message):
    messageAuthor = message.author

    if bannedWords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedWord in bannedWords:
            if msg_contains_word(message.content.lower(), bannedWord):
                await message.delete()
                await message.channel.send(f"{messageAuthor.mention} your message was removed as it contained a banned word.")

    await bot.process_commands(message)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)