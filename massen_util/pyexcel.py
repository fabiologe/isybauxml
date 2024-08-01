import openpyxl as xl
import pandas as pd
import os 
col_leitung = {
    "DN":{
        "start_cell": "A6",
        "data_type": "float"
    },
    "Laenge":{
        "start_cell": "F6",
        "data_type": "float"
    }
}
col_schacht = {
    "Schacht": {
        "start_cell":"A5",
        "data_type":"str"
    },
    "Tiefe": {
        "start_cell": "B5",
        "data_type":"float"
    },
    "DN Zulauf":{
        "start_cell": "C5",
        "data_type": "float"
    },
    "DN Ablauf":{
        "start_cell":"D5", 
        "data_type": "float"
    }
}
col_haltung = {
    "Status": {
        "start_cell": "W7",
        "data_type": "str"
    },
    "Knoten Nr. oben": {
        "start_cell": "A7",
        "data_type": "str"
    },
    "Knoten Nr. unten": {
        "start_cell": "B7",
        "data_type": "str"
    },
    "Deckelhoehe oben": {
        "start_cell": "C7",
        "data_type": "float"
    },
    "Deckelhoehe unten": {
        "start_cell": "D7",
        "data_type": "float"
    },
    "Sohlhoehe oben": {
        "start_cell": "E7",
        "data_type": "float"
    },
    "Sohlhoehe unten": {
        "start_cell": "F7",
        "data_type": "float"
    },
    "Laenge": {
        "start_cell": "G7",
        "data_type": "float"
    },
    "DN": {
        "start_cell": "L7",
        "data_type": "float"
    }
}
def to_xsls_haltung(col_haltung, col_schacht, col_leitung):
    csv_h = os.path.abspath('output_xlsx_csv/massen_haltungen.csv')
    csv_s = os.path.abspath('output_xlsx_csv/massen_schacht.csv')
    csv_l = os.path.abspath('output_xlsx_csv/massen_leitung.csv')
    src = os.path.abspath('massen_util/src/massen.xlsx')
    print(src)
    wb = xl.load_workbook(src)
    ws_haltung = wb["Massen_Haltung"]
    ws_leitung = wb["Massen_Leitung"]
    ws_schacht = wb["Massen_Schacht"]

    df_s = pd.read_csv(csv_s)
    df_h = pd.read_csv(csv_h)

    # Haltung-CSV to xsls
    column_lists = {
    "Status": df_h["Status"].tolist(),
    "Knoten Nr. oben": df_h["Knoten Nr. oben"].tolist(),
    "Knoten Nr. unten": df_h["Knoten Nr. unten"].tolist(),
    "Deckelhoehe oben": df_h["Deckelhoehe oben"].tolist(),
    "Deckelhoehe unten": df_h["Deckelhoehe unten"].tolist(),
    "Sohlhoehe oben": df_h["Sohlhoehe oben"].tolist(),
    "Sohlhoehe unten": df_h["Sohlhoehe unten"].tolist(),
    "Laenge": df_h["Laenge"].tolist(),
    "DN": df_h["DN"].tolist(),
    }
    for col_name, assignment in col_schacht.items():
        data_list = df_s[col_name].tolist()
        start_row, start_col = xl.utils.coordinate_to_tuple(assignment["start_cell"])
        start_row = max(start_row, 1)
        start_col = max(start_col, 1)

        for row_idx, value in enumerate(data_list):
            # Apply correct data type formatting before writing
            if assignment["data_type"] == "str":
                cell_value = str(value)
            else:
                cell_value = float(value)

            # Write to the cell based on row and column offset
            ws_schacht.cell(row=row_idx + start_row, column=start_col).value = cell_value

    for col_name, assignment in col_haltung.items():
        data_list = df_h[col_name].tolist()  

       
        start_row, start_col = xl.utils.coordinate_to_tuple(assignment["start_cell"])

       
        start_row = max(start_row, 1)
        start_col = max(start_col, 1)

        for row_idx, value in enumerate(data_list):
            # Apply correct data type formatting before writing
            if assignment["data_type"] == "str":
                cell_value = str(value)
            else:
                cell_value = float(value)

            # Write to the cell based on row and column offset
            ws_haltung.cell(row=row_idx + start_row, column=start_col).value = cell_value

    wb.save('output_xlsx_csv/massen_gesamt.xlsx')
    return print("Data successfully written to your XLS file!")

