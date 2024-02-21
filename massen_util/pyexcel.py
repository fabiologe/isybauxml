import openpyxl as xl
import pandas as pd
import os 


column_assignments = {
    "Status": {
        "start_cell": "W7",
        "data_type": "str"
    },
    "Schacht Nr. oben": {
        "start_cell": "A7",
        "data_type": "str"
    },
    "Schacht Nr. unten": {
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
def to_xsls_haltung(column_assignments):
    csv_h = os.path.abspath('massen_haltungen.csv')
    csv_s = os.path.abspath('massen_schacht.csv')
    csv_l = os.path.abspath('massen_leitung.csv')
    src = os.path.abspath('massen_util/src/massen.xlsx')
    print(src)
    wb = xl.load_workbook(src)
    ws_haltung = wb["Massen_Haltung"]
    ws_leitung = wb["Massen_Leitung"]
    ws_schacht = wb["Massen_Schacht"]

    df_s = pd.read_csv(csv_s)
    df_h = pd.read_csv(csv_h)

    column_lists = {
    "Status": df_h["Status"].tolist(),
    "Schacht Nr. oben": df_h["Schacht Nr. oben"].tolist(),
    "Schacht Nr. unten": df_h["Schacht Nr. unten"].tolist(),
    "Deckelhoehe oben": df_h["Deckelhoehe oben"].tolist(),
    "Deckelhoehe unten": df_h["Deckelhoehe unten"].tolist(),
    "Sohlhoehe oben": df_h["Sohlhoehe oben"].tolist(),
    "Sohlhoehe unten": df_h["Sohlhoehe unten"].tolist(),
    "Laenge": df_h["Laenge"].tolist(),
    "DN": df_h["DN"].tolist(),
    }
    for col_name, assignment in column_assignments.items():
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

    wb.save('massen_haltungen.xlsx')
    return print("Data successfully written to your XLS file!")

