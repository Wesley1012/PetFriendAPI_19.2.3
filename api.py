import requests
import json
import allure
from requests_toolbelt.multipart.encoder import MultipartEncoder
from utils import api_logger


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def _attach_request(self, method, url, headers=None, data=None):
        """Прикрепляет информацию о запросе к отчёту Allure"""
        request_info = f"{method} {url}\n\n"
        if headers:
            request_info += f"Headers: {headers}\n"
        if data:
            request_info += f"Data: {data}"
        allure.attach(request_info, name="📤 Запрос", attachment_type=allure.attachment_type.TEXT)

    def _attach_response(self, status, result):
        """Прикрепляет информацию об ответе к отчёту Allure"""
        response_info = f"Status: {status}\n\nResponse: {result}"
        allure.attach(response_info, name="📥 Ответ", attachment_type=allure.attachment_type.TEXT)

    @allure.step("GET /api/key - получение ключа авторизации")
    @api_logger
    def get_api_key(self, email: str, password: str) -> json:
        headers = {
            'email': email,
            'password': password
        }
        url = self.base_url + "api/key"
        self._attach_request("GET", url, headers=headers)

        res = requests.get(url, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("GET /api/pets - получение списка питомцев")
    @api_logger
    def get_list_pets(self, auth_key: json, filter: str = "") -> json:
        headers = {'auth_key': auth_key["key"]}
        url = self.base_url + 'api/pets'
        self._attach_request("GET", url, headers=headers, data={"filter": filter})

        res = requests.get(url, headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("GET /api/pets (all) - получение всех питомцев")
    @api_logger
    def get_list_all_pets(self, auth_key: json, filter: str) -> json:
        headers = {'auth_key': auth_key["key"]}
        url = self.base_url + 'api/pets'
        self._attach_request("GET", url, headers=headers, data={"filter": filter})

        res = requests.get(url, headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("POST /api/pets - добавление питомца с фото")
    @api_logger
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        url = self.base_url + 'api/pets'
        self._attach_request("POST", url, headers=headers, data=f"multipart: name={name}, age={age}")

        res = requests.post(url, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("POST /api/create_pet_simple - добавление питомца без фото")
    @api_logger
    def add_new_pet_without_photo(self, auth_key, name, animal_type, age):
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {"auth_key": auth_key["key"]}
        url = self.base_url + "api/create_pet_simple"
        self._attach_request("POST", url, headers=headers, data=data)

        res = requests.post(url, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("POST /api/pets/set_photo/{{pet_id}} - добавление фото питомцу")
    @api_logger
    def add_photo_for_pet(self, auth_key, pet_id, pet_photo):
        data = MultipartEncoder(
            fields={"pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpeg")})
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}
        url = self.base_url + "api/pets/set_photo/" + pet_id
        self._attach_request("POST", url, headers=headers, data=f"multipart: photo={pet_photo}")

        res = requests.post(url, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("DELETE /api/pets/{{pet_id}} - удаление питомца")
    @api_logger
    def delete_pet(self, auth_key: str, id_pet: str) -> json:
        headers = {"auth_key": auth_key["key"]}
        url = self.base_url + f"api/pets/{id_pet}"
        self._attach_request("DELETE", url, headers=headers)

        res = requests.delete(url, headers=headers)
        result = ""
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result

    @allure.step("PUT /api/pets/{{pet_id}} - обновление информации о питомце")
    @api_logger
    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str,
                        age: str) -> json:
        headers = {"auth_key": auth_key["key"]}
        data = {
            "name": name,
            "animal_type": animal_type,
            'age': age
        }
        url = self.base_url + "api/pets/" + pet_id
        self._attach_request("PUT", url, headers=headers, data=data)

        res = requests.put(url, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        self._attach_response(status, result)
        return status, result