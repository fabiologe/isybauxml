import csv
from xml_parser import *

def to_csv_bauwerk(mass_bauwerk_res):
    mass_index_bauwerk = ["Status", "Bauwerk", "Bauwerkart", "Tiefe", "Breite OK", "Laenge OK", "Flaeche OK", "Flaeche UK", "Volumen 1", "Volumen 2"]
    print("DEBUG:")
    print(mass_bauwerk_res)
    with open('storage/output_xlsx_csv/massen_bauwerk.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=mass_index_bauwerk)
        writer.writeheader()
        writer.writerows(mass_bauwerk_res )
    
    print('CSV for Bauwerk has been saved.')
        
        
def to_csv_schacht(mass_schacht):
    mass_schacht_index= ["Schacht",	"Tiefe",	"DN Zulauf",	"DN Ablauf"]


    with open('storage/output_xlsx_csv/massen_schacht.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write the header row
        writer.writerow(mass_schacht_index)
        
        # Write the data rows
        for item in mass_schacht:
            writer.writerow([item.get(key, '') for key in mass_schacht_index])
    return print('CSV for Schaechte could be saved')

def to_csv_haltung(massen_haltung_unique):
    massen_index_haltung = ['Status','Knoten Nr. oben', 'Knoten Nr. unten', 'Deckelhoehe oben', 'Deckelhoehe unten','Sohlhoehe oben', 'Sohlhoehe unten', 'Laenge', 'DN']

    with open('storage/output_xlsx_csv/massen_haltungen.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=massen_index_haltung)
        writer.writeheader()
        writer.writerows(massen_haltung_unique) 
    return print('CSV for Haltungen could be saved')


def to_csv_leitung(massen_leitung):
    massen_index_leitung = ['Status','DN','Rohrlaenge']
    with open('storage/output_xlsx_csv/massen_leitung.csv', mode='w', newline='', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=massen_index_leitung)
        writer.writeheader()
        writer.writerows(massen_leitung)  
    return print('CSV for Leitungen could be saved')