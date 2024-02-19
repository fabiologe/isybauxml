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
    tag: Optional[str] = 'EZG'


@dataclass
class Ende:
    punkt: Punkt
    tag: Optional[str] = 'EZG'


@dataclass
class Kante:
    start: Start
    ende: Ende


@dataclass
class Polygon:
    kante: Kante
    points= []

@dataclass
class Flaeche:
    flaechennummer: Optional[int] = None
    objektbezeichnung: Optional[str] = None
    flaechenart: Optional[int] = None # 1= befestigt ; 2= teilbefestigt ; 3= unbefestigt ; 4= natürlich ; 5= keine Infos
    flaecheneigenschaften: Optional[int] = None
    flaechenfunktion : Optional[int] = None
    flaechennutzung: Optional[int] = None
    materialzusatz: Optional[int] = None
    verschmutzungsklasse: Optional[int] = None
    flaechengroesse: Optional[float] = None
    neigungsklasse: Optional[int] = None    # Need to translate to floats 
    abflussbeiwert: Optional[float] = 0
    kommentar: Optional[str] = None
    gebietskennung: Optional[str] = None
    polygon = []
    kanten = [] 
    schwerpunkt: Optional[Punkt] = None
    schwerpunktlaufzeit: Optional[float] = None
    kb_wert: Optional[float] = None
    kst_wert: Optional[float] = None
    #custome made attributes:
    vertices= []
    nodes= []
    hydro_vertices= []
    width: Optional[float] = None
    def add_polygon(self, polygon: Polygon):
        self.polygon.append(polygon)
    def add_kante(self, kante: Kante):
        self.kanten.append(kante)
    def calc_width(self, polygon):
        pass 
    '''For creating INP needs to calculate the width of the polygon'''

def parse_flaeche(root):
    # Extract the data into custom classes
    for flaeche_objekt in root.getElementsByTagName('Flaeche'):
        flaeche = Flaeche()
        flaechennummer_element = flaeche_objekt.getElementsByTagName('Flaechennummer')
        if flaechennummer_element:
            flaeche.flaechennummer = int(flaechennummer_element[0].firstChild.nodeValue)
        flaechenbezeichnung_element = flaeche_objekt.getElementsByTagName('Flaechenbezeichnung')
        if flaechenbezeichnung_element:
            flaeche.objektbezeichnung = str(flaechenbezeichnung_element[0].firstChild.nodeValue)
        flaechenart_element = flaeche_objekt.getElementsByTagName('Flaechenart')
        if flaechenart_element: 
            flaeche.flaechenart = int(flaechenart_element[0].firstChild.nodeValue)
        flaecheneigenschaften_element = flaeche_objekt.getElementsByTagName('Flaecheneigenschaft')
        if flaecheneigenschaften_element:
            flaeche.flaecheneigenschaften = int(flaecheneigenschaften_element[0].firstChild.nodeValue)
        flaechenfunktion_element = flaeche_objekt.getElementsByTagName('Flaechenfunktion')
        if flaechenfunktion_element:
            flaeche.flaechenfunktion = int(flaechenfunktion_element[0].firstChild.nodeValue)
        flaechennutzung_element = flaeche_objekt.getElementsByTagName('Flaechennutzung')
        if flaechennutzung_element:
            flaeche.flaechennutzung = int(flaechennutzung_element[0].firstChild.nodeValue)
        materialzusatz_element = flaeche_objekt.getElementsByTagName('Materialzusatz')
        if materialzusatz_element:
            flaeche.materialzusatz = int(materialzusatz_element[0].firstChild.nodeValue)
        verschmutzungsklasse_element = flaeche_objekt.getElementsByTagName('Verschmutzungsklasse')
        if verschmutzungsklasse_element:
            flaeche.verschmutzungsklasse = int(verschmutzungsklasse_element[0].firstChild.nodeValue)
        flaechengroesse_element = flaeche_objekt.getElementsByTagName('Flaechengroesse')
        if flaechengroesse_element:
            flaeche.flaechengroesse = float(flaechengroesse_element[0].firstChild.nodeValue)
        neigungsklasse_element = flaeche_objekt.getElementsByTagName('Neigungsklasse')
        if neigungsklasse_element:
            flaeche.neigungsklasse = int(neigungsklasse_element[0].firstChild.nodeValue)
        abflussbeiwert_element = flaeche_objekt.getElementsByTagName('Abflussbeiwert')
        if abflussbeiwert_element:
            flaeche.abflussbeiwert = float(abflussbeiwert_element[0].firstChild.nodeValue)
        kommentart_element = flaeche_objekt.getElementsByTagName('Kommentar')
        if kommentart_element:
            flaeche.kommentar = str(kommentart_element[0].firstChild.nodeValue)
        gebietskennung_element = flaeche_objekt.getElementsByTagName('Gebietskennung')
        if gebietskennung_element:
            flaeche.gebietskennung = str(gebietskennung_element[0].firstChild.nodeValue)       
        for polygon_element in flaeche_objekt.getElementsByTagName('Polygon'):  
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
                                        flaeche.add_kante(kante)
                                        polygon= Polygon(kante=kante)
                                        point_tuple = (punkt_s,punkt_e)
                                polygon.points.append(point_tuple)
                                flaeche.add_polygon(polygon)
        for hydro_objekt in flaeche_objekt.getElementsByTagName('HydraulikObjekt'):
            if hydro_objekt:
                hydro_vertices = hydro_objekt.getElementsByTagName('Objektbezeichnung')
                if hydro_vertices:
                    haltung_bez = str(hydro_vertices[0].firstChild.nodeValue)
                    flaeche.hydro_vertices.append(haltung_bez) 
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
    print(f"Number of Flaechen objects: {len(flaechen_list)}")
    print('\n')
    #print(f"Number of unique Flaechen: {len(set(f.objektbezeichnung for f in flaechen_list))}")
    return flaechen_list

@dataclass
class hoehenlinien:
    punkte: Optional[List[Punkt]] = None
    polygon: Optional[List[Polygon]] = None

    def create_conturs(flaechen_list, netz_punkt):
         pass