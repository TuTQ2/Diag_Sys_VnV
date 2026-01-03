from Std.Std_Types import Std_ReturnType, E_OK
from BSW.PduR.PduR import PduR_RxIndication
from BSW.PduR.PduR_Types import PduInfoType_FromBytes
from BSW.PduR.PduR_Cfg import PDUR_RX_PDU_ID_DIAG_REQ

def SoAd_Init() -> Std_ReturnType:
    return E_OK

def SoAd_TpReceive(diag_req_bytes: bytes) -> bytes:
    # SoAd receives from "network", passes to PduR
    pdu_info = PduInfoType_FromBytes(diag_req_bytes)
    resp_pdu = PduR_RxIndication(PDUR_RX_PDU_ID_DIAG_REQ, pdu_info)
    return bytes(resp_pdu.SduDataPtr)
