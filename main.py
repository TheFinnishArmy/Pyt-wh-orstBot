import discord
import command_preprocessor
import json

try:
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
except FileNotFoundError:
    print('You have to copy the example_config.json to a file named config.json and place in the required details.')
    exit(1)

try:
    token = str(data["token"])
    owner_id = str(data["OwnerID"])
except KeyError:
    print("config.json is malformed please fix the file structure or create it from scratch.")
    exit(1)


client = discord.Client()


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
    is_owner = False
    if message.author.id == owner_id:
        is_owner = True

    await command_preprocessor.process(message, is_owner, client)


client.run(token)
