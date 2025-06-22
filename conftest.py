import random
import pytest
from faker import Faker
from settings import valid_password,valid_login
from api import PetFriends
pf = PetFriends()


@pytest.fixture(autouse=True)
def get_data():
    """ Получить словарь с значениями auth_key, name, animal_type, age"""

    status, result = pf.get_api_key(valid_login, valid_password)
    data = {
        "auth_key": result,
        "name": Faker().first_name(),
        "animal_type": Faker().word(ext_word_list=["Dog", "Cat", "Bird", "Snake", "Fish", "Potato", "Chertsuka"]),
        "age": random.randint(1, 50)
    }
    assert status == 200, "Запрос провален"
    assert "key" in result

    return data

@pytest.fixture(autouse=True)
def create_yield_delete_test_pet(get_data):
    """Pet_id, headers, data, update_data"""
    update_data = {
        "name": Faker().first_name(),
        "animal_type": Faker().word(
            ext_word_list=["Dog", "Cat", "Bird", "Snake", "Fish", "Potato", "Chertsuka"]),
        "age": random.randint(1, 50)
    }
    # headers = get_data["auth_key"]
    # data = {k: get_data[k] for k in list(get_data.keys())[1:]}  #Словарь с name, animal_type и age
    status, result = pf.add_new_pet_without_photo(get_data['auth_key'], get_data["name"], get_data["animal_type"], get_data["age"])

    assert status == 200, "POST запрос провален"
    assert "id" in result, "В ответе нет id"
    pet_id = result["id"]

    yield pet_id, get_data, update_data

    status, get_resp = pf.get_list_pets(get_data["auth_key"], "my_pets")

    assert status == 200, "GET запрос провален"

    if pet_id in get_resp:
        status, _ = pf.delete_pet(get_data['auth_key'], pet_id)
        assert status == 200, "DELETE запрос провален"


