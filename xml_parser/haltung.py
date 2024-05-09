
from typing import Optional, Union
from dataclasses import dataclass


haltung_list= []
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
 #Haltung: A57c, Number of edges: Polygon(kante=Kante(start=Start(punkt=Punkt(x=2564687.012, y=5461936.858, z=210.77), tag='RAP'), ende=Ende(punkt=Punkt(x=2564692.117, y=5461934.148, z=210.757), tag='RAP')))
    
@dataclass
class Haltung:
    objektbezeichnung: Optional[str] = None
    entwaesserungsart: Optional[str] = None
    status: Optional[Union[str, int]] = None
    baujahr: Optional[float]= None
    geo_objektart: Optional[int] = None
    geo_objekttyp: Optional[str]= None
    lagegenauigkeitsklasse: Optional[str]= None
    hoehengenauigkeitsklasse: Optional[int]= None
    kanten = []
    #Objektspezifische Attribute:
    haltungs_funtktion: Optional[int]= None
    dmplaenge: Optional[float]= None
    rohrlaenge: Optional[float]= None
    inneschutz: Optional[str]= None
    auskleidung: Optional[int]= None
    nenndruck: Optional[int]= None
    druckverfahren: Optional[int]= None
    anschluss_bez: Optional[str]= None
    entfernung: Optional[float]= None
    #Geometriedaten:
    polygons = []
    zulauf: Optional[str]= None
    ablauf: Optional[str]= None
    zulauf_sh: Optional[float]= None
    ablauf_sh: Optional[float]= None
    strang: Optional[str]= None
    laenge: Optional[float]= None
    material: Optional[str]= None
    profilart: Optional[int]= None
    profilbreite: Optional[int]= None
    profilhoehe: Optional[int]= None
    aussendurchmesser: Optional[int]= None
    def add_polygon(self, polygon: Polygon):
        self.polygons.append(polygon)

    def add_kante(self, kante: Kante):
        self.kanten.append(kante)
    def __str__(self):
        return f"Haltung: {self.objektbezeichnung}\nEntwaesserungsart: {self.entwaesserungsart}\nZulauf: {self.zulauf}\nAblauf: {self.ablauf}\nProfil: {self.profilart}\nKante: {self.kanten}"
   
    @staticmethod
    def fix_orientation(self):
        if self.zulauf_sh >= self.ablauf_sh:
            return self.zulauf, self.ablauf, self.zulauf_sh, self.ablauf_sh
        elif self.zulauf_sh <= self.ablauf_sh:
            # Swap the values of zulauf, ablauf, zulauf_sh, and ablauf_sh
            temp_zulauf = self.zulauf
            self.zulauf = self.ablauf
            self.ablauf = temp_zulauf
            
            temp_zulauf_sh = self.zulauf_sh
            self.zulauf_sh = self.ablauf_sh
            self.ablauf_sh = temp_zulauf_sh
            
            return self.zulauf, self.ablauf, self.zulauf_sh, self.ablauf_sh
def parse_haltung(root):
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        objektart_element = abwasser_objekt.getElementsByTagName('Objektart')
        if objektart_element:
            objektart = int(objektart_element[0].firstChild.nodeValue)
            if objektart == 1:
                kanten_typ_element = abwasser_objekt.getElementsByTagName('KantenTyp')
                if kanten_typ_element:
                    kanten_typ = int(kanten_typ_element[0].firstChild.nodeValue)
                    if kanten_typ == 0:
                        haltung = Haltung()
                        objektbezeichnung_element = abwasser_objekt.getElementsByTagName('Objektbezeichnung')
                        if objektbezeichnung_element:
                            haltung.objektbezeichnung = objektbezeichnung_element[0].firstChild.nodeValue
                        entwaesserungsart_element = abwasser_objekt.getElementsByTagName('Entwaesserungsart')
                        if entwaesserungsart_element:
                            haltung.entwaesserungsart = entwaesserungsart_element[0].firstChild.nodeValue
                        status_element = abwasser_objekt.getElementsByTagName('Status')
                        if status_element:
                            haltung.status= status_element[0].firstChild.nodeValue
                        baujahr_element = abwasser_objekt.getElementsByTagName('Baujahr')
                        if baujahr_element:
                            haltung.baujahr = float(baujahr_element[0].firstChild.nodeValue)
                        geo_objektart_element = abwasser_objekt.getElementsByTagName('GeoObjektart')
                        if geo_objektart_element:
                            haltung.geo_objektart = int(geo_objektart_element[0].firstChild.nodeValue)
                        geo_objekttyp_element = abwasser_objekt.getElementsByTagName('GeoObjekttyp')
                        if geo_objekttyp_element:
                            haltung.geo_objekttyp = str(geo_objekttyp_element[0].firstChild.nodeValue)
                        lagegenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Lagegenauigkeitsklasse')
                        if lagegenauigkeitsklasse_element:
                            haltung.lagegenauigkeitsklasse = lagegenauigkeitsklasse_element[0].firstChild.nodeValue
                        hoehengenauigkeitsklasse_element = abwasser_objekt.getElementsByTagName('Hoehengenauigkeitsklasse')
                        if hoehengenauigkeitsklasse_element:
                            haltung.hoehengenauigkeitsklasse = int(hoehengenauigkeitsklasse_element[0].firstChild.nodeValue)
                        haltungs_funtktion_element = abwasser_objekt.getElementsByTagName('haltungsFunktion')
                        if haltungs_funtktion_element:
                            haltung.haltungs_funtktion = int(haltungs_funtktion_element[0].firstChild.nodeValue)
                        dmplaenge_element = abwasser_objekt.getElementsByTagName('DmpLaenge')
                        if dmplaenge_element:
                            haltung.dmplaenge = float(dmplaenge_element[0].firstChild.nodeValue)
                        rohrlaenge_element = abwasser_objekt.getElementsByTagName('Rohrlaenge')
                        if rohrlaenge_element:
                            haltung.rohrlaenge = float(rohrlaenge_element[0].firstChild.nodeValue)
                        inneschutz_element = abwasser_objekt.getElementsByTagName('InnenSchutz')
                        if inneschutz_element:
                            haltung.inneschutz = inneschutz_element[0].firstChild.nodeValue
                        auskleidung_element = abwasser_objekt.getElementsByTagName('Auskleidung')
                        if auskleidung_element:
                            haltung.auskleidung = int(auskleidung_element[0].firstChild.nodeValue)
                        nenndruck_element = abwasser_objekt.getElementsByTagName('Nenndruck')
                        zulauf_element = abwasser_objekt.getElementsByTagName('KnotenZulauf')
                        if zulauf_element:
                            haltung.zulauf = zulauf_element[0].firstChild.nodeValue
                        ablauf_element = abwasser_objekt.getElementsByTagName('KnotenAblauf')
                        if ablauf_element:
                            haltung.ablauf = ablauf_element[0].firstChild.nodeValue
                        zulauf_sh_element = abwasser_objekt.getElementsByTagName('SohlhoeheZulauf')
                        if zulauf_sh_element:
                            haltung.zulauf_sh = float(zulauf_sh_element[0].firstChild.nodeValue)
                        ablauf_sh_element = abwasser_objekt.getElementsByTagName('SohlhoeheAblauf')
                        if ablauf_sh_element:
                            haltung.ablauf_sh = float(ablauf_sh_element[0].firstChild.nodeValue)
                        if nenndruck_element:
                            haltung.nenndruck = int(nenndruck_element[0].firstChild.nodeValue)
                        druckverfahren_element = abwasser_objekt.getElementsByTagName('Druckverfahren')
                        if druckverfahren_element:
                            haltung.druckverfahren = int(druckverfahren_element[0].firstChild.nodeValue)
                        anschluss_bez_element = abwasser_objekt.getElementsByTagName('AnschlussBez')
                        if anschluss_bez_element:
                            haltung.anschluss_bez = anschluss_bez_element[0].firstChild.nodeValue
                        entfernung_element = abwasser_objekt.getElementsByTagName('Entfernung')
                        if entfernung_element:
                            haltung.entfernung = float(entfernung_element[0].firstChild.nodeValue)
                        strang_element = abwasser_objekt.getElementsByTagName('Strang')
                        if strang_element:
                            haltung.strang = strang_element[0].firstChild.nodeValue
                        laenge_element = abwasser_objekt.getElementsByTagName('Laenge')
                        if laenge_element:
                            haltung.laenge = float(laenge_element[0].firstChild.nodeValue)
                        material_element = abwasser_objekt.getElementsByTagName('Material')
                        if material_element:
                            haltung.material = material_element[0].firstChild.nodeValue
                        profilart_element = abwasser_objekt.getElementsByTagName('Profilart')
                        if profilart_element:
                            haltung.profilart = str(profilart_element[0].firstChild.nodeValue)
                        profilbreite_element = abwasser_objekt.getElementsByTagName('Profilbreite')
                        if profilbreite_element:
                            haltung.profilbreite = int(profilbreite_element[0].firstChild.nodeValue)
                        profilhoehe_element = abwasser_objekt.getElementsByTagName('Profilhoehe')
                        if profilhoehe_element:
                            haltung.profilhoehe = int(profilhoehe_element[0].firstChild.nodeValue)
                        aussendurchmesser_element = abwasser_objekt.getElementsByTagName('Aussendurchmesser')
                        if aussendurchmesser_element:
                            haltung.aussendurchmesser = int(aussendurchmesser_element[0].firstChild.nodeValue)
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
                                        haltung.add_kante(kante)

                            polygon = Polygon(kante=kante)
                            haltung.add_polygon(polygon)
                        haltung_list.append(haltung)
    print(f"Number of Haltung objects: {len(haltung_list)}")
    print('\n')
    #Haltung.fix_orientation(self)
    #print(f"Number of unique Haltungen: {len(set(h.objektbezeichnung for h in haltung_list))}")
    return haltung_list



