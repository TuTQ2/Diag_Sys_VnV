# ECU Diagnostic Simulator (AUTOSAR-like)

Small, hardware-free ECU diagnostic simulator to practice:
- AUTOSAR-like layering: **SoAd → PduR → Dcm → (EcuM/Dem)**
- **pytest** unit tests
- **Robot Framework** system tests (black-box via CLI)
- CI/CD via **Jenkins Pipeline** (see `Jenkinsfile`)

## Requirements

- Python 3.10+

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

## Run unit tests (pytest)

```bash
pytest -q
```

## Run system tests (Robot Framework)

```bash
robot -d robot_reports robot
```

Reports are generated in `robot_reports/` (`log.html`, `report.html`).

## Run CLI (manual)

```bash
python -m App.Cli.EcuSim_Cli "10 03"
python -m App.Cli.EcuSim_Cli "14 FF FF FF" --voltage 3.3 --seed-dtc B122021
```

If you run into `ModuleNotFoundError: No module named 'App'` when running CLI directly, set `PYTHONPATH=src`.

## Jenkins

This repo includes a ready-to-use **Declarative Pipeline** in `Jenkinsfile`.
It will:

1. Create a virtualenv (`.venv`)
2. Install `requirements-dev.txt`
3. Run:
   - `pytest -q --junitxml=reports/pytest-junit.xml`
   - `robot -d robot_reports --xunit robot_reports/robot-xunit.xml robot`
4. Publish results to Jenkins:
   - JUnit test trend (pytest + robot)
   - Robot HTML report (requires **HTML Publisher** plugin)
