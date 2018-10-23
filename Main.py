import discord
import asyncio
import hashlib
import requests
import re

client = discord.Client()


# TODO in a another file (TODO.md)

def search_image_name(b_list):
    for item in b_list:
        if item.startswith('image'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            return b

    return None


def build_embed(json_list, image_url):
    title_string = ''
    description_string = ''

    for item in json_list:
        if item.startswith('name'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            title_string += b
        if item.startswith('description'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            description_string += b

    embed = discord.Embed(title=title_string, description=description_string)

    if image_url is not None and image_url is not '':
        embed.set_thumbnail(url=image_url)

    for item in json_list:
        if item.startswith('image'):
            continue
        elif item.startswith("name"):
            continue
        elif item.startswith('type'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Weapon type:", value=b)

        elif item.startswith('ammo'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Weapon ammo:", value=b)

        elif item.startswith('reload'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Reload time:", value=b)

        elif item.startswith('damage'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Weapon damage:", value=b)

        elif item.startswith('numofsmallies'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Number of pellets:", value=b)

        elif item.startswith('maxdamage'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Max damage potential:", value=b)

        elif item.startswith('falloffrange'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Weapon falloff range:", value=b)

        elif item.startswith('firerate'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Firerate:", value=b)

        elif item.startswith('isfalloff'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Weapon has falloff:", value=b, inline=True)

        elif item.startswith('isheadshot'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Weapon can headshot:", value=b, inline=True)

        elif item.startswith('heal'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Healing rate:", value=b)

        elif item.startswith('range'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Range:", value=b)

        elif item.startswith('radius'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Radius:", value=b)

        elif item.startswith('effect'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Effect:", value=b)

        elif item.startswith('duration'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Duration:", value=b)

        elif item.startswith('cool down'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Cooldown:", value=b)

        elif item.startswith('cast time'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Cast time:", value=b)

    return embed


def build_prim_embed(json_list):
    prim_title_string = ''

    for item in json_list:
        if item.startswith('primname'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_title_string += b

    prim_embed = discord.Embed(title=prim_title_string)

    for item in json_list:
        if item.startswith("primname"):
            continue
        elif item.startswith('primtype'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Weapon type:", value=b)

        elif item.startswith('primammo'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Weapon ammo:", value=b)

        elif item.startswith('primreload'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Reload time:", value=b)

        elif item.startswith('primdamage'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Weapon damage:", value=b)

        elif item.startswith('numofsmallies'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Number of pellets:", value=b)

        elif item.startswith('maxdamage'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Max damage potential:", value=b)

        elif item.startswith('falloffrange'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Weapon falloff range:", value=b)

        elif item.startswith('firerate'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Firerate:", value=b)

        elif item.startswith('isfalloff'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Weapon has falloff:", value=b, inline=True)

        elif item.startswith('isheadshot'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Weapon can headshot:", value=b, inline=True)

        elif item.startswith('heal'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Healing rate:", value=b, inline=True)

        elif item.startswith('range'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Range:", value=b)

        elif item.startswith('radius'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Radius:", value=b)

        elif item.startswith('effect'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Effect:", value=b)

        elif item.startswith('duration'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Duration:", value=b)

        elif item.startswith('cool down'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Cooldown:", value=b)

        elif item.startswith('cast time'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            prim_embed.add_field(name="Cast time:", value=b)

    return prim_embed


def build_secd_embed(json_list):
    secd_title_string = ''

    for item in json_list:
        if item.startswith('secdname'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_title_string += b

    secd_embed = discord.Embed(title=secd_title_string)

    for item in json_list:
        if item.startswith("secdname"):
            continue
        elif item.startswith('secdtype'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Weapon type:", value=b)

        elif item.startswith('secdammo'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Weapon ammo:", value=b)

        elif item.startswith('secdreload'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Reload time:", value=b)

        elif item.startswith('secddamage'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Weapon damage:", value=b)

        elif item.startswith('secdnumofsmallies'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Number of pellets:", value=b)

        elif item.startswith('secdmaxdamage'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Max damage potential:", value=b)

        elif item.startswith('secdfalloffrange'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Weapon falloff range:", value=b)

        elif item.startswith('secdfirerate'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Firerate:", value=b)

        elif item.startswith('secdisfalloff'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Weapon has falloff:", value=b, inline=True)

        elif item.startswith('secdisheadshot'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Weapon can headshot:", value=b, inline=True)

        elif item.startswith('secdheal'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Healing rate:", value=b, inline=True)

        elif item.startswith('secdrange'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Range:", value=b)

        elif item.startswith('secdradius'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Radius:", value=b)

        elif item.startswith('secdeffect'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Effect:", value=b)

        elif item.startswith('secdduration'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Duration:", value=b)

        elif item.startswith('secdcool down'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Cooldown:", value=b)

        elif item.startswith('secdcast time'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            secd_embed.add_field(name="Cast time:", value=b)

    return secd_embed


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
        message_string = message.content
        error = False
        try:
            a, b = message_string.split(' ')
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

        message_string = message.content
        error = False
        try:
            a, b = message_string.split(' ')
        except ValueError:
            await client.send_message(message.channel, 'Please input string to be searched as first parameter')
            error = True

        if not error:
            s = requests.Session()

            url = 'http://overwatch.wikia.com/api.php'

            title = b

            params_ability = {
                'action': 'query',
                'titles': title,
                'prop': 'revisions',
                'rvprop': 'content',
                'format': 'json'
            }

            r = s.get(url=url, params=params_ability)
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

                    print("Got past split")

                    a_list = a.split('\n')
                    a_list.pop(0)
                    a_list.pop()
                    a_list.pop()

                    b_list = []

                    for item in a_list:

                        item = item.replace('|', ' ')
                        item = item.replace('{', '')
                        item = item.replace('}', '')
                        item = item.replace('[', '')
                        item = item.replace(']', '')
                        item = item.replace('Texttip', '')
                        item = item.replace('texttip', '')
                        item = item.replace('/Texttip', '')
                        item = item.replace('/texttip', '')

                        regex = r'\<.*?\>'

                        item_regexed = re.sub(regex, '', item)

                        if item_regexed is not None and item_regexed != '':
                            b_list.append(item_regexed[2:])

                    image_name = search_image_name(b_list)

                    if image_name is not None and image_name is not '':
                        s = requests.Session()

                        url = 'http://overwatch.wikia.com/api.php'

                        params_image = {
                            'action': 'query',
                            'list': 'allimages',
                            'ailimit': '1',
                            'aifrom': image_name,
                            'aiprop': 'url',
                            'format': 'json'
                        }

                        r = s.get(url=url, params=params_image)
                        image_data = r.json()

                        try:
                            filtered_data = image_data['query']['allimages'][0]['url']
                            image_url = str(filtered_data)
                        except KeyError:
                            image_url = None

                        prim = False
                        secd = False

                        for item in b_list:
                            if item.startswith("prim"):
                                prim = True
                            elif item.startswith("secd"):
                                secd = True

                        if prim and secd:
                            prim_list = []
                            secd_list = []
                            main_list = []

                            for item in b_list:
                                if not (not item.startswith('image') and not
                                        item.startswith('name')) or item.startswith('description'):
                                    main_list.append(item)

                                elif item.startswith('secd'):
                                    secd_list.append(item)

                                elif item is not None and item != '':
                                    prim_list.append(item)

                            main_embed = build_embed(main_list, image_url)
                            prim_embed = build_prim_embed(prim_list)
                            secd_embed = build_secd_embed(secd_list)

                            await client.send_message(message.channel, embed=main_embed)
                            await client.send_message(message.channel, embed=prim_embed)
                            await client.send_message(message.channel, embed=secd_embed)
                        else:
                            c_list = []

                            for item in b_list:
                                item = item.replace('prim', '')
                                item = item.replace('secd', '')
                                if item is not None and item != '':
                                    c_list.append(item)

                            built_embed = build_embed(b_list, image_url)

                            await client.send_message(message.channel, embed=built_embed)

                except ValueError:
                    await client.send_message(message.channel,
                                              'Couldn\'t find a page with an ability description by that '
                                              'name. (All names are case-sensitive)')

    elif message.content.lower().startswith('wh!shutdown') or message.content.startswith('wh!stop'):
        await client.send_message(message.channel, 'Shutting down')
        await client.logout()


client.run('NTAyNDEyNTI2OTkxMTc5Nzg2.DqnjxA.tYxjA-AGeAg7XmuhYg-Ov6jA5Zk')
