# Watchdog LCSC replacement review

Reviewed 2026-10-14; recommendations rechecked in a live browser on https://www.lcsc.com/ at approximately 16:42 EDT. This is a sourcing and schematic compatibility review; the Altium BOM, schematics, and PCB have not been modified. Stock and prices are the figures displayed on the linked pages when checked and should be refreshed at purchase.

## Project evidence

Read Schematics & PCB/BOM.BomDoc and all four current SchDoc files, plus the four target SchLib files. All target uses are in Power Rails.SchDoc and USBC_Protection.SchDoc.

| Original LCSC ID | Manufacturer part | References / quantity per board | Required nominal specification |
| --- | --- | --- | --- |
| C15849 | Samsung CL10A105KB8NNNC | C1 (USB-C protection), C10 and C15 (power rails); 3 | 1 µF, ±10%, 50 V, X5R, 0603 |
| C466768 | SANYEAR C0603X7R104K250NT | C4 (power rails); 1 | 100 nF, ±10%, 25 V, X7R, 0603 |
| C1671 | Samsung CL10C470JB8NNNC | C11 (power rails); 1 | 47 pF, ±5%, 50 V, C0G, 0603 |
| C5349327 | MPS MP2329GG-Z | U5 (power rails); 1 | 6.5 A buck, 4.5–24 V input, QFN-11 2 × 2 mm |

C4 bypasses the 9V_Input rail. C1 bypasses the USB power input; C10 decouples U5 VCC; C15 bypasses the 5 V input of the AP2112. C11 is across the upper feedback resistor of the TPS54302 M.2 3.3 V converter, so preserve its capacitance and C0G/NP0 dielectric.

## Recommended capacitor substitutions

| Replace | Recommended LCSC part | Manufacturer part | Compatibility assessment | Displayed stock | Entry price / minimum |
| --- | --- | --- | --- | --- | --- |
| C15849 | [C128624](https://www.lcsc.com/product-detail/C128624.html) | YAGEO CC0603KRX5R9BB105 | Same 1 µF, ±10%, 50 V, X5R and 0603 | 49,420 | $0.0294 each / 20 |
| C466768 | [C24452](https://www.lcsc.com/product-detail/C24452.html) | Samsung CL10B104JB8NNNC | 100 nF, X7R, 0603; voltage increases to 50 V and tolerance tightens to ±5% | 481,580 | $0.0184 each / 20 |
| C1671 | [C105622](https://www.lcsc.com/product-detail/C105622.html) | YAGEO CC0603JRNPO9BN470 | Same 47 pF, ±5%, 50 V, 0603; NP0 is C0G | 1,046,500 | $0.0036 each / 100 |

These are suitable nominal electrical and package substitutions for the identified uses, without an intended circuit or footprint change. The two YAGEO parts have manufacturer-confirmed 1.6 × 0.8 mm bodies: [1 µF specification](https://yageogroup.com/download/specsheet/CC0603KRX5R9BB105), [47 pF specification](https://yageogroup.com/download/specsheet/CC0603JRNPO9BN470). Final assembly clearance/pad geometry and bench behavior were not validated.

First-pass alternative, not rechecked in the live browser: [C559769 / YAGEO CC0603KRX7R9BB105](https://www.lcsc.com/product-detail/C559769.html), 1 µF ±10%, 50 V, 0603, X7R; displayed stock 719,440, $0.0602 at 20 pieces. It offers a wider temperature class than X5R. Nominal voltage and dielectric class alone do not establish effective capacitance under DC bias. In particular, preserve adequate VCC bypass capacitance at C10 when qualifying either 1 µF replacement.

First-pass alternative with the original 100 nF rating, not rechecked in the live browser: [C1590 / Samsung CL10B104KA8NNNC](https://www.lcsc.com/product-detail/C1590.html), 100 nF ±10%, 25 V, X7R, 0603; displayed stock 1,178,900, $0.0144 at 50 pieces. Use it at C4; it would reduce the original 50 V rating if used for the separate C14663 positions.

## U5 regulator: stocked international LCSC option requiring redesign

Live www.lcsc.com site searches for MP2329 returned zero results. MP2386 returned only two unrelated SEMTECH ECLAMP2386 EMI filter parts; MP8759 returned zero results. Therefore the earlier MP2386GG-Z / C6674606 recommendation has been removed from the international LCSC purchasing shortlist. Its Chinese listing does not establish availability on the requested site. No pin-compatible stocked regulator replacement was confirmed.

**Available functional candidate: [TI TPS56837RPAR / C22428366](https://www.lcsc.com/product-detail/C22428366.html).** The live product page displayed 2,248 units in LCSC stock, $2.4937 each at quantity 1, $2.1096 at 10, and $1.6236 at 100. Minimum/multiple: 1. These are LCSC's own displayed in-stock figures, rather than the separately listed other-supplier inventory.

U5 converts 9V_Input to 5 V. The TI part supports 4.5–28 V input, 0.6–13 V output and 8 A continuous output, so its nominal voltage/current limits cover this application. This is an engineering inference from the circuit and [TI specifications](https://www.ti.com/product/TPS56837), not a completed converter design or bench qualification.

It requires a schematic and PCB redesign: 10-pin 3 × 3 mm VQFN-HR replaces the original 11-pin 2 × 2 mm QFN, and the pin functions/layout differ. TI uses D-CAP3 control and MODE-selected 500/800/1200 kHz operation, versus the original fixed 700 kHz. Recalculate the inductor/output-capacitor combination, configure MODE/current limit and soft start, and revise the bootstrap, internal-regulator bypass, EN and PG connections using the [TI datasheet](https://www.ti.com/lit/ds/symlink/tps56837.pdf).

The existing R10 = 40.2 kΩ and R9 = 5.49 kΩ would nominally calculate to 4.993 V with TI's 0.6 V reference, but resistor values and the 33 pF feed-forward capacitor still need review against TI's loop-design guidance. The existing 3.3 µH inductor and three 22 µF output capacitors are not automatically qualified by this sourcing review. Validate startup, load transients and thermal behavior after redesign.

## Other procurement and library findings

The main international pages for [C15849](https://www.lcsc.com/product-detail/C15849.html) and [C1671](https://www.lcsc.com/product-detail/C1671.html) displayed Out of Stock. The original C466768 and C5349327 international listings could not be retrieved.

The BOM marks C14663 / YAGEO CC0603KRX7R9BB104 as available, but its [current main product page](https://www.lcsc.com/product-detail/C14663.html) displayed Out of Stock. It is fitted at C3 and C7. C24452 preserves their 100 nF, X7R, 50 V and 0603 requirements while tightening tolerance, so it could consolidate all three 100 nF positions C3/C4/C7.

C466768.SchLib and C1671.SchLib contain copied footprint model descriptions saying 1 µF 50 V X5R. Their actual MPNs/Value parameters identify 100 nF and 47 pF respectively. Update those descriptions when updating library metadata. U5 uses the footprint name QFN-11_L2.0-W2.0-P0.50_MP2384CGG-Z; the name alone does not verify the actual PCB pad geometry.
