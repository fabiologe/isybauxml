from xml_parser import *

def parse_all(root):
    parse_schacht(root)
    parse_haltung(root)
    parse_leitung(root)
   
    
    parse_behandlungsanlage(root)
    parse_becken(root)
    parse_auslaufbauwerk(root)
    parse_pumpe(root)
    parse_klaeranlage(root)
    parse_drossel(root)
    parse_wehr(root)
    parse_schieber(root)
    parse_versickerungsanlage(root)
    parse_regenwassernutzungsanlage(root)
    parse_einlaufbauwerk(root)
    #parse_bauwerk_dump(root)
    
    parse_anschlusspunkt(root)
    parse_flaeche(root)
    parse_einzugsgebiete(root)

all_lists = [
    schacht_list, haltung_list, leitung_list, bauwerk_list, anschlusspunkt_list,  flaechen_list, einzugsgebiete_list
]