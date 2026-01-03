from dataclasses import dataclass

@dataclass
class EcuM_StateType:
    ecuM_IncarVoltage_V: float = 12.0
    ecuM_CurrentSession: int = 0x01  # default session
