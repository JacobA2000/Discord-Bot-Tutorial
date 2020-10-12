import discord
from discord.ext import commands

import json

with open("./config.json") as f:
    configData = json.load(f)

noPing = configData["noPing"]

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(word in message.content for word in noPing):
            await message.delete()
            await message.author.send("You cannot tag that user.")

    @commands.command()
    async def noping(self, ctx, member: discord.Member):
        noPing.append(member.mention)

        with open("./config.json", "r+") as f:
            data = json.load(f)
            data["noPing"] = noPing
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

        await ctx.send(f"{member.name} was added to the noping list.")

def setup(bot):
    bot.add_cog(Management(bot))