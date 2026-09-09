# Design Audit — 2026-09-08

## Status and scope

This is a local repository and CAD-state review, not a fabrication approval.
It records observed problems, open decisions, and a recommended work order. It
does not supersede any locked design decision in `documentation.md`.

The architecture remains a CM5 carrier board with a Hailo-8L M.2 module,
CSI-2 camera, dedicated USB-C power input, and separate USB-C programming and
recovery connection. The implementation is still in the schematic phase. The
repository contains six schematic documents and no PCB layout document.

## Ranked issues and decisions

### 1. Correct both CM5 connector libraries before further wiring

**Issue — release blocker:** The two Amphenol `10164227-1001A1RLF` connector
libraries are not yet safe for PCB transfer.

- Connector 1 must restore and connect required `GND` pins 3–6, 9–12, and
  15–20.
- Connector 2 uses global CM5 schematic pin numbers 101–200, while the
  physical connector footprint has pads 1–100. Its Altium PCB Model Pin Map
  must explicitly map schematic pin 101 to pad 1 through schematic pin 200 to
  pad 100.
- After correction, compile the project and inspect the schematic-to-PCB ECO
  for unmatched pins, pads, or unintended net assignments.

**Decision needed:** None about the electrical intent; these are mandatory
library corrections. Do not route, fabricate, or release the PCB until they
are verified.

### 2. Reset the project scope and schedule

**Issue:** The documented schedule called for schematic completion by August
9, layout completion by August 23, and ordering around September 16. On
September 8 the CM5 interfaces remain incomplete, the M.2 and new combined
sheet are blank, major power and camera decisions remain open, and no
`.PcbDoc` exists. The September 16 order target is therefore not credible.

**Decision needed:** Choose the objective for Rev A:

- complete CM5 + Hailo-8L + camera carrier board; or
- a smaller bring-up revision with intentionally reduced scope.

Once that choice is made, replace the obsolete schedule with milestones based
on schematic completion, review, PCB layout, fabrication, and bring-up.

### 3. Resolve the Altium sheet structure and preserve current work

**Issue:** `Schematics & PCB/M.2 Connection.SchDoc` is tracked but visually
blank. `Schematics & PCB/Buck to M.2 & CSI.SchDoc` and its preview are new,
blank, untracked, and absent from `Project Watchdog.PrjPcb`. The project
structure currently lists only the five older schematic sheets.

**Decision needed:** Choose which M.2/CSI sheet structure is authoritative.
Add the intended sheet or sheets to the Altium project, and remove or archive
the duplicate only after confirming that it contains no needed work. Do not
discard the current uncommitted documentation, library, history, or schematic
changes.

### 4. Complete and validate the CM5 schematic

**Issue:** Both 100-pin CM5 connector sheets are largely unwired. Decisions
recorded in Markdown are not yet a complete electrical implementation.

The schematic must implement and verify:

- every required CM5 5 V and ground contact;
- GPIO voltage reference;
- PCIe lane, reference clock, reset, clock request, and optional wake;
- camera CSI-2 lanes, I2C, and camera control signals;
- USB 2.0 programming/recovery path;
- `nRPIBOOT`, reset/power control, and debug UART;
- explicit no-connect markers for intentionally unused pins.

**Decision needed:** Resolve any still-unused multifunction pins only when a
subsystem requires them. After wiring, run Altium compile/ERC and review every
warning rather than suppressing errors globally.

### 5. Lock the complete power architecture against peak load

**Post-audit update:** The local Hailo regulator selection was closed after
this audit: `TPS54302DDCR` (JLCPCB/LCSC `C311983`) is the selected 3 A
5 V-to-3.3 V buck. The selection resolves the first action below, but not the
schematic implementation, transient/thermal verification, or reset sequencing.

**Issue:** The documented approximately 13 W budget is based substantially on
typical loading, while the Hailo-8L alone is documented at up to 6.6 W / 2 A.
The design must be checked for simultaneous peak loads, startup transients,
conversion losses, thermal derating, cable/charger capability, and regulator
current limits.

**Decisions and work required:**

- **Resolved after audit:** use `TPS54302DDCR` (`C311983`) as the local
  5 V-to-3.3 V Hailo switching regulator; its supporting circuit and margins
  still require verification.
- Select the Hailo power-switch/reset-sequencing implementation so 3.3 V is
  stable before reset is released.
- Finalize the simplified USB input-protection topology after removal of the
  TPS25947 eFuse.
- Verify the MP2329 feedback/compensation parts, inductor value and saturation
  current, capacitor ratings, efficiency, and thermal layout.
- Recalculate the USB-PD input and `5V_MAIN` capacity from a defensible peak
  load case before freezing component ratings.

### 6. Define behavior before or without successful USB-PD negotiation

**Issue:** The current documentation says the board refuses to operate from a
5 V-only charger. Removing the eFuse also removed a possible means of gating
the downstream converter. The behavior during initial 5 V attachment, failed
9 V negotiation, cable removal, and negotiation restart is not yet defined.

**Decision needed:** Define how the CH224A status/power-good signal controls
the MP2329 or a separate UVLO/load-switch stage. Confirm that the circuit
cannot enter a marginal 5 V brownout state and that the selected charger and
cable profile is unambiguous.

### 7. Implement and verify the Hailo M.2 mapping in CAD

**Issue:** The Hailo pin assignment is now documented, but the corresponding
schematic sheet remains blank. The imported `C601195.SchLib` reportedly has 68
schematic pins for a 67-contact M-key connector.

**Decisions and work required:**

- Identify the extra library pin from the connector drawing as an electrical,
  shield, or mechanical contact before assigning it.
- Implement all five `3V3_HAILO` pins and nine electrical grounds.
- Verify endpoint TX-to-host RX and endpoint RX-to-host TX, including polarity.
- Implement `REFCLK`, `PERST#`, and `CLKREQ#`; decide whether `PEWAKE#` remains
  unconnected.
- Mark lane 1, module-detection contacts, and other unused contacts explicitly
  as no-connect where appropriate.
- Do not add a second set of PCIe transmit AC-coupling capacitors unless a
  reviewed source requires it.

### 8. Select the exact camera and freeze its interface

**Issue:** Without the exact camera module, the design cannot finalize the CSI
lane count, flex-cable pinout and contact orientation, supply rails, I2C
pull-ups, control signals, or connector footprint. The previously listed
camera connector library is not present in the current Altium project.

**Decision needed:** Select the camera module and verify, from its documentation
and the CM5 reference design:

- two-lane versus four-lane CSI-2 operation;
- cable and connector orientation;
- 3.3 V and any 1.8 V requirement;
- I2C pull-up ownership and value;
- camera enable/control mapping;
- connector sourcing and footprint.

### 9. Complete the programming and recovery hardware

**Issue:** The architecture calls for a dedicated programming USB-C port, but
the corresponding complete schematic is not present.

Required implementation includes USB D+/D−, low-capacitance ESD protection,
USB-C device-side CC termination, safe VBUS presence sensing, ground, an
accessible `nRPIBOOT` control, reset/power control, and debug UART. Programming
VBUS must not be tied blindly to `5V_MAIN`, which would allow the host and main
converter to become competing power sources.

**Decision needed:** The dedicated connector is the latest documented choice.
Only reopen it if board area forces a formal change to a pogo/test-pad method.

### 10. Define mechanical and thermal constraints before layout

**Issue:** No PCB document, board outline, placement plan, or documented
mechanical envelope exists.

**Decisions needed:** Freeze the board dimensions, mounting holes, CM5 and M.2
retention geometry, USB and camera connector edges/orientations, enclosure
constraints, CM5 wireless antenna keepout, heatsink access, and fan/passive
cooling plan. Perform a 1:1 printed fit check with the real CM5 before release.

### 11. Establish PCB rules and release gates

**Issue:** The intended four-layer controlled-impedance construction is
documented, but it is not implemented in a PCB document.

Required work includes the exact JLCPCB stackup, differential-pair impedance
rules, widths and gaps, length/skew limits, continuous reference planes,
return-path rules, power-current constraints, clearances, and component/board
edge rules.

Release evidence should include:

- clean or fully adjudicated schematic ERC;
- reviewed schematic-to-PCB ECO with no unexplained differences;
- clean or fully adjudicated PCB DRC;
- connector symbol-to-footprint and pad-map checks;
- 1:1 mechanical fit check;
- reviewed BOM, fabrication, drill, placement, and assembly outputs.

### 12. Close manufacturing and repository hygiene items

**Issues:** JLCPCB's treatment and pricing of through-hole connector assembly
has not been confirmed. Part availability must be rechecked once the BOM is
stable. The working tree also contains uncommitted documentation, library,
history, and schematic work.

**Decisions and work required:**

- Confirm assembly support for the CM5 connectors, M.2 socket, and USB-C shell
  or mounting contacts.
- Recheck stock and alternates when the schematic and BOM are stable, rather
  than redesigning around temporary stock observations too early.
- Review and commit the current local work as a coherent checkpoint only after
  Bill explicitly authorizes the commit/push step.

## Recommended execution order

1. Correct and verify the CM5 connector libraries.
2. Decide Rev A scope and replace the obsolete schedule.
3. Clean up the Altium sheet/project structure without losing current work.
4. Complete CM5 and M.2 schematic wiring.
5. Close the Hailo power, sequencing, input-protection, and peak-budget work.
6. Select the camera and complete its power/control/CSI interface.
7. Complete programming, recovery, reset, UART, and test-point circuitry.
8. Compile and review the complete schematic.
9. Freeze mechanical constraints, create the PCB, and implement stackup/rules.
10. Complete layout, formal verification, manufacturing review, and release.

Pre-PCB Hailo testing on the existing Raspberry Pi 5 should run in parallel
when practical. It validates the module and software stack but does not replace
verification of the custom CM5 PCIe routing.
