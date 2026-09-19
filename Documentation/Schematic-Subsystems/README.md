# Schematic Subsystems

Last updated: 2026-09-19

This folder is the working record for Schematic V1 of the Wireless Watchdog
CM5 carrier board. Each file covers one independently reviewable subsystem.
The existing `Documentation/documentation.md` remains the current approved
architecture, and `Documentation/Journal.md` remains the chronological design
history.

## Schematic V1 objective

Schematic V1 is complete: every required subsystem is electrically drawn,
all required pins have an intentional connection or no-connect marker, selected
parts and values are recorded, and the design contains the hardware required to
power, flash, boot, recover, and debug the CM5. The clean compile/ECO and PCB
import were reported complete on 2026-09-19; PCB placement is next.

## Progress dashboard

| File | Subsystem | Draft status | Principal remaining work |
|---|---|---|---|
| [01](01-power-input-usb-pd.md) | USB-C power input and PD | Schematic complete | PCB placement and power-input review |
| [02](02-main-5v-power.md) | Main 5 V supply | Schematic complete | PCB placement and power-layout review |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Schematic complete | PCB placement and prototype timing validation |
| [04](04-camera-power.md) | Camera power | LDO drawn | Prototype thermal verification at camera load |
| [05](05-cm5-connectors.md) | CM5 connectors | Schematic complete | Mechanical placement and footprint review |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | Schematic complete | PCB impedance rules, routing, and length tuning |
| [07](07-csi2-camera.md) | CSI-2 camera | Schematic complete | FPC orientation check and PCB differential routing |
| [08](08-programming-usb.md) | Programming USB | Schematic complete | Place protection close to connector; route USB pair |
| [09](09-boot-recovery-reset.md) | Boot and recovery | Schematic complete | Place accessible recovery control/test access |
| [10](10-debug-uart.md) | Debug UART | Schematic complete | Place accessible connector and label pin order |
| [11](11-status-test-points.md) | Status and test access | Rough draft | Select final indicators and test points |

## Working order

1. Define the board outline, mounting constraints, and major connector/module placement.
2. Place the power stages and their critical loops/decoupling.
3. Select the final JLCPCB stackup and create PCIe/CSI/USB differential rules.
4. Place remaining support components and accessible controls/test points.
5. Route power, high-speed pairs, and remaining signals; then tune pairs.
6. Run PCB DRC, mechanical review, fabrication-output review, and BOM/CPL checks.

## Status vocabulary

- **Confirmed:** explicitly locked in the current project documentation.
- **Planned:** required work whose exact implementation may still need review.
- **Open:** requires a design choice or external verification.
- **Done:** implemented in CAD and subsequently verified.

## Session rule

After work on a subsystem, update its status, completed work, open questions,
and session notes. Material decisions must also be recorded in the project
journal following `Documentation/Agent-Decision-Workflow.md`.
