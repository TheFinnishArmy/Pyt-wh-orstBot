import discord


def build_embed(json_list, image_url=None):
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

    if description_string != '':
        embed = discord.Embed(title=title_string, description=description_string)
    else:
        embed = discord.Embed(title=title_string)

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

        elif item.startswith('cooldown'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Cooldown:", value=b)

        elif item.startswith('casttime'):
            try:
                a, b = item.split('=')
            except ValueError:
                continue
            embed.add_field(name="Casttime:", value=b)

    return embed
