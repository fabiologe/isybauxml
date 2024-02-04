
from typing import Optional, Union
from dataclasses import dataclass
from typing import List, Tuple

schacht_list = []
@dataclass
class Punkt:
    x: float
    y: float
    z: float
    def __str__(self):
        return f"Punkt(x={self.x}, y={self.y}, z={self.z})"
@dataclass
class Knoten:
    obj: Optional[str] = 'NA'
    tag: Optional[str] = 'S'
    punkte: List[Punkt] = None

    def add_punkt(self, *punkte: Punkt):
        if self.punkte is None:
            self.punkte = []
        self.punkte.extend(punkte)

    def __hash__(self):
        return hash(self.obj)
    
    def __eq__(self, other):
        return isinstance(other, Knoten) and self.obj == other.obj

@dataclass
class Start:
    punkt: Punkt
    tag: Optional[str] = 'S'


@dataclass
class Ende:
    punkt: Punkt
    tag: Optional[str] = 'S'


@dataclass
class Kante:
    start: Start
    ende: Ende
    
@dataclass
class Polygon:
    kante: Kante
    points= []
    
@dataclass
class Schacht:
    objektbezeichnung: Optional[str] = 'NOT-GIVEN'
    entwaesserungsart = Optional[str]
    status: Optional[Union[str, int]] = None
    baujahr: Optional[float]= None
    geo_objektart: Optional[int] = None
    geo_objekttyp: Optional[str]= None
    lagegenauigkeitsklasse: Optional[str]= None
    hoehengenauigkeitsklasse: Optional[int]= None
    knoten: Optional[List['Knoten']] = None
    kanten = []
    polygon = []
        #Geometrie Schaechtelement:
    aufbauform:Optional[str] = None
    konus: Optional[bool] = None
    laenge_aufbau: Optional[float] = None
    breite_aufbau: Optional[float] = None
    hoehe_aufbau: Optional[float] = None
    material: Optional[str] = None
        #weiters:
    schacht_funktion: Optional[str] = None
    schachttiefe: Optional[float] = None
    einstieghilfe: Optional[bool] = None
    art_einstieghilfe: Optional[str] = None
    material_steighilfen: Optional[str] = None
    innenschutz: Optional[str] = None
    anzahl_anschluesse: Optional[int] = None
    uebergabeschacht: Optional[bool] = None
    auflagering: Optional[str] = None
    aufbau: Optional[str] = None
    untere_schachtzone: Optional[str] = None
    unterteil: Optional[str] = None
    def add_knoten(self, knoten: 'Knoten'):
        if self.knoten is None:
            self.knoten = []
        self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
        self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
        self.polygon.append(polygon)

@dataclass
class SchachtManager:
    schacht_list: List[Schacht]

    def print_punkte(self, objektbezeichnung: str) -> List[Tuple[Knoten, List[Tuple[float, float, float]]]]:
        """
        Get the Knoten elements and corresponding Punkte for a given objektbezeichnung.
        
        Args:
            objektbezeichnung (str): The objektbezeichnung to search for.
        
        Returns:
            List[Tuple[Knoten, List[Tuple[float, float, float]]]]: A list of tuples containing Knoten elements and corresponding Punkte.
        """
        result = []
        for schacht in self.schacht_list:
            if schacht.objektbezeichnung == objektbezeichnung:
                knoten_punkte_dict = {}
                for knoten in schacht.knoten:
                    knoten_punkte = []
                    for punkt in knoten.punkte:
                        knoten_punkte.append((punkt.x, punkt.y, punkt.z))
                    knoten_punkte_dict[knoten] = knoten_punkte
                result.append(knoten_punkte_dict)
        return result
    
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
                        for aufbauform_element in aufbauform_element:
                            if aufbauform_element.firstChild.nodeValue in ['E', 'Z']:
                                    for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):  
                                        if polygon_element:
                                            for kanten_element in polygon_element.getElementsByTagName('Kante'):
                                                if kanten_element:
                                                    start_element = kanten_element.getElementsByTagName('Start')[0]
                                                    x = float(start_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue)
                                                    y = float(start_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue)
                                                    z = float(start_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                    punkt_s= Punkt(x=x, y=y, z=z)

                                                    start = Start(punkt=punkt_s)

                                                    ende_element = kanten_element.getElementsByTagName('Ende')[0]
                                                    x = float(ende_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue)
                                                    y = float(ende_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue)
                                                    z = float(ende_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                    punkt_e = Punkt(x=x, y=y, z=z)

                                                    ende = Ende(punkt=punkt_e)

                                                    kante = Kante(start=start, ende=ende)
                                                    schacht.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            schacht.add_polygon(polygon)
                        for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                            knoten = Knoten()
                            knoten.obj = str(objektbezeichnung_element[0].firstChild.nodeValue)
                            punkt_elements = knoten_element.getElementsByTagName('Punkt')
                            if punkt_elements:
                                for punkt_element in punkt_elements:
                                    punkt = Punkt( x = float(punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue),
                                                    y = float(punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue),
                                                    z = float(punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue))
                                    punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                    knoten.add_punkt(punkt)
                                schacht.add_knoten(knoten)
                        schacht_list.append(schacht)
    # Debug statement to check if schacht_list is empty
    print(f"Number of Schacht objects: {len(schacht_list)}")
    print(f"Number of unique Schacht: {len(set(s.objektbezeichnung for s in schacht_list))}")
    return schacht_list
