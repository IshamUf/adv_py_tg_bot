import asyncio
from pyrogram import Client
from config import pyr_api_id, pyr_api_hash

api_id = pyr_api_id
api_hash = pyr_api_hash


async def create_link(chat_id):
    async with Client("my_account", api_id, api_hash) as app:
        link = await app.create_chat_invite_link(chat_id, member_limit=1)
        return link.invite_link


async def send_chat_link_to_user(chat_id, user_id):  # Затестить ситуацию когда меня нет в контактах
    async with Client("my_account", api_id, api_hash) as app:
        link = await app.create_chat_invite_link(chat_id, member_limit=1)
        await app.send_message(user_id, link.invite_link)


async def get_chat_info(chat_id):
    async with Client("my_account", api_id, api_hash) as app:
        info = await app.get_chat(chat_id)
        return info.title


async def delete_user_from_chat(user_id, chat_id):
    async with Client("my_account", api_id, api_hash) as app:
        await app.ban_chat_member(chat_id, user_id)


async def add_user_to_chat(user_id, chat_id):
    async with Client("my_account", api_id, api_hash) as app:
        await app.add_chat_members(chat_id, user_id)


async def create_super_group(name: str, description: str):
    async with Client("my_account", api_id, api_hash) as app:
        await app.create_supergroup(name, description)


async def check_user_in_chat(chat_id, user_id):
    async with Client("my_account", api_id, api_hash) as app:
        async for member in app.get_chat_members(chat_id):
            if member.user.id == user_id:
                return True
            else:
                return False


async def get_users_info_from_chat(chat_id):
    dct = {}
    async with Client("my_account", api_id, api_hash) as app:
        async for member in app.get_chat_members(chat_id):
            if not (str(member.status).split('.')[-1] == 'OWNER'):
                dct[member.user.id] = member.user.first_name

    return dct


