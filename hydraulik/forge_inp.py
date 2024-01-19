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

    def get_flaeche(flaechen_list):
        for flaeche in flaechen_list:
            subcatchments_sgl = subcatchments(
                    name = flaeche.objektbezeichnung,
                    raingage = "RainGage",
                    outletID= str(flaeche.hydro_vertices[0]),
                    imperv = float(flaeche.abflussbeiwert),
                    width= 100, # NOT READY
                    slope = float(flaeche.neigungsklasse),
                    clength= 0,
                    spack= None
            )
    
    def to_subcatchment_string(self):
        header = [
            "[SUBCATCHMENTS]",
            ";;                                                 Total    Pcnt.             Pcnt.    Curb     Snow "  , 
            ";;Name           Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack " ,
            ";;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- --------"
        ]

@dataclass
class subareas:
    subcat: str
    nimp: Optional[float] = 0.5  # Manning impervious sub-area
    nperv: Optional[float] = 0.5 # Manning pervious sub-area 
    simp: Optional[float] = 0 # depression storage fo impervious sub-area(mm)
    sperv: Optional[float] = 0 # depression storage for pervious sub-area (mm)
    zero: Optional[float] = 0 # % of impervious area with no depression storage 
    route_to: Union[str("IMPERVIOUS"),str("PERVIOUS", str("OUTLETE"))] = str("OUTLET") 
    routed: Optional[float] = 100 # % of runoff routed from one type of area to another

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

@dataclass
class junctions:
    pass

@dataclass
class outfalls:
    pass

@dataclass
class conduits:
    pass

@dataclass
class xsection:
    pass

@dataclass
class losses:
    pass

@dataclass
class timeseries:
    pass

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


def create_inp(metadata):
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
