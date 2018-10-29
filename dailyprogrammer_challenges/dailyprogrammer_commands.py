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

                                                   '\n If you want more options supply one of those as the first '
                                                   'argument')
    else:
        if message_string is 'easy':
            await client.send_message(message.channel, 'This is the portal command for the easy challenges')
            easy.main()
        elif message_string is 'medium':
            await client.send_message(message.channel, 'This is the portal command for the medium challenges')
            medium.main()
        elif message_string is 'hard':
            await client.send_message(message.channel, 'This is the portal command for the hard challenges')
            hard.main()
        else:
            await client.send_message(message.channel, 'That is not a valid sub-category, valid options are;'
                                                       ' Easy, Medium & Hard')
