import requests
import json
from settings import appid, valid_login, valid_password

#
# params = {'q': 'Сочи', 'appid': appid, 'units': 'metric'}
# # city = str(input("ВВеди город: "))
#
# response = requests.get(f"https://api.openweathermap.org/data/2.5/weather", params=params)
#
# if response.status_code == 200:
#     data = json.loads(response.text)
#     temp = data['main']['temp']
# else:
#     print(response.status_code)
#
# print(f'Погода в городе {params['q']} {int(temp)} градуса')

url = "https://petfriends.skillfactory.ru/"

# Get auth_key (b11642cd39715a50fa3e025dadbcea6aac65f9670a556ffbc0647c2a)
headers = {
    "email": valid_login,
    "password": valid_password
}
auth_key = requests.get(url+"api/key", headers=headers).json()

# Get list of pets
filter = {'filter': "my_pets"}

her = {"auth_key": auth_key["key"]}
list_of_pets = requests.get(url+'api/pets', headers=her, params=filter)
# pprint.pprint(list_of_pets.json())

# Add new pet
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

pet_photo_path = os.path.join(os.path.dirname(__file__), "tests/images/mounts.jpg")

data = MultipartEncoder(
    fields={
        "name": "Try288",
        "animal_type": "Doter",
        "age": "1312",
        "pet_photo": ("mounts.jpg", open(pet_photo_path, "rb"), "image/jpeg")
    })

heads = {"auth_key": auth_key["key"], "Content-Type": data.content_type}
list_of_pets_before_post_pet = requests.get(url+'api/pets', headers=her, params=filter).json()["pets"]
print([i["name"] for i in list_of_pets_before_post_pet],f"\n{len(list_of_pets_before_post_pet)}")

# POST
# res = requests.post(url+"api/pets", headers=heads, data=data)
list_of_pets_after_post_pet = requests.get(url+'api/pets', headers=her, params=filter).json()

if list_of_pets_after_post_pet["pets"][0]["name"] == "Try288":
    print(f"Питомец: {list_of_pets_after_post_pet["pets"][0]["name"]} был чётко добавлен! Кол-во питомцев {len(list_of_pets_after_post_pet['pets'])}")

print([i['name'] for i in list_of_pets_after_post_pet["pets"]][0])

list_of_pets_before_delete_pet = requests.get(url+'api/pets', headers=her, params=filter).json()
headers = {"auth_key": auth_key["key"]}
names_before = [i['name'] for i in list_of_pets_before_delete_pet["pets"]]



id_pet = list_of_pets_before_delete_pet["pets"][0]["id"]
# DELETE
res = requests.delete(url+f"api/pets/{id_pet}", headers=headers)

list_of_pets_after_delete_pet = requests.get(url+'api/pets', headers=her, params=filter).json()

if res.status_code == 200:
    print(f"Статус код: {res.status_code}\nПитомец: {list_of_pets_after_delete_pet["pets"][0]["name"]} был жёстко удалён! Кол-во питомцев {len(list_of_pets_after_delete_pet["pets"])}")
names_after = [i['name'] for i in list_of_pets_after_delete_pet["pets"]]

print(names_after)

data = MultipartEncoder(
    fields={"pet_photo": ("tests/images/Dog", open("tests/images/Dog.jpg", "rb"), "image/jpeg")})

pet_id = list_of_pets_after_delete_pet["pets"][0]["id"]
headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

# res = requests.post(url + "api/pets/set_photo/" + pet_id, headers=headers, data=data)
ids = [i for i in list_of_pets_after_delete_pet["pets"]]

for i in ids:
    res = requests.delete(url + f"api/pets/{i["id"]}", headers=headers)
    print(f"Питомец {i["name"]} был безбожно удалён. Статус{res.status_code}")