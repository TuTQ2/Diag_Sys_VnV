import argparse
import sys

from Std.Std_Types import E_OK
from App.EcuM.EcuM import EcuM_Init, EcuM_SetIncarVoltage
from BSW.Dem.Dem import Dem_Init, Dem_SetDTC
from BSW.Dcm.Dcm import Dcm_Init, Dcm_ProcessRequest
from BSW.PduR.PduR import PduR_Init, PduR_SetDcmRxIndicationCallback
from MCAL.SoAd.SoAd import SoAd_Init, SoAd_TpReceive


def EcuSimCli_ParseHexBytes(hex_str: str) -> bytes:
    s = hex_str.strip().replace("-", " ").replace(",", " ")
    if " " in s:
        parts = [p for p in s.split(" ") if p]
        return bytes(int(p, 16) for p in parts)

    s = s.replace(" ", "")
    if len(s) % 2 != 0:
        raise ValueError("Hex string length must be even when no spaces.")
    return bytes(int(s[i:i+2], 16) for i in range(0, len(s), 2))


def EcuSimCli_FormatHex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)


def EcuSimCli_WireStack() -> int:
    # Init order (simplified)
    EcuM_Init()
    Dem_Init()
    Dcm_Init()
    PduR_Init()
    SoAd_Init()

    # Wire: PduR routes to Dcm
    PduR_SetDcmRxIndicationCallback(Dcm_ProcessRequest)
    return E_OK


def EcuSimCli_Main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="EcuSim",
        description="AUTOSAR-like ECU Diagnostic Simulator (CLI)",
    )
    parser.add_argument("request", help='UDS request as hex, e.g. "10 03" or "1003"')
    parser.add_argument("--voltage", type=float, default=12.0, help="Incar voltage (V)")
    parser.add_argument("--seed-dtc", action="append", default=[], help='Seed DTC string e.g. "B122021" (repeatable)')
    parser.add_argument("--print-state", action="store_true", help="Print debug state (not used in CI)")

    args = parser.parse_args(argv)

    EcuSimCli_WireStack()
    EcuM_SetIncarVoltage(args.voltage)

    for dtc_code_str in args.seed_dtc:
        Dem_SetDTC(dtc_code_str)

    try:
        diag_req = EcuSimCli_ParseHexBytes(args.request)
    except Exception as e:
        sys.stderr.write(f"ERR: invalid request hex: {e}\n")
        return 2

    diag_resp = SoAd_TpReceive(diag_req)
    sys.stdout.write(EcuSimCli_FormatHex(diag_resp) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(EcuSimCli_Main())
