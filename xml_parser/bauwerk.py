
from typing import Optional, Union
from dataclasses import dataclass
bauwerke_list = []


'''NOT FINISHED YET'''
@dataclass
class Polygon:
    def __init__(self):
        self.knoten = []
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def __str__(self):
        print("Inside __str__")
        return f"Polygon: {self.knoten}"
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
class Pumpwerk:   #1
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
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        self.grundflaeche: Optional[float]= None
        self.max_laenge: Optional[float]= None
        self.max_breite: Optional[float]= None
        self.max_hoehe: Optional[float]= None
        self.raum_hochbau: Optional[float]= None
        self.raum_tiefbau:Optional[float]= None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Objektbezeichnung: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                            for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    knoten = Knoten()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        knoten.add_punkt(punkt)
                                    pumpwerk.add_knoten(knoten)
                            for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    polygon = Polygon()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        polygon.add_punkt(punkt)
                                    pumpwerk.add_polygon(polygon)
                            bauwerke_list.append(pumpwerk)


@dataclass
class Becken:   #2
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
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        #Class specific attributes:
        self.beckenfunktion: Optional[str] = None
        self.beckenart: Optional[int] = None
        self.beckenbauart: Optional[int] = None
        self.beckenform: Optional[int] = None
        self.beckenausfuehrung: Optional[int] = None
        self.beckenablauf: Optional[int] = None
        self.grundflaeche: Optional[float]= None
        self.max_laenge: Optional[float]= None
        self.max_breite: Optional[float]= None
        self.max_hoehe: Optional[float]= None
        self.boechungsneigung: Optional[float]= None
        self.nutzvolumen: Optional[float]= None
        self.raum_hochbau: Optional[float]= None
        self.raum_tiefbau:Optional[float]= None
        self.anzahl_zulauf: Optional[int] = None
        self.anzahl_ablauf: Optional[int] = None
        self.anzahl_kammern: Optional[int] = None
        self.filterschicht: Optional[float]= None
        self.filtermaterial: Optional[int] = None
        self.bepflanzung: Optional[int] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Becken: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                            for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    knoten = Knoten()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        knoten.add_punkt(punkt)
                                    becken.add_knoten(knoten)
                            for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    polygon = Polygon()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        polygon.add_punkt(punkt)
                                    becken.add_polygon(polygon)
                            bauwerke_list.append(becken)

@dataclass
class Behandlungsanlage:   #3
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
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        self.behandlungsart: Optional[int] = None
        self.bypass: Optional[bool] = None
        self.aufstellungsart[int] = None
        self.breite[float]= None
        self.laenge[float] = None
        self.hoehe[float] = None
        self.hoehe_zulauf[float]= None
        self.hoehe_ablauf[float]= None
        self.material_anlage[str] = None
        #self.anlage ... kommt noch
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Behandlungsanlage: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                            for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    knoten = Knoten()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        knoten.add_punkt(punkt)
                                    behandlungsanlage.add_knoten(knoten)
                            for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    polygon = Polygon()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        polygon.add_punkt(punkt)
                                    behandlungsanlage.add_polygon(polygon)
                            bauwerke_list.append(behandlungsanlage)

@dataclass
class Klaeranlage:   #4
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.status: Optional[Union[str,int]] = None
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        self.klaeranlagefunktion: Optional[int]= None
        self.einwohnerwerte: Optional[int]= None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Klaeranlage: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                            for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    knoten = Knoten()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        knoten.add_punkt(punkt)
                                    klaeranlage.add_knoten(knoten)
                            for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    polygon = Polygon()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        polygon.add_punkt(punkt)
                                    klaeranlage.add_polygon(polygon)
                            bauwerke_list.append(klaeranlage)

@dataclass
class Auslaufbauwerk:   #5
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.status: Optional[Union[int,str]] = None
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
        self.art_auslaufbauwerk: Optional[int] = None
        self.einleitungsart: Optional[int] = None
        self.schutzgitter: Optional[int] = None
        self.sohlsicherung: Optional[int] = None
        self.boeschungssicherung: Optional[int] = None
        self.material: Optional[str] = None
        self.neigung: Optional[float] = None
        self.laenge: Optional[float] = None
        self.breite: Optional[float] = None
        self.hoehe: Optional[float] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Auslaufbauwerk: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                            for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    knoten = Knoten()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        knoten.add_punkt(punkt)
                                    auslaufbauwerk.add_knoten(knoten)
                            for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    polygon = Polygon()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        polygon.add_punkt(punkt)
                                    auslaufbauwerk.add_polygon(polygon)
                            bauwerke_list.append(auslaufbauwerk)

@dataclass
class Pumpe:   #6
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.status: Optional[Union[int,str]] = None
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        self.leistungsaufnahme: Optional[float] = None
        self.leistung: Optional[float] = None
        self.foerderhoehe_gesamt: Optional[float] = None
        self.foerderhoehe_manometrisch: Optional[float] = None
        self.pumpenart: Optional[int] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Pumpe: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                            for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                if punkt_elements:
                                    knoten = Knoten()
                                    for punkt_element in punkt_elements:
                                        punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                      y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                      z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                        if punkt.tag_element:
                                            punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                        knoten.add_punkt(punkt)
                                    pumpe.add_knoten(knoten)
                            bauwerke_list.append(pumpe)

@dataclass
class Wehr:   #7
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.status:Optional[Union[int,str]] = None
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        self.wehr_funktion: Optional[int] = None
        self.wehr_typ: Optional[int] = None
        self.oeffnungsweite: Optional[float] = None
        self.schwellenhoehe_min: Optional[float] = None
        self.schwellenhoehe_max: Optional[float] = None
        self.laenge_wehrschwelle: Optional[float] = None
        self.art_wehrkrone: Optional[int] = None
        self.verfahrgeschwindigkeit: Optional[float] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Wehr: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"  # noqa: E501
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
                                for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                    punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        knoten = Knoten()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            knoten.add_punkt(punkt)
                                        wehr.add_knoten(knoten)
                                for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                    punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        polygon = Polygon()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            polygon.add_punkt(punkt)
                                        wehr.add_polygon(polygon)
                                bauwerke_list.append(wehr)

@dataclass
class Drossel:   #8
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        status: Optional[Union[str, int]] = None
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
        self.ablaufart: Optional[int] = None
        self.nennleistung: Optional[float] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Drossel: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                    punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        knoten = Knoten()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            knoten.add_punkt(punkt)
                                        drossel.add_knoten(knoten)
                                bauwerke_list.append(drossel)

@dataclass
class Schieber:   #9
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.status: Optional[Union[int,str]]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
        self.schieber_funktion: Optional[int] = None
        self.schieber_art: Optional[int] = None
        self.schieber_breite: Optional[float] = None
        self.schieber_nulllage: Optional[float] = None
        self.hubhoehe_max: Optional[float] = None
        self.verfahrgeschwindigkeit: Optional[float] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Schieber: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                    punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        knoten = Knoten()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            knoten.add_punkt(punkt)
                                        schieber.add_knoten(knoten)
                                for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                    punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        polygon = Polygon()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            polygon.add_punkt(punkt)
                                        schieber.add_polygon(polygon)
                                    bauwerke_list.append(schieber)
    return bauwerke_list

@dataclass
class Rechen:   #10
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.status: Optional[Union[str,int]] =None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        # Additional attributes:
        self.rechentyp: Optional[int] = None
        self.rechenrost: Optional[int] = None
        self.aufstellungsart: Optional[int] = None
        self.breite: Optional[float] = None
        self.laenge: Optional[float] = None
        self.hoehe: Optional[float] = None
        self.reinigereingriff: Optional[int] = None
        self.material: Optional[str] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Rechen: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                    punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        knoten = Knoten()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            knoten.add_punkt(punkt)
                                        rechen.add_knoten(knoten)
                                for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                    punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        polygon = Polygon()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            polygon.add_punkt(punkt)
                                        rechen.add_polygon(polygon)
                                bauwerke_list.append(rechen)

@dataclass
class Sieb:   #11
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.status: Optional[Union[str,int]]= None    
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
        self.siebtyp: Optional[int] = None
        self.siebkoerper: Optional[int] = None
        self.aufstellungsart: Optional[int] = None
        self.einbauart: Optional[int] = None
        self.siebflaeche: Optional[int] = None
        self.material: Optional[str] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Sieb: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                    for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                        punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                        if punkt_elements:
                                            knoten = Knoten()
                                            for punkt_element in punkt_elements:
                                                punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                              y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                              z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                                if punkt.tag_element:
                                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                                knoten.add_punkt(punkt)
                                            sieb.add_knoten(knoten)
                                    for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                        punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                        if punkt_elements:
                                            polygon = Polygon()
                                            for punkt_element in punkt_elements:
                                                punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                              y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                              z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                                if punkt.tag_element:
                                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                                polygon.add_punkt(punkt)
                                            sieb.add_polygon(polygon)
                                    bauwerke_list.append(sieb)
    return bauwerke_list

@dataclass
class Versickerungsanlage:   #12
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.status: Optional[Union[str,int]]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
        self.versickerungsanlagetyp: Optional[int] = None
        self.datum_inbetriebnahme: Optional[str] = None
        self.art_flaechenanschluss: Optional[int] = None
        self.bemessungshaeufigkeit: Optional[float] = None
        self.max_versickerungsleistung: Optional[float] = None
        self.umfeld: Optional[str] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Versickerungsanlage: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                    for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                        punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                        if punkt_elements:
                                            knoten = Knoten()
                                            for punkt_element in punkt_elements:
                                                punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                              y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                              z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                                if punkt.tag_element:
                                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                                knoten.add_punkt(punkt)
                                            versickerungsanlage.add_knoten(knoten)
                                    for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                        punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                        if punkt_elements:
                                            polygon = Polygon()
                                            for punkt_element in punkt_elements:
                                                punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                              y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                              z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                                if punkt.tag_element:
                                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                                polygon.add_punkt(punkt)
                                            versickerungsanlage.add_polygon(polygon)
                                    bauwerke_list.append(versickerungsanlage)
    return bauwerke_list

@dataclass
class Regenwassernuntzungsanlage:   #13
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.status: Optional[Union[str,int]]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
        self.regenwassernutzung_funktion: Optional[int] = None
        self.laenge: Optional[float] = None
        self.breite: Optional[float] = None
        self.tiefe: Optional[float] = None
        self.hoehe: Optional[float] = None
        self.durchmesser: Optional[float] = None
        self.grundflaeche_rn: Optional[float] = None
        self.bauart: Optional[int] = None
        self.material_rn: Optional[int] = None
        self.filterart: Optional[int] = None
        self.art_flaechenanschluss: Optional[int] = None
        self.angeschlossene_flaeche: Optional[int] = None
        self.volumen_nutzbar: Optional[float] = None
        self.rueckhaltevolumen: Optional[float] = None
        self.drosselabfluss: Optional[float] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Regenwassernutzungsanlage: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                regenwassernutzungsanlage = Regenwassernuntzungsanlage()
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
                                for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                        punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                        if punkt_elements:
                                            knoten = Knoten()
                                            for punkt_element in punkt_elements:
                                                punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                              y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                              z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                                if punkt.tag_element:
                                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                                knoten.add_punkt(punkt)
                                            regenwassernutzungsanlage.add_knoten(knoten)
                                for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                    punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        polygon = Polygon()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            polygon.add_punkt(punkt)
                                        regenwassernutzungsanlage.add_polygon(polygon)
                                bauwerke_list.append(regenwassernutzungsanlage)
    return bauwerke_list

@dataclass
class Einlauf:   #14
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.status: Optional[Union[str,int]]=None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.knoten = []
        self.polygone = []
        #Objektspezifische Attribute:
        self.hersteller_typ: Optional[str] = None
        self.adresse_hersteller: Optional[str] = None
        self.ufis_baunummer: Optional[int] = None
        self.art_einstieghilfe: Optional[str] = None
        self.uebergabebauwerk: Optional[bool] = None
        #Additional attributes:
        self.art_einlaufbauwerk: Optional[int] = None
        self.schutzgitter: Optional[int] = None
    def add_knoten(self, knoten):
        self.knoten.append(knoten)
    def add_polygon(self, polygon):
        self.polygone.append(polygon)
    def __str__(self):
        print("Inside __str__")
        return f"Einlauf: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nBaujahr: {self.baujahr}\nGeoObjektart: {self.geo_objektart}\nGeoObjekttyp: {self.geo_objekttyp}"
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
                                einlaufbauwerk = Regenwassernuntzungsanlage()
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
                                for knoten_element in abwasser_objekt.getElementsByTagName('Knoten'):
                                        punkt_elements = knoten_element.getElementsByTagName('Punkt')
                                        if punkt_elements:
                                            knoten = Knoten()
                                            for punkt_element in punkt_elements:
                                                punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                              y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                              z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                                punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                                if punkt.tag_element:
                                                    punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                                knoten.add_punkt(punkt)
                                            einlaufbauwerk.add_knoten(knoten)
                                for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):
                                    punkt_elements = polygon_element.getElementsByTagName('Punkt')
                                    if punkt_elements:
                                        polygon = Polygon()
                                        for punkt_element in punkt_elements:
                                            punkt = Punkt(x=punkt_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue,
                                                          y=punkt_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue,
                                                          z=punkt_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                            punkt.tag_element = punkt_element.getElementsByTagName('PunktattributAbwasser')
                                            if punkt.tag_element:
                                                punkt.tag = punkt.tag_element[0].firstChild.nodeValue
                                            polygon.add_punkt(punkt)
                                        einlaufbauwerk.add_polygon(polygon)
                                bauwerke_list.append(einlaufbauwerk)
    return bauwerke_list
