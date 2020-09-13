import traceback
import sys
from discord.ext import commands
import discord
from discord.errors import DiscordException


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        # ignored = ()
        error = getattr(error, "original", error)
        # await ctx.send(type(error).__name__)

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"Command not found. Try !help for a list of commands")
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
            await ctx.send(ctx.command)
        else:
            return await ctx.send(f'{error}')


def setup(client):
    client.add_cog(CommandErrorHandler(client))