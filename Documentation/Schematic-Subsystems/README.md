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
| [02](02-main-5v-power.md) | Main 5 V supply | Validation open | Peak power budget; proposed Basic C4 |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Correction required | Recheck C8/C9; validate reset timing; buck is now U1 |
| [04](04-camera-power.md) | Camera power | Critical correction | Fix U3 pin mapping; add output capacitor; thermal review |
| [05](05-cm5-connectors.md) | CM5 connectors | Recovery verification open | SW now ECO-connected to CN1-93; verify access and mechanical fit |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | **High priority release blocker** | Resolve CN3 `-42-` part vs `-32-` footprint/STEP against drawings before fabrication or ordering |
| [07](07-csi2-camera.md) | CSI-2 camera | Power dependency open | Correct camera supply; FPC orientation and routing |
| [08](08-programming-usb.md) | Programming USB | Correction required | Recheck ground contacts under current designator; add ESD; review VBUS treatment |
| [09](09-boot-recovery-reset.md) | Boot and recovery | SW placed and ECO-connected | Validate footprint and test point; accessible placement/routing; recovery test |
| [10](10-debug-uart.md) | Debug UART | Schematic complete | Place accessible connector and label pin order |
| [11](11-status-test-points.md) | Status and test access | Rough draft | Select final indicators and test points |

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
6. Define outline, mounting/connector constraints, stackup and impedance rules;
   place critical power loops, decoupling, controls and remaining components.
7. Route and tune; run DRC, mechanical, fabrication-output and BOM/CPL reviews.
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
