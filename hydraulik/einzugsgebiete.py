from dataclasses import dataclass
from typing import Optional

einzugsgebiete_list = []
@dataclass
class einzugsgebiete:
    gebietskennung: Optional[str] = None
    gebietsname: Optional[str] = None
    kommentar: Optional[str] = None
    einwohner: Optional[float] = None
    einwohnerdichte: Optional[float] = None # E/hages
    trockenwetterkennung: Optional[str] = None


