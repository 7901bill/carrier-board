# Schematic Subsystems

Last updated: 2026-09-28

This folder is the detailed working record for Schematic V1 of the Wireless
Watchdog CM5 carrier board. Each file covers one independently reviewable
subsystem. `Documentation/Journal.md` is the source of truth for verified
decisions, while `Documentation/documentation.md` is the daily working summary
and active-blocker list.

## Schematic V1 objective

Schematic V1 completion is reopened. PCB import and a clean compile were
reported, but the saved-CAD review found electrical omissions and incorrect
LDO pin mapping. Correct and verify these before routing. The
[current design status](../documentation.md) contains the consolidated open
findings; the subsystem records below contain the supporting implementation
details.

## Progress dashboard

| File | Subsystem | Draft status | Principal remaining work |
|---|---|---|---|
| [01](01-power-input-usb-pd.md) | USB-C power input and PD | Validation open | Source/fuse budget; proposed Basic R1 |
| [02](02-main-5v-power.md) | Main 5 V supply | Validation open; placed | Reconcile main-rail/plane name; route converter loop; peak-power review |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Correction required; placed | Recheck C8/C9 before routing; route buck loop; validate reset timing |
| [04](04-camera-power.md) | Camera power | Critical correction | Fix U3 pin mapping; add output capacitor; thermal review |
| [05](05-cm5-connectors.md) | CM5 connectors | Placed; verification open | Verify alignment, retention, access, edge constraints, and mechanical fit |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | **High priority release blocker; placed** | Resolve CN3 identity; define/profile-link three pairs; route on L1/L2 |
| [07](07-csi2-camera.md) | CSI-2 camera | Power dependency open; placed | Correct camera supply; verify FPC orientation; define/profile-link five pairs |
| [08](08-programming-usb.md) | Programming USB | Correction required; placed | Recheck grounds; add ESD; define/profile-link USB pair; review VBUS |
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
require JLCPCB confirmation. The saved PCB contains no defined
differential-pair objects, the reported CSI class has no saved members, and
the generic 15 mil/10 mil rule is not linked to the profiles or approved for
routing.

## PCB layout setup

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

1. Fix U3 physical pin mapping and add the missing camera output capacitor.
2. Connect Hailo C8/C9 output pads and programming USB ground contacts.
3. Validate the placed recovery switch and resolve USB ESD/VBUS design requirements.
4. Resolve CN3's M.2 part/footprint/3D identity and verify mating,
   standoff, pad, and clearance geometry against manufacturer drawings before
   fabrication or connector procurement. Then close the power-budget, thermal,
   and reset-timing reviews and decide on the two proposed Basic substitutions
   without relaxing key requirements.
5. Audit ERC settings/electrical pin types/no-connects, compile, regenerate
   ECO, and explicitly inspect corrected PCB pad nets. Zero warnings alone
   is insufficient; `NetlistSinglePinNets=0` deserves particular review.
6. Reconcile and verify the saved plane/net/rule state, mechanical constraints,
   and fabrication capability. Define all nine pairs, populate the PCIe/MIPI/
   USB classes, and link their rules to the calculated impedance profiles.
7. Route converter/decoupling loops first, then high-speed and sensitive nets,
   ordinary signals, power and ground stitching. Run DRC, return-path,
   mechanical, silkscreen, fabrication-output and BOM/CPL reviews.
   Status LEDs remain optional, not a substitute for resolving these blockers.

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
