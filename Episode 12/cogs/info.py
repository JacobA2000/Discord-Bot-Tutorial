import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Gets the bot's latency.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000, 1)
        await ctx.send(f"Pong! {latency}ms")

    @commands.command()
    async def userinfo(self, ctx):
        user = ctx.author

        embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="NAME", value=user.name, inline=True)
        embed.add_field(name="NICKNAME", value=user.nick, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="STATUS", value=user.status, inline=True)
        embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))