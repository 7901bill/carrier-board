# 10 — Debug UART

Last updated: 2026-10-14

## Current release status — 2026-10-14

Bill reports routing, DRC, polygon pour, electrical testing, high-speed,
mechanical, and power verification complete. The earlier review findings in
this file are retained as historical records and are closed as active release
checklist blockers under that completion report. Specific correction details
and test results were not supplied; no independent CAD audit or test was
performed in this documentation pass.

Remaining work: Finalize UART-connector sourcing and carry pin labels and orientation into the assembly drawing.

Prepare the final fabrication/assembly package using the
[current checklist](../documentation.md). No schematic/PCB edits or manufacturing
exports were made in this pass. This update does not claim post-assembly
software or functional bring-up has occurred.

## Purpose

Provide a simple, independent serial-console path for observing CM5 bootloader,
kernel, and early userspace messages when USB software, Wi-Fi, or SSH is not
working.

## Historical status snapshot — superseded by the 2026-10-14 completion report

**Schematic complete and transferred to PCB.** The CM5 pins are routed to the
three-pin JST debug connector with TX, RX, and GND. The interface remains
3.3 V logic only.

## Confirmed design

- CM5 pin 55 `GPIO14/UART0_TX` connects to `DEBUG_UART_TX`.
- CM5 pin 51 `GPIO15/UART0_RX` connects to `DEBUG_UART_RX`.
- Interface: TX, RX, and GND on an accessible three-pin connector.
- Board connector: JST GH `SM03B-GHS-TB`, JLCPCB/LCSC `C514175`.
- Logic level: 3.3 V only.
- External adapter: a USB-to-UART adapter configured for 3.3 V signaling.
- The adapter's RX connects to carrier TX; adapter TX connects to carrier RX;
  grounds connect together.
- The UART header must not be used to power the carrier board.
- Recorded terminal format: 115200 baud, 8 data bits, no parity, 1 stop bit
  (`115200 8N1`).
- UART is for diagnosis; it does not replace USB eMMC flashing.

## Planned schematic content

- Three-pin connector with unmistakable TX, RX, and GND labels.
- Test points on UART signals if they do not reduce connector clarity.
- Pin-order marking suitable for silkscreen documentation later.

## Practical use

1. Power the carrier board normally.
2. Configure the USB-to-UART adapter for 3.3 V.
3. Connect adapter RX to carrier TX, adapter TX to carrier RX, and GND to GND.
4. Open the adapter's COM port at `115200 8N1`.
5. Power-cycle or reset the CM5 and capture all output from the beginning.

UART output can distinguish several failure classes: no power/no execution,
bootloader failure, missing boot files, kernel failure, Device Tree problems,
and userspace/service failures.

## Definition of done

- TX/RX direction is checked from both the CM5 and adapter perspectives.
- The connector pin order and voltage level are documented.
- The connector remains three-pin TX/RX/GND; no power pin is added.
- The signals are not connected to 5 V.
- The Linux image plan enables the appropriate serial console.
- The header remains physically accessible with the assembled CM5 installed.

## References

- `Documentation/Research MD/programming.md`.
- `Documentation/Research MD/I2C-UART-Explainer.md`.
- `Documentation/Research MD/CM5-Connector-Wiring-and-Bringup.md`.

## Session notes

- 2026-09-18: Initial UART draft created with operator-level connection and
  troubleshooting guidance.
- 2026-09-19: Completed the JST GH UART interface and transferred it to the
  PCB document. Accessibility and silkscreen pin labeling remain layout tasks.

- 2026-10-14: Updated current release status from Bill's completion report.
  Electrical, power, high-speed, mechanical, routing, DRC, and pour checks are
  closed as release checklist items. Only sourcing and manufacturing file
  preparation remain; older findings are preserved as superseded history.
