import pytest

from App.EcuM.EcuM import EcuM_Init
from BSW.Dem.Dem import Dem_Init
from BSW.Dcm.Dcm import Dcm_Init, Dcm_ProcessRequest
from BSW.PduR.PduR_Types import PduInfoType_FromBytes


def _req(data: bytes) -> bytes:
    resp = Dcm_ProcessRequest(PduInfoType_FromBytes(data))
    return bytes(resp.SduDataPtr)

@pytest.fixture(autouse=True)
def _init_stack():
    EcuM_Init()
    Dem_Init()
    Dcm_Init()


def test_UnknownSid_ShouldReturn_RequestOutOfRange():
    # SID 0x99 không support -> 7F 99 31
    out = _req(bytes([0x99, 0x00]))
    assert out == bytes([0x7F, 0x99, 0x31])


def test_0x10_SessionControl_WrongLength_ShouldReturn_13():
    # thiếu sub-function
    out = _req(bytes([0x10]))
    assert out == bytes([0x7F, 0x10, 0x13])


def test_0x10_SessionControl_UnsupportedSession_ShouldReturn_31():
    out = _req(bytes([0x10, 0x99]))
    assert out == bytes([0x7F, 0x10, 0x31])


def test_0x22_ReadDID_WrongLength_ShouldReturn_13():
    out = _req(bytes([0x22, 0xF1]))  # thiếu 1 byte DID
    assert out == bytes([0x7F, 0x22, 0x13])


def test_0x22_ReadDID_UnsupportedDID_ShouldReturn_31():
    out = _req(bytes([0x22, 0x12, 0x34]))
    assert out == bytes([0x7F, 0x22, 0x31])


def test_0x2E_WriteDID_WrongLength_ShouldReturn_13():
    out = _req(bytes([0x2E, 0xF1, 0x87]))  # thiếu payload
    assert out == bytes([0x7F, 0x2E, 0x13])


def test_0x2E_WriteDID_UnsupportedDID_ShouldReturn_31():
    out = _req(bytes([0x2E, 0x12, 0x34, 0x01]))
    assert out == bytes([0x7F, 0x2E, 0x31])


def test_0x11_EcuReset_WrongLength_ShouldReturn_13():
    out = _req(bytes([0x11]))  # thiếu resetType
    assert out == bytes([0x7F, 0x11, 0x13])


def test_0x11_EcuReset_PositiveResponse():
    out = _req(bytes([0x11, 0x01]))
    assert out == bytes([0x51, 0x01])


def test_0x14_ClearDTC_WrongLength_ShouldReturn_13():
    out = _req(bytes([0x14, 0xFF]))  # thiếu 2 bytes mask
    assert out == bytes([0x7F, 0x14, 0x13])
