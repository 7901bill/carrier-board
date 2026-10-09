# 08 — CM5 Programming USB

Last updated: 2026-10-09

## Saved PCB checkpoint - 2026-10-09

The saved October 8 PCB independently confirms substantial routing and all
nine differential-pair definitions, superseding the earlier no-pair/no-routing
snapshot below. Finish corner GND vias, the board outline, polygon pours,
connectivity checks, and final DRC. Differential-rule scope and USB skew need
review. This checkpoint does not close older electrical or mechanical findings.
See the [PCB audit](../PCB-Audit-2026-10-09.md) for current evidence.

## Purpose

Provide a dedicated USB 2.0 device connection from a development computer to
the CM5 for initial eMMC flashing and recovery.

## Earlier status snapshot

**Correction required.** The 2026-09-19 review found programming-port cable
ground-pad groups `A1B12` and `B1A12` without PCB nets. The current two
USB-C designators are `USBC 1` and `USBC2`, so first identify the programming
connector in the saved CAD and recheck its pad nets; grounded shell pads 1–4
do not replace signal ground. No USB data ESD array is present in the current
43-component inventory; select and implement suitable low-capacitance
protection before routing.

Duplicated D+/D− contacts and separate 5.1 kΩ CC resistors are connected.
VBUS groups join each other but remain isolated from main 5 V. No VBUS-sense
circuit is present; review the CM5 reference before deciding whether one is
required. Earlier completion notes are superseded. See the consolidated
[main design status](../documentation.md).

USBC2 and CN2 are placed. The layout note reports the 90-ohm USB profile
calculated for L1 over L2 ground, but the saved PCB has no USB differential
pair object/class membership and still uses the generic 15 mil/10 mil
differential rule. Ground-pad correction, ESD selection, VBUS treatment, pair
definition, profile-linked rule, and routing all remain open.

## Confirmed architecture

- The programming connector is separate from the main USB-PD power connector.
- Programming connector: a second HRO `TYPE-C-31-M-12`, LCSC `C165948`.
- Reusing the receptacle does not reuse the power-port circuit: this connector
  uses USB-device CC termination and USB 2.0 data, not another CH224A PD sink.
  ESD implementation and reference-based VBUS treatment remain open.
- Reuse of `C165948` is confirmed for Rev A to reduce unique BOM items.
- It carries the CM5 USB 2.0 D+ and D− device signals to a host computer.
- It is used with `nRPIBOOT` and Raspberry Pi `rpiboot` to expose the CM5 eMMC.
- It is not intended to power the complete carrier board.
- Programming-port VBUS must not be tied directly to `5V_MAIN`; that would
  create competing power sources between the host and main converter.
- Connector ground connects to the board ground plane.
- Low-capacitance USB ESD protection is required near the connector.
- Route D+ and D- as one 90-ohm differential pair, as required by the current
  official CM5 datasheet. Preserve polarity; USB 2.0 P/N swapping is not
  permitted.
- The USB-C programming receptacle requires the correct device/sink-side CC
  arrangement from an authoritative USB-C reference circuit.

## PCB-layout requirements

- Define `USB_P`/`USB_N` as a differential pair and derive its 90-ohm width
  and gap from the final JLCPCB stackup.
- The saved PCB's generic 15 mil/10 mil differential rule is a placeholder,
  not an approved USB geometry.
- Keep the pair over a continuous reference plane, minimize discontinuities,
  and avoid uncontrolled test-point stubs.
- Place the required low-capacitance ESD array close to `USBC2` and keep the
  protected path in line with the differential pair.
- Do not add a 90-ohm shunt resistor across D+/D-; controlled impedance is a
  transmission-line geometry requirement and the USB PHY handles termination.

## Planned schematic content

- Dedicated `C165948` USB-C receptacle.
- USB 2.0 D+ and D− path to the CM5.
- Correct USB-C device-side CC resistors.
- Low-capacitance ESD protection.
- Reference-based VBUS treatment; add sensing only if required by the reviewed design.
- Shield and ground treatment.
- Accessible D+/D− test access only if it can be provided without harmful stubs.
- Ground test access; VBUS-sense test access only if sensing is implemented.

## Flashing relationship

The programming connector supplies the USB data/recovery path. The main power
connector supplies adequate board power. Holding `nRPIBOOT` low during power-up
places the CM5 into USB recovery mode so `rpiboot` can expose the eMMC to the
development computer.

## Definition of done

- USB data routing reaches the correct CM5 pins with correct polarity.
- CC, ESD, VBUS treatment, shield, and ground are drawn from reviewed references.
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
- 2026-09-28: Locked the programming USB 2.0 pair to 90 ohms differential
  from the current CM5 datasheet and recorded that polarity must not be
  swapped. Pair creation, ESD selection, stackup geometry, routing, and tuning
  remain open; no CAD change was made.
- 2026-09-28: Layout setup placed USBC2/CN2 and reportedly calculated the
  90-ohm profile. Saved-CAD review still found no USB pair object or
  profile-linked rule, so the interface is not routing-ready.
