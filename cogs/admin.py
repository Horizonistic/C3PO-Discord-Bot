#
# Modified version of https://github.com/Rapptz/RoboDanny/blob/master/cogs/admin.py
#

from discord.ext import commands
import discord
import inspect

# to expose to the eval command
import datetime
from collections import Counter

import utilities as util

class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def load(self, ctx, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def unload(self, ctx, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def reload(self, ctx, module : str):
        """Reloads a module."""
        try:
                self.bot.reload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Reloads all loaded modules."""
        print(self.bot.cogs['RandomSelection'].qualified_name)
        try:
            for name, cog in self.bot.cogs.items():
                print(name)
                self.bot.reload_extension(name)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def debug(self, ctx, *, code : str):
        """Evaluates code."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await ctx.send(python.format(result))

def setup(bot):
    bot.add_cog(Admin(bot))