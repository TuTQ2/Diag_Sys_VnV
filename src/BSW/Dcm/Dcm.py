from Std.Std_Types import Std_ReturnType, E_OK
from App.EcuM.EcuM import (
    EcuM_GetIncarVoltage,
    EcuM_GetDcmSession,
    EcuM_SetDcmSession,
    ECUM_DCM_SESSION_DEFAULT,
    ECUM_DCM_SESSION_EXTENDED,
)
from BSW.Dem.Dem import Dem_ClearAllDTCs
from BSW.PduR.PduR_Types import PduInfoType, PduInfoType_FromBytes
from .Dcm_Cfg import (
    DCM_DID_TABLE_DEFAULT,
    DCM_NRC_INCORRECT_MESSAGE_LENGTH,
    DCM_NRC_CONDITIONS_NOT_CORRECT,
    DCM_NRC_REQUEST_OUT_OF_RANGE,
)
from .Dcm_Types import Dcm_DidDbType

_dcm_DidDb = Dcm_DidDbType(dcm_DidTable=dict(DCM_DID_TABLE_DEFAULT))

def Dcm_Init() -> Std_ReturnType:
    global _dcm_DidDb
    _dcm_DidDb = Dcm_DidDbType(dcm_DidTable=dict(DCM_DID_TABLE_DEFAULT))
    return E_OK

def Dcm_MainFunction() -> None:
    # Periodic task placeholder
    return

def Dcm_ProcessRequest(pdu_info: PduInfoType) -> PduInfoType:
    req = bytes(pdu_info.SduDataPtr)
    if len(req) < 1:
        return PduInfoType_FromBytes(bytes([0x7F, 0x00, DCM_NRC_INCORRECT_MESSAGE_LENGTH]))

    sid = req[0]

    if sid == 0x10:
        return _Dcm_Service_0x10_SessionControl(req)
    if sid == 0x11:
        return _Dcm_Service_0x11_EcuReset(req)
    if sid == 0x22:
        return _Dcm_Service_0x22_ReadDID(req)
    if sid == 0x2E:
        return _Dcm_Service_0x2E_WriteDID(req)
    if sid == 0x14:
        return _Dcm_Service_0x14_ClearDTC(req)

    return PduInfoType_FromBytes(bytes([0x7F, sid, DCM_NRC_REQUEST_OUT_OF_RANGE]))

def _Dcm_Service_0x10_SessionControl(req: bytes) -> PduInfoType:
    if len(req) != 2:
        return PduInfoType_FromBytes(bytes([0x7F, 0x10, DCM_NRC_INCORRECT_MESSAGE_LENGTH]))

    requested_session = req[1]
    if requested_session not in (ECUM_DCM_SESSION_DEFAULT, ECUM_DCM_SESSION_EXTENDED):
        return PduInfoType_FromBytes(bytes([0x7F, 0x10, DCM_NRC_REQUEST_OUT_OF_RANGE]))

    EcuM_SetDcmSession(requested_session)
    return PduInfoType_FromBytes(bytes([0x50, requested_session]))

def _Dcm_Service_0x11_EcuReset(req: bytes) -> PduInfoType:
    if len(req) != 2:
        return PduInfoType_FromBytes(bytes([0x7F, 0x11, DCM_NRC_INCORRECT_MESSAGE_LENGTH]))

    reset_type = req[1]
    # Reset behavior: back to default session
    EcuM_SetDcmSession(ECUM_DCM_SESSION_DEFAULT)
    return PduInfoType_FromBytes(bytes([0x51, reset_type]))

def _Dcm_Service_0x22_ReadDID(req: bytes) -> PduInfoType:
    if len(req) != 3:
        return PduInfoType_FromBytes(bytes([0x7F, 0x22, DCM_NRC_INCORRECT_MESSAGE_LENGTH]))

    did = (req[1] << 8) | req[2]
    if did not in _dcm_DidDb.dcm_DidTable:
        return PduInfoType_FromBytes(bytes([0x7F, 0x22, DCM_NRC_REQUEST_OUT_OF_RANGE]))

    payload = _dcm_DidDb.dcm_DidTable[did]
    resp = bytes([0x62, req[1], req[2]]) + bytes(payload)
    return PduInfoType_FromBytes(resp)

def _Dcm_Service_0x2E_WriteDID(req: bytes) -> PduInfoType:
    if len(req) < 4:
        return PduInfoType_FromBytes(bytes([0x7F, 0x2E, DCM_NRC_INCORRECT_MESSAGE_LENGTH]))

    did = (req[1] << 8) | req[2]
    payload = req[3:]

    if did not in _dcm_DidDb.dcm_DidTable:
        return PduInfoType_FromBytes(bytes([0x7F, 0x2E, DCM_NRC_REQUEST_OUT_OF_RANGE]))

    _dcm_DidDb.dcm_DidTable[did] = bytes(payload)
    return PduInfoType_FromBytes(bytes([0x6E, req[1], req[2]]))

def _Dcm_Service_0x14_ClearDTC(req: bytes) -> PduInfoType:
    # Requirement: 0x14 only clears DTCs if Incar voltage is within 0–5V; else keep DTC
    if len(req) != 4:
        return PduInfoType_FromBytes(bytes([0x7F, 0x14, DCM_NRC_INCORRECT_MESSAGE_LENGTH]))

    voltage_v = float(EcuM_GetIncarVoltage())
    if not (0.0 <= voltage_v <= 5.0):
        return PduInfoType_FromBytes(bytes([0x7F, 0x14, DCM_NRC_CONDITIONS_NOT_CORRECT]))

    Dem_ClearAllDTCs()
    return PduInfoType_FromBytes(bytes([0x54, req[1], req[2], req[3]]))
