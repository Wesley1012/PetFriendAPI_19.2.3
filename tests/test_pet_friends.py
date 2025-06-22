from api import PetFriends
from settings import valid_password, valid_login
from test_data import *
import os
import pytest
pf = PetFriends()


# Получаем ключ аунтентификации
@pytest.mark.get
@pytest.mark.api
def test_get_api_key_for_valid_user(email=valid_login, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


'''Большенство проверок с mark.parametrize явно негативные, но документация позволяет, поэтому эти проверки в модуле с позитивними'''

@pytest.mark.get
@pytest.mark.api
@pytest.mark.parametrize("filter",[
                                    generate_string(250),
                                    generate_string(1001),
                                    russian_chars(),
                                    russian_chars().upper(),
                                    chinese_chars(),
                                    special_chars(),
                                    "12345"], ids = [ "250 symbols", "1001 symbols", "russian", "RUSSIAN", "chinese", "special symbols", "digit"])
def test_get_all_pets_list_with_valid_data(get_data, filter):
    status, result = pf.get_list_pets(get_data["auth_key"], filter)
    assert status == 200
    assert len(result) > 0

# Добавление нового питомца
@pytest.mark.post
@pytest.mark.api
def test_add_new_pet_with_valid_data(get_data):
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/Dog.jpg')
    status, result = pf.add_new_pet(get_data["auth_key"], get_data["name"], get_data["animal_type"], str(get_data["age"]), pet_photo)
    assert status == 200
    assert result['name'] == get_data["name"]

# Добавление нового питомца без фото
@pytest.mark.post
@pytest.mark.api
@pytest.mark.parametrize("name", STRING_CHECK_LIST, ids=IDS_STRING_CHECK_LIST)
@pytest.mark.parametrize("animal_type", STRING_CHECK_LIST, ids=IDS_STRING_CHECK_LIST)
@pytest.mark.parametrize("age", INT_CHECK_LIST, ids=IDS_INT_CHECK_LIST)
def test_add_new_pet_without_photo(get_data, name, animal_type, age):
    status, result = pf.add_new_pet_without_photo(get_data["auth_key"], name, animal_type, age)
    assert status == 200
    assert result["name"] == name
    assert result["animal_type"] == animal_type
    assert result["age"] == age

# Добавление нового питомца
@pytest.mark.post
@pytest.mark.api
def test_add_photo_for_pet(create_yield_delete_test_pet):
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
    pet_id, headers, _, _= create_yield_delete_test_pet
    status, result = pf.add_photo_for_pet(headers, pet_id, pet_photo)
    assert status == 200
    assert pet_id == result['id']

# добавляем информацию питомцу
@pytest.mark.xfail
@pytest.mark.put
@pytest.mark.api
def test_update_pet_info(create_yield_delete_test_pet):
    pet_id, get_data, update_data = create_yield_delete_test_pet
    status, result = pf.update_pet_info(get_data['auth_key'], pet_id, update_data["name"], update_data["animal_type"], update_data["age"])
    assert status == 200
    assert get_data["name"] != result["name"]
    assert get_data["animal_type"] != result["animal_type"]
    assert get_data["age"] != result["age"]

# Удаление питомца
@pytest.mark.delete
@pytest.mark.api
def test_delete_pet(create_yield_delete_test_pet):
    pet_id, get_data, _ = create_yield_delete_test_pet
    status, _ = pf.delete_pet(get_data['auth_key'], pet_id)
    _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
    assert status == 200
    assert pet_id not in my_pets["pets"]

# Удаление чужого питомца
@pytest.mark.delete
@pytest.mark.api
def test_delete_of_another_pet(get_data):
    _, all_pets = pf.get_list_pets(get_data["auth_key"], "all_pets")
    _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
    # Проверка того что питомец чужой
    my_pets_ids = [i["id"] for i in my_pets["pets"]]
    for pet in all_pets["pets"]:
        if pet["id"] in my_pets_ids:
            continue
        else:
            status, _ = pf.delete_pet(get_data["auth_key"], pet["id"])
            break
            _, all_pets = pf.get_list_all_pets(get_data["auth_key"], "all_pets")
            assert status == 200
            assert pet["id"] not in all_pets["pets"]

