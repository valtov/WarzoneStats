import discord
from discord import colour
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

DIAMOND = 'https://cdn.discordapp.com/attachments/729088904916893729/829627088867819520/diamond_pepe.jpg'
GOLD = 'https://cdn.discordapp.com/attachments/729088904916893729/829627115121016862/gold_pepe.jpg'
SILVER = 'https://cdn.discordapp.com/attachments/729088904916893729/829627198788468766/silver_pepe.jpg'
BRONZE = 'https://cdn.discordapp.com/attachments/729088904916893729/829627057137909760/bronze_pepe.png'


ranks = [
    {'kd': 2.08, 'rank': 'master', 'image': DIAMOND},
    {'kd': 1.14, 'rank': 'diamond', 'image': DIAMOND},
    {'kd': .92, 'rank': 'platinum', 'image': GOLD},
    {'kd': .73, 'rank': 'gold', 'image': GOLD},
    {'kd': .53, 'rank': 'silver', 'image': SILVER},
    {'kd': 0, 'rank': 'bronze', 'image': BRONZE},
    ]

# ranks = {
#     'master': (2.08, DIAMOND),
#     'diamond': (1.14, DIAMOND),
#     'platinum': (.92, GOLD),
#     'gold': (.73, GOLD),
#     'silver': (.53, SILVER),
#     'bronze': (0, BRONZE)
# }

# urllib.parse.quote('zombieslaya3#1152')
# zombieslaya3%231152
client = commands.Bot(
    command_prefix='!', description='Command prefix is [!] use !help to see list of commands', help='Command prefix is [!] use !help to see list of commands')



db = FirestoreConnection()
wz = WarzoneTracker()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !help command"))


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
async def stats(ctx, gamemode=0):
    mode = {0:'Lifetime', 1:'Battle Royal', 2:'Plunder'}
    if gamemode not in [0,1,2]:
        await ctx.send('Invalid gamemode! Must be either 0, 1 or 2 where 0=lifetime, 1=battle royale only, 2=plunder only. Canceling.')
        return
    discord_name = str(ctx.author)
    user = db.get_user(discord_name)
    if user is None:
        await ctx.send('Must be registered! Canceling.')
        return
    platform = user['default']
    username = user[platform]
    overview = db.get_overview(discord_name)
    if overview is None:
        overview = wz.get_overview(username)
        db.set_overview(discord_name, overview)

    embed = discord.Embed(
        description = f'{mode[gamemode]} Stats', 
        colour = discord.Colour.random(), 
    )

    for name, stat in overview['data']['segments'][gamemode]['stats'].items():
        embed.add_field(name=name, value=stat['value'], inline=True)

    _kd = overview['data']['segments'][1]['stats']['kdRatio']['value']
    level_image = overview['data']['segments'][0]['stats']['level']['metadata']['imageUrl']

    embed.set_author(name=username.split('#')[0], icon_url=level_image)
    for rank in ranks:
        if _kd >= rank['kd']:
            embed.set_thumbnail(url=rank['image'])
            break
        
    await ctx.send(embed=embed)

@client.command()
async def lobby(ctx, num_games=1):
    try:
        if int(num_games) < 1:
            await ctx.send('Invalid num_games! Must be a positive number. Canceling.')
            return
    except:
        await ctx.send('Invalid num_games! Must be a positive number. Canceling.')
        return
    
    discord_name = str(ctx.author)
    user = db.get_user(discord_name)
    
    if user is None:
        await ctx.send('Must be registered! Canceling.')
        return
    platform = user['default']
    username = user[platform]

    matches = db.get_matches(discord_name)

    if matches is None:
        matches = wz.get_matches(username)
        db.set_matches(discord_name, matches)

    embed = discord.Embed(
        title = 'Lobby Stats', 
        colour = discord.Colour.random()
    )
    
    for name, stat in overview['data']['segments'][gamemode]['stats'].items():
        embed.add_field(name=name, value=stat['value'], inline=True)

    _kd = overview['data']['segments'][1]['stats']['kdRatio']['value']
    for rank in ranks:
        if _kd >= rank['kd']:
            embed.set_thumbnail(url=rank['image'])
            break

    await ctx.send(embed=embed)

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
