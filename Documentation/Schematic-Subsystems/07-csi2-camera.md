# 07 — CSI-2 Camera Interface

Last updated: 2026-09-19

## Purpose

Connect a Raspberry Pi camera module to the CM5 using the 22-pin FPC interface,
including video lanes, control, power, and grounds.

## Current status

**Schematic wiring complete.** All four MIPI data lanes, MIPI clock, camera
I²C, both camera GPIO controls, `3V3_CAMERA`, and ground contacts are connected
between the 22-pin FPC connector and the CM5 connector symbols. PCB
differential-pair rules, routing, and cable-orientation inspection remain
layout/review work.

## Confirmed design basis

- Camera: standard Raspberry Pi Camera Module 3 using the IMX708 sensor (not
  Camera Module 3 Wide).
- The carrier uses the same 22-contact, 0.5 mm-pitch style used for the
  Raspberry Pi 5 camera/display interface.
- Current carrier connector: Hirose `FH55-22S-0.5SH`, LCSC `C5182313`, a
  22-position, 0.5 mm-pitch, bottom-contact front-flip FPC connector.
- The normal Raspberry Pi 5 camera cable adapts the Pi 5-style 22-pin end to
  the standard Camera Module 3 connector.
- Camera video uses CSI-2 differential data and clock pairs.
- Camera configuration uses the CM5 camera I²C bus, not the CSI-2 data lanes.
- CM5 pin 80 `SCL0` maps to `CAM_I2C_SCL`.
- CM5 pin 82 `SDA0` maps to `CAM_I2C_SDA`.
- CM5 pin 97 `CAM_GPIO0` and pin 100 `CAM_GPIO1` provide camera controls.
- Camera connector power is `3V3_CAMERA` on pin 22.
- A separate 1.8 V carrier rail is not required for Camera Module 3.
- The current CM5 documentation states that SCL0/SDA0 have internal 1.8 kΩ
  pull-ups to the CM5 3.3 V rail. Do not fit an additional pair by default.

## Confirmed connector mapping

| CSI pin/signal | CM5 pin/signal |
|---|---|
| 2 `CAM_D0_N` | 115 `MIPI0_D0_N` |
| 3 `CAM_D0_P` | 117 `MIPI0_D0_P` |
| 5 `CAM_D1_N` | 121 `MIPI0_D1_N` |
| 6 `CAM_D1_P` | 123 `MIPI0_D1_P` |
| 8 `CAM_CLK_N` | 127 `MIPI0_C_N` |
| 9 `CAM_CLK_P` | 129 `MIPI0_C_P` |
| 11 `CAM_D2_N` | 133 `MIPI0_D2_N` |
| 12 `CAM_D2_P` | 135 `MIPI0_D2_P` |
| 14 `CAM_D3_N` | 139 `MIPI0_D3_N` |
| 15 `CAM_D3_P` | 141 `MIPI0_D3_P` |
| 17 `CAM_IO0` | 97 `CAM_GPIO0` |
| 18 `CAM_IO1` | 100 `CAM_GPIO1` |
| 20 `CAM_I2C_SCL` | 80 `SCL0` |
| 21 `CAM_I2C_SDA` | 82 `SDA0` |
| 22 `3V3_CAMERA` | AP2112 output |

CSI contacts 1, 4, 7, 10, 13, 16, and 19 connect to ground. The standard
Camera Module 3 uses two data lanes through the normal 22-to-15-pin cable;
wiring lanes 2 and 3 preserves the standard four-lane 22-pin interface.

## Completed schematic content

- `C5182313` FPC connector with verified contact numbering and cable orientation.
- All required CSI-2 data and clock pairs.
- Camera I²C and control connections.
- `3V3_CAMERA`, all required grounds, and local decoupling.
- Explicit no-connect markers on unused contacts, if any.
- Useful power, control, and ground test access without stubbing high-speed
  CSI-2 pairs.

## PCB-layout and review work remaining

- Verify FPC contact-side orientation and pad 1 against the `C5182313`
  connector drawing and the selected Raspberry Pi camera cable.
- Define all four data pairs plus the clock pair as PCB differential pairs.
- Derive the required MIPI geometry from the final JLCPCB stackup, route over
  continuous ground, and tune P/N skew within each pair.
- Keep test access off the MIPI pairs and verify connector-shell grounding.

## Definition of done

- The exact camera, cable, and connector drawings agree on contact orientation.
- Lane count and every CSI-2 polarity are checked against authoritative sources.
- Camera power, grounds, I²C, and control signals are complete.
- Pull-up ownership is documented without duplicating the CM5 pull-ups.
- No high-speed signal is left ambiguous or mislabeled.

## References

- `Documentation/documentation.md`, current camera decisions.
- Current CM5 datasheet and Camera Module 3 documentation.
- Official CM5 IO camera reference circuit.

## Session notes

- 2026-09-18: Initial subsystem draft created. Later confirmed pull-up guidance
  supersedes the older I²C explainer's external-pull-up recommendation.
- 2026-09-19: CSI-to-CM5 schematic wiring completed. Corrected the CM5 camera
  lane interpretation: CM5 pin 115 is `MIPI0_D0_N`; pin 141 is
  `MIPI0_D3_P`, not lane 0 negative. Updated the connector-library display
  labels accordingly.
