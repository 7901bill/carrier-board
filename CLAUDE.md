# CLAUDE.md — Wireless Watchdog: CM5 Carrier Board

Last updated: 2026-07-25

## Session log — read this first

Running recap, newest at the bottom. Purpose: know exactly where the last
session left off without re-reading the whole file.

- **Session 1 (2026-07-22):** Locked full component architecture — CM5
  (4GB/32GB eMMC, wireless), Hailo-8L on M.2 B+M (x1 Gen2 routed, link-trains
  down from rated x2 Gen3, same as RPi's own AI Kit), CSI + I2C control pair,
  two-stage power tree (PD → 5V/5A buck → local POL per rail), UART debug
  header (CM5-only, 3-pin, 3.3V logic). Re-confirmed CM5 over CM4 and carrier
  board over AI HAT+ (see "Decisions locked" below for reasoning on both).
  Sourced Hailo-8L pricing reality (RPi AI Kit discontinued, third-party
  modules ~$120-180, avoid freight-forwarder checkouts). Next up: power
  budget spreadsheet (wk1 action item, still not done), then order CM5 +
  Hailo-8L + camera.
- **Session 2 (2026-07-25):** Reworked the "Main Compute Module" canvas
  (`Graphical/Carrier Board PCB.canvas`) to a left-to-right tree layout
  (board → root → CM5/Hailo-8L/CSI Camera → their Connector/Power/Signal
  Integrity leaves) and turned each leaf's detail line into an Obsidian
  checkbox (`- [ ] ...`). Then did connector-sourcing research (JLCPCB/LCSC,
  cross-checked DigiKey) for all three subsystem connectors — see "Hardware
  updates & discoveries" below for the parts. Canvas leaves updated with the
  confirmed part numbers. Followed with a second research pass on the input
  power chain (PD sink, eFuse, buck, TVS), UART/I2C interfaces, and POL rail
  regulation — found the Hailo-8L's real max draw (6.6W/2A at 3.3V, not the
  "few hundred mA" originally assumed) and three open gaps (eFuse voltage
  margin, a real ≥2A 3.3V buck POL part, the actual CSI camera SKU) — see
  "Hardware updates & discoveries" and "Outstanding / carried over" below.
  Findings written into "Locked components," "Decisions locked," "Power
  architecture," and "Debug / bring-up" above, plus the canvas's Power &
  Protection node now has PD Sink/Protection/Buck Backbone checklist leaves
  matching the CM5/Hailo-8L/CSI pattern. Next up: close those three gaps, do
  the power budget spreadsheet, then order CM5 + Hailo-8L + camera +
  connectors.
- **Session 3 (2026-07-30):** Did the power budget spreadsheet (wk1 item,
  finally closed) — corrected total from ~20-23W to **~13W with margin**;
  the old number came from a Tom's Hardware CM5 figure measured under
  overclock + active cooling, not applicable here. Re-picked the PD sink
  (**CH224K → CH224A**, better VBUS/VHV voltage margin) and buck
  (**TPS54560 → MP2329GG-Z**), now requesting 9V instead of 20V since the
  corrected budget doesn't need the higher tier. Re-derived the full power
  tree conceptual model (PD passes voltage through unchanged; buck is the
  only conversion stage; POL rails downstream). Also revisited the
  Hailo-8L LDO-vs-buck question using a rough ~2.5W "realistic load"
  estimate and tentatively called an LDO acceptable for the M.2 3.3V rail —
  **this was wrong and got corrected in the next session**: re-read the
  Hailo-8L datasheet directly (`Datasheets/4746521.pdf`, §3.1) and confirmed
  it states max power is 6.6W/2A "at full utilization," with typical
  benchmark configs at 1.4-1.9W — none of which is 2.5W. The 6.6W/2A max
  figure already locked in this file was correct all along; the ≥2A buck
  POL requirement for that rail stands, LDO is still ruled out. Also
  consolidated the vault's documentation: `documentation.md` and
  `status.md` were pure re-narrations of what's already locked here (no new
  information) and were deleted; the dated `Session-Log-*.md` pattern is
  retired in favor of a single running `Journal.md` going forward. Next up:
  source the ≥2A 3.3V buck POL for the Hailo-8L rail (still the oldest open
  gap), the protection stage (eFuse/TVS/fuse), and confirm MP2329's FB
  divider resistor values against LCSC stock.

## Project summary

Summer 2026 goal: design a custom **CM5 carrier board in Altium** that turns the
Watchdog compute unit into a **standalone smart camera** — CM5 module + Hailo-8L
accelerator + CSI camera on one purpose-built 4-layer PCB. Inference moves
on-device; the PC server and imageZMQ pipeline are eliminated. Alarm path is
unchanged: detection → UDP over WiFi → ESP32 gateway → 433 MHz → alarm node.

Driver for the deadline: **fall new-grad recruiting.** Board must be back from
fab, populated, and booting by **late September 2026** so it's a finished,
documented portfolio piece.

Architecture was deliberately re-evaluated against "is this just the Raspberry
Pi AI HAT+" and against a full scrap-and-brainstorm detour (see "Decisions
locked" and "Architecture reasoning" below) — conclusion both times was to
proceed with the from-scratch carrier board, since the AI HAT+ only solves the
PCIe/M.2 slice and requires an existing Pi 5 underneath, and CM5 carrier
boards are still rare (CM5 shipped late 2024) versus the well-trodden CM4
ecosystem.

## Locked components

- **CM5**: 4GB RAM, 32GB eMMC, wireless. (2GB was seriously considered when
  4GB pricing spiked due to a stock shortage — official list price gap is
  only ~$25, the >$100 gap seen was reseller markup on a sold-out SKU. 4GB
  removes real OOM risk during heavy on-device builds, e.g. compiling OpenCV
  from source; 2GB would have worked for runtime but was riskier for dev.)
- **Hailo-8L**, 13 TOPS, M.2 B+M key (2242), PCIe Gen3 x2 rated.
  - Raspberry Pi no longer sells the module standalone (AI Kit discontinued;
    RPi explicitly states they can't offer Hailo-8L without the M.2 HAT+).
    Source: bare Hailo-8L or Hailo-8 M.2 modules from Waveshare/Yahboom
    (Amazon), or accept Hailo-8 (26 TOPS, similar/higher street price,
    ~$120-180) as a substitute if 8L pricing doesn't improve. Avoid
    international-forwarder checkouts (e.g. UP Products/up-shop.org) —
    shipping alone added ~56% on top of a $99 part in one quote checked.
  - **CM5 only exposes PCIe Gen2 x1** externally (BCM2712 controller is
    Gen3-capable but RPi certifies Gen2 only, jitter spec). Hailo-8L will
    link-train down from its rated x2 Gen3 to x1 Gen2 automatically — this
    is the exact same configuration as Raspberry Pi's own official AI Kit
    (Pi 5 + Hailo-8L), proven working. Reduced link bandwidth only, not
    reduced compute (13 TOPS is independent of the link). Detection
    payloads (boxes/labels, not raw video) are far below x1 Gen2 capacity.
  - M.2 socket footprint should be wired to full B+M spec (both PCIe lane
    pairs physically present in the connector), but only lane 0
    (TX0/RX0/REFCLK/PERST#/CLKREQ#) needs to be routed from the DF40 to the
    socket — lane 1 pins can be left unconnected.
- **Camera**: CSI-2, 4 data lanes + clock, length-matched, to CM5. Also needs
  an **I2C pair (SCL/SDA)** for camera control (exposure/gain/resolution) —
  separate from the CSI data lanes, easy to miss. RPi's own camera modules
  (Camera Module 3 / IMX708) carry **no on-board I2C pull-ups**, so the
  carrier board must add them — standard RPi value is **1.8kΩ to 3.3V** on
  both SCL and SDA. No double-pull-up risk since the module has none, but
  confirm once the actual camera SKU is picked.

## Decisions locked

- **Carrier board, not HAT, not full SBC.** CM5 carries the brutal parts
  (BGA fanout, DDR, WiFi certification); we design everything around it.
- **CM5 over CM4** (re-confirmed). Same DF40 connector family as CM4 but
  **different pin mapping (~23 pins differ)** — no pinout work is portable
  between them. CM4 is also a step down in CPU/RAM/eMMC speed and has no
  USB 3.0, with identical PCIe x1 Gen2 limitation, so switching would trade
  performance for no real benefit. CM4 carrier boards are also extremely
  well-trodden (tutorials, commercial kits) vs. CM5, which cuts against the
  "build something not already solved" goal.
- **Altium** (NYU license). Reference designs (KiCad) get imported for study.
- **4-layer**, JLCPCB controlled-impedance stackup, their SMT assembly for
  fine-pitch parts; hand-solder only connectors/through-hole.
- **Headless.** No HDMI (cut for scope — two fewer diff-pair groups). SSH over
  WiFi is the primary interface (zero board cost — WiFi is on the module).
  UART header is the non-negotiable fallback for boot/bring-up debug.
- **No Ethernet jack, no extra USB, no audio.**
- **PoE cut, deferred to rev B** (rev B swaps the front end, keeps the buck).
- **Battery ruled out** — 15–25W continuous load kills any pack in hours.
  Compute unit is wall-powered, full stop.
- **Power input = option (b): USB-C PD.** PD sink controller (**CH224A**,
  LCSC C42459160, Extended part on JLCPCB, confirmed in stock — resistor-
  strapped via CFG pins, no firmware, PD3.0/2.0 + QC) requests **9V** (not
  20V — corrected power budget below doesn't need the higher tier), single
  6.8kΩ resistor from CFG1 to GND. Not CH224K: CH224A's VHV/VBUS pins
  tolerate 32V vs. CH224K's 13.5V, better margin fit for the protection
  stage. CFG2/CFG3 broken out to the CM5 I2C bus for negotiation-status
  readback and live current monitoring during bring-up — rides along with
  single-resistor mode for free. VBUS must be shorted to VHV per reference
  schematic (easy to miss during schematic capture). eMarker emulation not
  needed — well under the 20V/60W threshold that requires it. CH224A
  negotiates and passes voltage through unchanged — it does not convert or
  regulate; PG (power-good) reports negotiation success, VBUS is just a
  sense pin. Refuse to run on 5V-only sources (prevents brownout mysteries).
  Escape hatch if week 2 runs hot: fall back to option (a) — bare USB-C +
  5.1V/5A official brick.
  Buck: **MP2329GG-Z** (MPS, LCSC C5349327, Extended part on JLCPCB,
  confirmed in stock) — 4.5–24V input, adjustable 0.6–13V output, 6.5A
  continuous/7.5A peak, synchronous COT topology, QFN-11 (2x2mm). This is
  the only stage that actually converts power — steps the negotiated 9V
  down to the 5V/5A backbone. 6.5A rating is a ceiling; real draw runs
  ~2.6A given the corrected ~13W budget, well under half capacity. 5V
  output resistor divider (from datasheet Table 1): R1 = 40.2kΩ, R2 =
  5.49kΩ, C4 = 33pF, L = 3.3µH — still need to confirm these exact values
  against current LCSC stock (open item).
- **Input protection regardless of option:** TVS on VBUS + eFuse/protection IC
  (TPS259xx-class: overvoltage block, inrush limit, short shutdown) + fuse.
  TVS candidate: **USBLC6-2SC6** (VBUS + 2 data lines, LCSC C7519, common
  basic part). eFuse candidate: **TPS25940** (LCSC C2867756) — **flag: only
  rated to 18V input, and PD can negotiate up to 20V**, so this is out of
  margin as specced; **TPS25947** (23V-rated) is the safer pick but its LCSC
  stock wasn't confirmed yet — verify before locking the BOM.
- **Weak-charger handling:** PD chip's capability indication gates an LED
  (minimum); optionally a GPIO to the CM5 so software knows the wattage.
  No dynamic throttling in rev A.
- **CM5 variant: with eMMC** (flashed over USB via nRPIBOOT jumper). Rejected
  reverting to microSD-based Lite variant — that would add a connector and a
  removable point of failure to what's supposed to be a sealed, finished unit
  for a minor CM5 module cost saving; not worth it this late in the timeline.

## Power architecture

Power budget (corrected 2026-07-30 — supersedes the earlier ~20-23W planning
number, which came from a Tom's Hardware CM5 figure measured under
overclocked 3GHz + active fan cooling, not applicable here):

| Component | Power |
|---|---|
| CM5 (stock clock, concurrent load estimate) | ~7.5W |
| Hailo-8L (13 TOPS inference) | ~2.5W |
| CSI camera (IMX708) | <1W |
| Housekeeping (LEDs, RTC trickle) | ~0.5W |
| **Raw total** | **~11.5W** |
| **With 15% margin** | **~13W** |

Note: the ~2.5W Hailo-8L figure above is a rough concurrent-load budgeting
estimate, not a datasheet number — the datasheet (`Datasheets/4746521.pdf`,
§3.1) states max power is **6.6W/2A at full utilization**, with typical
benchmark configs at 1.4-1.9W. The M.2 rail's POL regulator must be sized to
the 6.6W/2A max, not this budget estimate — see below.

Even a basic 5V/3A USB-C connection (15W, no PD) would nearly cover the ~13W
total, but the margin is thin (~2W), which is the reasoning for keeping PD
negotiation rather than dropping it.

```
USB-C VBUS ──→ CH224A (negotiates 9V, passes through unchanged, no conversion)
           ──→ [eFuse + TVS + fuse — protection stage, still unselected]
           ──→ MP2329 VIN (steps 9V down to 5V; current rises to match load, ~95% efficient)
           ──→ 5V/5A backbone rail (a bus, not a fixed allocation)
                ├──→ CM5 (uses 5V directly, CM5's internal PMIC handles further step-down)
                ├──→ buck POL (5V→3.3V, ≥2A) → Hailo-8L M.2 slot
                └──→ LDO (5V→3.3V, possibly 1.8V) → CSI camera
```

Voltage and current trade off at roughly constant power through the buck
stage (P ≈ V×I, ~90-95% efficient) — negotiating a higher voltage doesn't
increase the board's actual power draw, it changes the voltage/current split
of delivering the same wattage through a current-limited USB-C cable/
connector (often 3A ceiling on non-e-marked cables).

Two-stage: PD sink → single 5V/5A buck backbone → local point-of-load (POL)
regulation at each destination. Standard pattern, chosen over trying to
generate every voltage directly off the PD buck:

- CM5 takes 5V directly via DF40 (CM5's own internal PMIC handles further
  step-down to its core/RAM domains — not our job).
- M.2 slot: local 3.3V regulator near the Hailo-8L footprint. **Hailo-8L
  confirmed max draw is 6.6W / 2A at 3.3V (1.5W typical)** — per the
  module's own datasheet (`Datasheets/4746521.pdf`), well above the
  "few hundred mA" originally assumed. This rules out an LDO here (would
  dissipate ~3.4W as heat at max load) — needs a real **buck POL rated
  ≥2A**; a specific in-stock part hasn't been confirmed yet, open item.
- CSI camera: local 3.3V (and possibly 1.8V, check the specific camera
  module's datasheet — SKU not yet picked) regulator near the connector.
  Draw is well under 500mA, so an LDO is fine: **AP2112K-3.3** (600mA,
  LCSC C51118, well-stocked) is a confirmed candidate.

Why POL over one big regulator: shorter traces to each load (less resistive
drop, cleaner transients), independent debug/tuning per rail, and a fault on
one rail doesn't take the whole board down.

Also plan for:
- **Power sequencing** (RC delay or load-switch IC per rail enable) — e.g.
  3.3V should be stable on the M.2 slot before PERST# releases to Hailo.
- **Per-rail load switches**, specifically to support the bring-up plan
  already in this file: power up incrementally (rails with no CM5 mounted →
  module → UART console → peripherals) and verify each rail before anything
  expensive is powered. Confirmed candidates: **TPS22965** (6A, LCSC
  C347592) for the M.2/Hailo-8L rail, **TPS22918** (2A, LCSC C131941) for
  the smaller CSI camera rail.

## Debug / bring-up

- **UART is CM5-only.** Neither Hailo-8L nor the camera has anything that
  produces boot output — Hailo is controlled over PCIe by HailoRT running on
  CM5 (no OS of its own), camera is a dumb sensor. One UART header, off the
  CM5's DF40 pins, is the only debug path on the board.
- Header: 3-pin (TX, RX, GND), plain 2.54mm 1×3P through-hole pin header
  (commodity basic part, e.g. LCSC/JLCPCB C49257 — nothing exotic needed).
  External USB-to-TTL adapter, **must be 3.3V logic** (not 5V — will damage
  the pins). CP2102- or FT232RL-based adapters with a 3.3V/5V switch are the
  standard choice — **several ship defaulting to 5V, so verify the switch
  position before every first connection**, don't trust the label alone.
  Cross-wire TX↔RX. Terminal at 115200 baud, 8N1 (PuTTY on Windows, or
  screen/minicom in Git Bash/WSL).
- This is read-only visibility, not a flashing path. Flashing eMMC is via
  USB provisioning port + nRPIBOOT jumper (separate, already locked above).

## How each component gets "programmed" (mental model)

- **CM5**: has real persistent storage (eMMC), gets flashed once via USB
  provisioning + nRPIBOOT. Boots an OS afterward on its own.
- **Hailo-8L**: no persistent storage, no OS. A trained model (e.g. YOLOv8n)
  is compiled on a separate dev machine into a `.hef` file using Hailo's
  Dataflow Compiler, copied onto the CM5's filesystem as a normal file, and
  pushed onto the Hailo-8L over PCIe by the HailoRT runtime at startup —
  every power cycle, fresh. Nothing persists on the chip itself. Normal for
  this class of accelerator (same pattern as most GPU/NPU coprocessors).
- **Camera**: no storage, no flashing. CM5 configures it live over I2C each
  session (exposure, resolution, format); pixel data streams over CSI in
  real time.

## Physics notes agreed on

- Converters trade voltage for current at (nearly) constant power. Buck = V
  down / I up; boost = V up / I down. **Watts out ≤ watts in, always.** A weak
  charger cannot be "amped up" to 25W — the bottleneck doesn't move.
- With PD, the *charger* does the boosting on its side of the cable; the board
  only ever steps **down**. One conversion stage, downhill only.

## Subsystem risk list

- 🔴 **Power tree** — highest risk (brownouts look like software bugs), but
  Bill's strongest suit (LED driver experience). Budget first, worst case.
- 🔴 **DF40 connector pair** — highest consequence: footprint/pinout error =
  unfixable dead board. Pinout is **copied exactly** from the CM5 IO Board
  reference, not designed/invented. Mitigate by process: verified footprints
  only (SnapEDA/vault), cross-check Hirose drawing + CM5 mechanical spec,
  1:1 paper printout fit-check with a real CM5 before ordering.
- 🟡 **PCIe x1 to M.2** — the skill jump. Full signal set: TX0+/-, RX0+/-,
  REFCLK+/-, PERST#, CLKREQ# (8 wires total) + 3.3V power/GND. Stackup and
  Altium rules FIRST, then route. Fails soft (stays at negotiated x1 Gen2,
  which is expected/by design here) more often than dead.
- 🟡 **CSI-2** — 4 data pairs + clock, length matched, plus I2C control pair.
  Same discipline, same sitting as PCIe routing.
- 🟢 **USB 2.0 + provisioning** — one forgiving diff pair + nRPIBOOT jumper.
  Copy reference verbatim.
- 🟢 **Housekeeping** — UART header, per-rail power-good LEDs, RTC + coin
  cell, fan header (PWM + transistor). Cheap, mandatory for sane bring-up.
  First things cut if schedule slips: RTC, fan.

## Reference designs on hand

- **CM5 IO Board** (official, KiCad — import into Altium): connector pinout,
  power sequencing, protection scheme. This is the DF40 pinout source of
  truth — do not invent a mapping.
- **Raspberry Pi M.2 HAT+** (official, published schematic): the M.2 slot
  subsystem as a standalone worked example, incl. 3.3V arrangement and how
  a single-lane host connects to a wider-spec M.2 socket (same pattern as
  our Hailo-8L link-down situation).
- **Spectre RM DevBoard** (captain's board, STM32H743 TFBGA-240, 6-layer —
  NOT Bill's design): study its power input section (24V/XT30, TVS, dual
  LMR51450 bucks) and textbook 6-layer stack. Captain = layout reviewer in
  week 5.5.
- **Raspberry Pi AI HAT+ / AI Kit**: same Hailo chip family, useful as prior
  art for the PCIe-to-Hailo routing specifically, but NOT a template for the
  rest of the board — it only solves the PCIe/M.2 slice, requires a full Pi 5
  underneath (power, CM5-equivalent, CSI all inherited from that host), and
  solders the Hailo chip directly rather than socketing it.

## Timeline (6 weeks to fab)

- **Wk 1 (Jul 20–26):** Block diagram + power budget spreadsheet. Study CM5
  datasheet + IO board schematic. Lock part selection (PD chip, buck, eFuse,
  connectors). **Order CM5 + Hailo-8L + camera now** (lead times).
- **Wk 2–3 (Jul 27–Aug 9):** Full schematic. Order: power → DF40 → PCIe/M.2 →
  CSI → USB → housekeeping. Verified footprints pulled and checked.
  Gate: schematic review done by Aug 9 or cut RTC/fan.
- **Wk 3–5 (Aug 10–23):** Layout. Stackup + rules → DF40/module placement →
  power section → high-speed routing → rest. 1:1 paper fit-check here.
- **Wk 5.5 (Aug 24–28):** DRC clean, JLCPCB DFM check, captain reviews.
- **Wk 6 (Aug 29–31):** Generate outputs, order boards + stencil + SMT.
- **September:** Bring-up: rails with no CM5 mounted → module → UART console →
  peripherals. Software already proven ⇒ every failure is hardware.
- **Parallel (any weekend):** Hailo on the existing Pi 5 (PCIe FFC breakout) —
  compile YOLOv8n, wire to UDP→ESP32 path, measure real fps. De-risks bring-up
  to hardware-only.

## Outstanding / carried over

- **Rotate the WiFi router password** — open since May, repo was public.
- `wireless_detection_rpi.py` broken — moot if standalone pivot completes,
  but the Pi 5 + Hailo validation supersedes it.
- Per-animal alarm differentiation — still undecided; unaffected by carrier.
- `protocol.md` — still draftable from firmware (codes 11111 dog / 22222 cat /
  12345 default, pulse 350, 24-bit, 10 repeats, UDP 5005,
  `DETECTED:<classname>`).
- Source the Hailo-8L (or Hailo-8 fallback) module — pricing/availability is
  unsettled, revisit before the wk1 order deadline.
- **Confirm TPS25947 (or another ≥20V-rated eFuse) has real LCSC stock** —
  TPS25940 is only 18V-rated, under PD's 20V negotiation ceiling.
- **Find a real ≥2A 3.3V buck POL for the Hailo-8L M.2 rail** — confirmed
  6.6W/2A max draw rules out an LDO here; no specific in-stock part found
  yet (searched TPS62088/MP2143-class, not yet verified).
- **Pin down the actual CSI camera module SKU** — needed to confirm its
  1.8V rail requirement (if any) and its I2C address/pull-up specifics.
- **Protection stage (eFuse/TVS/fuse) part not yet finalized** — TVS
  (USBLC6-2SC6) and buck (MP2329) confirmed; eFuse still open per the
  TPS25947 stock-check item above; CC/SBU-specific protection
  (TPD4E02B04-class) also not yet confirmed in stock.
- **Power sequencing part** — RC delay network vs. dedicated load-switch IC
  choice not yet made (needed so 3.3V is stable on the M.2 slot before
  PERST# releases to Hailo). TPS22965/TPS22918 are candidates already
  listed above but the RC-vs-IC approach itself isn't decided.
- **Confirm MP2329's FB divider resistor values** (R1=40.2kΩ, R2=5.49kΩ,
  C4=33pF, L=3.3µH from datasheet Table 1) against current LCSC stock.

## Working style (for future sessions)

- Big picture before intricacy — Bill will say "slow down"; respect it.
- Step-by-step with explanations before commands. Direct tone, real opinions.
- Decouple workstreams to isolate variables (software proven on Pi 5 before
  custom hardware exists).
- When a scope-change or pivot idea comes up (e.g. "scrap on-device inference
  and stream to a server," "switch to CM4," "is this project just an existing
  product"), give a direct opinion on the tradeoff before executing — Bill
  wants pushback when something looks like it'd undo prior decisions or lose
  ground on the recruiting-deadline timeline, not silent compliance.

---

## Obsidian vault — what to build here

This folder is an Obsidian vault used to **visually map** the carrier board
project as it develops. This is a documentation/planning tool, not the code
repo — don't touch PCB files, firmware, or the actual git repo from here.

### Working style for this vault specifically

- **Bill does the planning. The agent's job is to build exactly what's asked
  and then get double-checked** — don't add scope, extra layers, colors,
  groupings, or "helpful" extras unless explicitly asked. Default to the
  smallest version of any request. Confirm scope in plain language before
  creating a `.canvas` file if a request is at all ambiguous.
- Prefer `.canvas` files for anything spatial/relational. Prefer plain `.md`
  notes for anything that's just text/reference.

### Current task: Main Compute Module map

- One root box: **Main Compute Module**
- Three child boxes: **CM5**, **Hailo-8L**, **CSI Camera**
- Three arrows: root → each child
- No colors, no groups, no layers, no overview text block — explicitly
  rejected as too much for this pass. Each child is where "spreading out"
  happens in future, separate requests — don't pre-build that structure now.

### Hardware updates & discoveries

Running log of concrete facts/decisions surfaced during hardware research —
distinct from the architecture summary above, this is the "what we learned
and when" trail. Update this section (or break it into its own vault note,
e.g. `Timeline/Hardware-Log.md`) as new sourcing/spec discoveries happen:

- **Hailo-8L no longer sold standalone by Raspberry Pi** — AI Kit
  discontinued; RPi confirms no plans to sell the module without the M.2
  HAT+. Third-party bare modules (Waveshare/Yahboom) are the path now.
- **CM5 external PCIe is Gen2 x1, not Gen3 x2** — controller is Gen3-capable
  but RPi certifies Gen2 only (jitter spec). Confirmed this is fine for
  Hailo-8L: it link-trains down automatically, identical to how RPi's own
  AI Kit works (Pi 5 + Hailo-8L, same lane limitation, proven working).
- **CM4 and CM5 use the same DF40 connector family but different pinouts**
  (~23 pins differ) — confirmed no DF40 pinout work transfers between them
  if the module choice ever gets revisited.
- **CM5 4GB module hit a stock shortage** — official list price gap between
  2GB and 4GB is only ~$25, but resellers were marking 4GB up past $100 over
  the 2GB price while it was sold out. Decision: bought 4GB/32GB eMMC
  wireless once reasoned through (real risk reduction on heavy on-device
  builds like compiling OpenCV from source, which can OOM-kill on 2GB).
- **International freight-forwarder checkouts inflate part cost badly** — a
  $99 Hailo-8 listing came out to $154.33 after a $55.33 forwarder shipping
  charge (UP Products/up-shop.org specifically). Domestic Amazon/Mouser/
  DigiKey listings are the better comparison baseline going forward.
- **M.2 key-adapter cards (E-key ↔ B-key PC expansion cards) are unrelated
  hardware** — not to be confused with the M.2 socket connector that goes
  directly on the carrier board. Worth remembering if sourcing research
  surfaces similar-looking parts again.
- **All three subsystem connectors confirmed sourceable on JLCPCB/LCSC**
  (cross-checked against DigiKey), 2026-07-25:
  - **CM5 DF40**: **Amphenol ICC 10164227-1001A1RLF** (100-pos, 0.4mm pitch,
    1.5mm stack, receptacle) — CM5 uses this Amphenol part, not CM4's Hirose
    DF40C-100DS-0.4V; per an RPi engineer the two are physically
    interchangeable but Amphenol is rated for higher current on CM5. Need
    two. JLCPCB/LCSC part **C6782225**.
  - **Hailo-8L M.2 socket**: **UMAX 91302-42-067RDM** (M-key, 67-pos, 0.5mm,
    "-42-" = mounting boss at the 2242 length). A B+M-keyed card (Hailo-8L)
    mechanically fits a plain M-key-only socket — dual-keying exists exactly
    so the card fits either single-keyed socket type — so no exotic
    "B+M socket" part is needed. JLCPCB/LCSC part **C601195**.
  - **CSI-2 FFC**: official RPi part is Molex 54548-2271 (22-pos, 0.5mm,
    bottom-contact ZIF) but it's now discontinued (DigiKey confirms EOL).
    Drop-in equivalent, same spec, in JLCPCB/LCSC library:
    **Hirose FH12-22S-0.5SH(55)**, part **C596813** (listed pre-order on
    JLCPCB — recheck stock before the Wk2-3 schematic order).
- **Power input, UART/I2C, and POL rail parts researched (JLCPCB/LCSC,
  cross-checked DigiKey), 2026-07-25:**
  - **PD sink**: CH224K, LCSC C970725 — confirmed resistor-strapped/
    firmware-free as specced.
  - **eFuse**: TPS25940 (LCSC C2867756) found but only 18V-rated — under
    PD's 20V ceiling. TPS25947 (23V-rated) is the right part but stock
    wasn't confirmed; open item.
  - **Buck**: TPS54560 (LCSC C31966, 60V-rated, well-stocked) for the
    5V/5A backbone — needs external inductor + catch diode.
  - **TVS**: USBLC6-2SC6 (LCSC C7519) for VBUS + data lines; CC/SBU-specific
    protection (TPD4E02B04-class) not yet confirmed in stock.
  - **UART header**: plain 2.54mm 1×3P through-hole, LCSC C49257. External
    adapter: CP2102/FT232RL with 3.3V/5V switch, verify switch position
    before connecting (defaults vary by board).
  - **I2C pull-ups**: RPi camera modules (Camera Module 3 / IMX708) have
    none on-board — carrier board must add 1.8kΩ to 3.3V on SCL/SDA.
  - **Hailo-8L real power draw**: 6.6W / 2A max at 3.3V, 1.5W typical (from
    the module datasheet already in `Datasheets/4746521.pdf`) — well above
    the "few hundred mA" originally assumed. Rules out an LDO for the M.2
    rail; needs a ≥2A buck POL, not yet sourced (open item).
  - **CSI camera rail**: AP2112K-3.3 LDO (LCSC C51118, 600mA) confirmed fine
    given <500mA draw.
  - **Load switches for sequencing**: TPS22965 (6A, LCSC C347592) for the
    M.2 rail, TPS22918 (2A, LCSC C131941) for the camera rail.
