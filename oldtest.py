#
# pf = PetFriends()
# # _, auth_key = pf.get_api_key(valid_login, valid_password)
#

def debug(func):
    """ Выводит сигнатуру функции и возвращает значение"""
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Вызываем {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} вернула значение - {value!r}")
        return value
    return wrapper_debug

# # Получаем ключ аунтентификации
# @pytest.mark.get
# @pytest.mark.api
# def test_get_api_key_for_valid_user(email=valid_login, password=valid_password):
#     status, result = pf.get_api_key(email, password)
#     assert status == 200
#     assert "key" in result
#
# # Получаем список питомцев
# @pytest.mark.get
# @pytest.mark.api
# def test_get_all_pets_list_with_valid_data(get_data, filter=''):
#     status, result = pf.get_list_pets(get_data["auth_key"], filter)
#     assert status == 200
#     assert len(result) > 0
#
# # Добавление нового питомца
# @pytest.mark.post
# @pytest.mark.api
# def test_add_new_pet_with_valid_data(get_data):
#     pet_photo = os.path.join(os.path.dirname(__file__), 'images/Dog.jpg')
#     status, result = pf.add_new_pet(get_data["auth_key"], get_data["name"], get_data["animal_type"], str(get_data["age"]), pet_photo)
#     assert status == 200
#     assert result['name'] == get_data["name"]
#
# # Добавление нового питомца без фото
# @pytest.mark.post
# @pytest.mark.api
# def test_add_new_pet_without_photo(get_data):
#     status, result = pf.add_new_pet_without_photo(get_data["auth_key"], get_data["name"], get_data["animal_type"], get_data["age"])
#     assert status == 200
#     assert result["name"] == get_data["name"]
#
# # Добавление нового питомца
# @pytest.mark.post
# @pytest.mark.api
# def test_add_photo_for_pet(create_yield_delete_test_pet):
#     pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
#     pet_id, headers, _ = create_yield_delete_test_pet
#     # _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     # Если питомцев нет создаём нового
#     # if not my_pets["pets"]:
#     #     _, my_pets = pf.add_new_pet_without_photo(get_data["auth_key"], get_data["name"], get_data["animal_type"], get_data["age"])
#     # pet_id = my_pets["pets"][0]["id"]
#     status, result = pf.add_photo_for_pet(headers, pet_id, pet_photo)
#     # _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     assert status == 200
#     assert pet_id == result['id']
#
# # добавляем информацию питомцу
# @pytest.mark.put
# @pytest.mark.api
# def test_update_pet_info(get_data):
#     _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     pet_id = my_pets["pets"][0]["id"]
#     if len(my_pets["pets"]) == 0:
#         _, new_pet = pf.add_new_pet_without_photo(get_data["auth_key"], name="", animal_type="", age=0)
#         _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#         pet_id = my_pets["pets"][0]["id"]
#         status, result = pf.update_pet_info(get_data["auth_key"], pet_id, get_data["name"], get_data["animal_type"], get_data["age"])
#         assert status == 200
#         assert new_pet["name"] != result["name"]
#     else:
#         status, result = pf.update_pet_info(get_data["auth_key"], pet_id, get_data["name"], get_data["animal_type"], get_data["age"])
#         _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#         assert status == 200
#         assert my_pets["pets"][0]["name"] == result["name"]
#
# # Удаление питомца
# @pytest.mark.delete
# @pytest.mark.api
# def test_delete_pet(get_data):
#     auth_key = get_data
#     _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     if len(my_pets["pets"]) == 0:
#         pf.add_new_pet(get_data["auth_key"], get_data["name"], get_data["animal_type"], get_data["age"], pet_photo="images/Dog.fpg")
#         _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     id_pet = my_pets["pets"][0]["id"]
#     status, _ = pf.delete_pet(get_data["auth_key"], id_pet)
#     _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     assert status == 200
#     assert id_pet not in my_pets.values()
#
# # Удаление чужого питомца
# @pytest.mark.delete
# @pytest.mark.api
# def test_delete_of_another_pet(get_data):
#     auth_key = get_data
#     _, all_pets = pf.get_list_all_pets(get_data["auth_key"], "all_pets")
#     _, my_pets = pf.get_list_pets(get_data["auth_key"], "my_pets")
#     # Проверка того что питомец чужой
#     my_pets_ids = [i["id"] for i in my_pets["pets"]]
#     for pet in all_pets["pets"]:
#         if pet["id"] in my_pets_ids:
#             continue
#         else:
#             status, _ = pf.delete_pet(get_data["auth_key"], pet["id"])
#             break
#             _, all_pets = pf.get_list_all_pets(get_data["auth_key"], "all_pets")
#             assert status == 200
#             assert pet["id"] not in all_pets["pets"]
#
