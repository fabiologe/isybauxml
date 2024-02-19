from typing import Optional, Union
from dataclasses import dataclass

anschlusspunkt_list = []
@dataclass
class Knoten:
    def __init__(self):
        self.punkte = []
    def add_punkt(self, punkt):
        self.punkte.append(punkt)
    def __str__(self):
        punkte_str = ", ".join(str(punkt) for punkt in self.punkte)
        return f"Knoten(punkte=[{punkte_str}])"
@dataclass
class Punkt:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.tag = str()
    def __str__(self):
        return f"Punkt(x={self.x}, y={self.y}, z={self.z}, tag={self.tag})"
@dataclass
class Anschlusspunkt:
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.status: Optional[Union[str,int]] = None
        #Objektspezifische Attribute:
        self.punktkennung: Optional[str]= None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
def parse_anschlusspunkt(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 1:
                        anschlusspunkt = Anschlusspunkt()
                        objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                        if objektbezeichnung_element:
                            anschlusspunkt.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                        status_element = abwasser_objekt.getElementsByTagName('Status')
                        if status_element:
                            anschlusspunkt.status= status_element[0].firstChild.nodeValue
                        entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                        if entwaesserungsart_element:
                            anschlusspunkt.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                        punktkennnung_element = abwasser_objekt.getElementsByTagName('Punktkennung')
                        if punktkennnung_element:
                            anschlusspunkt.punktkennung = punktkennnung_element[0].firstChild.nodeValue
                        punkt_elements = abwasser_objekt.getElementsByTagName('Punkt')
                        if punkt_elements:
                                knoten = Knoten()
                                punkt = Punkt(x=abwasser_objekt.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                  y=abwasser_objekt.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                  z=abwasser_objekt.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                punkt.tag_element = abwasser_objekt.getElementsByTagName('PunktattributAbwasser')
                                if punkt.tag_element:
                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                knoten.add_punkt(punkt)
                                anschlusspunkt.add_knoten(knoten)
                        anschlusspunkt_list.append(anschlusspunkt)
    print(f"Number of Anschluss objects: {len(anschlusspunkt_list)}")
    print('\n')
    #print(f"Number of unique Anschlusspunkte: {len(set(h.objektbezeichnung for h in anschlusspunkt_list))}")
    return anschlusspunkt_list
