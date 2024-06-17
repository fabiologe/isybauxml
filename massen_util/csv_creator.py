import csv
from xml_parser import *

def to_csv_bauwerke(bauwerke_list):
    for bauwerk in bauwerke_list:
        name = bauwerk.objektbezeichnung
        dh = bauwerk.knoten[0].punkte[0].z
        sh = bauwerk.knoten[0].punkte[1].z
        typ = bauwerk.classname
        typ_str = bauwerktypENUM(typ)
        
def to_csv_schacht(mass_schacht):
    mass_schacht_index = list(mass_schacht[0].keys())
    additional_columns = [key for key in mass_schacht_index if key.startswith('DN XY')]

    mass_schacht_index.extend(additional_columns)

    with open('massen_schacht.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write the header row
        writer.writerow(mass_schacht_index)
        
        # Write the data rows
        for item in mass_schacht:
            writer.writerow([item.get(key, '') for key in mass_schacht_index])
    return print('CSV for Schaechte could be saved')

def to_csv_haltung(massen_haltung_unique):
    massen_index_haltung = ['Status','Knoten Nr. oben', 'Knoten Nr. unten', 'Deckelhoehe oben', 'Deckelhoehe unten','Sohlhoehe oben', 'Sohlhoehe unten', 'Laenge', 'DN']

    with open('massen_haltungen.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=massen_index_haltung)
        writer.writeheader()
        writer.writerows(massen_haltung_unique) 
    return print('CSV for Haltungen could be saved')


def to_csv_leitung(massen_leitung):
    massen_index_leitung = ['Status','DN','Rohrlaenge']
    with open('massen_leitung.csv', mode='w', newline='', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=massen_index_leitung)
        writer.writeheader()
        writer.writerows(massen_leitung)  
    return print('CSV for Leitungen could be saved')