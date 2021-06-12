import discord
from discord.ext import commands
from firebase import FirestoreConnection
from warzone import WarzoneTracker

with open('discord_token.txt', 'r') as f:
    TOKEN = f.readline()
    print(TOKEN)

platforms = ['activision', 'battlenet', 'xbox', 'playstation']

ERROR_MESSAGE = 'Something went wrong, please try again later'

USAGE = f'''!register [username] [platform]
            Available platforms: {platforms}'''

#urllib.parse.quote('zombieslaya3#1152')
client = commands.Bot(command_prefix = '!', description='Command prefix is [!] use !help to see list of commands', help='Command prefix is [!] use !help to see list of commands')

db = FirestoreConnection()
wz = WarzoneTracker()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_command_error(ctx, error):
#     print(error)
#     # if isinstance(error, commands.MissingRequiredArgument):
#     await ctx.send('INVALID')
#     await ctx.send(USAGE)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if not message.content.startswith('!'):
#         return
    
#     await message.channel.send('Hello!')

@client.command()
async def kd(ctx):
    user = db.get_user(str(ctx.author))
    if user is None:
        await ctx.send('Must be registered! Canceling.')
    platform = user['default']
    username = user[platform]
    kd = wz.get_player_kd(username)
    await ctx.send(f'KD: [{kd}]')

@client.command()
async def stats(ctx):
    user = db.get_user(str(ctx.author))
    if user is None:
        await ctx.send('Must be registered! Canceling.')
    platform = user['default']
    username = user[platform]
    overview = wz.get_overview(username)
    await ctx.send(f'{overview}')

@client.command()
async def register(ctx, arg1, arg2):
    if arg2 not in platforms:
        await ctx.send(f'Invalid platform: [{arg2}], must register one of the following: {platforms}')
        return
    try:
        success = db.set_user(str(ctx.author), arg1, arg2, arg2)
    except Exception as e:
        await ctx.send(ERROR_MESSAGE)
        print(e)
    if success:
        await ctx.send(f'Succesfully registered platform: {arg2} username: {arg1} for {ctx.author}')
    else:
        await ctx.send(ERROR_MESSAGE)
    

@client.command()
async def test(ctx, arg):
    await ctx.send(f'You are {ctx.author}')
    print(type(arg))
    print(str(ctx.author))
    print(ctx.author.name)
    print(type(ctx.author))

@client.command()
async def matches(ctx, num_matches=0):
    await ctx.send(f'You are {ctx.author}')

client.run(TOKEN)
