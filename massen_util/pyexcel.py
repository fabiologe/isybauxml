import openpyxl as xl
import pandas as pd
import os 

csv = 'isybauxml/massen_haltungen.csv'
src = 'isybauxml/massen_util/src/src_haltung.xlsx'

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
    csv = os.path.abspath('massen_haltungen.csv')
    src = os.path.abspath('massen_util/src/src_haltung.xlsx')
    print(src)
    wb = xl.load_workbook(src)
    ws = wb["Massen_Haltung"]
    df = pd.read_csv(csv)
    column_lists = {
    "Status": df["Status"].tolist(),
    "Schacht Nr. oben": df["Schacht Nr. oben"].tolist(),
    "Schacht Nr. unten": df["Schacht Nr. unten"].tolist(),
    "Deckelhoehe oben": df["Deckelhoehe oben"].tolist(),
    "Deckelhoehe unten": df["Deckelhoehe unten"].tolist(),
    "Sohlhoehe oben": df["Sohlhoehe oben"].tolist(),
    "Sohlhoehe unten": df["Sohlhoehe unten"].tolist(),
    "Laenge": df["Laenge"].tolist(),
    "DN": df["DN"].tolist(),
}
    for col_name, assignment in column_assignments.items():
        data_list = df[col_name].tolist()  # Extract data list from DataFrame

        # Convert starting cell to row and column indices
        start_row, start_col = xl.utils.coordinate_to_tuple(assignment["start_cell"])

        # Ensure start_row and start_col are at least 1
        start_row = max(start_row, 1)
        start_col = max(start_col, 1)

        # Iterate through data and write to appropriate cells
        for row_idx, value in enumerate(data_list):
            # Apply correct data type formatting before writing
            if assignment["data_type"] == "str":
                cell_value = str(value)
            else:
                cell_value = float(value)

            # Write to the cell based on row and column offset
            ws.cell(row=row_idx + start_row, column=start_col).value = cell_value

    wb.save('massen_haltungen.xlsx')
    return print("Data successfully written to your XLS file!")


def to_xsls_schacht():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv('massen_haltungen.csv')
    # Iterate through each column containing "Schacht Nr. oben"
    for col_oben in df.filter(like="Schacht Nr. oben"):
        # Sort the column alphabetically
        df[col_oben] = df[col_oben].sort_values()
    
    # Iterate through each column containing "Schacht Nr. unten"
    for col_unten in df.filter(like="Schacht Nr. unten"):
        # Sort the column alphabetically
        df[col_unten] = df[col_unten].sort_values()
    
    # Output to CSV
    df.to_csv("sorted_data.csv", index=False)
    
    print("Sorted data saved to sorted_data.csv")
