# 09 — Boot, Recovery, and Reset

Last updated: 2026-09-20

## Purpose

Allow the CM5 to boot normally from eMMC, enter USB recovery mode on demand,
and be reset or power-controlled during development and fault recovery.

## Current status

**Button circuit still unfinished (confirmed 2026-09-20).** The selected
switch is XUNPU `TS-1088R-02026`, JLCPCB/LCSC `C455280`. The last saved-CAD
review found CN1-93 (`nRPIBOOT`) without a PCB net and no recovery
switch/jumper/test point in the active component inventory.
Add the planned accessible normally-open momentary switch to GND and verify
its physical pad nets after ECO. The internal pull-up supports normal boot
when released; leaving the pin open does not provide user recovery access.
Earlier completion notes are superseded by the
[saved-CAD review](../Parts-and-Schematic-Review-2026-09-19.md).
A separate CM5 power button remains intentionally omitted from Rev A.

## Confirmed boot model

- The selected CM5 variant contains eMMC; no microSD connector is required.
- Normal boot sequence is CM5 boot ROM → EEPROM bootloader → eMMC boot files →
  Linux → `systemd` → Watchdog services.
- Hailo and camera initialization occurs after Linux begins booting; neither
  device replaces the CM5 boot process.
- CM5 pin 93 is `nRPIBOOT`.
- Holding `nRPIBOOT` low during power-up enables USB boot/recovery.
- Releasing `nRPIBOOT` and power-cycling returns the CM5 to normal eMMC boot.
- Recovery control will be a normally-open momentary pushbutton from
  `nRPIBOOT` to ground. The CM5 provides the signal's internal pull-up.
- The recovery control must remain physically accessible with the CM5 installed.
- Selected switch: XUNPU `TS-1088R-02026`, JLCPCB/LCSC `C455280`;
  normally-open momentary SPST, two-terminal SMT, 3.9 x 2.93 mm body,
  2 mm height, 2.6 N operating force, 50 mA / 12 V rating, 100,000 cycles.
  JLCPCB lists it as Extended. This replaces TE `3-1437565-0` / `C86463`.
  See [JLCPCB listing](https://jlcpcb.com/partdetail/Xunpu-TS_1088R02026/C455280).
- Remaining work: verify the exact datasheet, symbol-to-pad mapping and
  footprint; wire one terminal to CN1-93 and the other to GND; add the
  labeled test point; transfer via ECO; place accessibly and route; verify
  released/pressed states and normal/USB boot. Selection is not completion.

## CM5 power-control decision

- CM5 pin 92 `PWR_BUT` replicates the Raspberry Pi 5 power button. A brief
  pull to ground requests wake or shutdown; holding it low for more than five
  seconds forces shutdown.
- CM5 pin 99 `PMIC_ENABLE` places the CM5 into its lowest power-down state when
  pulled low. Raspberry Pi recommends doing this only after OS shutdown.
- **Rev A decision:** do not fit a `PWR_BUT` pushbutton. Normal operation uses
  applied main power and software shutdown rather than a local power button.
- `PMIC_ENABLE` is not a reset button and will not receive a user pushbutton.

## Confirmed recovery workflow

1. Hold `nRPIBOOT` low.
2. Apply adequate power through the main power input.
3. Connect the programming USB-C connector to the development computer.
4. Run Raspberry Pi `rpiboot`/the supported mass-storage utility.
5. Write the operating-system image to the exposed eMMC.
6. Stop the flashing process and release `nRPIBOOT`.
7. Power-cycle and boot from eMMC.

## Planned schematic content

- Accessible pushbutton control for `nRPIBOOT`, plus a labeled test point.
- Defined normal and recovery states following the official CM5 reference.
- Clearly named recovery, reset/control, and ground test points.
- Status indication where it does not load a boot-critical signal.

## First software-image plan

- Raspberry Pi OS 64-bit.
- Correct CM5 bootloader and Device Tree configuration.
- Camera and PCIe interfaces enabled.
- Hailo runtime/driver support.
- Wi-Fi and SSH configuration.
- Serial console enabled for the debug UART.
- A diagnostic boot stage before the complete Watchdog application.

## Definition of done

- Normal eMMC boot and forced USB recovery are both supported by hardware.
- Recovery controls are accessible and clearly labeled.
- Programming USB and UART remain usable when Linux or Wi-Fi is unavailable.
- A bring-up operator can determine which control state produces normal boot
  versus recovery boot without modifying the board.

## References

- `Documentation/Research MD/programming.md`.
- Current Raspberry Pi Compute Module flashing documentation.
- Current CM5 datasheet and official CM5 IO reference design.

## Session notes

- 2026-09-18: Initial boot/recovery draft created with additional explanation
  because this is a high-priority learning and bring-up area.
- 2026-09-19: Earlier completion claim was superseded by the saved-CAD review;
  recovery control was absent.
- 2026-09-20: Selected C455280 in place of C86463. Bill explicitly confirmed
  the button remains unfinished; implementation and verification are open.
