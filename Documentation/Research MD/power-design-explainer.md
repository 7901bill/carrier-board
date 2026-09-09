# Power Design, Outlet to Component — A Working Explainer

Last updated: 2026-09-09

> **Note:** this note was written 2026-07-29, one day before the power
> system got recalculated and some parts changed (see documentation.md's Session 3
> and Session 4). A few specific facts below are now out of date — the
> power negotiation chip is now **CH224A** (not CH224K), the main converter
> is now **MP2329GG-Z** (not TPS54560), the board now requests **9V** (not
> an undecided voltage), and the total power budget is **~13W** (not the
> 15-25W range mentioned below). The general explanations of *how* each
> stage works are still accurate — just double-check any specific part
> number or number against documentation.md, which is always the current source of
> truth.

## Current implementation checkpoint — 2026-09-09

The current local-rail choices and required schematic connections are:

```text
5V_MAIN
    ├──> TPS54302DDCR (C311983), configured for 3.3 V
    │       └──> 3V3_HAILO
    │               └──> M.2 pins 2, 4, 70, 72, and 74
    │
    └──> AP2112K-3.3TRG1 (C51118)
            └──> 3V3_CAMERA
                    └──> Raspberry Pi 22-pin CSI connector pin 22
```

These branches share `5V_MAIN` and the board ground plane, but they do not
share a 3.3 V output rail. The Hailo-8L is rated for as much as 2 A at 3.3 V,
so raw 5 V must never reach the M.2 power contacts. The camera connector needs
one 3.3 V supply on pin 22; the standard Raspberry Pi camera module generates
its lower internal rails on the camera PCB.

Part selection is complete, but CAD implementation and verification are not.
The schematic still needs the two regulator branches, their datasheet-required
passives and local decoupling, test points, and the connections to the M.2 and
CSI connectors. Hailo reset sequencing also remains open because the
TPS54302DDCR has soft-start but no power-good output: `3V3_HAILO` must be
stable before `PERST#` is released.

This note walks through the actual path electricity takes on your board,
one stage at a time. Each stage answers one question: *what is this here
to do, and what breaks if it's missing?*

---

## The full chain, at a glance

```
Wall outlet (120V AC)
    ↓
USB-C charger   ← AC-to-DC conversion happens HERE, off your board
    ↓
USB-C cable (now DC power, exact voltage decided by negotiation)
    ↓
[YOUR BOARD STARTS HERE]
    ↓
Power negotiation chip (asks the charger for a specific voltage, e.g. 12V)
    ↓
Input protection (surge protector + protection chip + fuse)
    ↓
Voltage converter (12V → 5V, the "main rail")
    ↓
   ┌──────────────┬──────────────────┬──────────────┐
   ↓              ↓                  ↓
 CM5 (5V direct) Hailo-8L (needs   Camera (needs
                  local 3.3V)      local 3.3V)
```

One thing to understand right away: **converting wall power (AC) into DC
is not your problem to solve.** That happens inside the USB-C charger,
which is a sealed, pre-certified consumer product. Your board never sees
AC power directly — it only ever receives DC power that's already been
converted, and your job is just to negotiate a voltage and step it down
further. This is *why* USB-C Power Delivery is such a good choice for a
student project — it hands off the scariest, most heavily-regulated part
of the design (converting mains-voltage AC power to DC) to a part you buy
off the shelf, instead of a circuit you'd have to design and certify
yourself.

---

## Stage 1: The charger (not part of your board, but worth understanding)

A USB-C Power Delivery charger has its own AC-to-DC converter built in —
it takes 120V AC from the wall and turns it into DC power internally.
These chargers are also "smart": they don't just output one fixed voltage.
They listen for a request sent over the USB-C data wires and can offer
several voltage options (5V, 9V, 12V, 15V, 20V are common) at different
current limits, listed in a table called a "PDO" (Power Data Object).

This is the part you never touch, design, or certify — it's a bought,
tested, safety-certified product. Full stop.

---

## Stage 2: Voltage negotiation (the first thing that happens on your board)

**Why not just use 5V and skip negotiation entirely?**
Because power equals voltage times current, and current is what costs you
in wire thickness, connector rating, and wasted heat from resistance. At
25W, 5V means about 5A of current — that's a lot for a small connector and
thin circuit-board trace. At 12V, the same 25W is only about 2A. Asking for
a higher voltage from the charger and stepping it down on your own board
(where you control exactly how) is the standard approach for anything
drawing real power over USB-C.

**How the power negotiation chip does this:**
It's resistor-set — meaning specific resistor values on specific pins tell
the chip which voltage to request the moment it's plugged in. No software,
no separate microcontroller needed. The chip handles the USB Power Delivery
communication internally and simply outputs whichever voltage it's wired to
request, once the charger agrees to supply it.

**The requested voltage is a real tradeoff:**
- **A lower requested voltage:** less voltage the converter has to drop,
  slightly better converter efficiency, but higher input current for the
  same total wattage.
- **A higher requested voltage:** lower input current, but the converter
  and everything in its input path (surge protector, protection chip) has
  to be rated to safely handle that voltage, with margin in case a cheap,
  non-standard-compliant charger overshoots slightly during negotiation.

*(As noted at the top: the board now requests 9V, and the total power
budget is about 13W — both were still open questions when this note was
first written.)*

---

## Stage 3: Input protection

This is the stage most beginners skip, and most reliability problems trace
back to skipping it. Three separate parts, each catching a different kind
of failure:

**Surge protector (technically a "TVS diode") — USBLC6-2SC6**
Sits directly across the power and ground wires, right at the connector.
Its job: clamp any voltage spikes (static discharge from someone touching
the connector, a brief spike from unplugging a cable, a negotiation
glitch) before they reach anything sensitive further down the board. Think
of it as a pressure relief valve — normally doing nothing at all, only
kicking in during a spike, then going back to doing nothing.

**Protection chip ("eFuse")**
This is a smart, electronic circuit breaker. Unlike a plain fuse, it can:
- Limit the sudden rush of current at power-up (a capacitor charging up on
  the converter's input can otherwise briefly look like a dead short)
- Actively cut power if current draw goes above a set limit (a short
  circuit somewhere downstream)
- Cut power if voltage rises above a safe limit (a miswired or
  malfunctioning charger)
- This part was open at the time this note was written — see the note at
  the top of this file for the current status.

**Fuse (a simple, physical, one-time-use part)**
The last-resort backup. If the protection chip itself fails, or a fault
happens faster than it can react, the physical fuse breaks the circuit
permanently (you'd have to replace it). This is the "even if everything
else fails, the board doesn't catch fire" layer.

**Why this order (surge protector → protection chip → fuse), not some
other order:**
The surge protector has to come first because it needs to clamp any spike
before it even reaches the protection chip's sensitive internal circuitry.
The protection chip comes next because it's the fast-reacting, active
layer. The fuse is the slow, simple, final backup — its position relative
to the others doesn't matter much because it's not reacting during normal
use at all, only during a serious, sustained fault.

---

## Stage 4: The main voltage converter (the workhorse conversion)

**What a voltage converter actually does:**
It steps DC voltage *down* while stepping current *up*, at (roughly)
constant total power — the same idea covered earlier: total watts out can
never be more than watts in, and the conversion trades voltage for
current, it never creates power out of nothing.

**How this type of converter works, mechanically:**
This is a "switching" converter — it doesn't reduce voltage by just wasting
the difference as heat (that's what a simple linear regulator does, badly,
at any real power level). Instead, it rapidly switches an internal
transistor on and off, storing energy in a small inductor coil during "on"
and releasing it during "off," then smoothing the result with an output
capacitor. This kind of converter is typically 85-95% efficient, compared
to a linear regulator which might waste over half the power as heat at
this kind of voltage drop.

**What you have to specify, not just buy:**
- **Output voltage:** set by a pair of resistors on the chip's feedback
  pin — this is a real calculation from the datasheet's formula, not a
  default value. The target here is 5V.
- **Inductor value:** affects how smooth the output current is and how
  fast the converter reacts to load changes; the datasheet gives a formula
  or a recommended value for the chosen switching speed and voltage ratio.
- **Input/output capacitors:** sized to smooth ripple and keep the circuit
  stable; the datasheet's reference design gives typical values — copy
  these, don't guess.
- **Stability network** (if the chip isn't internally compensated):
  stabilizes the feedback loop so the converter doesn't oscillate.

This is genuinely "follow the datasheet's example circuit" work — the chip
maker has already done the hard math; the job here is correctly copying
it, not re-deriving it from scratch.

---

## Stage 5: Local voltage regulation — why not just use 5V everywhere?

The conceptual answer is already settled from earlier sessions: shorter
wire runs to each part, each rail can be tested/tuned on its own, and a
fault on one rail doesn't take down the whole board. Worth explaining the
underlying electrical reason too:

**Every wire has some resistance.** A long 5V wire feeding a chip that
actually needs a clean 3.3V, with a separate small regulator placed *right
next to that chip*, means the messy, longer part of the current path (the
shared 5V main rail, possibly feeding other parts too) doesn't directly
determine the voltage quality that sensitive chip sees. The local regulator
"cleans up" the power again right at the point where it's used.

**Your two local rails, and why they use different technology:**

| Rail       | Load            | Why a simple linear regulator works here                                                                                                                          | Why a switching converter is needed there                                                                              |
| ---------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Camera | <500mA          | Low current × small voltage drop (5V→3.3V) = very little wasted heat. A linear regulator is simpler and quieter (no switching noise near a sensitive camera signal — this matters!). | —                                                                                                                                      |
| Hailo-8L   | up to 2A / 6.6W | —                                                                                                                                                                 | A linear regulator here would waste about 3.4W as heat (a real, noticeable hot spot on the board). Needs a real switching converter for efficiency. |

The selected camera regulator is `AP2112K-3.3TRG1` (`C51118`). The selected
Hailo regulator is `TPS54302DDCR` (`C311983`), a 3 A synchronous buck
configured for 3.3 V. Selection does not close the remaining schematic,
thermal, transient, and reset-sequencing verification.

This is also *why* a linear regulator is preferred for the camera
specifically, beyond just "low current" — switching converters are
electrically noisy (that's just how the switching works), and camera
signal quality is sensitive to that kind of noise nearby. Using a linear
regulator next to the camera isn't just "cheaper because low current," it's
also "quieter where it matters."

---

## Stage 6: Sequencing — the part that's easy to forget entirely

Power rails don't all have to turn on at the exact same instant, but some
*must* turn on in a specific order relative to a control signal. Your
specific requirement: the 3.3V rail on the M.2 slot must be stable
**before** the Hailo-8L's reset-release signal goes active. Do it
backwards, and the Hailo-8L chip could see its reset release while its
power rail is still climbing — an undefined, flaky result, exactly the
kind of bug that looks like a software problem and isn't.

**How this gets built (still an open item in the design):**
- **Simplest: a delay circuit on an enable pin.** A resistor-capacitor
  circuit slows down when a switch chip's "on" pin sees a high signal,
  creating a predictable delay after the main power rail turns on before
  that specific rail is allowed to turn on. Cheap, no extra chip, but the
  delay is fixed and somewhat imprecise (varies a bit with part tolerance).
- **A switch chip with built-in slow-rise control** (which the two
  candidate switch chips partly provide) — controls *how fast* voltage
  rises once turned on, reducing the current inrush, but doesn't by itself
  sequence *relative to* another rail.
- **A dedicated sequencing/monitoring chip** — watches multiple rails and
  only releases an output (like the reset signal) once its inputs cross a
  threshold. More precise, but more expensive and more design work.

For a project at this power level and complexity, a delay circuit on the
enable pin is the right-sized choice — a dedicated sequencing chip solves
a problem this design doesn't really have at this scale.

---

## Stage 7: The return path (why "just connect ground" isn't the whole story)

Every current that flows out to a part has to flow back — that's not
optional, it's just basic circuit physics. The real question is *where*
that return current flows, and whether that path is clean.

**On a 4-layer board**, one full internal layer is usually a solid ground
layer. Current returning from any part takes the path of least resistance
back to the source — which, directly under a wire, is almost always the
ground layer immediately below it. This is why:
- **Don't route a wire over a slot or split in the ground layer below
  it.** The return current has to detour around the gap, which increases
  electrical noise and hurts signal quality. This matters far more for the
  high-speed PCIe/camera wiring than for the power rails themselves, but
  the ground layer is shared — a badly placed connector footprint anywhere
  can create a gap that hurts unrelated wires routed above it.
- **Filter capacitors need to sit physically close to the chip pin
  they're protecting**, with a short path to ground. The capacitor's job
  is to supply sudden current spikes a chip demands during fast switching
  (digital logic toggling, high-speed data being sent) faster than the
  main converter itself can respond. If the capacitor is far away, or its
  ground connection is a long, thin wire instead of a direct connection to
  the ground layer, it's much less effective — the extra wire length adds
  resistance and inductance that cancels out the capacitor's speed
  advantage.

This is genuinely a **layout-stage concern**, not a schematic-stage one —
you can't design "a good return path" into a schematic; you can only wire
correct connections now and then execute it well when actually placing
copper later (layer stack + rules first, then route — which is already the
plan).

---

## Where each part of *your* board's power design stood on 2026-07-29

*(Out of date — see the note at the top of this file. Kept here for
history.)*

| Stage | Part(s) | Status as of 2026-07-29 |
|---|---|---|
| Voltage negotiation | CH224K | Chip picked; **requested voltage not yet chosen** |
| Input protection | USBLC6-2SC6 (surge protector), TPS2594x protection chip, fuse | Surge protector confirmed; **protection chip voltage rating unresolved** |
| Main converter | TPS54560 | Chip picked; **output resistor values not yet calculated** |
| CM5 rail | — (direct 5V) | Ready, no design work needed |
| Hailo-8L local rail | — | **Converter chip not yet picked** — the one fully-open part |
| Camera local rail | AP2112K-3.3 | Ready |
| Sequencing | TPS22965, TPS22918 switch chips | Parts picked; **delay circuit values not yet designed** |

Five separate open action items sat inside "the power section," not one.
That was normal for week 2 of the project — but worth seeing laid out
plainly rather than folded into "just pick the last part." (See documentation.md
for what's since been resolved.)
