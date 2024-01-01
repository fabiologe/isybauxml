
from typing import Optional, Union
from dataclasses import dataclass
from typing import List

schacht_list = []
@dataclass
class Schacht:
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.status: Optional[Union[str, int]] = None
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        #Geometrie Schaechtelement:
        self.aufbauform:Optional[str] = None
        self.konus: Optional[bool] = None
        self.laenge_aufbau: Optional[float] = None
        self.breite_aufbau: Optional[float] = None
        self.hoehe_aufbau: Optional[float] = None
        self.material: Optional[str] = None
        #weiters:
        self.schacht_funktion: Optional[str] = None
        self.schachttiefe: Optional[float] = None
        self.einstieghilfe: Optional[bool] = None
        self.art_einstieghilfe: Optional[str] = None
        self.material_steighilfen: Optional[str] = None
        self.innenschutz: Optional[str] = None
        self.anzahl_anschluesse: Optional[int] = None
        self.uebergabeschacht: Optional[bool] = None
        self.auflagering: Optional[str] = None
        self.aufbau: Optional[str] = None
        self.untere_schachtzone: Optional[str] = None
        self.unterteil: Optional[str] = None
    def add_knoten(self, punkt):
        self.knoten.append(punkt)
    def __str__(self):
        return f"Schachtbezeichnung: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nAufbauform: {self.aufbauform}\nSchachtFunktion: {self.schacht_funktion}"
    def get_coordinates(self) -> List[List[float]]:
        coordinates = []
        for knoten in self.knoten:
            for punkt in knoten.punkte:
                coordinates.append([punkt.x, punkt.y, punkt.z])
        return coordinates


@dataclass
class Knoten:
    def __init__(self):
        self.punkte = []
        self.tag = str()
    def add_punkt(self, punkt):
        self.punkte.append(punkt)
    def __str__(self):
        punkte_str = ", ".join(str(punkt) for punkt in self.punkte)
        return f"Knoten(punkte=[{punkte_str},tag={self.tag})])"
@dataclass
class Punkt:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return f"Punkt(x={self.x}, y={self.y}, z={self.z})"
def parse_schacht(root):
    # Extract the data into custom classes
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 0:
                        schacht = Schacht()
                        objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                        if objektbezeichnung_element:
                            schacht.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                        entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                        if entwaesserungsart_element:
                            schacht.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                        status_element = abwasser_objekt.getElementsByTagName('Status')
                        if status_element:
                            schacht.status= status_element[0].firstChild.nodeValue
                        baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                        if baujahr_element:
                            schacht.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                        geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                        if geo_objektart_element:
                            schacht.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                        geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                        if geo_objekttyp_element:
                            schacht.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                        lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                        if lagegenauigkeitsklasse_element:
                            schacht.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                        hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                        if hoehengenauigkeitsklasse_element:
                            schacht.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                        schacht_funktion_element = abwasser_objekt.getElementsByTagName('SchachtFunktion')
                        if schacht_funktion_element:
                            schacht.schacht_funktion = schacht_funktion_element[0].firstChild.nodeValue
                        aufbauform_element = abwasser_objekt.getElementsByTagName('Aufbauform')
                        if aufbauform_element:
                            schacht.aufbauform = aufbauform_element[0].firstChild.nodeValue
                        konus_element = abwasser_objekt.getElementsByTagName('Konus')
                        if konus_element:
                            schacht.konus = konus_element[0].firstChild.nodeValue == 'true'
                        laenge_aufbau_element = abwasser_objekt.getElementsByTagName('LaengeAufbau')
                        if laenge_aufbau_element:
                            schacht.laenge_aufbau = float(laenge_aufbau_element[0].firstChild.nodeValue)
                        breite_aufbau_element = abwasser_objekt.getElementsByTagName('BreiteAufbau')
                        if breite_aufbau_element:
                            schacht.breite_aufbau = float(breite_aufbau_element[0].firstChild.nodeValue)
                        hoehe_aufbau_element = abwasser_objekt.getElementsByTagName('HoeheAufbau')
                        if hoehe_aufbau_element:
                            schacht.hoehe_aufbau = float(hoehe_aufbau_element[0].firstChild.nodeValue)
                        material_element = abwasser_objekt.getElementsByTagName('Material')
                        if material_element:
                            schacht.material = material_element[0].firstChild.nodeValue
                        schachttiefe_element = abwasser_objekt.getElementsByTagName('Schachttiefe')
                        if schachttiefe_element:
                            schacht.schachttiefe = float(schachttiefe_element[0].firstChild.nodeValue)
                        einstieghilfe_element = abwasser_objekt.getElementsByTagName('Einstieghilfe')
                        if einstieghilfe_element:
                            schacht.einstieghilfe = einstieghilfe_element[0].firstChild.nodeValue == 'true'
                        art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('ArtEinstieghilfe')
                        if art_einstieghilfe_element:
                            schacht.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                        material_steighilfen_element = abwasser_objekt.getElementsByTagName('MaterialSteighilfen')
                        if material_steighilfen_element:
                            schacht.material_steighilfen = material_steighilfen_element[0].firstChild.nodeValue
                        innenschutz_element = abwasser_objekt.getElementsByTagName('Innenschutz')
                        if innenschutz_element:
                            schacht.innenschutz = innenschutz_element[0].firstChild.nodeValue
                        anzahl_anschluesse_element = abwasser_objekt.getElementsByTagName('AnzahlAnschluesse')
                        if anzahl_anschluesse_element:
                            schacht.anzahl_anschluesse = int(anzahl_anschluesse_element[0].firstChild.nodeValue)
                        uebergabeschacht_element = abwasser_objekt.getElementsByTagName('Uebergabeschacht')
                        if uebergabeschacht_element:
                            schacht.uebergabeschacht = uebergabeschacht_element[0].firstChild.nodeValue == 'true'
                        auflagering_element = abwasser_objekt.getElementsByTagName('Auflagering')
                        if auflagering_element:
                            schacht.auflagering = auflagering_element[0].firstChild.nodeValue
                        aufbau_element = abwasser_objekt.getElementsByTagName('Aufbau')
                        if aufbau_element:
                            schacht.aufbau = aufbau_element[0].firstChild.nodeValue
                        #untere_schachtzone_element = abwasser_objekt.getElementsByTagName('UntereSchachtzone')
                        #if untere_schachtzone_element:
                        #   schacht.untere_schachtzone = untere_schachtzone_element[0].firstChild.nodeValue
                        #unterteil_element = abwasser_objekt.getElementsByTagName('Unterteil')
                        #if unterteil_element:
                        #    schacht.unterteil = unterteil_element[0].firstChild.nodeValue
                        for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                            punkt_elements = knoten_element.getElementsByTagName('Punkt')
                            if punkt_elements:
                                knoten = Knoten()
                                for punkt_element in punkt_elements:
                                    punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                  y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                  z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                    punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                    knoten.add_punkt(punkt)
                                schacht.add_knoten(knoten)
                        schacht_list.append(schacht)
    # Debug statement to check if schacht_list is empty
    print(f"Number of Schacht objects: {len(schacht_list)}")
    print(f"Number of unique Schacht: {len(set(s.objektbezeichnung for s in schacht_list))}")
    return schacht_list
