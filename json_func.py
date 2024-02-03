import json


def write_tel_id(id_):
    lst = read_data('users.json')
    lst.append(id_)
    data = json.loads(str(json.dumps(lst)))
    with open('users.json', "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def read_data(filename: str):
    with open(filename, "r", encoding='utf-8') as file:
        return json.load(file)


def check_user(id_):  #  заменить временная функция
    data = read_data('users.json')
    if id_ in data:
        return True
    else:
        return False


def check_admin(id_):
    data = read_data('admins.json')
    if id_ in data:
        return True
    else:
        return False


def get_full_chat_list():
    chats = read_data('test_chats.json')
    lst = []
    for chat in chats:
        lst.append([chat['name'], chat['chat_id']])
    return lst
