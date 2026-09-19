# 08 — CM5 Programming USB

Last updated: 2026-09-19

## Purpose

Provide a dedicated USB 2.0 device connection from a development computer to
the CM5 for initial eMMC flashing and recovery.

## Current status

**Schematic complete and transferred to PCB.** The dedicated USB-C programming
port, USB 2.0 data path, CC termination, protection, VBUS treatment, shield,
and ground connections are drawn. The project compile/ECO completed without
reported errors or warnings.

## Confirmed architecture

- The programming connector is separate from the main USB-PD power connector.
- Programming connector: a second HRO `TYPE-C-31-M-12`, LCSC `C165948`.
- Reusing the receptacle does not reuse the power-port circuit: this connector
  receives USB-device CC termination, USB 2.0 data, ESD, and safe VBUS sensing,
  not a second CH224A PD sink circuit.
- Reuse of `C165948` is confirmed for Rev A to reduce unique BOM items.
- It carries the CM5 USB 2.0 D+ and D− device signals to a host computer.
- It is used with `nRPIBOOT` and Raspberry Pi `rpiboot` to expose the CM5 eMMC.
- It is not intended to power the complete carrier board.
- Programming-port VBUS must not be tied directly to `5V_MAIN`; that would
  create competing power sources between the host and main converter.
- Connector ground connects to the board ground plane.
- Low-capacitance USB ESD protection is required near the connector.
- The USB-C programming receptacle requires the correct device/sink-side CC
  arrangement from an authoritative USB-C reference circuit.

## Planned schematic content

- Dedicated `C165948` USB-C receptacle.
- USB 2.0 D+ and D− path to the CM5.
- Correct USB-C device-side CC resistors.
- Low-capacitance ESD protection.
- Reference-based VBUS presence/sense circuit with no back-power path.
- Shield and ground treatment.
- Accessible D+/D− test access only if it can be provided without harmful stubs.
- VBUS-sense and ground test points.

## Flashing relationship

The programming connector supplies the USB data/recovery path. The main power
connector supplies adequate board power. Holding `nRPIBOOT` low during power-up
places the CM5 into USB recovery mode so `rpiboot` can expose the eMMC to the
development computer.

## Definition of done

- USB data routing reaches the correct CM5 pins with correct polarity.
- CC, ESD, VBUS sensing, shield, and ground are drawn from reviewed references.
- No direct host-VBUS-to-`5V_MAIN` path exists.
- The connector can be used while the board receives normal main power.
- The schematic supports both initial flashing and recovery of a corrupted
  eMMC image.

## References

- `Documentation/Research MD/programming.md`.
- `Documentation/Research MD/CM5-Connector-Wiring-and-Bringup.md`.
- Current CM5 datasheet and official CM5 IO reference design.

## Session notes

- 2026-09-18: Initial programming-USB draft created. This subsystem is a
  mandatory part of Schematic V1, not an optional accessory.
- 2026-09-19: Completed the programming-port schematic and imported its
  components into the PCB document. Placement and USB routing are next.
