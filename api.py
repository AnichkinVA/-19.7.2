import json
import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    '''Библиотека содержит API запросы к приложению PetFriens'''
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    ################################################################################################

    def get_api_key(self, email: str, password: str) -> json:
        '''Метод отправляет get запрос к API сервера с e-mail и паролем в header запроса,
        возвращает статус-код запроса и секретный ключ в формате json либо виде текста'''

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        '''Метод отправляет get запрос к API сервера с секретным ключом в headers и пустым значением в
        filter и возвращает статус-код запроса и список всех питомцев в формате json. Значение 'my_pets
        в фильтре вернет всех питомцев пользователя.'''

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        '''Метод отправляет post запрос к API сервера, добавляет данные питомца из data на сайт,
        возвращает статус-код запроса и результат в формате json с информацией о питомце.'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        '''Метод отправляет post запрос к API сервера, добавляет данные питомца без фото из data на
        сайт, возвращает статус-код запроса и результат в формате json с информацией о питомце.'''

        headers = {
            'auth_key': auth_key['key'],
        }

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        '''Метод отправляет post запрос к API сервера, добавляет новое фото питомца, id которого
        указан, возвращает статус-код запроса и результат в формате json с информацией о питомце.'''

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        '''Метод отправляет put запррс к API сервера, изменяет данные питомца, id которого
        указан и возвращает код статуса запроса и измененные данные питомца в формате json'''
        headers = {
            'auth_key': auth_key['key'],
            'pet_id': pet_id
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        '''Метод отправляет delete запрос к API сервера, удоляет
        питомца, ID которого указан и возвращает статус-код запроса'''
        headers = {
            'auth_key': auth_key['key'],
            'pet_id': pet_id
        }

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    ################################################################################################

###_end_###

