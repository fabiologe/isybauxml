from xml_parser import *
from massen_util.merge_elements import merger, find_status, sum_lengths
from massen_util.csv_creator import export_leitung, export_to_csv
from hydraulik.forge_inp import create_inp, SimulationMetadata
import xml.dom.minidom
import sys
import codecs







def main():
    file_path = ("input/6096A6.xml")
    if file_path:
   
        with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
            dom = xml.dom.minidom.parse(file)
        root = dom.documentElement
        update_punkthoehe(dom)
        update_haltunghoehe(dom)
        delete_incomplete_points(dom)
        analysis_results = analyze_xml(root)
        print(analysis_results)
        parse_all(root) 
        print(len(schacht_list))

        #schacht_manager = SchachtManager(schacht_list)


        
        #result = schacht_manager.print_punkte(objektbezeichnung="R1234")


        #print(result)


        '''for schacht in schacht_list:
            print(len(schacht.knoten[0].punkte))
            print(schacht.knoten[0].punkte[0].x)
            print(schacht.knoten[0].punkte[0].y)
            print(schacht.knoten[0].punkte[0].z)
            print(schacht.knoten[0].punkte[1].x)
            print(schacht.knoten[0].punkte[1].y)
            print(schacht.knoten[0].punkte[1].z)'''
        '''for data_list in all_lists:
            data_list = kill_duplicates(data_list, 'objektbezeichnung')  
        massen_haltung_unique = merger(schacht_list, haltung_list)
        massen_index_haltung = ['Status','Schacht Nr. oben', 'Schacht Nr. unten', 'Deckelhoehe oben', 'Deckelhoehe unten',
                        'Sohlhoehe oben', 'Sohlhoehe unten', 'Laenge', 'DN']
        massen_index_leitung = ['Status','DN','Rohrlaenge']
        export_to_csv(massen_haltung_unique, massen_index_haltung)
        massen_leitung = sum_lengths(leitung_list)
        massen_leitung
        export_leitung(massen_leitung, massen_index_leitung)'''
        metadata = SimulationMetadata("Kohn's Wasserwirtschaft", "Fabio Q.")
        create_inp(metadata, flaechen_list, schacht_list, bauwerke_list)
        
        sys.exit()


if __name__ == "__main__":
    main()  

        
    
