import discord
from discord.ext import commands
import firebase
import TOKEN

TOKEN = TOKEN.TOKEN
#urllib.parse.quote('zombieslaya3#1152')
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if not message.content.startswith('!'):
#         return
    
#     await message.channel.send('Hello!')

@client.command()
async def ping(ctx):
    await ctx.send(f'You are {ctx.author}')

@client.command()
async def register(ctx):
    await ctx.send(f'You are {ctx.author}')

@client.command()
async def stats(ctx):
    await ctx.send(f'You are {ctx.author}')

@client.command()
async def matches(ctx, num_matches=0):
    await ctx.send(f'You are {ctx.author}')

client.run(TOKEN)
