import os
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что ответ в переменной result содержит слово key, статус-код запроса 200."""
    status, result = pf.get_api_key(email, password)

    assert 'key' in result
    assert status == 200

def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем, что список всех питомцев не пустой, статус-код запроса 200.'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)

    assert len(result['pets']) > 0
    assert status == 200

def test_add_pets_with_valid_data(name='Мелкий', animal_type='cat', age='6', pet_photo='images/IMG_9737.JPG'):
    '''Передаем данные и фото питомца, api ключ и проверяем, что в
    ответе содержатся добавленные данные, статус-код запроса 200.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert result['name'] == name
    assert status == 200

def test_delete_pet():
    '''Проверяем возможность удаления питомца. Для этого запрашиваем список питомцев пользователя
    и, если он пуст, добавляем питомца из предшествующего теста, а затем уже удаляем его.'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(api_key, 'Мелкий', 'cat', '6', 'images/IMG_9737.JPG')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert pet_id not in my_pets.values()
    assert status == 200

def test_update_pet_info(name='Измен', animal_type='измененыч', age='00'):
    '''Проверяем возможность изменения данных питомца. При
    отсутствии питомцев у пользователя обрабатываем ошибку.'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert result['name'] == name
        assert status == 200
    else:
        raise Exception("У вас пока что отсутствуют питомцы")

def test_add_pets_with_valid_data_without_photo(name='Тимоха_без_фото', animal_type='cat', age='5'):
    '''Проверяем возможность добавления нового питомца без фото.'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert result['name'] == name
    assert status == 200

def test_add_photo_at_pet(pet_photo='images/IMG_20180618_155452.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        assert status == 200
    else:
        raise Exception("У вас пока что отсутствуют питомцы.")

def test_add_pet_negative_age_number(name='Мелкий', animal_type='cat', age='-1', pet_photo='images/IMG_9737.JPG'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле "возраст".'
    assert status == 200

def test_add_pet_with_four_digit_age_number(name='Мелкий', animal_type='cat', age='1234', pet_photo='images/IMG_9737.JPG'):
    '''Проверка с негативным сценарием. Добавление питомца с возрастом более трех знаков в переменной age.
    Тест не будет пройден, если питомец будет добавлен на сайт с возрастом, превышающим три знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом привышающим 3 знака в поле "возраст".'
    assert status == 200

def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='6', pet_photo='images/IMG_9737.JPG'):
    '''Проверка с негативным сценарием. Добавление питомца с пустым значением в переменной name.
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "имя".'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени.'
    assert status == 200

def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='cat', age='6', pet_photo='images/IMG_9737.JPG'):
    '''Проверка с негативным сценарием. Добавление питомца имя которого превышает 10 слов
    Тест не будет пройден, если питомец будет добавлен на сайт с именем состоящим из более 10 слов.'''
    name = 'Это Кот которого все любят гладят и зовут Мелким или Малышом'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    list_name = result['name'].split()
    word_count = len(list_name)

    assert word_count < 10, 'Имя питомца длинее 10 слов.'
    assert status == 200

def test_add_pet_with_special_characters_in_variable_animal_type(name='Мелкий', age='6', pet_photo='images/IMG_9737.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с спец.символами вместо букв в переменной animal_type.
    Тест не будет пройден, если питомец будет добавлен на сайт с спец.символами вместо букв в поле порода.'''
    animal_type = 'Cat%@'
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)

    assert symbol[0] not in result['animal_type'], 'Питомец добавлен с недопустимыми символами.'
    assert status == 200

def test_add_pet_with_numbers_in_variable_animal_type(name='Мелкий', animal_type='34562', age='6', pet_photo='images/IMG_9737.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден, если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле "порода".'
    assert status == 200

def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Fedor', age='2', pet_photo='images/IMG_9737.jpg'):
    '''Проверка с негативным сценарием. Добавления питомца название породы которого превышает 10 слов
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим из более 10 слов.'''

    animal_type = 'Котяро мокро но пушисто и было находянго ин кустисто которо свисалло над котяро'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert word_count < 10, 'Питомец добавлен с названием породы, состоящим более чем из 10 слов.'
    assert status == 200

def test_get_api_key_with_correct_emai_and_wrong_password_(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом. Проверяем нет ли ключа в ответе.'''
    status, result = pf.get_api_key(email, password)
    assert 'key' not in result
    assert status == 403

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом. Проверяем нет ли ключа в ответе.'''
    status, result = pf.get_api_key(email, password)
    assert 'key' not in result
    assert status == 403



