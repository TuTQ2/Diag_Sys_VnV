from dataclasses import dataclass

@dataclass
class Dcm_DidDbType:
    dcm_DidTable: dict  # DID(int) -> bytes
