from dataclasses import dataclass

@dataclass
class PduInfoType:
    SduDataPtr: bytes
    SduLength: int

def PduInfoType_FromBytes(data: bytes) -> PduInfoType:
    b = bytes(data)
    return PduInfoType(SduDataPtr=b, SduLength=len(b))
