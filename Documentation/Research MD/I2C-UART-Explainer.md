# I2C and UART — A Working Explainer

Last updated: 2026-07-30

Two different types of simple wired connections show up on this board, for
two different jobs. This note explains what each one is, why it's built
the way it is, and exactly where it's used on *your* design.

---

## The core difference, up front

**UART** connects exactly two chips, one wire for each direction, no
addressing needed. **I2C** is a shared connection: many chips can share the
same two wires, and each one gets its own address. If you only remember one
thing, remember that — it explains almost every other difference below.

---

## UART (Universal Asynchronous Receiver/Transmitter)

**What it's for on this board:** the debug console. It's the *only* way to
see boot-up messages from the CM5 — nothing else on the board (the Hailo-8L,
the camera) produces any output of its own to look at.

**How it physically works:**
- **2 signal wires, one for each direction: TX (transmit) and RX
  (receive)**, plus a shared ground wire. That's it — no clock wire.
- "Asynchronous" means there's no separate clock signal keeping both sides
  in sync. Instead, both sides agree ahead of time on a **baud rate**
  (yours: 115200) — a fixed speed they each count against on their own.
  Each byte has a start marker and stop marker so the receiving side knows
  exactly when a new byte begins, even with no shared clock signal.
- Because there's no clock wire, **TX and RX have to be cross-connected**:
  one device's TX goes to the other device's RX, and the other way around.
  Connect two TX pins together and nothing works — this is the single most
  common UART wiring mistake.

**Why it's used for debugging specifically:** UART is dead simple and
doesn't need the operating system or any driver software running to work —
it can show boot messages before the operating system has even finished
loading, all the way down to the very first startup code. That's exactly
the window you most need to see into during testing (is the board even
alive before any software starts).

**Your specific setup:**
- **3-pin header** (TX, RX, ground) — a plain 2.54mm-spacing through-hole
  header, LCSC part C49257. Wired only to the CM5's connector pins — the
  Hailo-8L and the camera have nothing to send over UART.
- **3.3V logic level, not 5V** — this is the part that will damage a pin
  if done wrong. An external USB-to-serial adapter (built around a CP2102
  or FT232RL chip) connects your laptop's USB port to this header. These
  adapters commonly support both 3.3V and 5V through a physical switch, and
  **several ship with the switch defaulted to 5V** — check the switch
  position before every first connection, don't trust the printed label.
- Terminal settings: 115200 baud rate, 8 data bits, no parity, 1 stop bit
  (often written "115200 8N1") — use PuTTY on Windows, or `screen`/`minicom`
  in Git Bash/WSL (Linux-style terminal tools).
- This only lets you **watch** what's happening — it's not a way to flash
  new software. Flashing the CM5's storage is a completely separate method
  (USB flashing port + the nRPIBOOT jumper wire).

---

## I2C (Inter-Integrated Circuit)

**What it's for on this board:** two separate, unrelated jobs happen to
use the same type of connection:
1. **Camera control** — exposure, gain, and resolution settings sent to
   the camera sensor. This is *separate* from the camera's video data
   wires (which carry the actual picture stream) — easy to miss because
   both connect to the same camera part, but they're two different
   physical connections doing two different jobs.
2. **Power negotiation readback** — two pins (CFG2/CFG3) on the power
   negotiation chip are wired to the CM5's I2C connection, letting the
   software check which voltage actually got negotiated and monitor the
   live current during testing.

**How it physically works:**
- **2 shared wires: SCL (clock) and SDA (data)**, plus a common ground.
  Unlike UART, there *is* a shared clock wire (SCL) — one device (the
  "master," here the CM5) generates it, and every other device reads and
  writes SDA in sync with it.
- Because it's a shared connection, every device needs a unique
  **address** (a small number) so the CM5 can say "I'm talking to device
  0x1A" and only that one device responds. This is what lets the camera and
  the power chip share the same two wires without interfering with each
  other — they're different addresses on the same shared connection.
- **Pull-up resistors are required, not optional.** I2C only lets a device
  actively pull the wire *low* — it can never actively push it *high*.
  Pulling it back up to a valid "high" signal is the pull-up resistor's
  job, automatically, whenever nothing is pulling the wire low. Without
  pull-up resistors, the connection simply doesn't work — the wires just
  float and never reach a valid high signal.

**Your specific setup:**
- Camera: Raspberry Pi's own camera modules (Camera Module 3 / IMX708)
  don't include pull-up resistors on-board, so the carrier board has to add
  them itself — the standard Raspberry Pi value is **1.8k ohms to 3.3V on
  both SCL and SDA**. Since the camera module has none of its own, there's
  no risk of "doubling up" (two sets of pull-ups on the same connection,
  which can distort the signal) — but this still needs to be re-confirmed
  once the actual camera model is picked (open item).
- Power chip's CFG2/CFG3: comes along "for free" with the resistor-based
  power-request setup — no added complexity, just wiring these two pins to
  the existing I2C connection instead of leaving them unused.

---

## Quick comparison table

| | UART | I2C |
|---|---|---|
| Wires (not counting ground) | 2 (TX, RX) | 2 (SCL, SDA) |
| Connects | Exactly two devices | Many devices, shared |
| Clock | None — both sides agree on a speed ahead of time | Shared clock wire (SCL) |
| Addressing | Not needed | Every device has an address |
| Needs pull-up resistors? | No | Yes, required |
| Used for, on this board | CM5 debug console only | Camera control + power chip readback |

---

## Where this stands in your design

| Item | Status |
|---|---|
| UART header | Locked — 3-pin, LCSC C49257, 115200 8N1 |
| UART adapter | External, bought separately — must check the 3.3V switch position every time |
| I2C pull-up resistors (camera) | Value locked (1.8k ohms to 3.3V) — exact placement pending the final camera model |
| I2C pull-up resistors (power chip) | Shares the same connection as the camera — confirm no conflict once the camera model is picked |
| I2C address conflicts | Not yet checked — worth confirming the camera's address and the power chip's I2C behavior don't collide once both are on the same connection |
