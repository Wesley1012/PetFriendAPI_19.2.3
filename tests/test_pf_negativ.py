from api import PetFriends
from test_data import *
import os
import pytest

pf = PetFriends()

'''Важно: сервер не принимает email с кириллицей в локальной части или password состоящий только из спец-символов'''

# Получение auth_key с невалидными данными
@pytest.mark.get
@pytest.mark.parametrize('email', NEGATIV_EMAIL_CHECK_LIST, ids=IDS_NEGATIV_EMAIL_CHECK_LIST)
@pytest.mark.parametrize('password', NEGATIV_PASSWORD_CHECK_LIST, ids=IDS_NEGATIV_PASSWORD_CHECK_LIST)
def test_get_api_key_with_invalid_user(email, password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# Получение списка питомцев с невалидным ключем
@pytest.mark.get
@pytest.mark.parametrize("invalid_auth_key", INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
def test_get_list_of_pets_with_invalid_auth_key(invalid_auth_key):
    status, result = pf.get_list_pets(invalid_auth_key, filter='')
    assert status == 403
    assert "pets" not in result

# Удаление питомца с невалидным ключем
@pytest.mark.delete
@pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
def test_delete_pet_with_invalid_auth_key(invalid_auth_key, create_yield_delete_test_pet):
    pet_id, get_data, _ = create_yield_delete_test_pet
    status, result = pf.delete_pet(invalid_auth_key, pet_id)
    _, pets_list_after_delete = pf.get_list_pets(get_data['auth_key'], "my_pets")
    assert status == 403
    assert pet_id == pets_list_after_delete["pets"][0]["id"]

# Добавление нового питомца с невалидным ключем
@pytest.mark.post
@pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
def test_add_pet_with_invalid_auth_key(invalid_auth_key, get_data):
    status, result = pf.add_new_pet_without_photo(invalid_auth_key, get_data['name'], get_data['animal_type'], get_data['age'])
    _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
    assert status == 403
    assert get_data['name'] not in my_pets["pets"]

# Добавление информации о питомце с невалидным ключем
@pytest.mark.put
@pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
def test_update_pet_info_with_invalid_auth_key(invalid_auth_key, create_yield_delete_test_pet):
    pet_id, get_data, update_data = create_yield_delete_test_pet
    status, result = pf.update_pet_info(invalid_auth_key, pet_id, update_data['name'], update_data['animal_type'], update_data['age'])
    _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
    assert status == 403
    assert update_data['name'] not in my_pets["pets"]


# @pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
# def test_update_pet_info_with_invalid_auth_key(name="Джанго", animal_type="Освобожденный", age=228):
#     _, my_pets = pf.get_list_pets(auth_key, "my_pets")
#     if len(my_pets["pets"]) == 0:
#         _, new_pet = pf.add_new_pet_without_photo(auth_key, name="", animal_type="", age=0)
#         _, my_pets = pf.get_list_pets(auth_key, "my_pets")
#     pet_id = my_pets["pets"][0]["id"]
#     status, result = pf.update_pet_info(invalid_auth_key, pet_id, name, animal_type, age)
#     _, my_pets = pf.get_list_pets(auth_key, "my_pets")
#     assert status == 403
#     assert name not in my_pets["pets"]

# Добавление фото питомца с невалидным ключем
@pytest.mark.post
@pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
def test_add_photo_for_pet_with_invalid_auth_key(invalid_auth_key, create_yield_delete_test_pet):
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
    pet_id, get_data, _ = create_yield_delete_test_pet
    # _, new_pet = pf.add_new_pet_without_photo(auth_key, name="PhotoTest", animal_type="Animal", age=2077)
    # _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    # pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.add_photo_for_pet(invalid_auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
    assert status == 403
    assert not my_pets["pets"][0]["pet_photo"]
    # Удаляем питомца(Опционально)
    # pf.delete_pet(auth_key, pet_id)

# Добавление информации чужому питомцу
@pytest.mark.post
def test_update_another_pet_info(get_data, name="ПочемуБы", animal_type="ИНет", age=1312):
    _, all_pets = pf.get_list_all_pets(get_data['auth_key'], "all_pets")
    _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
    # Проверка того что питомец чужой
    my_pets_ids = [i["id"] for i in my_pets["pets"]]
    if len(all_pets["pets"]) > 0:
        for pet in all_pets["pets"]:
            if pet["id"] in my_pets_ids:
                continue
            else:
                status, _ = pf.update_pet_info(get_data['auth_key'], pet["id"], name, animal_type, age)
                break
                _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
                assert status == 403
                assert name not in all_pets["pets"]
    else:
        raise Exception("Nothing to change!")

# Добавление фото чужому питомцу
@pytest.mark.post
def test_add_pet_with_photo_through_create_pet_simple(get_data):
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
    _, all_pets = pf.get_list_all_pets(get_data['auth_key'], "all_pets")
    _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
    # Проверка того что питомец чужой
    my_pets_ids = [i["id"] for i in my_pets["pets"]]
    if len(all_pets["pets"]) > 0:
        for pet in all_pets["pets"]:
            if pet["id"] in my_pets_ids:
                continue
            else:
                status, _ = pf.add_photo_for_pet(get_data['auth_key'], pet["id"], pet_photo)
                break
                _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
                assert status == 403
                assert pet_photo not in all_pets["pets"]
    else:
        raise Exception("Nothing to chenge!")

