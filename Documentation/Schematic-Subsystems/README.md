# Schematic Subsystems

Last updated: 2026-09-19

This folder is the working record for Schematic V1 of the Wireless Watchdog
CM5 carrier board. Each file covers one independently reviewable subsystem.
The existing `Documentation/documentation.md` remains the current approved
architecture, and `Documentation/Journal.md` remains the chronological design
history.

## Schematic V1 objective

Schematic V1 is complete when every required subsystem is electrically drawn,
all required pins have an intentional connection or no-connect marker, selected
parts and values are recorded, and the design contains the hardware required to
power, flash, boot, recover, and debug the CM5. Formal ERC correction and PCB
layout follow this first complete schematic pass.

## Progress dashboard

| File | Subsystem | Draft status | Principal remaining work |
|---|---|---|---|
| [01](01-power-input-usb-pd.md) | USB-C power input and PD | Rough draft | Final protection and failed-negotiation behavior |
| [02](02-main-5v-power.md) | Main 5 V supply | Rough draft | Verify support parts and worst-case budget |
| [03](03-hailo-power-sequencing.md) | Hailo power and sequencing | Buck drawn | Verify reset timing and run power/ERC review |
| [04](04-camera-power.md) | Camera power | LDO drawn | Prototype thermal verification at camera load |
| [05](05-cm5-connectors.md) | CM5 connectors | In progress | Complete remaining base wiring and verify footprint pin maps |
| [06](06-m2-hailo-pcie.md) | M.2 Hailo/PCIe | Schematic complete | PCB impedance rules, routing, and length tuning |
| [07](07-csi2-camera.md) | CSI-2 camera | Schematic complete | FPC orientation check and PCB differential routing |
| [08](08-programming-usb.md) | Programming USB | Rough draft | Draw reference-based USB recovery circuit |
| [09](09-boot-recovery-reset.md) | Boot and recovery | Rough draft | Finalize nRPIBOOT pushbutton; PWR_BUT omitted |
| [10](10-debug-uart.md) | Debug UART | Rough draft | Draw header and validate console setup |
| [11](11-status-test-points.md) | Status and test access | Rough draft | Select final indicators and test points |

## Working order

1. Complete the remaining CM5 base power, ground, and unused-pin treatment.
2. Complete programming USB, boot/recovery controls, and UART.
3. Close Hailo reset-release timing and remaining power-input questions.
4. Add status indicators and bring-up test points.
5. Perform a whole-schematic consistency pass, then compile and run ERC.
6. Select the final JLCPCB stackup and create PCIe/CSI differential rules.
7. Transfer to PCB, place, route, tune, and run fabrication checks.

## Status vocabulary

- **Confirmed:** explicitly locked in the current project documentation.
- **Planned:** required work whose exact implementation may still need review.
- **Open:** requires a design choice or external verification.
- **Done:** implemented in CAD and subsequently verified.

## Session rule

After work on a subsystem, update its status, completed work, open questions,
and session notes. Material decisions must also be recorded in the project
journal following `Documentation/Agent-Decision-Workflow.md`.
