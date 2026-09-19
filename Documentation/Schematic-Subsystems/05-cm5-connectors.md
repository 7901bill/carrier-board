# 05 — CM5 Connectors and Base Connections

Last updated: 2026-09-19

## Purpose

Provide the complete electrical and mechanical interface between the CM5 and
the carrier-board power, PCIe, camera, programming, recovery, and debug
subsystems.

## Current status

**Schematic complete and transferred to PCB.** Both placed
connectors have 100 unique pin designators numbered `1–100`. Required grounds
are grounded, required 5 V inputs are connected, unused GPIOs have no-connect
markers, and the M.2/PCIe, CSI-2, programming USB, recovery, and debug UART
nets are connected. The project compile/ECO completed with no reported errors
or warnings, and all components were imported into the PCB layout.

## Confirmed design

- The design uses a CM5, not a CM4; their pin assignments are not interchangeable.
- The two carrier connectors are Amphenol `10164227-1001A1RLF` 100-pin parts.
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

## Remaining PCB verification

1. Place both connectors and confirm CM5 mechanical alignment and orientation.
2. Compare both footprints with the connector manufacturer drawing.
3. Re-run PCB DRC after placement and routing.

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
  lane labels.
- 2026-09-19: Corrected CN2 to physical pin designators 1–100 and verified both
  placed connectors have 100 unique pins. Confirmed all required grounds are
  grounded and unused GPIOs are disconnected. Corrected the earlier false
  classification of Ethernet/control pins as grounds.
- 2026-09-19: Completed remaining wiring/no-connect treatment, obtained a
  clean compile/ECO with no reported errors or warnings, and transferred all
  components to the PCB document. Component placement is next.
