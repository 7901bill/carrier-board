# Parts cost and schematic review — 2026-09-19

## Result and scope

Reviewed the four active SchDoc files, their placed component records, the
saved `Watchdog PCB.PcbDoc` component/pad/net records, PCB-transfer ECO log,
local libraries, subsystem notes, and relevant manufacturer datasheets.
There are **42 placed components / 27 distinct C-numbers**. Unused libraries,
history archives, and prototype software are not part of this PCB BOM.

This is a read-only design review: no schematic, library, or PCB corrections
have been applied. Altium ERC was not rerun. The saved PCB contains definite
connectivity problems; the earlier documentation's blanket completion claims
must not be treated as electrical sign-off.

## Basic substitutions

| Reference | Current part | Proposed Basic part | Electrical comparison |
|---|---|---|---|
| C4 | C466768, SANYEAR C0603X7R104K250NT | **C14663**, YAGEO CC0603KRX7R9BB104 | Both 100 nF, X7R, ±10%, 0603. Voltage rating increases from 25 V to 50 V. Already used at C3/C7. |
| R1 | C2770993, UNI-ROYAL CQ03WAJ0682T5E | **C23212**, UNI-ROYAL 0603WAF6801T5E | Both 6.8 kΩ, 100 mW, 75 V, ±100 ppm/°C, 0603, −55 to +155°C. Tolerance improves from ±5% to ±1%. |

R1's existing library describes an AEC-Q200 automotive-qualified resistor.
The proposed part is an electrical substitute for this consumer board, but
does not preserve that qualification. Keep the original if automotive
qualification is a requirement.

Primary sources: [existing C4](https://jlcpcb.com/partdetail/SANYEAR-C0603X7R104K250NT/C466768),
[Basic C14663](https://jlcpcb.com/partdetail/Yageo-CC0603KRX7R9BB104/C14663),
[existing R1](https://jlcpcb.com/partdetail/2909448-CQ03WAJ0682T5E/C2770993),
[Basic C23212](https://jlcpcb.com/partdetail/0603WAF6801T5E/C23212).
Basic labels and parameters were checked; the accessible C23212 page did not
expose a stock count. Recheck order availability when selecting the BOM.

For Economic assembly, removing two fee-bearing Extended types would save
approximately **$6.14 per order**, before discounts, provided neither is
already exempt as Preferred. Standard assembly charges feeder loading for
Basic parts too, so this saving does not apply in the same way. Reusing C14663
also removes one distinct BOM type. See [current JLCPCB pricing](https://jlcpcb.com/help/article/pcb-assembly-price)
and [Preferred-part policy](https://jlcpcb.com/help/article/pcb-assembly-faqs).

## Inventory and disposition

Basic/Extended means the label retrieved from JLCPCB's official page during
this review, not a guaranteed future quote. Unknown means the current JLCPCB
classification could not be verified; LCSC stock does not establish it.
No exact Basic substitute was verified for rows marked keep/unverified.

| C-number | References | Part/value | Classification / decision |
|---|---|---|---|
| C14663 | C3, C7 | 100 nF, 50 V, X7R, 10%, 0603 | Basic; keep, also use for C4 |
| C15849 | C1, C10, C15 | 1 µF, 50 V, X5R, 10%, 0603 | Basic; keep |
| C1671 | C11 | 47 pF, 50 V, C0G, 5%, 0603 | Basic; keep |
| C21120 | C12 | 220 nF, 25 V, X7R, 10%, 0603 | Basic; keep |
| C45783 | C2, C5, C6, C8, C9, C14, C16, C17 | 22 µF, 25 V, X5R, 20%, 0805 | Basic; keep; validate effective capacitance |
| C25803 | R4, R6, R8 | 100 kΩ, 1%, 100 mW, 0603 | Basic; keep |
| C23186 | R2, R3 | 5.1 kΩ, 1%, 100 mW, 0603 | Basic; keep |
| C466768 | C4 | 100 nF, 25 V, X7R, 10%, 0603 | Extended; proposed C14663 |
| C2770993 | R1 | 6.8 kΩ, 5%, 100 mW, 0603 | Extended; proposed C23212, qualification caveat above |
| C25818 | R5 | 453 kΩ, 1%, 100 mW, 0603 | Extended; keep exact divider value |
| C723484 | R7 | 22.1 kΩ, 0.1%, 25 ppm/°C, 0603 | Extended; no equally precise Basic verified |
| C54102278 | R9 | 5.49 kΩ, 1%, 100 mW, 0603 | Unknown; no matching Basic verified |
| C12447 | R10 | 40.2 kΩ, 1%, 100 mW, 0603 | Parameters verified; classification unresolved |
| C48543706 | C13 | 33 pF, 1%, 50 V, C0G, 0603 | Extended; do not silently substitute 5% tolerance |
| C151251 | D1 | Littelfuse SMBJ12A, SMB | Unknown; verify manufacturer surge ratings before any substitute |
| C354897 | F1 | Walter 1206T3A63V, 3 A, 63 V fuse | Extended; retain time-current/I²t/interrupt ratings |
| C42459160 | U2 | CH224A PD controller | Extended; keep |
| C5349327 | U5 | MP2329GG-Z main buck | Unknown; no equivalent Basic verified |
| C311983 | U3 | TPS54302DDCR Hailo buck | Extended; keep |
| C51118 | U7 | AP2112K-3.3TRG1 camera LDO | Extended; fix pin numbering first |
| C7461350 | U4 | 6.8 µH, 3.5 A rated, 5 A saturation | Extended; no matching Basic verified |
| C19268654 | U6 | 3.3 µH, 20 A rated, 32 A saturation | Extended; no matching Basic verified |
| C165948 | U1, USBC1 | TYPE-C-31-M-12 USB-C | Extended; no matching Basic verified |
| C6782225 | CN1, CN2 | Amphenol 10164227-1001A1RLF | Extended; preserve CM5 mating geometry |
| C601195 | CN3 | UMAX 91302-42-067RDM M.2 | Extended; preserve keying, height and land pattern |
| C5182313 | CN4 | Hirose FH55-22S-0.5SH FPC | Extended; preserve cable/contact orientation |
| C514175 | U8 | JST SM03B-GHS-TB(LF)(SN) | Extended; preserve selected GH mating cable |

Seven existing types were confirmed Basic. Sixteen were shown Extended, and
four classifications remain unverified. A search with no confirmed match is
not proof that no Basic alternative exists anywhere in the catalog.

Examples not approved as equivalent: a 33 pF ±5% part for C13's ±1%; a 22 kΩ
1% resistor for R7's 22.1 kΩ 0.1%; a smaller inductor without matching current
and saturation ratings; or an AMS1117-style LDO with different pinout,
dropout, capacitor requirements and package. These require design review.

## Corrections before routing

### 1. Camera LDO U7: incorrect physical pin assignments — critical

The AP2112K symbol labels pin 2 as EN, and the PCB matches that incorrect
numbering. The [Diodes datasheet, pages 1–2](https://www.diodes.com/assets/Datasheets/AP2112.pdf)
specifies the following SOT25 mapping:

| Physical pad | Correct function | Saved PCB connection | Required connection |
|---|---|---|---|
| 1 | VIN | Main 5 V | Main 5 V |
| 2 | GND | Main 5 V | GND |
| 3 | EN | GND | Main 5 V for always-on operation |
| 4 | NC | CN4 pin 22 | Unconnected |
| 5 | VOUT | No net | Camera 3.3 V / CN4 pin 22 |

The actual regulator ground would receive 5 V; its output would not power the
camera. Correct symbol pin designators/functions, check footprint numbering
against the package drawing, update placed instances, and regenerate the ECO.

The camera rail also has **no output capacitor** in the saved PCB. C15 is on
the input rail. Add the datasheet-required output capacitor at the corrected
VOUT-to-GND connection, with effective capacitance checked at operating bias.

### 2. Hailo output capacitors C8/C9: positive pads have no net — critical

The PCB Pads6 data and ECO log both show C8-2/C9-2 on GND but C8-1/C9-1
unconnected. Neither capacitor is on the Hailo output net (`NetC11_2`), which
joins U4-2, R8-2, C11-2 and the five CN3 power contacts.

Connect the capacitors' actual electrical pin ends to the Hailo output and
update PCB nets. The schematic's line visually passes near the symbols, but
the exported pad connectivity is decisive. The
[TI TPS54302 datasheet, Table 7-2](https://www.ti.com/lit/ds/symlink/tps54302.pdf)
uses 44 µF output capacitance as the 3.3 V starting point. Check DC-bias and
tolerance losses after restoring both connections.

U3 EN pin 5 being unconnected is **not** a finding: TI explicitly permits
floating EN to enable this device.

### 3. Programming USB-C USBC1: signal ground missing — critical

USBC1 pads `A1B12` and `B1A12` have no net. Shell/mounting pads 1–4 are on
GND, but those do not replace the USB cable's signal-ground contacts. Connect
both ground-pad groups to GND and regenerate the PCB ECO.

The D+/D− duplicated contacts and separate 5.1 kΩ CC resistors are present.
Programming VBUS contacts join each other but are isolated from main 5 V;
no direct back-power connection is present. There is no USB data ESD array
among the 42 components, despite documentation saying protection is drawn.
Resolve the protection requirement before routing the external USB port.

### 4. Recovery control absent — required for the intended workflow

CN1 pad 93 (`nRPIBOOT`) has no net. There is no recovery switch/jumper/test
point component in the active sheets or PCB inventory. Add an accessible
means to pull this signal to ground for forced USB boot/recovery. The
[CM5 datasheet](https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf)
documents this function and its internal pull-up. Leaving it floating supports
normal boot, but does not implement the planned recovery control.

Earlier journal/subsystem claims that recovery, programming protection and
all regulator support circuitry were implemented were too broad. This review
supersedes those claims based on actual CAD connectivity.

## Other concerns and items needing validation

- Camera LDO thermal margin remains unresolved. The recorded 300 mA case
  dissipates (5−3.3)×0.3 = 0.51 W; using the datasheet's 184°C/W figure gives
  about 94°C rise. At 40°C ambient that is about 134°C junction. Confirm the
  actual selected camera's maximum current and PCB thermal performance.
- Hailo PERST# is directly driven from CN2-9; there is no supply-good gating.
  Prove reset remains asserted until the Hailo rail is stable, including
  brownout/restart, before claiming sequencing is closed.
- With a 9 V/3 A source, input power is 27 W before losses. A 6.5 A-rated
  buck does not make a 5 V/6.5 A (32.5 W) system possible from that input.
  Complete the simultaneous CM5/Hailo/camera peak budget and fuse derating.
- CN3's footprint name contains `91302-32-067RDM`, while the selected part is
  `91302-42-067RDM`. This is a naming/mechanical-review flag, not proof of a
  wrong land pattern; compare both drawings and the 4.2 mm module height.
- Numeric pin names in several imported symbols obscure function errors.
  Preserve preferred visible names if desired, but verify physical numbers
  and electrical types against manufacturer pin tables.
- Project option `NetlistSinglePinNets=0` omits single-pin nets from transfer.
  Investigate why the capacitor/USB ground omissions did not generate useful
  warnings. Check ERC reporting and no-connect settings; zero messages do not
  establish correct pin mapping or electrical completeness.
- Many rail connections exported with generic names (`NetC2_1`, `NetC11_2`,
  `NetCN4_22`). Clear net names would make layout and bring-up review easier.
- Before routing, verify CM5 connector geometry, FPC contact orientation,
  module clearances, mounting, stackup and impedance rules. CM5 documentation
  specifies 90 Ω USB 2.0 and 100 Ω MIPI differential routing.

## Evidence trail

- `Hardware/Schematics & PCB/Power Rails.SchDoc`: U7 pin records, C8/C9 wires.
- `Hardware/Schematics & PCB/USBC_Protection.SchDoc`: USBC1 and its CC resistors.
- `Hardware/Schematics & PCB/Amphenol ICC.SchDoc`: CN1 pin 93 and JST UART.
- `Hardware/Schematics & PCB/M.2 & CSI2.SchDoc`: module and camera connectivity.
- `Hardware/Schematics & PCB/Watchdog PCB.PcbDoc`: 42 Components6 records,
  431 Pads6 records and 50 Nets6 records read directly from the saved file.
- `Hardware/Project Logs for Project Watchdog/Watchdog PCB PCB ECO 9-19-2026 5-55-16 PM.LOG`:
  independently corroborates the pad/net findings.
- Local MP2329 and CH224A PDFs were used to check the main buck and PD
  pin wiring; no analogous pin-assignment discrepancy was found in those
  connections during this review. This is not a full transient simulation,
  exhaustive footprint certification, or replacement for Altium DRC.

Recommended order: fix U7 and camera output capacitor; connect C8/C9;
connect USB ground; implement recovery; settle USB protection; then apply the
two proposed BOM substitutions and rerun compile/ECO before layout.
