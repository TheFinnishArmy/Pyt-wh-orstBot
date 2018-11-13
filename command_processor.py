import discord
import hashlib
import re

import ability_info


def permission_check(message):
    truth_factor = message.channel.server.get_member(message.author.id).server_permissions.kick_members
    if message.author != message.channel.server.owner:
        if not truth_factor:
            return False

    return True


async def colour_me(message, message_string, client):
    current_server = message.channel.server
    author = current_server.get_member(message.author.id)

    role_list = author.roles
    role_regex = r'Colou?r #[0-F]{6}'
    message_regex = r'^[0-F]{6}$'

    message_string = message_string.replace('#', '')
    message_string = message_string.strip()
    message_string = message_string.upper()

    if re.match(message_regex, message_string):
        colour = discord.Colour(int(message_string, 16))

        role = None
        for role_candidate in role_list:
            if re.match(role_regex, role_candidate.name):
                role = role_candidate
                break

        if role is None:
            role_pos = author.top_role.position + 1
            new_role = await client.create_role(server=current_server, colour=colour, name= 'Colour #{}'.format(message_string))
            await client.move_role(server=current_server, role=new_role, position=role_pos)
            await client.add_roles(author, new_role)

        else:
            await client.edit_role(server=current_server, role=role, colour=colour, name= 'Colour #{}'.format(message_string))
            await client.add_roles(author, role)

    else:
        await  client.send_message(message.channel, 'The command requires a hexadecimal colour entered in:\n '
                                                    'ex. #008ad0')
        return

    await client.send_message(message.channel, 'Your new colour has been added.')

    return


async def process(message, message_string, is_owner, client):
    if message_string.startswith('wh!count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message_string.startswith('wh!colourme'):
        message_string = message_string.replace('wh!colourme', '')
        await colour_me(message, message_string, client)

    elif message_string.startswith('wh!colorme'):
        message_string = message_string.replace('wh!colorme', '')
        await colour_me(message, message_string, client)

    elif message_string.startswith('wh!hash'):
        message_string = message_string.replace('wh!hash', '')
        message_string = message_string.strip()

        if message_string is not '':
            await client.send_message(message.channel, 'SHA3-512 Hash of {}:'.format(message_string))
            await client.send_message(message.channel, hashlib.sha3_512(message_string.encode('utf-8')).hexdigest())

        else:
            await client.send_message(message.channel, 'Please input string to be hashed as first parameter')

    elif message_string.startswith('wh!changepresence'):
        if not is_owner:
            await client.send_message(message.channel, 'This command is only available to the owner of the bot.')
            return

        a, b, c = None, None, None
        message_string = message_string.replace('wh!changepresence', '')
        message_string = message_string.strip()
        try:
            presence_number = int(message_string[0:1])
        except ValueError:
            await client.send_message(message.channel, 'Please enter a number to dictate which presence "flavour" you '
                                                       'would like. \n \n'

                                                       'If you\'re not sure; "0" is always a good option')
            return

        presence_title = message_string.title()[1:]

        test_game = discord.Game(name=presence_title, type=presence_number)
        await client.change_presence(game=test_game)
        await client.send_message(message.channel, 'Changed presence to: {0}'.format(presence_title))

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

    elif message_string.startswith('wh!kick'):
        if permission_check(message):
            await client.send_message(message.channel, 'Would\'ve resulted in a successful kick')
        else:
            await client.send_message(message.channel, 'Wouldn\'t have resulted in a successful kick')

    elif message_string.startswith('wh!shutdown') or message_string.startswith('wh!stop'):
        if not is_owner:
            await client.send_message(message.channel, 'This command is only available to the owner of the bot.')
            return

        await client.send_message(message.channel, 'Shutting down')
        await client.logout()
