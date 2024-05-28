from dataclasses import dataclass
from typing import Optional, List

@dataclass
class vertex:
    x_value: Optional[float]
    y_value: Optional[float]
    z_value: Optional[float]

@dataclass
class triangle:
    vertices: List[vertex]
    typ: Optional[str] = 'Grass'
    perme: Optional[float]= 0
    focus: vertex


