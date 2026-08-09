# PCIe x1 and Matched Wire Pairs — A Working Explainer

Last updated: 2026-07-30

This note covers two ideas together because on your board they're really
one topic: the Hailo-8L talks to the CM5 over PCIe, and PCIe (like the
camera connection) is built entirely out of matched wire pairs. Understanding
matched pairs first makes the PCIe terms ("lane," "Gen," "x1/x2") make sense.

---

## Part 1: What a matched wire pair actually is

**The problem it solves:** a single wire carrying a signal is vulnerable
to noise. Any electrical interference near that wire (a switching power
converter, a nearby clock signal, outside electrical noise) adds unwanted
voltage on top of the real signal, and the receiving chip has no way to
tell "real signal" from "noise that got added along the way."

**The fix:** send the signal **twice, on two wires, as exact opposites of
each other** — one wire carries the signal, the other carries the exact
inverse (when one goes high, the other goes low, always). These two wires
are routed as a pair, physically close together and the same length. The
receiving chip doesn't look at either wire's voltage by itself — it looks
at the **difference** between the two.

**Why this cancels out noise so well:** because the two wires run right
next to each other, any noise source affects both wires almost identically
(this is called "common noise" — the same interference hitting both
wires). If wire A picks up an extra +50mV of noise, wire B (right next to
it) picks up almost exactly +50mV too. The receiving chip subtracts B from
A — the noise cancels out, since it was added equally to both. Only the
*real* difference between the two wires (the actual signal) survives that
subtraction.

**Naming convention:** you'll see pairs labeled with `+` and `-`, like
`TX0+` / `TX0-`. These are the two wires of one matched pair — always
routed together, always treated as one unit, never separated to route
individually.

**Why "length-matched" matters:** the noise-cancelling trick above only
works if both wires arrive at the receiving chip at (almost exactly) the
same instant — if one wire is physically longer than its partner, its
signal arrives slightly delayed, and the two are no longer true opposites
of each other at any given moment. This timing mismatch is called **skew**,
and it's why you'll see "length-matched" mentioned for every matched pair
on this board (both PCIe and the camera connection) — it's not a
nice-to-have, it's the entire mechanism the noise-cancelling depends on.

---

## Part 2: PCIe (Peripheral Component Interconnect Express)

**What it is:** the connection type the Hailo-8L uses to talk to the CM5.
It's how most fast add-on chips (graphics cards, storage drives, this AI
chip) connect to a main processor — a serial connection built from matched
wire pairs, the modern successor to an older, slower parallel connection
type.

**"Lane":** one PCIe lane is a set of **two matched wire pairs** — one pair
for sending data (TX+/TX-), one pair for receiving data (RX+/RX-). Both
directions work at the same time, on physically separate wires — unlike
UART, where only one wire handles each direction and there's no shared
clock at all.

**"x1", "x2", etc. (lane count):** how many lanes are bundled together to
act as one wider connection. More lanes roughly means more data per
second (x2 is roughly double the speed of x1, at the same generation).
This is a *physical wire-count* question, separate from "Gen" below.

**"Gen" (generation):** the signaling speed *per lane*. Each PCIe
generation (Gen1, Gen2, Gen3, and so on) roughly doubles the raw data rate
per lane compared to the one before it, using the same number of wires.
This is independent of lane count — a 1-lane Gen3 connection and a 2-lane
Gen2 connection end up at roughly similar total speed, because doubling
the per-lane speed and doubling the lane count both double the total.

**Your specific situation — why x1 Gen2, not x2 Gen3:**
- The Hailo-8L chip is *rated* for PCIe Gen3, using 2 lanes.
- The CM5 only *exposes* Gen2, using 1 lane, on its external connector —
  not because the chip inside the CM5 can't go faster (it's Gen3-capable
  internally), but because Raspberry Pi only *certifies* Gen2 on the
  external connector, for signal-quality reasons.
- PCIe devices are designed to **automatically drop to a slower speed**
  when needed: at power-up, both ends figure out the fastest speed they
  both support. A Gen3, 2-lane-capable chip connected to a Gen2,
  1-lane-only host simply settles for Gen2, 1-lane — this is normal,
  expected behavior, not a bug or a workaround. It's the exact same setup
  Raspberry Pi's own official AI Kit uses (Pi 5 + Hailo-8L), which is
  proven to work.
- **This only costs data speed, not AI processing power.** The Hailo-8L's
  13 TOPS of AI processing happens entirely inside the chip — the PCIe
  connection only carries the results back (detection boxes, class labels),
  plus the compiled AI model file loaded once at startup. That amount of
  data is far below what even the slower 1-lane Gen2 connection can carry.

**The 8 wires that make up your PCIe connection (plus power/ground):**
| Signal | Purpose |
|---|---|
| TX0+/TX0- | Send data (CM5 → Hailo-8L) |
| RX0+/RX0- | Receive data (Hailo-8L → CM5) |
| REFCLK+/REFCLK- | Shared reference clock — both chips' internal timing circuits sync to this, needed for the connection to lock onto correct bit timing |
| PERST# | Reset signal (active when low, hence the `#`) — has to happen in a specific order relative to power stability, see the note below |
| CLKREQ# | Clock request (active when low) — lets the Hailo-8L ask for the reference clock to turn on, part of a power-saving feature (lets the clock turn off when the connection is idle) |

**Why the reset signal's timing matters (ties back to the power design):**
PERST# tells the Hailo-8L "the rest of the system is stable, you can come
out of reset now." If PERST# is released while the Hailo-8L's 3.3V power
rail is still climbing up to full voltage, the chip can come out of reset
into an undefined state — a bug that looks exactly like a flaky software
problem, when really it's a hardware timing issue. This is why the M.2
rail's power sequencing (3.3V stable *before* PERST# releases) is called
out as a specific requirement, not just a general "power everything up"
note.

**Connector footprint vs. actual wiring — a distinction worth knowing:**
The M.2 socket footprint on the board is wired for the *full* B+M
connector spec (both PCIe lane pairs physically present, since that's what
the standard connector part provides), but only **lane 0** is actually
wired from the main connector to the socket. Lane 1's pins are left
unconnected — there's nothing on the CM5 side to drive them, since it only
exposes 1 lane. This isn't wasted design work; it's just using a standard
connector part that happens to support more than what's actually wired up.

---

## Part 3: How this connects to the camera interface (your other matched-pair subsystem)

The camera connection (CSI-2) is a *different* protocol from PCIe, but
built on the exact same matched-wire-pair foundation: **4 data pairs +
1 clock pair, each a matched pair**, length-matched for the same
noise-cancelling reason described in Part 1. The design rules (match the
two wires of each pair to each other, match pair-to-pair lengths where the
spec requires it, keep pairs away from noise sources, don't route over
power/ground layer splits) are the same for both subsystems — which is why
both are flagged at the same risk level in the project's risk list. If you
understand *why* PCIe needs matched lengths, you already understand why the
camera connection does too.

---

## Where this stands in your design

| Item | Status |
|---|---|
| Lane count / Gen | Locked: 1 lane, Gen2 (drops down automatically from the Hailo-8L's native 2 lanes, Gen3) |
| Wire list | Locked: TX0±, RX0±, REFCLK±, PERST#, CLKREQ# (8 wires) + 3.3V/ground |
| M.2 socket | Sourced: UMAX 91302-42-067RDM, LCSC C601195, full B+M footprint |
| Lane wiring | Only lane 0 wired from the main connector to the socket; lane 1 left unconnected |
| Reset signal timing | Requirement identified (3.3V stable before release); exact circuit not designed yet, see the power architecture notes |
| Length matching / layer rules | Not done yet — planned as "set up the layer stack and design rules first, then route the wires," part of the layout phase |
