# Journal — Wireless Watchdog: CM5 Carrier Board

An ongoing, append-only log of notes from each work session. This is the
raw record of what was discussed — not the official spec (CLAUDE.md is the
current source of truth). Notes here get folded into CLAUDE.md the same day
they're written, then left alone as history. This file replaces the old
pattern of separate per-session log files (retired 2026-07-30) and the old
`documentation.md`/`status.md` files (also retired that day — both just
repeated what was already in CLAUDE.md with nothing new).

---

## 2026-07-30 — Power system correction + notes cleanup

Folded into CLAUDE.md the same day. See CLAUDE.md's "Session log" (Session
3) for the summary — corrected the power budget (~20-23W → ~13W), switched
the power negotiation chip (CH224K → CH224A) and voltage converter
(TPS54560 → MP2329GG-Z), and fixed an earlier mistake where the Hailo-8L's
power rail was briefly (and wrongly) called okay for a simple linear
regulator, before double-checking the datasheet confirmed the 6.6W/2A max
number already in CLAUDE.md was correct all along — it still needs a real
switching converter.

Also merged `documentation.md` and `status.md` into CLAUDE.md (nothing new
in either, both deleted) and switched from separate dated session-log files
to this one running Journal.md.

---

## 2026-08-01 — Timeline pushed back, assembly plan reversed, GitHub sync gap found

Folded into CLAUDE.md the same day. See CLAUDE.md's "Session log" (Session
4) for the summary. Raw notes below for details that didn't need to go into
the main file.

**Timeline pushed back.** The class instructor (Design Project III) will
review the board before it gets ordered. Class starts Sep 2; budgeting
about 2 weeks after that for review and fixes, so the board order moves
from Aug 29-31 to **around Sep 16**. The internal work deadlines (schematic
done Aug 9, layout done Aug 23) are staying the same on purpose — the extra
time is a buffer for review and fixes *after* layout is finished, not extra
time for the design work itself. Worked out what this means down the line:
bare circuit board back around Sep 23-25, assembled board back around
Sep 30-Oct 6 (parts take extra time to source), so a realistic
finished-and-working board is mid-to-late October, not the "late
September" target in CLAUDE.md's project summary. Flagged as an open,
unresolved tension with the recruiting deadline — the decision to push the
timeline back was made on purpose (a correct board matters more than
hitting the calendar date), but nobody has separately checked whether
mid-October still works for recruiting timing.

**Assembly plan reversed.** Decided to have JLCPCB machine-assemble
everything, including the connectors and other through-hole parts — no
hand-soldering step at all. This removes the risk of a bad hand-soldered
joint (bad connections, solder bridging between pins, parts standing up at
an angle) but does **not** remove the risk of a wrong part footprint — a
perfectly, professionally soldered wrong footprint is still a dead board.
Realized during the discussion that the original "hand-solder the
connectors" plan was never really doable anyway, given how tiny and
closely-spaced the DF40 connector's pins are — so this is more of a
correction than a real tradeoff. Still to check: does JLCPCB's assembly
quote need a separate line item for through-hole parts (DF40, M.2 socket,
maybe the USB-C connector) versus regular surface-mount assembly?

**USB-C connector added to the schematic, no exact part picked yet.** First
part placed in the power-input section. The protection chip is still the
oldest open item (unchanged since 2026-07-25) — noted that finishing the
protection chip, the USB-C connector part, and the Hailo-8L's local
converter should all happen *before* placing more parts in the power
section, to avoid designing around gaps.

**Simulation plan discussed and scoped down.** Decided against simulating
every part of the power system. LTspice (the simulation tool) is only used
for analog power behavior (voltage, current, stability) — not for checking
PCIe/camera signal quality, which is a separate, later step done in Altium
after the board layout exists. Two simulations picked as worth doing: the
MP2329 converter (9V→5V, which finishes checking an open question about the
resistor values, checks stability, and tests how it responds to a sudden
jump in power demand from CM5 idle to Hailo-8L full load) and the eventual
Hailo-8L local converter, once picked — both using the manufacturer's own
simulation models. Everything else (the CH224A pass-through chip, the
camera's linear regulator, the sequencing delay circuit) was judged not
worth simulating. Decided to finish picking the protection chip and local
converter first, then run both simulations back-to-back, rather than
simulating now and having to redo it later with different parts.

**GitHub sync gap found and fixed.** Partway through this session,
CLAUDE.md and Journal.md turned out to be 6 days out of date (still showing
"Last updated: 2026-07-25" even though Session 3 happened on 2026-07-30)
when re-uploaded to a claude.ai session for timeline planning — meaning an
earlier timeline discussion in that session was based on stale information
about the protection chip and converter status. Root cause: the GitHub
connection in a claude.ai Project is **read-only** — it only pulls files
from GitHub into the conversation, it can't push changes back out. There's
no way to push from the claude.ai web interface. Actual pushes require
Claude Code, plain git commands, or editing files directly on GitHub.com.
Added a rule to CLAUDE.md to push documentation to GitHub at the end of
every work session, instead of "whenever."

**Converting LCSC parts to Altium footprints, settled separately (not
folded into CLAUDE.md — this is a tooling choice, not a hardware
decision).** After a long research thread, decided: don't build a custom
converter, and don't bother with third-party tools from GitHub either
(like EasyEDALoader), since only about 2 parts (CH224A, the UMAX M.2
socket) are LCSC-only without an official design-software library entry
(name-brand library services cover everything else in the parts list by
part number). EasyEDA's own built-in Altium export feature (File → Export →
Altium Designer, confirmed free — the design tool itself has no paywalled
features, only cloud storage/support are paid) is the answer for those two
parts: export to a scratch project, then use `Design → Make Schematic/PCB
Library` in Altium. Checking the footprint against the real part (1:1
printout, comparing against the manufacturer's drawing) is still required
either way — this shortcut saves drawing time, not checking time, and
doesn't change the required fit-check for the CM5/M.2 connectors already
locked into CLAUDE.md.

---

## 2026-08-08 — Input protection stage closed out (TVS, eFuse, backup fuse)

Folded into CLAUDE.md the same day. See CLAUDE.md's "Session log" (Session
5) and "Decisions locked → Input protection" for the summary. Raw notes
below.

**Started from a basic question:** confirmed the input-protection stage
actually needs three separate parts — TVS, eFuse ("protection chip" in
earlier sessions' language), and a plain backup fuse — not just the
protection chip that was already being tracked. The backup fuse had never
actually made it onto the Outstanding list despite being named in
"Decisions locked" since Session 2; that gap is now closed.

**Read what was already on hand first.** No datasheet in `Datasheets/`
covers any of the three parts — confirmed by listing the folder (only
CM5, Hailo-8L, CH224A, and MP2329 datasheets exist). Pulled the CH224A and
MP2329 datasheets specifically to ground the voltage ceiling the
protection stage has to survive under: CH224A operates 4-30V input,
MP2329's absolute max input is 26V. That 26V number is the real ceiling —
whatever gets picked has to clamp/limit below it.

**Picked all three parts**, each backed by a real, stock-checked LCSC part
number:
- TVS: **SMBJ12A** (Littelfuse, LCSC C151251) over SMAJ12A (smaller
  package, less pulse-energy margin — not worth it given the connector
  gets plugged/unplugged a lot during bring-up).
- eFuse: **TPS25947** (LCSC C3662799) over TPS25940 (LCSC C2867756) — now
  that the design requests 9V not 20V, TPS25940's 18V rating isn't
  actually tight anymore, but TPS25947 still wins on lower on-resistance
  and real reverse-polarity blocking (back-to-back FETs) for similar cost.
- Backup fuse: **1206T3A63V** (Walter Elec, LCSC C354897, 3A/63V,
  fast-acting, 18.4k in stock) over a PTC resettable fuse — deliberately
  picked the one-time type instead of a self-healing PTC, because this
  fuse's whole job is to be the last-resort signal that the *active*
  protection (the eFuse) already failed. A PTC that quietly resets doesn't
  force that failure to actually get noticed and fixed.

**Found and fixed a topology mistake mid-discussion.** The first pass at
ordering the three parts was TVS → fuse → eFuse (TVS closest to the
connector, for best transient response). Caught during discussion: TVS
diodes have a known failure mode of failing *shorted* under an
over-energy event. If the fuse sits after the TVS, a shorted TVS shorts
VBUS straight to ground without the fuse — which only sees current in the
path toward the eFuse — ever tripping. Reordered to **fuse → TVS →
eFuse**, so the fuse also backs up a shorted TVS, not just a shorted
eFuse. Traded a few mm of extra trace length between the connector and
the TVS clamp point (marginally worse transient response) for that
coverage.

**Not yet resolved:** this reordering was reasoned from first principles,
not copied from a reference design — same caution that already applies to
the DF40 connector pin layout. Should be checked against the Spectre RM
DevBoard's power-input section (already on hand, has its own surge
protection/two-converter input stage) before being treated as final.

---

## 2026-08-09 — USB-C connector part picked (TYPE-C-31-M-12 / C165948)

Folded into CLAUDE.md the same day. See CLAUDE.md's "Session log" (Session
7) and "Decisions locked" for the summary. Raw notes below.

**Checked the new datasheet (`Datasheets/C165948.pdf`) against what the
connector actually needs to cover**, rather than just trusting the part
number: CC1/CC2 both present (required for CH224A's PD negotiation and
cable-orientation detection), VBUS/GND spread across multiple pins, and
DP1/DN1 + DP2/DN2 (a mirrored pair, no SuperSpeed pins) for the USB 2.0
debug/flashing line — matches the plan, since no USB 3.0 is used anywhere
on this board. SBU1/SBU2 are broken out on the part but not needed
(alt-mode/audio only) — left no-connect.

**Rating check:** part is rated 5A/20V. At the fixed 9V PD request and the
~13W power budget, actual draw is ~1.5A — well under the 5A rating, and
20V comfortably covers the 9V request. Not the bottleneck anywhere in the
chain.

**Mechanical finding, ties back to an open item:** the datasheet's bottom
view shows through-hole mounting legs (2× Ø0.50 holes), not a pure-SMT
shell. This directly answers part of the "confirm through-hole shell"
question that had been sitting open since Session 4 — now three parts
(DF40, M.2 socket, USB-C connector) are confirmed through-hole and need
the JLCPCB assembly-quote question resolved together. Also noted the part
is a board-edge-mount footprint (datasheet flags "PCB EDGE" against one
side) — true of any USB-C receptacle, not a special property of this part,
but worth remembering when placing it so the board outline lines up.

**Also revisited the power-distribution flow itself** while going through
this (not a new decision, just confirmed out loud): PD negotiation (CH224A)
happens first since it only passes voltage through unchanged and doesn't
protect anything; the fuse → TVS → eFuse protection stage sits after it,
sized against the actual negotiated 9V rather than an unknown worst-case
input; then the MP2329 converts down to the 5V rail. One flow, not
parallel paths.

Next: Bill starts the footprint for C165948. Then the Hailo-8L's local
converter (5V→3.3V, ≥2A) is the next open item — the last unpicked part in
the power chain.

---

## 2026-08-10 — Main power path and USB-C/CH224A schematic decisions

Started the power schematic from the USB-C input and resolved the naming and
topology before adding the downstream regulators.

**Fixed names.** The USB-C connector pins are named `VBUS`. The project net
before the fuse is `USB_VBUS`; the first fuse is component `F1`; the net after
F1 is `FUSED_VBUS`. FUSED_VBUS is a node, not another component. The CH224A
pin names remain exactly as in its datasheet: pin 1 is `VHV`, pin 8 is `VBUS`,
pin 6 is `CC2`, pin 7 is `CC1`, pin 4 is `DP`, and pin 5 is `DM`.

**Main power path:** USB-C VBUS pins → USB_VBUS → F1 → FUSED_VBUS. From
FUSED_VBUS, the CH224A VHV and VBUS pins are tied together, the TVS is a
shunt to ground, and the TPS25947 input is connected. The TPS25947 output
feeds the MP2329, whose output is `5V_MAIN`. The CH224A is a PD controller
on the VBUS node, not a series power converter or a separate PD output stage.

**CH224A configuration.** Use the CH224A/CH224Q reference schematic, not the
CH224D drawing. A 6.8k ohm resistor from CFG1 to ground requests 9V. CFG2
and CFG3 may remain floating when I2C control is not used. CC1 and CC2 stay
separate and connect to the corresponding USB-C pins. If BC1.2 detection is
not used, the CH224A DP and DM pins are no-connect; the connector USB 2.0
D+ and D- remain separate signals for the CM5 flashing/debug connection.

**C165948 pin mapping.** Tie A4/A9/B4/B9 together for VBUS; tie A1/A12/B1/B12
together for ground; tie A6/B6 for USB D+; and tie A7/B7 for USB D-. Leave
SBU1 (A8) and SBU2 (B8) no-connect. EH1 through EH4 are the connector
shell/mounting contacts and connect to ground for this schematic.

**Repository boundary.** The Altium directory was removed from the GitHub
documentation repository. The authoritative Altium project remains at
`C:\Users\Bill\Desktop\Bill's Folder\Altium\Project Watchdog` and is not
part of the Obsidian documentation checkout. GitHub authentication uses a
Personal Access Token in place of the account password; the token must not
be stored in project files or documentation.

Next: finish the power schematic from the locked FUSED_VBUS node through the
eFuse and MP2329, then verify the CH224A and MP2329 reference circuits before
adding the local Hailo and camera rails.

---

## 2026-08-16 — Programming plan, current datasheets, and documentation cleanup

Defined how the CM5 will be programmed and recovered. The carrier board does
not contain a separate firmware microcontroller: the CM5 is flashed through
USB boot mode, with the operating system and Watchdog software installed on
the CM5's onboard eMMC. The normal boot chain is CM5 ROM → EEPROM bootloader
→ eMMC → Linux → systemd → Watchdog services.

Created `Research MD/programming.md`, covering factory eMMC flashing with
`rpiboot`, normal SSH/Wi-Fi development, debug UART use, `nRPIBOOT` recovery,
reset/power control, and the PCB connections required for bring-up. The
programming design still needs a final choice between a dedicated USB
programming connector and a factory pogo/test-pad connection.

Re-read the current power-chain datasheets from the local Obsidian project
folder and copied all eight into `Documentation/Datasheets`, including the
current `TPS259470ARPWR` eFuse datasheet plus the capacitor and resistor
datasheets. The main documentation file was renamed from `CLAUDE.md` to
`documentation.md`.

Tomorrow: read `Research MD/programming.md`, then connect the CH224A PD request
node through the fuse, TVS, TPS259470ARPWR eFuse, and MP2329 buck converter
using the current datasheets as the source of truth. Verify every eFuse pin,
required passive, power net, and ground connection before continuing to the
local rails.
---

## 2026-09-03 — CM5 connector wiring and bring-up architecture

Clarified the physical and software architecture for the CM5 carrier board
before continuing the schematic. The CM5 is the complete computer: processor,
Linux, bootloader, onboard eMMC, Wi-Fi, Bluetooth, USB, UART, I2C, GPIO, and
PCIe are already inside the module. The carrier board does not need a separate
MCU or bridge chip for the planned design; it routes the required CM5 signals
through the two Amphenol 100-pin board-to-board connectors.

Locked the bring-up connections:

- One USB-C connector is dedicated to power. Its path is USB-C power input →
  protection/PD circuitry → 9V internal rail → 5V regulator → CM5 5V pins.
- A second USB-C connector is dedicated to CM5 programming and recovery. It
  routes USB 2.0 D+/D− to the CM5 and lets a host computer expose the CM5's
  onboard eMMC as USB mass storage for Raspberry Pi OS flashing.
- Pin 93 (`nRPIBOOT`) gets an accessible jumper or pushbutton to ground. This
  selects USB recovery mode during power-up; it does not provide power or do
  the flashing itself.
- A separate three-pin UART debug connector exposes TX, RX, and GND for an
  external 3.3V USB-to-UART adapter. UART is the early-boot diagnostic path;
  USB programming and UART are separate physical connections.

The full CM5 variant has onboard eMMC, so it does not need a physical SD-card
socket. Initial bring-up will be staged: power and CM5 only; USB flash; eMMC
boot; UART verification; Wi-Fi/SSH; camera; then Hailo-8L.

The communication roles were separated clearly. Camera video uses CSI-2;
camera configuration uses I2C; Hailo-8L communication uses PCIe; UART is for
the CM5 debug console; SPI is not currently needed. Hardware routing comes
first, but Linux Device Tree configuration, drivers, HailoRT, camera support,
and application software are still required after the board is assembled.

Before committing to the custom Hailo connection, the Hailo-8L currently
installed on the Raspberry Pi M.2 HAT+ should be tested on a Raspberry Pi 5.
That test verifies the module, power, PCIe communication, firmware, HailoRT,
and inference software. It does not fully validate the custom CM5 carrier
board's PCIe routing, because the Raspberry Pi AI Kit is commonly configured
for PCIe Gen 3 while the CM5 carrier board is designed for supported PCIe Gen
2 x1 operation.

Ethernet was considered and remains out of scope for this revision. Wi-Fi is
already built into the selected CM5, and Ethernet would require the MagJack,
ESD protection, four 100-ohm differential pairs, and additional board area.

---

## 2026-09-07 — Simplified first revision and connector schematic work

Removed the TPS25947 eFuse from the first board revision. The eFuse adds
design and bring-up complexity that is not justified for this iteration. The
previous eFuse selection and fuse → TVS → eFuse discussion remain above as
historical research; they no longer describe the active schematic.

The active schematic work is now the CM5 interface: the two 100-pin CM5
connectors and the M.2 socket for the Hailo-8L M+B-key card. This includes the
CM5-to-M.2 PCIe connection, the associated power and ground connections, and
the required control signals.

The board retains UART for early-boot debugging: CM5 pin 55 (`GPIO14` /
`UART0_TX`) connects to the debug adapter's RX input, and CM5 pin 51
(`GPIO15` / `UART0_RX`) connects to the adapter's TX output. CM5 pin 93
(`nRPIBOOT`) connects to an accessible jumper or pushbutton to ground for USB
recovery during power-up. CM5 pins 94 and 96 (`CC1` and `CC2`) remain
intentionally unconnected because the separate CH224A power-input circuit owns
its USB-C CC signals.

**Connector 1 GPIO reference completed.** CM5 pin 78 (`GPIO_VREF`) is tied to
the 3.3 V output net from pins 84 and 86. Pin 78 is a reference input, so this
sets the CM5 GPIO bank to 3.3 V signaling; it is not another 3.3 V supply
output. The next schematic task is the second 100-pin CM5 connector. Detailed
decisions about the remaining pin uses and wiring are deferred until that
sheet is in place.

---

## 2026-09-08 — Hailo-8L M.2 custom-symbol pinout locked

Verified the custom M.2 socket assignment against the Hailo-8L M.2 Key B+M
ET Module Data Sheet Rev. 4.0, section 2.2, and the current Raspberry Pi CM5
datasheet. The board uses the UMAX `91302-42-067RDM` 67-contact M-key socket
(LCSC `C601195`); the Hailo-8L B+M-key module fits this socket.

The custom symbol is grouped by function as follows:

- Power: pins 2, 4, 70, 72, and 74 are `3V3_HAILO`. Ground: pins 3, 27,
  33, 39, 45, 51, 57, 71, and 73 are `GND`.
- PCIe lane 0: pin 41 `PETn0` → CM5 pin 118 `PCIe_RX_N`; pin 43 `PETp0`
  → CM5 pin 116 `PCIe_RX_P`; pin 47 `PERn0` → CM5 pin 124 `PCIe_TX_N`;
  pin 49 `PERp0` → CM5 pin 122 `PCIe_TX_P`.
- Clock/control: pin 53 `REFCLKn` → CM5 pin 112 `PCIe_CLK_N`; pin 55
  `REFCLKp` → CM5 pin 110 `PCIe_CLK_P`; pin 50 `PERST#` → CM5 pin 109
  `PCIe_nRST`; pin 52 `CLKREQ#` → CM5 pin 102 `PCIe_CLK_nREQ`. Pin 54
  `PEWAKE#` can connect to CM5 pin 104 `PCIE_nWAKE`, but wake is currently
  unsupported by CM5 software and this signal may be left unconnected.
- PCIe lane 1 is deliberately unused because CM5 exposes only x1: pins 29
  `PETn1`, 31 `PETp1`, 35 `PERn1`, and 37 `PERp1` get explicit no-connects.
- Configuration contacts describe the module: pins 1, 21, and 75 are the
  module-grounded configuration bits and pin 69 is the module's NC
  configuration bit. They are detection signals, not extra power grounds;
  leave the carrier side open unless module-type detection is implemented.
- All remaining M-key socket contacts are unused for this Hailo module and
  get explicit no-connect markers. Pins 59–66 are absent because they form
  the M-key notch. The imported `C601195.SchLib` reports 68 pins, so its one
  extra pin must be checked against the connector drawing as a shield or
  mechanical contact before it is tied to ground.

**Power wiring still required.** `5V_MAIN` must feed a local 5 V-to-3.3 V
switching converter rated for at least 2 A, then the sequenced/switched
`3V3_HAILO` rail must connect to all five M.2 power pins. Raw 5 V must never
be connected to the Hailo M.2 socket. A separate camera branch is also still
unfinished: `5V_MAIN` must feed the selected camera regulator, and its
verified output rail(s) must connect to the CSI-2 camera connector power pins.
Confirm the exact camera module voltage requirements and connector pin map
before wiring that branch. Both local rails need nearby decoupling, test
points, and a common ground return.

> Later the same day, the component-selection portion of this open item was
> closed by the “Local Hailo and camera power rails selected” entry below.
> Physical schematic wiring and Hailo reset sequencing remain open.

The detailed pin table is recorded in
`Research MD/PCIe-x1-Differential-Pairs-Explainer.md`. No schematic-library
binary was modified during this documentation pass, and nothing was pushed.

---

## 2026-09-08 — Repository and design-state audit

**Status: Findings and proposed work; no architecture decision superseded.**

Reviewed the current documentation, Git state, Altium project membership, CAD
file inventory, and schematic previews. The detailed ranked findings are in
`Design-Audit-2026-09-08.md`.

The audit confirmed that the two CM5 connector-library corrections in the
root README remain the highest-priority release blockers. It also found that
there is no PCB layout document, both CM5 sheets remain largely unwired, the
tracked M.2 sheet is blank, and the new blank `Buck to M.2 & CSI.SchDoc` is
untracked and not included in the Altium project. The documented August layout
deadline and approximately September 16 order date are no longer credible.

The next decisions are to choose the Rev A scope, choose the authoritative
M.2/CSI sheet structure, finish the Hailo regulator and sequencing design,
define behavior before successful 9 V USB-PD negotiation, and select the exact
camera. Programming/recovery circuitry, mechanical constraints, PCB rules, and
manufacturing verification remain required before release.

No design choice was made on Bill's behalf. Existing local documentation,
library, history, and schematic changes were preserved. These documentation
edits are local only; nothing was committed or pushed.

---

## 2026-09-08 — Local Hailo and camera power rails selected

**Confirmed:** keep two separate local branches from `5V_MAIN`. The Hailo-8L
has large and fast load changes, so its 3.3 V switching rail must not be shared
directly with the camera. The rails still share the upstream 5 V source and
ground, but separate regulation, local decoupling, and careful layout reduce
the noise and voltage-transient coupling into the camera supply.

The Hailo branch now uses Texas Instruments **TPS54302DDCR**,
JLCPCB/LCSC **C311983**. It is a 4.5 V to 28 V input, adjustable 3 A,
400 kHz synchronous buck in TSOT-23-6 and provides margin above the Hailo
module's documented 3.3 V/2 A maximum. For a 3.3 V output, the TI datasheet
starting values are 100 kΩ output-to-FB, 22.1 kΩ FB-to-ground, 47 pF across
the upper feedback resistor, 6.8 µH inductance, at least 10 µF ceramic input
decoupling, 0.1 µF BOOT-to-SW, and 44 µF effective ceramic output capacitance.
Use an inductor rated for at least 3 A RMS and preferably above 4 A saturation.
The IC has internal soft-start but no power-good output, so stable-rail versus
PCIe-reset sequencing remains unresolved by the regulator alone.

The camera branch uses the previously selected genuine Diodes Incorporated
**AP2112K-3.3TRG1**, JLCPCB/LCSC **C51118**, a fixed 3.3 V/600 mA LDO in
SOT-25-5. Use at least 1 µF X5R/X7R capacitors directly at its input and
output. JLCPCB showed 64,064 units in stock during this check; C311983 also
had healthy distributor availability. Stock is a dated snapshot and must be
checked again when the assembly order is prepared.

**Confirmed CSI power correction:** the standard Raspberry Pi 22-pin CSI
connector has one 3.3 V supply input on pin 22. It does not require a separate
1.8 V supply from the carrier. Camera Module 3 generates its lower internal
rails on the camera PCB. Raspberry Pi budgets approximately 250 mA for a
camera, or about 0.825 W at 3.3 V. The AP2112 dissipates approximately 0.425 W
at that load from 5 V, so it needs useful copper area and should not be assumed
to deliver its full electrical 600 mA rating continuously from 5 V without a
thermal check.

**Superseded:** the older note requiring external 1.8 kΩ camera I2C pull-ups.
The current CM5 datasheet states that SCL0 and SDA0 already have internal
1.8 kΩ pull-ups to `CM5_3.3V`. Do not fit another pair by default because the
parallel result would be approximately 900 Ω.

Documentation only was changed. No Altium binary was edited, and no commit or
push was requested.

---

## 2026-09-09 — M.2 and local-power documentation normalized

Placed each current decision in its intended long-term reference:

- `Research MD/PCIe-x1-Differential-Pairs-Explainer.md` is the detailed source
  of truth for the Hailo M.2 socket pins, lane directions, CM5 mapping,
  no-connects, and power contacts.
- `Research MD/power-design-explainer.md` is the detailed source of truth for
  the separate `5V_MAIN` → TPS54302 → `3V3_HAILO` and `5V_MAIN` → AP2112K →
  `3V3_CAMERA` branches.
- `documentation.md` holds the current design summary and session index, while
  this journal preserves the chronological decisions and resume checkpoint.
- `Design-Audit-2026-09-08.md` now marks selection of the Hailo regulator as
  resolved after the audit without closing the remaining implementation work.

Next CAD work remains: draw and verify both regulator branches and their
required passives/decoupling, connect `3V3_HAILO` to M.2 pins 2, 4, 70, 72,
and 74, connect `3V3_CAMERA` to CSI pin 22, and ensure the Hailo rail is stable
before `PERST#` is released. No Altium binary was changed by this
documentation pass, and nothing was committed or pushed.

---

## 2026-09-18 — Schematic subsystem records and Rev A simplifications

**Confirmed:** Schematic V1 is now tracked in per-subsystem working notes under
`Documentation/Schematic-Subsystems/`. The standard Raspberry Pi Camera Module
3 is selected, using the normal Raspberry Pi 5-style camera cable and the
current 22-pin carrier connector.

The second programming/recovery USB-C port will reuse the existing HRO
`TYPE-C-31-M-12` receptacle (`C165948`) to reduce unique BOM items. Its circuit
remains electrically separate from the USB-PD power input: USB 2.0 device
wiring, appropriate CC termination, ESD protection, and safe VBUS sensing will
be used without tying host VBUS directly to `5V_MAIN`.

**Confirmed Rev A simplification:** omit both previously considered load
switches. TPS22965 (`C347592`) is not fitted on the Hailo branch, and TPS22918
(`C131941`) is not fitted on the camera branch. These are load switches, not
voltage regulators. TPS54302DDCR (`C311983`) remains the Hailo 5 V-to-3.3 V
buck regulator, and AP2112K-3.3TRG1 (`C51118`) remains the camera 5 V-to-3.3 V
LDO. Hailo power/reset timing will be verified using `3V3_HAILO` and `PERST#`
test access.

**Confirmed:** omit a CM5 `PWR_BUT` pushbutton from Rev A, retain the existing
`C15849` capacitor, leave M.2 `PEWAKE#` disconnected, and retain the three-pin
TX/RX/GND debug UART. A normally-open `nRPIBOOT` recovery pushbutton remains
required; its exact JLCPCB component is pending approval.

---

## 2026-09-18 — Hailo buck and camera LDO circuits completed

The local M.2/Hailo TPS54302 buck circuit and the CSI-2 camera AP2112 LDO
circuit are now drawn. The camera regulator remains Diodes Incorporated
`AP2112K-3.3TRG1` (JLCPCB/LCSC `C51118`), whose `-3.3` ordering suffix fixes
the output at 3.3 V without feedback resistors. `VIN` and `EN` share
`5V_MAIN`, GND is connected normally, NC is intentionally open, and VOUT
creates `3V3_CAMERA` for camera-connector pin 22.

Both AP2112 local capacitors use the existing `C15849` library part: 1 µF,
50 V, X5R, 0603. One is placed from VIN to GND and one from VOUT to GND. The
selected Arducam-class camera is expected to remain at or below approximately
300 mA. At the 300 mA maximum, the SOT25 LDO dissipates about 0.51 W and has
an estimated 94°C junction rise using the datasheet's 184°C/W value; useful
copper and prototype thermal testing remain required.

The Hailo output network uses the final selected sourcing substitutions:
6.8 µH inductor `C7461350`, 100 kΩ upper feedback resistor `C25803`, 22.1 kΩ
lower feedback resistor `C723484`, 47 pF feed-forward capacitor `C1671`, two
22 µF output capacitors `C45783`, and 100 nF bootstrap capacitor `C14663`.

---

## 2026-09-19 — M.2 and CSI-2 connector wiring completed

The Hailo M.2 socket is now connected to the CM5 connector through PCIe Gen 2
x1: lane 0 TX/RX, reference clock, `PERST#`, and `CLKREQ#`, together with all
required `3V3_HAILO` and ground contacts. Lane 1, `PEWAKE#`, the unused module
configuration contacts, CM5 `PCIE_nWAKE`, and CM5 `PCIE_PWR_EN` remain
unconnected for Rev A. The M.2 module supplies its required transmit-side AC
coupling, so no duplicate series capacitors were added on the carrier.

The 22-pin CSI connector is also fully connected: four MIPI data pairs, one
MIPI clock pair, `SCL0`/`SDA0`, `CAM_GPIO0`/`CAM_GPIO1`, `3V3_CAMERA`, and all
ground contacts. No additional I²C pull-ups were added because the CM5 owns
the camera-bus pull-ups. Review found and corrected misleading friendly labels
in the imported CM5 connector symbol: the authoritative mapping is CM5 pins
115/117 for MIPI0 lane 0, 121/123 for lane 1, 127/129 for clock, 133/135 for
lane 2, and 139/141 for lane 3.

Both interfaces are schematically complete. Controlled-impedance rules,
differential-pair routing, intra-pair length tuning, continuous reference-plane
verification, and final FPC cable-orientation review remain PCB-layout tasks.

---

## 2026-09-19 — CM5 connector numbering and base audit corrected

Both placed Amphenol connector instances now contain 100 unique physical pin
designators numbered 1–100. `CN1` represents CM5 logical pins 1–100 and `CN2`
represents logical pins 101–200; their component designators distinguish the
two identical footprints. The prior documentation claiming CN1 pins 3–6,
9–12, and 15–20 were grounds was incorrect. They are Ethernet, fan, LED,
sync, and EEPROM-control signals and remain unused for Rev A.

Verified all 21 CN1 grounds and all 30 CN2 grounds are connected. Unused GPIOs
have no-connect markers; pins 51/55 remain for UART and pins 97/100 for camera
control. Pins 21, 76, 92, 95, and 99 are unused and still need explicit
no-connect markers; pin 93 remains reserved for `nRPIBOOT` recovery.

A potential later status task is to add resistor-limited rail-presence LEDs
for `5V_MAIN`, `CM5_3.3V`, `3V3_HAILO`, and `3V3_CAMERA`, plus buffered CM5
power/activity indication only if it provides useful diagnostics.

---

## 2026-09-19 — Schematic V1 closed and transferred to PCB

Completed the programming USB-C, `nRPIBOOT` recovery control, three-pin JST GH
UART, remaining intentional no-connects, and final component placement on the
schematic sheets. The unavailable 3.3 µH main-rail inductor `C19268642` was
replaced by stocked SHOU HAN `CYA1250-3.3UH` (`C19268654`), rated 20 A with
32 A saturation current; its dedicated PCB footprint was imported.

The Altium project compile/ECO completed with no reported errors or warnings,
and all schematic components were imported into `Watchdog PCB.PcbDoc`. The
active phase is now PCB layout, beginning with board outline/constraints and
major component placement before detailed routing.
