# 11 — Status Indicators and Test Points

Last updated: 2026-10-14

## Current release status — 2026-10-14

Bill reports routing, DRC, polygon pour, electrical testing, high-speed,
mechanical, and power verification complete. The earlier review findings in
this file are retained as historical records and are closed as active release
checklist blockers under that completion report. Specific correction details
and test results were not supplied; no independent CAD audit or test was
performed in this documentation pass.

Remaining work: Include existing test-point labels, any populated indicators, and do-not-populate notes in the assembly drawings and BOM. Optional new indicators are outside this release-file task.

Prepare the final fabrication/assembly package using the
[current checklist](../documentation.md). No schematic/PCB edits or manufacturing
exports were made in this pass. This update does not claim post-assembly
software or functional bring-up has occurred.

## Purpose

Provide safe measurement and visible diagnostic access during initial power-up,
CM5 flashing, boot, camera bring-up, and Hailo bring-up.

## Historical status snapshot — superseded by the 2026-10-14 completion report

**Rough draft.** The need for diagnostic access is confirmed. Visible main
power and PD-negotiation indicators are planned. Additional per-subsystem LEDs
and physical test-point package choices can be decided later.

## Confirmed bring-up philosophy

- Power and test one section at a time.
- Intended sequence: empty board/power system → CM5 → USB flashing → eMMC boot
  and UART → Wi-Fi/SSH → camera → Hailo.
- Status circuits must not significantly load power-good, reset, clock, or
  other boot-critical signals.
- High-speed PCIe, CSI-2, and USB test access must not create uncontrolled
  routing stubs.

## Planned minimum test access

- Multiple ground probe points.
- Negotiated/input supply after the USB-PD section.
- `5V_MAIN`.
- `3V3_HAILO`.
- `3V3_CAMERA`.
- Hailo enable/load-switch control.
- Hailo `PERST#`.
- `nRPIBOOT`.
- CM5 reset/power-control signal.
- Programming-port VBUS presence/sense.
- UART TX and RX through the debug connector.

## Planned indicator functions

- Main board/5 V power present.
- Successful USB-PD negotiation using the CH224A status signal.
- **Potential task:** add low-current rail-presence LEDs in parallel with
  `5V_MAIN`, `CM5_3.3V`, `3V3_HAILO`, and `3V3_CAMERA`, each with its own
  series current-limiting resistor. These show rail presence, not load margin
  or correct connection of every power pin.
- **Potential task:** consider buffered `LED_nPWR` or `LED_nACT` indication
  only if CM5 power-state or activity feedback is desired. Neither signal is
  needed for simple power-rail indication.
- Optional local-rail indications where they will not compromise regulation or
  create misleading results.
- Recovery/activity indication only when supported by a safe, reviewed signal.

## Definition of done

- A multimeter and oscilloscope can reach every major rail safely.
- Sequencing between `3V3_HAILO` and `PERST#` can be measured directly.
- Flash/recovery control states can be probed.
- LEDs have explicit current-limiting resistors.
- No indicator overloads or changes a critical signal state.
- High-speed interfaces remain free of unnecessary test stubs.

## Bring-up measurements to record later

- Input voltage before and after PD negotiation.
- `5V_MAIN` startup, ripple, and load behavior.
- `3V3_HAILO` startup time and reset-release delay.
- `3V3_CAMERA` voltage and regulator temperature.
- CM5 current during recovery and normal boot.
- UART boot log and PCIe/camera detection results.

## References

- `Documentation/Research MD/programming.md`.
- `Documentation/Research MD/power-design-explainer.md`.
- Project bring-up sequence in `Documentation/documentation.md`.

## Session notes

- 2026-09-18: Initial status/test-access draft created.

- 2026-10-14: Updated current release status from Bill's completion report.
  Electrical, power, high-speed, mechanical, routing, DRC, and pour checks are
  closed as release checklist items. Only sourcing and manufacturing file
  preparation remain; older findings are preserved as superseded history.
