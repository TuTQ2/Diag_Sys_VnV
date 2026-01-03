from App.EcuM.EcuM import EcuM_Init
from BSW.Dcm.Dcm import Dcm_Init, Dcm_ProcessRequest
from BSW.PduR.PduR_Types import PduInfoType_FromBytes

def test_Dcm_ReadDID_VIN_OK():
    EcuM_Init()
    Dcm_Init()

    resp = Dcm_ProcessRequest(PduInfoType_FromBytes(bytes([0x22, 0xF1, 0x90])))
    out = bytes(resp.SduDataPtr)
    assert out[0:3] == bytes([0x62, 0xF1, 0x90])
    assert b"VIN:" in out

def test_Dcm_WriteDID_SW_OK():
    EcuM_Init()
    Dcm_Init()

    write_req = bytes([0x2E, 0xF1, 0x87]) + b"SW:2.0.0"
    resp = Dcm_ProcessRequest(PduInfoType_FromBytes(write_req))
    assert bytes(resp.SduDataPtr) == bytes([0x6E, 0xF1, 0x87])

    read_resp = Dcm_ProcessRequest(PduInfoType_FromBytes(bytes([0x22, 0xF1, 0x87])))
    assert bytes(read_resp.SduDataPtr).endswith(b"SW:2.0.0")
