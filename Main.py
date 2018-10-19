import discord
import asyncio
import hashlib
import requests
import json

client = discord.Client()

# TODO in a another file (TODO.md)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    testGame = discord.Game(name="my creators ramblings", type=2)
    await client.change_presence(game=testGame)


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
            await client.send_message(message.channel, 'Please input string to be hashed as first parameter')
            error = True
        if not error:
            await client.send_message(message.channel, 'SHA3-512 Hash of {}:'.format(b))
            await client.send_message(message.channel, hashlib.sha3_512(b.encode('utf-8')).hexdigest())

    elif message.content.startswith('wh!changePresence'):
        messageString = message.content
        error = False
        a, b, c = None, None, None
        try:
            try:
                a, b, c = messageString.split(' ')
            except ValueError:
                a, b = messageString.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be used as the game')
            error = True

        if not error:
            error = False
            try:
                cInt = int(c)
            except ValueError:
                await client.send_message(message.channel,
                                          'Please enter a int as the second parameter, current entered has been '
                                          'discarded as it couldn\'t be converted')
                error = True
            except TypeError:
                error = True

            if not error:
                testGame = discord.Game(name=b, type=cInt)
                await client.change_presence(game=testGame)
                await client.send_message(message.channel, 'Changed to status: {0} \n and game: {1}'.format(c, b))
            else:
                testGame = discord.Game(name=b)
                await  client.change_presence(game=testGame)
                await client.send_message(message.channel, 'Changed to game: {}'.format(b))

    elif message.content.startswith('wh!wikiFetch'):

        hashable_message = message.content
        error = False
        try:
            a, b = hashable_message.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be searched as first parameter')
            error = True
        if not error:
            S = requests.Session()

            URL = 'http://overwatch.wikia.com/api.php'

            TITLE = b

            PARAMS = {
                'action': 'query',
                'titles': TITLE,
                'prop': 'revisions',
                'rvprop':  'content',
                'format': 'json'
            }

            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()

            error = False

            try:
                filteredData1 = DATA['query']['pages']
                filteredData2 = filteredData1[next(iter(filteredData1))]['revisions'][0]['*']
                filteredDataString = str(filteredData2)
            except KeyError:
                await client.send_message(message.channel, 'Couldn\'t find a wikipage by that name. (All names are '
                                                           'case-sensitive)')
                error = True
            if not error:
                try:
                    a, b = filteredDataString.split('</onlyinclude>')
                except ValueError:
                    await client.send_message(message.channel, 'Couldn\'t find a page with an ability description by that '
                                                           'name. (All names are case-sensitive)')
                    error = True

                if not error:
                    await client.send_message(message.channel, a)

    elif message.content.startswith('wh!eval'):
        await client.send_message(message.channel, 'Currently not working, @ my creator if you really want it.')
        '''
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
        '''

    elif message.content.startswith('wh!shutdown') or message.content.startswith('wh!stop'):
        await client.send_message(message.channel, 'Shutting down')
        await client.logout()


client.run('NTAyNDEyNTI2OTkxMTc5Nzg2.DqnjxA.tYxjA-AGeAg7XmuhYg-Ov6jA5Zk')
