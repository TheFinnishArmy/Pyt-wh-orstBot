import discord
import asyncio
import hashlib
import requests

client = discord.Client()


# TODO in a another file (TODO.md)

def search_image_name(b_list):
    for item in b_list:
        if item.startswith('image'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            return item

    return None

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    test_game = discord.Game(name="my creators ramblings", type=2)
    await client.change_presence(game=test_game)


@client.event
async def on_message(message):
    if message.content.lower().startswith('wh!count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.lower().startswith('wh!hash'):
        messageString = message.content
        error = False
        try:
            a, b = messageString.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be hashed as first parameter')
            error = True
        if not error:
            await client.send_message(message.channel, 'SHA3-512 Hash of {}:'.format(b))
            await client.send_message(message.channel, hashlib.sha3_512(b.encode('utf-8')).hexdigest())

    elif message.content.lower().startswith('wh!changePresence'):
        message_string = message.content
        error = False
        a, b, c = None, None, None
        try:
            try:
                a, b, c = message_string.split(' ')
            except ValueError:
                a, b = message_string.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be used as the game')
            error = True

        if not error:
            error = False
            try:
                c_int = int(c)
            except ValueError:
                await client.send_message(message.channel,
                                          'Please enter a int as the second parameter, current entered has been '
                                          'discarded as it couldn\'t be converted')
                error = True
            except TypeError:
                error = True

            if not error:
                test_game = discord.Game(name=b, type=c_int)
                await client.change_presence(game=test_game)
                await client.send_message(message.channel, 'Changed to status: {0} \n and game: {1}'.format(c, b))
            else:
                test_game = discord.Game(name=b)
                await  client.change_presence(game=test_game)
                await client.send_message(message.channel, 'Changed to game: {}'.format(b))

    elif message.content.lower().startswith('wh!abilityinfo'):

        messageString = message.content
        error = False
        try:
            a, b = messageString.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be searched as first parameter')
            error = True

        if not error:
            s = requests.Session()

            url = 'http://overwatch.wikia.com/api.php'

            title = b

            paramsAbility = {
                'action': 'query',
                'titles': title,
                'prop': 'revisions',
                'rvprop': 'content',
                'format': 'json'
            }

            r = s.get(url=url, params=paramsAbility)
            data = r.json()

            error = False

            try:
                filtered_data1 = data['query']['pages']
                filtered_data2 = filtered_data1[next(iter(filtered_data1))]['revisions'][0]['*']
                filtered_data_string = str(filtered_data2)
            except KeyError:
                await client.send_message(message.channel, 'Couldn\'t find a wikipage by that name. (All names are '
                                                           'case-sensitive)')
                error = True
            if not error:
                try:
                    a, b = filtered_data_string.split('</onlyinclude>')

                    a_list = a.split('\n')
                    a_list.pop(0)
                    a_list.pop()
                    a_list.pop()

                    b_list = None

                    await client.send_message(message.channel, 'Somewhat formatted response:')

                    for item in a_list:
                        item = item.replace('|', ' ')
                        item = item.replace('{', '')
                        item = item.replace('}', '')
                        item = item.replace('Texttip', '')
                        if item is not None and item != '':
                            b_list.append(item)

                    image_name = search_image_name(b_list)

                    if image_name is not None and image_name is not '':
                        s = requests.Session()

                        url = 'http://overwatch.wikia.com/api.php'

                        params_image = {
                            'action': 'query',
                            'list': 'allimages',
                            'ailimit': '1',
                            'aifrom': x,
                            'aiprop': 'url',
                            'format': 'json'
                        }

                        r = s.get(url=url, params=params_image)
                        image_data = r.json()

                        print(image_data)

                except ValueError:
                    await client.send_message(message.channel,
                                              'Couldn\'t find a page with an ability description by that '
                                              'name. (All names are case-sensitive)')

    elif message.content.lower().startswith('wh!eval'):
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

    elif message.content.lower().startswith('wh!shutdown') or message.content.startswith('wh!stop'):
        await client.send_message(message.channel, 'Shutting down')
        await client.logout()


client.run('NTAyNDEyNTI2OTkxMTc5Nzg2.DqnjxA.tYxjA-AGeAg7XmuhYg-Ov6jA5Zk')
