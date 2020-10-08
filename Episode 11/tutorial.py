import discord
from discord.ext import commands, tasks
import re

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

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@bot.command(description="repeats the specified message every specified seconds")
async def repeatmessage(ctx, enabled="start", interval=10, message=""):
    if enabled.lower() == "stop":
        messageInterval.cancel()
    elif enabled.lower() == "start":
        messageInterval.change_interval(seconds=int(interval))
        messageInterval.start(ctx, message)

@tasks.loop(seconds=10)
async def messageInterval(ctx, message):
    await ctx.send(message)

bot.run(token)