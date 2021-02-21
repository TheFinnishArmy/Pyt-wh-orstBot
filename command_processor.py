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
            new_role = await client.create_role(server=current_server, colour=colour,
                                                name='Colour #{}'.format(message_string))
            await client.move_role(server=current_server, role=new_role, position=role_pos)
            await client.add_roles(author, new_role)

        else:
            await client.edit_role(server=current_server, role=role, colour=colour,
                                   name='Colour #{}'.format(message_string))
            await client.add_roles(author, role)

    else:
        await  message.channel.send('The command requires a hexadecimal colour entered in:\n '
                                    'ex. #008ad0')
        return

    await message.channel.send('Your new colour has been added.')

    return


async def process(message: discord.Message, message_string: str, is_owner, client: discord.Client):
    # ToDo: Untested if broken
    if message_string.startswith('wh!colourme'):
        message_string = message_string.replace('wh!colourme', '')
        await colour_me(message, message_string, client)

    elif message_string.startswith('wh!colorme'):
        message_string = message_string.replace('wh!colorme', '')
        await colour_me(message, message_string, client)

    elif message_string.startswith('wh!hash'):
        message_string = message_string.replace('wh!hash', '')
        message_string = message_string.strip()

        if message_string != '':
            await message.channel.send('SHA3-512 Hash of {}:'.format(message_string))
            await message.channel.send(hashlib.sha3_512(message_string.encode('utf-8')).hexdigest())

        else:
            await message.channel.send('Please input string to be hashed as first parameter')

    elif message_string.startswith('wh!changepresence'):
        if not is_owner:
            await message.channel.send('This command is only available to the owner of the bot.')
            return

        message_string = message_string.replace('wh!changepresence', '')
        message_string = message_string.strip()
        try:
            presence_number = int(message_string[0:1])
        except ValueError:
            await message.channel.send('Please enter a number to dictate which presence "flavour" you '
                                       'would like. \n \n'

                                       'If you\'re not sure; "0" is always a good option')
            return

        presence_title = message_string.title()[2:]

        test_game = discord.Activity(name=presence_title, type=presence_number)
        await client.change_presence(activity=test_game)
        await message.channel.send('Changed presence to: {0}'.format(presence_title))

    elif message_string.startswith('wh!abilityinfo'):
        try:
            embed_pack = ability_info.build(message_string)

        except ValueError:
            await message.channel.send('Please input string to be searched as first parameter')
        except AttributeError:
            await message.channel.send('Couldn\'t find a page with an ability description by that '
                                       'name. (All names are case-sensitive)')
        except KeyError:
            await message.channel.send('Couldn\'t find a wikipage by that name. (All names are '
                                       'case-sensitive)')

        else:
            main_embed = embed_pack['main_embed']
            prim_embed = embed_pack['prim_embed']
            secd_embed = embed_pack['secd_embed']

            await message.channel.send(embed=main_embed)
            await message.channel.send(embed=prim_embed)
            if secd_embed is not None:
                await message.channel.send(embed=secd_embed)

    elif message_string.startswith('wh!poll'):
        message_string = message_string.replace('wh!poll', '')
        message_string = message_string.strip()
        message_string_list = message_string.split('" "')

        whitespace_regex = r'\s+'
        non_whitespace_list = []

        for item in message_string_list:
            item = item.replace('"', '')

            if re.match(whitespace_regex, item) or item == "":
                continue

            non_whitespace_list.append(item)

        if len(non_whitespace_list) == 1:
            yes_emoji = None
            no_emoji = None

            server_emoji = message.channel.server.emojis

            for candidate_emoji in server_emoji:
                if candidate_emoji.name == 'yes':
                    yes_emoji = candidate_emoji
                elif candidate_emoji.name == 'no':
                    no_emoji = candidate_emoji

            if yes_emoji is None or no_emoji is None:
                await message.channel.send('This server hasn\'t setup the yes and no reaction emojis.')
                return

            embed = discord.Embed(description=non_whitespace_list[0])
            sent_message = await message.channel.send(embed=embed)

            await client.add_reaction(sent_message, yes_emoji)
            await client.add_reaction(sent_message, no_emoji)

        elif 10 >= len(non_whitespace_list) > 0:
            emoji_list = [
                'one',
                'two',
                'three',
                'four',
                'five',
                'six',
                'seven',
                'eight',
                'nine',
                'keycap_ten'
            ]

            index = 0
            embed = discord.Embed(description=non_whitespace_list[0])

            for _ in non_whitespace_list:
                index += 1
                embed.add_field(name='Option {}:'.format(index), value=non_whitespace_list[index])

            sent_message = await message.channel.send(embed=embed)

            i = 0
            while i <= index:
                await client.add_reaction(sent_message, emoji_list[i])

        else:
            await message.channel.send('This command can be used with 1 question or'
                                       ' 1 title and 2 to 7 options.')

    elif message_string.startswith('wh!shutdown') or message_string.startswith('wh!stop'):
        if not is_owner:
            await message.channel.send('This command is only available to the owner of the bot.')
            return

        await message.channel.send('Shutting down')
        await client.logout()
