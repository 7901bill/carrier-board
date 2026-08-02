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
