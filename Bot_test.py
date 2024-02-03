from aiogram.fsm.storage.redis import RedisStorage

from config import TOKEN, corp_mail
from api_1c_func import (phone_check_uit,
                         email_check_uit,
                         get_role_dep,
                         get_user_tg_id_tel,
                         get_user_tg_id_email)

from keyboards import (get_keyboard_yes_no,
                       get_keyboard_tel_email,
                       get_keyboard_yes_no_email,
                       get_keyboard_emailnotinbase,
                       get_keyboard_main_menu,
                       get_keyboard_main_menu_admin,
                       get_keyboard_test_admin,
                       generate_chats_buttons_adduser,
                       get_keyboard_yes_no_add_user,
                       get_keyboard_tel_email_add_user,
                       get_keyboard_yes_no_email_add_user,
                       generate_users_buttons_from_chat)
import re

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from json_func import write_tel_id, read_data, check_user, check_admin
from filter import chat_filter
from pyr_func import (create_link,
                      check_user_in_chat,
                      get_chat_info,
                      send_chat_link_to_user,
                      get_users_info_from_chat,
                      delete_user_from_chat)

from aioredis import Redis

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
redis = Redis()

dp = Dispatcher(storage=RedisStorage(redis=redis))


class AccountCheck(StatesGroup):
    waiting_phone = State()
    phone_gotten = State()
    waiting_email = State()
    email_gotten = State()


class AddUserToChat(StatesGroup):
    waiting_phone = State()
    phone_gotten = State()
    waiting_email = State()
    email_gotten = State()


class AdminPanel(StatesGroup):
    addUserDirect = State()
    deleteUserFromChat = State()
    deleteUserSelected = State()
    createNewChat = State()
    deleteChatDirect = State()
    changeDirectSettings = State()




# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear() # Неуверен нужно ли второй раз удалять стате пользователя?
    if not check_user(message.chat.id):
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text="Отправить контакт", request_contact=True)
        )
        await message.answer("Привет, поделись своим контактом, нажми на кнопку ниже или напиши свой номер телефона",
                             reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(AccountCheck.waiting_phone)
    else:
        if check_admin(message.chat.id):
            await message.answer("Привет, ты главный админ",
                                 reply_markup=get_keyboard_main_menu_admin())
        else:
            await message.answer("Привет, не админ",
                                 reply_markup=get_keyboard_main_menu())

'''
Спрашиваем правильность телефона, которым поделились контактом
'''


@dp.message(F.contact, AccountCheck.waiting_phone)
async def get_contact_button(message: types.Message, state: FSMContext):
    if message.contact.user_id == message.chat.id:
        await message.answer(f"Ваш номер телефона: {message.contact.phone_number} ?",
                             reply_markup=get_keyboard_yes_no())
        await state.set_state(AccountCheck.phone_gotten)
    else:
        await message.answer("Шалун отправил не свой контакт")

'''
Парсим правильность набора талефона
'''


@dp.message(F.text, AccountCheck.waiting_phone)
async def get_contact_writing(message: types.Message, state: FSMContext):
    str_number = ''
    lst_number = re.findall(r'\d', message.text.strip())
    for i in lst_number:
        str_number += i
    if len(str_number) == 11:
        await message.answer(f"Ваш номер телефона: {str_number} ?", reply_markup=get_keyboard_yes_no())
        await state.set_state(AccountCheck.phone_gotten)
    else:
        await message.answer(f"Вы ввели не правильный номер телефона: {str_number}")


@dp.callback_query(F.data.startswith("Tel_"), AccountCheck.phone_gotten)
async def phone_checker(callback: types.CallbackQuery, state: FSMContext):
    phone = callback.message.text.split(' ')[-2]
    answer = callback.data.split("_")[1]
    if answer == 'no':
        await callback.message.edit_text('Введите номер повторно')
        await state.set_state(AccountCheck.waiting_phone)
    elif answer == 'yes':
        checker = phone_check_uit(phone[1:])
        if not checker:
            await callback.message.edit_text('Вашего номера нет в базе, вы можете ввести номер телефона повторно '
                                             'или ввести рабочую почту', reply_markup=get_keyboard_tel_email())
        else:
            await callback.message.edit_text('Ваш номер найден в базе')
            await state.clear()
            write_tel_id(callback.message.chat.id)
            await cmd_start(callback.message, state)

'''
Выбор между повторным вводом телефона или емаила
'''


@dp.callback_query(F.data.startswith("TelorEmail_"), AccountCheck.phone_gotten)
async def phone_or_email(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]
    if answer == 'tel':
        await callback.message.edit_text('Введите номер повторно')
        await state.set_state(AccountCheck.waiting_phone)
    elif answer == 'email':
        await callback.message.edit_text('Введите свою рабочую почту')
        await state.set_state(AccountCheck.waiting_email)

'''
Получили емаил и проводим проверку
'''

@dp.message(F.text, AccountCheck.waiting_email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text.strip()
    work_file = corp_mail
    if work_file in email:
        await message.answer(f'Подтвердите ваш email: {email}', reply_markup=get_keyboard_yes_no_email())
        await state.set_state(AccountCheck.email_gotten)
    else:
        await message.answer(f'Ваш email не соответствует фильтру: {email} \n Введите рабочую почту') # тут нужна кнопка отмены


@dp.callback_query(F.data.startswith("email_"), AccountCheck.email_gotten)
async def email_checker(callback: types.CallbackQuery, state: FSMContext):
    email = callback.message.text.split(' ')[-1]
    answer = callback.data.split("_")[1]
    if answer == 'no':
        await callback.message.edit_text('Введите рабочую почту повторно')
        await state.set_state(AccountCheck.waiting_email)
    elif answer == 'yes':
        checker = email_check_uit(email)
        if not checker:
            await callback.message.edit_text(f'Вашей почты нет в базе {email}, вы можете ввести рабочую почту повторно'
                                             , reply_markup=get_keyboard_emailnotinbase())
        else:
            await callback.message.edit_text('Ваша почта найдена в базе')
            await state.clear()
            write_tel_id(callback.message.chat.id)
            await cmd_start(callback.message, state)


@dp.callback_query(F.data.startswith("emailnotinbase_"), AccountCheck.email_gotten)
async def phone_or_email_st_email_gotten(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]
    if answer == 'onemore':
        await callback.message.edit_text('Введите рабочую почту повторно')
        await state.set_state(AccountCheck.waiting_email)
    elif answer == 'support':
        await callback.message.edit_text('Свяжитесь с поддержкой')  # тут заканчивается, надо связаться с поддержкой
        await state.clear()


'''
Описывается логика добавления в чат по нажатию кнопки добавиться в чат
'''


@dp.callback_query(F.data.startswith("main_add"))
async def add_to_the_chats(callback: types.CallbackQuery):
    role, dep = get_role_dep(callback.message.chat.id)
    chats = chat_filter(dep, role)
    if not chats:
        await callback.message.answer('На данный момент ваши чаты еще не созданы, обратитесь в техническую поддержку')
    else:
        for chat in chats:
            if not check_user_in_chat(chat, callback.message.chat.id):
                link = await create_link(chat)
                await callback.message.answer(link)
            else:
                chat_name = await get_chat_info(chat)
                await callback.message.answer(f'Вы уже присутствуете в чате {chat_name}')
        await callback.message.answer('Нажмите /start для перехода в главное меню')

'''
Тут заканчивается функционал кнопки добавление в чат, далее описывается функционал админки
'''


@dp.callback_query(F.data.startswith("main_admin"))
async def admin_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Это админ меню', reply_markup=get_keyboard_test_admin())


async def admin_menu_answer(callback: types.CallbackQuery):
    await callback.message.answer('Это админ меню', reply_markup=get_keyboard_test_admin())


@dp.callback_query(F.data.startswith("admin_"))
async def admin_menu_action(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()  # тут нужно ли вообще тут это
    answer = callback.data.split("_")[1]
    if answer == 'adduser':  # Тут нужно подумать , чтобы показывались именно чаты, в которых пользователь админ
        await callback.message.edit_text('Доступные чаты:', reply_markup=generate_chats_buttons_adduser())
        await state.set_state(AdminPanel.addUserDirect)
    elif answer == 'deleteUser':
        await callback.message.edit_text('Доступные чаты:', reply_markup=generate_chats_buttons_adduser())
        await state.set_state(AdminPanel.deleteUserFromChat)
    elif answer == 'createChat':
        print(f'Ненаписанная кнопка {answer}')
    elif answer == 'deleteChat':
        print(f'Ненаписанная кнопка {answer}')
    elif answer == 'changeSettings':
        print(f'Ненаписанная кнопка {answer}')


'''
Тут писывается функицонал добаление в чат админом
'''


@dp.callback_query(F.data, AdminPanel.addUserDirect)
async def add_user_to_chat(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(chat_id=callback.data)
    await state.set_state(AddUserToChat.waiting_phone)
    await callback.message.edit_text('Напиши номер телефона или отправь контакт')


@dp.message(F.contact, AddUserToChat.waiting_phone)
async def get_contact_add_user(message: types.Message, state: FSMContext):
    await message.answer(f"Номер телефона пользователя: {message.contact.phone_number} ?",
                         reply_markup=get_keyboard_yes_no_add_user())
    await state.set_state(AddUserToChat.phone_gotten)


@dp.message(F.text, AddUserToChat.waiting_phone)
async def get_contact_writing_add_user(message: types.Message, state: FSMContext):
    str_number = ''
    lst_number = re.findall(r'\d', message.text.strip())
    for i in lst_number:
        str_number += i
    if len(str_number) == 11:
        await message.answer(f"Номер телефона пользователя: {str_number} ?",
                             reply_markup=get_keyboard_yes_no_add_user())
        await state.set_state(AddUserToChat.phone_gotten)
    else:
        await message.answer(f"Вы ввели не правильный номер телефона: {str_number}, введите номер повторно:")


@dp.callback_query(F.data.startswith("Teladduser_"), AddUserToChat.phone_gotten)
async def phone_checker(callback: types.CallbackQuery, state: FSMContext):
    phone = callback.message.text.split(' ')[-2]
    answer = callback.data.split("_")[1]
    if answer == 'no':
        await callback.message.edit_text('Введите номер повторно')
        await state.set_state(AddUserToChat.waiting_phone)
    elif answer == 'yes':
        checker_uit = phone_check_uit(phone[1:])
        if not checker_uit:
            await callback.message.edit_text('Написанного номера нет в базе, вы можете ввести номер телефона повторно '
                                             'или ввести рабочую почту', reply_markup=get_keyboard_tel_email_add_user())
        else:
            await callback.message.edit_text('Номер пользователя найден в базе')
            user_id = get_user_tg_id_tel(phone[1:])
            data = await state.get_data()
            chat_id = data["chat_id"]
            await state.clear()
            checker_tg = await check_user_in_chat(chat_id, user_id)
            if not checker_tg:
                await send_chat_link_to_user(chat_id, user_id)
                await callback.message.edit_text('Сотруднику была отправлена ссылка приглашение')
            else:
                await callback.message.edit_text('Пользователь уже состоит в выбранном чате.')  # Проверить что будет если челие уже есть в чате
            await admin_menu_answer(callback)
'''
Заканчивается проверка телефона и предлагается проверить маил, 
должен запуститься функицонал отправки сообщерия с линками
'''


@dp.callback_query(F.data.startswith("TelorEmailadduser_"), AddUserToChat.phone_gotten)
async def phone_or_email_add_user(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]
    if answer == 'tel':
        await callback.message.edit_text('Введите номер повторно')
        await state.set_state(AddUserToChat.waiting_phone)
    elif answer == 'email':
        await callback.message.edit_text('Введите рабочую почту пользователя')
        await state.set_state(AddUserToChat.waiting_email)


@dp.message(F.text, AddUserToChat.waiting_email)
async def get_email_add_user(message: types.Message, state: FSMContext):
    email = message.text.strip()
    work_file = corp_mail
    if work_file in email:
        await message.answer(f'Подтвердите ваш email: {email}', reply_markup=get_keyboard_yes_no_email_add_user())
        await state.set_state(AddUserToChat.email_gotten)
    else:
        await message.answer(f'Ваш email не соответствует фильтру: {email} \n Введите рабочую почту')


@dp.callback_query(F.data.startswith("emailadduser_"), AddUserToChat.email_gotten)
async def email_checker_add_user(callback: types.CallbackQuery, state: FSMContext):
    email = callback.message.text.split(' ')[-1]
    answer = callback.data.split("_")[1]
    if answer == 'no':
        await callback.message.edit_text('Введите рабочую почту повторно')
        await state.set_state(AddUserToChat.waiting_email)
    elif answer == 'yes':
        checker_uit = email_check_uit(email)
        if not checker_uit:
            await callback.message.edit_text(f'Почты сотрудника нет в базе {email}, '
                                             f'вы можете ввести рабочую почту повторно'
                                             , reply_markup=get_keyboard_emailnotinbase())
        else:
            user_id = get_user_tg_id_email(email)
            data = await state.get_data()
            chat_id = data["chat_id"]
            await state.clear()
            checker_tg = await check_user_in_chat(chat_id, user_id)
            if not checker_tg:
                await send_chat_link_to_user(chat_id, user_id)
                await callback.message.edit_text('Сотруднику была отправлена ссылка приглашение')
            else:
                await callback.message.edit_text('Пользователь уже состоит в выбранном чате.') # Проверить что будет если челие уже есть в чате
            await admin_menu_answer(callback)


@dp.callback_query(F.data.startswith("emailnotinbase_"), AddUserToChat.email_gotten)
async def phone_or_email(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[1]
    if answer == 'onemore':
        await callback.message.edit_text('Введите рабочую почту повторно')
        await state.set_state(AddUserToChat.waiting_email)
    elif answer == 'support':
        await callback.message.edit_text('Свяжитесь с поддержкой') # скинуть ссылку на поддержку
        await state.clear()

'''
Заканчивается проверка майл или предлагается связаться с поддержкой, 
должен запуститься функицонал отправки сообщерия с линками
'''


'''
Начинаем писать функционал для удаления пользователя из чатов
'''


@dp.callback_query(F.data, AdminPanel.deleteUserFromChat)
async def choose_user_to_delete(callback: types.CallbackQuery, state: FSMContext):  # Тут нужен список всех чатов
    await state.set_state(AdminPanel.deleteUserSelected)
    users_dct = await get_users_info_from_chat(callback.data)
    await callback.message.edit_text(f'Выберите пользователя из чата',
                                     reply_markup=generate_users_buttons_from_chat(users_dct, callback.data))


@dp.callback_query(F.data, AdminPanel.deleteUserSelected) # Тут вообще все максимально нужно проверить
async def delete_selected_user_from_chat(callback: types.CallbackQuery, state: FSMContext):
    user_id, chat_id = callback.data.split('_')  # Разделяем дату из кнопки на чат id и юсер id
    await delete_user_from_chat(user_id, chat_id)
    await callback.message.edit_text(f'Пользователь был удален')
    await state.clear()
    await admin_menu_answer(callback)


'''
Закончили писать функционал для удаления пользователя из чатов
'''

# await state.update_data(chat_id=callback.data)
# await state.set_state(AddUserToChat.waiting_phone)
# await callback.message.edit_text('Напиши номер телефона или отправь контакт')
# сделать кнопки назад, где это нужно в админ понеле


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())