# CLAUDE.md — Wireless Watchdog: CM5 Carrier Board

Last updated: 2026-08-01

## Session log — read this first

A running summary, newest entry at the bottom. This lets you pick up where
the last work session left off without reading the whole file.

- **Session 1 (2026-07-22):** Picked the main parts — CM5 (4GB RAM, 32GB
  storage, WiFi built in), Hailo-8L AI chip on an M.2 slot (connects at PCIe
  Gen2 x1 speed, same setup Raspberry Pi's own AI Kit uses), a camera
  connector with its own control wires, a two-stage power system (main power
  chip → local regulators near each part), and a debug port (CM5 only,
  3 pins, 3.3V signal level). Confirmed CM5 over CM4 and a custom board over
  Raspberry Pi's AI HAT+ (reasons below under "Decisions locked"). Looked
  into pricing for the Hailo-8L (Raspberry Pi's AI Kit version is
  discontinued, third-party versions run $120-180, avoid international
  shipping forwarders). Next step: build the power budget spreadsheet
  (still not done), then order the CM5, Hailo-8L, and camera.
- **Session 2 (2026-07-25):** Redrew the "Main Compute Module" diagram
  (`Graphical/Carrier Board PCB.canvas`) as a left-to-right tree (board →
  root → CM5/Hailo-8L/Camera → their connector/power/signal-quality details),
  and turned each detail line into a checkbox. Then researched and picked
  connectors for all three parts (see "Hardware updates & discoveries"
  below). Also researched the power-input chain (power negotiation chip,
  protection chip, voltage converter, surge protector), the debug/control
  wiring, and the local regulators — and found that the Hailo-8L actually
  draws much more power than first assumed (6.6W / 2A, not "a few hundred
  mA"). Found three open questions: does the protection chip have enough
  voltage headroom, what part handles the Hailo-8L's power converter, and
  which exact camera model to buy. Next step: close those three questions,
  finish the power budget, then order parts.
- **Session 3 (2026-07-30):** Finished the power budget spreadsheet
  (closing a task from Session 1) — the real total power draw is **about
  13W with safety margin**, much lower than the ~20-23W first guessed. That
  old number came from a review of the CM5 running overclocked with a
  cooling fan, which doesn't apply here. Switched the power-negotiation chip
  (CH224K → CH224A, better voltage safety margin) and the main voltage
  converter (TPS54560 → MP2329GG-Z), and now request 9V from the charger
  instead of 20V since the corrected power number doesn't need it. Also
  double-checked the Hailo-8L's power needs directly in its datasheet
  (`Datasheets/4746521.pdf`, section 3.1): confirmed max draw is 6.6W/2A at
  full load, with typical use around 1.4-1.9W. This confirms a simple linear
  regulator (LDO) is not a good fit for that rail — it needs a real
  switching converter rated for at least 2A. Also cleaned up the project
  notes: deleted two files (`documentation.md`, `status.md`) that just
  repeated what's already in this file, and switched from separate
  per-session log files to one running `Journal.md`. Next step: pick the
  ≥2A converter for the Hailo-8L's power rail (oldest open item), pick the
  protection-chip part, and confirm the MP2329's resistor values against
  what's actually in stock.
- **Session 4 (2026-08-01):** Two planning decisions this session, no new
  parts picked. (1) **Timeline pushed back about 2.5 weeks** to add a
  professor review before ordering the board (class starts Sep 2, review +
  fixes budgeted about 2 weeks after that) — see "Timeline" below for exact
  dates. The internal work deadlines (schematic done Aug 9, layout done
  Aug 23) stay the same; the extra time is added *after* layout is done, not
  mixed into the design work itself. (2) **Changed the assembly plan**: the
  whole board — including connectors and other through-hole parts — will
  now be machine-assembled by JLCPCB, with no hand-soldering step. This
  fixes an earlier plan that was never really realistic: the 100-pin,
  very-fine-pitch DF40 connector was never something to hand-solder safely.
  Still open: confirm with JLCPCB whether through-hole parts (the DF40
  connector, M.2 socket, USB-C connector) need a separate line item on the
  assembly quote. The USB-C connector was added to the schematic this
  session, but the exact part number isn't picked yet. Next step (same as
  before): pick the protection chip, pick the USB-C connector part, pick the
  Hailo-8L power converter, confirm the MP2329's resistor values are in
  stock.

## Project summary

Summer 2026 goal: design a custom **CM5 carrier board in Altium** (PCB
design software) that turns the Watchdog device into a **standalone smart
camera** — CM5 computer + Hailo-8L AI chip + camera, all on one custom
4-layer circuit board. The AI processing moves onto the device itself; the
old setup (PC server + video streaming pipeline) goes away. The alarm system
stays the same: detection → WiFi message → ESP32 gateway → radio signal →
alarm unit.

Why the deadline matters: **fall new-grad job recruiting.** The board needs
to be built, working, and documented as a finished portfolio piece in time
for that.

> **Timeline note (2026-08-01):** the target finish date has slipped from
> "late September" to a more realistic **mid-to-late October**, because of
> the Session 4 decision to add a professor review before ordering the
> board, plus normal manufacturing and part-sourcing time. This is a
> deliberate tradeoff (a correct board matters more than the calendar date),
> but it's worth double-checking that mid-October still works for the
> recruiting timeline. Full breakdown under "Timeline" below.

The design approach was checked twice against "is this just reinventing the
Raspberry Pi AI HAT+" and against a full rethink from scratch (see
"Decisions locked" and "Architecture reasoning" below) — both times the
answer was to keep building the custom board. The AI HAT+ only solves the
AI-chip connector problem and still needs a full separate Raspberry Pi 5
underneath it. Custom CM5 boards are also still rare (the CM5 only came out
in late 2024), unlike the older, well-documented CM4.

## Locked components

- **CM5**: 4GB RAM, 32GB built-in storage, WiFi. (A 2GB version was
  considered when 4GB prices spiked due to a shortage — the real price
  difference between 2GB and 4GB is only about $25; resellers were just
  marking up the sold-out 4GB version by over $100. The 4GB version avoids
  running out of memory during heavy tasks like compiling OpenCV from
  source code — the 2GB version would work for normal use but was riskier
  for development.)
- **Hailo-8L**, an AI chip rated at 13 TOPS (trillion operations per
  second — a measure of AI processing speed), on an M.2 B+M connector
  (2242 size), rated for PCIe Gen3 x2 (a faster connection standard than
  what we'll actually use).
  - Raspberry Pi no longer sells this chip by itself (their AI Kit is
    discontinued, and they've said they won't sell the Hailo-8L without
    their own HAT board). Buy it from third-party sellers (Waveshare,
    Yahboom on Amazon) instead, or use the Hailo-8 (a similar but
    higher-performance chip, 26 TOPS, similar price) if the 8L isn't
    available. Avoid international shipping-forwarder websites — one $99
    part quoted came out to $154 after forwarder shipping fees.
  - **The CM5 only exposes a PCIe Gen2 x1 connection** externally (its
    internal chip can technically go faster, but Raspberry Pi limits the
    external connector to Gen2 for signal-quality reasons). The Hailo-8L
    will automatically negotiate down to this slower connection — this is
    completely normal and is the exact same setup Raspberry Pi's own AI Kit
    uses (Pi 5 + Hailo-8L), which is proven to work. This only reduces data
    transfer speed, not the chip's actual AI processing power (13 TOPS
    stays the same). The data going back and forth (detection boxes and
    labels, not raw video) is small enough that the slower connection is
    still plenty fast.
  - The M.2 connector footprint on the board should support the full B+M
    spec (both sets of PCIe wire pairs, since that's what the standard
    connector part provides), but only one set (lane 0) actually needs to
    be wired up — the second set can be left unconnected.
- **Camera**: connects over CSI-2 (a 4-wire-pair video interface, plus a
  clock wire, wire lengths need to be closely matched) to the CM5. Also
  needs a **separate 2-wire control connection (I2C)** for camera settings
  (exposure, gain, resolution) — easy to miss since it's separate from the
  video wires. Raspberry Pi's own camera modules (Camera Module 3 / IMX708)
  don't include the small "pull-up" resistors these control wires need, so
  the carrier board has to add them — standard value is **1.8k ohms to
  3.3V** on each of the two control wires. Since the camera module has none
  of its own, there's no risk of doubling up — but this should be
  re-confirmed once the exact camera model is picked.

## Decisions locked

- **A custom carrier board, not a HAT (add-on board), not a full computer
  board.** The CM5 handles the hardest parts (the dense chip packaging,
  memory, WiFi certification); everything else is built around it.
- **CM5 over CM4** (re-confirmed). They use the same connector family but
  **different pin arrangements (~23 pins differ)** — so none of the
  connector wiring work carries over between them. The CM4 is also slower
  (CPU, RAM, storage) and has no USB 3.0, with the same PCIe speed limit as
  the CM5 anyway — so switching would give up performance for no real
  benefit. CM4 boards are also extremely common already (lots of tutorials
  and off-the-shelf kits), while CM5 boards are still rare, which works
  against the goal of building something that isn't already a solved
  problem.
- **Altium** (the PCB design software, available through an NYU license).
  Existing reference designs (in KiCad, a different tool) get imported just
  to study, not copied directly.
- **4 layers**, JLCPCB's controlled-impedance stackup (a specific
  layer/material setup that keeps signal quality consistent), **full
  JLCPCB machine assembly for every part — including connectors and other
  through-hole parts** (changed 2026-08-01; no hand-soldering planned at
  all). This replaces the earlier plan below, which wasn't realistic anyway
  for a connector with 100 tiny 0.4mm-spaced pins.
  **Still open:** confirm with JLCPCB whether through-hole parts (DF40
  connector, M.2 socket, USB-C connector if it has a through-hole shell)
  need a separate line item from the regular surface-mount assembly.
  <br>*(Replaced 2026-08-01, kept here for history: the old plan was
  "machine-assemble the small surface-mount parts; hand-solder the
  connectors and through-hole parts.")*
- **No screen output.** No HDMI port (cut to reduce design complexity —
  two fewer sets of matched wire pairs to route). Remote login over WiFi is
  the main way to use the board (free — WiFi is already built into the CM5).
  The debug port is the required backup for troubleshooting boot problems.
- **No Ethernet port, no extra USB ports, no audio.**
- **Power-over-Ethernet cut**, pushed to a future revision (that revision
  would replace the power-input section but keep the voltage converter).
- **Battery ruled out** — a 15-25W continuous power draw would drain any
  reasonable battery pack in a few hours. The device stays plugged into the
  wall, full stop.
- **Power input: USB-C with Power Delivery (a standard that lets a device
  ask a charger for a specific voltage).** The negotiation chip (**CH224A**,
  LCSC part C42459160, confirmed in stock — set by resistor values on its
  control pins, no software needed, works with PD3.0/2.0 and Quick Charge)
  requests **9V** (not 20V — the corrected power number doesn't need the
  higher voltage), set with a single 6.8k-ohm resistor. Chose CH224A over
  CH224K because CH224A's power-input pins can handle up to 32V versus
  CH224K's 13.5V, giving more safety margin for the protection stage. Two
  extra pins (CFG2/CFG3) are wired to the CM5's control bus so the software
  can check which voltage actually got negotiated and monitor live current
  during testing — this comes essentially for free with the resistor-based
  setup. The VBUS pin must be connected directly to the VHV pin per the
  reference design (easy to forget when drawing the schematic). No special
  "e-marker" chip needed since we're well under the 20V/60W threshold that
  requires one. The CH224A only negotiates and passes voltage through
  unchanged — it doesn't convert or regulate voltage itself; its "power
  good" pin just reports whether negotiation succeeded. The board refuses
  to run on plain 5V-only chargers (avoids weird brownout bugs). Backup
  plan if this gets complicated: switch to a plain USB-C connector with a
  standard 5.1V/5A charger, no negotiation.
  **USB-C connector: added to the schematic 2026-08-01, exact part number
  still not picked** (see "Outstanding" below).
  Voltage converter: **MP2329GG-Z** (from MPS, LCSC part C5349327,
  confirmed in stock) — accepts 4.5-24V in, outputs an adjustable 0.6-13V,
  rated for 6.5A continuous / 7.5A peak, small QFN-11 package. This is the
  only part in the chain that actually converts power — it steps the
  negotiated 9V down to the 5V/5A main power rail (the "backbone" that
  feeds everything else). The 6.5A rating is a ceiling; actual draw is
  around 2.6A given the corrected ~13W budget — well under half its
  capacity. The 5V-output resistor values (from the datasheet): R1 =
  40.2k ohms, R2 = 5.49k ohms, C4 = 33pF, inductor = 3.3µH — still need to
  confirm these exact parts are currently in stock (open item).
- **Input protection, regardless of connector choice:** a surge protector
  on the power line, plus a protection chip (an electronic "smart fuse"
  that blocks overvoltage, limits inrush current, and shuts off on a
  short circuit), plus a plain backup fuse. Surge protector: **USBLC6-2SC6**
  (protects the power line and the two data lines, LCSC part C7519, a
  common basic part). Protection chip candidate: **TPS25940** (LCSC part
  C2867756) — **flagged: only rated for 18V input, and the charger could in
  theory negotiate up to 20V**, so this part is technically out of margin.
  **TPS25947** (rated to 23V) is the safer choice, but its stock wasn't
  confirmed yet — check before finalizing the parts list. Note: since we're
  now only requesting 9V (not 20V), TPS25940's 18V rating actually has real
  safety margin on this specific design, even though it's tight against
  what USB-C PD could theoretically request in general — worth reconsidering
  once stock on TPS25947 is checked, rather than automatically ruling
  TPS25940 out.
- **Handling weak chargers:** the negotiation chip's status output lights
  an LED at minimum (so you can see if a weak charger is connected);
  optionally also wired to a CM5 input pin so software can check the
  wattage. No automatic power-limiting based on this in the first version.
- **CM5 version: with built-in storage** (flashed once over USB using a
  jumper wire trick called nRPIBOOT). Decided against the microSD-card
  version — that would add a connector and a removable part that could fail,
  for a device that's supposed to be a sealed, finished unit. The small cost
  savings weren't worth it this late in the schedule.

## Power architecture

Power budget (corrected 2026-07-30 — replaces the earlier ~20-23W estimate,
which came from a review of the CM5 running overclocked with active cooling,
which doesn't apply to this project):

| Component | Power |
|---|---|
| CM5 (normal speed, typical concurrent workload) | ~7.5W |
| Hailo-8L (running AI detection) | ~2.5W |
| Camera (IMX708 sensor) | <1W |
| Other stuff (status LEDs, backup clock chip) | ~0.5W |
| **Raw total** | **~11.5W** |
| **With 15% safety margin** | **~13W** |

Note: the ~2.5W Hailo-8L number above is a rough estimate for typical use,
not from the datasheet — the actual datasheet (`Datasheets/4746521.pdf`,
section 3.1) lists the max power draw as **6.6W/2A at full load**, with
typical benchmark tests around 1.4-1.9W. The local voltage regulator for
that chip's power rail has to be sized for the 6.6W/2A worst case, not the
rough typical-use estimate — see below.

Even a basic 5V/3A USB-C connection (no negotiation needed, 15W total) would
almost cover the ~13W total, but the safety margin would be thin (~2W),
which is why we're keeping the smarter negotiation setup instead of
dropping it for simplicity.

```
USB-C power in ──→ CH224A (asks for 9V, passes it straight through — no conversion)
               ──→ [protection chip + surge protector + fuse — part not picked yet]
               ──→ MP2329 voltage converter (drops 9V to 5V; current rises to match load, ~95% efficient)
               ──→ 5V/5A main power rail (a shared bus, not a fixed split)
                    ├──→ CM5 (uses 5V directly; its own internal power chip handles further conversion)
                    ├──→ local converter (5V→3.3V, ≥2A) → Hailo-8L M.2 slot
                    └──→ local linear regulator (5V→3.3V, maybe 1.8V) → Camera
```

Voltage and current trade off against each other at roughly constant power
through the converter stage (power = volts × amps, at ~90-95% efficiency) —
requesting a higher voltage from the charger doesn't change how much total
power the board actually uses. It just changes the voltage/current split of
delivering that same power through a USB-C cable, which usually has a
current limit of about 3A unless it's a special higher-rated cable.

Two stages: negotiation chip → one shared 5V/5A power rail → separate local
regulators at each part that needs a different voltage. This is a standard,
proven pattern, chosen instead of trying to generate every needed voltage
straight off the main converter:

- The CM5 uses 5V directly through its connector (its own internal power
  chip handles further conversion to whatever its processor/memory need —
  that's not something we have to design).
- M.2 slot: a local 3.3V regulator near the Hailo-8L connector. **Confirmed
  the Hailo-8L can draw up to 6.6W / 2A at 3.3V (1.5W typical)** — from the
  chip's own datasheet (`Datasheets/4746521.pdf`), much higher than the
  "few hundred mA" first assumed. This rules out a simple linear regulator
  here (it would waste about 3.4W as heat at max load) — needs a real
  switching converter rated for ≥2A; a specific in-stock part hasn't been
  picked yet, still an open item. When picking one, prefer a well-known
  brand (TI or MPS) over a lesser-known part that does the same job — same
  price and stock availability, but much better design-software library
  support.
- Camera: a local 3.3V (and possibly 1.8V — check once the camera model is
  picked) regulator near the connector. Draw is well under 500mA, so a
  simple linear regulator works fine: **AP2112K-3.3** (rated 600mA, LCSC
  part C51118, well-stocked) is the confirmed choice.

Why use local regulators instead of one big one: shorter wire runs to each
part (less voltage loss, cleaner power), each rail can be tested/tuned on
its own, and a problem on one rail doesn't take down the whole board.

Also still needs to be figured out:
- **Power-up sequencing** (a delay circuit or a switch chip on each power
  rail) — for example, the 3.3V rail on the M.2 slot needs to be stable
  *before* the reset signal to the Hailo-8L is released.
- **Per-rail power switches**, specifically to support the planned bring-up
  process: power on one section at a time (empty board → CM5 installed →
  debug console working → the rest of the parts), checking each step before
  turning on anything expensive. Confirmed candidates: **TPS22965** (6A,
  LCSC C347592) for the M.2/Hailo-8L rail, **TPS22918** (2A, LCSC C131941)
  for the smaller camera rail.

## Debug / bring-up

- **The debug port only works with the CM5.** Neither the Hailo-8L nor the
  camera produces any boot-up messages of its own — the Hailo-8L is
  controlled over PCIe by software (HailoRT) running on the CM5, and it has
  no operating system of its own; the camera is a simple sensor with
  nothing to report. This one debug port, wired straight to the CM5's
  connector pins, is the only way to see what's happening on the board.
- Header: a plain 3-pin (transmit, receive, ground) 2.54mm-spacing
  through-hole pin header (a basic, common part, LCSC/JLCPCB part C49257).
  Connect an external USB-to-serial adapter, and it **must be set to 3.3V
  logic level, not 5V** — 5V will damage the pins. Common adapter chips
  (CP2102 or FT232RL) usually have a 3.3V/5V switch — **several ship with
  the switch defaulted to 5V, so always check the switch position before
  the first connection**, don't just trust the printed label. Connect the
  adapter's transmit wire to the board's receive pin and vice versa (this
  is the standard, required wiring for this kind of connection). Terminal
  settings: 115200 baud rate, 8 data bits, no parity, 1 stop bit — use
  PuTTY on Windows, or `screen`/`minicom` on Git Bash/WSL (Linux-style
  terminal tools).
- This only lets you *watch* what's happening — it can't be used to flash
  new software. Flashing the CM5's built-in storage uses a separate method
  (USB port + the nRPIBOOT jumper wire, already covered above).

## How each part gets "programmed" (the mental model)

- **CM5**: has real permanent storage built in, gets flashed once over USB
  using the nRPIBOOT jumper. After that, it boots its own operating system
  on its own like a normal computer.
- **Hailo-8L**: has no permanent storage and no operating system. An AI
  model (for example YOLOv8n, an object-detection model) gets converted on
  a separate computer using Hailo's compiler tool into a `.hef` file, which
  gets copied onto the CM5 like any normal file, and then loaded onto the
  Hailo-8L chip over the PCIe connection every time the board powers on.
  Nothing stays saved on the chip itself between power cycles — this is
  completely normal for this type of AI/graphics accelerator chip.
- **Camera**: no storage, nothing to flash. The CM5 sets it up live over the
  control wires every time it starts (exposure, resolution, video format),
  and the video data streams over the CSI connection in real time.

## Physics notes agreed on

- Voltage converters trade voltage for current at (roughly) constant total
  power. A "buck" converter steps voltage down and current up; a "boost"
  converter does the opposite. **Total watts out can never be more than
  watts in — always.** A weak charger can't be forced to output more power
  than it's actually able to supply.
- With Power Delivery, the *charger* does any voltage boosting on its side
  of the cable — the board itself only ever steps voltage **down**. One
  conversion stage, one direction.

## Simulation plan (added 2026-08-01)

LTspice (a circuit simulation tool) only covers analog power behavior —
voltage, current, ripple, loop stability, and how the circuit responds to
sudden changes in load. It does **not** cover PCIe or CSI-2 signal
quality — that's a separate, later step done in Altium after the board
layout exists.

Only two simulations are planned, not a simulation of every part:

- **Skip:** the CH224A (it's just resistor-set pass-through, nothing
  changes over time to simulate), the camera's linear regulator (a simple,
  well-understood part), and the sequencing delay circuit (simple math from
  the datasheet is enough).
- **Simulate: the MP2329 converter (9V→5V main rail).** The highest-value
  simulation — it closes an open question (confirming the resistor values
  actually produce exactly 5.0V), checks that the circuit stays stable, and
  tests how the rail responds to a sudden jump in load (from the CM5 idling
  to the Hailo-8L at full power, roughly 1.5W→6.6W almost instantly) to
  check the voltage doesn't dip low enough to cause a brownout. Use MPS's
  own simulation model for this part, not a generic stand-in.
- **Simulate: the Hailo-8L's local converter**, once it's picked — same
  kind of test, same reasoning. The candidate parts (TI/MPS brands) publish
  their own simulation models too.

Plan: finish picking the protection chip and the Hailo-8L's converter
*before* running either simulation, so both simulations happen back-to-back
with the real parts' models instead of simulating once now and having to
redo it later with different parts.

## Subsystem risk list

- 🔴 **Power system** — highest risk (a bad power design causes bugs that
  look like software problems), but also Bill's strongest area (from LED
  driver design experience). Budget for the worst case first.
- 🔴 **DF40 connector pair** — highest consequence if wrong: a wrong
  footprint or pin arrangement means a dead, unfixable board. The pin
  layout is **copied exactly** from the official CM5 reference board, never
  guessed or redesigned. Managed by process: only use verified connector
  footprints, double-check against the manufacturer's drawing and the CM5's
  official mechanical spec, and do a 1:1 printed paper fit-check with a real
  CM5 before ordering the board. Full machine assembly (see "Decisions
  locked") removes the risk of a bad hand-solder joint on this connector,
  but does **not** remove the risk of a wrong footprint or pin layout — the
  paper fit-check is still required no matter who solders it.
- 🟡 **PCIe connection to the M.2 slot** — the trickiest new skill on this
  project. Full wire list: 2 pairs for data (transmit and receive), 1 pair
  for the shared clock, plus 2 single control wires, plus power/ground (8
  signal wires total). Plan: set up the board's layer stack and design
  rules *first*, then route the wires. Usually fails "soft" (falls back to
  the slower expected speed) rather than failing completely.
- 🟡 **Camera connection (CSI-2)** — 4 data wire pairs plus a clock pair,
  lengths closely matched, plus the separate 2-wire control connection.
  Same care needed as the PCIe wiring above.
- 🟢 **USB 2.0 + flashing port** — one easy-to-route wire pair plus the
  nRPIBOOT jumper. Copy the reference design directly.
- 🟢 **Basic extras** — debug port, per-rail status LEDs, backup clock chip
  + coin-cell battery, fan connector (speed-control wire + transistor).
  Cheap and useful for testing, but the first things cut if the schedule
  gets tight: backup clock chip and fan.

## Reference designs on hand

- **CM5 IO Board** (official Raspberry Pi reference design, in KiCad —
  imported into Altium for study): the source of truth for the connector
  pin layout, power sequencing, and protection design. Never invent a pin
  mapping — always copy this one.
- **Raspberry Pi M.2 HAT+** (official, published schematic): a good worked
  example of the M.2 slot wiring on its own, including the 3.3V setup and
  how a single-lane connection can plug into a wider-spec M.2 socket (same
  situation as our Hailo-8L link speed).
- **Spectre RM DevBoard** (belongs to the project's outside reviewer, not
  Bill's design — a different chip, 6 layers): worth studying for its power
  input section (higher voltage input, surge protection, two converters)
  and its standard 6-layer layer stack. The reviewer looks over the layout
  in week 5.5 (see "Timeline" below for updated dates).
- **Raspberry Pi AI HAT+ / AI Kit**: uses the same family of AI chip, useful
  specifically as a reference for the PCIe-to-Hailo wiring, but NOT a
  template for the rest of the board — it only solves the AI-chip connector
  problem, needs a full separate Raspberry Pi 5 underneath it for power and
  everything else, and solders the AI chip permanently instead of using a
  removable slot like this project does.

## Timeline

**Revised 2026-08-01 (Session 4).** The internal work deadlines are
unchanged from the original plan below — schematic finished by Aug 9,
layout finished by Aug 23. What's new is a **professor review step added
between "layout finished" and "order the board"**: class starts Sep 2,
review + any fixes budgeted about 2 weeks after that, pushing the board
order to **around Sep 16** (was Aug 29-31). This is a deliberate tradeoff —
spending extra calendar time to reduce the risk of ordering a wrong board,
on an expensive, fully-machine-assembled design — not slower design work.
The original internal deadlines should **not** relax just because there's
more time downstream.

Result: bare circuit board back around Sep 23-25, assembled board back
around Sep 30-Oct 6 (parts sourcing adds lead time), then testing/bring-up
after that. Realistic finished, working board: **mid-to-late October**, not
the original "late September" target (see the note under Project Summary
above) — this is a real, unresolved tension against the recruiting
deadline, worth revisiting.

Original 6-week plan (the dates below are the internal work deadlines;
everything from the board order onward is replaced by the paragraph above):

- **Week 1 (Jul 20-26):** Block diagram + power budget spreadsheet. Study
  the CM5 datasheet and reference board schematic. Pick key parts (power
  chip, converter, protection chip, connectors). **Order the CM5, Hailo-8L,
  and camera now** (they take time to ship). ✅ Done — all three ordered
  and in transit as of Session 4, the one deadline in this plan that didn't
  depend on schematic progress.
- **Weeks 2-3 (Jul 27-Aug 9):** Full schematic. Order: power section →
  main connectors → PCIe/M.2 → camera → USB → extras. Use only verified,
  checked connector footprints.
  Deadline: schematic review done by Aug 9, or cut the backup clock chip
  and fan to stay on schedule.
- **Weeks 3-5 (Aug 10-23):** Layout. Order: layer stack + design rules →
  connector/module placement → power section → high-speed wiring → the
  rest. Do the 1:1 paper fit-check here.
- **Professor review window (Sep 2 → ~Sep 16):** New in Session 4. Hand off
  the design (finished wiring, clean design-rule check, a short list of
  what to focus on — the connector wiring and power system are the top
  priorities) to the reviewer, then apply any fixes.
- **~Sep 16:** Order the board — design files, boards, stencil, and full
  assembly (surface-mount + through-hole).
- **~Sep 23-25:** Bare circuit board arrives from JLCPCB (standard turn
  time).
- **~Sep 30-Oct 6:** Assembled board arrives (parts sourcing adds lead
  time).
- **Bring-up (right after assembly arrives):** power on one section at a
  time — empty board → CM5 installed → debug console working → rest of the
  parts. The software side is already proven to work, so any problem found
  here is a hardware issue, not a software one.
- **Parallel work (any weekend, ongoing):** run the Hailo-8L on the
  existing Raspberry Pi 5 (using a PCIe adapter cable) — compile YOLOv8n,
  connect it to the existing WiFi→ESP32 alarm path, measure real
  frames-per-second. This proves out the software side separately from the
  hardware, so bring-up in October only has to debug hardware.

## Outstanding / carried over

- **Change the WiFi router password** — has been open since May, back when
  the code repository was public.
- `wireless_detection_rpi.py` (old detection script) is broken — doesn't
  matter if the move to a standalone board goes through, since the
  Raspberry Pi 5 + Hailo test setup replaces it anyway.
- Whether to have different alarm behavior per animal type — still
  undecided, doesn't affect the carrier board work.
- `protocol.md` (a doc describing the radio protocol) — still needs to be
  written up from the existing firmware code (codes: 11111 = dog, 22222 =
  cat, 12345 = default; pulse length 350; 24-bit code; sent 10 times; UDP
  port 5005; message format `DETECTED:<classname>`).
- Buy the Hailo-8L (or Hailo-8 as backup) — pricing/availability was
  unsettled. **Update: ordered as of Session 4** (see the checkmark under
  Timeline, Week 1) — keeping this line for history, can be deleted next
  cleanup.
- **Confirm TPS25947 (or another ≥20V-rated protection chip) is actually in
  stock** — TPS25940 is only rated for 18V; since we're now only requesting
  9V, this margin concern is less urgent than originally flagged, but still
  unresolved. **Oldest open item, unchanged since Session 2 (2026-07-25).**
- **Find a real ≥2A, 3.3V converter for the Hailo-8L's power rail** —
  confirmed 6.6W/2A max draw rules out a simple linear regulator here; no
  specific in-stock part found yet (looked at TPS62088/MP2143-type parts,
  not yet confirmed). Prefer a well-known brand (TI/MPS) for better design
  software support.
- **Pick the exact camera model** — needed to confirm whether it needs a
  1.8V rail and to check its control-bus address/resistor details.
- **Protection stage part not finalized** — surge protector (USBLC6-2SC6)
  and converter (MP2329) are confirmed; the protection chip is still open
  (see the TPS25947 stock-check item above); a separate small protection
  chip for the USB data lines (TPD4E02B04-type) also not yet confirmed in
  stock.
- **Power-up sequencing part** — delay circuit vs. dedicated switch chip
  approach not decided yet (needed so the 3.3V rail is stable before the
  Hailo-8L's reset signal releases). TPS22965/TPS22918 are candidate parts
  already listed above, but which approach to use isn't decided.
- **Confirm the MP2329's resistor values** (R1 = 40.2k ohms, R2 = 5.49k
  ohms, C4 = 33pF, inductor = 3.3µH, from the datasheet) are actually
  available in current stock.
- **USB-C connector part number not chosen yet** — new as of Session 4.
  Placed on the schematic without a specific part behind it. Once picked,
  confirm whether it has a through-hole shell (likely, for mechanical
  strength) and whether that changes the assembly line-item question
  flagged in "Decisions locked" above.
- **Confirm JLCPCB's through-hole assembly terms** — new as of Session 4.
  Does the switch to full machine assembly (no hand-soldering) need a
  separate quote line for the DF40 connector, M.2 socket, and USB-C
  connector versus regular surface-mount assembly? Not yet checked against
  JLCPCB's assembly options.

## Working style (for future sessions)

- Big picture before small details — Bill will say "slow down" if needed;
  respect that.
- Step-by-step, explain before acting. Direct tone, real opinions welcome.
- Keep the software and hardware work separate so problems can be isolated
  (prove the software works on the Raspberry Pi 5 before the custom board
  even exists).
- When a scope-change or pivot idea comes up (like "skip on-device AI and
  stream to a server instead," "switch to CM4," "is this project just an
  existing product") — give a direct opinion on the tradeoff before doing
  anything. Bill wants pushback if something would undo earlier decisions
  or hurt the recruiting deadline, not silent agreement.
- **Push documentation to GitHub at the end of every work session, not
  "eventually."** Added 2026-08-01 after finding CLAUDE.md and Journal.md
  were 6 days out of date mid-planning-session — an outdated Journal entry
  leads to bad timeline/status decisions. Note: the GitHub connection in
  claude.ai is read-only — it can only read from GitHub into a
  conversation, not push changes back. Actual pushes have to happen through
  Claude Code, plain git commands, or editing directly on GitHub.com.

---

## Obsidian vault — what to build here

This folder is an Obsidian vault (a note-taking app) used to **visually
map** the carrier board project as it develops. This is a planning/notes
tool, not the actual code repository — don't touch PCB design files,
firmware code, or the real git repo from here.

### Working style for this vault specifically

- **Bill does the planning. The assistant's job is to build exactly what's
  asked, then get double-checked** — don't add extra scope, layers,
  colors, groupings, or "helpful" extras unless specifically asked for.
  Default to the smallest version of any request. If a request is at all
  unclear, confirm in plain language before creating a `.canvas` (diagram)
  file.
- Use `.canvas` files for anything spatial/relational (diagrams). Use plain
  `.md` notes for anything that's just text/reference.

### Current task: Main Compute Module map

- One root box: **Main Compute Module**
- Three child boxes: **CM5**, **Hailo-8L**, **Camera**
- Three arrows: root → each child
- No colors, no groups, no layers, no summary text block — explicitly
  ruled out as too much for this pass. Each child box is where more detail
  gets added in future, separate requests — don't build that structure in
  advance.

### Hardware updates & discoveries

A running log of concrete facts and decisions found during research — this
is the "what we learned and when" record, separate from the summary above.
Update this section (or split it into its own note, e.g.
`Timeline/Hardware-Log.md`) as new sourcing or spec findings come up:

- **Hailo-8L no longer sold by itself by Raspberry Pi** — their AI Kit is
  discontinued, and they've confirmed no plans to sell the chip without
  their own HAT board. Third-party sellers (Waveshare, Yahboom) are the
  path forward now.
- **The CM5's external PCIe connection is Gen2 x1, not Gen3 x2** — the
  chip inside can technically go faster, but Raspberry Pi only certifies
  the slower speed for the external connector, for signal-quality reasons.
  Confirmed this is fine for the Hailo-8L: it automatically drops to the
  slower speed, identical to how Raspberry Pi's own AI Kit works (Pi 5 +
  Hailo-8L, same speed limit, proven to work).
- **CM4 and CM5 use the same connector family but different pin
  layouts** (~23 pins differ) — confirmed no connector wiring work carries
  over between them if the choice of module is ever revisited.
- **The CM5 4GB module hit a stock shortage** — the official price
  difference between the 2GB and 4GB versions is only about $25, but
  resellers were marking the 4GB version up over $100 above the 2GB price
  while it was sold out. Decision: bought the 4GB/32GB WiFi version once
  reasoned through (real risk reduction for heavy on-device tasks like
  compiling OpenCV from source, which can run out of memory on 2GB).
- **International shipping-forwarder websites inflate part cost badly** —
  a $99 Hailo-8 listing came out to $154.33 after a $55.33 forwarder
  shipping charge (specifically UP Products/up-shop.org). Regular
  Amazon/Mouser/DigiKey listings are the better price comparison going
  forward.
- **M.2 key-adapter cards (a different kind of expansion card for PCs) are
  unrelated hardware** — not to be confused with the M.2 socket connector
  that goes directly on the carrier board. Worth remembering if future
  parts research turns up similar-looking parts.
- **All three main connectors confirmed available on JLCPCB/LCSC**
  (double-checked against DigiKey), as of 2026-07-25:
  - **CM5 connector (DF40)**: **Amphenol ICC 10164227-1001A1RLF** (100-pin,
    0.4mm spacing, receptacle) — the CM5 uses this exact part, not the
    similar-looking Hirose part used on CM4. According to a Raspberry Pi
    engineer, the two are physically interchangeable, but the Amphenol
    version is rated for more current on the CM5. Need two of them. JLCPCB
    part **C6782225**.
  - **Hailo-8L M.2 socket**: **UMAX 91302-42-067RDM** (67-pin, 0.5mm
    spacing, sized for the 2242 card length). The Hailo-8L's dual-keyed
    card physically fits this single-keyed socket by design — dual-keying
    exists exactly so a card like this can fit either kind of socket — so
    no special part is needed. JLCPCB part **C601195**.
  - **Camera connector (CSI-2 flex cable connector)**: the official
    Raspberry Pi part (Molex 54548-2271, 22-pin, 0.5mm spacing) is now
    discontinued. A drop-in equivalent, same spec, available on JLCPCB/LCSC:
    **Hirose FH12-22S-0.5SH(55)**, part **C596813** (listed as pre-order —
    recheck stock before ordering parts for the schematic phase).
- **Power-input, debug/control wiring, and local-regulator parts
  researched (JLCPCB/LCSC, cross-checked against DigiKey), 2026-07-25:**
  - **Power negotiation chip**: CH224K, LCSC C970725 — confirmed
    resistor-set, no firmware needed, as planned.
  - **Protection chip**: TPS25940 (LCSC C2867756) found but only rated for
    18V — under the 20V a charger could theoretically negotiate. TPS25947
    (rated to 23V) is the right part, but stock wasn't confirmed yet; still
    open.
  - **Voltage converter**: TPS54560 (LCSC C31966, rated to 60V,
    well-stocked) for the 5V/5A main rail — needs an external inductor and
    diode.
  - **Surge protector**: USBLC6-2SC6 (LCSC C7519) for the power line and
    data lines; a separate small protection chip for the USB data lines
    (TPD4E02B04-type) not yet confirmed in stock.
  - **Debug port**: plain 2.54mm 3-pin through-hole header, LCSC C49257.
    External adapter: CP2102/FT232RL-type with a 3.3V/5V switch, verify
    the switch position before connecting (default position varies by
    board).
  - **Camera control-wire resistors**: Raspberry Pi's own camera modules
    (Camera Module 3 / IMX708) don't include the pull-up resistors these
    control wires need — carrier board must add 1.8k-ohm resistors to
    3.3V on each of the two wires.
  - **Hailo-8L's real power draw**: 6.6W / 2A max at 3.3V, 1.5W typical
    (from the chip's own datasheet, `Datasheets/4746521.pdf`) — much higher
    than the "few hundred mA" first assumed. Rules out a simple linear
    regulator for that power rail; needs a ≥2A converter, not yet picked
    (open item).
  - **Camera power rail**: AP2112K-3.3 linear regulator (LCSC C51118,
    600mA) confirmed fine given the camera's draw is under 500mA.
  - **Power-sequencing switch chips**: TPS22965 (6A, LCSC C347592) for the
    M.2 rail, TPS22918 (2A, LCSC C131941) for the camera rail.

**Later corrections (superseded by Session 3, 2026-07-30):**
- **Power negotiation chip**: switched from CH224K to CH224A for better
  voltage safety margin — see "Decisions locked" above.
- **Voltage converter**: switched from TPS54560 to MP2329GG-Z — see
  "Decisions locked" above.
