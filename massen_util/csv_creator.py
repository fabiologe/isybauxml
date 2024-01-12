import csv


def export_to_csv(massen_haltung_unique, massen_index_haltung):
    with open('massen_haltungen.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=massen_index_haltung)
        writer.writeheader()
        writer.writerows(massen_haltung_unique) 

def export_leitung(massen_leitung, massen_index_leitung):
    with open('massen_leitung.csv', mode='w', newline='', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=massen_index_leitung)
        writer.writeheader()
        writer.writerows(massen_leitung)  