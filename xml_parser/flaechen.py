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
class Flaeche:
    flaechennummer: Optional[int] = None
    flaechenbezeichnung: Optional[str] = None
    objektbezeichnung: Optional[str] = None #Haltung_ID
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
    polygon= []
    kanten = [] 
    schwerpunkt: Optional[Punkt] = None
    schwerpunktlaufzeit: Optional[float] = None
    kb_wert: Optional[float] = None
    kst_wert: Optional[float] = None

    width: Optional[float] = None
    def add_polygon(self, kante: Kante):
        self.polygons.append(kante)
    def add_kante(self, kante: Kante):
        self.kanten.append(kante)
    def calc_width(self, polygon):
        pass 
    '''For creating INP needs to calculate the width of the polygon'''

def parse_flaeche(root):
    # Extract the data into custom classes
    print("\n[DEBUG] Starte Parsing der Flächen...")
    for flaeche_objekt in root.getElementsByTagName('Flaeche'):
        flaeche = Flaeche()
        print("\n[DEBUG] Verarbeite neue Fläche:")
        
        flaechennummer_element = flaeche_objekt.getElementsByTagName('Flaechennummer')
        if flaechennummer_element:
            flaeche.flaechennummer = int(flaechennummer_element[0].firstChild.nodeValue)
            print(f"  - Flaechennummer: {flaeche.flaechennummer}")
            
        flaechenbezeichnung_element = flaeche_objekt.getElementsByTagName('Flaechenbezeichnung')
        if flaechenbezeichnung_element:
            flaeche.flaechenbezeichnung = str(flaechenbezeichnung_element[0].firstChild.nodeValue)
            print(f"  - Flaechenbezeichnung: {flaeche.flaechenbezeichnung}")
            
        flaechenart_element = flaeche_objekt.getElementsByTagName('Flaechenart')
        if flaechenart_element: 
            flaeche.flaechenart = int(flaechenart_element[0].firstChild.nodeValue)
            print(f"  - Flaechenart: {flaeche.flaechenart}")
            
        flaechengroesse_element = flaeche_objekt.getElementsByTagName('Flaechengroesse')
        if flaechengroesse_element:
            flaeche.flaechengroesse = float(flaechengroesse_element[0].firstChild.nodeValue)
            print(f"  - Flaechengroesse: {flaeche.flaechengroesse} m²")
            
        abflussbeiwert_element = flaeche_objekt.getElementsByTagName('Abflussbeiwert')
        if abflussbeiwert_element:
            flaeche.abflussbeiwert = float(abflussbeiwert_element[0].firstChild.nodeValue)
            print(f"  - Abflussbeiwert: {flaeche.abflussbeiwert}")
            
        for hydro_objekt in flaeche_objekt.getElementsByTagName('HydraulikObjekt'):
            if hydro_objekt:
                hydro_bezeichung = hydro_objekt.getElementsByTagName('Objektbezeichnung')
                if hydro_bezeichung:
                    flaeche.objektbezeichnung = str(hydro_bezeichung[0].firstChild.nodeValue)
                    print(f"  - Objektbezeichnung (Haltung): {flaeche.objektbezeichnung}")
        
        flaechen_list.append(flaeche)
        print(f"[DEBUG] Fläche erfolgreich zur Liste hinzugefügt")
    
    print(f"\n[DEBUG] Gesamtanzahl der gefundenen Flächen: {len(flaechen_list)}")
    return flaechen_list
