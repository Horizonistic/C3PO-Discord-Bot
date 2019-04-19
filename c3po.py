import discord
from discord.ext import commands

import random
import validators

# File extension enums
from utilities import FileExtensions as ext
import utilities as util

description = '''C-3PO has been modernized to interface with contemporary chat software like Discord.'''
bot = commands.Bot(command_prefix='!', description=description)

bot.load_extension("cogs.admin")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.random_selection")
bot.load_extension("cogs.other")

# todo: make a way to check if channel is moderated
# todo: make a list of cog names (e.g. "cogs.randomselection") to !reloadall easily
# todo: use databases instead of files to save settings (maybe in the future)

######
# Events
######
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# For the bot authentication token
botinfo = __import__("botinfo")
bot.run(botinfo.token)