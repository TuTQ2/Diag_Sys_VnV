from App.EcuM.EcuM import EcuM_Init, EcuM_GetDcmSession, ECUM_DCM_SESSION_EXTENDED
from BSW.Dcm.Dcm import Dcm_Init, Dcm_ProcessRequest
from BSW.PduR.PduR_Types import PduInfoType_FromBytes

def test_Dcm_SessionControl_Extended_OK():
    EcuM_Init()
    Dcm_Init()

    resp = Dcm_ProcessRequest(PduInfoType_FromBytes(bytes([0x10, ECUM_DCM_SESSION_EXTENDED])))
    assert bytes(resp.SduDataPtr) == bytes([0x50, ECUM_DCM_SESSION_EXTENDED])
    assert EcuM_GetDcmSession() == ECUM_DCM_SESSION_EXTENDED
