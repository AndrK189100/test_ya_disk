import requests


class GetVkPhotos:
    __api_url = 'https://api.vk.com/method/'
    def __init__(self, token: str, user_str: str,  api_v='5.131'):
        self.token = token
        self.api_v = api_v
        params = {'user_ids': user_str, 'access_token': self.token, 'v': self.api_v}
        user = requests.get(self.__api_url + 'users.get', params = params).json()
        if user['response']:
            self.user_id = user['response'][0]['id']
        else:
            raise ValueError("user not found")

    def get(self, album_id = 'profile', count = '1000'):

        max_sizes_photos = []
        params = {'owner_id': self.user_id, 'album_id': album_id, 'count': count, 'access_token': self.token,
                  'v': self.api_v, 'extended': '1'}
        resp = requests.get(url='https://api.vk.com/method/photos.get', params=params)

        if resp.status_code != 200:
            return {'error': resp.status_code}

        resp = resp.json()
        if 'error' in resp:
            return {'error': resp["error"]["error_code"]}

        for item in resp['response']['items']:
            item['sizes'].sort(key=lambda val: int(val['width']) * int(val['height']), reverse=True)
            max_sizes_photos.append({'size': item['sizes'][0]['height'] * item['sizes'][0]['width'],
                                     'name': str(item['likes']['count']), 'url': item['sizes'][0]['url']})

        return max_sizes_photos
