# 05 — CM5 Connectors and Base Connections

Last updated: 2026-09-19

## Purpose

Provide the complete electrical and mechanical interface between the CM5 and
the carrier-board power, PCIe, camera, programming, recovery, and debug
subsystems.

## Current status

**In progress / release blocker.** The two connector symbols are consolidated
in `Amphenol ICC.SchDoc`. The M.2/PCIe and CSI-2 nets are connected, and the
misleading MIPI friendly labels were corrected. Remaining CM5 base power,
ground, recovery/debug wiring, no-connect treatment, and final schematic-to-
footprint pin-map verification must be completed before PCB transfer.

## Confirmed design

- The design uses a CM5, not a CM4; their pin assignments are not interchangeable.
- The two carrier connectors are Amphenol `10164227-1001A1RLF` 100-pin parts.
- Connector 1 uses CM5 logical pins 1–100.
- Connector 2 uses CM5 logical pins 101–200 while its physical footprint pads
  remain numbered 1–100.
- Connector 1 must include required ground pins 3–6, 9–12, and 15–20.
- Connector 2 requires an explicit Altium model pin map from schematic pins
  101–200 to footprint pads 1–100.
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

## Mandatory library verification

1. Restore and connect the missing Connector 1 grounds.
2. Create and inspect Connector 2's 101–200 to 1–100 model mapping.
3. Compare both symbols and footprints with the CM5 datasheet, connector
   manufacturer drawing, and official CM5 IO reference design.
4. After Schematic V1, inspect the Altium ECO for unmatched or incorrectly
   assigned pins and pads before creating/routing the PCB.

## Definition of done

- Both connector symbols and footprints are independently verified.
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
  lane labels. Full connector power/ground and footprint mapping still require
  the release review described above.
