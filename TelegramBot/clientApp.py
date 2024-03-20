import random
from config import*
from telethon.sync import TelegramClient

client = TelegramClient('cocks', API_ID, API_HASH)
actual_msgs = None

async def get_messages_async():
    chanell = await client.get_entity(CHANNEL_ID)
    global actual_msgs
    actual_msgs = await client.get_messages(entity=chanell)

def get_messages():
    chanell = client.get_entity(CHANNEL_ID)
    global actual_msgs
    actual_msgs = client.get_messages(entity=chanell)

async def get_random_message():
    print(len(actual_msgs))
    return random.choice([msg for msg in actual_msgs])

async def get_message_by_id(id):
    
    chanell = await client.get_entity(CHANNEL_ID)
    return await client.get_messages(entity=chanell,ids=id)

async def send_message(text,id):
    chat = await client.get_entity(CHAT_ID)
    await client.send_message(chat,message=text,reply_to=id)


    


