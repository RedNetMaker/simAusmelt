class MatBalance:
    def __init__(self, data):
        self.Cu_out = data["Содержание меди в штейне(%)"]
        self.e = data["Извлечение Cu в штейн(%)"]
        self.slag = {
            "SiO2": data["Состав шлака из печи"]["SiO2"],
            "CaO": data["Состав шлака из печи"]["CaO"]
        }
        self.quartz = {
            "SiO2": 0,
            "Прочие": 0,
            "Влажность": 0
        }
        self.limestone = {
            "CaO": 0,
            "CO2": 0,
            "Прочие": 0,
            "Влажность": 0
        }