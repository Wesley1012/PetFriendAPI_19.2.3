import allure
import os
import pytest
from allure_commons.types import Severity
from api import PetFriends
from test_data import *

pf = PetFriends()

'''Важно: сервер не принимает email с кириллицей в локальной части или password состоящий только из спец-символов'''


@allure.epic("PetFriends API")
@allure.feature("Негативные сценарии")
class TestPetsNegative:

    @allure.story("Авторизация")
    @allure.title("Получение auth_key с невалидными данными [email={email}, password={password}]")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative", "auth")
    @pytest.mark.get
    @pytest.mark.parametrize('email', NEGATIV_EMAIL_CHECK_LIST, ids=IDS_NEGATIV_EMAIL_CHECK_LIST)
    @pytest.mark.parametrize('password', NEGATIV_PASSWORD_CHECK_LIST, ids=IDS_NEGATIV_PASSWORD_CHECK_LIST)
    def test_get_api_key_with_invalid_user(self, email, password):
        status, result = pf.get_api_key(email, password)
        assert status == 403
        assert "key" not in result

    @allure.story("Получение списка питомцев")
    @allure.title("Получение списка питомцев с невалидным ключом")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative", "get")
    @pytest.mark.get
    @pytest.mark.parametrize("invalid_auth_key", INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
    def test_get_list_of_pets_with_invalid_auth_key(self, invalid_auth_key):
        status, result = pf.get_list_pets(invalid_auth_key, filter='')
        assert status == 403
        assert "pets" not in result

    @allure.story("Удаление питомца")
    @allure.title("Удаление питомца с невалидным ключом")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative", "delete")
    @pytest.mark.delete
    @pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
    def test_delete_pet_with_invalid_auth_key(self, invalid_auth_key, create_yield_delete_test_pet):
        pet_id, get_data, _ = create_yield_delete_test_pet
        status, result = pf.delete_pet(invalid_auth_key, pet_id)
        _, pets_list_after_delete = pf.get_list_pets(get_data['auth_key'], "my_pets")
        assert status == 403
        assert pet_id == pets_list_after_delete["pets"][0]["id"]

    @allure.story("Создание питомца")
    @allure.title("Добавление питомца с невалидным ключом")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative", "post")
    @pytest.mark.post
    @pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
    def test_add_pet_with_invalid_auth_key(self, invalid_auth_key, get_data):
        status, result = pf.add_new_pet_without_photo(
            invalid_auth_key,
            get_data['name'],
            get_data['animal_type'],
            get_data['age']
        )
        _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
        assert status == 403
        assert get_data['name'] not in my_pets["pets"]

    @allure.story("Редактирование питомца")
    @allure.title("Обновление информации о питомце с невалидным ключом")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative", "put")
    @pytest.mark.put
    @pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
    def test_update_pet_info_with_invalid_auth_key(self, invalid_auth_key, create_yield_delete_test_pet):
        pet_id, get_data, update_data = create_yield_delete_test_pet
        status, result = pf.update_pet_info(
            invalid_auth_key,
            pet_id,
            update_data['name'],
            update_data['animal_type'],
            update_data['age']
        )
        _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
        assert status == 403
        assert update_data['name'] not in my_pets["pets"]

    @allure.story("Редактирование питомца")
    @allure.title("Добавление фото питомцу с невалидным ключом")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative", "post")
    @pytest.mark.post
    @pytest.mark.parametrize('invalid_auth_key', INVALID_AUTH_KEYS, ids=IDS_INVALID_AUTH_KEYS)
    def test_add_photo_for_pet_with_invalid_auth_key(self, invalid_auth_key, create_yield_delete_test_pet):
        pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
        pet_id, get_data, _ = create_yield_delete_test_pet
        status, _ = pf.add_photo_for_pet(invalid_auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")
        assert status == 403
        assert not my_pets["pets"][0]["pet_photo"]

    @allure.story("Редактирование питомца")
    @allure.title("Обновление информации чужому питомцу")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative", "put")
    @pytest.mark.post
    def test_update_another_pet_info(self, get_data, name="ПочемуБы", animal_type="ИНет", age=1312):
        _, all_pets = pf.get_list_all_pets(get_data['auth_key'], "all_pets")
        _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")

        my_pets_ids = [i["id"] for i in my_pets["pets"]]
        if len(all_pets["pets"]) > 0:
            for pet in all_pets["pets"]:
                if pet["id"] in my_pets_ids:
                    continue
                else:
                    status, _ = pf.update_pet_info(get_data['auth_key'], pet["id"], name, animal_type, age)
                    assert status == 403
                    _, all_pets = pf.get_list_all_pets(get_data['auth_key'], "all_pets")
                    assert name not in str(all_pets["pets"])
                    break
        else:
            raise Exception("Nothing to change!")

    @allure.story("Редактирование питомца")
    @allure.title("Добавление фото чужому питомцу")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative", "post")
    @pytest.mark.post
    def test_add_photo_to_another_pet(self, get_data):
        pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
        _, all_pets = pf.get_list_all_pets(get_data['auth_key'], "all_pets")
        _, my_pets = pf.get_list_pets(get_data['auth_key'], "my_pets")

        my_pets_ids = [i["id"] for i in my_pets["pets"]]
        if len(all_pets["pets"]) > 0:
            for pet in all_pets["pets"]:
                if pet["id"] in my_pets_ids:
                    continue
                else:
                    status, _ = pf.add_photo_for_pet(get_data['auth_key'], pet["id"], pet_photo)
                    assert status == 403
                    _, all_pets = pf.get_list_all_pets(get_data['auth_key'], "all_pets")
                    # Проверяем, что у питомца всё ещё нет фото
                    for p in all_pets["pets"]:
                        if p["id"] == pet["id"]:
                            assert not p.get("pet_photo")
                            break
                    break
        else:
            raise Exception("Nothing to change!")