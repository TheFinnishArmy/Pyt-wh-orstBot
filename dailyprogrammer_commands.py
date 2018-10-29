async def main(message, message_string, client):
    message_string = message_string.replace('wh!dp', '')
    message_string = message_string.strip()
    if message_string is '':
        await client.send_messsage(message.channel, 'This is the portal command for r/dailyprogrammer challenge '
                                                    'implementations '
                                                    
                                                    ' \n There are 3 categories; Easy, Medium & Hard '
                                                    
                                                    '\n If you want more options supply one of those as the first '
                                                    'argument')
    else:
        if message_string is 'easy':
            await client.send_messsage(message.channel, 'This is the portal command for the easy challenges')
        elif message_string is 'medium':
            await client.send_messsage(message.channel, 'This is the portal command for the medium challenges')
        elif message_string is 'hard':
            await client.send_messsage(message.channel, 'This is the portal command for the hard challenges')
        else:
            await client.send_messsage(message.channel, 'That is not a valid sub-category, valid options are;'
                                                        ' Easy, Medium & Hard')