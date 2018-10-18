import base64
import os
import uuid
from math import fmod

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
    if message.content.startswith('wh!count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('wh!hash'):
        hashable_message = message.content
        error = False
        try:
            a, b = hashable_message.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be hashed as second parameter')
            error = True
        if not error:
            await client.send_message(message.channel, 'SHA3-512 Hash of {}:'.format(b))
            await client.send_message(message.channel, hashlib.sha3_512(b.encode('utf-8')).hexdigest())

    elif message.content.startswith('wh!eval'):
        secret = 'TestSecret'
        nonce = uuid.uuid4().hex
        await client.send_message(message.channel,
                                  'Please calculate the hash of the secret and nonce: \n {} \n You have 30 seconds'
                                  .format(nonce))
        msg = await client.wait_for_message(author=message.author, timeout=30)
        if msg is not None:
            if msg is hashlib.sha3_512(secret.encode('utf-8') + nonce.encode('utf-8')).hexdigest():
                await client.send_message(message.channel, 'You would\'ve gotten eval, it\'s not implemented though.')
            else:
                await client.send_message(message.channel, 'You sent an invalid hash or you timed out.')
        else:
            await client.send_message(message.channel, 'You sent an invalid hash or you timed out.')

    elif message.content.startswith('wh!shutdown') or message.content.startswith('wh!stop'):
        await client.send_message(message.channel, 'Shutting down')
        await client.logout()


client.run('NTAyNDEyNTI2OTkxMTc5Nzg2.DqnjxA.tYxjA-AGeAg7XmuhYg-Ov6jA5Zk')
