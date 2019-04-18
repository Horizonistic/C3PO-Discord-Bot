import discord
from discord.ext import commands
import random
import requests

from file_extensions import FileExtensions as ext

loot_rolls_suffix = 'users'
c3po_quotes_filename = 'c3po_quotes'

description = '''C-3PO has been modernized to interface with contemporary chat software like Discord.'''
bot = commands.Bot(command_prefix='!', description=description)
client = discord.Client()

######
# Events
######
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Deletes posts in specified channel that are just URLs
# @bot.event
# async def on_message(message):
    # print(message)

######
# Names
######
@bot.group(pass_context=True,description='Commands for dealing with the list of names for drawings')
async def names(ctx):
    """Deals with the list of names"""
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid users command, try "!names help"\n' + get_random_from_file(c3po_quotes_filename))

@names.group(pass_context=True, description='Chooses who takes home the prize')
async def choose(ctx):
    """Select at random from the list of names"""
    filename = get_data_file(ctx.message.server.id, ext.ROLLS.value)

    winner = get_random_from_file(filename)
    await bot.say("The winner is " + winner)
    print("The winner is " + winner)

# Adds users to the pool
@names.group(pass_context=True,description='Adds any number of users to the list of names, separated by a space')
async def add(ctx, *users : str):
    """Add users to the list"""
    filename = get_data_file(ctx.message.server.id, ext.ROLLS.value)

    with open(filename, 'r') as file:
        lines = file.read().splitlines()

    confirmed_new_users = set(users).difference(lines)

    with open(filename, 'a') as file:
        for new_user in confirmed_new_users:
            file.write(new_user + '\n')
            print("Adding: " + new_user)

    if len(confirmed_new_users):
        bot_reply = ', '.join('{}'.format(k) for k in confirmed_new_users)
        await bot.say("Added users " + bot_reply + '\n' + get_random_from_file(c3po_quotes_filename))
    else:
        await bot.say("All those users were already added.\n" + get_random_from_file(c3po_quotes_filename))

# Removes a user from the pool
@names.group(pass_context=True,description='Removes one users from the list of already added names')
async def remove(ctx, user : str):
    """Removes a user"""
    filename = get_data_file(ctx.message.server.id, ext.ROLLS.value)

    lines = open(filename, 'r').readlines()
    
    # Iterate over file to check if passed name is in it
    for i, line in enumerate(lines[:]):
        line = line.rstrip('\n')
        if line == user:
            del lines[i]
            await bot.say("Removed user " + user + '\n' + get_random_from_file(c3po_quotes_filename))
            print("Deleting: " + user)

    open(filename, 'w').writelines(lines)

# Clears the filename list
@names.group(pass_context=True,description='Clears the list of all currently added names')
async def clear(ctx):
    """Clears the list"""
    filename = get_data_file(ctx.message.server.id, ext.ROLLS.value)
    
    file = open(filename, 'w')
    file.seek(0)
    file.truncate()
    await bot.say('Cleared users from ' + filename + '\n' + get_random_from_file(c3po_quotes_filename))
    return

@names.group(pass_context=True,description='Lists all names added')
async def show(ctx):
    """Lists all names added"""
    filename = get_data_file(ctx.message.server.id, ext.ROLLS.value)

    lines = open(filename, 'r').readlines()
    users = ''.join('{}'.format(k) for k in lines)
    await bot.say("Current user list:\n" + users)



######
# Other commands
######
@bot.command(description='For when you really need that bit of robot in your life')
async def quote():
    """Says a quote"""
    await bot.say(get_random_from_file(c3po_quotes_filename))

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses from a list"""
    await bot.say(random.choice(choices))

@bot.command(description='Rolls a totally fair and random dice in the NdN format.  For example, 2d20 rolls two d20 dice and returns the result.  Guaranteed cryptographically-secure randomness')
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(pass_context=True, description='When you just really really have to know')
async def check(ctx, *user : str):
    """For when you're really curious"""
    # If no user passed
    if len(user) is 0:
        if ctx.message.author.top_role.name == ctx.message.server.role_hierarchy[0].name:
            await bot.say("You are indeed gay.\n" + get_random_from_file(c3po_quotes_filename))
        else:
            await bot.say("You are not gay.\n" + get_random_from_file(c3po_quotes_filename))
    # If user passed
    else:
        user = ' '.join(user)
        member = ctx.message.server.get_member_named(user)
        if member is not None:
            if member.top_role.name == ctx.message.server.role_hierarchy[0].name:
                await bot.say(member.mention + " is indeed gay.\n" + get_random_from_file(c3po_quotes_filename))
            else:
                await bot.say(member.mention + " is not gay.\n" + get_random_from_file(c3po_quotes_filename))
        else:
            await bot.say("That user doesn't exist.\n" + get_random_from_file(c3po_quotes_filename))

######
# Utilities
######
# Returns a random C-3PO quote
def get_random_from_file(filename : str):
    lines = open(filename, 'r').readlines()
    secure_random = random.SystemRandom()
    return secure_random.choice(lines)

# Returns filename to save added roll names, check for file and creates if it doesn't exist
def get_data_file(server_id : str, extension : ext):
    filename = server_id + '.' + extension
    if not does_file_exists(filename):
        create_file(filename)
        # await bot.say("There was no file meaning you hadn't added any names.  Do that first please!\n" + get_random_from_file(c3po_quotes_filename))
        return None
    else:
        return filename

# Returns True/False whether passed filename exists or not
def does_file_exists(filename : str):
    try:
        file = open(filename, 'r')
        return True
    except FileNotFoundError:
        return False

# Creates file from passed filename
def create_file(filename : str):

    file = open(filename, 'a+')

botinfo = __import__("botinfo")
bot.run(botinfo.token)