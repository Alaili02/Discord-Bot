from discord.ext import commands
import random
from random import shuffle


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = [line.rstrip('\n') for line in open('chat/Messages.txt', 'r')]
        self.responses = [line.rstrip('\n') for line in open('chat/Responses.txt', 'r')]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        msg_content = message.content.lower()
        if 'rem' in msg_content:
            if msg_content.startswith('rem '):
                msg_content = msg_content[4:]
            elif msg_content.endswith(' rem'):
                msg_content = msg_content[:-4]
            else:
                return
            msg_content.strip()      

            if msg_content == "check":
                await message.channel.send(f'Message user ID: {message.author.id}\nOwner user ID: {self.bot.owner_id}')
            elif msg_content in self.messages:
                await message.channel.trigger_typing()
                await message.channel.send(f'{self.responses[self.messages.index(msg_content)]} {message.author.name}')

def setup(bot):
    bot.add_cog(Event(bot))

