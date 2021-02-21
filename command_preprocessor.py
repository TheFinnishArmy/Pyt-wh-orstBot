import command_processor as command
import discord


async def process(message: discord.Message, is_owner, client: discord.Client):
    if message.author.id == client.user.id:
        return
    if not message.content.startswith('wh!'):
        return
    if message.channel.type != discord.ChannelType.text:
        await message.channel.send('Please use this bot from a guild channel, many features depend on '
                                                   'it.')
        return

    message_string = message.content.lower()

    await command.process(message, message_string, is_owner, client)
