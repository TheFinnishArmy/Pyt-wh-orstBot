import command_processor as command


async def process(message, client):
    if message.author is client.id:
        return
    if message.content.startswith('wh!'):
        return

    message_string = message.content.lower()

    command.process(message, message_string, client)