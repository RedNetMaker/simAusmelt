import dearpygui.dearpygui as dpg

def create_initial_table(data):
    keys = ["Cu", "Fe", "S", "SiO2", "CaO", "MgO", "Al2O3", "Zn", "Pb", "Влажность"]
    summ = [0, 0, 0]


    with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                        borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):

        dpg.add_table_column(label="Компонент")
        dpg.add_table_column(label="Концентрат")
        dpg.add_table_column(label="Кварц")
        dpg.add_table_column(label="Известняк")

        # once it reaches the end of the columns
        for i in range(0, 9):
            with dpg.table_row():
                with dpg.table_cell():
                    dpg.add_text(keys[i])
                with dpg.table_cell():
                    dpg.add_text(f"{data["Состав сухого концентрата"][keys[i] + "(%)"]:.2f}")
                    summ[0] += data["Состав сухого концентрата"][keys[i] + "(%)"]
                with dpg.table_cell():
                    if keys[i] == "SiO2":
                        value = data["Состав кварцевго флюса"][keys[i] + "(%)"]
                    else:
                        value = 0
                    dpg.add_text(f"{value:.2f}")
                    summ[1] += value
                with dpg.table_cell():
                    if keys[i] == "CaO":
                        value = 56
                    else:
                        value = 0
                    dpg.add_text(f"{value:.2f}")
                    summ[2] += value

        with dpg.table_row():
            with dpg.table_cell():
                dpg.add_text("Прочие+CO2")
            with dpg.table_cell():
                dpg.add_text(f"{100 - summ[0]:.2f}")
            with dpg.table_cell():
                dpg.add_text(f"{100 - summ[1]:.2f}")
            with dpg.table_cell():
                dpg.add_text(f"{100 - summ[2]:.2f}")

        with dpg.table_row():
            with dpg.table_cell():
                dpg.add_text(keys[9])
            with dpg.table_cell():
                dpg.add_text(f"{data["Состав сухого концентрата"][keys[9] + "(%)"]:.2f}")
            with dpg.table_cell():
                dpg.add_text(f"{data["Состав кварцевго флюса"][keys[9] + "(%)"]:.2f}")
            with dpg.table_cell():
                dpg.add_text(f"{5:.2f}")