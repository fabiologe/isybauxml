from xml_parser import *
from massen_util.merge_elements import mass_haltung, find_status, mass_leitung, mass_schacht, mass_bauwerk
from massen_util.pyexcel import to_xsls_haltung, col_haltung, col_schacht , col_leitung, col_bauwerk
from massen_util.csv_creator import to_csv_haltung, to_csv_leitung, to_csv_schacht, to_csv_bauwerk
import xml.dom.minidom
import codecs
import os





def process_xml_to_xsls(schacht_list, bauwerk_list, haltung_list):
        mass_haltung_res = mass_haltung(schacht_list, bauwerk_list, haltung_list)
        to_csv_haltung(mass_haltung_res)
        mass_schacht_res = mass_schacht(schacht_list, haltung_list)
        to_csv_schacht(mass_schacht_res)
        massen_leitung_res = mass_leitung(leitung_list)
        to_csv_leitung(massen_leitung_res)
        massen_bauwerk_res = mass_bauwerk(bauwerk_list)
        to_csv_bauwerk(massen_bauwerk_res)


        output_directory = "storage/output_xlsx_csv"
        haltung_file = os.path.join(output_directory, 'haltung.csv')
        schacht_file = os.path.join(output_directory, 'schacht.csv')
        leitung_file = os.path.join(output_directory, 'leitung.csv')
        bauwerk_file = os.path.join(output_directory, 'bauwerk.csv')
        xls_file = os.path.join(output_directory, 'haltung.xlsx')
        
        to_xsls_haltung(col_haltung, col_schacht, col_leitung, col_bauwerk)
        
        return {
            "haltung_file": haltung_file,
            "schacht_file": schacht_file,
            "leitung_file": leitung_file,
            "bauwerk_file": bauwerk_file,
            "xls_file": xls_file
        }