# Schematic Subsystems

Last updated: 2026-10-14

This folder is the detailed working record for Schematic V1 of the Wireless
Watchdog CM5 carrier board. Each file covers one independently reviewable
subsystem. `Documentation/Journal.md` is the source of truth for verified
decisions, while `Documentation/documentation.md` is the daily working summary
and active-blocker list.

## Current release status — 2026-10-14

Bill reports routing, DRC, polygon pour, electrical testing, high-speed,
mechanical, and power verification complete. Earlier electrical and layout
findings are superseded as active release blockers. This is a user-reported
completion checkpoint; no new CAD audit or test was performed in this pass.

Only final component sourcing and preparation/review of the fabrication and
assembly file package remain. See the [current checklist](../documentation.md).
Older subsystem sections preserve previous design intent and audit findings;
follow the October 14 current-status section in each file for release work.

## Progress dashboard

| File | Subsystem | Current release status | Remaining release work |
|---|---|---|---|
| [01](01-power-input-usb-pd.md) | USB-C input and PD | Power/electrical checks complete, user-reported | Final part sourcing; release drawings/BOM |
| [02](02-main-5v-power.md) | Main 5 V supply | Power/electrical/layout checks complete, user-reported | Settle U5 procurement and final passive sourcing |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Power/electrical/layout checks complete, user-reported | Final capacitor sourcing; BOM and output package |
| [04](04-camera-power.md) | Camera power | Power/electrical checks complete, user-reported | Final capacitor sourcing; BOM and output package |
| [05](05-cm5-connectors.md) | CM5 connectors | Electrical/mechanical/layout checks complete, user-reported | Final sourcing and assembly output data |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | Electrical/high-speed/mechanical checks complete, user-reported | Final connector sourcing and assembly notes |
| [07](07-csi2-camera.md) | CSI-2 camera | Electrical/high-speed/mechanical checks complete, user-reported | Final connector sourcing and assembly notes |
| [08](08-programming-usb.md) | Programming USB | Electrical/high-speed/layout checks complete, user-reported | Final sourcing and assembly output data |
| [09](09-boot-recovery-reset.md) | Boot and recovery | Design checks closed under the completion report | Final sourcing and assembly drawing labels |
| [10](10-debug-uart.md) | Debug UART | Design checks closed under the completion report | Final sourcing and assembly drawing pin labels |
| [11](11-status-test-points.md) | Status and test access | Release scope frozen under the completion report | Include existing test access and population notes in drawings |

Optional indicators and post-assembly software/functional bring-up are not
new tasks in the current fabrication/assembly file-preparation scope.

## Locked high-speed routing requirements — verification complete, user-reported

The current official CM5 datasheet establishes two controlled-impedance
classes for the nine routed differential pairs:

- 90 ohms differential: PCIe TX, PCIe RX, PCIe reference clock, and
  programming USB 2.0 D+/D-.
- 100 ohms differential: MIPI0 data lanes 0-3 and MIPI0 clock.

The earlier 85-ohm PCIe project note is superseded. The following geometry/rule
observations are retained from the October 9 checkpoint and are superseded as
active checks by the October 14 high-speed completion report. Actual widths and gaps
have reportedly been calculated from the configured stackup, but they still
require JLCPCB confirmation. The October 9 audit confirms all nine pair objects. The highest-priority
`USB_DiffPair` rule is profile-driven at 90 ohms but scoped to `All`; confirm
and correct its effective scope, particularly for the 100-ohm MIPI pairs.
The lower-priority generic rule remains a placeholder.

## Historical PCB layout setup

The bullets below record the September setup. The current saved plane net
assignments are GND and `5V`; see the October 9 audit for current evidence.


- Working outline: approximately 100 mm x 60 mm; all 43 components are placed
  top-side and inside it. Mechanical fit and connector/retention checks remain.
- Stack: L1 `SIG 1`, L2 solid `GND`, L3 `PWR` intended as the main 5 V plane,
  and L4 `SIG 2`.
- General rules: 0.15 mm clearance, 0.20 mm minimum/0.25 mm preferred width,
  and 0.60 mm/0.30 mm through vias. Resolve the external note's 1.0 mm maximum
  versus the saved rule's 0.50 mm maximum.
- Keep CSI, PCIe, and USB on L1 over continuous L2 ground where practical.
  Avoid L4 for these pairs because its adjacent reference is the power plane.
- The reported PCB rail rename to `5V` is not present in the current saved net
  table, which still uses `NetC2_1`; reconcile it with schematic/documentation
  names before the next ECO.

## Working order

1. Finalize all component sourcing and record accepted substitutions.
2. Save the final consistent schematic, PCB, and BOM revision.
3. Generate Gerbers and NC Drill data, BOM, CPL, assembly drawings,
   fabrication/stackup notes, schematic PDF, and the retained DRC report.
4. Review exported geometry/drills and BOM/CPL quantities, designators,
   placement, side, rotation, polarity, and population notes.
5. Assemble the manufacturer handoff package using the supplier's required
   formats. The assembly provider has not been confirmed in this session.

If a sourcing change alters the circuit or layout, update the affected checks
and regenerate the outputs for the new revision. No exports were generated by
this documentation-only update.

## Status vocabulary

- **Confirmed:** explicitly locked in the current project documentation.
- **Planned:** required work whose exact implementation may still need review.
- **Open:** requires a design choice or external verification.
- **Done:** implemented in CAD and subsequently verified.
- **Complete, user-reported:** Bill reports the check complete; this documentation
  pass did not independently repeat the test or inspect the correction details.

## Session rule

After work on a subsystem, update its status, completed work, open questions,
and session notes. Record verified material decisions in
`Documentation/Journal.md` and keep the active summary in
`Documentation/documentation.md` synchronized.
