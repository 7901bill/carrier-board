# Carrier Board — Read This First

## Current PCB finishing work - 2026-10-09

Routing is substantially implemented in the saved PCB: all nine differential
pairs are defined and each member has top-layer tracks. Finish corner GND
vias, revise the board outline, and add/re-pour the required polygon copper.
Then refresh connectivity and resolve remaining DRC items in Altium. Final
routing, impedance, and release sign-off remain open.

The read-only saved-file audit found 85 connection records (83 GND and two
`NetCN1_78`), a broadly scoped 90-ohm differential rule, and unequal USB
track-only lengths. No DRC report was found, so a small remaining violation
count is not independently confirmed. See the [PCB audit](Documentation/PCB-Audit-2026-10-09.md) for evidence
and the limits of this inspection.

See the [current design status](Documentation/documentation.md) and
[subsystem dashboard](Documentation/Schematic-Subsystems/README.md).

## Earlier schematic-review findings requiring final re-verification

Both Amphenol `10164227-1001A1RLF` schematic instances now contain 100 unique
pin designators numbered `1–100`, matching their physical footprint pads.
`CN1` represents CM5 logical pins 1–100 and `CN2` represents logical pins
101–200; the unique component designators distinguish their identical pad
numbers.

The earlier warning that CN1 pins `3–6`, `9–12`, and `15–20` were grounds was
incorrect. Those are Ethernet, fan, LED, sync, and EEPROM-control signals.
Unused signals remain open; only pins identified as GND by the CM5 datasheet
are grounded.

The [current design status](Documentation/documentation.md) records all 43
schematic components in the saved LiveBOM and PCB, with their footprint names
matching. The earlier 2026-09-19 saved-CAD review found
incorrect camera-LDO pin assignments, disconnected Hailo output capacitors,
and USB ground contacts. The camera-LDO mapping remains incorrect in the
2026-09-24 ECO. Recovery switch `SW` has since been added and ECO-connected,
but its physical operation remains unverified. A clean compile is not
electrical sign-off.

At the 2026-09-29 documentation checkpoint, PCB layout setup had an
approximately 100 mm x 60 mm working outline,
all 43 components placed, a four-layer `SIG 1`/`GND`/`PWR`/`SIG 2` stack, and
basic clearance/width/via rules. That review listed open schematic,
mechanical, differential-pair, and net-name checks. Do not assume those older
items are closed merely because routing has started; re-verify affected nets
and rules before final sign-off.

## Documentation workflow

- [`Documentation/Journal.md`](Documentation/Journal.md) is the source of
  truth for verified decisions, evidence, and completed work.
- [`Documentation/documentation.md`](Documentation/documentation.md) is the
  daily progress record, active-blocker list, and resume checkpoint.
- [`Documentation/Schematic-Subsystems/`](Documentation/Schematic-Subsystems/README.md)
  contains the detailed implementation and verification status for each
  schematic block.

Whenever Bill asks to **update the documentation**, synchronize all three
layers in the same documentation pass:

1. Record verified facts and decisions in `Journal.md`.
2. Update the current progress, blockers, reminders, and daily changes in
   `documentation.md`.
3. Update the affected subsystem files and the subsystem progress dashboard.

Resolve contradictory current-status statements during that pass. Preserve
dated history, but clearly mark any older conclusion that a newer verified
entry supersedes.

Do **not** release or fabricate until PCB placement/routing and final DRC,
mechanical, BOM, and CPL reviews are complete.

Review the current design status, project journal, and affected subsystem
records before continuing.

