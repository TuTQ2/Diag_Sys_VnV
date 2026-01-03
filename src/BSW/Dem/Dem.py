from Std.Std_Types import Std_ReturnType, E_OK, E_NOT_OK
from .Dem_Types import Dem_DtcStoreType, Dem_DtcEntryType
from .Dem_Cfg import DEM_MAX_DTC_COUNT

_dem_Store = Dem_DtcStoreType()

def Dem_Init() -> Std_ReturnType:
    global _dem_Store
    _dem_Store = Dem_DtcStoreType()
    return E_OK

def Dem_SetDTC(dtc_code_str: str, status: str = "ACTIVE") -> Std_ReturnType:
    if len(_dem_Store.dem_DtcTable) >= DEM_MAX_DTC_COUNT and dtc_code_str not in _dem_Store.dem_DtcTable:
        return E_NOT_OK
    _dem_Store.dem_DtcTable[str(dtc_code_str)] = Dem_DtcEntryType(status=str(status))
    return E_OK

def Dem_ClearAllDTCs() -> Std_ReturnType:
    _dem_Store.dem_DtcTable.clear()
    return E_OK

def Dem_HasAnyDTC() -> bool:
    return len(_dem_Store.dem_DtcTable) > 0

def Dem_GetDtcCount() -> int:
    return len(_dem_Store.dem_DtcTable)
