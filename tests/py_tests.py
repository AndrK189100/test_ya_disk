import pytest
import requests
from YaUploadFiles import YaUploadFiles

token = '**************************************************'
wrong_token = 'AQAAAAAAE'
url = 'https://cloud-api.yandex.net/v1/disk/resources'
path = 'disk:/andrew_pd-fpy_py-51'


def test_create_folder():
    ya = YaUploadFiles(token)
    assert ya.create_folder() == {'ok': 201}

    params = {'path': path, 'limit': '0'}
    headers = {'Authorization': token}
    resp = requests.get(url=url, params=params, headers=headers)
    assert resp.status_code == 200
    assert resp.json()['name'] == 'andrew_pd-fpy_py-51'


def test_not_authorized():
    ya = YaUploadFiles(wrong_token)
    assert ya.create_folder() == {'error': 401}


@pytest.fixture(scope='session', autouse=True)
def cleanup(request):
    def remove_folder():
        params = {'path': path, 'permanently': 'true'}
        headers = {'Authorization': token}
        requests.delete(url=url, params=params, headers=headers)

    request.addfinalizer(remove_folder)
