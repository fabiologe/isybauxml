from xml_parser.parse_all import all_lists
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Union


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
    spack: Optional[str] = None # Name of the Snowpack if needed 

    def from_flache(flaechen_list: List) -> List['subcatchments']:
        subcatchment_list = []
        for flaeche in flaechen_list:
            subcatchment_sgl = subcatchments(
            name = flaeche.flaechenbezeichnung,
            raingage = "RainGage",
            outletID = str(flaeche.hydro_vertices[0]) if flaeche.hydro_vertices else "NO_HYDRO",
            imperv = flaeche.abflussbeiwert,
            area = flaeche.flaechengroesse,
            width = flaeche.width or 100, 
            slope = flaeche.neigungsklasse,
            clength= 0,
            spack= None ) 
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
            data = f"{subcatchment.name:<16} {subcatchment.raingage:<16} {subcatchment.outletID:<16} {subcatchment.area:<8.2f} {subcatchment.imperv:<8.2f} {subcatchment.width:<8.2f} {subcatchment.slope:<8.2f} {subcatchment.clength:<8.2f} {subcatchment.spack or '<none>':<8}"
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

    def from_subcatchment(flaechen_list: List, subcatchment_list: List) -> List['subareas']:
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
            ";;-------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------", 
        ]
        subarea_strings = []
        for subarea in subarea_list:
            data = f"{subarea.subcat:<16} {subarea.nimp:<16} {subarea.nperv:<16} {subarea.simp:<8.2f} {subarea.sperv:<8.2f} {subarea.zero:<8.2f} {subarea.route_to:<8.2f} {subarea.routed:<8.2f}"
            subarea_strings.append(data)
        return '\n'.join(header + subarea_strings)

@dataclass
class infiltration_H: #For Horton/ Modified Horton
    maxrate: Optional[float] = 0 # maximum infiltration rate on Horton curve (in/hr or mm/hr)
    minrate: Optional[float] = 0 # minimum infiltration rate on Horton curve (in/hr or mm/hr)
    decay: Optional[float] = 0 # decay rate constant of Horton curve (1/hr).
    drytime: Optional[float] = 0 # time it takes for fully saturated soil to dry  (days).
    maxinf: Optional[float] = 0 #maximum infiltration volume possible  (mm)

@dataclass
class infiltration_G: # Green- Ampt Infiltration
    psi: Optional[float] = 0 #soil capillary suction (mm)
    ksat: Optional[float] = None 
    imd: Optional[float] = None

@dataclass
class infiltration_C: # Curve-Number Infiltration
    curveno: Optional[float]
    ksat: Optional[float]
    drytime: Optional[float]

@dataclass
class lid_controls:
    name: str 
    type: Optional[str] # Surface , Soil, Pavement, Storage, Drain, Drainment


@dataclass
class lid_usage:
    subcat: str 
    lid: str
    number: int
    area: Optional[float]
    width: Optional[float]
    initsat: Optional[float]
    fromimp: Optional[float] = 0
    toperv: Optional[float] = 0
    drainTo: Optional[str] = None

'''MISSING CLASSES: AQUIFIER , GROUNDWATER , GWF , SNOWPACK ---> maybe when there is an project I gonna add them '''

@dataclass
class junctions:
    name: str
    elev: float
    ymax : Optional[float] = 0
    y0: Optional[float]  = 0
    ysur: Optional[float]  = 0
    apond: Optional[float]  = 0 

@dataclass
class divider:
    name: str
    elev: Optional[float] 
    divlink: Optional[str] 
    Qmin: Optional[float] 
    Dcurve: Optional[str]
    ht: Optional[float] 
    cd: Optional[float] 
    ymax: Optional[float]  = 0
    y0: Optional[float] = 0
    ysur: Optional[float] = 0
    apond: Optional[float] = 0


@dataclass
class outfalls:  #AUSLASS 
    name: str
    elev: Optional[float] 
    stage: Optional[float]
    tcurve: Optional[str]
    tseries: Optional[str]
    gated: Optional[bool] = False
    routeto: Optional[str]


@dataclass
class storage:
    name: str
    elev: Optional[float]
    ymax: Optional[float]
    y0: Optional[float]
    acurve: Optional[str] = 'TABULAR'
    apond: Optional[float] = 0
    fevap: Optional[float] = 0
    psi : Optional[float]
    ksat: Optional[float]
    imd : Optional[float]
    
@dataclass
class conduits: #abflusswirksame Verbindungen
    name: str
    node1: str
    node2: str
    length: float
    n: Optional[float] #roughness paramater
    z1: float
    z2: float
    Q0: Optional[float] = 0
    Qmax: float
@dataclass
class pumps:
    name: str
    node1: str
    node2: str
    pcurve: str
    status: bool = True
    startup: Optional[float] = 0
    shutoff: Optional[float] = 0
@dataclass
class orifices: #SCHIEBER
    name: str
    node1: str
    node2: str
    type : str='SIDE'  # can also be BOTTOM
    offset: Optional[float]
    cd: Optional[float] 
    flap:  str='NO'
    orate: Optional[float] = 0
@dataclass
class weirs:   # WEHR
    name: str
    node1: str
    node2: str
    type: str #TRANSVERSE, SIDEFLOW, V-NOTCH, TRAPEZOIDAL or ROADWAY
    crestht: Optional[float]
    cd: float = 3322
    gated: str = 'NO' #YES if flap gate present to prevent reverse flow, NO if not (default is NO)
    ec: float= 0
    cd2: float = 3322
    sur: str = 'YES' 
    width: float
    surface: Optional[str]
@dataclass
class outlets: #DROSSEL
    name: str
    node1: str
    node2: str
    offset: Optional[float]
    Qcurve: str
    c1: Optional[float]
    c2: Optional[float]
    gated: str= 'NO'


@dataclass
class xsection:
    link: str
    shape: str
    geom1: float
    geom2: Optional[float]
    geom3: Optional[float]
    geom4: Optional[float]
    barrels: int = 1 
    culvert: Optional[int] = None
    curve: Optional[str]
    tsec: Optional[str]
    

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
    nleft: float = 0
    nright: float = 0
    nchanl: float = 0
    name: str 
    nsta: Optional[float]
    xleft: Optional[float]
    xright: Optional[float]
    lfactor: float = 0
    wfactor: float = 0
    Eoffset: float = 0
    elev: Optional[float]
    station: Optional[float]
'''NO SUPPORT FOR CONTROLS'''
@dataclass
class pollutants:
    name: str
    units: str = 'MG/L'
    crain: Optional[float]
    cgw: Optional[float]
    cii: Optional[float]
    kdecay: Optional[float]
    sflag: str = 'NO'

@dataclass
class landuses:
    name: str
    sweepintervall: Optional[int]
    availability: Optional[float]
    lastsweep: Optional[int]

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
    base: float = 0.0
    pat: Optional[str]

@dataclass
class dwf: # Trockenwetterabfluss
    node: str
    type: str = 'FLOW'
    base: float 

@dataclass
class hydrographs:
    name: str
    raingage: str
    month: str = 'ALL'
    term: str= 'MEDIUM'  #SHORT ; MEDIUM ; LONG
    R: float
    T: float
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



def create_inp(metadata, flaechen_list):

    subcatchment_list = subcatchments.from_flache(flaechen_list)
    subarea_list = subareas.from_subcatchment(subcatchment_list)

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
        f.write(subcatchments.to_subcatchment_string(subcatchment_list))
        f.write("\n")
        f.write("\n")
        f.write(subareas.to_subarea_string(subarea_list))
        f.write("\n")
        f.write("\n")
        