# 4-Layer PCB Stackup — Why, and Design Pointers

Last updated: 2026-07-26

Reference note for the carrier board's stackup decision. This is background
and options, not a locked design — CLAUDE.md already locks "4-layer,
JLCPCB controlled-impedance stackup" as a decision, but the *specific
layer arrangement* (which layer is what) is still open. Laid out as
pros/cons per option so the actual arrangement can be picked deliberately,
not defaulted into.

## Why 4 layers, not 2

A 2-layer board (top signal + bottom signal, no dedicated plane layers) is
cheaper and simpler, but this board has three things that push past what
2 layers can do cleanly:

- **Controlled-impedance differential pairs.** PCIe Gen2 x1 (TX0±/RX0±) and
  CSI-2 (4 data pairs + clock) both need controlled impedance (typically
  ~90Ω differential for PCIe, ~100Ω differential for MIPI CSI/DSI-class
  signals — exact target depends on the calculator run, see below).
  Controlled impedance requires a **known, continuous reference plane**
  directly under the signal layer at a fixed dielectric height — that's a
  dedicated ground layer, not achievable with just two signal layers and no
  planes.
- **DF40 fanout density.** ~200 pins across two DF40 connectors (100 each)
  broken out to PCIe, CSI, USB, power, and GPIO in a small footprint. Fanout
  from a high-density BGA-style connector like this routinely needs more
  than 2 layers just to escape the pins without impossible trace/via
  congestion, independent of signal integrity concerns.
- **Power distribution + return path quality.** A dedicated ground plane
  gives every signal a clean, low-inductance return path directly beneath
  it (critical for EMI and for the PCIe/CSI eye diagrams not degrading), and
  a dedicated power plane means power delivery isn't fighting for space
  with signal routing.

None of these strictly *require* 4 layers (people do route PCIe on 2-layer
boards), but doing it reliably, on a first-time high-speed layout, within a
6-week timeline, without spending weeks hand-tuning return paths on a
signal-only layer — 4 layers is the standard, de-risked choice. This
matches what the CM5 IO Board reference and the RPi AI HAT+ both do.

## Stackup arrangement options

All of these are physically "4 layers" and cost the same at JLCPCB — the
difference is which layer does what. Layer numbering: L1 (top) / L2 / L3 /
L4 (bottom).

### Option A — Signal / GND / PWR / Signal (the classic default)

```
L1: Signal (top components + routing)
L2: GND (solid plane)
L3: PWR (solid or split plane)
L4: Signal (bottom components + routing)
```

**Pros:**
- Every signal layer (L1, L4) has an adjacent reference plane one layer
  away — clean, simple impedance calculations, this is what JLCPCB's own
  impedance calculator and most stackup guides assume by default.
- Power plane on L3 gives low-impedance power distribution with good
  decoupling behavior (power and ground planes close together form a
  natural high-frequency bypass capacitor).
- Best-documented option — most reference designs (including likely the
  CM5 IO Board) use this or something close to it, so cross-checking your
  stackup against theirs is straightforward.

**Cons:**
- If the power plane needs splitting (e.g. separate 3.3V zones for M.2 vs
  CSI vs CM5), any high-speed signal on L4 that needs to reference L3
  crosses a plane split wherever the zones divide — a return-path
  discontinuity that hurts signal integrity if a differential pair happens
  to route over that boundary. Manageable with care (route sensitive pairs
  on L1 referencing the solid L2 ground instead), but it's a constraint to
  actively design around, not ignore.

### Option B — Signal / GND / GND / Signal (dual ground)

```
L1: Signal
L2: GND (solid plane)
L3: GND (solid plane, stitched to L2 with vias)
L4: Signal
```

**Pros:**
- Both signal layers reference a *solid, unsplit* ground plane — no
  plane-split return-path risk at all, which is the cleanest option for
  signal integrity and EMI.
- Simplifies impedance calculation and de-risks the PCIe/CSI routing
  specifically, since neither of those has to think about power-plane
  splits.

**Cons:**
- Power distribution has to happen as **traces**, not a plane — meaning
  wider/thicker copper pours or careful trace-based power routing instead
  of just "drop a via to the power plane anywhere." More layout discipline
  needed for the 5V backbone and the POL rail fan-out.
- Loses the power/ground plane self-capacitance bypass effect Option A
  gets for free — decoupling caps have to do more of the work (not a big
  deal at these switching frequencies, but worth knowing).

### Option C — Signal / PWR / GND / Signal (power on top pair)

```
L1: Signal
L2: PWR (solid plane)
L3: GND (solid plane)
L4: Signal
```

**Pros:**
- Puts ground (L3) directly under the bottom signal layer (L4) — useful if
  most of the high-speed/sensitive routing (e.g. the DF40-to-M.2 PCIe run)
  naturally ends up on the bottom side.
- Same plane-adjacency benefits as Option A, just mirrored.

**Cons:**
- Functionally very similar to Option A with top/bottom swapped — the real
  question is which physical side of the board your sensitive traces end
  up on, which depends on component placement decisions not yet made.
  Worth deciding only after DF40/M.2/CSI connector placement is roughed
  out, not before.

### Which to pick

No single "correct" answer without knowing final placement — that's a call
to make once you know roughly where DF40, the M.2 socket, and the CSI
connector land relative to each other. Rule of thumb while placing
components: whichever signal layer carries PCIe and CSI, make sure the
adjacent layer is a **solid, unsplit** reference plane under those specific
traces, even if you mix strategies elsewhere on the board (e.g. Option A's
power plane can still have a split *away* from where the high-speed traces
run).

## JLCPCB-specific stackup facts (confirmed 2026-07-26)

- JLCPCB's impedance calculator computes trace width from board thickness,
  copper weight, layer, target impedance, and pair spacing — use it
  directly rather than hand-calculating, it matches what they'll actually
  fabricate.
- Standard tolerance is **±10%** on impedance; **±5%** is available as a
  paid option if the design margin is tight.
- Accepted impedance range: **20–90Ω single-ended, 50–150Ω differential** —
  both PCIe (~90Ω diff) and CSI (~100Ω diff, sensor-dependent) fall
  comfortably inside this.
- For impedance-controlled orders, material selection should be **FR-4
  TG155** (their standard high-Tg controlled-impedance material).
- At **2.0mm board thickness**, JLCPCB only offers one specific controlled
  stackup (JLC7628) — if a non-default thickness is wanted, check their
  calculator for what stackups are actually available at that thickness
  before designing around it. Default 1.6mm thickness has more stackup
  options.

Sources:
- [JLCPCB Impedance Calculator / Controlled Impedance page](https://jlcpcb.com/impedance)
- [User Guide to the JLCPCB Impedance Calculator](https://jlcpcb.com/help/article/User-Guide-to-the-JLCPCB-Impedance-Calculator)
- [PCB Layers Explained: Smart Stackup and Design Practices](https://jlcpcb.com/blog/pcb-stackup-best-practices)

## Design pointers (apply regardless of which stackup option is picked)

- **Never route a controlled-impedance differential pair over a plane
  split** in its reference layer — the return current has nowhere
  continuous to flow, which shows up as ringing/EMI/eye-diagram
  degradation. Check this explicitly for both PCIe and CSI once plane
  shapes are drawn.
- **Length-match within a pair tightly, match pair-to-pair loosely.**
  Intra-pair skew (P vs N of the same pair) matters far more than skew
  between e.g. TX0 and RX0 — tune to the datasheet's actual skew tolerance,
  don't over-engineer by matching everything to the same length.
- **Keep differential pairs tightly coupled** (spacing between P/N smaller
  than spacing to neighboring traces) — this is what makes them reject
  common-mode noise; the JLCPCB calculator's "conductor spacing" input is
  this gap and directly sets your target impedance.
- **Via stitching around high-speed traces**: place ground vias near
  layer-transition vias on differential pairs (where a pair moves from L1
  to L4, for instance) so the return current has a nearby low-inductance
  path to follow the signal through the layer change. Skipping this on a
  layer transition is a common first-timer mistake.
- **Decouple at the point of load, not just at the connector.** Each POL
  regulator (M.2 3.3V, CSI 3.3V) needs its own local decoupling network
  close to its output pin — don't rely on the plane's bulk capacitance
  alone.
- **Keep the DF40 fanout on the layer(s) closest to the connector** where
  possible, minimizing vias-per-net for the highest-pin-density part on the
  board — fewer vias means fewer opportunities for a footprint/pinout
  mistake to hide, which matters given DF40 is flagged 🔴 in the risk list.
- **Run the actual JLCPCB impedance calculator once real trace geometry is
  known** (after stackup + board thickness are chosen) — don't rely on
  rule-of-thumb impedance numbers from other people's boards; JLCPCB's
  dielectric thicknesses are specific to their process.
