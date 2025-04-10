import dearpygui.dearpygui as dpg
import load

def create_initial_table():
    keys = ["Cu", "Fe", "S", "SiO2", "CaO", "MgO", "Al2O3", "Zn", "Pb", "Влажность"]
    summ = [0, 0, 0]
    data = load.load_data()
    
    if dpg.does_item_exist("Init_window"):
        dpg.show_item("Init_window")
    else:
        with dpg.window(label="Составы исходных материалов", tag="Init_window", width=500, height=350, no_resize=True):
            with dpg.table(header_row=True, resizable=True, row_background=True,
                        borders_innerH=True, borders_outerH=True, borders_innerV=True,
                        borders_outerV=True):
                
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


def create_mol_table():
    mol_weight = load.load_mol_weight()
    
    if dpg.does_item_exist("Mol_window"):
        dpg.show_item("Mol_window")
    else:
        with dpg.window(label="Молекулярные веса", tag="Mol_window", width=500, height=400, no_resize=True):
            with dpg.table(header_row=False, resizable=True):
                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.table_cell():
                        with dpg.table(header_row=True, resizable=True, row_background=True,
                                    borders_innerH=True, borders_outerH=True, borders_innerV=True,
                                    borders_outerV=True):

                            dpg.add_table_column(label="Элементы")
                            dpg.add_table_column(label="Масса")

                            # once it reaches the end of the columns
                            for i in mol_weight["elements"].keys():
                                with dpg.table_row():
                                    with dpg.table_cell():
                                        dpg.add_text(i)
                                    with dpg.table_cell():
                                        dpg.add_text(mol_weight["elements"][i])

                    with dpg.table_cell():
                        with dpg.table(header_row=True, resizable=True, row_background=True,
                                    borders_innerH=True, borders_outerH=True, borders_innerV=True,
                                    borders_outerV=True):

                            dpg.add_table_column(label="Соединения")
                            dpg.add_table_column(label="Масса")

                            # once it reaches the end of the columns
                            for i in mol_weight["compounds"].keys():
                                with dpg.table_row():
                                    with dpg.table_cell():
                                        dpg.add_text(i)
                                    with dpg.table_cell():
                                        dpg.add_text(mol_weight["compounds"][i])