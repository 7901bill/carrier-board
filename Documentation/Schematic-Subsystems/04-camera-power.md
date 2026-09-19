# 04 — Camera Power

Last updated: 2026-09-18

## Purpose

Provide a quiet, dedicated 3.3 V rail to the Raspberry Pi camera connector.

## Current status

**LDO circuit complete in CAD.** The regulator, fixed 3.3 V configuration,
enable connection, and local input/output capacitors are drawn. Connection to
the camera connector and prototype thermal verification remain to be checked
as part of the full-sheet review.

## Confirmed design

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
- The selected Arducam-class camera is expected to draw no more than
  approximately 300 mA.
- At 300 mA from a 5 V input, the LDO dissipates approximately 0.51 W. Using
  the datasheet's 184°C/W SOT25 junction-to-ambient figure gives an estimated
  94°C junction rise, so useful copper area and prototype thermal testing are
  required. Typical camera consumption is expected to be below this maximum.
- The camera rail is separate from the Hailo switching rail.

## Schematic implementation

- Completed: AP2112K VIN, VOUT, GND, EN, NC treatment, and required local
  capacitors.
- Completed: `5V_MAIN` input and `3V3_CAMERA` output rail definition.
- Verify during full-sheet review: `3V3_CAMERA` reaches camera-connector pin
  22, camera grounds are complete, and intended rail/ground test access is
  present.

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
- 2026-09-18: LDO circuit completed using `C51118`; selected two `C15849`
  1 µF X5R capacitors, tied EN to `5V_MAIN`, and left NC open. Recorded the
  approximately 300 mA maximum camera load and required thermal validation.
