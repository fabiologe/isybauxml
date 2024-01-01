
import codecs
from tkinter import messagebox
import xml.dom.minidom



xsd_files = ['xml_parser/source_xsd/1707-stammdaten.xsd',
             'xml_parser/source_xsd/1707-referemzlisten.xsd',
             'xml_parser/source_xsd/1707-betriebsdate.xsd',
             'xml_parser/source_xsd/1707-hydraulikdaten.xsd',
             'xml_parser/source_xsd/1707-geometriedaten.xsd']


schemas = []
def validate_schema():
    for xsd_file in xsd_files:
        with open(xsd_file, 'r') as xsdin:
            schema = xmlschema.XMLSchema(source=xsdin)
        schemas.append(schema)

    with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file_path:
        dom = xml.dom.minidom.parse(file_path)

    is_valid = True
    for schema in schemas:
        errors = schema.validate(dom)
        if errors:
            is_valid = False
            print(f"Validation errors in {schema.name}:")
            for error in errors:
                print(error)
            break

    if is_valid:
        messagebox.showinfo(f"Die ausgewählte XML-Datei ist valide:\n{file_path}")
    else:
        messagebox.showinfo(f"Die ausgewählte XML-Datei ist nicht valide:\n{file_path}")
