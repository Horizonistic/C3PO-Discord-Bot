import discord
from discord.ext import commands

import validators
import random
import re

# File extension enums
from utilities import FileExtensions as ext
import utilities as util

######
# Channel moderation commands
######
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Deletes posts in specified channel that are just URLs
    @commands.Cog.listener()
    async def on_message(self, message):
        # This is interesting because I have to read through one file for each extension type for every single message
        # This seems inefficient so on_ready() should have something to load them into memory
        # If I switch over to a database instead of files this won't really be a problem
        # That's doesn't seem scalable, but why am I caring about scalability??

        # Make sure it's not running against its own messages, AND it's in a guild text channel
        if not isinstance(message.channel, discord.channel.TextChannel):
            return

        if message.author == message.guild.me:
            return
        
        # Iterate over all extensions to check all files for the channel ID that the message was just sent in
        for key, value in ext.__members__.items():
            if key != "ROLLS":
                filename = util.get_data_file(str(message.guild.id), ext[key].value)

                with open(filename, 'r') as file:
                    lines = file.read().splitlines()

                # If channel is being moderated
                if str(message.channel.id) in lines:
                    # URL detection
                    if value is ext.URL_CHANNELS:
                        if not validators.url(message.content):
                            pm_content = "Your message _\"{0}\"_ was removed from the channel _{1}_ because it wasn't just a URL.".format(message.content, message.channel.name)
                            await message.delete()
                            await message.author.send(content=pm_content)

                    # Shift code detection
                    if value is ext.SHIFT_CHANNELS:
                        regex = re.compile('^([a-zA-Z0-9]{5}-){4}[a-zA-Z0-9]{5}$')
                        message_lines = message.content.splitlines()
                        # Iterate over all lines of message
                        for line in message_lines:
                            if not regex.match(line.strip()):
                                # Invalid shift code!
                                pm_content = "Your message _\"{0}\"_ was removed from the channel _{1}_ because it contained one or more invalid shift code.".format(message.content, message.channel.name)
                                await message.delete()
                                await message.author.send(content=pm_content)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.author.send("You don't have the permissions to run the command _{0}_ on the server _{1}_.  You need the Manage Messages permission.".format(ctx.message.content, ctx.guild.name))

    @commands.command(pass_context=True,description='Lists all names added')
    @commands.has_permissions(manage_messages=True)
    async def moderate(self, ctx, type_str: str):
        """Adds channel to moderation list"""
        # Basically a switch statement for getting the enum based on argument passed
        if type_str == "urls":
            type = ext.URL_CHANNELS.value
            pass
        elif type_str == "shift":
            type = ext.SHIFT_CHANNELS.value
            pass
        else:
            await util.send_with_quote(ctx, "Not a valid option")

        filename = util.get_data_file(str(ctx.guild.id), type)
        channel = str(ctx.channel.id)

        # Reads the file into a set
        with open(filename, 'r') as file:
            lines = file.read().splitlines()

        # Toggle moderating the channel
        if channel not in lines:
            with open(filename, 'a') as file:
                file.write(channel + '\n')
                ctx.message.delete()
                pm_content = "Now monitoring _{0}_ on server _{1}_ for _{2}_".format(ctx.channel.name, ctx.guild.name, type_str)
                await ctx.author.send(content=pm_content)
        else:
            for i, line in enumerate(lines[:]):
                line = line.rstrip('\n')
                if line == channel:
                    del lines[i]
                    pm_content = "No longer monitoring _{0}_ on server _{1}_ for _{2}_.  Your command will still be deleted.".format(ctx.channel.name, ctx.guild.name, type_str)
                    await ctx.author.send(content=pm_content)
            open(filename, 'w').writelines(lines)

def setup(bot):
    bot.add_cog(Moderation(bot))