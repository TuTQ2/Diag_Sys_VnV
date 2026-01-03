from Std.Std_Types import Std_ReturnType, E_OK
from .EcuM_Types import EcuM_StateType

# Sessions (AUTOSAR-like constants)
ECUM_DCM_SESSION_DEFAULT = 0x01
ECUM_DCM_SESSION_EXTENDED = 0x03

_ecuM_State = EcuM_StateType()

def EcuM_Init() -> Std_ReturnType:
    global _ecuM_State
    _ecuM_State = EcuM_StateType(
        ecuM_IncarVoltage_V=12.0,
        ecuM_CurrentSession=ECUM_DCM_SESSION_DEFAULT,
    )
    return E_OK

def EcuM_SetIncarVoltage(voltage_v: float) -> Std_ReturnType:
    _ecuM_State.ecuM_IncarVoltage_V = float(voltage_v)
    return E_OK

def EcuM_GetIncarVoltage() -> float:
    return _ecuM_State.ecuM_IncarVoltage_V

def EcuM_SetDcmSession(session: int) -> Std_ReturnType:
    _ecuM_State.ecuM_CurrentSession = int(session)
    return E_OK

def EcuM_GetDcmSession() -> int:
    return _ecuM_State.ecuM_CurrentSession
