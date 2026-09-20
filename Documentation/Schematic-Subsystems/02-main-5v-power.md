# 02 — Main 5 V Power Supply

Last updated: 2026-09-19

## Open review actions — 2026-09-19

- Open: the 6.5 A converter rating is not the available system budget.
  A 5 V/6.5 A load is 32.5 W, exceeding the 27 W input before losses.
  Close peak/continuous load and fuse/thermal margins with subsystem 01.
- Proposed only: C4 `C466768` → Basic `C14663` (already C3/C7):
  100 nF, X7R, ±10%, 0603; voltage rating increases from 25 V to 50 V.
- Optional clarity improvement: label main 5 V (`NetC2_1`), Hailo output
  (`NetC11_2`) and camera output (`NetCN4_22`) with their intended rail names.

These actions are not implemented. Evidence and parts caveats are in the
[review report](../Parts-and-Schematic-Review-2026-09-19.md).

## Subsystem purpose

Convert the negotiated 9 V input into the shared `5V_MAIN` rail used by the
CM5 and the local Hailo and camera regulators.

## Current status

**Schematic complete and transferred to PCB.** The converter and target rail
are confirmed. Peak-load, transient, efficiency, and thermal verification
remain prototype-validation tasks.

## Confirmed design

- Converter: MPS `MP2329GG-Z`, LCSC `C5349327`.
- Input: negotiated 9 V from the USB-PD input section.
- Output: `5V_MAIN`.
- The device is rated for 6.5 A continuous and 7.5 A peak, subject to the
  complete design and thermal conditions.
- Recorded datasheet starting values for 5 V are:
  - upper feedback resistor: 40.2 kΩ, `C12447`;
  - lower feedback resistor: 5.49 kΩ, `C54102278`;
  - feed-forward capacitor: 33 pF, `C48543706`;
  - inductor: 3.3 µH, `C19268654` (`CYA1250-3.3UH`, 20 A rated,
    32 A saturation). This stocked replacement supersedes `C19268642`.
- The CAD sheet also uses 22 µF/25 V capacitors `C45783`, 220 nF/25 V
  capacitor `C21120`, and 100 nF/25 V capacitor `C466768` in the power section.
- MP2329 input qualification is implemented with 453 kΩ `C25818` and 100 kΩ
  `C25803`, targeting an approximately 7.5 V startup threshold.
- `5V_MAIN` directly supplies the CM5 and feeds separate local regulators for
  the Hailo and camera rails.

## Confirmed load facts

- The earlier approximately 13 W system estimate is based mainly on typical
  loading and is not sufficient by itself for final component ratings.
- The Hailo-8L alone can require as much as 6.6 W/2 A at 3.3 V.
- Final verification must consider simultaneous peak load, startup, conversion
  loss, thermal derating, charger capability, and cable capability.

## Planned schematic content

- Complete MP2329 reference circuit.
- Input/output ceramic capacitors with voltage and effective-capacitance margin.
- Feedback and feed-forward network.
- Inductor with suitable RMS and saturation-current ratings.
- Enable and startup behavior coordinated with the USB-PD section.
- `5V_MAIN`, input, switch-node, and ground test access where safe.
- Clear net connections to the CM5 and both local 3.3 V branches.

## Definition of done

- All component values are checked against the current MP2329 datasheet.
- A defensible worst-case power budget is recorded.
- Inductor and capacitors meet electrical and thermal margins.
- The expected startup state is defined for 5 V input and successful 9 V PD.
- Every CM5 5 V input is supplied as required by the CM5 reference design.

## References

- `Documentation/documentation.md`, Power architecture.
- `Documentation/Research MD/power-design-explainer.md`.
- MP2329 datasheet in `Documentation/Datasheets/`.

## Session notes

- 2026-09-18: Initial subsystem draft created from confirmed project records.
- 2026-09-19: Replaced unavailable `C19268642` with stocked `C19268654` and
  imported its dedicated footprint into the PCB project.
