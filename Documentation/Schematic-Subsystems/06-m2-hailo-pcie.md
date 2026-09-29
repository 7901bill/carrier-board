# 06 — Hailo-8L M.2 and PCIe

Last updated: 2026-09-28

## Open review actions — 2026-09-24

- **HIGH PRIORITY - CN3 release blocker. Resolve before PCB fabrication or
  connector procurement.** The selected schematic and BoM DesignItemId is
  UMAX `91302-42-067RDM` (LCSC `C601195`), while the placed PCB footprint
  and embedded STEP model are named for `91302-32-067RDM`. The supplier lists
  the selected `-42-` variant at 4.2 mm and the `-32-` variant at 3.2 mm.
  These are distinct orderable parts. Their name difference does not prove a
  copper land-pattern mismatch, but unverified mating height, locating posts,
  or standoff geometry could prevent the Hailo module from seating and force
  a board rework or respin.
  Compare manufacturer drawings for both variants: contact and mounting pad
  layout, locating posts, board edge, card mating plane, module standoff, and
  nearby clearance. Record the drawing revisions and verified intended part.
  If `-42-` is intended, use or validate a `-42-` footprint and 3D model; if
  `-32-` is intended, correct the schematic part identity and supplier code.
  Refresh the BoM, transfer the change to the PCB, and confirm that CAD and
  purchasing identifiers agree. Do not close this item on matching names alone.
- The latest 2026-09-28 LiveBOM save now agrees with the schematic on CN3's
  Comment, `Name=C601195`, `Source=LCSC`, and selected part. This resolves
  the earlier saved-parameter discrepancy; the `-42-` part versus `-32-`
  footprint/3D mechanical review remains open. See the consolidated
  [main design status](../documentation.md).
- Power dependency: fix disconnected C8/C9 in [03](03-hailo-power-sequencing.md).
  Direct PERST# has no supply-good gating; startup/brownout timing is open.
- Confirm stackup/impedance rules and module mounting before routing.

These actions are not implemented. Current release blockers are consolidated
in the [main design status](../documentation.md).

## Subsystem purpose

Connect the Hailo-8L module to the CM5 over PCIe Gen 2 x1 and provide its
power, clock, reset, and ground connections.

## Current status

**Schematic wiring complete.** The M.2 power, ground, PCIe lane 0, reference
clock, reset, and clock-request signals are connected to the CM5 connector.
Unused lane, wake, configuration, and remaining contacts are intentionally
left unconnected. PCB differential-pair rules, routing, and length tuning
remain layout-phase work.

**PCB layout setup:** CN2 and CN3 are placed, and the configured stack places
L1 over a continuous L2 ground reference. The layout note reports the 90-ohm
profile calculation complete, but the saved PCB still has no PCIe pair objects
or populated PCIe pair class, and its differential routing rule remains the
generic 15 mil/10 mil placeholder. Create the three pair objects, populate the
PCIe class, link its rule to the 90-ohm profile, and verify the geometry with
JLCPCB before routing on L1. The CN3 part/footprint/STEP identity blocker still
must be resolved before placement is considered mechanically final.

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
- Route all three pairs at 90 ohms differential, as specified by the current
  official CM5 datasheet. This supersedes the older 85-ohm project note. The
  Hailo module datasheet does not state a conflicting value and instead refers
  the interface to the PCIe M.2 specification.
- Derive the actual width and gap for 90 ohms from the final JLCPCB stackup; do
  not use the PCB document's generic 15 mil/10 mil placeholder geometry.
- Route each pair over continuous ground and tune P/N skew within each pair.
- Keep the pairs away from the TPS54302 switch node and inductor.
- Verify useful rail, reset, clock-request, and ground test access without
  adding stubs to high-speed pairs.
- Do not add external parallel termination across the pairs. CM5 already has
  AC-coupling capacitors on its PCIe transmitter, and the M.2 module provides
  transmitter-side coupling for the opposite direction; do not duplicate
  those capacitors without a reviewed device-specific reason.

## Definition of done

- Pin mapping is checked against the Hailo module datasheet and CM5 datasheet.
- Polarity and TX/RX direction are reviewed independently.
- Power, ground, clock, and control connections are complete.
- All unused contacts are explicitly marked.
- The extra library pin is identified and documented.
- CN3's selected MPN, supplier code, PCB land pattern, 3D model, card seating
  height, and module standoff are checked against manufacturer drawings; the
  refreshed BoM and PCB agree on the verified variant.
- Reset release is coordinated with `3V3_HAILO` stability.

## References

- `Documentation/Research MD/PCIe-x1-Differential-Pairs-Explainer.md`.
- Hailo-8L M.2 Key B+M ET Module Data Sheet Rev. 4.0.
- CM5 datasheet and Raspberry Pi M.2 HAT+ reference schematic.
- [Selected `-42-` connector, C601195](https://jlcpcb.com/partdetail/UMAX-91302_42067RDM/C601195)
  and [`-32-` connector, C1509730](https://item.szlcsc.com/1600530.html);
  use their manufacturer drawings for the compatibility decision.

## Session notes

- 2026-09-18: Initial subsystem draft created from the locked pin table.
- 2026-09-19: M.2-to-CM5 schematic wiring completed. Confirmed that pin 41
  `PETn0` connects to CM5 `PCIe_RX_N` pin 118 and pin 43 `PETp0` connects to
  `PCIe_RX_P` pin 116; pin 42 is not part of the lane-0 connection.
- 2026-09-24: Raised the CN3 `-42-` purchasing part versus `-32-` PCB
  footprint/STEP identity to a high-priority release blocker. Mechanical and
  land-pattern compatibility remain unverified; no CAD change was made.
- 2026-09-28: Verified the current CM5 routing guidance and locked all three
  used PCIe pairs, including reference clock, to 90 ohms differential. This
  supersedes the earlier 85-ohm note. Pair creation, stackup geometry, routing,
  and tuning remain PCB work; no CAD change was made.
- 2026-09-28: Layout setup subsequently placed CN2/CN3 and reportedly
  calculated the 90-ohm profile. Saved-CAD review still found zero pair
  objects and the generic unlinked rule, so pair/class/rule completion remains
  open before routing.
