*** Settings ***
Resource   resources/keywords.resource

*** Test Cases ***
Unknown SID Should Return NRC 31
    Run ECU CLI And Expect    99 00    7F 99 31    12.0

Session Control Wrong Length Should Return NRC 13
    Run ECU CLI And Expect    10    7F 10 13    12.0

Session Control Unsupported Session Should Return NRC 31
    Run ECU CLI And Expect    10 99    7F 10 31    12.0

Read DID Wrong Length Should Return NRC 13
    Run ECU CLI And Expect    22 F1    7F 22 13    12.0

Read DID Unsupported DID Should Return NRC 31
    Run ECU CLI And Expect    22 12 34    7F 22 31    12.0

Write DID Wrong Length Should Return NRC 13
    Run ECU CLI And Expect    2E F1 87    7F 2E 13    12.0

Write DID Unsupported DID Should Return NRC 31
    Run ECU CLI And Expect    2E 12 34 01    7F 2E 31    12.0

ECU Reset Wrong Length Should Return NRC 13
    Run ECU CLI And Expect    11    7F 11 13    12.0

ECU Reset Positive Response
    Run ECU CLI And Expect    11 01    51 01    12.0

Clear DTC Wrong Length Should Return NRC 13
    Run ECU CLI And Expect    14 FF    7F 14 13    12.0
