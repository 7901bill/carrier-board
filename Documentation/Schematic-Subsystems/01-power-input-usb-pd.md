# 01 — USB-C Power Input and Power Delivery

Last updated: 2026-09-19

## Open review actions — 2026-09-19

- Open: validate simultaneous CM5/Hailo/camera load against the 9 V/3 A
  source (27 W before conversion losses), fuse derating and transient demand.
- Proposed only: R1 `C2770993` → Basic `C23212`, same 6.8 kΩ/0603,
  100 mW/75 V/100 ppm/°C, with tolerance improved to 1%. The replacement
  does not retain the existing AEC-Q200 qualification. Confirm that is
  acceptable, and recheck stock and fee classification before substitution.

These actions are not implemented. Evidence and parts caveats are in the
[review report](../Parts-and-Schematic-Review-2026-09-19.md).

## Subsystem purpose

Accept DC power from an external USB-C PD charger, request 9 V, protect the
board input, and deliver the negotiated supply to the main 5 V converter.

## Current status

**Schematic complete and transferred to PCB.** The connector, negotiation
controller, requested voltage, and simplified fuse-plus-TVS Rev A protection
are implemented. The MP2329 enable network prevents startup from the default
5 V USB supply.

## Confirmed design

- This is the board's main power connector; it is separate from the CM5
  programming/recovery connector.
- Connector: HRO `TYPE-C-31-M-12`, LCSC `C165948`.
- The connector is a 12-pin mid-mount USB-C receptacle rated for 5 A/20 V and
  has through-hole mounting legs.
- USB-PD sink controller: `CH224A`, LCSC `C42459160`.
- The CH224A uses resistor configuration and requires no microcontroller.
- Requested input voltage: 9 V using the documented 6.8 kΩ configuration.
- CH224A `VBUS` must connect to `VHV` as required by its reference design.
- Retain the existing 1 µF/50 V/0603 capacitor `C15849`; no capacitor
  substitution is approved or required for the current design.
- The earlier TPS25947 eFuse decision is superseded; it is not part of Rev A.
- `USBC_Protection.SchDoc` contains the physical fast-acting fuse: Walter
  `1206T3A63V`, LCSC/JLCPCB `C354897`, rated 3 A/63 V.
- `Power Rails.SchDoc` contains the `SMBJ12A` TVS, LCSC/JLCPCB `C151251`.
- Rev A therefore retains fuse + TVS but omits the earlier TPS25947 eFuse.
- The MP2329 external enable divider uses 453 kΩ (`C25818`) from input to EN
  and 100 kΩ (`C25803`) from EN to ground. Including the MP2329's internal
  1 MΩ EN resistance, the nominal start threshold is approximately 7.5 V.
  Default 5 V USB input therefore remains below the intended start threshold,
  while a negotiated 9 V input enables the converter.
- A plain 5 V-only charger is not intended to operate the complete board.

## Planned schematic content

- USB-C receptacle and shield/ground connections.
- CH224A and all datasheet-required support connections.
- The confirmed 9 V configuration resistor.
- Fuse `C354897` in the input-current path and TVS `C151251` at the protected
  input node.
- Input and negotiated-voltage test points.
- A visible indication of successful negotiation where practical.
- A controlled path from negotiated VBUS to the MP2329 input.

## Dependencies

- The peak-power calculation in [02-main-5v-power.md](02-main-5v-power.md).
- The final definition of failed or incomplete PD negotiation behavior.
- Connector assembly capability and footprint verification.

## Definition of done

- The power connector, CH224A, and all required support parts are drawn.
- The 9 V request configuration is checked against the current datasheet.
- The fuse-plus-TVS Rev A protection topology is explicitly documented and drawn.
- The circuit cannot accidentally create a second power path through the
  programming USB connector.
- Connector shell and mounting contacts are correctly represented.
- Relevant voltage, status, and ground test access is provided.

## References

- `Documentation/documentation.md`, power-input decisions.
- `Documentation/Research MD/power-design-explainer.md`.
- CH224A and `TYPE-C-31-M-12` datasheets in `Documentation/Datasheets/`.

## Session notes

- 2026-09-18: Initial subsystem draft created from confirmed project records.
