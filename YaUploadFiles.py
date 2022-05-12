import requests


class YaUploadFiles:
    __path = 'disk:/andrew_pd-fpy_py-51/'
    __url = 'https://cloud-api.yandex.net/v1/disk/'
    def __init__(self, token: str):
        self.__token = token

    def create_folder(self):

        url = self.__url + 'resources'
        params = {'path': self.__path}
        headers = {'Authorization': self.__token}
        resp = requests.put(url=url, params=params, headers=headers)
        if (resp.status_code == 409) or (resp.status_code == 201):
            return {'ok': resp.status_code}
        else:
            return {'error': resp.status_code}

    def upload_files(self, file_url, file_name):

        url = self.__url + 'resources/upload'
        params = {'path': self.__path + file_name, 'url': file_url}
        headers = {'Authorization': self.__token}
        resp = requests.post(url, params = params, headers = headers)

        if resp.status_code != 202:
            return {'error': resp.status_code}
        else:
            return {'ok': resp.status_code}

    def get_files(self):
        url = self.__url + 'resources'
        params = {'path': self.__path, 'limit': '1000000'}
        headers = {'Authorization': self.__token}
        resp = requests.get(url, params = params, headers = headers)

        if resp.status_code != 200:
            return {'error': resp.status_code}
        else:
            file_names = []
            items = resp.json()['_embedded']['items']

            for item in items:
                file_names.append(item['name'])

            return file_names


