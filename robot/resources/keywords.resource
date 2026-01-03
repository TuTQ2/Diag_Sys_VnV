*** Settings ***
Library    Process
Library    Collections
Library    String

*** Keywords ***
Run ECU CLI And Expect
    [Arguments]    ${req_hex}    ${expected_hex}    ${voltage}=12.0    @{seed_dtcs}

    ${src_path}=    Set Variable    ${CURDIR}${/}..${/}..${/}src

    ${args}=    Create List     -m    App.Cli.EcuSim_Cli    ${req_hex}    --voltage    ${voltage}
    FOR    ${d}    IN    @{seed_dtcs}
        Append To List    ${args}    --seed-dtc
        Append To List    ${args}    ${d}
    END

    ${res}=    Run Process    python    @{args}
    ...    stdout=PIPE    stderr=PIPE    shell=${False}
    ...    env:PYTHONPATH=${src_path}

    Should Be Equal As Integers    ${res.rc}    0
    ...    msg=CLI failed (rc=${res.rc})\nSTDERR:\n${res.stderr}\nSTDOUT:\n${res.stdout}

    ${out}=    Strip String    ${res.stdout}
    ${out}=    Strip String    ${out}
    Should Be Equal    ${out}    ${expected_hex}
    ...    msg=Output mismatch\nSTDERR:\n${res.stderr}\nSTDOUT:\n${res.stdout}
