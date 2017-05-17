from urllib.parse import urlparse, urlencode
import requests
import pprint

# import vk

# AUTHORISE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
# APP_ID = '5944949'

# auth_data = {
#     'client_id': APP_ID,
#     'display': 'mobile',
#     'response_type': 'token',
#     'scope': 'friends,status,video,groups',
#     'v': VERSION
# }

# print('?'.join((AUTHORISE_URL, urlencode(auth_data))))


# token_url = 'https://oauth.vk.com/blank.html#access_token=16124c69865ccab515ec419b8188abe3fa2935b49ebec1ba8b2799f43dd67a3b4092359861cc0c430c370&expires_in=86400&user_id=25359024'

params = {
    'access_token': 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22',
    'v': VERSION,
    'user_id': '25359024',
    'fields': 'name',
    'extended': '1'
}


# сделать запрос к API
def get_api_data(method, params):
    api_link = 'https://api.vk.com/method/{}'.format(method)
    return requests.get(api_link, params=params)


groups = get_api_data('groups.get', params)
friends = get_api_data('friends.get', params)

# составляем список из словарей, каждый из которых - данные о друге
valid_friends = [fr for fr in friends.json()['response']['items'] if 'deactivated' not in fr]

# проходимся по id valid_friends и для каждого делаем запрос групп, объединяем это в один set  friends_groups

pprint.pprint(friends.json())
pprint.pprint(valid_friends)
