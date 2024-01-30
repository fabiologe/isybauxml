from dataclasses import dataclass
from typing import Optional

einzugsgebiete_list = []
@dataclass
class einzugsgebiete:
    gebietskennung: Optional[str] = None
    gebietsname: Optional[str] = None
    kommentar: Optional[str] = None
    einwohner: Optional[float] = None
    einwohnerwerte: Optional[str] = None
    einwohnerdichte: Optional[float] = None # E/hages
    trockenwetterkennung: Optional[str] = None

def parse_einzugsgebiete(root):
    # Extract the data into custom classes
    for einzugsgebiet_objekt in root.getElementsByTagName('Einzugsgebiet'):
        einzugsgebiet = einzugsgebiete()
        gebietskennung_element = einzugsgebiet_objekt.getElementsByTagName('Gebietskennung')
        if gebietskennung_element:
            einzugsgebiet.gebietskennung = str(gebietskennung_element[0].firstChild.nodeValue)
        gebietsname_element = einzugsgebiet_objekt.getElementsByTagName('Gebietsname')
        if gebietsname_element:
            einzugsgebiet.gebietsname = str(gebietsname_element[0].firstChild.nodeValue)
        kommentart_element = einzugsgebiet_objekt.getElementsByTagName('Kommentar')
        if kommentart_element: 
            einzugsgebiet.kommentar = str(einzugsgebiet_objekt[0].firstChild.nodeValue)
        einwohnerwerte_element = einzugsgebiet_objekt.getElementsByTagName('Einwohnerwerte')
        if einwohnerwerte_element:
            einzugsgebiet.einwohnerwerte = float(einzugsgebiet_objekt[0].firstChild.nodeValue)
        einwohnerdichte_element = einzugsgebiet_objekt.getElementsByTagName('Einwohnerdichte')
        if einwohnerdichte_element:
            einzugsgebiet.einwohnerdichte = float(einzugsgebiet_objekt[0].firstChild.nodeValue)
        trockenwetterkennung_element = einzugsgebiet_objekt.getElementsByTagName('Trockenwetterkennung')
        if trockenwetterkennung_element:
            einzugsgebiet.trockenwetterkennung = str(einzugsgebiet_objekt[0].firstChild.nodeValue)
        
        einzugsgebiete_list.append(einzugsgebiet)
    return einzugsgebiete_list
