
from typing import Optional, Union
from dataclasses import dataclass
from typing  import List
import string
import random
bauwerke_list = []
def generate_unique_id(length=7) -> str:
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choices(characters, k=length))
    return unique_id

'''NOT FINISHED YET'''
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
class Pumpwerk:   #1
        objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
        hersteller_typ: Optional[str] = None
        adresse_hersteller: Optional[str] = None
        ufis_baunummer: Optional[int] = None
        art_einstieghilfe: Optional[str] = None
        uebergabebauwerk: Optional[bool] = None
        grundflaeche: Optional[float]= None
        max_laenge: Optional[float]= None
        max_breite: Optional[float]= None
        max_hoehe: Optional[float]= None
        raum_hochbau: Optional[float]= None
        raum_tiefbau:Optional[float]= None
        def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
        def add_kante(self, kante: Kante):
            self.kanten.append(kante)
        def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)
def parse_pumpwerk(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element= abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element == 1:
                            pumpwerk = Pumpwerk()
                            objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                            if objektbezeichnung_element:
                                pumpwerk.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                            entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                            if entwaesserungsart_element:
                                pumpwerk.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                            status_element = abwasser_objekt.getElementsByTagName('Status')
                            if status_element:
                                pumpwerk.status= status_element[0].firstChild.nodeValue
                            baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                            if baujahr_element:
                                pumpwerk.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                            geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                            if geo_objektart_element:
                                pumpwerk.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                            geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                            if geo_objekttyp_element:
                                pumpwerk.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                            lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                            if lagegenauigkeitsklasse_element:
                                pumpwerk.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                            hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                            if hoehengenauigkeitsklasse_element:
                                pumpwerk.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                            hersteller_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                            if hersteller_element:
                                pumpwerk.hersteller_typ = hersteller_element[0].firstChild.nodeValue
                            adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                            if adresse_hersteller_element:
                                pumpwerk.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                            ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                            if ufis_baunummer_element:
                                pumpwerk.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                            art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                            if art_einstieghilfe_element:
                                pumpwerk.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                            uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                            if uebergabebauwerk_element:
                                pumpwerk.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                            # Class specific attributes:
                            grundflaeche_element = abwasser_objekt.getElementsByTagName('Grundflaeche')
                            if grundflaeche_element:
                                pumpwerk.grundflaeche = float(grundflaeche_element[0].firstChild.nodeValue)
                            max_laenge_element = abwasser_objekt.getElementsByTagName('MaxLaenge')
                            if max_laenge_element:
                                pumpwerk.max_laenge = float(max_laenge_element[0].firstChild.nodeValue)
                            max_breite_element = abwasser_objekt.getElementsByTagName('MaxBreite')
                            if max_breite_element:
                                pumpwerk.max_breite = float(max_breite_element[0].firstChild.nodeValue)
                            max_hoehe_element = abwasser_objekt.getElementsByTagName('MaxHoehe')
                            if max_hoehe_element:
                                pumpwerk.max_hoehe = float(max_hoehe_element[0].firstChild.nodeValue)
                            raum_hochbau_element = abwasser_objekt.getElementsByTagName('RaumHochbau')
                            if raum_hochbau_element:
                                pumpwerk.raum_hochbau = float(raum_hochbau_element[0].firstChild.nodeValue)
                            raum_tiefbau_element = abwasser_objekt.getElementsByTagName('RaumTiefbau')
                            if raum_tiefbau_element:
                                pumpwerk.raum_tiefbau = float(raum_tiefbau_element[0].firstChild.nodeValue)
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
                                                    pumpwerk.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            pumpwerk.add_polygon(polygon)
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
                                    pumpwerk.add_knoten(knoten)
                            bauwerke_list.append(pumpwerk)
    print(f"Number of Bauwerke objects: {len(bauwerke_list)}")
    print(f"Number of unique Bauwerke: {len(set(b.objektbezeichnung for b in bauwerke_list))}")
    return bauwerke_list                        


@dataclass
class Becken:   #2
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        #Class specific attributes:
    beckenfunktion: Optional[str] = None
    beckenart: Optional[int] = None
    beckenbauart: Optional[int] = None
    beckenform: Optional[int] = None
    beckenausfuehrung: Optional[int] = None
    beckenablauf: Optional[int] = None
    grundflaeche: Optional[float]= None
    max_laenge: Optional[float]= None
    max_breite: Optional[float]= None
    max_hoehe: Optional[float]= None
    boechungsneigung: Optional[float]= None
    nutzvolumen: Optional[float]= None
    raum_hochbau: Optional[float]= None
    raum_tiefbau:Optional[float]= None
    anzahl_zulauf: Optional[int] = None
    anzahl_ablauf: Optional[int] = None
    anzahl_kammern: Optional[int] = None
    filterschicht: Optional[float]= None
    filtermaterial: Optional[int] = None
    bepflanzung: Optional[int] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_becken(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element= abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element == 2:
                            becken = Becken()
                            objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                            if objektbezeichnung_element:
                                becken.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                            entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                            if entwaesserungsart_element:
                                becken.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                            status_element = abwasser_objekt.getElementsByTagName('Status')
                            if status_element:
                                becken.status= status_element[0].firstChild.nodeValue
                            baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                            if baujahr_element:
                                becken.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                            geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                            if geo_objektart_element:
                                becken.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                            geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                            if geo_objekttyp_element:
                                becken.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                            lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                            if lagegenauigkeitsklasse_element:
                                becken.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                            hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                            if hoehengenauigkeitsklasse_element:
                                becken.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                            hersteller_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                            if hersteller_element:
                                becken.hersteller_typ = hersteller_element[0].firstChild.nodeValue
                            adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                            if adresse_hersteller_element:
                                becken.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                            ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                            if ufis_baunummer_element:
                                becken.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                            art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                            if art_einstieghilfe_element:
                                becken.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                            uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                            if uebergabebauwerk_element:
                                becken.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                            # Class specific attributes:
                            beckenfunktion_element = abwasser_objekt.getElementsByTagName('BeckenFunktion')
                            if beckenfunktion_element:
                                becken.beckenfunktion = beckenfunktion_element[0].firstChild.nodeValue
                            beckenart_element = abwasser_objekt.getElementsByTagName('Beckenart')
                            if beckenart_element:
                                becken.beckenart = int(beckenart_element[0].firstChild.nodeValue)
                            beckenbauart_element = abwasser_objekt.getElementsByTagName('BeckenBauart')
                            if beckenbauart_element:
                                becken.beckenbauart = int(beckenbauart_element[0].firstChild.nodeValue)
                            beckenform_element = abwasser_objekt.getElementsByTagName('Beckenform')
                            if beckenform_element:
                                becken.beckenform = int(beckenform_element[0].firstChild.nodeValue)
                            beckenausfuehrung_element = abwasser_objekt.getElementsByTagName('BeckenAusfuehrung')
                            if beckenausfuehrung_element:
                                becken.beckenausfuehrung = int(beckenausfuehrung_element[0].firstChild.nodeValue)
                            beckenablauf_element = abwasser_objekt.getElementsByTagName('Ablaufart')
                            if beckenablauf_element:
                                becken.beckenablauf = int(beckenablauf_element[0].firstChild.nodeValue)
                            grundflaeche_element = abwasser_objekt.getElementsByTagName('Grundflaeche')
                            if grundflaeche_element:
                                becken.grundflaeche = float(grundflaeche_element[0].firstChild.nodeValue)
                            max_laenge_element = abwasser_objekt.getElementsByTagName('MaxLaenge')
                            if max_laenge_element:
                                becken.max_laenge = float(max_laenge_element[0].firstChild.nodeValue)
                            max_breite_element = abwasser_objekt.getElementsByTagName('MaxBreite')
                            if max_breite_element:
                                becken.max_breite = float(max_breite_element[0].firstChild.nodeValue)
                            max_hoehe_element = abwasser_objekt.getElementsByTagName('MaxHoehe')
                            if max_hoehe_element:
                                becken.max_hoehe = float(max_hoehe_element[0].firstChild.nodeValue)
                            boechungsneigung_element = abwasser_objekt.getElementsByTagName('Boeschungsneigung')
                            if boechungsneigung_element:
                                becken.boechungsneigung = float(boechungsneigung_element[0].firstChild.nodeValue)
                            nutzvolumen_element = abwasser_objekt.getElementsByTagName('NutzVolumen')
                            if nutzvolumen_element:
                                becken.nutzvolumen = float(nutzvolumen_element[0].firstChild.nodeValue)
                            raum_hochbau_element = abwasser_objekt.getElementsByTagName('RaumHochbau')
                            if raum_hochbau_element:
                                becken.raum_hochbau = float(raum_hochbau_element[0].firstChild.nodeValue)
                            raum_tiefbau_element = abwasser_objekt.getElementsByTagName('RaumTiefbau')
                            if raum_tiefbau_element:
                                becken.raum_tiefbau = float(raum_tiefbau_element[0].firstChild.nodeValue)
                            anzahl_zulauf_element = abwasser_objekt.getElementsByTagName('AnzahlZulaeufe')
                            if anzahl_zulauf_element:
                                becken.anzahl_zulauf = int(anzahl_zulauf_element[0].firstChild.nodeValue)
                            anzahl_ablauf_element = abwasser_objekt.getElementsByTagName('AnzahlAblaeufe')
                            if anzahl_ablauf_element:
                                becken.anzahl_ablauf = int(anzahl_ablauf_element[0].firstChild.nodeValue)
                            anzahl_kammern_element = abwasser_objekt.getElementsByTagName('AnzahlKammern')
                            if anzahl_kammern_element:
                                becken.anzahl_kammern = int(anzahl_kammern_element[0].firstChild.nodeValue)
                            filterschicht_element = abwasser_objekt.getElementsByTagName('Filterschicht')
                            if filterschicht_element:
                                becken.filterschicht = float(filterschicht_element[0].firstChild.nodeValue)
                            filtermaterial_element = abwasser_objekt.getElementsByTagName('Filtermaterial')
                            if filtermaterial_element:
                                becken.filtermaterial = int(filtermaterial_element[0].firstChild.nodeValue)
                            bepflanzung_element = abwasser_objekt.getElementsByTagName('Bepflanzung')
                            if bepflanzung_element:
                                becken.bepflanzung = int(bepflanzung_element[0].firstChild.nodeValue)
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
                                                    becken.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            becken.add_polygon(polygon)
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
                                    becken.add_knoten(knoten)
                            bauwerke_list.append(becken)
    print("Found objects Bauwerktyp 2")
    return bauwerke_list

@dataclass
class Behandlungsanlage:   #3
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
    behandlungsart: Optional[int] = None
    bypass: Optional[bool] = None
    aufstellungsart: Optional[int] = None
    breite: Optional[float]= None
    laenge: Optional[float] = None
    hoehe: Optional[float] = None
    hoehe_zulauf: Optional[float]= None
    hoehe_ablauf: Optional[float]= None
    material_anlage: Optional[str] = None
        #self.anlage ... kommt noch
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_behandlungsanlage(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element= abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element == 3:
                            behandlungsanlage = Behandlungsanlage()
                            objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                            if objektbezeichnung_element:
                                behandlungsanlage.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                            entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                            if entwaesserungsart_element:
                                behandlungsanlage.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                            status_element = abwasser_objekt.getElementsByTagName('Status')
                            if status_element:
                                behandlungsanlage.status= status_element[0].firstChild.nodeValue
                            baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                            if baujahr_element:
                                behandlungsanlage.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                            geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                            if geo_objektart_element:
                                behandlungsanlage.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                            geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                            if geo_objekttyp_element:
                                behandlungsanlage.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                            lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                            if lagegenauigkeitsklasse_element:
                                behandlungsanlage.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                            hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                            if hoehengenauigkeitsklasse_element:
                                behandlungsanlage.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                            hersteller_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                            if hersteller_element:
                                behandlungsanlage.hersteller_typ = hersteller_element[0].firstChild.nodeValue
                            adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                            if adresse_hersteller_element:
                                behandlungsanlage.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                            ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                            if ufis_baunummer_element:
                                behandlungsanlage.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                            art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                            if art_einstieghilfe_element:
                                behandlungsanlage.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                            uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                            if uebergabebauwerk_element:
                                behandlungsanlage.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                            # Class specific attributes:
                            behandlungsart_element = abwasser_objekt.getElementsByTagName('Behandlungsart')
                            if behandlungsart_element:
                                behandlungsanlage.behandlungsart = behandlungsart_element[0].firstChild.nodeValue
                            bypass_element = abwasser_objekt.getElementsByTagName('Bypass')
                            if bypass_element:
                                behandlungsanlage.bypass = int(bypass_element[0].firstChild.nodeValue)
                            aufstellungsart_element = abwasser_objekt.getElementsByTagName('Aufstellungsart')
                            if aufstellungsart_element:
                                behandlungsanlage.aufstellungsart = int(aufstellungsart_element[0].firstChild.nodeValue)
                            breite_element = abwasser_objekt.getElementsByTagName('Breite')
                            if breite_element:
                                behandlungsanlage.breite = int(breite_element[0].firstChild.nodeValue)
                            laenge_element = abwasser_objekt.getElementsByTagName('Laenge')
                            if laenge_element:
                                behandlungsanlage.laenge = int(laenge_element[0].firstChild.nodeValue)
                            hoehe_element = abwasser_objekt.getElementsByTagName('Hoehe')
                            if hoehe_element:
                                behandlungsanlage.hoehe = int(hoehe_element[0].firstChild.nodeValue)
                            hoehezulauf_element = abwasser_objekt.getElementsByTagName('HoeheZulauf')
                            if hoehezulauf_element:
                                behandlungsanlage.hoehe_zulauf = float(hoehezulauf_element[0].firstChild.nodeValue)
                            hoeheablauf_element = abwasser_objekt.getElementsByTagName('HoeheAblauf')
                            if hoeheablauf_element:
                                behandlungsanlage.hoehe_ablauf = float(hoeheablauf_element[0].firstChild.nodeValue)
                            materialanlage_element = abwasser_objekt.getElementsByTagName('MaterialAnlage')
                            if materialanlage_element:
                                behandlungsanlage.material_anlage = float([0].firstChild.nodeValue)
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
                                                    behandlungsanlage.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            behandlungsanlage.add_polygon(polygon)
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
                                    behandlungsanlage.add_knoten(knoten)
                            bauwerke_list.append(behandlungsanlage)
    print("Found objects Bauwerktyp 3")
    return bauwerke_list

@dataclass
class Klaeranlage:   #4
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
    klaeranlagefunktion: Optional[int]= None
    einwohnerwerte: Optional[int]= None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_klaeranlage(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element= abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element == 4:
                            klaeranlage = Klaeranlage()
                            objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                            if objektbezeichnung_element:
                                klaeranlage.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                            entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                            if entwaesserungsart_element:
                                klaeranlage.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                            status_element = abwasser_objekt.getElementsByTagName('Status')
                            if status_element:
                                klaeranlage.status= status_element[0].firstChild.nodeValue
                            baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                            if baujahr_element:
                                klaeranlage.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                            geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                            if geo_objektart_element:
                                klaeranlage.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                            geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                            if geo_objekttyp_element:
                                klaeranlage.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                            lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                            if lagegenauigkeitsklasse_element:
                                klaeranlage.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                            hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                            if hoehengenauigkeitsklasse_element:
                                klaeranlage.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                            hersteller_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                            if hersteller_element:
                                klaeranlage.hersteller_typ = hersteller_element[0].firstChild.nodeValue
                            adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                            if adresse_hersteller_element:
                                klaeranlage.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                            ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                            if ufis_baunummer_element:
                                klaeranlage.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                            art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                            if art_einstieghilfe_element:
                                klaeranlage.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                            uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                            if uebergabebauwerk_element:
                                klaeranlage.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                            # Class specific attributes:
                            klaeranlagefunktion_element = abwasser_objekt.getElementsByTagName('KlaeranlageFunktion')
                            if klaeranlagefunktion_element:
                                klaeranlage.klaeranlagefunktion = klaeranlagefunktion_element[0].firstChild.nodeValue
                            einwohnerwert_element = abwasser_objekt.getElementsByTagName('Einwohnerwerte')
                            if einwohnerwert_element:
                                klaeranlage.einwohnerwerte = int(einwohnerwert_element[0].firstChild.nodeValue)
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
                                                    klaeranlage.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            klaeranlage.add_polygon(polygon)
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
                                    klaeranlage.add_knoten(knoten)
                            bauwerke_list.append(klaeranlage)
    print("Found objects Bauwerktyp 4")
    return bauwerke_list

@dataclass
class Auslaufbauwerk:   #5
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
    art_auslaufbauwerk: Optional[int] = None
    einleitungsart: Optional[int] = None
    schutzgitter: Optional[int] = None
    sohlsicherung: Optional[int] = None
    boeschungssicherung: Optional[int] = None
    material: Optional[str] = None
    neigung: Optional[float] = None
    laenge: Optional[float] = None
    breite: Optional[float] = None
    hoehe: Optional[float] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_auslaufbauwerk(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element= abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element == 5:
                            auslaufbauwerk = Auslaufbauwerk()
                            objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                            if objektbezeichnung_element:
                                auslaufbauwerk.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                            entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                            if entwaesserungsart_element:
                                auslaufbauwerk.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                            status_element = abwasser_objekt.getElementsByTagName('Status')
                            if status_element:
                                auslaufbauwerk.status= status_element[0].firstChild.nodeValue
                            baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                            if baujahr_element:
                                auslaufbauwerk.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                            geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                            if geo_objektart_element:
                                auslaufbauwerk.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                            geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                            if geo_objekttyp_element:
                                auslaufbauwerk.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                            lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                            if lagegenauigkeitsklasse_element:
                                auslaufbauwerk.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                            hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                            if hoehengenauigkeitsklasse_element:
                                auslaufbauwerk.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                            hersteller_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                            if hersteller_element:
                                auslaufbauwerk.hersteller_typ = hersteller_element[0].firstChild.nodeValue
                            adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                            if adresse_hersteller_element:
                                auslaufbauwerk.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                            ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                            if ufis_baunummer_element:
                                auslaufbauwerk.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                            art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                            if art_einstieghilfe_element:
                                auslaufbauwerk.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                            uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                            if uebergabebauwerk_element:
                                auslaufbauwerk.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                            art_auslaufbauwerk_element = abwasser_objekt.getElementsByTagName('ArtAuslaufbauwerk')
                            if art_auslaufbauwerk_element:
                                auslaufbauwerk.art_auslaufbauwerk = int(art_auslaufbauwerk_element[0].firstChild.nodeValue)
                            einleitungsart_element = abwasser_objekt.getElementsByTagName('Einleitungsart')
                            if einleitungsart_element:
                                auslaufbauwerk.einleitungsart = int(einleitungsart_element[0].firstChild.nodeValue)
                            schutzgitter_element = abwasser_objekt.getElementsByTagName('Schutzgitter')
                            if schutzgitter_element:
                                auslaufbauwerk.schutzgitter = int(schutzgitter_element[0].firstChild.nodeValue)
                            sohlsicherung_element = abwasser_objekt.getElementsByTagName('Sohlsicherung')
                            if sohlsicherung_element:
                                auslaufbauwerk.sohlsicherung = int(sohlsicherung_element[0].firstChild.nodeValue)
                            boeschungssicherung_element = abwasser_objekt.getElementsByTagName('Boeschungssicherung')
                            if boeschungssicherung_element:
                                auslaufbauwerk.boeschungssicherung = int(boeschungssicherung_element[0].firstChild.nodeValue)
                            material_element = abwasser_objekt.getElementsByTagName('Material')
                            if material_element:
                                auslaufbauwerk.material = material_element[0].firstChild.nodeValue
                            neigung_element = abwasser_objekt.getElementsByTagName('Neigung')
                            if neigung_element:
                                auslaufbauwerk.neigung = float(neigung_element[0].firstChild.nodeValue)
                            laenge_element = abwasser_objekt.getElementsByTagName('Laenge')
                            if laenge_element:
                                auslaufbauwerk.laenge = float(laenge_element[0].firstChild.nodeValue)
                            breite_element = abwasser_objekt.getElementsByTagName('Breite')
                            if breite_element:
                                auslaufbauwerk.breite = float(breite_element[0].firstChild.nodeValue)
                            hoehe_element = abwasser_objekt.getElementsByTagName('Hoehe')
                            if hoehe_element:
                                auslaufbauwerk.hoehe = float(hoehe_element[0].firstChild.nodeValue)
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
                                                    auslaufbauwerk.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            auslaufbauwerk.add_polygon(polygon)
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
                                    auslaufbauwerk.add_knoten(knoten)
                            bauwerke_list.append(auslaufbauwerk)
    print("Found objects Bauwerktyp 5")
    return bauwerke_list

@dataclass
class Pumpe:   #6
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
    leistungsaufnahme: Optional[float] = None
    leistung: Optional[float] = None
    foerderhoehe_gesamt: Optional[float] = None
    foerderhoehe_manometrisch: Optional[float] = None
    pumpenart: Optional[int] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_pumpe(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element= abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element == 6:
                            pumpe = Pumpe()
                            objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                            if objektbezeichnung_element:
                                pumpe.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                            entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                            if entwaesserungsart_element:
                                pumpe.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                            status_element = abwasser_objekt.getElementsByTagName('Status')
                            if status_element:
                                pumpe.status= status_element[0].firstChild.nodeValue
                            baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                            if baujahr_element:
                                pumpe.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                            geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                            if geo_objektart_element:
                                pumpe.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                            geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                            if geo_objekttyp_element:
                                pumpe.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                            lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                            if lagegenauigkeitsklasse_element:
                                pumpe.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                            hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                            if hoehengenauigkeitsklasse_element:
                                pumpe.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                            hersteller_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                            if hersteller_element:
                                pumpe.hersteller_typ = hersteller_element[0].firstChild.nodeValue
                            adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                            if adresse_hersteller_element:
                                pumpe.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                            ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                            if ufis_baunummer_element:
                                pumpe.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                            art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                            if art_einstieghilfe_element:
                                pumpe.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                            uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                            if uebergabebauwerk_element:
                                pumpe.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                            leistungsaufnahme_element = abwasser_objekt.getElementsByTagName('Leistungsaufnahme')
                            if leistungsaufnahme_element:
                                pumpe.leistungsaufnahme = float(leistungsaufnahme_element[0].firstChild.nodeValue)
                            leistung_element = abwasser_objekt.getElementsByTagName('Leistung')
                            if leistung_element:
                                pumpe.leistung = float(leistung_element[0].firstChild.nodeValue)
                            foerderhoehe_gesamt_element = abwasser_objekt.getElementsByTagName('FoerderhoeheGesamt')
                            if foerderhoehe_gesamt_element:
                                pumpe.foerderhoehe_gesamt = float(foerderhoehe_gesamt_element[0].firstChild.nodeValue)
                            foerderhoehe_manometrisch_element = abwasser_objekt.getElementsByTagName('FoerderhoeheManometrisch')
                            if foerderhoehe_manometrisch_element:
                                pumpe.foerderhoehe_manometrisch = float(foerderhoehe_manometrisch_element[0].firstChild.nodeValue)
                            pumpenart_element = abwasser_objekt.getElementsByTagName('Pumpenart')
                            if pumpenart_element:
                                pumpe.pumpenart = int(pumpenart_element[0].firstChild.nodeValue)
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
                                                    pumpe.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            pumpe.add_polygon(polygon)
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
                                    pumpe.add_knoten(knoten)
                            bauwerke_list.append(pumpe)
    print("Found objects Bauwerktyp 6")
    return bauwerke_list

@dataclass
class Wehr:   #7
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
    wehr_funktion: Optional[int] = None
    wehr_typ: Optional[int] = None
    oeffnungsweite: Optional[float] = None
    schwellenhoehe_min: Optional[float] = None
    schwellenhoehe_max: Optional[float] = None
    laenge_wehrschwelle: Optional[float] = None
    art_wehrkrone: Optional[int] = None
    verfahrgeschwindigkeit: Optional[float] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_wehr(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element:
                            bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                            if bauwerkstyp == 7:
                                wehr = Wehr()
                                objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                if objektbezeichnung_element:
                                    wehr.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                if entwaesserungsart_element:
                                    wehr.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                status_element = abwasser_objekt.getElementsByTagName('Status')
                                if status_element:
                                    wehr.status= status_element[0].firstChild.nodeValue
                                baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                if baujahr_element:
                                    wehr.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                if geo_objektart_element:
                                    wehr.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                if geo_objekttyp_element:
                                    wehr.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                if lagegenauigkeitsklasse_element:
                                    wehr.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                if hoehengenauigkeitsklasse_element:
                                    wehr.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                if hersteller_typ_element:
                                    wehr.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                if adresse_hersteller_element:
                                    wehr.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                if ufis_baunummer_element:
                                    wehr.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                if art_einstieghilfe_element:
                                    wehr.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                if uebergabebauwerk_element:
                                    wehr.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                wehr_funktion_element = abwasser_objekt.getElementsByTagName('WehrFunktion')
                                if wehr_funktion_element:
                                    wehr.wehr_funktion = int(wehr_funktion_element[0].firstChild.nodeValue)
                                wehr_typ_element = abwasser_objekt.getElementsByTagName('Wehrtyp')
                                if wehr_typ_element:
                                    wehr.wehr_typ = int(wehr_typ_element[0].firstChild.nodeValue)
                                oeffnungsweite_element = abwasser_objekt.getElementsByTagName('Oeffnungsweite')
                                if oeffnungsweite_element:
                                    wehr.oeffnungsweite = float(oeffnungsweite_element[0].firstChild.nodeValue)
                                schwellenhoehe_min_element = abwasser_objekt.getElementsByTagName('SchwellenhoeheMin')
                                if schwellenhoehe_min_element:
                                    wehr.schwellenhoehe_min = float(schwellenhoehe_min_element[0].firstChild.nodeValue)
                                schwellenhoehe_max_element = abwasser_objekt.getElementsByTagName('SchwellenhoeheMax')
                                if schwellenhoehe_max_element:
                                    wehr.schwellenhoehe_max = float(schwellenhoehe_max_element[0].firstChild.nodeValue)
                                laenge_wehrschwelle_element = abwasser_objekt.getElementsByTagName('LaengeWehrschwelle')
                                if laenge_wehrschwelle_element:
                                    wehr.laenge_wehrschwelle = float(laenge_wehrschwelle_element[0].firstChild.nodeValue)
                                art_wehrkrone_element = abwasser_objekt.getElementsByTagName('ArtWehrkrone')
                                if art_wehrkrone_element:
                                    wehr.art_wehrkrone = int(art_wehrkrone_element[0].firstChild.nodeValue)
                                verfahrgeschwindigkeit_element = abwasser_objekt.getElementsByTagName('Verfahrgeschwindigkeit')
                                if verfahrgeschwindigkeit_element:
                                    wehr.verfahrgeschwindigkeit = float(verfahrgeschwindigkeit_element[0].firstChild.nodeValue)
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
                                                    wehr.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            wehr.add_polygon(polygon)
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
                                    wehr.add_knoten(knoten)
                            bauwerke_list.append(wehr)
    print("Found objects Bauwerktyp 7")
    return bauwerke_list

@dataclass
class Drossel:   #8
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
    ablaufart: Optional[int] = None
    nennleistung: Optional[float] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_drossel(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element:
                            bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                            if bauwerkstyp == 8:
                                drossel = Drossel()
                                objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                if objektbezeichnung_element:
                                    drossel.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                if entwaesserungsart_element:
                                    drossel.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                status_element = abwasser_objekt.getElementsByTagName('Status')
                                if status_element:
                                    drossel.status= status_element[0].firstChild.nodeValue
                                baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                if baujahr_element:
                                    drossel.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                if geo_objektart_element:
                                    drossel.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                if geo_objekttyp_element:
                                    drossel.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                if lagegenauigkeitsklasse_element:
                                    drossel.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                if hoehengenauigkeitsklasse_element:
                                    drossel.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                if hersteller_typ_element:
                                    drossel.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                if adresse_hersteller_element:
                                    drossel.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                if ufis_baunummer_element:
                                    drossel.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                if art_einstieghilfe_element:
                                    drossel.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                if uebergabebauwerk_element:
                                    drossel.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                ablaufart_element = abwasser_objekt.getElementsByTagName('Ablaufart')
                                if ablaufart_element:
                                    drossel.ablaufart = int(ablaufart_element[0].firstChild.nodeValue)
                                nennleistung_element = abwasser_objekt.getElementsByTagName('Nennleistung')
                                if nennleistung_element:
                                    drossel.nennleistung = float(nennleistung_element[0].firstChild.nodeValue)
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
                                                    drossel.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            drossel.add_polygon(polygon)
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
                                    drossel.add_knoten(knoten)
                            bauwerke_list.append(drossel)
    print("Found objects Bauwerktyp 8")
    return bauwerke_list

@dataclass
class Schieber:   #9
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
    schieber_funktion: Optional[int] = None
    schieber_art: Optional[int] = None
    schieber_breite: Optional[float] = None
    schieber_nulllage: Optional[float] = None
    hubhoehe_max: Optional[float] = None
    verfahrgeschwindigkeit: Optional[float] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)
def parse_schieber(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element:
                            bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                            if bauwerkstyp == 9:
                                schieber = Schieber()
                                objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                if objektbezeichnung_element:
                                    schieber.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                if entwaesserungsart_element:
                                    schieber.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                status_element = abwasser_objekt.getElementsByTagName('Status')
                                if status_element:
                                    schieber.status= status_element[0].firstChild.nodeValue
                                baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                if baujahr_element:
                                    schieber.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                if geo_objektart_element:
                                    schieber.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                if geo_objekttyp_element:
                                    schieber.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                if lagegenauigkeitsklasse_element:
                                    schieber.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                if hoehengenauigkeitsklasse_element:
                                    schieber.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                if hersteller_typ_element:
                                    schieber.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                if adresse_hersteller_element:
                                    schieber.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                if ufis_baunummer_element:
                                    schieber.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                if art_einstieghilfe_element:
                                    schieber.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                if uebergabebauwerk_element:
                                    schieber.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                schieber_funktion_element = abwasser_objekt.getElementsByTagName('SchieberFunktion')
                                if schieber_funktion_element:
                                    schieber.schieber_funktion = int(schieber_funktion_element[0].firstChild.nodeValue)
                                schieber_art_element = abwasser_objekt.getElementsByTagName('Schieberart')
                                if schieber_art_element:
                                    schieber.schieber_art = int(schieber_art_element[0].firstChild.nodeValue)
                                schieber_breite_element = abwasser_objekt.getElementsByTagName('Schieberbreite')
                                if schieber_breite_element:
                                    schieber.schieber_breite = float(schieber_breite_element[0].firstChild.nodeValue)
                                schieber_nulllage_element = abwasser_objekt.getElementsByTagName('SchieberNulllage')
                                if schieber_nulllage_element:
                                    schieber.schieber_nulllage = float(schieber_nulllage_element[0].firstChild.nodeValue)
                                hubhoehe_max_element = abwasser_objekt.getElementsByTagName('HubhoeheMax')
                                if hubhoehe_max_element:
                                    schieber.hubhoehe_max = float(hubhoehe_max_element[0].firstChild.nodeValue)
                                verfahrgeschwindigkeit_element = abwasser_objekt.getElementsByTagName('Verfahrgeschwindigkeit')
                                if verfahrgeschwindigkeit_element:
                                    schieber.verfahrgeschwindigkeit = float(verfahrgeschwindigkeit_element[0].firstChild.nodeValue)
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
                                                    schieber.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            schieber.add_polygon(polygon)
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
                                        schieber.add_knoten(knoten)
                                bauwerke_list.append(schieber)
    print("Found objects Bauwerktyp 9")
    return bauwerke_list

@dataclass
class Rechen:   #10
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
    rechentyp: Optional[int] = None
    rechenrost: Optional[int] = None
    aufstellungsart: Optional[int] = None
    breite: Optional[float] = None
    laenge: Optional[float] = None
    hoehe: Optional[float] = None
    reinigereingriff: Optional[int] = None
    material: Optional[str] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_rechen(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element:
                            bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                            if bauwerkstyp == 10:
                                rechen = Rechen()
                                objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                if objektbezeichnung_element:
                                    rechen.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                if entwaesserungsart_element:
                                    rechen.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                status_element = abwasser_objekt.getElementsByTagName('Status')
                                if status_element:
                                    rechen.status= status_element[0].firstChild.nodeValue
                                baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                if baujahr_element:
                                    rechen.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                if geo_objektart_element:
                                    rechen.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                if geo_objekttyp_element:
                                    rechen.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                if lagegenauigkeitsklasse_element:
                                    rechen.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                if hoehengenauigkeitsklasse_element:
                                    rechen.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                if hersteller_typ_element:
                                    rechen.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                if adresse_hersteller_element:
                                    rechen.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                if ufis_baunummer_element:
                                    rechen.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                if art_einstieghilfe_element:
                                    rechen.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                if uebergabebauwerk_element:
                                    rechen.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                rechentyp_element = abwasser_objekt.getElementsByTagName('Rechentyp')
                                if rechentyp_element:
                                    rechen.rechentyp = int(rechentyp_element[0].firstChild.nodeValue)
                                rechenrost_element = abwasser_objekt.getElementsByTagName('Rechenrost')
                                if rechenrost_element:
                                    rechen.nennleisrechenrost = float(rechentyp_element[0].firstChild.nodeValue)
                                aufstellungsart_element = abwasser_objekt.getElementsByTagName('Aufstellungsart')
                                if aufstellungsart_element:
                                    rechen.aufstellungsart = float(aufstellungsart_element[0].firstChild.nodeValue)
                                breite_element = abwasser_objekt.getElementsByTagName('Breite')
                                if breite_element:
                                    rechen.breite = float(breite_element[0].firstChild.nodeValue)
                                laenge_element = abwasser_objekt.getElementsByTagName('Laenge')
                                if laenge_element:
                                    rechen.laenge = float(laenge_element[0].firstChild.nodeValue)
                                hoehe_element = abwasser_objekt.getElementsByTagName('Hoehe')
                                if hoehe_element:
                                    rechen.hoehe = float(hoehe_element[0].firstChild.nodeValue)
                                reinigereingriff_element = abwasser_objekt.getElementsByTagName('Reinigereingriff')
                                if reinigereingriff_element:
                                    rechen.reinigereingriff = float(reinigereingriff_element[0].firstChild.nodeValue)
                                material_element = abwasser_objekt.getElementsByTagName('Material')
                                if material_element:
                                    rechen.material = float(material_element[0].firstChild.nodeValue)
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
                                                    rechen.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            rechen.add_polygon(polygon)
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
                                    rechen.add_knoten(knoten)
                            bauwerke_list.append(rechen)
    print("Found objects Bauwerktyp 10")
    return bauwerke_list

@dataclass
class Sieb:   #11
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
    siebtyp: Optional[int] = None
    siebkoerper: Optional[int] = None
    aufstellungsart: Optional[int] = None
    einbauart: Optional[int] = None
    siebflaeche: Optional[int] = None
    material: Optional[str] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_sieb(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
            objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
            if objektart_element:
                objektart = int(objektart_element[0].firstChild.nodeValue)
                if objektart == 2:
                    knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                    if knoten_typ_element:
                        knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                        if knoten_typ == 2:
                            bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                            if bauwerkstyp_element:
                                bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                                if bauwerkstyp == 11:
                                    sieb = Sieb()
                                    objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                    if objektbezeichnung_element:
                                        sieb.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                    entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                    if entwaesserungsart_element:
                                        sieb.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                    status_element = abwasser_objekt.getElementsByTagName('Status')
                                    if status_element:
                                        sieb.status= status_element[0].firstChild.nodeValue
                                    baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                    if baujahr_element:
                                        sieb.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                    geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                    if geo_objektart_element:
                                        sieb.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                    geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                    if geo_objekttyp_element:
                                        sieb.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                    lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                    if lagegenauigkeitsklasse_element:
                                        sieb.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                    hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                    if hoehengenauigkeitsklasse_element:
                                        sieb.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                    hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                    if hersteller_typ_element:
                                        sieb.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                    adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                    if adresse_hersteller_element:
                                        sieb.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                    ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                    if ufis_baunummer_element:
                                        sieb.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                    art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                    if art_einstieghilfe_element:
                                        sieb.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                    uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                    if uebergabebauwerk_element:
                                        sieb.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                    siebtyp_element = abwasser_objekt.getElementsByTagName('Siebtyp')
                                    if siebtyp_element:
                                        sieb.siebtyp = int(siebtyp_element[0].firstChild.nodeValue)
                                    siebkoerper_element = abwasser_objekt.getElementsByTagName('Siebkoerper')
                                    if siebkoerper_element:
                                        sieb.siebkoerper = int(siebkoerper_element[0].firstChild.nodeValue)
                                    aufstellungsart_element = abwasser_objekt.getElementsByTagName('Aufstellungsart')
                                    if aufstellungsart_element:
                                        sieb.aufstellungsart = int(aufstellungsart_element[0].firstChild.nodeValue)
                                    einbauart_element = abwasser_objekt.getElementsByTagName('Einbauart')
                                    if einbauart_element:
                                        sieb.einbauart = int(einbauart_element[0].firstChild.nodeValue)
                                    siebflaeche_element = abwasser_objekt.getElementsByTagName('Siebflaeche')
                                    if siebflaeche_element:
                                        sieb.siebflaeche = int(siebflaeche_element[0].firstChild.nodeValue)
                                    material_element = abwasser_objekt.getElementsByTagName('Material')
                                    if material_element:
                                        sieb.material = str(material_element[0].firstChild.nodeValue)
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
                                                    sieb.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            sieb.add_polygon(polygon)
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
                                    sieb.add_knoten(knoten)
                            bauwerke_list.append(sieb)
    print("Found objects Bauwerktyp 11")
    return bauwerke_list

@dataclass
class Versickerungsanlage:   #12
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
    versickerungsanlagetyp: Optional[int] = None
    datum_inbetriebnahme: Optional[str] = None
    art_flaechenanschluss: Optional[int] = None
    bemessungshaeufigkeit: Optional[float] = None
    max_versickerungsleistung: Optional[float] = None
    umfeld: Optional[str] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_versickerungsanlage(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
            objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
            if objektart_element:
                objektart = int(objektart_element[0].firstChild.nodeValue)
                if objektart == 2:
                    knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                    if knoten_typ_element:
                        knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                        if knoten_typ == 2:
                            bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                            if bauwerkstyp_element:
                                bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                                if bauwerkstyp == 12:
                                    versickerungsanlage = Versickerungsanlage()
                                    objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                    if objektbezeichnung_element:
                                        versickerungsanlage.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                    entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                    if entwaesserungsart_element:
                                        versickerungsanlage.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                    status_element = abwasser_objekt.getElementsByTagName('Status')
                                    if status_element:
                                        versickerungsanlage.status= status_element[0].firstChild.nodeValue
                                    baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                    if baujahr_element:
                                        versickerungsanlage.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                    geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                    if geo_objektart_element:
                                        versickerungsanlage.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                    geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                    if geo_objekttyp_element:
                                        versickerungsanlage.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                    lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                    if lagegenauigkeitsklasse_element:
                                        versickerungsanlage.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                    hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                    if hoehengenauigkeitsklasse_element:
                                        versickerungsanlage.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                    hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                    if hersteller_typ_element:
                                        versickerungsanlage.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                    adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                    if adresse_hersteller_element:
                                        versickerungsanlage.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                    ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                    if ufis_baunummer_element:
                                        versickerungsanlage.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                    art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                    if art_einstieghilfe_element:
                                        versickerungsanlage.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                    uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                    if uebergabebauwerk_element:
                                        versickerungsanlage.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                    versickerungsanlagetyp_element = abwasser_objekt.getElementsByTagName('Versickerungsanlagetyp')
                                    if versickerungsanlagetyp_element:
                                        versickerungsanlage.versickerungsanlagetyp = int(versickerungsanlagetyp_element[0].firstChild.nodeValue)
                                    datuminbetriebname_element = abwasser_objekt.getElementsByTagName('DatumInbetriebnahme')
                                    if datuminbetriebname_element:
                                        versickerungsanlage.datum_inbetriebnahme = int(datuminbetriebname_element[0].firstChild.nodeValue)
                                    artflaechenanschluss_element = abwasser_objekt.getElementsByTagName('ArtFlaechenanschluss')
                                    if artflaechenanschluss_element:
                                        versickerungsanlage.art_flaechenanschluss = int(artflaechenanschluss_element[0].firstChild.nodeValue)
                                    bemessungshaeufigkeit_element = abwasser_objekt.getElementsByTagName('Bemesungshaeufigkeit')
                                    if bemessungshaeufigkeit_element:
                                        versickerungsanlage.bemessungshaeufigkeit = int(bemessungshaeufigkeit_element[0].firstChild.nodeValue)
                                    maxversickerungsleistung_element = abwasser_objekt.getElementsByTagName('MaxVersickerungsleistung')
                                    if maxversickerungsleistung_element:
                                        versickerungsanlage.max_versickerungsleistung = int(maxversickerungsleistung_element[0].firstChild.nodeValue)
                                    umfeld_element = abwasser_objekt.getElementsByTagName('Umfeld')
                                    if umfeld_element:
                                        versickerungsanlage.umfeld = str(umfeld_element[0].firstChild.nodeValue)
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
                                                    versickerungsanlage.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            versickerungsanlage.add_polygon(polygon)
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
                                            versickerungsanlage.add_knoten(knoten)
                                    bauwerke_list.append(versickerungsanlage)
    print("Found objects Bauwerktyp 12")
    return bauwerke_list

@dataclass
class Regenwassernutzungsanlage:   #13
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
    regenwassernutzung_funktion: Optional[int] = None
    laenge: Optional[float] = None
    breite: Optional[float] = None
    tiefe: Optional[float] = None
    hoehe: Optional[float] = None
    durchmesser: Optional[float] = None
    grundflaeche_rn: Optional[float] = None
    bauart: Optional[int] = None
    material_rn: Optional[int] = None
    filterart: Optional[int] = None
    art_flaechenanschluss: Optional[int] = None
    angeschlossene_flaeche: Optional[int] = None
    volumen_nutzbar: Optional[float] = None
    rueckhaltevolumen: Optional[float] = None
    drosselabfluss: Optional[float] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_regenwassernutzungsanlage(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element:
                            bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                            if bauwerkstyp == 13:
                                regenwassernutzungsanlage = Regenwassernutzungsanlage()
                                objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                if objektbezeichnung_element:
                                    regenwassernutzungsanlage.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                if entwaesserungsart_element:
                                    regenwassernutzungsanlage.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                status_element = abwasser_objekt.getElementsByTagName('Status')
                                if status_element:
                                    regenwassernutzungsanlage.status= status_element[0].firstChild.nodeValue
                                baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                if baujahr_element:
                                    regenwassernutzungsanlage.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                if geo_objektart_element:
                                    regenwassernutzungsanlage.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                if geo_objekttyp_element:
                                    regenwassernutzungsanlage.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                if lagegenauigkeitsklasse_element:
                                    regenwassernutzungsanlage.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                if hoehengenauigkeitsklasse_element:
                                    regenwassernutzungsanlage.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                if hersteller_typ_element:
                                    regenwassernutzungsanlage.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                if adresse_hersteller_element:
                                    regenwassernutzungsanlage.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                if ufis_baunummer_element:
                                    regenwassernutzungsanlage.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                if art_einstieghilfe_element:
                                    regenwassernutzungsanlage.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                if uebergabebauwerk_element:
                                    regenwassernutzungsanlage.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                # Additional attributes for Regenwassernutzungsanlage
                                regenwassernutzung_funktion_element = abwasser_objekt.getElementsByTagName('RegenwassernutzungFunktion')
                                if regenwassernutzung_funktion_element:
                                    regenwassernutzungsanlage.regenwassernutzung_funktion = int(regenwassernutzung_funktion_element[0].firstChild.nodeValue)
                                laenge_element = abwasser_objekt.getElementsByTagName('Laenge')
                                if laenge_element:
                                    regenwassernutzungsanlage.laenge = float(laenge_element[0].firstChild.nodeValue)
                                breite_element = abwasser_objekt.getElementsByTagName('Breite')
                                if breite_element:
                                    regenwassernutzungsanlage.breite = float(breite_element[0].firstChild.nodeValue)
                                tiefe_element = abwasser_objekt.getElementsByTagName('Tiefe')
                                if tiefe_element:
                                    regenwassernutzungsanlage.tiefe = float(tiefe_element[0].firstChild.nodeValue)
                                hoehe_element = abwasser_objekt.getElementsByTagName('Hoehe')
                                if hoehe_element:
                                    regenwassernutzungsanlage.hoehe = float(hoehe_element[0].firstChild.nodeValue)
                                durchmesser_element = abwasser_objekt.getElementsByTagName('Durchmesser')
                                if durchmesser_element:
                                    regenwassernutzungsanlage.durchmesser = float(durchmesser_element[0].firstChild.nodeValue)
                                grundflaeche_rn_element = abwasser_objekt.getElementsByTagName('GrundflaecheRn')
                                if grundflaeche_rn_element:
                                    regenwassernutzungsanlage.grundflaeche_rn = float(grundflaeche_rn_element[0].firstChild.nodeValue)
                                bauart_element = abwasser_objekt.getElementsByTagName('Bauart')
                                if bauart_element:
                                    regenwassernutzungsanlage.bauart = int(bauart_element[0].firstChild.nodeValue)
                                material_rn_element = abwasser_objekt.getElementsByTagName('MaterialRn')
                                if material_rn_element:
                                    regenwassernutzungsanlage.material_rn = int(material_rn_element[0].firstChild.nodeValue)
                                filterart_element = abwasser_objekt.getElementsByTagName('Filterart')
                                if filterart_element:
                                    regenwassernutzungsanlage.filterart = int(filterart_element[0].firstChild.nodeValue)
                                art_flaechenanschluss_element = abwasser_objekt.getElementsByTagName('ArtFlaechenanschluss')
                                if art_flaechenanschluss_element:
                                    regenwassernutzungsanlage.art_flaechenanschluss = int(art_flaechenanschluss_element[0].firstChild.nodeValue)
                                angeschlossene_flaeche_element = abwasser_objekt.getElementsByTagName('AngeschlosseneFlaeche')
                                if angeschlossene_flaeche_element:
                                    regenwassernutzungsanlage.angeschlossene_flaeche = int(angeschlossene_flaeche_element[0].firstChild.nodeValue)
                                volumennutzbar_element = abwasser_objekt.getElementsByTagName('Volumennutzbar')
                                if volumennutzbar_element:
                                    regenwassernutzungsanlage.volumen_nutzbar = float(volumennutzbar_element[0].firstChild.nodeValue)
                                rueckhaltevolumen_element = abwasser_objekt.getElementsByTagName('Rueckhaltevolumen')
                                if rueckhaltevolumen_element:
                                    regenwassernutzungsanlage.rueckhaltevolumen = float(rueckhaltevolumen_element[0].firstChild.nodeValue)
                                drosselabfluss_element = abwasser_objekt.getElementsByTagName('Drosselabfluss')
                                if drosselabfluss_element:
                                    regenwassernutzungsanlage.drosselabfluss = float(drosselabfluss_element[0].firstChild.nodeValue)
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
                                                    regenwassernutzungsanlage.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            regenwassernutzungsanlage.add_polygon(polygon)
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
                                        regenwassernutzungsanlage.add_knoten(knoten)
                                bauwerke_list.append(regenwassernutzungsanlage)
    print("Found objects Bauwerktyp 13")
    return bauwerke_list

@dataclass
class Einlaufbauwerk:   #14
    objektbezeichnung: Optional[str] = str(generate_unique_id)
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
        #Objektspezifische Attribute:
    hersteller_typ: Optional[str] = None
    adresse_hersteller: Optional[str] = None
    ufis_baunummer: Optional[int] = None
    art_einstieghilfe: Optional[str] = None
    uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
    art_einlaufbauwerk: Optional[int] = None
    schutzgitter: Optional[int] = None
    def add_knoten(self, knoten: 'Knoten'):
            if self.knoten is None:
                self.knoten = []
            self.knoten.append(knoten)
    def add_kante(self, kante: Kante):
            self.kanten.append(kante)
    def add_polygon(self, polygon: Polygon):
            self.polygon.append(polygon)

def parse_einlaufbauwerk(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 2:
                knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
                if knoten_typ_element:
                    knoten_typ = int(knoten_typ_element[0].firstChild.nodeValue)
                    if knoten_typ == 2:
                        bauwerkstyp_element = abwasser_objekt.getElementsByTagName('Bauwerkstyp')
                        if bauwerkstyp_element:
                            bauwerkstyp = int(bauwerkstyp_element[0].firstChild.nodeValue)
                            if bauwerkstyp == 13:
                                einlaufbauwerk = Einlaufbauwerk()
                                objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                                if objektbezeichnung_element:
                                    einlaufbauwerk.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                                entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                                if entwaesserungsart_element:
                                    einlaufbauwerk.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                                status_element = abwasser_objekt.getElementsByTagName('Status')
                                if status_element:
                                    einlaufbauwerk.status= status_element[0].firstChild.nodeValue
                                baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                                if baujahr_element:
                                    einlaufbauwerk.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                                geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                                if geo_objektart_element:
                                    einlaufbauwerk.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                                geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                                if geo_objekttyp_element:
                                    einlaufbauwerk.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                                lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                                if lagegenauigkeitsklasse_element:
                                    einlaufbauwerk.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                                hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                                if hoehengenauigkeitsklasse_element:
                                    einlaufbauwerk.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                                hersteller_typ_element = abwasser_objekt.getElementsByTagName('Hersteller_Typ')
                                if hersteller_typ_element:
                                    einlaufbauwerk.hersteller_typ = hersteller_typ_element[0].firstChild.nodeValue
                                adresse_hersteller_element = abwasser_objekt.getElementsByTagName('Adresse_Hersteller')
                                if adresse_hersteller_element:
                                    einlaufbauwerk.adresse_hersteller = adresse_hersteller_element[0].firstChild.nodeValue
                                ufis_baunummer_element = abwasser_objekt.getElementsByTagName('UFIS_BauNr')
                                if ufis_baunummer_element:
                                    einlaufbauwerk.ufis_baunummer = int(ufis_baunummer_element[0].firstChild.nodeValue)
                                art_einstieghilfe_element = abwasser_objekt.getElementsByTagName('Art_Einstieghilfe')
                                if art_einstieghilfe_element:
                                    einlaufbauwerk.art_einstieghilfe = art_einstieghilfe_element[0].firstChild.nodeValue
                                uebergabebauwerk_element = abwasser_objekt.getElementsByTagName('Uebergabebauwerk')
                                if uebergabebauwerk_element:
                                    einlaufbauwerk.uebergabebauwerk = bool(uebergabebauwerk_element[0].firstChild.nodeValue)
                                art_element = abwasser_objekt.getElementsByTagName('ArtEinlaufbauwerk')
                                if art_element:
                                    einlaufbauwerk.art_einlaufbauwerk = int(art_element[0].firstChild.nodeValue)
                                schutzgitter_element = abwasser_objekt.getElementsByTagName('Schutzgitter')
                                if schutzgitter_element:
                                    einlaufbauwerk.schutzgitter = int(schutzgitter_element[0].firstChild.nodeValue)
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
                                                    einlaufbauwerk.add_kante(kante)
                                                    polygon= Polygon(kante=kante)
                                            einlaufbauwerk.add_polygon(polygon)
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
                                        einlaufbauwerk.add_knoten(knoten)
                                bauwerke_list.append(einlaufbauwerk)
    print("Found objects Bauwerktyp 14")
    return bauwerke_list
