# 09 — Boot, Recovery, and Reset

Last updated: 2026-09-18

## Purpose

Allow the CM5 to boot normally from eMMC, enter USB recovery mode on demand,
and be reset or power-controlled during development and fault recovery.

## Current status

**Rough draft.** The eMMC boot/recovery method, `nRPIBOOT` assignment, and use
of a recovery pushbutton are confirmed. The exact pushbutton part awaits
approval. A separate CM5 power button is omitted from Rev A.

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
