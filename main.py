import json
import os.path
import time

import GetVkPhotos
import YaUploadFiles


def create_json(photos: list):
    photos_json = []
    for photo in photos:
        photos_json.append({'file_name': photo['name'], 'size': photo['size']})

    with open('result.json', 'w') as f:
        json.dump(photos_json, f, indent=4)


def read_token_file(path_file: str):
    with open(path_file, 'r', encoding='UTF-8') as f_token:
        return f_token.readline().split('\n')[0]


def get_photos():
    api_v = '5.131'
    user_id = input('Введите ID пользователя Вконтакте или короткое имя(Screen_Name): ')
    # user_id = '552934290'
    vk_token = input(f'Введите токен Вконтакте или путь к содержащему его файлу.\n Файл должен содержать одну строку '
                     f'являющуюся токеном.\nПуть: ')
    album_id = input('Введите ID альбома пользователя: ')
    photos_count = input('Введите количество фотографий: ')

    print('Работаем)')
    if os.path.isfile(vk_token):
        vk_token = read_token_file(vk_token)
    with open('log.txt', mode='w', encoding='UTF-8') as log:
        try:
            vk_user = GetVkPhotos.GetVkPhotos(vk_token, user_id)
            log.write('Пользователь найден\n\n')
        except:
            print('Пользователь не найден.')
            log.write('Пользовтель не найден.\nпрограмма завершена\n\n')
            exit(0)

        photos = vk_user.get(album_id, photos_count)
        if type(photos) is list:
            log.write('Ссылки на фотографии профиля пользователя получены.\n\n')
            print('Фотографии получены')
            return photos
        else:
            print('Не удалось получить фотографии')
            log.write('Ошибка загрузки фотографий.\nПрограмма завершена\n')
            exit(0)


def upload_photos(photos: list):
    ya_token = input(f'Введите токен Яндекс Диска или путь к содержащему его файлу.\n Файл должен содержать одну строку'
                     f'являющуюся токеном.\nПуть: ')

    print('Ожидайте')

    # ya_token = 'ya_token.txt'
    if os.path.isfile(ya_token):
        ya_token = read_token_file(ya_token)

    for i in range(len(photos) - 1):
        j = i + 1
        count = 1
        while j != len(photos):
            if photos[i]['name'] == photos[j]['name']:
                photos[j]['name'] = photos[j]['name'] + '(' + str(count) + ')'
                count += 1
            j += 1
    for photo in photos:
        photo['name'] = photo['name'] + '.jpg'

    ya_disk = YaUploadFiles.YaUploadFiles(ya_token)

    with open('log.txt', mode='a', encoding='UTF-8') as log:
        result = ya_disk.create_folder()
        if 'error' in result:
            print(f'Не удалось создать каталог. Status code: {result["error"]}')
            log.write('Не удалось создать каталог на Яндекс диске.\nПрограмма завершена\n\n')
            exit(0)

        downloaded_files = []

        if result['ok'] == 409:
            uploaded_files = ya_disk.get_files()
            if 'error' in uploaded_files:
                print(f'Не удалось получить список загруженных файлов. Status code: {uploaded_files["error"]}')
                log.write('Не удалось получить файлы с Яндекс диска.\nПрограмма завершена\n\n')
                exit(0)

            for photo in photos:
                if photo['name'] in uploaded_files:
                    photo['name'] = photo['name'].replace('.', '_' + str(time.time()) + '.')

        for photo in photos:
            result = ya_disk.upload_files(photo['url'], photo['name'])
            if 'ok' in result:
                downloaded_files.append(f'Файл {photo["name"]} загружен. Status code: {result["ok"]}')
                log.write(f'Файл {photo["name"]} загружен. Status code: {result["ok"]}\n')
            else:
                downloaded_files.append(f'Ошибка загрузки файла {photo["name"]}. Status code: {result["error"]}')
                log.write(f'Ошибка загрузки файла {photo["name"]}. Status code: {result["error"]}\n')
        log.write('\n')
    print('Загрузка файлов на Яндекс диск завершена.')
    return downloaded_files


if __name__ == '__main__':
    vk_photos = get_photos()
    upload_photos(vk_photos)
    create_json(vk_photos)

    print('Информация по работе программы находится в файлах result.json и log.txt\n'
          'рабочего каталога программы')
