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
