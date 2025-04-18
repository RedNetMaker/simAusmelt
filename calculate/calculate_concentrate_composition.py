"""
Файл: calculate_concentrate_composition.py
Описание: Расчет рационального состава концентрата на основе входных параметров.
Автор: EmergencyController
Дата: 2025
"""

import load

def to_mass(input_concentrate: dict, mass_kg: float):
    concentrate = {}
    #Переводит % в кг
    concentrate["Прочие"] = 0
    for c in input_concentrate:
        if c != "Прочие":
            if c != "Влажность(%)":
                concentrate["Прочие"] += input_concentrate[c]
                concentrate[c] = input_concentrate[c] * mass_kg / 100
            else:
                concentrate[c] = input_concentrate[c] * mass_kg / (100 - input_concentrate[c])
    concentrate["Прочие"] = (100 - concentrate["Прочие"]) * mass_kg / 100

    return concentrate


def calculate_composition(input: dict, mass_kg: float, proc_cufes2: float):
    components = ["Cu", "Fe", "S", "Zn", "Pb", "SiO2", "Al2O3", "CaO", "MgO", "CO2", "Прочие", "Всего"]
    compounds = ["CuFeS2", "CuS", "Cu2S", "FeS2", "ZnS", "PbS", "CaCO3", "MgCO3", "SiO2", "Al2O3", "Прочие", "Всего"]
    rational_composition = {}
    mol_weight = load.load_mol_weight()

    #Составляем массив из элементов
    for r in components:
        composition = {}
        for c in compounds:
            composition[c] = None
        rational_composition[r] = composition

    #Переводит % в кг
    input_concentrate = to_mass(input, mass_kg)

    #Расчет

    #CuFeS2
    CuFeS2 = input_concentrate["Cu(%)"] * proc_cufes2 / 100 * mol_weight["compounds"]["CuFeS2"] / mol_weight["elements"]["Cu"]
    rational_composition["Cu"]["CuFeS2"] = CuFeS2 * mol_weight["elements"]["Cu"] / mol_weight["compounds"]["CuFeS2"]
    rational_composition["Fe"]["CuFeS2"] = CuFeS2 * mol_weight["elements"]["Fe"] / mol_weight["compounds"]["CuFeS2"]
    rational_composition["S"]["CuFeS2"] = CuFeS2 * 2 * mol_weight["elements"]["S"] / mol_weight["compounds"]["CuFeS2"]
    #Проверка CuFeS2
    if round(CuFeS2, 2) == round((rational_composition["Cu"]["CuFeS2"] + rational_composition["Fe"]["CuFeS2"] + rational_composition["S"]["CuFeS2"]), 2):
        rational_composition["Всего"]["CuFeS2"] = rational_composition["Cu"]["CuFeS2"] + rational_composition["Fe"]["CuFeS2"] + rational_composition["S"]["CuFeS2"]

    #FeS2
    FeS2 = (input_concentrate["Fe(%)"] - rational_composition["Fe"]["CuFeS2"]) * mol_weight["compounds"]["FeS2"] / mol_weight["elements"]["Fe"]
    rational_composition["Fe"]["FeS2"] = FeS2 * mol_weight["elements"]["Fe"] / mol_weight["compounds"]["FeS2"]
    rational_composition["S"]["FeS2"] = FeS2 * 2 * mol_weight["elements"]["S"] / mol_weight["compounds"]["FeS2"]
    #Проверка FeS2
    if round(FeS2, 2) == round(rational_composition["Fe"]["FeS2"] + rational_composition["S"]["FeS2"], 2):
        rational_composition["Всего"]["FeS2"] = rational_composition["Fe"]["FeS2"] + rational_composition["S"]["FeS2"]

    #ZnS
    ZnS = input_concentrate["Zn(%)"] / mol_weight["elements"]["Zn"] * (mol_weight["elements"]["Zn"] + mol_weight["elements"]["S"])
    rational_composition["S"]["ZnS"] = ZnS * mol_weight["elements"]["S"] / mol_weight["compounds"]["ZnS"]
    rational_composition["Zn"]["ZnS"] = ZnS * mol_weight["elements"]["Zn"] / mol_weight["compounds"]["ZnS"]
    #Проверка ZnS
    if round(ZnS, 2) == round(rational_composition["S"]["ZnS"] + rational_composition["Zn"]["ZnS"], 2):
        rational_composition["Всего"]["ZnS"] = rational_composition["S"]["ZnS"] + rational_composition["Zn"]["ZnS"]

    #PbS
    PbS = input_concentrate["Pb(%)"] / mol_weight["elements"]["Pb"] * (mol_weight["elements"]["Pb"] + mol_weight["elements"]["S"])
    rational_composition["S"]["PbS"] = PbS * mol_weight["elements"]["S"] / mol_weight["compounds"]["PbS"]
    rational_composition["Pb"]["PbS"] = PbS * mol_weight["elements"]["Pb"] / mol_weight["compounds"]["PbS"]
    #Проверка PbS
    if round(PbS, 2) == round(rational_composition["S"]["PbS"] + rational_composition["Pb"]["PbS"], 2):
        rational_composition["Всего"]["PbS"] = rational_composition["S"]["PbS"] + rational_composition["Pb"]["PbS"]

    #Общее CuS и Cu2S
    Gcu = input_concentrate["Cu(%)"] - rational_composition["Cu"]["CuFeS2"]
    Gs = input_concentrate["S(%)"] - rational_composition["S"]["CuFeS2"] - rational_composition["S"]["FeS2"] - rational_composition["S"]["ZnS"] - rational_composition["S"]["PbS"]

    a1 = 2 * mol_weight["elements"]["Cu"] / mol_weight["compounds"]["Cu2S"]
    a2 = mol_weight["elements"]["Cu"] / mol_weight["compounds"]["CuS"]
    a3 = mol_weight["elements"]["S"] / mol_weight["compounds"]["Cu2S"]
    a4 = mol_weight["elements"]["S"] / mol_weight["compounds"]["CuS"]

    Cu2S = (Gs - Gcu * a4 / a2) / (a3 - a1 * a4 / a2)
    CuS = (Gcu - Cu2S * a1) / a2

    #Cu2S
    rational_composition["Cu"]["Cu2S"] = Cu2S * 2 * mol_weight["elements"]["Cu"] / mol_weight["compounds"]["Cu2S"]
    rational_composition["S"]["Cu2S"] = Cu2S * mol_weight["elements"]["S"] / mol_weight["compounds"]["Cu2S"]
    #Проверка Cu2S
    if round(Cu2S, 2) == round(rational_composition["Cu"]["Cu2S"] + rational_composition["S"]["Cu2S"], 2):
        rational_composition["Всего"]["Cu2S"] = rational_composition["Cu"]["Cu2S"] + rational_composition["S"]["Cu2S"]

    #CuS
    rational_composition["Cu"]["CuS"] = CuS * mol_weight["elements"]["Cu"] / mol_weight["compounds"]["CuS"]
    rational_composition["S"]["CuS"] = CuS * mol_weight["elements"]["S"] / mol_weight["compounds"]["CuS"]
    #Проверка CuS
    if round(CuS, 2) == round(rational_composition["Cu"]["CuS"] + rational_composition["S"]["CuS"], 2):
        rational_composition["Всего"]["CuS"] = rational_composition["Cu"]["CuS"] + rational_composition["S"]["CuS"]


    #Проверка ошибку на серу
    allS = rational_composition["S"]["CuFeS2"] + rational_composition["S"]["FeS2"] + rational_composition["S"]["ZnS"] + rational_composition["S"]["PbS"] + rational_composition["S"]["Cu2S"] + rational_composition["S"]["CuS"]
    # print(round((allS - input_concentrate["S(%)"]) * 100 / input_concentrate["S(%)"], 3))

    #CaCO3
    CaCO3 = input_concentrate["CaO(%)"] * mol_weight["compounds"]["CaCO3"] / (mol_weight["elements"]["Ca"] + mol_weight["elements"]["O"])
    rational_composition["CaO"]["CaCO3"] = CaCO3 * (mol_weight["elements"]["Ca"] + mol_weight["elements"]["O"]) / mol_weight["compounds"]["CaCO3"]
    rational_composition["CO2"]["CaCO3"] = CaCO3 * (mol_weight["elements"]["C"] + 2 * mol_weight["elements"]["O"]) / mol_weight["compounds"]["CaCO3"]
    #Проверка CaCO3
    if round(CaCO3, 2) == round(rational_composition["CaO"]["CaCO3"] + rational_composition["CO2"]["CaCO3"], 2):
        rational_composition["Всего"]["CaCO3"] = rational_composition["CaO"]["CaCO3"] + rational_composition["CO2"]["CaCO3"]

    #MgCO3
    MgCO3 = input_concentrate["MgO(%)"] * mol_weight["compounds"]["MgCO3"] / (mol_weight["elements"]["Mg"] + mol_weight["elements"]["O"])
    rational_composition["MgO"]["MgCO3"] = MgCO3 * (mol_weight["elements"]["Mg"] + mol_weight["elements"]["O"]) / mol_weight["compounds"]["MgCO3"]
    rational_composition["CO2"]["MgCO3"] = MgCO3 / mol_weight["compounds"]["MgCO3"] * (mol_weight["elements"]["C"] + 2 * mol_weight["elements"]["O"])
    #Проверка MgCO3
    if round(MgCO3, 2) == round(rational_composition["MgO"]["MgCO3"] + rational_composition["CO2"]["MgCO3"], 2):
        rational_composition["Всего"]["MgCO3"] = rational_composition["MgO"]["MgCO3"] + rational_composition["CO2"]["MgCO3"]

    #SiO2
    rational_composition["SiO2"]["SiO2"] = input_concentrate["SiO2(%)"]
    rational_composition["Всего"]["SiO2"] = input_concentrate["SiO2(%)"]

    #Al2O3
    rational_composition["Al2O3"]["Al2O3"] = input_concentrate["Al2O3(%)"]
    rational_composition["Всего"]["Al2O3"] = input_concentrate["Al2O3(%)"]

    #Прочие
    rational_composition["Прочие"]["Прочие"] = input_concentrate["Прочие"] - rational_composition["CO2"]["CaCO3"] - rational_composition["CO2"]["MgCO3"]
    rational_composition["Всего"]["Прочие"] = input_concentrate["Прочие"] - rational_composition["CO2"]["CaCO3"] - rational_composition["CO2"]["MgCO3"]


    #Цикл подсчета всего
    for c in rational_composition.keys():
        sum_items = 0
        for i in rational_composition[c].keys():
            if i != "Всего" and rational_composition[c][i] is not None:
                sum_items += rational_composition[c][i]
        rational_composition[c]["Всего"] = sum_items

    return rational_composition
