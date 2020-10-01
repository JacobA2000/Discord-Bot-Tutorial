import discord
from discord.ext import commands

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
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(activity=discord.Game(name=f"{prefix} - prefix"))

@bot.command(description="Gets the bot's latency.")
async def ping(ctx):
    latency = round(bot.latency * 1000, 1)
    await ctx.send(f"Pong! {latency}ms")

@bot.command()
async def hi(ctx, member):
    await ctx.send(f"Hello! {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} was unbanned.")
            return

@bot.command()
@commands.has_permissions(administrator=True)
async def activity(ctx, *, activity):
    await bot.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f"Bot's activity changed to {activity}")

@bot.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx, commandSent=None):
    if commandSent != None:

        for command in bot.commands:
            if commandSent.lower() == command.name.lower():

                paramString = ""

                for param in command.clean_params:
                    paramString += param + ", "

                paramString = paramString[:-2]

                if len(command.clean_params) == 0:
                    paramString = "None"
                    
                embed=discord.Embed(title=f"HELP - {command.name}", description=command.description)
                embed.add_field(name="parameters", value=paramString)
                await ctx.message.delete()
                await ctx.author.send(embed=embed)
        
    else:
        embed=discord.Embed(title="HELP")
        embed.add_field(name="ping", value="Gets the bots latency", inline=True)
        embed.add_field(name="hi", value="Says hello to a specified user, Parameters: Member", inline=True)
        embed.add_field(name="userinfo", value="Retreives info about the user", inline=True)

        await ctx.message.delete()
        await ctx.author.send(embed=embed)

bot.run(token)