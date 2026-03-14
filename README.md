# PetFriends API Testing

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Requests](https://img.shields.io/badge/Requests-2EAD33?style=flat&logo=python&logoColor=white)](https://docs.python-requests.org/)
[![Allure](https://img.shields.io/badge/Allure-DE5C43?style=flat&logo=allure&logoColor=white)](https://allurereport.org/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/yourusername/petfriends-tests)

Автоматические тесты для API сервиса [PetFriends](https://petfriends.skillfactory.ru/) — учебного проекта для тренировки тестирования REST API.

---

## 📋 О проекте

Проект содержит позитивные и негативные тесты для проверки API PetFriends (Swagger: https://petfriends.skillfactory.ru/apidocs/).  
Тесты покрывают основные сценарии работы с питомцами: создание, получение, обновление, удаление, а также проверки авторизации.

**Важно:** сервер не принимает email с кириллицей в локальной части или password состоящий только из спец-символов.

---

## Структура проекта (актуальная)

<pre>
PetFriendAPI_19.2.3/
├── api.py # API клиент (все эндпоинты)
├── conftest.py # Pytest фикстуры
├── pytest.ini # Конфигурация pytest
├── settings.py # Настройки и credentials
├── test_data.py # Тестовые данные (генерация строк, чисел)
├── utils.py # Вспомогательные функции (логгер)
├── tests/ # Директория с тестами
│ ├── images/ # Изображения для тестов
│ │ ├── Dog.jpg
│ │ ├── mounts.jpg
│ │ └── Пчела.jpg
│ ├── test_pet_friends.py # Позитивные тесты
│ └── test_pf_negativ.py # Негативные тесты
├── .gitignore # Игнорируемые файлы
└── README.md # Этот файл
</pre>

## Эндпоинты API

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| **GET** | `/api/key` | Получение API ключа по email/password |
| **GET** | `/api/pets` | Получение списка питомцев (с фильтром) |
| **POST** | `/api/pets` | Добавление питомца с фото |
| **POST** | `/api/create_pet_simple` | Добавление питомца без фото |
| **POST** | `/api/pets/set_photo/{pet_id}` | Добавление фото питомцу |
| **PUT** | `/api/pets/{pet_id}` | Обновление информации о питомце |
| **DELETE** | `/api/pets/{pet_id}` | Удаление питомца |

---

# Установка и запуск

## 1. Клонировать репозиторий
git clone https://github.com/Wesley1012/PetFriendAPI_19.2.3.git
cd ApiTests

# Создать виртуальное окружение
python -m venv .venv  
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows  

# Установить зависимости
pip install -r requirements.txt  

# Установить Allure (для отчётов)  
sudo pacman -S allure # Arch Linux  
brew install allure # macOS  
scoop install allure # Windows (scoop)  

# Запустить тесты
pytest
allure serve allure-results # Allure отчёты

