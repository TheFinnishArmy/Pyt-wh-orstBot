from dailyprogrammer_challenges.easy import easy_main as easy
from dailyprogrammer_challenges.medium import medium_main as medium
from dailyprogrammer_challenges.hard import hard_main as hard


async def main(message, message_string, client):
    message_string = message_string.replace('wh!dp', '')
    message_string = message_string.strip()
    if message_string is '':
        await client.send_message(message.channel, 'This is the portal command for r/dailyprogrammer challenge '
                                                   'implementations '

                                                   ' \n There are 3 categories; Easy, Medium & Hard '

                                                   '\n The challenge list can be found here: '
                                                   '\n https://www.reddit.com/r/dailyprogrammer/wiki/challenges')
    else:
        if message_string.startswith('easy'):
            message_string.replace('medium', '')
            message_string.strip()
            if message_string is not '':
                easy.main(message, message_string, client)
            else:
                await client.send_message(message.channel, 'This is the portal command for the easy challenges')

        elif message_string.startswith('medium'):
            message_string.replace('medium', '')
            message_string.strip()
            if message_string is not '':
                medium.main(message, message_string, client)
            else:
                await client.send_message(message.channel, 'This is the portal command for the medium challenges')

        elif message_string.startswith('hard'):
            message_string.replace('medium', '')
            message_string.strip()
            if message_string is not '':
                hard.main(message, message_string, client)
            else:
                await client.send_message(message.channel, 'This is the portal command for the hard challenges')
        else:
            await client.send_message(message.channel, 'That is not a valid sub-category, valid options are;'
                                                       ' Easy, Medium & Hard')
