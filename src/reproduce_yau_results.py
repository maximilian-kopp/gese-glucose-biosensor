#!/usr/bin/env python3
"""Reproduce stated arithmetic from the Yau 2024 manuscript CSVs.

This script uses only numbers that appear in the manuscript text (or the
two angle labels printed on Figure 21). It does not digitize plots.

Checks:
  * 100 deg / 1.59 deg/(mg/dL) rounds to the stated 62.9 mg/dL
  * Figure 21 printed labels 235 deg - 135 deg == 100 deg
  * 658 nm corresponds to the stated 1.88 eV
  * External quantum efficiency from the stated 0.15 mA/W at 658 nm
    rounds to the stated 0.028%

It cannot refit the 1.59 deg/(mg/dL) slope or any R^2, because the
manuscript has no (concentration, angle) table.

Usage, from the repo or package root:

    python src/reproduce_yau_results.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# CODATA 2018 constants for the EQE and photon-energy checks
H = 6.62607015e-34  # J s
C = 299792458.0  # m/s
E = 1.602176634e-19  # C
EV_NM = (H * C / E) * 1e9  # eV·nm, ≈ 1239.84


def load_rows(path: Path, key: str) -> dict[str, dict]:
    with path.open(newline="") as f:
        reader = csv.DictReader((ln for ln in f if not ln.startswith("#")))
        return {row[key]: row for row in reader}


def main() -> int:
    stated = load_rows(DATA / "yau-2024-stated-results.csv", "quantity")
    methods = load_rows(DATA / "yau-2024-methods-parameters.csv", "parameter")
    labels = load_rows(DATA / "yau-2024-figure21-printed-angle-labels.csv", "condition_as_printed")

    sensitivity = float(stated["detection_sensitivity"]["value"])
    rotation = float(stated["self_test_polarization_angle_rotation"]["value"])
    reported_increase = float(stated["self_test_inferred_glucose_increase"]["value"])
    computed_increase = rotation / sensitivity
    increase_ok = round(computed_increase, 1) == reported_increase

    empty = float(labels["Empty stomach"]["printed_angle_deg"])
    after = float(labels["Half hour after dinner"]["printed_angle_deg"])
    delta = after - empty
    delta_ok = delta == rotation

    wavelength_nm = float(methods["laser_wavelength_nm_in_text"]["value"])
    stated_eV = float(methods["example_photon_energy_for_658nm"]["value"])
    computed_eV = EV_NM / wavelength_nm
    ev_ok = round(computed_eV, 2) == stated_eV

    responsivity_mA_per_W = float(stated["photoresponsivity_at_1V"]["value"])
    stated_eqe_percent = float(stated["external_quantum_efficiency"]["value"])
    R_A_per_W = responsivity_mA_per_W * 1e-3
    eqe = R_A_per_W * (EV_NM / wavelength_nm)
    eqe_percent = eqe * 100
    eqe_ok = round(eqe_percent, 3) == stated_eqe_percent

    print("Yau 2024 manuscript: stated-number checks")
    print("-----------------------------------------")
    print(f"Sensitivity (text, §4.2):          {sensitivity} deg/(mg/dL)")
    print(f"Self-test rotation (text, §4.4):    {rotation} deg")
    print(f"Computed increase:                  {computed_increase:.6f} mg/dL")
    print(f"Rounded to 1 decimal:               {round(computed_increase, 1)} mg/dL")
    print(f"Value stated in the manuscript:     {reported_increase} mg/dL")
    print(f"100 / 1.59 matches 62.9:            {increase_ok}")
    print()
    print(f"Figure 21 printed labels:           {empty:.0f} deg and {after:.0f} deg")
    print(f"235 - 135:                          {delta:.0f} deg")
    print(f"Matches stated 100 deg:             {delta_ok}")
    print()
    print(f"Laser wavelength in the text:       {wavelength_nm:.0f} nm")
    print(f"Computed photon energy:             {computed_eV:.4f} eV")
    print(f"Value stated in §2.2 (1.88 eV):     {stated_eV} eV")
    print(f"658 nm rounds to 1.88 eV:           {ev_ok}")
    print()
    print(f"Photoresponsivity at 1 V (text):    {responsivity_mA_per_W} mA/W")
    print(f"EQE from R and 658 nm:              {eqe_percent:.5f} %")
    print(f"Value stated in §4.1:               {stated_eqe_percent} %")
    print(f"Rounds to 0.028 %:                  {eqe_ok}")
    print()
    print("Calibration fit / R^2")
    print("---------------------")
    print("No (concentration, angle) table is printed in the manuscript.")
    print("The 1.59 deg/(mg/dL) slope and any R^2 cannot be refit from the CSVs.")
    print()

    ok = increase_ok and delta_ok and ev_ok and eqe_ok
    print("RESULT:", "PASS (stated arithmetic matches)" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
