from xml_parser import *
import xml.dom.minidom
import sys
import codecs
import os

def main():
    file_path = ("input/Stammdaten_ISY.xml")
    if file_path:
   
        with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
            dom = xml.dom.minidom.parse(file)
        root = dom.documentElement
        update_punkthoehe(dom)
        update_haltunghoehe(dom)
        #DN_bug(dom)
        delete_incomplete_points(dom)
        analysis_results = analyze_xml(root)
        print(analysis_results)
        parse_all(root) 
        print(len(schacht_list))
        transform_crs(dom)

        
        sys.exit()


if __name__ == "__main__":
    main()  
