from App.EcuM.EcuM import EcuM_Init, EcuM_SetIncarVoltage
from BSW.Dem.Dem import Dem_Init, Dem_SetDTC, Dem_HasAnyDTC
from BSW.Dcm.Dcm import Dcm_Init, Dcm_ProcessRequest
from BSW.PduR.PduR_Types import PduInfoType_FromBytes

def test_Dcm_ClearDTC_Voltage_OK_Clears():
    EcuM_Init()
    Dem_Init()
    Dcm_Init()

    Dem_SetDTC("B122021")
    EcuM_SetIncarVoltage(3.3)

    resp = Dcm_ProcessRequest(PduInfoType_FromBytes(bytes([0x14, 0xFF, 0xFF, 0xFF])))
    assert bytes(resp.SduDataPtr) == bytes([0x54, 0xFF, 0xFF, 0xFF])
    assert Dem_HasAnyDTC() is False

def test_Dcm_ClearDTC_Voltage_High_Blocked():
    EcuM_Init()
    Dem_Init()
    Dcm_Init()

    Dem_SetDTC("B122021")
    EcuM_SetIncarVoltage(12.0)

    resp = Dcm_ProcessRequest(PduInfoType_FromBytes(bytes([0x14, 0xFF, 0xFF, 0xFF])))
    assert bytes(resp.SduDataPtr)[0:2] == bytes([0x7F, 0x14])
    assert Dem_HasAnyDTC() is True
