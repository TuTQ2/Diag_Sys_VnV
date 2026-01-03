*** Settings ***
Resource   resources/keywords.resource

*** Test Cases ***
Session Control Should Switch To Extended
    Run ECU CLI And Expect    10 03    50 03    12.0

Read DID VIN Should Return Exact Payload
    # VIN:TESTVIN000000001 in ASCII:
    # 56 49 4E 3A 54 45 53 54 56 49 4E 30 30 30 30 30 30 30 30 31
    Run ECU CLI And Expect    22 F1 90    62 F1 90 56 49 4E 3A 54 45 53 54 56 49 4E 30 30 30 30 30 30 30 30 31    12.0

Clear DTC Should Work When Voltage In 0..5V
    Run ECU CLI And Expect    14 FF FF FF    54 FF FF FF    3.3    B122020

Clear DTC Should Be Blocked When Voltage High
    Run ECU CLI And Expect    14 FF FF FF    7F 14 22    12.0    B122021
