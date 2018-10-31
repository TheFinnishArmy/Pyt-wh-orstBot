import command_processor as command


async def process(message, owner_id, client):
    if message.author is client.user.id:
        return
    if not message.content.startswith('wh!'):
        return

    message_string = message.content.lower()

    await command.process(message, message_string, owner_id, client)
