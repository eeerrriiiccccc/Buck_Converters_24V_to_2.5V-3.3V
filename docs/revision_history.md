# Revision History

**Rev 2 is the current and final revision.** Rev 1 is the original design. Its README and calculations are kept in [`archive/`](archive/).

[← Back to project page](../README.md)

## At a glance

| | Rev 1 | Rev 2 (current) |
|---|---|---|
| Regulator | TI LM60430 (3 A) | TI **LM60440DRPKR** (4 A) |
| Switching frequency | 400 kHz | **1 MHz** ("D" option) |
| Inductors (2.5 V / 3.3 V) | 6.8 µH / 8.2–10 µH, generic | **3.3 µH / 4.7 µH**, Würth WE-XHMI |
| Feed-forward cap | Upper bound only | **10 pF / 15 pF** |
| Input / output caps | Not specified | 10 µF 50 V X7R + 2 × 220 nF / 2 × 100 µF 1210 + 100 nF |
| Crowbar parts | Generic Zener and SCR | MMSZ3V3 / SZMMSZ5V1 Zeners, **MCR706A** SCR |
| Fuse | Holder only, no value | **4 A** fast-acting, Littelfuse 0217004.MXP |
| Analysis | Nominal values | Worst-case values, each cited to its datasheet section |

## Regulator and power stage

| Item | Rev 1 | Rev 2 | Reason for the change |
|---|---|---|---|
| Regulator | LM60430 | LM60440DRPKR | Rev 1 ran a 3 A part at a 3 A load. The 4 A part guarantees $`I_{OUT,max} \ge 4.35`$ A (Eq. 1), which leaves at least 45 % headroom. |
| $`f_{SW}`$ | 400 kHz | 1 MHz | Lets the design use about half the inductance and a smaller output capacitance. The minimum on-time check (Eq. 2) shows the 2.5 V rail stays at a fixed frequency up to about 27 V input in the worst case. |
| Ripple factor $`K`$ | 0.30 target | 0.23 / 0.20 actual | Computed from the inductors actually chosen. Both sit inside TI's 20–40 % window. |
| Inductor, 2.5 V | 6.8 µH (no part number) | 3.3 µH, WE 74439324033 (4030) | Ripple is 0.68 A. The worst-case peak current of 3.5 A (with −20 % inductance) is below $`I_{SAT,10\%}`$ = 3.9 A. |
| Inductor, 3.3 V | 8.2 or 10 µH (not chosen) | 4.7 µH, WE 74439384047 (7030) | Ripple is 0.61 A, with $`I_{SAT,10\%}`$ = 4.9 A. On both parts $`I_{SAT,30\%}`$ (8.2 A / 11 A) exceeds the 6 A short-circuit limit. |
| Feedback divider | 100 k / 66.5 k and 100 k / 43.2 k | Unchanged | Rev 2 adds the worst-case output window: 2.437–2.572 V and 3.220–3.412 V. |
| $`C_{FF}`$ | Bound only (< 65.9 pF / "100 pF") | 10 pF / 15 pF | Chosen below the Eq. 8 bound computed with effective $`C_{OUT}`$ (32.9 pF / 50 pF), as TI recommends. |
| Input caps | Not specified | Yageo CC1210KKX7R9BB106 10 µF 50 V + 2 × 220 nF | Meets TI's ≥ 10 µF bulk requirement plus an HF bypass at each VIN/PGND pin pair, rated at 2 × VIN. |
| Output caps | Not specified | 2 × 100 µF 1210 + 100 nF | Eq. 5 needs 117 µF / 94 µF effective to hold a 0→3 A step within ±5 %. |
| CBOOT / CVCC | 100 nF / 1 µF | Unchanged | These are the datasheet values. |

## Overvoltage protection

| Item | Rev 1 | Rev 2 | Reason for the change |
|---|---|---|---|
| 2.5 V Zener | 3.0 V | MMSZ3V3T1G (3.3 V) | More margin above the 2.57 V worst-case rail, so less leakage reaches the SCR gate in normal operation. |
| 2.5 V gate resistor | 1 kΩ (τ = 100 µs) | 100 Ω (τ = 10 µs) | The Zener now fires at 5–10 mA, near the 5 mA current where its voltage is specified. A lower $`R_{GK}`$ also diverts more leakage away from the gate. |
| 3.3 V Zener | 5.1 V (no part number) | SZMMSZ5V1T1G | Specific automotive-grade part with a tolerance and $`Z_{ZT}`$ spec, so the trip window can be calculated. |
| SCR | "Small-signal SCR, e.g. MCR100" | MCR706AT4G | Rated 4 A RMS and 25 A surge, compared with 0.8 A for the MCR100 class. It has to carry the fault current until the fuse opens. |
| Trip point | 3.7 V / 5.8 V (typical only) | 3.6–5.0 V / 5.4–6.7 V (windows) | Rev 2 takes the window across Zener tolerance and SCR gate-voltage spread (−40 °C to 110 °C) instead of a single typical number. |
| Fuse | Holder only | Littelfuse 0217004.MXP, 4 A fast-acting, in a Würth WR-FSH 696108003002 holder | A 3 A load is 75 % of the rating. The fuse drops 48 mV and opens in ≤ 20 ms at 10 × rated current. |

## Downstream loads (as documented)

| Rail | Rev 1 | Rev 2 |
|---|---|---|
| 2.5 V | KSZ9897S Ethernet switch | MIC2774N supervisor, TPS7A8300A LDO |
| 3.3 V | KSZ8995XA switch, TPS23861 PoE PSE, 3.3 → 1.8 V LDO | 2 × KSZ9897S, 2 × KSZ8895RQ, TPS23861 PoE PSE, SFP+ cage |

## Documentation

| Item | Rev 1 | Rev 2 |
|---|---|---|
| Calculations | Nominal, with no datasheet references | Worst-case, with every step tied to an LM604x0 section, equation and page ([design calculations](design_calculations.md)) |
| $`C_{FF}`$ formula | Written with $`2\pi f_{SW}`$, which does not match the datasheet. The resulting numbers did match Eq. 8. | Eq. 8 as printed: $`C_{FF} < \frac{V_{OUT}C_{OUT}}{120\,R_{FBT}\sqrt{V_{REF}/V_{OUT}}}`$ |
| Simulation | Had a "Simulation" section | Removed, because no simulation has been run. A [bring-up test plan](bringup_test_plan.md) with pass criteria replaces it. |
| Reproducibility | None | [`calc/buck_calcs.py`](../calc/buck_calcs.py) recomputes every number |

## Known limitations

No further revision is planned. The worst-case analysis of Rev 2 identified the following, recorded so the results are read with the right context:

1. **3.3 V crowbar threshold.** The crowbar trips at 5.4–6.7 V, while the TPS23861 VDD abs max is 4.0 V. It still clamps a full regulator runaway toward 24 V, but it does not cover a moderate overvoltage between 4 V and the trip point.
2. **2.5 V hot margin.** At the 2.57 V worst-case rail, a worst-case MMSZ3V3 can pass 1–2 mA, which puts 0.1–0.2 V on the SCR gate. The MCR706A only guarantees non-triggering below 0.2 V at 110 °C. Bring-up test 13 checks this.
3. **Fuse/SCR I²t.** The fuse's melting I²t (29.2 A²s) is above the SCR's rating (2.6 A²s). In a hard high-side short fed by a stiff 24 V source, the SCR may fail before the fuse opens. SCRs usually fail short, which keeps the rail clamped, but that is not guaranteed.
4. **Input capacitance.** Under 24 V DC bias, a single 10 µF 50 V X7R gives less than its 10 µF nameplate value.
5. **Output capacitor part number.** Only the 1210 footprint is fixed. The chosen part must provide ≥ 117 µF effective on the 2.5 V rail at its DC bias.
6. **EN and PG.** EN is tied to VIN and PG is only pulled up, so the rails have no external UVLO, sequencing or fault reporting.
