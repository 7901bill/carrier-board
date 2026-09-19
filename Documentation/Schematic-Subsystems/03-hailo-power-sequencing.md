# 03 — Hailo Power and Reset Sequencing

Last updated: 2026-09-19

## Purpose

Generate the dedicated Hailo-8L 3.3 V rail and ensure that the module remains
in reset until its supply is stable.

## Current status

**Schematic complete and transferred to PCB.** The TPS54302 circuit is drawn,
its final sourced passives are recorded, and `3V3_HAILO` reaches all five M.2
power contacts. Reset behavior and electrical/thermal performance remain
prototype-validation items.

## Confirmed design

- Regulator: TI `TPS54302DDCR`, LCSC `C311983`.
- Input: `5V_MAIN`.
- Output: `3V3_HAILO`.
- The Hailo-8L maximum documented load is 2 A at 3.3 V/6.6 W.
- Raw 5 V must never be connected to the Hailo M.2 power contacts.
- The Hailo rail is separate from the camera 3.3 V rail.
- The TPS54302 is an adjustable 3 A, 400 kHz synchronous buck with internal
  soft-start but no power-good output.
- Datasheet starting values recorded by the project are:
  - 100 kΩ from output to FB;
  - 22.1 kΩ from FB to ground;
  - 47 pF across the upper feedback resistor;
  - 6.8 µH inductor;
  - at least 10 µF ceramic input decoupling;
  - 0.1 µF from BOOT to SW;
  - 44 µF effective ceramic output capacitance.
- The inductor must support at least 3 A RMS and preferably more than 4 A
  saturation current.
- Final selected passives are:
  - 6.8 µH molded inductor `C7461350`, 3.5 A rated and 5 A saturation;
  - 100 kΩ upper feedback resistor `C25803`;
  - 22.1 kΩ lower feedback resistor `C723484`;
  - 47 pF C0G feed-forward capacitor `C1671`;
  - two 22 µF output capacitors `C45783`;
  - 100 nF bootstrap capacitor `C14663`.
- `3V3_HAILO` must be stable before M.2 `PERST#` is released.

## Completed schematic content

- Complete TPS54302 circuit and datasheet-required passives.
- Local bulk and high-frequency decoupling at the M.2 socket.
- Regulator enable and CM5-controlled reset connections; no separate load
  switch.
- Connection to all five M.2 power contacts.

## Verification remaining

- Confirm useful test access for `5V_MAIN`, `3V3_HAILO`, reset, and ground.
- Compile and run ERC after the remaining schematic subsystems are complete.
- Measure startup and confirm `PCIe_nRST` remains asserted until
  `3V3_HAILO` is stable.
- Verify ripple, load transient response, inductor temperature, and effective
  ceramic capacitance on the prototype.

## Load-switch decision

- **Omitted from Rev A:** `TPS22965`, LCSC `C347592`.
- TPS22965 is a load switch, not a step-down regulator. It would only add
  independent rail isolation, slew control, or power cycling.
- `TPS54302DDCR` (`C311983`) remains the required 5 V-to-3.3 V buck regulator.
- Rev A relies on the TPS54302's 5 ms soft-start and the CM5-controlled
  `PCIe_nRST`/M.2 `PERST#` connection. Their relative timing will be measured
  during bring-up.

## Definition of done

- The regulator is fully drawn and configured for 3.3 V.
- All five M.2 power contacts receive `3V3_HAILO`.
- Input/output capacitance is verified at operating bias.
- Inductor current and thermal margins are verified.
- The sequencing circuit provides a documented guarantee that power is stable
  before reset release.
- Enable, reset, and rail behavior can be measured during bring-up.

## References

- `Documentation/Research MD/power-design-explainer.md`.
- `Documentation/Research MD/PCIe-x1-Differential-Pairs-Explainer.md`.
- TPS54302 and Hailo-8L datasheets.

## Session notes

- 2026-09-18: Initial subsystem draft created from confirmed project records.
- 2026-09-19: Completed the sourced TPS54302 circuit and all M.2 power
  connections; reset-timing and prototype validation remain open.
