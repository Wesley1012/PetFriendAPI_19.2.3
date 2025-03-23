from api import PetFriends
from settings import valid_password, valid_login
import os

pf = PetFriends()
_, auth_key = pf.get_api_key(valid_login, valid_password)

# Получаем ключ аунтентификации
def test_get_api_key_for_valid_user(email=valid_login, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

# Получаем список питомцев
def test_get_all_pets_list_with_valid_data(filter=''):
    status, result = pf.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result) > 0

# Добавление нового питомца
def test_add_new_pet_with_valid_data(name='СынСобаки', animal_type='Кент',
                                     age='44', pet_photo='images/Dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Добавление нового питомца без фото
def test_add_new_pet_without_photo(name="Биба", animal_type="Боба", age=55):
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name

# Добавление нового питомца
def test_add_photo_for_pet():
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    # Если питомцев нет создаём нового
    if not my_pets["pets"]:
        _, my_pets = pf.add_new_pet_without_photo(auth_key, name="Пчел", animal_type="Пацанчик", age=2077)
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.add_photo_for_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    assert status == 200
    assert my_pets["pets"][0]["pet_photo"]

# добавляем информацию питомцу
def test_update_pet_info():
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    if len(my_pets["pets"]) == 0:
        _, new_pet = pf.add_new_pet_without_photo(auth_key, name="", animal_type="", age=0)
        _, my_pets = pf.get_list_pets(auth_key, "my_pets")
        pet_id = my_pets["pets"][0]["id"]
        status, result = pf.update_pet_info(auth_key, pet_id, name="Бадай", animal_type="СынСобаки", age=1223)
        assert status == 200
        assert new_pet["name"] != result["name"]
    else:
        status, result = pf.update_pet_info(auth_key, pet_id, name="Бадай", animal_type="СынСобаки", age=1223)
        _, my_pets = pf.get_list_pets(auth_key, "my_pets")
        assert status == 200
        assert my_pets["pets"][0]["name"] == result["name"]

# Удаление питомца
def test_delete_pet():
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, name="Бомжа", animal_type="ЭЭЭЭ", age=50, pet_photo="images/Dog.fpg")
        _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    id_pet = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, id_pet)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    assert status == 200
    assert id_pet not in my_pets.values()

# Удаление чужого питомца
def test_delete_of_another_pet():
    _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    # Проверка того что питомец чужой
    my_pets_ids = [i["id"] for i in my_pets["pets"]]
    for pet in all_pets["pets"]:
        if pet["id"] in my_pets_ids:
            continue
        else:
            status, _ = pf.delete_pet(auth_key, pet["id"])
            break
            _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
            assert status == 200
            assert pet["id"] not in all_pets["pets"]
