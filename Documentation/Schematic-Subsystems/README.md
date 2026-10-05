# Schematic Subsystems

Last updated: 2026-10-05

This folder is the detailed working record for Schematic V1 of the Wireless
Watchdog CM5 carrier board. Each file covers one independently reviewable
subsystem. `Documentation/Journal.md` is the source of truth for verified
decisions, while `Documentation/documentation.md` is the daily working summary
and active-blocker list.

## Current layout sprint

Routing is targeted for completion by 2026-10-06, with final cleanup and
sign-off checks targeted for the following work session. The top priority is
the complete high-speed differential-pair set. A direct check of the current
saved `Watchdog PCB.PcbDoc` on 2026-10-05 found zero saved differential-pair
objects, so pair creation and rule verification are part of the routing task.
Component placement may be adjusted as needed for the critical routes and must
receive a separate final review. DRC must be run during routing and again after
all routing, plane pours, and placement changes are complete.

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
| [05](05-cm5-connectors.md) | CM5 connectors | **Component/footprint verified; placed; ready to route** | Preserve verified 10164227-1001A1RLF parts; finish board-level alignment, access, and fit checks |
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

1. Define and verify all nine PCIe/MIPI/USB differential-pair objects, classes,
   impedance-linked rules, and skew constraints; then route the complete pair
   set as the first routing block.
2. Adjust placement where the critical escapes, return paths, decoupling,
   connector access, or mechanical clearance require it. Freeze and review
   placement after the high-speed paths work.
3. Re-verify the earlier U3, Hailo C8/C9, programming USB, recovery-switch,
   CN3, plane/net, and ECO findings before locking affected routes.
4. Finish converter and decoupling loops, remaining sensitive controls,
   ordinary signals, power distribution, and ground stitching.
5. Re-pour planes/polygons and run DRC iteratively. Finish with no unexplained
   violations or unrouted connections; review return paths and differential
   geometry rather than relying only on the violation count.
6. Complete placement/mechanical, silkscreen, ERC/ECO, BoM/CPL,
   fabrication-output, and drill-output reviews before release. Status LEDs
   remain optional and are not a substitute for resolving release blockers.

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
