from aiogram import types
from json_func import get_full_chat_list


def get_keyboard_yes_no():
    buttons = [
        [
            types.InlineKeyboardButton(text="Да", callback_data="Tel_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="Tel_no")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_yes_no_email():
    buttons = [
        [
            types.InlineKeyboardButton(text="Подтверждаю", callback_data="email_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="email_no")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_yes_no_email_add_user():
    buttons = [
        [
            types.InlineKeyboardButton(text="Подтверждаю", callback_data="emailadduser_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="emailadduser_no")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_tel_email():
    buttons = [
        [
            types.InlineKeyboardButton(text="Номер телефона", callback_data="TelorEmail_tel"),
            types.InlineKeyboardButton(text="Рабочая почта", callback_data="TelorEmail_email")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_tel_email_add_user():
    buttons = [
        [
            types.InlineKeyboardButton(text="Номер телефона", callback_data="TelorEmailadduser_tel"),
            types.InlineKeyboardButton(text="Рабочая почта", callback_data="TelorEmailadduser_email")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_emailnotinbase():
    buttons = [
        [
            types.InlineKeyboardButton(text="Ввести повторно", callback_data="emailnotinbase_onemore"),
            types.InlineKeyboardButton(text="Связаться с поддержкой ", callback_data="emailnotinbase_support")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_main_menu_admin():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавиться в чаты", callback_data="main_add")
        ],
        [
            types.InlineKeyboardButton(text="Администрирование чатов", callback_data="main_admin")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_main_menu():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавиться в чаты", callback_data="main_add")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_chat_admin():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавиться в чаты", callback_data="main_add")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_hr_admin():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавиться в чаты", callback_data="main_add")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_test_admin():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавить пользователя в чат", callback_data="admin_adduser")
        ], [
            types.InlineKeyboardButton(text="Удалить пользователя из чата", callback_data="admin_deleteUser")
        ], [
            types.InlineKeyboardButton(text="Создать новый чат", callback_data="admin_createChat")
        ], [
            types.InlineKeyboardButton(text="Удалить чат", callback_data="admin_deleteChat")
        ], [
            types.InlineKeyboardButton(text="Изменить чат", callback_data="admin_changeSettings")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_chats_buttons_adduser():
    chats = get_full_chat_list()
    buttons = []
    if chats:
        for name, id_ in chats:
            buttons.append([types.InlineKeyboardButton(text=f"{name}", callback_data=f"{id_}")])
        buttons.append([types.InlineKeyboardButton(text=f"Назад", callback_data=f"main_admin")])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_users_buttons_from_chat(dct, chat_id):
    buttons = []
    if dct:
        for id_, name in dct.items():
            buttons.append([types.InlineKeyboardButton(text=f"{name}", callback_data=f"{id_}_{chat_id}")])
    buttons.append([types.InlineKeyboardButton(text=f"Назад", callback_data=f"main_admin")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_yes_no_add_user():
    buttons = [
        [
            types.InlineKeyboardButton(text="Да", callback_data="Teladduser_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="Teladduser_no")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard