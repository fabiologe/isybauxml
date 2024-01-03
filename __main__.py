from xml_parser import *
from massen import *
from hydraulik.forge_inp import create_inp, SimulationMetadata
import xml.dom.minidom
import sys
import codecs







def main():
    file_path = r"input/Stammdaten_ISY.xml"
    if file_path:
   
        with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
            dom = xml.dom.minidom.parse(file)
        root = dom.documentElement
        update_punkthoehe(dom)
        update_haltunghoehe(dom)
        delete_incomplete_points(dom)
        parse_all(root) 
        

        for data_list in all_lists:
            data_list = kill_duplicates(data_list, 'objektbezeichnung')  
        massen_haltung_unique = merger(schacht_list, haltung_list)
        massen_index_haltung = ['Status','Schacht Nr. oben', 'Schacht Nr. unten', 'Deckelhoehe oben', 'Deckelhoehe unten',
                        'Sohlhoehe oben', 'Sohlhoehe unten', 'Laenge', 'DN']
        massen_index_leitung = ['Status','DN','Rohrlaenge']
        export_to_csv(massen_haltung_unique, massen_index_haltung)
        massen_leitung = sum_lengths(leitung_list)
        massen_leitung
        export_leitung(massen_leitung, massen_index_leitung)
        metadata = SimulationMetadata("Kohn's Wasserwirtschaft", "Fabio Q.")

        create_inp(metadata)
        
        sys.exit()




if __name__ == "__main__":
    main()  

        
    
