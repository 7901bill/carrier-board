# 4-Layer PCB Stackup — Why, and Design Pointers

Last updated: 2026-07-26

A reference note explaining the board's layer-stack decision. This is
background and options, not a locked design — documentation.md already locks in
"4 layers, JLCPCB's controlled-impedance stackup" as a decision, but the
*exact arrangement* (which layer does what) is still open. Laid out below
as pros/cons for each option, so the final choice gets made on purpose,
not by default.

## Why 4 layers, not 2

A 2-layer board (one signal layer on top, one on the bottom, no dedicated
power/ground layers) is cheaper and simpler, but this board has three
things that push past what 2 layers can handle cleanly:

- **Controlled-impedance wire pairs.** The PCIe connection (2 matched wire
  pairs) and the camera connection (4 data pairs + clock) both need
  "controlled impedance" — a consistent electrical property along the
  whole trace (roughly 90 ohms for PCIe, roughly 100 ohms for the camera
  interface, exact target depends on a calculator, see below). Controlled
  impedance requires a **known, unbroken ground layer** directly underneath
  the signal wires, at a fixed distance — that means a dedicated ground
  layer, which isn't possible with just two signal layers and no other
  layers.
- **Dense connector wiring.** About 200 pins across the two main
  connectors (100 pins each) need to be broken out to the PCIe, camera,
  USB, power, and other connections in a small space. Fanning out that many
  pins from a dense connector like this usually needs more than 2 layers
  just to physically escape the pins without impossible wire/via crowding.
- **Power distribution and clean return paths.** A dedicated ground layer
  gives every signal a clean, short path back to its source (important for
  reducing electrical noise and keeping the PCIe/camera signal quality
  good), and a dedicated power layer means the power wiring isn't competing
  for space with signal wiring.

None of these strictly *require* 4 layers (people do route PCIe on 2-layer
boards), but doing it reliably, as a first attempt at high-speed board
design, on a 6-week schedule, without spending weeks hand-tuning return
paths on a signal-only layer — 4 layers is the standard, lower-risk choice.
This matches what both the CM5 reference board and the Raspberry Pi AI
HAT+ do.

## Stackup arrangement options

All of these are physically "4 layers" and cost the same at JLCPCB — the
difference is which layer does what. Layer numbering: L1 (top) / L2 / L3 /
L4 (bottom).

### Option A — Signal / Ground / Power / Signal (the classic default)

```
L1: Signal (top parts + wiring)
L2: Ground (solid layer)
L3: Power (solid or split layer)
L4: Signal (bottom parts + wiring)
```

**Pros:**
- Every signal layer (L1, L4) has a ground layer directly next to it —
  simple, clean impedance math, and this is the default assumption in
  JLCPCB's own impedance calculator and in most guides.
- The power layer on L3 gives clean power distribution and works like a
  natural high-frequency filter (a power layer and ground layer close
  together act a bit like a built-in capacitor).
- Best-documented option — most reference designs (probably including the
  CM5 reference board) use this or something close to it, making it easy
  to cross-check.

**Cons:**
- If the power layer needs to be split into zones (say, separate 3.3V
  areas for the M.2 slot vs. the camera vs. the CM5), any high-speed signal
  on L4 that needs the L3 layer as its reference crosses that split
  wherever the zones divide — this breaks the clean return path if a
  matched wire pair happens to route over that boundary. Manageable with
  care (route the sensitive pairs on L1 instead, referencing the solid L2
  ground layer), but it's something to actively design around, not ignore.

### Option B — Signal / Ground / Ground / Signal (double ground)

```
L1: Signal
L2: Ground (solid layer)
L3: Ground (solid layer, connected to L2 with vias)
L4: Signal
```

**Pros:**
- Both signal layers reference a *solid, unbroken* ground layer — no risk
  of a broken return path at all, which is the cleanest option for signal
  quality and electrical noise.
- Simplifies the impedance math and makes the PCIe/camera wiring lower-risk
  specifically, since neither one has to worry about a split power layer.

**Cons:**
- Power has to be distributed as **wires**, not a solid layer — meaning
  wider/thicker copper traces or more careful wire-based power routing
  instead of just connecting to a power layer anywhere. More care needed
  laying out the 5V main rail and the local regulator connections.
- Loses the natural filtering effect Option A gets for free from having a
  power layer next to a ground layer — the filter capacitors on the board
  have to do more of that work (not a big deal at these switching speeds,
  but worth knowing).

### Option C — Signal / Power / Ground / Signal (power on top pair)

```
L1: Signal
L2: Power (solid layer)
L3: Ground (solid layer)
L4: Signal
```

**Pros:**
- Puts the ground layer (L3) directly under the bottom signal layer (L4) —
  useful if most of the sensitive, high-speed wiring (like the connector-to-
  M.2 PCIe run) ends up on the bottom side of the board.
- Same benefits as Option A, just flipped top-to-bottom.

**Cons:**
- Functionally almost identical to Option A with top and bottom swapped —
  the real question is which physical side of the board the sensitive
  wires end up on, which depends on part placement decisions not made yet.
  Worth deciding only after the connector/M.2/camera placement is roughed
  out, not before.

### Which to pick

There's no single "correct" answer without knowing the final part
placement — that's a decision to make once it's roughly known where the
main connector, M.2 socket, and camera connector will sit relative to each
other. Rule of thumb while placing parts: whichever signal layer carries
the PCIe and camera wiring, make sure the layer right next to it is a
**solid, unbroken** reference layer under those specific wires, even if
other strategies get mixed in elsewhere on the board (for example, Option
A's power layer can still be split *away* from where the high-speed wires
run).

## JLCPCB-specific facts (confirmed 2026-07-26)

- JLCPCB's impedance calculator works out the trace width needed from
  board thickness, copper weight, layer, target impedance, and pair
  spacing — use it directly instead of doing the math by hand, since it
  matches what they'll actually manufacture.
- Standard tolerance is **±10%** on impedance; **±5%** is available as a
  paid option if the design margin is tight.
- Accepted impedance range: **20-90 ohms single wire, 50-150 ohms for
  matched pairs** — both PCIe (~90 ohms) and the camera interface (~100
  ohms, depends on the sensor) fall comfortably inside this.
- For controlled-impedance orders, the material should be **FR-4 TG155**
  (their standard high-temperature controlled-impedance material).
- At **2.0mm board thickness**, JLCPCB only offers one specific
  controlled-impedance stackup (JLC7628) — if a non-default thickness is
  wanted, check their calculator for what's actually available at that
  thickness before designing around it. The default 1.6mm thickness has
  more options.

Sources:
- [JLCPCB Impedance Calculator / Controlled Impedance page](https://jlcpcb.com/impedance)
- [User Guide to the JLCPCB Impedance Calculator](https://jlcpcb.com/help/article/User-Guide-to-the-JLCPCB-Impedance-Calculator)
- [PCB Layers Explained: Smart Stackup and Design Practices](https://jlcpcb.com/blog/pcb-stackup-best-practices)

## Design pointers (apply no matter which stackup option is picked)

- **Never route a controlled-impedance matched pair over a split** in its
  reference layer — the return current has no continuous path to flow,
  which shows up as noise and worse signal quality. Check this specifically
  for both the PCIe and camera wiring once the power/ground layer shapes
  are drawn.
- **Match wire lengths tightly within a pair, loosely between pairs.** The
  length difference between the two wires of the same pair matters far
  more than the length difference between, say, the transmit pair and
  receive pair — match to the datasheet's actual tolerance, don't
  over-engineer by matching everything to the exact same length.
- **Keep matched pairs close together** (the gap between the two wires of
  a pair should be smaller than the gap to neighboring wires) — this is
  what makes them reject noise that hits both wires equally; the JLCPCB
  calculator's "conductor spacing" input is exactly this gap, and it
  directly sets the target impedance.
- **Add extra ground vias near layer-change vias on high-speed wire
  pairs** (where a pair moves from L1 to L4, for example) so the return
  current has a nearby, short path to follow the signal through the layer
  change. Skipping this on a layer change is a common beginner mistake.
- **Put filter capacitors right at the part that needs them, not just at
  the connector.** Each local voltage regulator (M.2 3.3V, camera 3.3V)
  needs its own nearby filter capacitors close to its output pin — don't
  rely on the ground/power layer alone to smooth things out.
- **Keep the main connector's wiring on the layer(s) closest to the
  connector** where possible, minimizing the number of vias per wire for
  the highest-pin-density part on the board — fewer vias means fewer
  chances for a footprint or pin mistake to hide, which matters since the
  main connector is flagged as highest-risk in the risk list.
- **Run the actual JLCPCB impedance calculator once the real wire geometry
  is known** (after the stackup and board thickness are chosen) — don't
  rely on rule-of-thumb numbers from other people's boards, since JLCPCB's
  exact layer thicknesses are specific to their manufacturing process.
