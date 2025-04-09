import json


class Data:
    path = "test_data.json"

    def load_data():
        try:
            with open("test_data.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Файл не найден!")
        except json.JSONDecodeError:
            print("Ошибка в формате JSON!")

    def get_init_structure(data):
        pass