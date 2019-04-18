import discord
from discord.ext import commands

import random

# File extension enums
from utilities import FileExtensions as ext
import utilities as util

class RandomSelection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ######
    # Names
    ######
    @commands.group(pass_context=True,description='Commands for dealing with the list of names for drawings')
    async def names(self, ctx):
        """Deals with the list of names"""
        if ctx.invoked_subcommand is None:
            await util.send_with_quote(ctx, "Invalid users command, try \" !help names\"")

    @names.group(pass_context=True, description='Chooses who takes home the prize')
    async def choose(self, ctx):
        """Select at random from the list of names"""
        filename = util.get_data_file(str(ctx.guild.id), ext.ROLLS.value)

        winner = util.get_random_from_file(filename)
        await ctx.send("The winner is " + winner + "!")
        await ctx.send("The winner is " + winner + "!")

    # Adds users to the pool
    @names.group(pass_context=True,description='Adds any number of users to the list of names, separated by a space')
    async def add(self, ctx, *users : str):
        """Add users to the list"""
        filename = util.get_data_file(str(ctx.guild.id), ext.ROLLS.value)

        with open(filename, 'r') as file:
            lines = file.read().splitlines()

        confirmed_new_users = set(users).difference(lines)

        with open(filename, 'a') as file:
            for new_user in confirmed_new_users:
                file.write(new_user + '\n')

        if len(confirmed_new_users):
            bot_reply = ', '.join('{}'.format(k) for k in confirmed_new_users)
            await util.send_with_quote(ctx, "Added users " + bot_reply)
        else:
            await util.send_with_quote(ctx, "All those users were already added")

    # Removes a user from the pool
    @names.group(pass_context=True,description='Removes one users from the list of already added names')
    async def remove(self, ctx, user : str):
        """Removes a user"""
        filename = util.get_data_file(str(ctx.guild.id), ext.ROLLS.value)

        lines = open(filename, 'r').readlines()
        
        # Iterate over file to check if passed name is in it
        for i, line in enumerate(lines[:]):
            line = line.rstrip('\n')
            if line == user:
                del lines[i]
                await util.send_with_quote(ctx, "Removed user " + user)

        open(filename, 'w').writelines(lines)

    # Clears the filename list
    @names.group(pass_context=True,description='Clears the list of all currently added names')
    async def clear(self, ctx):
        """Clears the list"""
        filename = util.get_data_file(str(ctx.guild.id), ext.ROLLS.value)
        
        file = open(filename, 'w')
        file.seek(0)
        file.truncate()
        await util.send_with_quote(ctx, "Cleared users from the list")
        return

    @names.group(pass_context=True,description='Lists all names added')
    async def show(self, ctx):
        """Lists all names added"""
        filename = util.get_data_file(str(ctx.guild.id), ext.ROLLS.value)

        lines = open(filename, 'r').readlines()
        users = ''.join('{}'.format(k) for k in lines)
        await ctx.send("Current user list:\n" + users)

def setup(bot):
    bot.add_cog(RandomSelection(bot))