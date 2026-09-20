# Carrier Board — Read This First

## Schematic corrections required before routing

Both Amphenol `10164227-1001A1RLF` schematic instances now contain 100 unique
pin designators numbered `1–100`, matching their physical footprint pads.
`CN1` represents CM5 logical pins 1–100 and `CN2` represents logical pins
101–200; the unique component designators distinguish their identical pad
numbers.

The earlier warning that CN1 pins `3–6`, `9–12`, and `15–20` were grounds was
incorrect. Those are Ethernet, fan, LED, sync, and EEPROM-control signals.
Unused signals remain open; only pins identified as GND by the CM5 datasheet
are grounded.

All schematic components and footprints have been transferred into
`Watchdog PCB.PcbDoc`. The 2026-09-19 compile/ECO completed with no reported
errors or warnings. However, the subsequent saved-CAD review found incorrect
camera-LDO pin assignments, disconnected Hailo output capacitors and USB
ground contacts, and missing recovery control and USB data protection.
These issues remain open; a clean compile is not electrical sign-off.

See the [review and proposed Basic substitutions](Documentation/Parts-and-Schematic-Review-2026-09-19.md)
and [prioritized task dashboard](Documentation/Schematic-Subsystems/README.md).

Do **not** release or fabricate until PCB placement/routing and final DRC,
mechanical, BOM, and CPL reviews are complete.

See [CM5 connector wiring and bring-up](Documentation/Research%20MD/CM5-Connector-Wiring-and-Bringup.md)
and the current project journal before continuing.

