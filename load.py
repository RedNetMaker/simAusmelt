import json

path = "data/"

def load_data():
    try:
        with open(path + "test_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Файл не найден!")
    except json.JSONDecodeError:
        print("Ошибка в формате JSON!")

def load_mol_weight():
    try:
        with open(path + "mol_weight.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Файл не найден!")
    except json.JSONDecodeError:
        print("Ошибка в формате JSON!")

def get_init_structure(data):
    pass