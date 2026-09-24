# Schematic Subsystems

Last updated: 2026-09-24

This folder is the working record for Schematic V1 of the Wireless Watchdog
CM5 carrier board. Each file covers one independently reviewable subsystem.
The existing `Documentation/documentation.md` remains the current approved
architecture, and `Documentation/Journal.md` remains the chronological design
history.

## Schematic V1 objective

Schematic V1 completion is reopened. PCB import and a clean compile were
reported, but the saved-CAD review found electrical omissions and incorrect
LDO pin mapping. Correct and verify these before routing. The
[review report](../Parts-and-Schematic-Review-2026-09-19.md) contains evidence,
the full parts inventory, and proposed cost reductions; none is implemented yet.

## Progress dashboard

| File | Subsystem | Draft status | Principal remaining work |
|---|---|---|---|
| [01](01-power-input-usb-pd.md) | USB-C power input and PD | Validation open | Source/fuse budget; proposed Basic R1 |
| [02](02-main-5v-power.md) | Main 5 V supply | Validation open | Peak power budget; proposed Basic C4 |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Correction required | Connect C8/C9; validate reset timing |
| [04](04-camera-power.md) | Camera power | Critical correction | Fix U7 pin mapping; add output capacitor; thermal review |
| [05](05-cm5-connectors.md) | CM5 connectors | Recovery incomplete | Connect CN1-93 control; mechanical review |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | **High priority release blocker** | Resolve CN3 `-42-` part vs `-32-` footprint/STEP against drawings before fabrication or ordering; power/reset dependencies |
| [07](07-csi2-camera.md) | CSI-2 camera | Power dependency open | Correct camera supply; FPC orientation and routing |
| [08](08-programming-usb.md) | Programming USB | Correction required | Ground cable contacts; add ESD; review VBUS treatment |
| [09](09-boot-recovery-reset.md) | Boot and recovery | Unfinished; C455280 selected | Verify footprint; wire button from CN1-93 to GND; add test point; ECO/layout/test |
| [10](10-debug-uart.md) | Debug UART | Schematic complete | Place accessible connector and label pin order |
| [11](11-status-test-points.md) | Status and test access | Rough draft | Select final indicators and test points |

## Working order

1. Fix U7 physical pin mapping and add the missing camera output capacitor.
2. Connect Hailo C8/C9 output pads and programming USB ground contacts.
3. Implement recovery control and resolve USB ESD/VBUS design requirements.
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
and session notes. Material decisions must also be recorded in the project
journal following `Documentation/Agent-Decision-Workflow.md`.
