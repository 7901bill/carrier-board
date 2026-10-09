# Schematic Subsystems

Last updated: 2026-10-09

This folder is the detailed working record for Schematic V1 of the Wireless
Watchdog CM5 carrier board. Each file covers one independently reviewable
subsystem. `Documentation/Journal.md` is the source of truth for verified
decisions, while `Documentation/documentation.md` is the daily working summary
and active-blocker list.

## Current PCB finishing work - 2026-10-09

Routing is substantially implemented in the saved PCB: all nine differential
pairs are defined and each member has top-layer tracks. Finish corner GND
vias, revise the board outline, and add/re-pour the required polygon copper.
Then refresh connectivity and resolve remaining DRC items in Altium. Final
routing, impedance, and release sign-off remain open.

The read-only saved-file audit found 85 connection records (83 GND and two
`NetCN1_78`), a broadly scoped 90-ohm differential rule, and unequal USB
track-only lengths. No DRC report was found, so a small remaining violation
count is not independently confirmed. See the [PCB audit](../PCB-Audit-2026-10-09.md) for evidence
and the limits of this inspection.


## Earlier schematic review findings

These are historical findings pending final re-verification, rather than a
new electrical audit. The October 9 PCB audit confirms routing progress but
does not close the earlier electrical or mechanical review items.


Schematic V1 completion is reopened. PCB import and a clean compile were
reported, but the saved-CAD review found electrical omissions and incorrect
LDO pin mapping. Re-verify affected items before release. The
[current design status](../documentation.md) contains the consolidated open
findings; the subsystem records below contain the supporting implementation
details.

## Progress dashboard

| File | Subsystem | Draft status | Principal remaining work |
|---|---|---|---|
| [01](01-power-input-usb-pd.md) | USB-C power input and PD | Validation open | Source/fuse budget; proposed Basic R1 |
| [02](02-main-5v-power.md) | Main 5 V supply | Validation open; placed | Reconcile main-rail/plane name; verify routed converter loop; peak-power review |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Correction required; placed | Recheck C8/C9; verify routed buck loop; validate reset timing |
| [04](04-camera-power.md) | Camera power | Critical correction | Fix U3 pin mapping; add output capacitor; thermal review |
| [05](05-cm5-connectors.md) | CM5 connectors | **Component/footprint verified; placed; routing substantially implemented** | Preserve verified 10164227-1001A1RLF parts; finish board-level alignment, access, and fit checks |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | **High priority release blocker; placed** | Resolve CN3 identity; verify three routed pairs and rule/profile scopes |
| [07](07-csi2-camera.md) | CSI-2 camera | Power dependency open; placed | Correct camera supply; verify FPC orientation; verify five routed pairs and 100-ohm rule scope |
| [08](08-programming-usb.md) | Programming USB | Correction required; placed | Recheck grounds; add ESD; verify routed USB pair, rule scope, and skew; review VBUS |
| [09](09-boot-recovery-reset.md) | Boot and recovery | SW placed and ECO-connected | Validate footprint and test point; accessible placement/routing; recovery test |
| [10](10-debug-uart.md) | Debug UART | Schematic complete | Place accessible connector and label pin order |
| [11](11-status-test-points.md) | Status and test access | Rough draft | Select final indicators and test points |

## Locked high-speed routing requirements

The current official CM5 datasheet establishes two controlled-impedance
classes for the nine routed differential pairs:

- 90 ohms differential: PCIe TX, PCIe RX, PCIe reference clock, and
  programming USB 2.0 D+/D-.
- 100 ohms differential: MIPI0 data lanes 0-3 and MIPI0 clock.

The earlier 85-ohm PCIe project note is superseded. Actual widths and gaps
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

1. Add corner GND vias and revise the board shape.
2. Add/re-pour polygon copper and review ground continuity and islands.
3. Refresh connectivity; inspect saved GND and `NetCN1_78` connections.
4. Verify differential profile/rule scopes and USB length/skew.
5. Resolve remaining DRC items and run final DRC after all layout changes.
6. Re-verify historical electrical/mechanical findings and complete final
   silkscreen, ERC/ECO, BOM/CPL, fabrication, and drill-output reviews.

## Status vocabulary

- **Confirmed:** explicitly locked in the current project documentation.
- **Planned:** required work whose exact implementation may still need review.
- **Open:** requires a design choice or external verification.
- **Done:** implemented in CAD and subsequently verified.

## Session rule

After work on a subsystem, update its status, completed work, open questions,
and session notes. Record verified material decisions in
`Documentation/Journal.md` and keep the active summary in
`Documentation/documentation.md` synchronized.
