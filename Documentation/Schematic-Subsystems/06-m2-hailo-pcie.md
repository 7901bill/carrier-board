# 06 — Hailo-8L M.2 and PCIe

Last updated: 2026-09-19

## Open review actions — 2026-09-19

- Open mechanical check: selected CN3 is `91302-42-067RDM` (4.2 mm),
  but its footprint name contains `91302-32-067RDM`. Compare manufacturer
  drawings, pad geometry, module height and clearances. The name mismatch
  alone does not prove the footprint is wrong.
- Power dependency: fix disconnected C8/C9 in [03](03-hailo-power-sequencing.md).
  Direct PERST# has no supply-good gating; startup/brownout timing is open.
- Confirm stackup/impedance rules and module mounting before routing.

These actions are not implemented. Evidence and parts caveats are in the
[review report](../Parts-and-Schematic-Review-2026-09-19.md).

## Subsystem purpose

Connect the Hailo-8L module to the CM5 over PCIe Gen 2 x1 and provide its
power, clock, reset, and ground connections.

## Current status

**Schematic wiring complete.** The M.2 power, ground, PCIe lane 0, reference
clock, reset, and clock-request signals are connected to the CM5 connector.
Unused lane, wake, configuration, and remaining contacts are intentionally
left unconnected. PCB differential-pair rules, routing, and length tuning
remain layout-phase work.

## Confirmed parts and architecture

- Socket: UMAX `91302-42-067RDM`, LCSC `C601195`.
- The socket is a 67-contact M-key socket and accepts the Hailo-8L B+M module.
- Link: PCIe Gen 2 x1 from the CM5.
- Only PCIe lane 0 is used; lane 1 receives explicit no-connect markers.
- The M.2 module includes transmit-side AC-coupling capacitors; the carrier
  must not add a duplicate set without a reviewed reason.

## Confirmed power and ground mapping

- `3V3_HAILO`: M.2 pins 2, 4, 70, 72, and 74.
- Ground: pins 3, 27, 33, 39, 45, 51, 57, 71, and 73.
- All listed power and ground contacts must be connected.

## Confirmed PCIe mapping

| M.2 pin/signal | CM5 pin/signal |
|---|---|
| 41 `PETn0` | 118 `PCIe_RX_N` |
| 43 `PETp0` | 116 `PCIe_RX_P` |
| 47 `PERn0` | 124 `PCIe_TX_N` |
| 49 `PERp0` | 122 `PCIe_TX_P` |
| 53 `REFCLKn` | 112 `PCIe_CLK_N` |
| 55 `REFCLKp` | 110 `PCIe_CLK_P` |
| 50 `PERST#` | 109 `PCIe_nRST` |
| 52 `CLKREQ#` | 102 `PCIe_CLK_nREQ` |

The endpoint's transmit signals connect to the host's receive signals, and the
endpoint's receive signals connect to the host's transmit signals.

## Confirmed no-connect intent

- Lane 1 pins 29, 31, 35, and 37 are unused.
- Configuration contacts 1, 21, and 75 are module-grounded detection bits and
  remain open unless detection is implemented; pin 69 is NC on the module.
- The complete unused-pin list is maintained in
  `Documentation/Research MD/PCIe-x1-Differential-Pairs-Explainer.md`.
- M.2 pin 54 `PEWAKE#` and CM5 pin 104 `PCIE_nWAKE` are unused in Rev A.
- CM5 pin 106 `PCIE_PWR_EN` is unused because Rev A uses an always-on
  `3V3_HAILO` regulator and omits the external PCIe load switch.

## Completed schematic content

- All confirmed PCIe, clock, reset, power, and ground connections.
- Explicit no-connect markers on every unused electrical contact.
- Local bulk and high-frequency M.2 decoupling.
- Net-label continuity between the M.2 sheet and CM5 connector sheet.

## PCB-layout work remaining

- Define `PCIe_TX_P/N`, `PCIe_RX_P/N`, and `PCIe_CLK_P/N` as differential
  pairs.
- Derive 85 Ω differential geometry from the final JLCPCB stackup.
- Route each pair over continuous ground and tune P/N skew within each pair.
- Keep the pairs away from the TPS54302 switch node and inductor.
- Verify useful rail, reset, clock-request, and ground test access without
  adding stubs to high-speed pairs.

## Definition of done

- Pin mapping is checked against the Hailo module datasheet and CM5 datasheet.
- Polarity and TX/RX direction are reviewed independently.
- Power, ground, clock, and control connections are complete.
- All unused contacts are explicitly marked.
- The extra library pin is identified and documented.
- Reset release is coordinated with `3V3_HAILO` stability.

## References

- `Documentation/Research MD/PCIe-x1-Differential-Pairs-Explainer.md`.
- Hailo-8L M.2 Key B+M ET Module Data Sheet Rev. 4.0.
- CM5 datasheet and Raspberry Pi M.2 HAT+ reference schematic.

## Session notes

- 2026-09-18: Initial subsystem draft created from the locked pin table.
- 2026-09-19: M.2-to-CM5 schematic wiring completed. Confirmed that pin 41
  `PETn0` connects to CM5 `PCIe_RX_N` pin 118 and pin 43 `PETp0` connects to
  `PCIe_RX_P` pin 116; pin 42 is not part of the lane-0 connection.
