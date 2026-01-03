from Std.Std_Types import Std_ReturnType, E_OK
from .PduR_Types import PduInfoType
from .PduR_Cfg import PDUR_RX_PDU_ID_DIAG_REQ

# Hook to upper layer (Dcm)
_pduR_Dcm_RxIndication = None

def PduR_Init() -> Std_ReturnType:
    return E_OK

def PduR_SetDcmRxIndicationCallback(cb) -> Std_ReturnType:
    global _pduR_Dcm_RxIndication
    _pduR_Dcm_RxIndication = cb
    return E_OK

def PduR_RxIndication(rx_pdu_id: int, pdu_info: PduInfoType) -> PduInfoType:
    # Route diagnostic request to Dcm
    if rx_pdu_id == PDUR_RX_PDU_ID_DIAG_REQ and _pduR_Dcm_RxIndication is not None:
        return _pduR_Dcm_RxIndication(pdu_info)
    # No route -> empty response
    return PduInfoType(SduDataPtr=b"", SduLength=0)
