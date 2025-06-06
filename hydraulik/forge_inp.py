from xml_parser import * 
from hydraulik.rain_tabels.load_rain import rain_wrapper
from hydraulik.utils import site_middle, site_corner, remove_outfall_double
from hydraulik.utils import search_potential_out, num_potential_out
from hydraulik.dfs_routes import find_sewer_routes
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Union, Set
import random
import string
import math


def generate_unique_id(length=7):
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choices(characters, k=length))
    return unique_id

class SimulationMetadata:
    def __init__(self, title, name):
        self.title = title
        self.name = name
        self.date = datetime.now().strftime('%Y-%m-%d')

    def to_title_string(self):
        return f"{self.title}\n{self.name}\n{self.date}\n"
@dataclass
class option:
    flow_units: str
    infiltration: str
    flow_routing: str
    start_date: str
    start_time: str
    report_start_date: str
    report_start_time: str
    end_date: str
    end_time: str
    sweep_start: str
    sweep_end: str
    dry_days: str
    report_step: str
    wet_step: str
    dry_step: str
    routing_step: str
    allow_ponding: str
    inertial_damping: str
    variable_step: str
    lengthening_step: str
    min_surfarea: str
    normal_flow_limited: str
    skip_steady_state: str
    force_main_equation: str
    link_offsets: str
    min_slope: str

    def to_options_string(self):
        return "\n".join(f"{k:<20s} {v}" for k, v in self.__dict__.items())

option_data = option(flow_units='CMS', infiltration='HORTON', flow_routing='KINWAVE', start_date='01/01/2007', start_time='00:00:00', 
                    report_start_date='01/01/2007', report_start_time='00:00:00', end_date='01/01/2007', end_time='12:00:00', 
                    sweep_start='01/01', sweep_end='12/31', dry_days='0', report_step='00:01:00', wet_step='00:01:00', dry_step='01:00:00', 
                    routing_step='0:01:00', allow_ponding='NO', inertial_damping='PARTIAL', variable_step='0.75', lengthening_step='0', 
                    min_surfarea='0', normal_flow_limited='SLOPE', skip_steady_state='NO', force_main_equation='H-W', link_offsets='DEPTH',
                    min_slope='0')
'''
FLOW_UNITS              CFS / GPM / MGD / CMS / LPS / MLD
INFILTRATION            HORTON / MODIFIED_HORTON / GREEN_AMPT/ MODIFIED_GREEN_AMPT / CURVE_NUMBER(need to implement Curve_Number with tabels)
FLOW_ROUTING            STEADY / KINWAVE / DYNWAVE
LINK_OFFSETS            DEPTH / ELEVATION
FORCE_MAIN_EQUATION     H-W / D-W
IGNORE_RAINFALL         YES / NO
IGNORE_SNOWMELT         YES / NO
IGNORE_GROUNDWATER      YES / NO
IGNORE_RDII             YES / NO
IGNORE_ROUTING          YES / NO
IGNORE_QUALITY          YES / NO
ALLOW_PONDING           YES / NO
SKIP_STEADY_STATE       YES / NO
SYS_FLOW_TOL                value
LAT_FLOW_TOL                value
START_DATE              month/day/year
START_TIME              hours:minutes
END_DATE                month/day/year
END_TIME                hours:minutes
REPORT_START_DATE       month/day/year
REPORT_START_TIME       hours:minutes
SWEEP_START             month/day
SWEEP_END               month/day
DRY_DAYS                days
REPORT_STEP             hours:minutes:seconds
WET_STEP                hours:minutes:seconds
DRY_STEP                hours:minutes:seconds
ROUTING_STEP            seconds
LENGTHENING_STEP        seconds
VARIABLE_STEP                 value
MINIMUM_STEP            seconds
INERTIAL_DAMPING        NONE / PARTIAL / FULL
NORMAL_FLOW_LIMITED     SLOPE / FROUDE / BOTH
'''
@dataclass
class evaporation:
    constant: float
    monthly: Optional[List[float]] = None
    timeseries: Optional[List[float]] = None
    temperature: Optional[float] = None

    def to_evaporation_string(self):
        result = ['[EVAPORATION]', ';;Type       Parameters', ';;---------- ----------']
        result.extend(f"{k.upper():<10s} {v}" for k, v in self.__dict__.items() if v is not None)
        return "\n".join(result)
evaporation_data = evaporation(constant=0.0)

@dataclass
class raingage:
    name: str
    type: str
    interval: str
    catch: float
    source_type: str
    source_info: Optional[List[str]] = None

    def to_raingage_string(self):
        # Create the header
        header = [
            "[RAINGAGES]",
            ";;               Rain      Time   Snow   Data",      
            ";;Name           Type      Intrvl Catch  Source",    
            ";;-------------- --------- ------ ------ ----------"
        ]
        
        values = f"{self.name:<15s} {self.type:<9s} {self.interval:<6s} {str(self.catch):<6s} {self.source_type:<10s} {self.source_info:<5}"
        # Join header and values with newline characters
        return "\n".join(header + [values])
    
raingage_data = raingage(name="RainGage", type="INTENSITY", interval="0:05", catch=1.0, source_type="TIMESERIES", source_info="5-yr")


@dataclass
class subcatchments:
    name: str
    raingage: str 
    outletID: str  # name of node or subcatchment that receives runoff from subcatchment. 
    area: float  # naked area 
    imperv : float #percent imperviousness of subcatchment /& Befestigungsgrad
    width: float # charact. width of subcatachment
    slope: float # gefaelle (DE)
    clength : Optional[float] = 0 # Bordsteinlaenge ??
    #spack: Optional[str] = '' # Name of the Snowpack if needed 
    
    def from_flache(flaechen_list: List) -> List['subcatchments']:
        subcatchment_list = []
        for flaeche in flaechen_list:
            subcatchment_sgl = subcatchments(
                name= flaeche.objektbezeichnung,
                raingage="RainGage",
                outletID=str(flaeche.hydro_vertices[0]) or "NO_HYDRO",
                imperv=float(flaeche.abflussbeiwert) if flaeche.abflussbeiwert is not None else 1,
                area=float(flaeche.flaechengroesse) if flaeche.flaechengroesse is not None else 0,
                width=float(flaeche.width) if flaeche.width is not None else 100,
                slope=float(flaeche.neigungsklasse) if flaeche.neigungsklasse is not None else 1,
                clength=0,
                
        )
            subcatchment_list.append(subcatchment_sgl)
        return subcatchment_list
            
    def to_subcatchment_string(flaechen_list: List, subcatchment_list: List['subcatchments']) -> str:
        
        header = [
            "[SUBCATCHMENTS]",
            ";;                                                         Total        Pcnt.             Pcnt.    Curb     Snow ",
            ";;Name                   Raingage         Outlet           Area         Imperv   Width    Slope    Length   Pack ",
            ";;---------------------- ---------------- ---------------- ------------ -------- -------- -------- -------- --------"
        ]
        subcatchment_strings = []
        for subcatchment in subcatchment_list:
            data = f"{subcatchment.name:<25} {subcatchment.raingage:<16} {subcatchment.outletID:<16} {subcatchment.area:<12} {subcatchment.imperv:<8} {subcatchment.width:<8} {subcatchment.slope:<8} {subcatchment.clength:<8}"#{subcatchment.spack:<8}
            subcatchment_strings.append(data)
        return '\n'.join(header + subcatchment_strings)
        
        
@dataclass
class subareas:
    subcat: str
    nimp: Optional[float] = 0.015  # Manning impervious sub-area
    nperv: Optional[float] = 0.24 # Manning pervious sub-area 
    simp: Optional[float] = 0.06 # depression storage fo impervious sub-area(mm)
    sperv: Optional[float] = 0.03 # depression storage for pervious sub-area (mm)
    zero: Optional[float] = 25 # % of impervious area with no depression storage 
    route_to: str = "OUTLET" 
    routed: Optional[float] = 100 # % of runoff routed from one type of area to another

    def from_subcatchment(subcatchment_list: List) -> List['subareas']:
        subarea_list = []
        for subcatchment in subcatchment_list:
            subarea_sgl = subareas(
            subcat = subcatchment.name ,
            nimp = 0.015,
            nperv = 0.24,
            simp = 0.06,
            sperv = 0.03,
            zero = 25,
            route_to = "OUTLET",
            routed = 100) 
            subarea_list.append(subarea_sgl)
        return subarea_list
    
    def to_subarea_string(subarea_list: List, subcatchment_list : List) -> str:
        subareas.from_subcatchment(subcatchment_list)
        header = [
            "[SUBAREAS]",
            ";;Subcatchment              N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted ",
            ";;------------------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------"
        ]
        subarea_strings = []
        for subarea in subarea_list:
            data = f"{subarea.subcat:<30} {subarea.nimp:<10} {subarea.nperv:<10} {subarea.simp:<8} {subarea.sperv:<8} {subarea.zero:<8} {subarea.route_to:<8} {subarea.routed:<8}"
            subarea_strings.append(data)
        return '\n'.join(header + subarea_strings)

@dataclass
class infiltration_H: #For Horton/ Modified Horton
    subname: str
    maxrate: Optional[float] = 4.5 # maximum infiltration rate on Horton curve (in/hr or mm/hr)
    minrate: Optional[float] = 0.2 # minimum infiltration rate on Horton curve (in/hr or mm/hr)
    decay: Optional[float] = 6.5  # decay rate constant of Horton curve (1/hr).
    drytime: Optional[float] = 7 # time it takes for fully saturated soil to dry  (days).
    maxinf: Optional[float] =  0 #maximum infiltration volume possible  (mm)

    def from_subcatchment(subcatchment_list: List) -> List['infiltration_H']:
        infiltration_list = []
        for subcatchment in subcatchment_list:
            infiltration_sgl = infiltration_H(
                subname = str(subcatchment.name),
                maxrate = 4.5,
                minrate= 0.2,
                decay= 6.5,
                drytime= 7,
                maxinf= 0)
            infiltration_list.append(infiltration_sgl)
        return infiltration_list
    def to_infiltration_string(infiltration_list: List, subcatchment_list: List) -> str:
        infiltration_H.from_subcatchment(subcatchment_list)
        header = [
            "[INFILTRATION]",
            ";;Subcatchment         MaxRate    MinRate    Decay      DryTime    MaxInfil",
            ";;------------------- ---------- ---------- ---------- ---------- ----------"
        ]
        infiltration_strings = []
        for infiltration in infiltration_list:
            data = f"{infiltration.subname:<21} {infiltration.maxrate:<10} {infiltration.minrate:<10} {infiltration.decay:<10} {infiltration.drytime:<10} {infiltration.maxinf:<10}"
            infiltration_strings.append(data)
        return '\n'.join(header + infiltration_strings)

@dataclass
class infiltration_G: # Green- Ampt Infiltration
    psi: Optional[float] = 0 #soil capillary suction (mm)
    ksat: Optional[float] = None 
    imd: Optional[float] = None

@dataclass
class infiltration_C: # Curve-Number Infiltration
    curveno: Optional[float] = 0
    ksat: Optional[float] = 0
    drytime: Optional[float] = 0

@dataclass
class lid_controls:
    name: str 
    type: Optional[str] = None # Surface , Soil, Pavement, Storage, Drain, Drainment


@dataclass
class lid_usage:
    subcat: str 
    lid: str
    number: int
    area: Optional[float] = 0
    width: Optional[float] = 0
    initsat: Optional[float] = 0
    fromimp: Optional[float] = 0
    toperv: Optional[float] = 0
    drainTo: Optional[str] = None

'''MISSING CLASSES: AQUIFIER , GROUNDWATER , GWF , SNOWPACK ---> maybe when there is an project I gonna add them '''

@dataclass #= an node element like Schacht or Bauwerk
class junction:
    name: str
    elev: float  #SH
    ymax : Optional[float] = 0 #max Tiefe
    y0: Optional[float] = 0   #DH
    ysur: Optional[float] = 0 
    apond: Optional[float] = 0  #ueberflutungsflaeche

    '''SOMETHING NOT RIGTH--------------------------------------------------'''
    def fict_junc(element_list: List, element, junction_list) -> List['junction']:
            elev = None
            y0 = None
            if element.knoten:
                knoten = element.knoten[0]
                print(f"Fictional Element: {element.objektbezeichnung}")
                print(f"Number of Knoten: {len(element.knoten)}")
                for i, knoten in enumerate(element.knoten):
                    print(f"  Knoten {i + 1}:")
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        elev = float(punkt.z)
                        print(f"    Elevation (elev): {elev}")
                        if len(knoten.punkte) > 1:
                            y0 = float(knoten.punkte[1].z)
                            print(f"    Y0 (second Punkt): {y0}")
                        else:
                            y0 = 0
                            print("    Y0 (second Punkt): Not available, using default (0)")
                    else:
                        print("    No Punkte in this Knoten")
                junction_a = junction(
                            name = element.objektbezeichnung + '_A',
                            elev = elev,
                            y0 = y0 ,
                            ysur=0,
                            apond=0
                                )
                junction_b = junction(
                            name = element.objektbezeichnung + '_B',
                            elev = elev + 0.1 ,
                            y0 = y0 + 0.1 ,
                            ysur=0,
                            apond=0
                                )
                junction_list.append(junction_a)
                junction_list.append(junction_b)
            return junction
    

    def from_node_elem(schacht_list: List, bauwerk_list:List) -> List['junction']:
        junctions_list = []
        for schacht in schacht_list:
            elev = 0
            ymax = 0
            y0 = 0
            if schacht.knoten:
                knoten = schacht.knoten[0]
                print(f"Schacht: {schacht.objektbezeichnung}")
                print(f"Number of Knoten: {len(schacht.knoten)}")
                for i, knoten in enumerate(schacht.knoten):
                    #print(f"  Knoten {i + 1}:")
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        elev = float(punkt.z)
                        #print(f"    Elevation (elev): {elev}")
                        if len(knoten.punkte) > 1:
                            ymax = float(knoten.punkte[1].z)
                            #print(f"    Y0 (second Punkt): {ymax}")
                        else:
                            ymax = 1000
                            print("    Y0 (second Punkt): Not available, using default (0)")
                        y0 = abs(ymax- elev)
                        y0 = round(y0, 2)

                    else:
                        print("    No Punkte in this Knoten")

            junction_sgl = junction(
                name=str(schacht.objektbezeichnung),
                elev=elev,
                ymax = 0,
                y0=0,
                ysur=0,
                apond=0
            )
            junctions_list.append(junction_sgl)
        #print(junctions_list)
        #print("Iter Bauwerke")
        for bauwerk in bauwerk_list:
            if bauwerk.bauwerktyp == 1:
                continue
            elev = 0
            ymax = 0
            y0 = 0
            if bauwerk.knoten:
                knoten = bauwerk.knoten[0]
                #print(f"bauwerk: {bauwerk.objektbezeichnung}")
                #print(f"Number of Knoten: {len(bauwerk.knoten)}")
                for i, knoten in enumerate(bauwerk.knoten):
                    #print(f"  Knoten {i + 1}:")
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        elev = float(punkt.z)
                        #print(f"    Elevation (elev): {elev}")
                        if len(knoten.punkte) > 1:
                            ymax = float(knoten.punkte[1].z)
                            #print(f"    Y0 (second Punkt): {ymax}")
                        else:
                            ymax = 1000
                            print("    Y0 (second Punkt): Not available, using default (0)")
                        y0 = abs(ymax- elev)
                        y0 = round(y0, 2)

                    else:
                        print("    No Punkte in this Knoten")

            junction_sgl = junction(
                name=str(bauwerk.objektbezeichnung),
                elev=elev,
                ymax = 0,
                y0=0,
                ysur=0,
                apond=0
            )
            junctions_list.append(junction_sgl)
        #print(Junction_list)
        return junctions_list

    def to_junction_string(junctions_list: List) -> str:
        header = [
            "[JUNCTIONS]",
            ";;               Invert     Max.       Init.      Surcharge  Ponded ",
            ";;Name           Elev.      Depth      Depth      Depth      Area ",
            ";;-------------- ---------- ---------- ---------- ---------- ----------"
        ]
        
        junction_strings = []
        for junction in junctions_list :
            if junction is not None:
                data = f"{junction.name:<16} {junction.elev:<10} {junction.ymax:<10} {junction.y0:<10} {junction.ysur:<10} {junction.apond:<10}"
                junction_strings.append(data)
        return '\n'.join(header + junction_strings) 
    
@dataclass
class divider: #gets skipped not cant find it inside ISYBAUXML
    name: Optional[str] = None
    elev: Optional[float] = 0
    divlink: Optional[str] = None 
    Qmin: Optional[float] = 0
    Dcurve: Optional[str] = None
    ht: Optional[float] = 0
    cd: Optional[float] = 0
    ymax: Optional[float] = 0
    y0: Optional[float] = 0
    ysur: Optional[float] = 0
    apond: Optional[float] = 0


@dataclass
class outfall:  # AUSLASS 
    name: Optional[str] = None
    elev: Optional[float] = 0
    type: Optional[str] = 'FREE'
    stage: Optional[float] = None
    tcurve: Optional[str] = None
    tseries: Optional[str] = None
    gated: Optional[str] = None
    routeto: Optional[str] = None

    @classmethod
    def check_outfall(cls, schacht_list, haltung_list, bauwerk_list) -> List['outfall']:
        outfalls_list = []
        found_auslaufbauwerk = False
        
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Auslaufbauwerk):
                print("Found Auslaufbauwerk")
                for knoten in bauwerk.knoten:
                    elev = knoten.punkte[1].z
                outfall_sgl = cls(
                    name=bauwerk.objektbezeichnung,
                    elev=elev,
                    type='FREE'
                )
                outfalls_list.append(outfall_sgl)
                found_auslaufbauwerk = True

        if not found_auslaufbauwerk:
            print("No given Auslaufbauwerk")
            find_sewer_routes(schacht_list, haltung_list,bauwerk_list)
            num_outfall = int(input("How many outfalls are needed:"))
            for i in range(num_outfall):
                outfall_sgl = cls.search_set(schacht_list)
                outfalls_list.append(outfall_sgl)
        
        return outfalls_list

    @classmethod
    def search_set(cls, schacht_list):
        while True:
            search_potential_out(schacht_list)
            outfall_name = input("Enter outfall name: ")
            for schacht in schacht_list:
                if schacht.objektbezeichnung == outfall_name:
                    print(f"Found Schacht {outfall_name}. Setting as outfall.")
                    for knoten in schacht.knoten:
                        elev = knoten.punkte[1].z
                        print(f"Elevation of {outfall_name}: {elev}")
                    outfall_sgl = cls(
                        name=str(outfall_name),
                        elev=elev,
                        type='FREE',
                        gated='NO',
                        tcurve='',
                        tseries='',
                        routeto=''
                    )
                    return outfall_sgl  
            print(f"No Schacht found with name {outfall_name}. Please enter a valid name.")

    @classmethod
    def to_outfall_string(cls, outfalls_list: List['outfall']) -> str:
        header = [
            "[OUTFALLS]",
            ";;               Invert     Outfall    Stage/Table      Tide",
            ";;Name           Elev.      Type       Time Series      Gate",
            ";;-------------- ---------- ---------- ---------------- ----"
        ]
        outfall_strings = []
        for outfall in outfalls_list:
            data = f"{outfall.name:<16} {outfall.elev:<10} {outfall.type:<10} {outfall.tseries:<16} {outfall.gated:<5}"
            outfall_strings.append(data)
        return '\n'.join(header + outfall_strings)




@dataclass
class storage:
    name: str
    elev: Optional[float] = 0
    ymax: Optional[float] = 0
    y0: Optional[float] = 0
    acurve: Optional[str] = 'TABULAR'
    curv: Optional[str] = None
    apond: Optional[float] = 0
    fevap: Optional[float] = 0
    psi : Optional[float] = 0
    ksat: Optional[float] = 0
    imd : Optional[float] = 0
    def set_area(becken_list: List)-> List['curves']:
        pass
    def get_becken(self, bauwerk_list) -> List['Becken']:
        becken_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Becken):
                becken_list.append(bauwerk)
        return becken_list
    def get_storage(becken_list: List)-> List['storage']:
        storages_list = []
        for becken in becken_list:
            for knoten in becken.knoten:
                elev = knoten.punkte[1].z
                print("Found Storage")
            storage_sgl = storage(name=becken.objektbezeichnung,
                                      elev= elev,
                                      ymax = becken.max_hoehe,
                                      y0 = 0,
                                      acurve= 'TABULAR',
                                      curve = becken.objektbezeichnung
                                      )
            storages_list.append(storage_sgl)
            return storages_list
    def to_storage_string(storages_list: List) -> str:
        header = [
            "[STORAGE]",
            ";;               Invert   Max.     Init.    Storage    Curve                      Ponded   Evap."   ,
            ";;Name           Elev.    Depth    Depth    Curve      Params                     Area     Frac.    Infiltration Parameters",
            ";;-------------- -------- -------- -------- ---------- -------- -------- -------- -------- -------- -----------------------",
        ]
        storage_strings = []
        for storage in storages_list:
            data = f"{storage.name:<15} {storage.elev:>8} {storage.ymax:>8} {storage.y0:>8} " \
                   f"{storage.acurve:>10} {storage.curve:>8} {storage.apond:>8} {storage.fevap:>8}"
            storage_strings.append(data)
        return "\n".join(header + storage_strings)

    
    
@dataclass
class conduit:  # abflusswirksame Verbindungen
    name: str
    node1: str
    node2: str
    length: float
    n: Optional[float] = 0  # roughness parameter
    z1: Optional[float] = 0
    z2: Optional[float] = 0
    Q0: Optional[float] = 0
    Qmax: Optional[float] = 0

    @staticmethod
    def fict_cond(fict_conds: List) -> List['conduit']:
        conduits_list = []
        names_set: Set[str] = set()

        for element in fict_conds:
            zn = None
            if element.knoten:
                knoten = element.knoten[0]
                for i, knoten in enumerate(element.knoten):
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        zn = float(punkt.z)

            conduit_sgl = conduit(
                name=element.objektbezeichnung,
                node1=element.objektbezeichnung + '_B',
                node2=element.objektbezeichnung + '_A',
                length=0.1,
                n=0.01,
                z1=zn + 0.1 if zn is not None else 0,
                z2=zn if zn is not None else 0,
                Q0=0,
                Qmax=0
            )
            if conduit_sgl.name not in names_set:
                names_set.add(conduit_sgl.name)
                conduits_list.append(conduit_sgl)

        return conduits_list

    @staticmethod
    def from_haltung(haltung_list: List) -> List['conduit']:
        conduits_list = []
        names_set: Set[str] = set()

        for haltung in haltung_list:
            conduit_sgl = conduit(
                name=haltung.objektbezeichnung,
                node1=haltung.zulauf or 'NONE FOUND',
                node2=haltung.ablauf or 'NONE FOUND',
                length=haltung.laenge,
                n=0.01,  # concrete
                z1=haltung.zulauf_sh if haltung.zulauf_sh is not None else 0,
                z2=haltung.ablauf_sh if haltung.ablauf_sh is not None else 0,
                Q0=0,
                Qmax=0
            )
            if conduit_sgl.name not in names_set:
                names_set.add(conduit_sgl.name)
                conduits_list.append(conduit_sgl)

        return conduits_list

    @staticmethod
    def to_conduits_str(conduits_list: List) -> str:
        header = [
            "[CONDUITS]",
            ";;                          Inlet                     Outlet                               Manning    Inlet      Outlet     Init.      Max.",
            ";;Name                      Node                      Node                      Length     N          Offset     Offset     Flow       Flow",
            ";;------------------------- ------------------------- ------------------------- ---------- ---------- ---------- ---------- ---------- ----------"
        ]
        conduits_strings = []
        names_set: Set[str] = set()

        for conduit in conduits_list:
            if conduit.name not in names_set:
                data = f"{conduit.name:<28}{conduit.node1:<28}{conduit.node2:<28}{conduit.length:<10}{conduit.n:<8}{conduit.z1:<12}{conduit.z2:<12}{conduit.Q0:<12}{conduit.Qmax:<12}"
                conduits_strings.append(data)
                names_set.add(conduit.name)

        return "\n".join(header + conduits_strings)



@dataclass
class pump:
    name: str
    node1: str
    node2: str
    pcurve: str
    status: str
    startup: Optional[float] = 0
    shutoff: Optional[float] = 0
    Xcoord: Optional[float] = 0
    Ycoord: Optional[float] = 0
    Zcoord: Optional[float] = 0
    Xcoord1: Optional[float] = 0
    Ycoord1: Optional[float] = 0
    Zcoord1: Optional[float] = 0
    Xcoord2: Optional[float] = 0
    Ycoord2: Optional[float] = 0
    Zcoord2: Optional[float] = 0
    '''
     Drossel and Pumpe getting put together and stored as pump
     ----because most of Drossel getting as input an continuous laminar flow-----
    '''
    def get_drossel(bauwerk_list : List)-> List['Drossel']:
        drossel_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Drossel):
                drossel_list.append(bauwerk)
                print(f"Found Drossel...",{bauwerk})
        return drossel_list
    def get_pump(bauwerk_list : List)-> List['Pumpe']:
        '''returns isybau pumpen from bauwerke '''
        pumpe_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Pumpe):
                pumpe_list.append(bauwerk)
                print(f"Found Pumpe...",{bauwerk})
        return pumpe_list
    def get_pumpwerk(bauwerk_list: List)-> List['Pumpwerk']:
        pumpwerk_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Pumpwerk):
                pumpwerk_list.append(bauwerk)
                print(f"Found Pumpwerk...",{bauwerk.objektbezeichnung})
        return pumpwerk_list
    def from_drossel(drossel_list: List, pumps_list)-> List['pump']:
        for drossel in drossel_list:
            if drossel.knoten:
                knoten = drossel.knoten[0]
                
                for i, knoten in enumerate(drossel.knoten):
                    if knoten.punkte:
                        punkt= knoten.punkte[0]
                        Xcoord = float(punkt.x)
                        Ycoord = float(punkt.y)
                        Zcoord = float(punkt.z)
                    else: 
                        print("No PUNKTE in this KNOTEN")
                
            drossel_sgl = pump(
                name= drossel.objektbezeichnung,
                node1 = drossel.objektbezeichnung + '_B',
                node2 = drossel.objektbezeichnung + '_A',
                pcurve= 'coming',  #-------------------------------------------->
                status = 'ON',
                startup = 0,
                shutoff = 0,
                Xcoord= Xcoord,
                Ycoord= Ycoord,
                Zcoord= Zcoord

            )
            pumps_list.append(drossel_sgl)
        return pumps_list
   
    def from_pumpe(pumpe_list: List, pumps_list)-> List['pump']:   
        for pumpe in pumpe_list:
            if pumpe.knoten:
                knoten = pumpe.knoten[0]
                
                for i, knoten in enumerate(pumpe.knoten):
                    if knoten.punkte:
                        punkt= knoten.punkte[0]
                        Xcoord = float(punkt.x)
                        Ycoord = float(punkt.y)
                        Zcoord = float(punkt.z)
                    else: 
                        print("No PUNKTE in this KNOTEN")
            pump_sgl = pump(
                name = pumpe.objektbezeichnung,
                node1 = pumpe.objektbezeichnung + '_B',
                node2 = pumpe.objektbezeichnung + '_A',
                pcurve= 'coming',  #-------------------------------------------->
                status = 'ON',
                startup = 0,
                shutoff = 0,
                Xcoord= Xcoord,
                Ycoord= Ycoord,
                Zcoord = Zcoord
            )
            pumps_list.append(pump_sgl)
            
        return pumps_list
    
    def from_pumpwerk(pumpwerk_list: List, pumps_list)-> List['pump']:
        
        for pumpwerk in pumpwerk_list:
            if pumpwerk.knoten:
                knoten = pumpwerk.knoten[0]
                
                for i, knoten in enumerate(pumpwerk.knoten):
                    if knoten.punkte:
                        punkt= knoten.punkte[0]
                        Xcoord = float(punkt.x)
                        Ycoord = float(punkt.y)
                        Zcoord = float(punkt.z)
                    else: 
                        print("No PUNKTE in this KNOTEN")
            pumpwerk_sgl = pump(
                name = pumpwerk.objektbezeichnung,
                node1 = pumpwerk.objektbezeichnung + '_B',
                node2 = pumpwerk.objektbezeichnung + '_A',
                pcurve= 'coming',  #-------------------------------------------->
                status = 'ON',
                startup = 0,
                shutoff = 0,
                Xcoord= Xcoord,
                Ycoord= Ycoord,
                Zcoord= Zcoord
            )
            pumps_list.append(pumpwerk_sgl)
        return pumps_list
    
    def write_fict_junctions(pumps_list: List, junction_list: List)-> List['junction']:
        elev = 0
        y0 = 0
        for pumps in pumps_list:
            if pumps.Zcoord is not None:
                elev = pumps.Zcoord
            ymax = 0
            y0 = 0
            junction_a = junction(
                        name = pumps.name + '_A' if pumps.name is not None else '',
                        elev = elev ,
                        y0 = y0 ,
                        ysur=0,
                        apond=0
                            )
            junction_b = junction(
                        name = pumps.name + '_B' if pumps.name is not None else '',
                        elev = round(elev + 0.1, 2) ,
                        y0 = round(y0 + 0.1, 2) ,
                        ysur=0,
                        apond=0
                            )
            junction_list.append(junction_a)
            print(junction_a)
            junction_list.append(junction_b)
            print(junction_b)
        return junction_list
    
    def write_fict_conduits(pumps_list: List, conduits_list: List)-> List['conduit']:
        names_set: Set[str] = set()

        for pumps in pumps_list:
            if pumps.Zcoord is not None:
                zn = pumps.Zcoord
            ymax = 0
            y0 = 0

            conduit_sgl = conduit(
                name=pumps.name,
                node1=pumps.name + '_B',
                node2=pumps.name + '_A',
                length=1.0,
                n=0.01,
                z1=round(zn + 0.1, 2) if zn is not None else 0.00,  
                z2=round(zn, 2) if zn is not None else 0.00,
                Q0=0,
                Qmax=0
            )
            if conduit_sgl.name not in names_set:
                names_set.add(conduit_sgl.name)
                conduits_list.append(conduit_sgl)

        return conduits_list
    
    def write_fict_coords(pumps_list: List[Pumpe], coordinates_list: List['coordinates']) -> List['coordinates']:
        for pump in pumps_list:
            x0, y0 = pump.Xcoord, pump.Ycoord
            node1 = pump.node1
            node2 = pump.node2

            # Calculate the two points that are 0.5 units away from the original point in opposite directions
            # Let's assume the angle is 0 degrees (horizontal line)
            angle = 0  # Angle in degrees; can be adjusted as needed
            angle_rad = math.radians(angle)  # Convert to radians

            # Calculate the first point
            x1 = x0 - math.cos(angle_rad) * 0.5
            y1 = y0 - math.sin(angle_rad) * 0.5

            # Calculate the second point
            x2 = x0 + math.cos(angle_rad) * 0.5
            y2 = y0 + math.sin(angle_rad) * 0.5
            pump.Xcoord1 = x1
            pump.Ycoord1 = y1
            pump.Xcoord2 = x2
            pump.Ycoord2 = y2
            # Create the coordinates objects
            coord1 = coordinates(
                node=node1,
                Xcoord=x1,
                Ycoord=y1
            )
            coord2 = coordinates(
                node=node2,
                Xcoord=x2,
                Ycoord=y2
            )

           
            coordinates_list.append(coord1)
            coordinates_list.append(coord2)

        return coordinates_list

    def to_pumps_string(pumps_list: List) -> str:
        header = [
            "[PUMPS]",
            ";;               Inlet            Outlet                                 Start      Shut",
            ";;Name           Node             Node             Pcurve     Status     up         off",
            ";;-------------- ---------------- ---------------- ---------- ---------- ---------- ----------"
        ]
        pumps_string = []
        for pump in pumps_list:
            

            data = f"{pump.name:<15} {pump.node1:<15} {pump.node2:<15} {pump.pcurve:<10} {pump.status:<10} {pump.startup:<10} {pump.shutoff:<10}"
            pumps_string.append(data)
    
        return '\n'.join(header + pumps_string)


@dataclass
class orifice: #SCHIEBER 
    name: str
    node1: str
    node2: str
    typ: str='SIDE'  # can also be BOTTOM
    offset: Optional[float] = 0
    crest : Optional[float] = 0
    cd: Optional[float] = 0
    flap:  str='NO'
    orate: Optional[float] = 0
    def get_schieber(bauwerk_list: List)-> List['Schieber']:
        schieber_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Schieber):
                schieber_list.append(bauwerk)
        return schieber_list
    def to_junctions(schieber_list :List, junction_list: List):
        for schieber in schieber_list:
            fict_junc = junction.fict_junc(schieber)
            junction_list.append(fict_junc)
        return junction_list
    def to_conduit(schieber_list: List, conduit_list: List):
        for schieber in schieber_list:
            fict_cont = conduit.fict_cond(schieber)
            conduit_list.append(fict_cont)
        return conduit_list
    def from_schieber(schieber_list: List, haltung_list: List)->List['orifice']:
        orifices_list = []
        for schieber in schieber_list:
            for haltung in haltung_list:
                from_schieber = next((node for node in node_list if node.objektbezeichnung == haltung.zulauf), None)
                if from_schieber:
                    if haltung.zulauf_sh is not None:
                        sh_orifice = haltung.zulauf_sh
            if schieber.knoten:
                knoten = schieber.knoten[0]
                print(f"Schieber: {schieber.objektbezeichnung}")
                print(f"Number of Knoten: {len(schieber.knoten)}")
                for i, knoten in enumerate(schieber.knoten):
                    print(f"  Knoten {i + 1}:")
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        elev = float(punkt.z)
                        print(f"    Elevation (elev): {elev}")
                    else:
                        print("No Punkte in this Knoten")
            if elev is not None and sh_orifice is not None:
                crest_height = abs(sh_orifice - elev) 
            orifice_sgl = orifice(
                name = schieber.objektbezeichnung,
                node1 = schieber.objektbezeichnung + '_B',
                node2 = schieber.objektbezeichnung + '_A',
                typ = 'SIDE',
                offset = 0,
                crest= crest_height,
                cd = 0.65,
                flap = 'NO',
                orate= 0
            )
            orifices_list.append(orifice_sgl)
        return orifices_list
    def to_orifices_string(orifices_list: List)-> str:
        header = [
            "[ORIFICES]",
            ";;               Inlet            Outlet           Orifice      Crest      Disch.     Flap Open/Close",
            ";;Name           Node             Node             Type         Height     Coeff.     Gate Time",      
            ";;-------------- ---------------- ---------------- ------------ ---------- ---------- ---- ----------"
        ]
        orifice_strings = []
        for orifice in orifices_list:
            data = f"{orifice.name:<15} {orifice.ode1:<16} {orifice.node2:<16} {orifice.typ:<12} {orifice.crest:<10} {orifice.cd:<10} {orifice.flap:<4} {orifice.orate:<4}"
            orifice_strings.append(data)
            return '\n'.join(header + orifice_strings)
        

@dataclass
class weirs:   # WEHR
    name: str
    node1: str
    node2: str
    typ: str #TRANSVERSE, SIDEFLOW, V-NOTCH, TRAPEZOIDAL or ROADWAY
    crestht: Optional[float] = 0
    cd: float = 3322
    gated: str = 'NO' #YES if flap gate present to prevent reverse flow, NO if not (default is NO)
    ec: float= 0
    cd2: float = 3322
    sur: str = 'YES' 
    width: Optional[float] = 0
    surface: Optional[str] = None
    def get_cresth(wehr_list: List, haltung_list: List)->str:
        for haltung in haltung_list:
            from_wehr = next((wehr for wehr in wehr_list if wehr.objektbezeichnung == haltung.zulauf), None)
            if from_wehr:
                if haltung.zulauf_sh is not None:
                    sh_weirs = haltung.zulauf_sh
            if wehr.knoten:
                knoten = wehr.knoten[0]
                print(f"Schieber: {wehr.objektbezeichnung}")
                print(f"Number of Knoten: {len(wehr.knoten)}")
                for i, knoten in enumerate(wehr.knoten):
                    print(f"  Knoten {i + 1}:")
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        elev = float(punkt.z)
                        print(f"    Elevation (elev): {elev}")
                    else:
                        print("No Punkte in this Knoten")
            if elev is not None and sh_orifice is not None:
                crest_height = abs(sh_orifice - elev) 
        return crest_heigh
    def get_type (wehr)->str:
        if wehr.wehrtyp == 1:
            typ = 'TRANSVERSE'
            return typ
        if wehr.wehrtyp == 2: 
            typ = 'SIDEFLOW'
            return typ
        else:
            print('no fitting weirs-type using TRANSVERSE')
            typ = 'TRANSVERSE'
            return typ 
    def get_gated(wehr)-> str: 
        if wehr.wehrtyp == 3 or 4:
            gated = 'YES'
            return gated
        else: 
            gated = 'NO'
            return gated
    def get_weirs(bauwerk_list: List)-> List['Wehr']:
        wehr_list = []
        for bauwerk in bauwerk_list:
            if isinstance (bauwerk, Wehr):
                wehr_list.append(bauwerk)
        return wehr_list
    def to_junctions(wehr_list :List, junction_list: List):
        for wehr in wehr_list:
            fict_junc = junction.fict_junc(wehr)
            junction_list.append(fict_junc)
        return junction_list
    def to_conduit(wehr_list: List, conduits_list: List):
        for wehr in wehr_list:
            fict_cont = conduit.fict_cond(wehr)
            conduits_list.append(fict_cont)
        return conduits_list
    '''def from_wehr(wehr_list: List, haltung_list: List)-> List['weirs']:
        weirs_list = []
        for wehr in wehr_list:
            typ = get_type(wehr)
            crestht = get_cresth(wehr, haltung_list)
            gated = get_gated(wehr)
            weirs_sgl = weirs(
                name = wehr.objektbezeichnung.,
                node1 = wehr.objektbezeichnung + '_B',
                node2 = wehr.objektbezeichnung + '_A',
                typ = typ ,
                crestht = crestht,
                cd = 3, #---------
                gated = gated,
                ec = 0,
                cd2 = 3322,
                sur = 'YES',
                width = 0,
                surface = None
            ) 
        return weirs_list'''
    def to_weirs_strings(weirs_list: List)-> str:
        header = [
        "[WEIRS]",
        ";;               Inlet            Outlet           Weir         Crest      Disch.     Flap End      End",       
        ";;Name           Node             Node             Type         Height     Coeff.     Gate Con.     Coeff.",    
        ";;-------------- ---------------- ---------------- ------------ ---------- ---------- ---- -------- ----------"
        ]
        weir_strings = []
        for weir in weirs_list:
            data = f"{weir.name:<(15)} {weir.node1:<(16)} {weir.node2:<(16)} {weir.typ:<(12)} {str(weir.crestht):<(10)} {str(weir.cd):<(10)} {weir.gated:<(4)}"
            weir_strings.append(data)
        return '\n'.join(header + weir_strings)

'''Dont know if this needs to be used '''
@dataclass
class outlets: 
    name: str
    node1: str
    node2: str
    offset: Optional[float] = None
    Qcurve: Optional[str] = None
    c1: Optional[float] = 0
    c2: Optional[float] = 0
    gated: str= 'NO'
   
    
@dataclass
class xsection:
    link: str  
    shape: str
    geom1: float
    geom2: Optional[float] = 0 
    geom3: Optional[float] = 0
    geom4: Optional[float] = 0
    barrels: int = 1 
    culvert: Optional[int] = None
    curve: Optional[str] = None
    tsec: Optional[str] = None
    def from_haltung(haltung_list: List[Haltung])-> List['xsection']:
        xsection_list= []
        for haltung in haltung_list:
            
            link = haltung.objektbezeichnung
            if haltung.profilart == int(0):
                shape = 'CIRCULAR'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = 0,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
                else:
                    print(f'NO DN for Haltung: {haltung.objektbezeichnung} setting to 250mm')
                    geom1 = float(0.25)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = 0,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)

            elif haltung.profilart == int(1):
                shape = 'EGG'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = 0,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
                else:
                    print(f'NO DN for Haltung: {link} setting to 500mm')
                    geom1 = float(0.5)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = 0,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
            
            elif haltung.profilart == int(2):
                shape = 'CATENARY'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = 0,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
                else:
                    print(f'NO DN for Haltung: {link} setting to 500mm')
                    geom1 = float(0.5)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = 0,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
            
            elif haltung.profilart == int(3):
                shape = 'RECT_CLOSED'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                    if haltung.profilbreite is not None:
                        geom2 = float(haltung.profilbreite / 1000)
                        xsection_sgl = xsection(
                                                link = link,
                                                shape = shape,
                                                geom1= geom1,
                                                geom2 = geom2,
                                                geom3 = 0,
                                                geom4 = 0
                                                    )
                        xsection_list.append(xsection_sgl)
                    else: 
                        print(f'NO profilbreite for Haltung: {link} setting to 1000mm')
                        geom2 = float(1.0)
                        xsection_sgl = xsection(
                                                link = link,
                                                shape = shape,
                                                geom1= geom1,
                                                geom2 = geom2,
                                                geom3 = 0,
                                                geom4 = 0
                                                    )
                        xsection_list.append(xsection_sgl)
                else:
                    print(f'NO Geometry for Haltung: {link} setting to 1/2')
                    geom1 = float(0.5)
                    geom2 = float(1.0)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = geom2,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
                
            
            elif haltung.profilart == int(5):
                shape = 'RECT_OPEN'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                    if haltung.profilbreite is not None:
                        geom2 = float(haltung.profilbreite / 1000)
                        xsection_sgl = xsection(
                                                link = link,
                                                shape = shape,
                                                geom1= geom1,
                                                geom2 = geom2,
                                                geom3 = 0,
                                                geom4 = 0
                                                    )
                        xsection_list.append(xsection_sgl)
                    else: 
                        print(f'NO profilbreite for Haltung: {link} setting to 1000mm')
                        geom2 = float(1.0)
                        xsection_sgl = xsection(
                                                link = link,
                                                shape = shape,
                                                geom1= geom1,
                                                geom2 = geom2,
                                                geom3 = 0,
                                                geom4 = 0
                                                    )
                        xsection_list.append(xsection_sgl)
                else:
                    print(f'NO Geometry for Haltung: {link} setting to 1/2')
                    geom1 = float(0.5)
                    geom2 = float(1.0)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = geom2,
                                            geom3 = 0,
                                            geom4 = 0
                                                )
                    xsection_list.append(xsection_sgl)
            
            elif haltung.profilart == int(8):
                shape = 'TRAPEZOIDAL'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                    if haltung.profilbreite is not None:
                        geom2 = float(haltung.profilbreite / 1000)
                        geom3 = 0.5
                        geom4 = 0.5 
                        xsection_sgl = xsection(
                                                link = link,
                                                shape = shape,
                                                geom1= geom1,
                                                geom2 = geom2,
                                                geom3 = geom3,
                                                geom4 = geom4
                                                    )
                        xsection_list.append(xsection_sgl)
                    else: 
                        print(f'NO profilbreite for Haltung: {link} setting to 1000mm')
                        geom2 = float(1.0)
                        xsection_sgl = xsection(
                                                link = link,
                                                shape = shape,
                                                geom1= geom1,
                                                geom2 = geom2,
                                                geom3 = geom4,
                                                geom4 = geom4
                                                    )
                        xsection_list.append(xsection_sgl)
                else:
                    print(f'NO Geometry for Haltung: {link} setting to 1/2')
                    geom1 = float(0.5)
                    geom2 = float(1.0)
                    xsection_sgl = xsection(
                                            link = link,
                                            shape = shape,
                                            geom1= geom1,
                                            geom2 = geom2,
                                            geom3 = geom3,
                                            geom4 = geom4
                                                )
                    xsection_list.append(xsection_sgl)
            
            
        
        return xsection_list
    def to_xsection_string(xsection_list : List)-> str:
        header = [
            "[XSECTIONS]",
            ";;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels",   
            ";;-------------- ------------ ---------------- ---------- ---------- ---------- ----------",
        ]
        xsection_strings = []
        for xsection in xsection_list:
            data = f"{xsection.link:<15}{xsection.shape:<15}{xsection.geom1:<10}{xsection.geom2:<10}{xsection.geom3:<10}"\
                   f"{xsection.geom4:<10}{xsection.barrels:<4}"
            xsection_strings.append(data)
        return"\n".join(header + xsection_strings)

    
    
'''Only needed when DYNAMIC WAVE in Options'''
@dataclass
class losses:
    conduit: str
    kentry: Optional[float]
    kexit: Optional[float]
    kavg: Optional[float]
    flap: str = 'YES'
    seepage: float= 0
'''Only needed when river and other irregulare shape'''
@dataclass
class transects:
    name: str 
    nleft: float = 0
    nright: float = 0
    nchanl: float = 0
    nsta: Optional[float] = 0
    xleft: Optional[float] = 0
    xright: Optional[float] = 0
    lfactor: float = 0
    wfactor: float = 0
    Eoffset: float = 0
    elev: Optional[float] = 0
    station: Optional[float] = 0
'''NO SUPPORT FOR CONTROLS'''
'''pullutants will be later added need to search data first'''
@dataclass
class pollutants:
    name: str
    units: str = 'MG/L'
    crain: Optional[float] = 0
    cgw: Optional[float] = 0
    cii: Optional[float] = 0
    kdecay: Optional[float] = 0
    sflag: str = 'NO'

@dataclass
class landuses:
    name: str
    sweepintervall: Optional[int] = 0
    availability: Optional[float] = 0
    lastsweep: Optional[int]= 0

@dataclass
class coverages:
    subcat: str
    landuse: str
    percent: float

@dataclass
class loadings:
    subcat: str
    pollut: str
    initbuildup: float #kg/hectare

@dataclass
class buildup:
    landuse: str
    pollutant: str
    functype: str
    c1: str
    c2: str
    c3: str
    perunit: str= 'AREA'

@dataclass
class washoff:
    landuse: str
    pollutant: str
    functype: str
    c1: str
    c2: str
    sweeprmvl: float
    bmprmvl: float

@dataclass
class treatment: 
    node: str
    pollut: str
    result: str= 'R'
    func: str = 'FLOW'

@dataclass
class inflow:
    node: str
    pollut: str
    tseries: str
    type: str = 'CONCEN'
    mfactor: float = 1.0
    sfactor: float = 1.0
    base: Optional[float] = 0
    pat: Optional[str] = None

@dataclass
class dwf: # Trockenwetterabfluss
    node: str
    type: str = 'FLOW'
    base: Optional[float] = 0

@dataclass
class hydrographs:
    name: str
    raingage: str
    month: str = 'ALL'
    term: str= 'MEDIUM'  #SHORT ; MEDIUM ; LONG
    R: Optional[float] = 0
    T: Optional[float] = 0
    K: float = 2.0

@dataclass
class curves:
    name: str
    typ: str
    x_values: List[float]
    y_values: List[float]

    def set_curve(element) -> List[float]:
        height_steps = []
        height = float(element.knoten[0].punkte[1].z) - float(element.knoten[0].punkte[0].z)


        if height is None or height < 0.5:
            height_steps = [0.4]  
        else:

            for step in range(1, int(height * 10) + 1):
                height_steps.append(step * 0.1)

        return height_steps


    def get_curves(storages_list: List, pumps_list: List, pumps_list_d: List) -> List['curves']:
            curves_list = []
            for storage in storages_list:
            
                x_values = curves.set_curve(storage)  
                curve_sgl = curves(
                    name=storage.name,
                    typ='STORAGE', #x_y values in m²
                    x_values=x_values  
                )
                curves_list.append(curve_sgl)
            return curves_list

        
    
@dataclass
class timeseries:
    name: str
    date: str
    hour: str
    time: float
    value: str
    @staticmethod
    def to_rain_string(x, y):
        rain_data = rain_wrapper(x, y)
        date = ''
        header = [
            "[TIMESERIES]",
            ";;Name           Date       Time       Value",
            ";;-------------- ---------- ---------- ----------" 
        ]
        rain_strings = []

        for duration in rain_data.keys():
            for yearly_rain_type in rain_data[duration].keys():
                if yearly_rain_type.endswith('_euler'):
                    name = yearly_rain_type[:-6]
                    max_name_length = max(len(name), 10)  # Adjust for minimum column width
                    euler_data = rain_data[duration][yearly_rain_type]
                    rain_string = ""
                    for time_point, rain_value in euler_data:
                        rain_string += f"{name:<{max_name_length}}{date:13}{'':5}{time_point: >5}:00{'':5}{rain_value:.2f}\n"
                    rain_strings.append(rain_string)

        return "\n".join(header + rain_strings)

@dataclass
class report:
    input: str = 'NO'
    continuity: str = 'NO'
    flowstats: str = 'NO'
    controls: str = 'NO'
    subcatchments: str = 'ALL'
    nodes: str = 'ALL'
    links: str = 'ALL'

    def to_report_string(self) -> str:
        # Create the header
        header = ["[REPORT]"]

        # Join the attribute values with newlines and add extra spaces for alignment
        values = "\n".join([
            f"INPUT     {self.input: <12} \nCONTINUITY     {self.continuity: <12}",     
            f"FLOWSTATS     {self.flowstats: <12}\nCONTROLS     {self.controls: <12}",
            f"SUBCATCHMENTS     {self.subcatchments: <12}\nNODES         {self.nodes: <12}",
            f"LINKS     {self.links: <12}"
        ])

        return "\n".join(header + [values])

@dataclass
class map:
    X1: float
    Y1: float
    X2: float
    Y2: float

    @classmethod
    def calc_dimensions(cls, coordinates_list: List['coordinates']):
        Xs = [coord.Xcoord for coord in coordinates_list]
        Ys = [coord.Ycoord for coord in coordinates_list]
        X1, Y1 = min(Xs), min(Ys)
        X2, Y2 = max(Xs), max(Ys)
        return cls(X1, Y1, X2, Y2)
    def to_map_string(self)-> str : 
        header = "[MAP]"
        dimensions = f"DIMENSIONS  {self.X1} {self.Y1} {self.X2} {self.Y2}"
        units = "UNITS     METERS"
        return f"{header}\n{dimensions}\n{units}"

@dataclass
class tags:
    pass

@dataclass
class coordinates:
    node: str
    Xcoord: float
    Ycoord: float

    def from_schacht(schacht_list: List) -> List['coordinates']:
        coordinates_list = []
        for schacht in schacht_list:
            if schacht.knoten:
                knoten = schacht.knoten[0]
                node = schacht.objektbezeichnung
                for i, knoten in enumerate(schacht.knoten):
                    if knoten.punkte:
                        punkt= knoten.punkte[0]
                        Xcoord = float(punkt.x)
                        Ycoord = float(punkt.y)
                    else: 
                        print("No PUNKTE in this KNOTEN")
                node_sgl = coordinates(
                    node=node,
                    Xcoord=Xcoord,
                    Ycoord=Ycoord
                )            
                coordinates_list.append(node_sgl)
        return coordinates_list
    
            
    @staticmethod
    def to_coordinates_string(coordinates_list: List['coordinates']) -> str: 
        header = [
            "[COORDINATES]",
            ";;Node           X-Coord            Y-Coord  ",         
            ";;-------------- ------------------ ------------------"
        ]
        coordinates_strings = []
        for coordinate in coordinates_list:
            data = f"{coordinate.node:<16} {coordinate.Xcoord:<20} {coordinate.Ycoord:<20}"
            coordinates_strings.append(data)
        return '\n'.join(header + coordinates_strings)
  


@dataclass #still not working 
class vertices:
    link: str
    Xcoord: float
    Ycoord: float
   
    def from_haltung(haltung_list: List) -> List['vertices']:
        vertices_list = []
        for haltung in haltung_list:
            link = haltung.objektbezeichnung
            if haltung.polygon:
                for kanten in haltung.polygon:
                    Xcoord_S = kanten.start.punkt.x
                    #print(Xcoord_S)
                    Ycoord_S = kanten.start.punkt.y
                    #print(Ycoord_S)
                    Xcoord_E = kanten.ende.punkt.x
                    #print(Xcoord_E)
                    Ycoord_E = kanten.ende.punkt.y
                    #print(Ycoord_E)
                    vertices_start = vertices(
                        link=link,
                        Xcoord=Xcoord_S,
                        Ycoord=Ycoord_S
                    )
                    vertices_ende = vertices(
                        link=link,
                        Xcoord=Xcoord_E,
                        Ycoord=Ycoord_E
                    )
                    vertices_list.append(vertices_start)
                    vertices_list.append(vertices_ende)
        
        print(f'dont work yet :/{vertices_list}')
        return vertices_list
    
    def to_vertices_string(vertices_list: List)-> str: 
        header = [
            "[VERTICES]",
            ";;Link           X-Coord            Y-Coord  ",
            ";;-------------- ------------------ ------------------"
        ]
        vertices_strings = []
        for vertices in vertices_list:
            data = f"{vertices.link:<16} {vertices.Xcoord:<20}{vertices.Ycoord:<20}"
            vertices_strings.append(data)
        return '\n'.join(header + vertices_strings)

'''Dont know if its working with Hatlung which have an polyline added for example when there
are more then one kante inside the polygon'''
                


@dataclass
class polygons:
    subcat: str
    Xcoord: float
    Ycoord: float 
    def from_flaeche(flaechen_list: List)-> List['polygons']:
        polygons_list= []
        for flaeche in flaechen_list:
            subcat = flaeche.objektbezeichnung
            if flaeche.polygon:
                for kanten in flaeche.polygon:
                        Xcoord_S = kanten.start.punkt.x
                        #print(Xcoord_S)
                        Ycoord_S = kanten.start.punkt.y
                        #print(Ycoord_S)
                        Xcoord_E = kanten.ende.punkt.x
                        #print(Xcoord_E)
                        Ycoord_E = kanten.ende.punkt.y
                        #print(Ycoord_E)
                        polygon_start = polygons(
                            subcat = subcat,
                            Xcoord = Xcoord_S,
                            Ycoord = Ycoord_S
                        )
                        polygon_end = polygons(
                            subcat = subcat,
                            Xcoord = Xcoord_E,
                            Ycoord = Ycoord_E
                        )
                        polygons_list.append(polygon_start)
                        polygons_list.append(polygon_end)
        #print(polygons_list)
        return polygons_list
    def to_polygons_string(polygons_list: List)-> str:
        header = [
            "[Polygons]", 
            ";;Subcatchment                    X-Coord            Y-Coord",           
            ";;------------------------------ ------------------ ------------------"
            ]
        polygons_strings = []
        for polygons in polygons_list:
            data = f"{polygons.subcat:<32}{polygons.Xcoord:<20}{polygons.Ycoord:<20}"
            polygons_strings.append(data)
        return '\n'.join(header +    polygons_strings)




@dataclass
class symbols: 
    gage: str
    Xcoord: float
    Ycoord: float
    def from_raingage(schacht_list: List)-> List['symbols']:
        symbols_list = []
        Xcoord, Ycoord = site_middle(schacht_list)
        symbol_sgl = symbols(
            gage = "RainGage",
            Xcoord = Xcoord,
            Ycoord = Ycoord
        )
        symbols_list.append(symbol_sgl)
        return symbols_list
    def to_symbols_strings(symbols_list: List)->str:
        header = [  '[SYMBOLS]',
                    ';;Gage           X-Coord            Y-Coord',           
                    ';;-------------- ------------------ ------------------'
        ]
        symbols_strings = []
        for symbol in symbols_list:
            data = f"{symbol.gage:<16}{symbol.Xcoord:<20}{symbol.Ycoord:<20}"
            symbols_strings.append(data)
        return '\n'.join(header + symbols_strings)

@dataclass
class labels:
    Xcoord: float
    Ycoord: float
    label: str
    anchor: str
    font: str
    size: int
    bold: str = 'NO'
    italic: str = 'NO'
    
    pass 

@dataclass
class backdrop:
    fname: str
    X1: float
    Y1: float
    X2: float
    Y2: float
    def from_utils(schacht_list: List):
        points = site_corner(schacht_list)
        if points is None:
            raise ValueError("Not enough points to determine farthest points")

        (X1, Y1), (X2, Y2) = points
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        backdrop_sgl = backdrop(
            fname=f'hg_{current_time}.png',
            X1=X1,
            Y1=Y1,
            X2=X2,
            Y2=Y2
        )
        return backdrop_sgl
    def to_backdrop_string(self) -> str:
        header = [
            '[BACKDROP]',
            ';;Filename          X1                 Y1                 X2                 Y2',
            ';;----------------- ----------------- ----------------- ----------------- -----------------'
        ]
        data = f"{self.fname:<17} {self.X1:<17} {self.Y1:<17} {self.X2:<17} {self.Y2:<17}"
        return '\n'.join(header + [data])


def create_inp(metadata, flaechen_list, schacht_list, haltung_list, bauwerk_list):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    x = 6.99641136598768
    y = 49.2853524841828
    pumps_list = []
    
    coordinate_list = []
    report_1 =report(input='NO', continuity='NO', flowstats='NO', controls='NO', subcatchments='ALL', nodes='ALL', links='ALL')
    subcatchment_list = subcatchments.from_flache(flaechen_list)
    subarea_list = subareas.from_subcatchment(subcatchment_list)
    infiltration_list = infiltration_H.from_subcatchment(subcatchment_list)
    junction_list = junction.from_node_elem(schacht_list, bauwerk_list)
    #------------working
    conduit_list = conduit.from_haltung(haltung_list)
    xsection_list = xsection.from_haltung(haltung_list)
    pumpe_list = pump.get_pump(bauwerk_list)
   
    drossel_list = pump.get_drossel(bauwerk_list)
  
    pumpwerk_list = pump.get_pumpwerk(bauwerk_list)

    pumps_list = pump.from_drossel(drossel_list, pumps_list)

    pumps_list = pump.from_pumpe(pumpe_list, pumps_list)

    pumps_list = pump.from_pumpwerk(pumpwerk_list, pumps_list)
    print(f"Pumps_list:{pumps_list}")
    if pumps_list:
        junction_list =pump.write_fict_junctions(pumps_list, junction_list)
    else:
        print("No pumps in pumps_list. Skipping write_fict_junctions.")
    print(junction_list)
    conduit_list =pump.write_fict_conduits(pumps_list, conduit_list)

    coordinate_list= pump.write_fict_coords(pumps_list, coordinate_list)

    
   
    #orc etc
    outfall_list = outfall.check_outfall(schacht_list, haltung_list, bauwerk_list)
    coordinate_list = coordinates.from_schacht(schacht_list)
    vertices_list = vertices.from_haltung(haltung_list)
    polygons_list = polygons.from_flaeche(flaechen_list)
    symbols_list = symbols.from_raingage(schacht_list)
    backdrop_sgl = backdrop.from_utils(schacht_list)

    junction_list = remove_outfall_double(junction_list, outfall_list)

    with open(f"hydraulik/inp/model{current_time}.inp", "w") as f:
        f.write("[TITLE]\n")
        f.write(metadata.to_title_string())
        f.write("\n")
        f.write("[OPTIONS]\n")
        f.write(option.to_options_string(option_data))
        f.write("\n")
        f.write("\n")
        f.write(evaporation.to_evaporation_string(evaporation_data))
        f.write("\n")
        f.write("\n")
        f.write(raingage.to_raingage_string(raingage_data))
        f.write("\n")
        f.write("\n")
        f.write(subcatchments.to_subcatchment_string(flaechen_list, subcatchment_list))
        f.write("\n")
        f.write("\n")
        f.write(subareas.to_subarea_string(subarea_list, subcatchment_list))
        f.write("\n")
        f.write("\n")
        f.write(infiltration_H.to_infiltration_string(infiltration_list, subcatchment_list))
        f.write("\n")
        f.write("\n")
        f.write(junction.to_junction_string(junction_list))
        f.write("\n")
        f.write("\n")
        f.write(conduit.to_conduits_str(conduit_list))
        f.write("\n")
        f.write("\n")
        f.write(xsection.to_xsection_string(xsection_list))
        f.write("\n")
        f.write("\n")
        f.write(pump.to_pumps_string(pumps_list))
        f.write("\n")
        f.write("\n")
        f.write(outfall.to_outfall_string(outfall_list))
        f.write("\n")
        f.write("\n")
        f.write(timeseries.to_rain_string(x,y))
        f.write("\n")
        f.write("\n")
        f.write(report_1.to_report_string())
        f.write("\n")
        f.write("\n")
        f.write(coordinates.to_coordinates_string(coordinate_list))
        f.write("\n")
        f.write("\n")
        f.write(vertices.to_vertices_string(vertices_list))
        f.write("\n")
        f.write("\n")
        f.write(polygons.to_polygons_string(polygons_list))
        f.write("\n")
        f.write("\n")
        f.write(symbols.to_symbols_strings(symbols_list))
        f.write("\n")
        f.write("\n")
        f.write(backdrop.to_backdrop_string(backdrop_sgl))
