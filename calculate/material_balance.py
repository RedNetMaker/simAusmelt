from .calculate_concentrate_composition import to_mass
import load

class MatBalance:
    matt = {"Cu": {}, "Pb": {}, "Zn": {}, "Fe": {}, "S": {}, "O": {}, "Прочие": {}, "Всего": {"%": 0, "кг": 0},}
    matt = {"SiO2": {}, "Fe": {}, "Pb": {}, "Zn": {}, "CaO": {}, "MgO": {}, "O": {}, "Cu": {}, "Al2O3": {}, "Прочие": {}, "Всего": {"%": 0, "кг": 0},}

    def __init__(self, data, composition):
        self.composition = composition
        self.mol_weight = load.load_mol_weight()
        self.concentrate = to_mass(data["Состав сухого концентрата"], 100.0)
        self.data_in = {
            "Требуемое содержание меди в штейне": data["Содержание меди в штейне(%)"],
            "Задаем извлечение меди в штейн": data["Извлечение Cu в штейн(%)"],
            "Плавку ведем на шлак состава": {
                "SiO2": data["Состав шлака из печи"]["SiO2"],
                "CaO": data["Состав шлака из печи"]["CaO"]
            },
            "Состав кв. флюса": {
                "SiO2": data["Состав кварцевго флюса"]["SiO2(%)"],
                "Прочие": 100 - data["Состав кварцевго флюса"]["SiO2(%)"],
                "Влажность": data["Состав кварцевго флюса"]["Влажность(%)"]
            },
            "Состав изв. флюса": {
                "CaO": 56,
                "CO2": 100 - 56,
                "Прочие": 0,
                "Влажность": 5
            },
            "Выход Pb": {
                "В газ": data["Выход в газ"]["Pb(%)"],
                "В штейн": data["Выход в штейн"]["Pb(%)"],
                "В шлак": 100 - data["Выход в газ"]["Pb(%)"] - data["Выход в штейн"]["Pb(%)"]
            },
            "Выход Zn": {
                "В газ": data["Выход в газ"]["Zn(%)"],
                "В штейн": data["Выход в штейн"]["Zn(%)"],
                "В шлак": 100 - data["Выход в газ"]["Zn(%)"] - data["Выход в штейн"]["Zn(%)"]
            },
            "Задаем содержание прочих в штейне": 1,
            "Кол-во конвер. шлака на 100 кг сух.к-та": data["Подача конверторного шлака(т/ч)"] * (100 / (1 - data["Состав сухого концентрата"]["Влажность(%)"] / 100)) / data["Производительность по влажному концентрату(т/ч)"]
        }

        self.conv_slag = {
            "Cu": self.data_in["Кол-во конвер. шлака на 100 кг сух.к-та"] * 3 / 100,
            "Fe": self.data_in["Кол-во конвер. шлака на 100 кг сух.к-та"] * 3 / 100,
            "Pb": self.data_in["Кол-во конвер. шлака на 100 кг сух.к-та"] * 52 / 100,
            "Zn": self.data_in["Кол-во конвер. шлака на 100 кг сух.к-та"] * 2 / 100,
        }

    def matte(self):
        self.matt["Cu"]["кг"] = (self.concentrate["Cu(%)"] * self.data_in["Задаем извлечение меди в штейн"] + self.conv_slag["Cu"] * 80) / 100
        mass = self.matt["Cu"]["кг"] / self.data_in["Требуемое содержание меди в штейне"] * 100
        self.matt["Cu"]["%"] = self.matt["Cu"]["кг"] * 100 / mass
        self.matt["S"]["%"] = 25
        self.matt["S"]["кг"] = mass * self.matt["S"]["%"] / 100
        self.matt["O"]["%"] = 6.4 - 0.08 * self.data_in["Требуемое содержание меди в штейне"]
        self.matt["O"]["кг"] = self.matt["O"]["%"] / 100 * mass
        self.matt["Pb"]["кг"] = (self.concentrate["Pb(%)"] + self.conv_slag["Pb"]) * self.data_in["Выход Pb"]["В штейн"] / 100
        self.matt["Pb"]["%"] = self.matt["Pb"]["кг"] / mass * 100
        self.matt["Zn"]["кг"] = (self.concentrate["Zn(%)"] + self.conv_slag["Zn"]) * self.data_in["Выход Zn"]["В штейн"] / 100
        self.matt["Zn"]["%"] = self.matt["Zn"]["кг"] / mass * 100
        self.matt["Прочие"]["%"] = 1
        self.matt["Прочие"]["кг"] = self.matt["Прочие"]["%"] * mass / 100
        self.matt["Fe"]["%"] = 100 - (self.data_in["Требуемое содержание меди в штейне"] + self.matt["S"]["%"] + self.matt["O"]["%"] + 1 + self.matt["Pb"]["%"] + self.matt["Zn"]["%"])
        self.matt["Fe"]["кг"] = self.matt["Fe"]["%"] / 100 * mass

        for i in self.matt:
            if i != "Всего":
                self.matt["Всего"]["кг"] += self.matt[i]["кг"]
                self.matt["Всего"]["%"] += self.matt[i]["%"]

        return self.matt
    
    def slag(self):
        self.slag["Fe"]["кг"] = self.concentrate["Fe(%)"] + self.conv_slag["Fe"] - self.matt["Fe"]["кг"]
        FeO = self.slag["Fe"]["кг"] * (self.mol_weight["Fe"] + self.mol_weight["O"]) / self.mol_weight["Fe"]
        self.slag["Pb"]["кг"] = (self.concentrate["Pb(%)"] + self.conv_slag["Pb"]) * self.data_in["Выход Pb"]["В шлак"] / 100
        PbO = self.slag["Pb"]["кг"] * (self.mol_weight["Pb"] + self.mol_weight["O"]) / self.mol_weight["Pb"]
        self.slag["Zn"]["кг"] = (self.concentrate["Zn(%)"] + self.conv_slag["Zn"]) * self.data_in["Выход Zn"]["В шлак"] / 100
        ZnO = self.slag["Zn"]["кг"] * (self.mol_weight["Zn"] + self.mol_weight["O"]) / self.mol_weight["Zn"]
        self.slag["O"]["кг"] = FeO + PbO + ZnO - self.slag["Fe"]["кг"] - self.slag["Pb"]["кг"] - self.slag["Zn"]["кг"]
        #Нужно расчитать прочие в конверторном шлаке
        self.slag["Прочие"]["кг"] = self.composition["Прочие"]["Всего"]