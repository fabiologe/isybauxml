from xml_parser import * 
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Union
import random
import string


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
        # Create the value string. The source_info list is unrolled with space as separator
        source_info_str = ' '.join(self.source_info) if self.source_info else ''
        values = f"{self.name:<15s} {self.type:<9s} {self.interval:<6s} {str(self.catch):<6s} {self.source_type:<10s} {source_info_str}"
        # Join header and values with newline characters
        return "\n".join(header + [values])
    
raingage_data = raingage(name="RainGage", type="INTENSITY", interval="0:05", catch=1.0, source_type="TIMESERIES", source_info="2-yr")


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
                name= str(flaeche.objektbezeichnung) if flaeche.objektbezeichnung is not None else str(generate_unique_id()),
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
        subcatchments.from_flache(flaechen_list)
        header = [
            "[SUBCATCHMENTS]",
            ";;                                                 Total    Pcnt.             Pcnt.    Curb     Snow ",
            ";;Name           Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack ",
            ";;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- --------"
        ]
        subcatchment_strings = []
        for subcatchment in subcatchment_list:
            data = f"{subcatchment.name:<16} {subcatchment.raingage:<16} {subcatchment.outletID:<16} {subcatchment.area:<8} {subcatchment.imperv:<8} {subcatchment.width:<8} {subcatchment.slope:<8} {subcatchment.clength:<8}"#{subcatchment.spack:<8}
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
            ";;Subcatchment   N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted ",
            ";;-------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------"
        ]
        subarea_strings = []
        for subarea in subarea_list:
            data = f"{subarea.subcat:<16} {subarea.nimp:<16} {subarea.nperv:<16} {subarea.simp:<8} {subarea.sperv:<8} {subarea.zero:<8} {subarea.route_to:<8} {subarea.routed:<8}"
            subarea_strings.append(data)
        return '\n'.join(header + subarea_strings)

@dataclass
class infiltration_H: #For Horton/ Modified Horton
    subname: str
    maxrate: Optional[float] = 100 # maximum infiltration rate on Horton curve (in/hr or mm/hr)
    minrate: Optional[float] = 5 # minimum infiltration rate on Horton curve (in/hr or mm/hr)
    decay: Optional[float] = 6.5  # decay rate constant of Horton curve (1/hr).
    drytime: Optional[float] = 7 # time it takes for fully saturated soil to dry  (days).
    maxinf: Optional[float] =  0 #maximum infiltration volume possible  (mm)

    def from_subcatchment(subcatchment_list: List) -> List['infiltration_H']:
        infiltration_list = []
        for subcatchment in subcatchment_list:
            infiltration_sgl = infiltration_H(
                subname = str(subcatchment.name),
                maxrate = 100,
                minrate= 5,
                decay= 6.5,
                drytime= 7,
                maxinf= 0)
            infiltration_list.append(infiltration_sgl)
        return infiltration_list
    def to_infiltration_string(infiltration_list: List, subcatchment_list: List) -> str:
        infiltration_H.from_subcatchment(subcatchment_list)
        header = [
            "[INFILTRATION]",
            ";;Subcatchment   MaxRate    MinRate    Decay      DryTime    MaxInfil",
            ";;-------------- ---------- ---------- ---------- ---------- ----------"
        ]
        infiltration_strings = []
        for infiltration in infiltration_list:
            data = f"{infiltration.subname:<16} {infiltration.maxrate:<10} {infiltration.minrate:<10} {infiltration.decay:<10} {infiltration.drytime:<10} {infiltration.maxinf:<10}"
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

@dataclass
class junction:
    name: str
    elev: float  #SH
    ymax : Optional[float] = 0 #DH
    y0: Optional[float] = 0   #Wasserspiegel
    ysur: Optional[float] = 0 
    apond: Optional[float] = 0  #ueberflutungsflaeche
    def fict_junc(fict_junc: List):
        for element in fict_list:
            elev = None
            y0 = None
            if element-knoten:
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
                junction_a = junctions(
                            name = element.objektbezeichnung + '_A',
                            elev = elev,
                            y0 = y0 ,
                            ysur=0,
                            apond=0
                                )
                junction_b = junctions(
                            name = element.objektbezeichnung + '_B',
                            elev = elev + 0.1 ,
                            y0 = y0 + 0.1 ,
                            ysur=0,
                            apond=0
                                )
                fict_junc.append(junction_a)
                fict_junc.append(junction_b)
        return fict_junc

    def from_schacht(schacht_list: List) -> List['junction']:
        junctions_list = []
        for schacht in schacht_list:
            elev = None
            y0 = None
            if schacht.knoten:
                knoten = schacht.knoten[0]
                print(f"Schacht: {schacht.objektbezeichnung}")
                print(f"Number of Knoten: {len(schacht.knoten)}")
                for i, knoten in enumerate(schacht.knoten):
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

            junction_sgl = junction(
                name=str(schacht.objektbezeichnung),
                elev=elev,
                y0=y0,
                ysur=0,
                apond=0
            )
            junctions_list.append(junction_sgl)
        return junctions_list

    def to_junction_string(junctions_list: List) -> str:
        header = [
            "[JUNCTIONS]",
            ";;               Invert     Max.       Init.      Surcharge  Ponded ",
            ";;Name           Elev.      Depth      Depth      Depth      Area ",
            ";;-------------- ---------- ---------- ---------- ---------- ----------"
        ]
        junction_strings = []
        for junction in junctions_list:
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
class outfall:  #AUSLASS 
    name: Optional[str] = None
    elev: Optional[float] = 0
    type: Optional[str] = 'FREE'
    stage: Optional[float] = None
    tcurve: Optional[str] = None
    tseries: Optional[str] = None
    gated: Optional[str] = None
    routeto: Optional[str] = None

    def check_outfall(self, schacht_list, bauwerke_list) -> List['outfalls']:
        outfalls_list = []
        found_auslaufbauwerk = False
        
        for bauwerk in bauwerke_list:
            if isinstance(bauwerk, Auslaufbauwerk):
                print("Found Auslaufbauwerk")
                for knoten in bauwerk.knoten:
                    elev = knoten.punkte[1].z
                outfall_sgl = outfall(
                    name=bauwerk.objektbezeichnung,
                    elev=elev,
                    type='FREE'
                )
                outfalls_list.append(outfall_sgl)
                found_auslaufbauwerk = True

        if not found_auslaufbauwerk:
            print("No given Auslaufbauwerk")
            num_outfall = int(input("How many outfalls are needed:"))
            for i in range(num_outfall):
                outfall_sgl = self.search_set(schacht_list)
                outfalls_list.append(outfall_sgl)
        
        return outfalls_list

    def search_set(self, schacht_list):
        while True:
            outfall_name = input("Enter outfall name: ")
            for schacht in schacht_list:
                if schacht.objektbezeichnung == outfall_name:
                    print(f"Found Schacht {outfall_name}. Setting as outfall.")
                    for knoten in schacht.knoten:
                        elev = knoten.punkte[1].z
                        print(f"Elevation of {outfall_name}: {elev}")
                    outfall_sgl = outfalls(
                        name=str(outfall_name),
                        elev=elev,
                        type= 'FREE',
                        gated='NO',
                        tcurve='',
                        tseries='',
                        routeto=''
                    )
                    return outfall_sgl  
            print(f"No Schacht found with name {outfall_name}. Please enter a valid name.")

    def to_outfall_string(self, outfalls_list: List) -> str:
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
    def load_storage(self, bauwerke_list) -> List['storage']:
        storages_list = []
        for bauwerk in bauwerke_list:
            if isinstance(bauwerk, Becken):
                for knoten in bauwerk.knoten:
                    elev = knoten.punkte[1].z
                print("Found Storage")
                storage_sgl = storage(name=bauwerk.objektbezeichnung,
                                      elev= elev,
                                      ymax = bauwerk.max_hoehe,
                                      y0 = 0,
                                      acurve= 'TABULAR',
                                      curve = bauwerk.objektbezeichnung
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
class conduit: #abflusswirksame Verbindungen
    name: str
    node1: str
    node2: str
    length: float
    n: Optional[float] = 0 #roughness paramater
    z1: Optional[float] = 0
    z2: Optional[float] = 0
    Q0: Optional[float] = 0
    Qmax: Optional[float] = 0 
    def fict_cond(fict_conds: List) -> List['conduit']:
        for element in fict_conds:
            zn = None
            if element.knoten:
                knoten = schacht.knoten[0]
                print(f"Fict haltung: {element.objektbezeichnung}")
                print(f"Number of Knoten: {len(element.knoten)}")
                for i, knoten in enumerate(element.knoten):
                    print(f"  Knoten {i + 1}:")
                    if knoten.punkte:
                        punkt = knoten.punkte[0]
                        zn = float(punkt.z)
                        print(f"    Elevation (elev): {zn}")
                    else:
                        print("    No Punkte in this Knoten")
            conduit_sgl = conduit(
                name = element.objektbezeichnung,
                node1 = element.objektbezeichnung + '_B',
                node2 = element.objektbezeichnung + '_A',
                length = 0.1,
                n = 0.01,
                z1 = zn + 0.1 ,
                z2 = zn, 
                Q0 = 0,
                Qmax = 0   
            )
            fict_conds.append(conduit_sgl)
        return fict_conds
    def from_haltung(haltung_list : List) -> List['conduit']:
        conduits_list = []
        for haltung in haltung_list:
            conduits_sgl = conduit(
                name = haltung.objektbezeichung,
                node1= haltung.zulauf,
                node2= haltung.ablauf, 
                length= haltung.laenge,
                n= 0.01, # concrete 
                z1 = haltung.zulauf_sh,
                z2 = haltung.anlauf_sh,
                Q0 = 0,
                Qmax = 0            
            )
            conduits_list.append(conduits_sgl)
        return conduits_list
    def to_conduits_str(conduits_list  : List) -> str:
        header = [
        "[CONDUITS]",
        ";;               Inlet            Outlet                      Manning    Inlet      Outlet     Init.      Max.",      
        ";;Name           Node             Node             Length     N          Offset     Offset     Flow       Flow",
        ";;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------"
        ]
        conduits_strings = []
        for conduit in conduits_list:
            data = f"{conduit.name:<15}{conduit.node1:<15}{conduit.node2:<15}{conduit.length:<10}{conduit.n:<8}"\
                   f"{conduit.z1:<10}{conduit.z2:<10}{conduit.Q0:<8}{conduit.Qmax:<8}"
            conduits_strings.append(data)
        return  "\n".join(header + conduits_strings)



@dataclass
class pump:
    name: str
    node1: str
    node2: str
    pcurve: str
    status: str
    startup: Optional[float] = 0
    shutoff: Optional[float] = 0
    
    def get_pump(bauwerk_list : List)-> List['Pumpe']:
        '''returns isybau pumpen from bauwerke '''
        pumps_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Pumpe):
                pumps_list.append(bauwerk)
        return pumpe_list
    def to_junctions(pumps_list :List, junctions_list: List):
        for pump in pumps_list:
            fict_junc = junction.fict_junc(pumps_list)
            junctions_list.append(fict_junc)
        return junction_list
    def to_conduit(pumps_list: List, conduits_list: List):
        for pump in pumps_list:
            fict_cont = conduitS.fict_cond(pumps_list)
            conduits_list.append(fict_cont)
        return conduits_list
    def from_pumpe(pumpe_list: List)-> List['pump']:
        pumps_list = []
        for pumpe in pumpe_list:
            
            pump_sgl = pump(
                name = pumpe.objektbezeichnung,
                node1 = pumpe.objektbezeichnung + '_B',
                node2 = pumpe.objektbezeichnung + '_A',
                pcurve= 'coming',  #-------------------------------------------->
                status = 'ON',
                startup = 0,
                shutoff = 0
            )
            pumps_list.append(pump_sgl)
        return pumps_list
    def to_pumps_string(pumps_list: List) -> str:
        header = [
            "[PUMPS]",
            ";;               Inlet            Outlet                                 Start      Shut",
            ";;Name           Node             Node             Pcurve     Status     up         off",
            ";;-------------- ---------------- ---------------- ---------- ---------- ---------- ----------"
        ]
        pumps_string = []
        for pump in pumps_list:
            # Adjusting field lengths for better alignment
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
    cd: Optional[float] = 0
    flap:  str='NO'
    orate: Optional[float] = 0
    def get_orifices(bauwerk_list: List)-> List['Schieber']:
        schieber_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Schieber):
                schieber_list.append(bauwerk)
        return schieber_list
    def to_junctions(orifices_list :List, junctions_list: List):
        for orifice in orifices_list:
            fict_junc = junction.fict_junc(pumps_list)
            junctions_list.append(fict_junc)
        return junction_list
    def to_conduit(orifices_list: List, conduits_list: List):
        for orifice in orifices_list:
            fict_cont = conduitS.fict_cond(pumps_list)
            conduits_list.append(fict_cont)
        return conduits_list
    def from_orifices(schieber_list: List)->List['orifice']:
        pass
        

@dataclass
class weirs:   # WEHR
    name: str
    node1: str
    node2: str
    type: str #TRANSVERSE, SIDEFLOW, V-NOTCH, TRAPEZOIDAL or ROADWAY
    crestht: Optional[float] = 0
    cd: float = 3322
    gated: str = 'NO' #YES if flap gate present to prevent reverse flow, NO if not (default is NO)
    ec: float= 0
    cd2: float = 3322
    sur: str = 'YES' 
    width: Optional[float] = 0
    surface: Optional[str] = None
    def get_weirs(bauwerk_list: List)-> List['Wehr']:
        weirs_list = []
        for bauwerk in bauwerk_list:
            if isinstance (bauwerk, Wehr):
                weirs_list.append(bauwerk)
        return weirs_list

@dataclass
class outlets: #DROSSEL
    name: str
    node1: str
    node2: str
    offset: Optional[float] = None
    Qcurve: Optional[str] = None
    c1: Optional[float] = 0
    c2: Optional[float] = 0
    gated: str= 'NO'
    def get_outlets(bauwerk_list: List)->List['Drossel']:
        outlets_list = []
        for bauwerk in bauwerk_list:
            if isinstance(bauwerk, Drossel):
                outlets_list.append(bauwerk)
        return outlets_list


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
    def from_haltung(haltung_list : List)-> List['xsection']:
        xsection_list = []
        for haltung in haltung_list:
            if haltung.profilart == 0:
                shape = 'CIRCULAR'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe / 1000)
                else:
                    geom1 = float(haltung.profilbreite / 1000)

            elif haltung.profilart == 1:
                shape = 'EGG'
            elif haltung.profilart == 2:
                shape = 'CATENARY'
            elif haltung.profilart == 3:
                shape = 'RECT_CLOSED'
            elif haltung.profilart == 5:
                shape = 'RECT_OPEN'
                if haltung.profilhoehe is not None:
                    geom1  = float(haltung.profilhoehe/1000)
                else: 
                    geom1 = 1
                if haltung.profilbreite is not None:
                    geom2 = float(haltung.profilbreite/1000)
                else:
                    geom2 = 1 
            elif haltung.profilart == 8:
                shape = 'TRAPEZOIDAL'
                if haltung.profilhoehe is not None:
                    geom1 = float(haltung.profilhoehe/1000)
                if haltung.profilbreite is not None:
                    geom2 = float(haltung.proiflbreite/1000)
                geom3 = 1
                geom4 = 1
            xsection_sgl = xsection(
                link = haltung.objektbezeichung,
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

    
    

@dataclass
class losses:
    conduit: str
    kentry: Optional[float]
    kexit: Optional[float]
    kavg: Optional[float]
    flap: str = 'YES'
    seepage: float= 0
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
    type: str
    x_values: List[float]
    y_values: List[float]
    
@dataclass
class timeseries:
    name: str
    date: str
    hour: str
    time: float
    value: str

@dataclass
class report:
    pass

@dataclass
class tags:
    pass

@dataclass
class cooordinates:
    pass

@dataclass 
class vertices:
    pass

@dataclass
class polygons:
    pass

@dataclass
class symbols: 
    pass 

@dataclass
class labels:
    pass 

@dataclass
class backdrop:
    pass 


def create_inp(metadata, flaechen_list, schacht_list, bauwerke_list):
    fict_cond = []
    
    subcatchment_list = subcatchments.from_flache(flaechen_list)
    subarea_list = subareas.from_subcatchment(subcatchment_list)
    infiltration_list = infiltration_H.from_subcatchment(subcatchment_list)
    junction_list = junctions.from_schacht(schacht_list)
    pumps_list = pumps.get_pump(bauwerk_list)
    junction_list = pumps.to_junctions(pumps_list, junction_list)
    #orc etc
    outfall = outfalls()
    outfall_list = outfall.check_outfall(schacht_list, bauwerke_list)


    with open("model.inp", "w") as f:
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
        f.write(junctions.to_junction_string(junction_list))
        f.write("\n")
        f.write("\n")
        f.write(outfall.to_outfall_string(outfall_list))
