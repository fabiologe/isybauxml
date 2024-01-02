from dataclasses import dataclass
from typing import Optional, List

flaechen_list = []
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
class flaeche:
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
    schwerpunkt: Optional[Punkt] = None
    schwerpunktlaufzeit: Optional[float] = None
    kb_wert: Optional[float] = None
    kst_wert: Optional[float] = None