import command_processor as command


async def process(message, is_owner, client):
    if message.author is client.user.id:
        return
    if not message.content.startswith('wh!'):
        return

    message_string = message.content.lower()

    await command.process(message, message_string, is_owner, client)
