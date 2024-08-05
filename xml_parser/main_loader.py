from xml_parser import *
import codecs
import xml.dom.minidom

class XMLDataLoader:
    _instance = None
    _data = None

    def __new__(cls, file_path: str):
        if cls._instance is None:
            cls._instance = super(XMLDataLoader, cls).__new__(cls)
            cls._data = cls.load_xml(file_path)
        return cls._instance

    @staticmethod
    def load_xml(file_path: str) -> xml.dom.minidom.Document:
        if file_path:
            with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
                xml_content = file.read()
            
            fixed_content = umlaut_mapping(xml_content)
            fixed_content = bauwerk_fix(fixed_content)
            fixed_content = DN_bug(fixed_content)
        
            if isinstance(fixed_content, bytes):
                fixed_content = fixed_content.decode('ISO-8859-1')
            
            try:
                dom = xml.dom.minidom.parseString(fixed_content)
                print(dom.toprettyxml())
            except Exception as e:
                print(f"Error parsing XML: {e}")
                return None
            
            replace_umlaut(dom)
            update_punkthoehe(dom)
            update_haltunghoehe(dom)
            delete_incomplete_points(dom)
            replace_umlaut(dom)

            return dom
    @staticmethod
    def load_transform(file_path:str)-> xml.dom.minidom.Document:
        if file_path:
            with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
                xml_content = file.read()
            
            fixed_content = umlaut_mapping(xml_content)
            fixed_content = bauwerk_fix(fixed_content)
            fixed_content = DN_bug(fixed_content)
        
            if isinstance(fixed_content, bytes):
                fixed_content = fixed_content.decode('ISO-8859-1')
            
            try:
                dom = xml.dom.minidom.parseString(fixed_content)
                print(dom.toprettyxml())
            except Exception as e:
                print(f"Error parsing XML: {e}")
                return None
            
            replace_umlaut(dom)
            update_punkthoehe(dom)
            update_haltunghoehe(dom)
            delete_incomplete_points(dom)
            replace_umlaut(dom)
            transform_crs(dom)

            return dom


    def get_data(self):
        return self._data