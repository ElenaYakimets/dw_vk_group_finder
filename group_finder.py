# -*- coding: utf-8 -*-
import time
import requests
import json


# сделать запрос к API
def get_api_data(api, method, params):
    response = dict()
    api_link = '{}{}'.format(api, method)
    while True:
        response = requests.get(api_link, params=params).json()
        print('*')
        if 'response' in response:
            return response['response']['items']
        else:
            error = response['error']['error_code']
            if error == 6:
                time.sleep(3)
                continue
            else:
                return response


# получить группы
def get_groups(api, user_id, common_params):
    params = {
        'user_id': user_id,
        'count': 1000,
        'extended': 1,
        'fields': 'members_count'
        }
    params.update(common_params)
    groups = get_api_data(api, 'groups.get', params)
    return groups


# получить друзей
def get_user_friends(api, common_params):
    while True:
        user_id = input('Введите id пользователя для анализа: ')
        params = {
            'user_id': user_id,
            'fields': 'name'
            }
        params.update(common_params)

        friends = get_api_data(api, 'friends.get', params)
        if 'error' in friends:
            print('Пользователь не найден. Повторите ввод')
            continue
        else:
            break
    # выбираем только неудаленных друзей
    valid_friends = [fr for fr in friends if 'deactivated' not in fr]
    return (user_id, valid_friends)


def read_json_file(filename):
    with open(filename, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return data


def write_json_data(filename, text):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(text)


def main():
    API_VK = 'https://api.vk.com/method/'
    CONFIG_PATH = 'config/configuration.json'

    # читаем настройки
    settings = read_json_file(CONFIG_PATH)[0]

    params = {
        'access_token': settings['access_token'],
        'v': settings['version']
        }

    user_friends = get_user_friends(API_VK, params)
    user_id, friends = user_friends
    groups = get_groups(API_VK, user_id, params)

    # составляем список из словарей, каждый из которых - данные о друге
    my_groups = [(gr['id'], gr['name']) for gr in groups]

    friend_groups_overall = set()
    len_friends = len(friends)
    # проходимся по id valid_friends и для каждого делаем запрос групп, объединяем это в один ses
    for i, friend in enumerate(friends):
        print('{} из {} пользователей'.format(i, len_friends))
        print('Обработка групп пользователя {} {}'.format(friend['first_name'], friend['last_name']))
        friend_groups_json = get_groups(API_VK, friend['id'], params)
        friend_groups_list = [(gr['id'], gr['name']) for gr in friend_groups_json]
        friend_groups_overall = friend_groups_overall.union(friend_groups_list)

    result_set = set(my_groups).difference(friend_groups_overall)

    # преобразуем итог в список с id
    result_groups_ids = [group_id for group_id, name in result_set]
    # для финального результата собираем список словарей с полями 'id', 'name', 'members_count'
    result_groups_json = [{k: v for k, v in gr.items() if (k in ['id', 'name', 'members_count'])} for gr in groups if gr['id'] in result_groups_ids]
    # пишем json в файл
    write_json_data('groups.json', str(result_groups_json))
    print('Обработано успешно, результат сохранен в файле groups.json')


if __name__ == "__main__":
    main()
