from discord.ext import commands
import random
from enum import Enum
import os
import os.path

c3po_quotes_filename = "c3po_quotes"
data_files_folder = "data"

class FileExtensions(Enum):
    ROLLS = "users"
    URL_CHANNELS = "urlmonitor"
    SHIFT_CHANNELS = "shiftmonitor"

class CogNames(Enum):
    ADMIN = "cogs.admin"
    RANDOM = "cogs.random_selection"
    MODERATION = "cogs.moderation"

async def send_with_quote(ctx, message: str):
    await ctx.send(message + '\n' + get_random_from_file(c3po_quotes_filename))

# Returns a random C-3PO quote
def get_random_from_file(filename: str):
    if does_file_exist(filename):
        lines = open(filename, 'r').readlines()
        secure_random = random.SystemRandom()
        return (secure_random.choice(lines)).rstrip('\n')

# Returns filename to save added roll names, check for file and creates if it doesn't exist
def get_data_file(server_id: str, extension: FileExtensions):
    filename = build_file_path(server_id, extension)

    if not does_file_exist(filename):
        create_file(filename)

    return filename

# This is a weird function that's not _entirely_ necessary but I like it
# It's like I'm planning for something bigger than this actually is
def build_file_path(server_id: str, extension: FileExtensions):
    return data_files_folder + '/' + server_id + '/' + extension

# Returns True/False whether passed filename exists or not
def does_file_exist(filename: str):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        file = open(filename, 'r')
        return True
    except FileNotFoundError:
        return False

# Creates file from passed filename
def create_file(filename: str):
    file = open(filename, 'a+')