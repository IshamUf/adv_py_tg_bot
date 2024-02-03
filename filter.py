from json_func import read_data
#  Может быть несколько ролей, одна роль несолько департаментов?




def chat_filter(dep_list, role_list):
    chats = read_data('test_chats.json')
    res = []
    count = 0
    for dep in dep_list:
        for role in role_list:
            for i in chats:
                count += 1
                if dep in i['dep'] and role in i['roles']:
                    res.append(i['chat_id'])
    return set(res)




# print(chat_filter(['Саратов', "Питер"], ['Сотрудник финансового департамента']))