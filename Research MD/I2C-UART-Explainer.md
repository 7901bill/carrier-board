# I2C and UART — A Working Explainer

Last updated: 2026-07-30

Two different serial buses show up on this board, for two different jobs.
This walks what each one is, why it's shaped the way it is, and exactly
where it appears on *your* design.

---

## The core distinction, up front

**UART** is point-to-point: two chips, one wire each direction, no
addressing. **I2C** is a shared bus: many chips, two shared wires, every
device gets an address. If you only remember one thing, remember that —
it explains almost every difference below.

---

## UART (Universal Asynchronous Receiver/Transmitter)

**What it's for on this board:** the debug console. It's the *only* way to
see boot output from the CM5 — nothing else on the board (Hailo-8L, camera)
produces any output of its own to watch.

**How it physically works:**
- **2 signal wires, one direction each: TX (transmit) and RX (receive)**,
  plus a shared GND. That's it — no clock wire.
- "Asynchronous" means there's no separate clock signal keeping the two
  sides in lock-step. Instead, both sides agree in advance on a **baud
  rate** (yours: 115200) — a fixed timing rate they both count against
  independently. Each byte is framed with a start bit and stop bit so the
  receiver knows exactly when a new byte begins, even with no shared clock.
- Because there's no clock line, **TX and RX must be cross-wired**: one
  device's TX goes to the other device's RX, and vice versa. Plug two TX
  pins into each other and nothing works — this is the single most common
  UART wiring mistake.

**Why it's the debug path specifically:** UART is dead simple and doesn't
need the OS or any driver stack to be working — it can output boot
messages before Linux has even finished loading, all the way down to the
bootloader. That's exactly the failure window you most need visibility
into during bring-up (is the board even alive before software starts).

**Your specific implementation:**
- **3-pin header** (TX, RX, GND) — plain 2.54mm 1×3P through-hole, LCSC
  C49257. Off the CM5's DF40 pins only; Hailo-8L and the camera have
  nothing to say over UART.
- **3.3V logic, not 5V** — this is the part that will kill a pin if you
  get it wrong. An external USB-to-TTL adapter (CP2102 or FT232RL-based)
  connects your laptop's USB port to this header. These adapters commonly
  support both 3.3V and 5V logic via a physical switch, and **several ship
  defaulting to 5V** — verify the switch position before every first
  connection, don't trust the printed label.
- Terminal settings: 115200 baud, 8 data bits, No parity, 1 stop bit
  ("115200 8N1") — PuTTY on Windows, or `screen`/`minicom` in Git Bash/WSL.
- This is **read-only visibility**, not a flashing path. Flashing the
  eMMC is a completely separate mechanism (USB provisioning port +
  nRPIBOOT jumper).

---

## I2C (Inter-Integrated Circuit)

**What it's for on this board:** two separate, unrelated jobs happen to
use the same bus type:
1. **Camera control** — exposure, gain, resolution settings sent to the
   CSI camera sensor. This is *separate* from the CSI data lanes (which
   carry the actual pixel stream) — easy to miss because both go to the
   same connector/component, but they're two different physical
   interfaces doing two different jobs.
2. **CH224A negotiation readback** — CFG2/CFG3 on the PD sink chip are
   broken out to the CM5's I2C bus, letting software read back which
   voltage was actually negotiated and monitor live current draw during
   bring-up.

**How it physically works:**
- **2 shared wires: SCL (clock) and SDA (data)**, plus common GND. Unlike
  UART, there *is* a shared clock (SCL) — one device (the "master," here
  the CM5) generates it, and all devices read/write SDA in sync with it.
- Because it's a shared bus, every device needs a unique **address** (a
  7-bit or 10-bit number) so the master can say "I'm talking to device
  0x1A" and only that device responds. This is what lets the camera and
  the CH224A coexist on the same two wires without interfering — they're
  different addresses on the same electrical bus.
- **Pull-up resistors are mandatory and not optional.** I2C uses
  "open-drain" signaling — a device can only actively pull the line
  *low*, never actively drive it *high*. Pulling it back up to logic-high
  is the pull-up resistor's job, passively, whenever no device is pulling
  low. Without pull-ups, the bus simply doesn't work — the lines float
  and never reach a valid high state.

**Your specific implementation:**
- Camera: RPi's own camera modules (Camera Module 3 / IMX708) carry **no
  on-board pull-ups**, so the carrier board must add them itself — the
  standard RPi value is **1.8kΩ to 3.3V on both SCL and SDA**. Since the
  module has none of its own, there's no risk of "double pull-up" (two
  sets of pull-ups on the same bus, which can over-pull the line and
  distort signal timing) — but this still needs reconfirming once the
  actual camera SKU is picked (open item).
- CH224A CFG2/CFG3: rides along "for free" alongside the resistor-strapped
  voltage-request config — no added board complexity, just wiring these
  two pins to the existing I2C bus instead of leaving them unconnected.

---

## Quick comparison table

| | UART | I2C |
|---|---|---|
| Wires (excl. GND) | 2 (TX, RX) | 2 (SCL, SDA) |
| Topology | Point-to-point (one device pair) | Shared bus (many devices) |
| Clock | None — both sides agree on a baud rate | Shared clock line (SCL) |
| Addressing | None needed | Every device has an address |
| Needs pull-ups? | No | Yes, mandatory |
| On this board | CM5 debug console only | Camera control + CH224A readback |

---

## Where this stands in your design

| Item | Status |
|---|---|
| UART header | Locked — 3-pin, LCSC C49257, 115200 8N1 |
| UART adapter | External, user-supplied — must verify 3.3V switch position each time |
| I2C pull-ups (camera) | Value locked (1.8kΩ to 3.3V) — placement pending actual camera SKU |
| I2C pull-ups (CH224A) | Rides on the same bus as the camera — confirm no conflict once camera SKU is picked |
| I2C address conflicts | Not yet checked — worth confirming the camera's address and CH224A's I2C behavior don't collide once both are on the same bus |
