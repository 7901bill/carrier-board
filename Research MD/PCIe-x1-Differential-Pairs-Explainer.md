# PCIe x1 and Differential Pairs — A Working Explainer

Last updated: 2026-07-30

This covers the two ideas together because on your board they're really
one subsystem: the Hailo-8L talks to the CM5 over PCIe, and PCIe (like
CSI) is built entirely out of differential pairs. Understanding diff
pairs first makes the PCIe "lane," "Gen," and "x1/x2" language make sense.

---

## Part 1: What a differential pair actually is

**The problem it solves:** a single wire carrying a signal is vulnerable
to noise. Any electrical interference near that wire (a switching
regulator, a nearby clock, EMI from outside the board) adds unwanted
voltage to the signal, and the receiver has no way to tell "real signal"
from "noise that got added on the way."

**The fix:** send the signal **twice, on two wires, as inverted copies of
each other** — one wire is the signal, the other is the exact opposite
(if one goes high, the other goes low, always). These two wires are
routed as a matched pair, physically close together and the same length.
The receiver doesn't look at either wire's absolute voltage — it looks at
the **difference** between them.

**Why this rejects noise so effectively:** because the two wires run
right next to each other, any noise source affects both wires almost
identically (this is called "common-mode noise" — the same interference,
common to both). If wire A picks up +50mV of noise, wire B (right next to
it) picks up almost exactly +50mV too. The receiver subtracts B from A —
the noise cancels out, because it was added equally to both sides. Only
the *intentional* difference between the two wires (the real signal)
survives the subtraction.

**Naming convention:** you'll see pairs labeled with `+` and `-` suffixes,
e.g. `TX0+` / `TX0-`. These are the two wires of one differential pair —
always routed together, always treated as a single unit, never split
apart to route separately.

**Why "length-matched" matters:** the noise-cancellation trick above only
works if both wires arrive at the receiver at (almost exactly) the same
time — if one trace is longer than its partner, the signal on it arrives
slightly delayed, and the two are no longer true inverses of each other
at any given instant. This timing mismatch is called **skew**, and it's
why you'll see "length-matched" called out on every diff pair on this
board (PCIe *and* CSI) — it's not a nice-to-have, it's the entire
mechanism the noise rejection depends on.

---

## Part 2: PCIe (Peripheral Component Interconnect Express)

**What it is:** the interface the Hailo-8L uses to talk to the CM5. It's
how most fast peripherals (GPUs, NVMe drives, this AI accelerator)
connect to a host processor — a serial, differential-pair-based link,
successor to the older parallel PCI bus.

**"Lane":** one PCIe lane is a set of **two differential pairs** — one
pair for transmit (TX+/TX-), one pair for receive (RX+/RX-). This is
"full duplex" — data can flow both directions simultaneously, on
physically separate wires, unlike UART's single-direction-per-wire but
still-shared-timing scheme.

**"x1", "x2", etc. (lane count):** how many lanes are bonded together to
work as one wider link. More lanes = more bandwidth, roughly linearly
(x2 is roughly double the bandwidth of x1, same Gen). This is a
*physical* wire-count question, separate from "Gen."

**"Gen" (generation):** the signaling speed *per lane*. Each PCIe
generation (Gen1, Gen2, Gen3...) roughly doubles the raw bit rate per
lane over the previous one, using the same physical wire count. This is
independent of lane count — a x1 Gen3 link and a x2 Gen2 link happen to
land at similar total bandwidth, because 2x the speed and 2x the lanes
both double throughput.

**Your specific situation — why x1 Gen2, not x2 Gen3:**
- The Hailo-8L module is *rated* for PCIe Gen3, x2 (two lanes).
- The CM5 only *exposes* Gen2, x1 externally — not because the BCM2712
  controller can't do more (it's Gen3-capable internally), but because
  Raspberry Pi only *certifies* Gen2 on the external connector, for
  signal jitter reasons.
- PCIe devices are designed to **link-train down** automatically: at
  power-up, both ends negotiate the fastest mutually-supported
  configuration. A Gen3 x2-capable device connected to a Gen2 x1-only
  host simply settles at Gen2 x1 — this is normal, expected behavior, not
  a fault or workaround. It's the exact same configuration Raspberry
  Pi's own official AI Kit uses (Pi 5 + Hailo-8L), which is proven
  working in the field.
- **This costs bandwidth, not compute.** The Hailo-8L's 13 TOPS of
  inference happens entirely on-chip — the PCIe link only carries
  results (bounding boxes, class labels) back to the CM5, plus the
  compiled model (`.hef` file) loaded once at startup. That traffic is
  far below what even a reduced x1 Gen2 link can carry.

**The 8 wires that make up your PCIe link (plus power/ground):**
| Signal | Purpose |
|---|---|
| TX0+/TX0- | Transmit differential pair (CM5 → Hailo-8L) |
| RX0+/RX0- | Receive differential pair (Hailo-8L → CM5) |
| REFCLK+/REFCLK- | Reference clock differential pair — both ends' internal PLLs sync to this, needed for the serial link to lock and interpret bit timing correctly |
| PERST# | Reset signal (active-low, hence the `#`) — must be held/released in the correct sequence relative to power stability, see the power-sequencing note below |
| CLKREQ# | Clock request (active-low) — lets the endpoint request the reference clock be active, part of PCIe power management (lets REFCLK be gated off to save power when the link is idle) |

**Why PERST# sequencing matters (ties back to the power design):**
PERST# tells the Hailo-8L "the rest of the system is stable, you can come
out of reset now." If PERST# is released while the Hailo-8L's 3.3V rail
is still ramping up, the chip can come out of reset into an undefined
electrical state — a bug that manifests as flaky, inconsistent behavior
that looks exactly like a software problem, not a hardware timing issue.
This is why the M.2 rail's power sequencing (3.3V stable *before* PERST#
releases) is called out as a specific requirement, not a generic "power
everything up" note.

**Footprint vs. routing — a distinction worth knowing:**
Your M.2 socket footprint is wired to the *full* B+M key spec (both PCIe
lane pairs physically present in the connector, since that's what the
standard connector footprint provides), but only **lane 0** is actually
routed from the DF40 to the socket. Lane 1's pins are left unconnected —
there's no host-side signal to drive them, since the CM5 only exposes x1.
This isn't wasted footprint; it's just using a standard connector that
happens to support more than you're wiring up.

---

## Part 3: How this connects to CSI (your other diff-pair subsystem)

CSI-2 (your camera interface) is a *different* protocol from PCIe, but
built on the exact same differential-pair foundation: **4 data lanes +
1 clock lane, each a differential pair**, length-matched for the same
skew-cancellation reason described in Part 1. The routing discipline
(match the +/- pair lengths to each other, match lane-to-lane lengths
where the spec requires it, keep pairs away from noise sources, avoid
routing across ground plane splits) is the same discipline for both
subsystems — which is why both are flagged at the same risk tier in the
project's risk list. If you understand *why* PCIe needs length matching,
you already understand why CSI does too.

---

## Where this stands in your design

| Item | Status |
|---|---|
| Lane count / Gen | Locked: x1 Gen2 (link-trains down from Hailo-8L's native x2 Gen3) |
| Signal set | Locked: TX0±, RX0±, REFCLK±, PERST#, CLKREQ# (8 wires) + 3.3V/GND |
| M.2 socket | Sourced: UMAX 91302-42-067RDM, LCSC C601195, full B+M footprint |
| Lane routing | Only lane 0 routed from DF40 to socket; lane 1 left unconnected |
| PERST# sequencing | Requirement identified (3.3V stable before release); exact sequencing implementation still open, see power architecture notes |
| Length matching / stackup rules | Not yet done — planned as "stackup + Altium rules first, then route," part of the wk3-5 layout phase |
