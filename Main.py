import discord
import asyncio
import hashlib

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!hash'):
        hashable_message = message.content
        error = False
        try:
            a, b = hashable_message.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be hashed as second parameter')
            error = True
        if not error:
            await client.send_message(message.channel, 'SHA3-512 Hash of the message:')
            await client.send_message(message.channel, hashlib.sha3_512(b.encode('utf-8')).hexdigest())
    elif message.content.startswith('!shutdown') or message.content.startswith('!stop'):
        await client.send_message(message.channel, 'Shutting down')
        await client.logout()


client.run('NTAyNDEyNTI2OTkxMTc5Nzg2.DqnjxA.tYxjA-AGeAg7XmuhYg-Ov6jA5Zk')
