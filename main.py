import data_components
import calc_components
import load
from calculate.material_balance import MatBalance
from calculate.calculate_concentrate_composition import calculate_composition
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Ausmelt', width=1600, height=900)

with dpg.font_registry():
    with dpg.font("data/gilroy-regular.ttf", 16, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

data = load.load_data()
composition = calculate_composition(data["Состав сухого концентрата"], 100.0, 85.0)
balance = MatBalance(data, composition)

with dpg.window(label="Симуляция", width=1000, height=700, min_size=[800, 500]):
    with dpg.menu_bar():
        with dpg.menu(label="Данные"):
            dpg.add_menu_item(label="Состав", callback=data_components.create_initial_table)
            dpg.add_menu_item(label="Молекуляр. веса", callback=data_components.create_mol_table)
        with dpg.menu(label="Расчет"):
            dpg.add_menu_item(label="Рац.состав", callback=calc_components.create_composition_table)
            dpg.add_menu_item(label="Штейн", callback=calc_components.create_matte_table)


dpg.setup_dearpygui()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()