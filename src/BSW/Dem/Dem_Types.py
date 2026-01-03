from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Dem_DtcEntryType:
    status: str = "ACTIVE"

@dataclass
class Dem_DtcStoreType:
    # DTC as string like "B122021"
    dem_DtcTable: Dict[str, Dem_DtcEntryType] = field(default_factory=dict)
