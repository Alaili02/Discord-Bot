import discord
from discord.ext import commands
import random
import praw


class Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reddit = praw.Reddit(client_id='2ZIY25fKtQIIRw',
                         client_secret='oh9je5-QZ0S5vy5goCaEqQIR5WQ',
                         user_agent='pythondiscord:RemApplication to scrape posts (by u/alaili)')

    @commands.command()
    async def check(self, ctx):
        await ctx.send(ctx.channel.guild.me.guild_permissions)
        if 0x2147483647 & 0x134217728:
            await ctx.send("can change nicknames")
        # await ctx.send(ctx.author.user.server_permissions)
        # await ctx.send("true")

    @commands.command(pass_context=True)
    async def roll(self, ctx, min_number=0, max_number=100):
        min_number = int(min_number)
        max_number = int(max_number)
        await ctx.send(f'Rolling a random number between {min_number} and {max_number}:')
        await ctx.send(f'{random.randrange(min_number, max_number+1)}')

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Only enter integers baka.\nAppropriate usage: !roll (minimum_number) (maximum_number)')

    @commands.command(pass_context=True)
    async def send(self, ctx, *, name):
        if name == "Random" or name == "random":
            image_path = f'./Media/Reaction Images/{random.randrange(0,118)}.png'
        else:
            await ctx.send("Invalid image")
            return
        await ctx.send(file=discord.File(f'{image_path}'))

    # Embed help with list and details of commands
    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='Help : list of commands available')
        embed.add_field(name='!shutdown', value='Not implemented yet', inline=False)
        embed.add_field(name='!join', value='Joins voice channel', inline=False)
        embed.add_field(name='!leave', value='Leaves voice channel', inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def chnick(self, ctx, member: discord.Member, nick):
        await member.edit(nick=nick)
        await ctx.send(f'{member.name}\'s nickname changed to {nick}')

    @commands.command(pass_context=True, name="reddit")
    async def reddit_(self, ctx, meme="dankmeme", user: discord.Member = 'None'):
        if meme == 'dankmeme':
            sub = 'dankmemes'
        elif meme == 'animeme':
            sub = 'goodanimemes'
        elif meme == 'memrimeme':
            sub = 'memritvmemes'
        else:
            await ctx.send("Usage: `!reddit (dankmeme, animeme, or memrimeme) (user_name)`")
            return
        await ctx.trigger_typing()
        memes_submissions = self.reddit.subreddit(sub).hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        if user == 'None':
            await ctx.channel.send(submission.url)
            await ctx.channel.send(f'https://www.reddit.com/r/{sub}/comments/{submission}')
        else:
            await ctx.send(f'Sent https://www.reddit.com/r/{sub}/comments/{submission} to {user}')
            await user.send(submission.url)
            await user.send(f'https://www.reddit.com/r/{sub}/comments/{submission}')


def setup(bot):
    bot.add_cog(Command(bot))
