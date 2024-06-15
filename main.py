from xml_parser import *
from massen_util.merge_elements import mass_haltung, find_status, mass_leitung, mass_schacht
from massen_util.pyexcel import to_xsls_haltung, col_haltung, col_schacht , col_leitung
from massen_util.csv_creator import to_csv_haltung, to_csv_leitung, to_csv_schacht
from hydraulik.forge_inp import create_inp, SimulationMetadata
from hydraulik.run_simulation import default_sim, default_plot
from orientation.validate_CRS import find_CRS
import xml.dom.minidom
import sys
import codecs
import os








def main():
    file_path = "input/Stammdaten_ISY.xml"
    if file_path:
        with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
            xml_content = file.read()
        
        # Apply umlaut mapping (if needed)
        fixed_content = umlaut_mapping(xml_content)
        
        # Fix the content to remove unwanted patterns
        fixed_content = bauwerk_fix(fixed_content)

        fixed_content = DN_bug(fixed_content)
        
        # Ensure the fixed content is a string
        if isinstance(fixed_content, bytes):
            fixed_content = fixed_content.decode('ISO-8859-1')
        
        # Parse the fixed XML content
        try:
            dom = parseString(fixed_content)
            print(dom.toprettyxml())
        except Exception as e:
            print(f"Error parsing XML: {e}")
        
        # Parse the fixed XML content
        dom = xml.dom.minidom.parseString(fixed_content)
        
        # Replace umlauts in the parsed DOM
        replace_umlaut(dom)
        update_punkthoehe(dom)
        update_haltunghoehe(dom)
        delete_incomplete_points(dom)
        replace_umlaut(dom)

        root = dom.documentElement
        analysis_results = analyze_xml(root)
        print(analysis_results)
        parse_all(root) 
        print(len(schacht_list))
        #transform_crs(dom)

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
        for data_list in all_lists:
            data_list = kill_duplicates(data_list, 'objektbezeichnung')  
        mass_haltung_res = mass_haltung(schacht_list,bauwerke_list, haltung_list)
        to_csv_haltung(mass_haltung_res)
        mass_schacht_res = mass_schacht(schacht_list, haltung_list)
        to_csv_schacht(mass_schacht_res)
        massen_leitung_res = mass_leitung(leitung_list)
        to_csv_leitung(massen_leitung_res)
        print(os.getcwd())
        to_xsls_haltung(col_haltung, col_schacht , col_leitung)
        '''metadata = SimulationMetadata("Kohn's Wasserwirtschaft", "Fabio Q.")
        create_inp(metadata, flaechen_list, schacht_list,haltung_list, bauwerke_list)
        default_sim()
        default_plot(schacht_list)'''
        sys.exit()


if __name__ == "__main__":
    main()  

        
    
