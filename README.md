# Carrier Board — Read This First

## ⛔ PCB release blocked: CM5 connector libraries need correction

Do **not** release, fabricate, or route the CM5 carrier PCB until the two
Amphenol `10164227-1001A1RLF` connector library issues below are resolved and
an Altium compile/ECO reports no unmatched pins or pads.

1. **CM5 connector 1 (logical pins 1–100):** restore and connect these
   required `GND` pins: `3–6`, `9–12`, and `15–20`.
2. **CM5 connector 2 (logical pins 101–200):** add an explicit Altium PCB
   Model Pin Map so schematic pin `101` maps to physical footprint pad `1`,
   through schematic pin `200` mapping to physical pad `100`.

The second connector intentionally starts at global CM5 pin 101; its physical
Amphenol contacts remain numbered 1–100. This mapping is mandatory for correct
net assignment on the PCB.

See [CM5 connector wiring and bring-up](Documentation/Research%20MD/CM5-Connector-Wiring-and-Bringup.md)
and the current project journal before continuing.

