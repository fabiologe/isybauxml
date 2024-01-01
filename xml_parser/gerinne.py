from typing import Optional
from dataclasses import dataclass


gerinne_list = []

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
class Gerinne:
    def __init__(self):
        self.objektbezeichnung = ""
        self.entwaesserungsart = ""
        self.baujahr: Optional[float]= None
        self.geo_objektart = int()
        self.geo_objekttyp: Optional[str]= None
        self.lagegenauigkeitsklasse: Optional[str]= None
        self.hoehengenauigkeitsklasse: Optional[int]= None
        self.kanten = []
        #Objektspezifische Attribute:
        self.gerinne_funtktion: Optional[int]= None
        self.dmplaenge: Optional[float]= None
        self.rohrlaenge: Optional[float]= None
        self.inneschutz: Optional[str]= None
        self.auskleidung: Optional[int]= None
        self.nenndruck: Optional[int]= None
        self.druckverfahren: Optional[int]= None
        self.anschluss_bez: Optional[str]= None
        self.entfernung: Optional[float]= None
        #Geometriedaten:
        self.Polygons = []
        self.zulauf: Optional[str]= None
        self.ablauf: Optional[str]= None
        self.zulauf_sh: Optional[float]= None
        self.ablauf_sh: Optional[float]= None
        self.strang: Optional[str]= None
        self.laenge: Optional[float]= None
        self.material: Optional[str]= None
    def add_polygon(self, polygon: Polygon):
        self.Polygons.append(polygon)
    def add_kante(self, kante: Kante):
        self.kanten.append(kante)
    def __str__(self):
        return f"Gerinne: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nZulauf: {self.zulauf}\nAblauf: {self.ablauf}\nProfil: {self.profilart}\nKante: {self.kanten}"

def parse_geinne(root):
    gerinne= Gerinne()
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage')
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 1:
                kanten_typ_element = abwasser_objekt.getElementsByTagName('KantenTyp')
                if kanten_typ_element:
                    kanten_typ = int(kanten_typ_element[0].firstChild.nodeValue)
                    if kanten_typ == 0:
                        objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                        if objektbezeichnung_element:
                            gerinne.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                        entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                        if entwaesserungsart_element:
                            gerinne.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                        baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                        if baujahr_element:
                            gerinne.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                        geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                        if geo_objektart_element:
                            gerinne.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                        geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                        if geo_objekttyp_element:
                            gerinne.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                        lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                        if lagegenauigkeitsklasse_element:
                            gerinne.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                        hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                        if hoehengenauigkeitsklasse_element:
                            gerinne.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                        gerinnes_funtktion_element = abwasser_objekt.getElementsByTagName('gerinnesFunktion')
                        if gerinnes_funtktion_element:
                            gerinne.gerinnes_funtktion = int(gerinnes_funtktion_element[0].firstChild.nodeValue)
                        dmplaenge_element = abwasser_objekt.getElementsByTagName('DmpLaenge')
                        if dmplaenge_element:
                            gerinne.dmplaenge = float(dmplaenge_element[0].firstChild.nodeValue)
                        rohrlaenge_element = abwasser_objekt.getElementsByTagName('RohrLaenge')
                        if rohrlaenge_element:
                            gerinne.rohrlaenge = float(rohrlaenge_element[0].firstChild.nodeValue)
                        inneschutz_element = abwasser_objekt.getElementsByTagName('InnenSchutz')
                        if inneschutz_element:
                            gerinne.inneschutz = inneschutz_element[0].firstChild.nodeValue
                        auskleidung_element = abwasser_objekt.getElementsByTagName('Auskleidung')
                        if auskleidung_element:
                            gerinne.auskleidung = int(auskleidung_element[0].firstChild.nodeValue)
                        nenndruck_element = abwasser_objekt.getElementsByTagName('Nenndruck')
                        zulauf_element = abwasser_objekt.getElementsByTagName('KnotenZulauf')
                        if zulauf_element:
                            gerinne.zulauf = zulauf_element[0].firstChild.nodeValue
                        ablauf_element = abwasser_objekt.getElementsByTagName('KnotenAblauf')
                        if ablauf_element:
                            gerinne.ablauf = ablauf_element[0].firstChild.nodeValue
                        zulauf_sh_element = abwasser_objekt.getElementsByTagName('SohlhoeheZulauf')
                        if zulauf_sh_element:
                            gerinne.zulauf_sh = float(zulauf_sh_element[0].firstChild.nodeValue)
                        ablauf_sh_element = abwasser_objekt.getElementsByTagName('SohlhoeheAblauf')
                        if ablauf_sh_element:
                            gerinne.ablauf_sh = float(ablauf_sh_element[0].firstChild.nodeValue)
                        if nenndruck_element:
                            gerinne.nenndruck = int(nenndruck_element[0].firstChild.nodeValue)
                        druckverfahren_element = abwasser_objekt.getElementsByTagName('Druckverfahren')
                        if druckverfahren_element:
                            gerinne.druckverfahren = int(druckverfahren_element[0].firstChild.nodeValue)
                        anschluss_bez_element = abwasser_objekt.getElementsByTagName('AnschlussBez')
                        if anschluss_bez_element:
                            gerinne.anschluss_bez = anschluss_bez_element[0].firstChild.nodeValue
                        entfernung_element = abwasser_objekt.getElementsByTagName('Entfernung')
                        if entfernung_element:
                            gerinne.entfernung = float(entfernung_element[0].firstChild.nodeValue)
                        strang_element = abwasser_objekt.getElementsByTagName('Strang')
                        if strang_element:
                            gerinne.strang = strang_element[0].firstChild.nodeValue
                        laenge_element = abwasser_objekt.getElementsByTagName('Laenge')
                        if laenge_element:
                            gerinne.laenge = float(laenge_element[0].firstChild.nodeValue)
                        material_element = abwasser_objekt.getElementsByTagName('Material')
                        if material_element:
                            gerinne.material = material_element[0].firstChild.nodeValue
                        profilart_element = abwasser_objekt.getElementsByTagName('Profilart')
                        if profilart_element:
                            gerinne.profilart = int(profilart_element[0].firstChild.nodeValue)
                        profilbreite_element = abwasser_objekt.getElementsByTagName('Profilbreite')
                        if profilbreite_element:
                            gerinne.profilbreite = int(profilbreite_element[0].firstChild.nodeValue)
                        profilhoehe_element = abwasser_objekt.getElementsByTagName('Profilhoehe')
                        if profilhoehe_element:
                            gerinne.profilhoehe = int(profilhoehe_element[0].firstChild.nodeValue)
                        aussendurchmesser_element = abwasser_objekt.getElementsByTagName('Aussendurchmesser')
                        if aussendurchmesser_element:
                            gerinne.aussendurchmesser = int(aussendurchmesser_element[0].firstChild.nodeValue)
                        for polygon_element in abwasser_objekt.getElementsByTagName('Polygon'):  
                            if polygon_element:
                                for kanten_element in polygon_element.getElementsByTagName('Kante'):
                                    if kanten_element:
                                        start_element = kanten_element.getElementsByTagName('Start')[0]
                                        x = float(start_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue)
                                        y = float(start_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue)
                                        z = float(start_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt = Punkt(x=x, y=y, z=z)
                                        tag = start_element.getElementsByTagName('PunktattributAbwasser')[0].firstChild.nodeValue
                                        start = Start(punkt=punkt, tag=tag)

                                        ende_element = kanten_element.getElementsByTagName('Ende')[0]
                                        x = float(ende_element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue)
                                        y = float(ende_element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue)
                                        z = float(ende_element.getElementsByTagName('Punkthoehe')[0].firstChild.nodeValue)
                                        punkt = Punkt(x=x, y=y, z=z)
                                        tag = ende_element.getElementsByTagName('PunktattributAbwasser')[0].firstChild.nodeValue
                                        ende = Ende(punkt=punkt, tag=tag)

                                        kante = Kante(start=start, ende=ende)
                                        gerinne.add_kante(kante)

                                polygon = Polygon(kante=kante)
                                gerinne.add_polygon(polygon)
                        gerinne_list.append(gerinne)
    print(f"Number of Gerinne objects: {len(gerinne_list)}")
    return gerinne_list
