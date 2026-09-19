# Carrier Board — Read This First

## Schematic complete; PCB placement is next

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
errors or warnings. The active phase is board outline and component placement,
followed by layout rules, routing, DRC, and fabrication-output review.

Do **not** release or fabricate until PCB placement/routing and final DRC,
mechanical, BOM, and CPL reviews are complete.

See [CM5 connector wiring and bring-up](Documentation/Research%20MD/CM5-Connector-Wiring-and-Bringup.md)
and the current project journal before continuing.

