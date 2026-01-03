from dataclasses import dataclass

Std_ReturnType = int

E_OK: Std_ReturnType = 0
E_NOT_OK: Std_ReturnType = 1

@dataclass(frozen=True)
class Std_VersionInfoType:
    vendor_id: int
    module_id: int
    sw_major_version: int
    sw_minor_version: int
    sw_patch_version: int
