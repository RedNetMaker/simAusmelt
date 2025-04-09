import json
import components
from data import Data
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Ausmelt', width=1200, height=700)

with dpg.font_registry():
    with dpg.font("gilroy-regular.ttf", 20, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

data = Data.load_data()

with dpg.window(label="Данные"):
    components.create_initial_table(data)


dpg.setup_dearpygui()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()