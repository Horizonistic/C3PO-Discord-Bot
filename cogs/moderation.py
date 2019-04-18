import discord
from discord.ext import commands

import random

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
    async def on_message(message):
        # This is interesting because I have to read through one file for each extension type for every single message
        # This seems inefficient so on_ready() should have something to load them into memory
        # That's doesn't seem scalable, but why am I caring about scalability??
        
        # Iterate over all extensions to check all files for the channel ID that the message was just sent in
        for key, value in ext.__members__.items():
            if key != "ROLLS":
                filename = util.get_data_file(str(message.guild.id), ext[key].value)

                with open(filename, 'r') as file:
                    lines = file.read().splitlines()

                if str(message.channel.id) in lines:
                    if value is ext.URL_CHANNELS:
                        print("yes")

                    if value is ext.SHIFT_CHANNELS:
                        print("yes2")
                    # Check against message type for each moderation type

        await bot.process_commands(message)

    @commands.command(pass_context=True,description='Lists all names added')
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
                await util.send_with_quote(ctx, "Now monitoring this channel")
        else:
            for i, line in enumerate(lines[:]):
                line = line.rstrip('\n')
                if line == channel:
                    del lines[i]
                    await util.send_with_quote(ctx, "No longer monitoring this channel")
            open(filename, 'w').writelines(lines)

def setup(bot):
    bot.add_cog(Moderation(bot))