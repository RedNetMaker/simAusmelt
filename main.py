import components
import load
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Ausmelt', width=1600, height=900)

with dpg.font_registry():
    with dpg.font("data/gilroy-regular.ttf", 16, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

data = load.load_data()
mol_weight = load.load_mol_weight()

with dpg.window(label="Симуляция", width=1000, height=700, min_size=[800, 500]):
    with dpg.menu_bar():
        with dpg.menu(label="Данные"):
            dpg.add_menu_item(label="Состав", callback=components.create_initial_table(data))
            dpg.add_menu_item(label="Молекуляр. веса")

# with dpg.window(label="Данные", width=800, height=500, min_size=[800, 500]):
#     with dpg.table(header_row=False):
#         dpg.add_table_column()
#         dpg.add_table_column()

#         with dpg.table_row():
#                 with dpg.table_cell():
#                     components.create_initial_table(data)
#                 with dpg.table_cell():
#                     components.create_mol_table(mol_weight)


dpg.setup_dearpygui()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()