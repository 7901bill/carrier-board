# 04 — Camera Power

Last updated: 2026-09-28

## Purpose

Provide a quiet, dedicated 3.3 V rail to the Raspberry Pi camera connector.

## Current status

**Critical correction required.** The AP2112 is now `U3` (formerly `U7`).
The 2026-09-24 PCB ECO retained the incorrect physical pin mapping, and the
camera output capacitor remains unverified. Earlier completion notes below
are not evidence of an implemented fix.

| U3 physical pin | Required function/connection | Saved PCB/ECO connection |
|---|---|---|
| 1 | VIN / main 5 V | Main 5 V |
| 2 | GND | Main 5 V — incorrect |
| 3 | EN / main 5 V | GND — incorrect |
| 4 | NC / unconnected | CN4-22 — incorrect |
| 5 | VOUT / camera 3.3 V, CN4-22 | No net — incorrect |

Correct the symbol designators/functions and placed instance, verify footprint
numbering against the [AP2112 datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf),
then regenerate the ECO. C15 is input decoupling only; add the intended 1 µF
output capacitor from corrected VOUT to GND and check effective capacitance.
See the consolidated [main design status](../documentation.md).

## Confirmed design intent (not verified as-built)

- Regulator: Diodes Incorporated `AP2112K-3.3TRG1`, LCSC `C51118`.
- Input: `5V_MAIN`.
- Output: `3V3_CAMERA`.
- The output is fixed at 3.3 V with a maximum electrical rating of 600 mA.
- Input capacitor: 1 µF, 50 V, X5R, 0603, LCSC `C15849`, directly from
  `5V_MAIN`/VIN to GND.
- Output capacitor: 1 µF, 50 V, X5R, 0603, LCSC `C15849`, directly from
  `3V3_CAMERA`/VOUT to GND.
- `VIN` and `EN` connect to the same `5V_MAIN` net for always-on operation.
  The EN input must not float because the AP2112 contains an internal 3 MΩ
  pull-down.
- `NC` is intentionally left unconnected.
- The standard Raspberry Pi 22-pin camera connector receives 3.3 V on pin 22.
- A separate 1.8 V carrier-board camera rail is not required for Camera
  Module 3; the module generates its lower internal rails.
- The selected camera is the standard Raspberry Pi Camera Module 3 using the
  IMX708 sensor, not Camera Module 3 Wide. Its documented maximum load still
  needs to be confirmed. Treat 300 mA as a thermal review case, not a verified
  maximum.
- At 300 mA from a 5 V input, the LDO dissipates approximately 0.51 W. Using
  the datasheet's 184°C/W SOT25 junction-to-ambient figure gives an estimated
  94°C junction rise, so useful copper area and prototype thermal testing are
  required. Typical camera consumption is expected to be below this maximum.
- The camera rail is separate from the Hailo switching rail.

## Schematic implementation

- Open: correct physical pins 2–5 and add output decoupling as listed above.
- Open: verify the corrected VOUT reaches CN4-22 and has no connection to NC.
- Open: confirm rail/ground test access and use clear rail net labels.
- Open: close thermal margin for the actual camera. The 300 mA case gives
  about 134°C junction at 40°C ambient using the cited thermal resistance;
  a 600 mA electrical rating does not establish usable thermal capacity.

## Load-switch decision

- **Omitted from Rev A:** `TPS22918`, LCSC `C131941`.
- TPS22918 is a load switch, not a voltage regulator. It would only add
  separate rail isolation or power cycling.
- `AP2112K-3.3TRG1` (`C51118`) remains the confirmed 5 V-to-3.3 V camera LDO.

## Definition of done

- The complete LDO circuit is drawn from the current datasheet.
- Camera power and ground pins are fully connected.
- Capacitor values, voltage ratings, and placement intent are recorded.
- Thermal margin is checked for the planned camera load.
- Camera power enable behavior is coordinated with the CM5 camera controls.

## References

- `Documentation/documentation.md`, current camera-power decision.
- `Documentation/Research MD/power-design-explainer.md`.
- AP2112K and selected camera documentation.

## Session notes

- 2026-09-18: Initial subsystem draft created from confirmed project records.
- 2026-09-18: Recorded the intended LDO circuit using `C51118`, two `C15849`
  1 µF X5R capacitors, EN tied to `5V_MAIN`, and NC open. The later saved-CAD
  review superseded the completion claim: U3 is wired incorrectly and the
  output capacitor is missing. The 300 mA value remains a thermal review case.
