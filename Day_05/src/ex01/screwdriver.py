from http.client import responses
from urllib.parse import urljoin

import requests
import argparse

url='http://127.0.0.1:8888/'

def list_of_files():
    response=requests.get(urljoin(url, 'files'))

    if response.status_code == 200:
        print('Список файлов:')
        for file in response.json():
            print(file)
    else:
        print('Произошла ошибка:', responses[response.status_code])


def upload(file):
    requests.post(url, files={'file': open(file, 'rb')})


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Screwdriver')
    subparsers = parser.add_subparsers(dest='action')

    upload_parser = subparsers.add_parser('upload', help='Загрузить локальный аудиофайл на сервер')
    upload_parser.add_argument('file_path', help='Путь к локальному аудиофайлу')

    list_parser = subparsers.add_parser('list', help='Вывести имена всех файлов на сервере')

    args = parser.parse_args()

    if args.action == 'upload':
        file_path = args.file_path
        upload(file_path)

    elif args.action == 'list':
        list_of_files()
