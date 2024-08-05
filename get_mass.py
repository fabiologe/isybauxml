from xml_parser import *
from massen_util.merge_elements import mass_haltung, find_status, mass_leitung, mass_schacht
from massen_util.pyexcel import to_xsls_haltung, col_haltung, col_schacht , col_leitung
from massen_util.csv_creator import to_csv_haltung, to_csv_leitung, to_csv_schacht
import xml.dom.minidom
import codecs
import os





def process_xml_to_xsls(schacht_list, bauwerke_list, haltung_list):
        mass_haltung_res = mass_haltung(schacht_list, bauwerke_list, haltung_list)
        to_csv_haltung(mass_haltung_res)
        mass_schacht_res = mass_schacht(schacht_list, haltung_list)
        to_csv_schacht(mass_schacht_res)
        massen_leitung_res = mass_leitung(leitung_list)
        to_csv_leitung(massen_leitung_res)
        
        output_directory = "output_xlsx_csv"
        haltung_file = os.path.join(output_directory, 'haltung.csv')
        schacht_file = os.path.join(output_directory, 'schacht.csv')
        leitung_file = os.path.join(output_directory, 'leitung.csv')
        xls_file = os.path.join(output_directory, 'haltung.xlsx')
        
        to_xsls_haltung(col_haltung, col_schacht, col_leitung)
        
        return {
            "haltung_file": haltung_file,
            "schacht_file": schacht_file,
            "leitung_file": leitung_file,
            "xls_file": xls_file
        }