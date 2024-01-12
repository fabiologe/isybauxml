from dataclasses import dataclass
from typing import Optional, List
flaechen_list = []

flaechen_punkt = []
@dataclass
class Punkt:
    x: float
    y: float
    z: float


@dataclass
class Start:
    punkt: Punkt
    tag: str


@dataclass
class Ende:
    punkt: Punkt
    tag: str


@dataclass
class Kante:
    start: Start
    ende: Ende


@dataclass
class Polygon:
    kante: Kante

@dataclass
class Flaeche:
    flaechennummer: Optional[int] = None
    flaechenbezeichnung: Optional[str] = None
    flaechenart: Optional[int] = None # 1= befestigt ; 2= teilbefestigt ; 3= unbefestigt ; 4= natürlich ; 5= keine Infos
    flaecheneigenschaften: Optional[int] = None
    flaechenfunktion : Optional[int] = None
    flaechennutzung: Optional[int] = None
    materialzusatz: Optional[int] = None
    verschmutzungsklasse: Optional[int] = None
    flaechengroesse: Optional[float] = None
    neigungsklasse: Optional[int] = None
    abflussbeiwert: Optional[float] = None
    kommentar: Optional[str] = None
    gebietskennung: Optional[str] = None
    polygon: Optional[List] = None
    kante: Optional[List] = None    
    schwerpunkt: Optional[Punkt] = None
    schwerpunktlaufzeit: Optional[float] = None
    kb_wert: Optional[float] = None
    kst_wert: Optional[float] = None
    #custome made attributes:
    vertices: Optional[List] = None
    nodes: Optional[List] = None
    def add_polygon(self, polygon: Polygon):
        self.polygon.append(polygon)
    def add_kante(self, kante: Kante):
        self.kante.append(kante)

def parse_flaeche(root):
    # Extract the data into custom classes
    for flaeche_objekt in root.getElementsByTagName('Flaechen'):
        flaeche = Flaeche()
        flaechennummer_element = flaeche_objekt.getElementsByTagName('Flaechennummer')
        if flaechennummer_element:
            flaeche.flaechennummer = int(flaechennummer_element[0].firstChild.nodeValue)
        flaechenbezeichnung_element = flaeche_objekt.getElementsByTagName('Flaechenbezeichnung')
        if flaechenbezeichnung_element:
            flaeche.flaechenbezeichnung = str(flaechenbezeichnung_element[0].firstChild.nodeValue)
        flaechenart_element = flaeche_objekt.getElementsByTagName('Flaechenart')
        if flaechenart_element: 
            flaeche.flaechenart = int(flaeche_objekt[0].firstChild.nodeValue)
        flaecheneigenschaften_element = flaeche_objekt.getElementsByTagName('Flaecheneigenschaft')
        if flaecheneigenschaften_element:
            flaeche.flaecheneigenschaften = int(flaeche_objekt[0].firstChild.nodeValue)
        flaechenfunktion_element = flaeche_objekt.getElementsByTagName('Flaechenfunktion')
        if flaechenfunktion_element:
            flaeche.flaechenfunktion = int(flaeche_objekt[0].firstChild.nodeValue)
        flaechennutzung_element = flaeche_objekt.getElementsByTagName('Flaechennutzung')
        if flaechennutzung_element:
            flaeche.flaechennutzung = int(flaeche_objekt[0].firstChild.nodeValue)
        materialzusatz_element = flaeche_objekt.getElementsByTagName('Materialzusatz')
        if materialzusatz_element:
            flaeche.materialzusatz = int(flaeche_objekt[0].firstChild.nodeValue)
        verschmutzungsklasse_element = flaeche_objekt.getElementsByTagName('Verschmutzungsklasse')
        if verschmutzungsklasse_element:
            flaeche.verschmutzungsklasse = int(flaeche_objekt[0].firstChild.nodeValue)
        flaechengroesse_element = flaeche_objekt.getElementsByTagName('Flaechengroesse')
        if flaechengroesse_element:
            flaeche.flaechengroesse = float(flaeche_objekt[0].firstChild.nodeValue)
        neigungsklasse_element = flaeche_objekt.getElementsByTagName('Neigungsklasse')
        if neigungsklasse_element:
            flaeche.neigungsklasse = int(flaeche_objekt[0].firstChild.nodeValue)
        abflussbeiwert_element = flaeche_objekt.getElementsByTagName('Abflussbeiwert')
        if abflussbeiwert_element:
            flaeche.abflussbeiwert = float(flaeche_objekt[0].firstChild.nodeValue)
        kommentart_element = flaeche_objekt.getElementsByTagName('Kommentar')
        if kommentart_element:
            flaeche.kommentar = str(flaeche_objekt[0].firstChild.nodeValue)
        gebietskennung_element = flaeche_objekt.getElementsByTagName('Gebietskennung')
        if gebietskennung_element:
            flaeche.gebietskennung = str(flaeche_objekt[0].firstChild.nodeValue)       
        for polygon_element in flaeche_objekt.getElementsByTagName('Polygon'):  
                            if polygon_element:
                                for kanten_element in polygon_element.getElementsByTagName('Kante'):
                                    if kanten_element:
                                        start_element = kanten_element.getElementsByTagName('Start')[0]
                                        x = float(start_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue)
                                        y = float(start_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue)
                                        z = float(start_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt = Punkt(x=x, y=y, z=z)
                                        flaechen_punkt.append(punkt)
                                        tag = start_element.getElementsByTagName('PunktattributAbwasser')[0].firstChild.nodeValue
                                        start = Start(punkt=punkt, tag=tag)

                                        ende_element = kanten_element.getElementsByTagName('Ende')[0]
                                        x = float(ende_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue)
                                        y = float(ende_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue)
                                        z = float(ende_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt = Punkt(x=x, y=y, z=z)
                                        flaechen_punkt.append(punkt)
                                        tag = ende_element.getElementsByTagName('PunktattributAbwasser')[0].firstChild.nodeValue
                                        ende = Ende(punkt=punkt, tag=tag)

                                        kante = Kante(start=start, ende=ende)
                                        flaeche.add_kante(kante)
                                polygon = Polygon(kante=kante)
                                flaeche.add_polygon(polygon)
        schwerpunktlaufzeit_element = flaeche_objekt.getElementsByTagName('Schwerpunktlaufzeit')
        if schwerpunktlaufzeit_element:
             flaeche.schwerpunktlaufzeit = float(flaeche_objekt[0].firstChild.nodeValue)
        kb_wert_element = flaeche_objekt.getElementsByTagName('RauigkeitsbeiwertKb')
        if kb_wert_element:
             flaeche.kb_wert = float(flaeche_objekt[0].firstChild.nodeValue)
        kst_wert_element = flaeche_objekt.getElementsByTagName('RauigkeitsbeiwertKst')
        if kst_wert_element:
             flaeche.kst_wert = float(flaeche_objekt[0].firstChild.nodeValue)
        flaechen_list.append(flaeche)

@dataclass
class hoehenlinien:
    punkte: Optional[List[Punkt]] = None
    polygon: Optional[List[Polygon]] = None

    def create_conturs(flaechen_list, netz_punkt):
         pass