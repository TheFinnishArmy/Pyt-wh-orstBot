import discord
import hashlib

import ability_info


async def process(message, message_string, client):
    if message_string.startswith('wh!count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message_string.startswith('wh!hash'):
        message_string = message_string.replace('wh!hash', '')
        message_string = message_string.strip()

        if message_string is not '':
            await client.send_message(message.channel, 'SHA3-512 Hash of {}:'.format(message_string))
            await client.send_message(message.channel, hashlib.sha3_512(message_string.encode('utf-8')).hexdigest())

        else:
            await client.send_message(message.channel, 'Please input string to be hashed as first parameter')

    elif message_string.startswith('wh!changePresence'):
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
            try:
                c_int = int(c)
            except ValueError:
                await client.send_message(message.channel,
                                          'Please enter a int as the second parameter, current entered has been '
                                          'discarded as it couldn\'t be converted')
                c_int = None
            except TypeError:
                c_int = None

            if c_int is not None:
                test_game = discord.Game(name=b, type=c_int)
                await client.change_presence(game=test_game)
                await client.send_message(message.channel, 'Changed to status: {0} \n and game: {1}'.format(c, b))
            else:
                test_game = discord.Game(name=b)
                await client.change_presence(game=test_game)
                await client.send_message(message.channel, 'Changed to game: {}'.format(b))

    elif message_string.startswith('wh!abilityinfo'):
        try:
            embed_pack = ability_info.build(message_string)

        except ValueError:
            await client.send_message(message.channel, 'Please input string to be searched as first parameter')
        except AttributeError:
            await client.send_message(message.channel,
                                      'Couldn\'t find a page with an ability description by that '
                                      'name. (All names are case-sensitive)')
        except KeyError:
            await client.send_message(message.channel, 'Couldn\'t find a wikipage by that name. (All names are '
                                                       'case-sensitive)')

        else:
            main_embed = embed_pack['main_embed']
            prim_embed = embed_pack['prim_embed']
            secd_embed = embed_pack['secd_embed']

            await client.send_message(message.channel, embed=main_embed)
            await client.send_message(message.channel, embed=prim_embed)
            if secd_embed is not None:
                await client.send_message(message.channel, embed=secd_embed)

    elif message_string.startswith('wh!shutdown') or message_string.startswith('wh!stop'):
        await client.send_message(message.channel, 'Shutting down')
        await client.logout()
