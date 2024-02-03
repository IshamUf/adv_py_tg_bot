from json_func import read_data


def phone_check_uit(tel):
    data = read_data('users1c.json')
    for user in data:
        if user['tel_num'] == tel:
            return True
    return False


def email_check_uit(email):
    data = read_data('users1c.json')
    for user in data:
        if user['email'] == email:
            return True
    return False


def get_user_tg_id_tel(tel):
    data = read_data('users1c.json')
    for user in data:
        if user['tel_num'] == tel:
            return user['id']
    return False


def get_user_tg_id_email(email):
    data = read_data('users1c.json')
    for user in data:
        if user['email'] == email:
            return user['id']
    return False


def get_role_dep(id_):
    user_role = []
    user_dep = []
    users = read_data("users1c.json")
    for i in users:
        if id_ == i['id']:
            user_role = i['role']
            user_dep = i['department']
    return user_role, user_dep




