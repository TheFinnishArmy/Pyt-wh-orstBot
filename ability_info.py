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
    message_string = message_string.replace('wh!abilityinfo', '')
    message_string = message_string.strip()
    message_string = message_string.replace(' ', '_')
    message_string = message_string.title()

    if message_string is '':
        raise ValueError('Couldn\'t split message')

    b = message_string

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

    try:
        filtered_data1 = data['query']['pages']
        filtered_data2 = filtered_data1[next(iter(filtered_data1))]['revisions'][0]['*']
        filtered_data_string = str(filtered_data2)
    except KeyError:
        raise KeyError()

    try:
        split_list = filtered_data_string.split('</onlyinclude>')
        a = split_list[0]

    except ValueError:
        raise AttributeError('Couldn\'t find ability template')

    else:
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
            item_regexed_stripped = item_regexed.strip()

            if item_regexed_stripped is not None and item_regexed_stripped != '':

                if item_regexed_stripped.startswith('image') or item_regexed_stripped.startswith('name') \
                        or item_regexed_stripped.startswith('description'):

                    main_list.append(item_regexed_stripped)

                elif item_regexed_stripped.startswith('secd'):
                    item_regexed_stripped = item_regexed_stripped.replace('secd', '')
                    secd_list.append(item_regexed_stripped)

                else:
                    item_regexed_stripped = item_regexed_stripped.replace('prim', '')
                    prim_list.append(item_regexed_stripped)

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
