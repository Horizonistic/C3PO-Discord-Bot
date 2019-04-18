import discord
from discord.ext import commands

import random

# File extension enums
from utilities import FileExtensions as ext
import utilities as util

######
# Other commands
######
class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @bot.command(pass_context=True,description='For when you really need that bit of robot in your life')
    # async def quote(ctx):
    #     """Says a quote"""
    #     await ctx.send(util.get_random_from_file(c3po_quotes_filename))

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(ctx, *choices: str):
        """Chooses from a list"""
        await ctx.send(random.choice(choices))

    @commands.command(description='Rolls a totally fair and random dice in the NdN format.  For example, 2d20 rolls two d20 dice and returns the results.  Guaranteed cryptographically-secure randomness')
    async def roll(ctx,dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(pass_context=True, description='When you just really really have to know')
    async def check(ctx, *user : str):
        """For when you're really curious"""
        # If no user passed
        if len(user) is 0:
            if ctx.message.author.top_role.name == ctx.guild.roles[len(ctx.guild.roles) - 1].name:
                await util.send_with_quote(ctx, "You are indeed gay.")
            else:
                await util.send_with_quote(ctx, "You are not gay.")
        # If user passed
        else:
            user = ' '.join(user)
            member = ctx.guild.get_member_named(user)
            if member is not None:
                if member.top_role.name == ctx.guild.roles[len(ctx.guild.roles) - 1].name:
                    await util.send_with_quote(ctx, member.mention + " is indeed gay.")
                else:
                    await util.send_with_quote(ctx, member.mention + " is not gay.")
            else:
                await util.send_with_quote(ctx, "That user doesn't exist.")

def setup(bot):
    bot.add_cog(Other(bot))