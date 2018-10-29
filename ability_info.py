import requests
import re

import embed_builder


def search_image_name(b_list):
    for item in b_list:
        if item.startswith('image'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            return b

    return None


def build(message_string):
    try:
        a, b = message_string.split(' ')
    except ValueError:
        raise ValueError('Couldn\'t split message')

    b = b.title()

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
        raise KeyError()

    if not error:
        try:
            a, b = filtered_data_string.split('</onlyinclude>')

            a_list = a.split('\n')
            a_list.pop(0)
            a_list.pop()
            a_list.pop()

            prim_list = []
            secd_list = []
            main_list = []

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
                item_regexed = item_regexed[2:]

                if item_regexed is not None and item_regexed != '':

                    if item_regexed.startswith('image') or item_regexed.startswith('name') \
                            or item_regexed.startswith('description'):

                        main_list.append(item_regexed)

                    elif item_regexed.startswith('secd'):
                        item_regexed = item_regexed.replace('secd', '')
                        secd_list.append(item_regexed)

                    else:
                        item_regexed = item_regexed.replace('prim', '')
                        prim_list.append(item_regexed)

            image_url = None
            image_name = search_image_name(main_list)

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

            main_embed = embed_builder.build_embed(main_list, image_url)
            prim_embed = embed_builder.build_embed(prim_list)
            if secd_list:
                secd_embed = embed_builder.build_embed(secd_list)
            else:
                secd_embed = None

            return {'main_embed': main_embed, 'prim_embed': prim_embed, 'secd_embed': secd_embed}

        except ValueError:
            raise AttributeError('Couldn\'t find ability template')