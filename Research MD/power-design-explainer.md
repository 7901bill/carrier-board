# Power Design, Outlet to Component — A Working Explainer

Last updated: 2026-07-29

This walks the actual path electricity takes on your board, in order, stage
by stage. Each stage answers one question: *what is this here to do, and
what breaks if it's missing?*

---

## The full chain, at a glance

```
Wall outlet (120V AC)
    ↓
USB-C PD charger/brick   ← AC→DC conversion happens HERE, off your board
    ↓
USB-C cable (now DC, voltage TBD by negotiation)
    ↓
[YOUR BOARD STARTS HERE]
    ↓
PD sink chip (negotiates voltage, e.g. requests 12V)
    ↓
Input protection (TVS + eFuse + fuse)
    ↓
Buck converter (12V → 5V, the "backbone")
    ↓
   ┌──────────────┬──────────────────┬──────────────┐
   ↓              ↓                  ↓
 CM5 (5V direct) Hailo-8L (needs   CSI camera (needs
                  3.3V POL)         3.3V POL)
```

One thing to internalize immediately: **the hard part of AC-to-DC
conversion is not your problem.** That happens inside the USB-C charger
brick, which is a sealed, pre-certified consumer product. Your board never
sees AC. It only ever sees DC that's already been converted and is now
being negotiated and stepped down further. This is *why* USB-C PD is such
a good choice for a student project — it outsources the scariest, most
heavily-regulated part of the design (mains-voltage AC/DC conversion) to a
part you buy off the shelf instead of a circuit you'd have to design,
certify, and trust with your life.

---

## Stage 1: The charger brick (off-board, but worth understanding)

A USB-C PD charger contains its own AC-DC converter — it takes 120V AC
from the wall, rectifies it, and produces a DC voltage internally. USB-C
PD chargers are also "smart": they don't just output one fixed voltage.
They listen for a request over the USB-C data lines and can supply
multiple voltage options (5V, 9V, 12V, 15V, 20V are common) at various
current limits, advertised in a "PDO" (Power Data Object) table.

This is the part you never touch, design, or certify. It's a bought,
tested, UL-listed product. Full stop.

---

## Stage 2: PD negotiation (first thing that happens on your board)

**Why not just use 5V and skip negotiation entirely?**
Because power = voltage × current, and current is what costs you in wire
gauge, connector rating, and I²R heating losses. At 25W, 5V means ~5A —
that's a lot of current for a small connector and thin PCB trace. At 12V,
the same 25W is only ~2A. Negotiating a higher voltage upstream and
stepping it down on-board (where you control the conversion) is the
standard move for anything drawing real power over USB-C.

**How CH224K (your PD sink chip) does this:**
It's resistor-strapped — meaning you set specific resistor values on
specific pins, and those values tell the chip which voltage to request
(9V, 12V, 15V, 20V) the moment it's plugged in. No firmware, no
microcontroller involved. The chip handles the USB-PD communication
protocol internally and simply outputs whichever voltage you've hard-wired
it to request, once the charger agrees to supply it.

**Open decision for you:** which voltage to request. This is a real
tradeoff:
- **Lower requested voltage (9V):** less voltage the buck has to drop,
  slightly better buck efficiency, but higher input current for the same
  wattage.
- **Higher requested voltage (20V):** lower input current, but your buck
  converter and every component in its input path (TVS, eFuse) must be
  rated to survive 20V, and if a *cheap* non-compliant charger overshoots
  during negotiation, you want margin.

Your total board draw isn't nailed down yet — that's what the power budget
spreadsheet (still on the to-do list) is for. The one hard number you have
is the Hailo-8L at 6.6W max. The CM5's own draw hasn't been measured or
found in its datasheet yet, so don't treat any total-wattage figure as
settled until that spreadsheet exists. That said, the project already
estimated the whole board lands somewhere in the 15-25W range (this is
also why battery power got ruled out), and 12V is a reasonable, common
middle choice for that range — it's what most PD trigger boards default to.

---

## Stage 3: Input protection

This is the stage most beginners skip and most reliability problems trace
back to. Three separate components, each catching a different failure
mode:

**TVS diode (Transient Voltage Suppressor) — USBLC6-2SC6**
Sits directly across VBUS and GND, right at the connector. Its job:
clamp voltage spikes (ESD from a person touching the connector,
inductive kickback from cable unplug, brief negotiation glitches) before
they reach anything sensitive downstream. Think of it as a pressure
relief valve — normally invisible/inactive, snaps into a low-impedance
state only during a spike, then goes back to being invisible.

**eFuse / protection IC — TPS259xx-class**
This is the smart circuit breaker. Unlike a plain fuse, it can:
- Limit inrush current at power-up (capacitor charging on the buck's
  input can otherwise look like a dead short for a few microseconds)
- Actively cut power if current draw exceeds a set threshold (short
  circuit downstream)
- Cut power if voltage rises above a safe threshold (overvoltage — e.g.
  a miswired or malfunctioning charger)
- This is what's currently open in your project — TPS25940 is rated
  18V, which doesn't have margin if you're requesting up to 20V from PD.
  TPS25947 (23V-rated) is the fix, pending stock confirmation.

**Fuse (passive, physical, one-time)**
The last-resort backstop. If the eFuse itself fails, or a fault happens
faster than the eFuse can react, the physical fuse opens the circuit
permanently (you'd replace it). This is the "even if everything else
fails, the board doesn't catch fire" layer.

**Why this order (TVS → eFuse → fuse), not some other order:**
The TVS has to be first because it needs to clamp transients before they
even reach the eFuse's sensitive control circuitry. The eFuse comes next
because it's the active, fast-reacting layer. The fuse is the dumb,
slow, final backstop — it doesn't care about order relative to the
others because it's not reacting to normal operation at all, only to
sustained fault conditions.

---

## Stage 4: The buck backbone (the workhorse conversion)

**What a buck converter actually does:**
Steps DC voltage *down* while stepping current *up*, at (near) constant
power — this is the same principle you already worked through: watts
out ≤ watts in, always, and the conversion trades V for I, never
creates power from nothing.

**TPS54560 (your backbone buck), the mechanics:**
This is a switching converter — it doesn't drop voltage by wasting the
difference as heat (that's what an LDO does, badly, at any real power
level). Instead, it rapidly switches an internal transistor on and off,
storing energy in an inductor during "on" and releasing it during "off,"
smoothing the result with an output capacitor. Efficiency in the 85-95%
range is typical, versus an LDO which might waste 50%+ of the power as
heat at this voltage drop.

**What you have to specify, not just buy:**
- **Output voltage:** set by a resistor divider on the feedback (FB) pin
  — this is a real calculation from the datasheet formula, not a
  default. You're targeting 5V.
- **Inductor value:** affects ripple current and transient response;
  the datasheet gives you a formula or a recommended value for your
  switching frequency and voltage conversion ratio.
- **Input/output capacitors:** sized for ripple and stability; datasheet
  reference design gives typical values — copy these, don't guess.
- **Compensation network** (if not internally compensated): stabilizes
  the feedback loop so the converter doesn't oscillate.

This is genuinely "follow the datasheet's typical application circuit"
work — the IC vendor has already done the hard math; your job is
correctly transcribing it, not re-deriving it from first principles.

---

## Stage 5: Point-of-load (POL) regulation — why not just use 5V everywhere?

You already have the conceptual answer locked from earlier sessions:
shorter traces to each load, independent debug/tuning per rail, and
fault isolation. Worth restating the electrical *why* underneath that:

**Every trace has resistance.** A long 5V trace feeding a chip that needs
a clean 3.3V, with a separate regulator sitting *right next to that chip*,
means the messy, longer part of the current path (the 5V backbone,
possibly shared with other loads) doesn't directly determine the voltage
quality the sensitive chip sees. The local regulator "re-cleans" the
supply right at the point of use.

**Your two POL rails, and why they're different technologies:**

| Rail       | Load            | Why LDO works here                                                                                                                                                | Why buck is needed there                                                                                                               |
| ---------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| CSI camera | <500mA          | Low current × small V drop (5V→3.3V) = little wasted heat. LDO is simpler, quieter (no switching noise near a sensitive analog camera interface — this matters!). | —                                                                                                                                      |
| Hailo-8L   | up to 2A / 6.6W | —                                                                                                                                                                 | An LDO here would dissipate ~3.4W as waste heat (a real, physical hot spot on your board). Needs a real switching buck for efficiency. |

This is also *why* an LDO is often preferred for the camera specifically
beyond just "low current" — switching regulators are electrically noisy
(that's the switching action itself), and camera analog/CSI signal
integrity is sensitive to that kind of noise nearby. Using an LDO next to
a camera isn't just "cheaper because low current," it's also "quieter
where it matters."

---

## Stage 6: Sequencing — the part that's easy to forget entirely

Power rails don't all have to come up at the exact same instant, but
some *must* come up in a specific order relative to a control signal.
Your specific requirement: 3.3V must be stable on the M.2 slot **before**
PERST# (the Hailo's reset-release signal) goes active. Do it backwards,
and the Hailo chip could see a reset release while its rails are still
climbing — undefined, flaky behavior, exactly the kind of bug that looks
like a software problem and isn't.

**How this gets implemented (the part still open in your design):**
- **Simplest: RC delay on an enable pin.** A resistor-capacitor network
  slows down when a load switch's enable pin sees "high," creating a
  predictable delay after backbone power-up before that rail is allowed
  to turn on. Cheap, no extra part, but the delay is fixed and somewhat
  imprecise (varies with cap tolerance).
- **Load switch with built-in slew control** (which TPS22965/TPS22918
  partially provide) — controls *how fast* voltage rises once enabled,
  reducing inrush, but doesn't by itself sequence *relative to* another
  rail.
- **Dedicated sequencer/supervisor IC** — monitors multiple rails and
  only asserts an output (like PERST#) once its inputs cross a threshold.
  More precise, more expensive, more design overhead.

For a project at your power level and complexity, RC-delay-on-enable is
the proportionate choice — a dedicated sequencer IC is solving a problem
you don't really have at this scale.

---

## Stage 7: The return path (why "just connect GND" isn't the whole story)

Every current that flows out to a component has to flow back — that's
not optional, it's just physics (Kirchhoff's current law). The question
is *where* that return current flows, and whether that path is clean.

**On a 4-layer board**, one full internal layer is typically a solid
ground plane. Current returning from any component takes the path of
least impedance back to the source — which, directly under a trace, is
almost always the ground plane immediately below it. This is why:
- **Don't route a trace over a slot or split in the ground plane below
  it.** The return current has to detour around the gap, increasing loop
  area, which increases EMI radiation and signal integrity risk. This
  matters far more for your PCIe/CSI high-speed traces than for the
  power rails themselves, but the ground plane is shared — a badly
  placed connector footprint anywhere can create a slot that hurts
  unrelated nets routed above it.
- **Decoupling capacitors need to be physically close to the IC pin
  they're protecting**, with a short path to ground. The cap's job is to
  supply the sudden current spikes a chip demands during fast switching
  (digital logic toggling, PCIe transceivers driving) faster than the
  regulator itself can respond. If the cap is far away, or its ground
  connection is a long thin trace instead of a direct via to the ground
  plane, it's much less effective — the parasitic inductance of that
  extra trace length undoes the capacitor's speed advantage.

This is genuinely a **layout-phase concern**, not a schematic-phase one —
you can't wire "a good return path" into a schematic, you can only wire
correct connectivity now and then execute it well in copper later
(stackup + rules first, then route — which is already your plan).

---

## Where each part of *your* board's power design currently stands

| Stage | Component(s) | Status |
|---|---|---|
| PD negotiation | CH224K | Chip picked; **requested voltage not yet chosen** |
| Input protection | USBLC6-2SC6 (TVS), TPS2594x eFuse, fuse | TVS confirmed; **eFuse voltage rating (25947 vs 25940) unresolved** |
| Backbone buck | TPS54560 | Chip picked; **output-set resistor divider not yet calculated** |
| CM5 rail | — (direct 5V) | Ready, no design work needed |
| Hailo-8L POL | — | **Buck IC not yet selected** — the one fully-open component |
| CSI camera POL | AP2112K-3.3 LDO | Ready |
| Sequencing | TPS22965, TPS22918 load switches | Parts picked; **delay implementation (RC values) not yet designed** |

Five concrete action items sit inside "the power sheet," not one. That's
normal for week 2 — but worth seeing laid out plainly rather than
folded into "just pick the last part."
