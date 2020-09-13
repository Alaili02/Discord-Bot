# bot.py
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')

bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True,
    owner_id=int(OWNER_ID),
    activity = discord.Activity(name="Re Zero", type=discord.ActivityType.watching)
)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('I have logged in as {0.user.name}'.format(bot))
    for guild in bot.guilds:
        general = discord.utils.find(lambda x: x.name == 'general',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            print("Joined " + general.name)
            # await general.send('Moshi mosh {}!'.format(guild.name))
            # for emoji in guild.emojis:
            #     print(emoji.id)


@bot.command(pass_context=True)
async def load(ctx, extension):
    if ctx.message.author.id == bot.owner_id:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send("Loaded "+extension+" cog")
    else:
        await ctx.send("Only Alaili can use this command")


@bot.command(pass_context=True)
async def unload(ctx, extension):
    if ctx.message.author.id == bot.owner_id:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send("Unloaded "+extension+" cog")
    else:
        await ctx.send("Only Alaili can use this command")


@bot.command(pass_context=True)
async def reload(ctx, extension):
    if ctx.message.author.id == bot.owner_id:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send("Reloaded "+extension+" cog")
    else:
        await ctx.send("Only Alaili can use this command")


@bot.command()
async def shutdown(ctx):
    if ctx.message.author.id == bot.owner_id:
        print("Shutdown")
        await ctx.send("Sayonara")
        await bot.logout()
    else:
        await ctx.send("Only Alaili can use this command")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN, bot=True)
