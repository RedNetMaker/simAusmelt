import dearpygui.dearpygui as dpg

from calculate.material_balance import MatBalance
from calculate.calculate_concentrate_composition import calculate_composition
import load

def create_composition_table():
    data = load.load_data()
    composition = calculate_composition(data["Состав сухого концентрата"], 100.0, 85.0)
    
    if dpg.does_item_exist("composition_window"):
        dpg.show_item("composition_window")
    else:
        with dpg.window(label="Рациональный состав", tag="composition_window", width=900, height=370, no_resize=True):
            with dpg.table(header_row=True, resizable=True, row_background=True,
                        borders_innerH=True, borders_outerH=True, borders_innerV=True,
                        borders_outerV=True):
                dpg.add_table_column(label="Компоненты")
                for head in composition["Cu"].keys():
                    dpg.add_table_column(label=head)

                for key in composition.keys():
                    with dpg.table_row():
                        with dpg.table_cell():
                                dpg.add_text(key)
                        for value in composition[key].keys():
                            with dpg.table_cell():
                                if composition[key][value] is None:
                                    dpg.add_text()
                                else:
                                    dpg.add_text(f"{composition[key][value]:.2f}")

def create_matte_table():
    data = load.load_data()
    composition = calculate_composition(data["Состав сухого концентрата"], 100.0, 85.0)
    balance = MatBalance(data, composition)
    matte = balance.matte()
    
    if dpg.does_item_exist("matte_window"):
        dpg.show_item("matte_window")
    else:
        with dpg.window(label="Состав и количество штейна", tag="matte_window", width=400, height=300, no_resize=True):
            with dpg.table(header_row=True, resizable=True, row_background=True,
                        borders_innerH=True, borders_outerH=True, borders_innerV=True,
                        borders_outerV=True):
                
                dpg.add_table_column(label="Компоненты")
                dpg.add_table_column(label="кг")
                dpg.add_table_column(label="%")
                

                for key in matte:
                    with dpg.table_row():
                        dpg.add_text(key)
                        dpg.add_text(f"{matte[key]["кг"]:.2f}")
                        dpg.add_text(f"{matte[key]["%"]:.2f}")