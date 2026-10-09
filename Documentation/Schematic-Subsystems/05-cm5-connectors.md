# 05 — CM5 Connectors and Base Connections

Last updated: 2026-10-09

## Saved PCB checkpoint - 2026-10-09

The saved October 8 PCB independently confirms substantial routing and all
nine differential-pair definitions, superseding the earlier no-pair/no-routing
snapshot below. Finish corner GND vias, the board outline, polygon pours,
connectivity checks, and final DRC. Differential-rule scope and USB skew need
review. This checkpoint does not close older electrical or mechanical findings.
See the [PCB audit](../PCB-Audit-2026-10-09.md) for current evidence.

## Purpose

Provide the complete electrical and mechanical interface between the CM5 and
the carrier-board power, PCIe, camera, programming, recovery, and debug
subsystems.

## Earlier status snapshot

**Connector component verified and approved for placement and routing.** `CN1`
and `CN2` use the exact Raspberry Pi-specified Amphenol
`10164227-1001A1RLF` (`C6782225`). Both symbols have 100 unique physical pin
designators `1–100`, and both use the verified manufacturer-matching footprint
`CONN-SMD_100P-P0.40_10164227-1001A1RLF`. No symbol, footprint, or component
replacement is required.

The two placed connector instances are ready to route. Preserve the user's
chosen visible pin names and the verified physical numbering/electrical types.
The 2026-09-23 PCB ECO connects CN1-93 to recovery switch `SW`, which is
grounded on its other terminal. Access, test point, and functional recovery
remain open in [09](09-boot-recovery-reset.md).
Programming USB ground/protection and camera/Hailo supply corrections are
tracked in the [main design status](../documentation.md).
The reported clean compile/ECO does not close those unrelated subsystem
issues. Final board-level CM5 alignment, clearance, and 1:1 assembly fit remain
placement checks, not reasons to change the verified connector component.

## Confirmed design

- The design uses a CM5, not a CM4; their pin assignments are not interchangeable.
- The two carrier connectors are Amphenol `10164227-1001A1RLF` 100-pin parts.
- The exact component identity, schematic pin count, pad numbering, footprint
  association, and copper land geometry were independently verified on
  2026-09-29. The footprint has 100 SMT pads, 0.40 mm pitch, 0.20 mm x 0.70 mm
  lands, 19.60 mm end-to-end contact span, and 3.08 mm row-center spacing,
  matching the Amphenol recommended PCB layout.
- The `-1001A1RLF` variant is the no-hold-down, 1.5 mm mated-stack-height
  receptacle specified for the standard low-profile CM5 installation.
- Connector 1 uses CM5 logical pins 1–100.
- Both schematic symbols and both footprints use physical pin numbers 1–100.
  `CN1` represents CM5 logical pins 1–100; `CN2` represents logical pins
  101–200. Their unique component designators distinguish the two instances.
- CN1 pins 3–6 and 9–12 are Ethernet pairs, not grounds. Pins 15–20 are
  Ethernet/fan/EEPROM-control signals, not grounds. They remain unused in
  Rev A except where later requirements explicitly say otherwise.
- All 21 CN1 ground pins and all 30 CN2 ground pins were checked as connected.
- Unused GPIOs are explicitly disconnected. Pins 51/55 are reserved for UART,
  and pins 97/100 are used for camera control.
- Pins 56/58 (`GPIO3/SCL1`, `GPIO2/SDA1`) are unused; camera control instead
  uses pins 80/82 (`SCL0`, `SDA0`).
- Pins 21 `LED_nACT`, 76 `VBAT`, 92 `PWR_BUT`, 95 `LED_nPWR`, and 99
  `PMIC_ENABLE` are unused in Rev A and have no-connect markers. Pin 93
  `nRPIBOOT` remains reserved for the recovery circuit.
- CM5 pin 78 `GPIO_VREF` connects to the CM5 3.3 V output net from pins 84 and
  86 to select 3.3 V GPIO signaling.
- CM5 pin 55 `GPIO14/UART0_TX` is the debug transmit signal.
- CM5 pin 51 `GPIO15/UART0_RX` is the debug receive signal.
- CM5 pin 93 `nRPIBOOT` is used for USB recovery control.
- CM5 pins 94 and 96 (`CC1` and `CC2`) remain intentionally unconnected in
  this design; neither board USB-C connector uses them.
- CM5 pin 80 `SCL0` and pin 82 `SDA0` are assigned to camera control.
- CM5 pin 97 `CAM_GPIO0` and pin 100 `CAM_GPIO1` are assigned to camera control.
- CM5 MIPI0 mapping is verified as pins 115/117 for data lane 0, 121/123 for
  lane 1, 127/129 for clock, 133/135 for lane 2, and 139/141 for lane 3.
- CM5 pin 141 is `MIPI0_D3_P`; it is not camera lane 0 negative.
- The full CM5 variant has eMMC and does not require a microSD connector.

## Planned schematic content

- Every required CM5 5 V and ground contact.
- Complete PCIe lane, reference clock, reset, and clock-request connections.
- Complete CSI-2, camera I²C, and camera-control connections.
- USB 2.0 programming/recovery signals.
- `nRPIBOOT`, reset/power control, and UART.
- Explicit no-connect markers for every intentionally unused pin.
- Clear cross-sheet net labels with consistent spelling.

## Remaining board-level checks

1. Both connectors are placed; confirm final CM5 mechanical alignment,
   orientation, retention, installed-module clearance, and 1:1 assembly fit.
   This is a placement/system check; the component and footprint are approved.
2. Confirm connector-edge, camera-cable, antenna, heatsink, and access
   constraints within the approximately 100 mm x 60 mm working outline.
3. Re-run PCB DRC after routing and every relevant ECO. Watch for recurrence of
   the stale/corrupt placed-footprint DRC behavior reported during placement.

## Definition of done

- Both connector symbols and footprints are independently verified. Complete
  as of 2026-09-29; do not replace or redraw them without a new approved part.
- Every required power and ground pin is connected.
- Every used interface reaches its corresponding subsystem.
- Every intentionally unused pin has a no-connect marker.
- No CM4 pin assumptions are present.
- A later compile/ECO produces no unexplained connector mismatch.

## References

- Root `README.md` release warning.
- `Documentation/Research MD/CM5-Connector-Wiring-and-Bringup.md`.
- Current CM5 datasheet and official CM5 IO reference design.
- Amphenol connector drawing.

## Session notes

- 2026-09-18: Initial subsystem draft created; connector corrections remain
  the first schematic priority.
- 2026-09-19: Consolidated the connector sheets, connected the complete M.2
  and CSI interfaces, and corrected the imported symbol's displayed camera
  lane labels.
- 2026-09-19: Corrected CN2 to physical pin designators 1–100 and verified both
  placed connectors have 100 unique pins. Confirmed all required grounds are
  grounded and unused GPIOs are disconnected. Corrected the earlier false
  classification of Ethernet/control pins as grounds.
- 2026-09-19: Completed remaining wiring/no-connect treatment, obtained a
  clean compile/ECO with no reported errors or warnings, and transferred all
  components to the PCB document. Component placement is next.
- 2026-09-28: All components, including CN1 and CN2, are placed inside the
  working outline. Placement does not close alignment, retention, clearance,
  footprint, or full mechanical-fit verification.
- 2026-09-29: Closed component and footprint verification for CN1/CN2. Both
  instances are confirmed as Amphenol `10164227-1001A1RLF` / LCSC `C6782225`;
  each symbol has 100 unique pins and each linked footprint matches the
  manufacturer's 100-pad land pattern. No connector-library change is needed.
  The placed instances are approved for routing, subject only to the remaining
  board-level alignment, clearance, and final fit checks above.
