import time

import requests

# AUTHORISE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
ACCESS_TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'
USER_ID = '5030613',  # 25359024


# сделать запрос к API
def get_api_data(method, params):
    api_link = 'https://api.vk.com/method/{}'.format(method)
    response = requests.get(api_link, params=params)
    return response


def get_groups(user_id, params):
    params['user_id'] = user_id
    params['count'] = 1000
    params['extended'] = 1
    groups = get_api_data('groups.get', params)
    print('*')

    return groups


def write_json_data(filename, text):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(text)


def main():
    params = {
        'access_token': ACCESS_TOKEN,
        'v': VERSION,
        'user_id': USER_ID,
        'fields': 'name',
    }

    friends = get_api_data('friends.get', params)
    groups = get_groups(USER_ID, params)

    # составляем список из словарей, каждый из которых - данные о друге
    valid_friends = [fr for fr in friends.json()['response']['items'] if 'deactivated' not in fr]
    my_groups = [(gr['id'], gr['name']) for gr in groups.json()['response']['items']]

    print(my_groups)

    # проходимся по id valid_friends и для каждого делаем запрос групп, объединяем это в один set  friends_groups
    friend_groups = set()
    i = 0
    len_friends = len(valid_friends)
    for friend in valid_friends:
        i += 1
        print('{} из {} пользователей'.format(i, len_friends))
        print('Обработка групп пользователя {} {}'.format(friend['first_name'], friend['last_name']))

        # print(friend['id']) id друга
        # получаем список групп друга
        while True:
            try:

                friend_groups_json = get_groups(friend['id'], params)
                # преобразовываем в список
                friend_groups_list = [(gr['id'], gr['name']) for gr in friend_groups_json.json()['response']['items']]
                # print(friend_groups_list)
                friend_groups = friend_groups.union(friend_groups_list)
            except KeyError:
                time.sleep(3)
                continue
            break
    print('Мои группы: ', my_groups)
    # print('Группы друзей', friend_groups)
    result_set = set(my_groups).difference(friend_groups)

    print('Итог:', result_set)
    # преобразуем итог в список с id
    result_groups_ids = [group_id for group_id, name in result_set]
    print('в виде списка: ', result_groups_ids)
    # для финального результата пишем в формате json
    result_groups_json = [gr for gr in groups.json()['response']['items'] if gr['id'] in result_groups_ids]
    print(result_groups_json)
    # пишем в файл
    write_json_data('groups.json', str(result_groups_json))


main()
