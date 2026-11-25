# Design Calculations: 24 V → 2.5 V / 3.3 V Buck Converters

All equation numbers, sections and page numbers refer to **TI SNVSBN5A**, *LM604x0 3.8-V to 36-V, 3-A and 4-A Ultra-Small Synchronous Step-Down Converter*, Rev. A (June 2020): <https://www.ti.com/lit/ds/symlink/lm60430.pdf>. The same numbers are produced by [`calc/buck_calcs.py`](../calc/buck_calcs.py).

[← Back to project page](../README.md)

---

## 0. Inputs

| Parameter | Symbol | 2.5 V rail | 3.3 V rail | Source |
|---|---|---|---|---|
| Regulator | | LM60440DRPKR | LM60440DRPKR | schematic |
| Input voltage | $`V_{IN}`$ | 24 V | 24 V | system |
| Output voltage | $`V_{OUT}`$ | 2.5 V | 3.3 V | system |
| Design load | $`I_{OUT}`$ | 3 A | 3 A | system |
| Device rating | | 4 A | 4 A | §7.3, p.5 |
| Switching frequency | $`f_{SW}`$ | 1 MHz (0.85–1.15 MHz) | 1 MHz | "D" version, §5 p.3 and §7.5 p.7 |
| Reference | $`V_{REF}`$ | 1.000 V (0.985–1.015 V) | same | §7.5, p.6 |
| Min on-time | $`t_{ON,min}`$ | 55 ns typ / 80 ns max | same | §7.6, p.7 |
| High-side current limit | $`I_{SC}`$ | 4.7 / 5.5 / 6.0 A | same | §7.5, p.6 (LM60440) |
| Low-side current limit | $`I_{LIMIT}`$ | 4.0 / 4.5 / 4.9 A | same | §7.5, p.6 (LM60440) |

The datasheet covers both the LM60430 (3 A) and the LM60440 (4 A); the two are pin-compatible (§1). This design uses the LM60440, so the 4 A limits apply.

---

## 1. Switching frequency and minimum on-time (§8.4.3, Eq. 2, p.15)

At high $`V_{IN}`$ and low $`V_{OUT}`$ the on-time per cycle gets short. Once it reaches $`t_{ON,min}`$, the device folds its frequency back. The highest input voltage that still allows fixed-frequency operation is:

```math
V_{IN} \le \frac{V_{OUT}}{t_{ON}\cdot f_{SW}}
```

| | 2.5 V | 3.3 V |
|---|---|---|
| Duty cycle $`D = V_{OUT}/V_{IN}`$ | 0.104 | 0.1375 |
| On-time at 24 V, 1 MHz | 104 ns | 138 ns |
| $`V_{IN}`$ limit, typical (55 ns, 1.00 MHz) | 45.5 V | 60.0 V |
| $`V_{IN}`$ limit, worst case (80 ns, 1.15 MHz) | **27.2 V** | **35.9 V** |

**Conclusion.** Both rails run at a fixed 1 MHz at 24 V. In the worst case the 2.5 V rail starts frequency foldback above about 27 V. Foldback is handled automatically and is not a failure, but it raises ripple, so it is worth knowing if the bus can sit above 27 V. TI's 400 kHz "A" variant would remove the concern, at the cost of roughly 2× the inductance and output capacitance (Table 2, p.17).

---

## 2. Output voltage divider (§9.2.2.3, Eq. 3, p.18)

TI recommends $`R_{FBT} = 100\ \text{k}\Omega`$.

```math
R_{FBB} = \frac{R_{FBT}}{\dfrac{V_{OUT}}{V_{REF}} - 1}
```

| | 2.5 V | 3.3 V |
|---|---|---|
| Ideal $`R_{FBB}`$ | 66.67 kΩ | 43.48 kΩ |
| Chosen (E96, 1 %) | **66.5 kΩ** (R75) | **43.2 kΩ** (R80) |
| Resulting $`V_{OUT} = V_{REF}(1 + R_{FBT}/R_{FBB})`$ | 2.504 V | 3.315 V |
| Worst case ($`V_{REF}`$ ±1.5 %, R ±1 %) | 2.437 – 2.572 V (±2.7 %) | 3.220 – 3.412 V (±2.9 %) |

The 43.2 kΩ value matches TI's own 3.3 V recommendation (Tables 2–3, p.17).

---

## 3. Inductor (§9.2.2.4, Eq. 4, p.18)

```math
L = \frac{V_{IN} - V_{OUT}}{f_{SW}\cdot K\cdot I_{OUT,max}}\cdot\frac{V_{OUT}}{V_{IN}}
```

TI recommends a ripple factor $`K`$ of 20–40 % (30 % ideal). For current-mode control to work properly, the ripple must also be at least about 10 % of the device's maximum rated current (0.4 A for the 4 A part).

| | 2.5 V | 3.3 V |
|---|---|---|
| $`L`$ for K = 0.4 / 0.3 / 0.2 | 1.87 / 2.49 / 3.73 µH | 2.37 / 3.16 / 4.74 µH |
| Chosen | **3.3 µH**, WE 74439324033 | **4.7 µH**, WE 74439384047 |
| Ripple $`\Delta I_L = \frac{(V_{IN}-V_{OUT})V_{OUT}}{V_{IN} f_{SW} L}`$ | 0.68 A (K = 0.23) | 0.61 A (K = 0.20) |
| Worst-case ripple (0.85 MHz, L −20 %) | 1.00 A | 0.89 A |
| Peak current $`I_{OUT} + \Delta I_L/2`$, typ / worst case | 3.34 / 3.50 A | 3.30 / 3.45 A |
| $`I_{SAT}`$ at 10 % / 30 % inductance drop (WE datasheet) | 3.9 A / 8.2 A | 4.9 A / 11 A |
| Rated current (ΔT = 40 K) | 7.1 A | 9.5 A |
| DCR typ / max; copper loss at 3 A | 20.2 / 25.5 mΩ; 0.23 W | 19.8 / 25.0 mΩ; 0.22 W |

**Why these values.** Both sit at the low-ripple end of TI's window. That gives lower RMS current and output ripple, and a smaller peak-to-average spread, while staying above the 0.4 A floor that current-mode control needs. The datasheet asks that $`I_{SAT}`$ ideally be at least $`I_{SC}`$ (6 A max) so the inductor can't saturate during an output short. The WE-XHMI parts use a metal-alloy powder core that saturates softly; they lose under 10 % of their inductance at the 3.5 A worst-case operating peak and under 30 % at 8.2 A / 11 A, well beyond the 6 A current limit. TI's own 1 MHz table lists 3.3 µH for 3.3 V on the LM60430 and 2.2 µH on the LM60440 (p.17). The 4.7 µH choice trades a little transient speed for lower ripple, and the load-step test in bring-up checks that trade-off.

---

## 4. Current capability (§8.3.3, Eq. 1, p.13)

```math
I_{OUT,max} \approx \frac{I_{LIMIT} + I_{SC}}{2} = \frac{4.0 + 4.7}{2} = 4.35\ \text{A (worst-case minimum)}
```

That leaves 45 % headroom over the 3 A design load. The LM60430 would give only $`(2.9 + 3.85)/2 = 3.38`$ A, a 12 % margin, which is why the 4 A part was chosen.

---

## 5. Output capacitor (§9.2.2.5, Eqs. 5–6, pp.18–19)

Minimum effective capacitance and maximum ESR for a load step $`\Delta I_{OUT}`$ with allowed deviation $`\Delta V_{OUT}`$:

```math
C_{OUT} \ge \frac{\Delta I_{OUT}}{f_{SW}\,\Delta V_{OUT}\,K}\left[(1-D)(1+K) + \frac{K^2}{12}(2-D)\right]
```

```math
ESR \le \frac{(2+K)\,\Delta V_{OUT}}{2\,\Delta I_{OUT}\left[1 + K + \dfrac{K^2}{12}\left(1 + \dfrac{1}{1-D}\right)\right]}
```

Design target: 0 → 3 A step, ±5 % deviation.

| | 2.5 V | 3.3 V |
|---|---|---|
| $`\Delta V_{OUT}`$ | 125 mV | 165 mV |
| $`C_{OUT,min}`$ (effective) | **117 µF** | **94 µF** |
| $`ESR_{max}`$ | 37.5 mΩ | 50.1 mΩ |
| Installed | 2 × 100 µF 1210 + 100 nF | 2 × 100 µF 1210 + 100 nF |

Ripple check (Eq. 6), assuming 50 % effective capacitance (100 µF) and about 1 mΩ total ESR:

```math
V_r \approx \Delta I_L\sqrt{ESR^2 + \left(\frac{1}{8 f_{SW} C_{OUT}}\right)^2} \;\Rightarrow\; 1.1\ \text{mV (2.5 V)},\ 1.0\ \text{mV (3.3 V)}
```

**Open item.** MLCCs lose capacitance under DC bias, and TI defines every capacitance in this section as the *effective* value (note, p.16). Only the 1210 footprint is chosen so far. The final MPN should be ≥ 10 V rated (TI's guidance for outputs ≤ 3.3 V, p.19), and its bias curve must show ≥ 117 µF on the 2.5 V rail. Total capacitance must stay below about 10× the design value, or 1000 µF (p.19).

The 100 nF caps (C137, C125) follow TI's advice to add a small 1–100 nF ceramic to suppress high-frequency spikes (p.19).

---

## 6. Feed-forward capacitor (§9.2.2.9, Eq. 8, p.20)

```math
C_{FF} < \frac{V_{OUT}\cdot C_{OUT}}{120\cdot R_{FBT}\cdot\sqrt{\dfrac{V_{REF}}{V_{OUT}}}}
```

| | 2.5 V | 3.3 V |
|---|---|---|
| Upper bound with $`C_{OUT}`$ = 200 µF nominal | 65.9 pF | 99.9 pF |
| Upper bound with $`C_{OUT}`$ = 100 µF effective | 32.9 pF | 50.0 pF |
| Chosen | **10 pF** (C135) | **15 pF** (C123) |
| Added zero $`f_z = 1/(2\pi R_{FBT} C_{FF})`$ | 159 kHz | 106 kHz |

TI treats Eq. 8 as an upper starting point and recommends trying lower values (p.20). With $`R_{FBT}`$ = 100 kΩ the FB-pin parasitic pole is not a concern, so a small CFF that adds a little phase boost is a conservative choice. The bring-up Bode plot will confirm it.

---

## 7. Input capacitors (§9.2.2.6, Eq. 7, pp.19–20)

Requirements:
- At least 10 µF of ceramic capacitance.
- Rated ≥ $`V_{IN,max}`$, preferably 2×.
- A small 220 nF / 50 V X7R as close to the device as possible.
- Capacitors split between the two VIN/PGND pin pairs.

```math
I_{RMS} \approx \frac{I_{OUT}}{2} = 1.5\ \text{A}
```

| Part | Value | Rationale |
|---|---|---|
| C141 / C126 | 10 µF, 50 V, X7R, 1210 (Yageo CC1210KKX7R9BB106) | Bulk ceramic, rated at 2× the 24 V bus |
| C128, C129 / C138, C139 | 220 nF, 50 V, X7R, 0805 | HF bypass, one at each VIN/PGND pair |

**Open item.** At 24 V (48 % of rated voltage), a 50 V X7R 1210 delivers noticeably less than its nameplate 10 µF, so the effective input capacitance is below TI's 10 µF guideline (a [known limitation](revision_history.md#known-limitations)). Average input current is $`V_{OUT}I_{OUT}/(V_{IN}\eta)`$ ≈ 0.37 A (2.5 V) and 0.49 A (3.3 V) at an assumed 85 % efficiency (Eq. 11, p.25).

---

## 8. Bootstrap, VCC, Enable and Power-Good

| Function | Value | Datasheet requirement |
|---|---|---|
| CBOOT (C134 / C122) | 100 nF | "100 nF and at least 10 V" (§9.2.2.7, p.20) |
| CVCC (C140 / C130) | 1 µF | "1-µF, 16-V ceramic" (§9.2.2.8, p.20) |
| EN | Tied to VIN | Allowed: "Can be connected directly to VIN" (§6, p.4) |
| PG pull-up (R78 / R35) | 100 kΩ to VOUT | "pulled up to either VCC or VOUT, through a 100-kΩ resistor" (§8.3.1, p.10) |

PG thresholds (typ): it flags undervoltage below 92 % (2.30 V / 3.04 V) and overvoltage above 107 % (2.68 V / 3.53 V).

---

## 9. Thermal estimate (§9.2.2.11, Eq. 10, p.21)

```math
I_{OUT,max} = \frac{T_J - T_A}{R_{\theta JA}}\cdot\frac{\eta}{1-\eta}\cdot\frac{1}{V_{OUT}}
```

Rearranged to give the maximum allowed effective $`R_{\theta JA}`$ for $`T_J \le 150`$ °C at $`T_A`$ = 85 °C (the WE inductors' rated ambient). IC loss is total loss minus inductor copper loss. Efficiency $`\eta`$ is assumed until measured.

| $`\eta`$ (assumed) | 2.5 V: IC loss → max $`R_{\theta JA}`$ | 3.3 V: IC loss → max $`R_{\theta JA}`$ |
|---|---|---|
| 0.80 | 1.65 W → 39 °C/W | 2.25 W → 29 °C/W |
| 0.85 | 1.09 W → 59 °C/W | 1.52 W → 43 °C/W |
| 0.90 | 0.60 W → 108 °C/W | 0.88 W → 74 °C/W |

TI states that the 54 °C/W JEDEC figure "can not be used for design purposes" (§7.4, p.6). The real value depends on copper area and vias. This board uses 2 oz outer copper on a 6-layer stack, which matches TI's recommended 2 oz / 1 oz / 1 oz / 2 oz construction (§11.1.1, p.27). The 3.3 V rail is the tighter case, and bring-up will measure it.

---

## 10. Fuse selection

Holder: Würth WR-FSH 696108003002, 5×20 mm cartridge, PCB clip with cover.
Chosen fuse: **Littelfuse 0217004.MXP**, 4 A, 250 V, fast-acting (IEC 60127-2 sheet 2).

| Criterion | Value | Check |
|---|---|---|
| Continuous loading at 3 A | 75 % of rating | Common 75 % derating guideline ✓ |
| IEC behaviour | 150 %: ≥ 60 min; 210 %: ≤ 30 min; 1000 %: ≤ 20 ms | Fast clearing under a crowbar short ✓ |
| Cold resistance / drop at 3 A | 16 mΩ / 48 mV / 0.14 W | 1.9 % of the 2.5 V rail; outside the regulation loop |
| Nominal melting I²t | 29.2 A²s | See coordination note |
| Interrupting rating | 35 A or 10 × $`I_n`$ | |

**Coordination with the SCR.** The MCR706A is rated for $`I^2t`$ = 2.6 A²s and $`I_{TSM}`$ = 25 A (half sine, 60 Hz). That is below the fuse's 29 A²s melting I²t, so in a hard high-side-FET short fed by a stiff 24 V source, the SCR may fail before the fuse opens. SCRs usually fail short, so the rail stays clamped, but this is not guaranteed.

**Feedback-sense placement.** FB is taken *before* the fuse on purpose. If it were taken after, a blown fuse would read as 0 V on FB, and the regulator would push to maximum duty cycle and charge its own output capacitors toward 24 V.

---

## 11. Crowbar trip analysis

Topology (both rails): a Zener from the rail (after the fuse) to the SCR gate, with $`R_{GK}`$ = 100 Ω and $`C_{GK}`$ = 100 nF from gate to cathode. The SCR fires when the Zener current through $`R_{GK}`$ develops $`V_{GT}`$:

```math
I_Z = \frac{V_{GT}}{R_{GK}} \approx 5\text{–}10\ \text{mA},\qquad V_{TRIP} = V_Z(I_Z) + V_{GT},\qquad V_Z(I_Z) \approx V_{Z,5\text{mA}} + (I_Z - 5\,\text{mA})\,Z_{ZT}
```

Part data:
- **MMSZ3V3T1G:** $`V_Z`$ = 3.14 / 3.30 / 3.47 V at 5 mA, $`Z_{ZT}`$ = 95 Ω; 2.3–2.9 V at 1 mA.
- **SZMMSZ5V1T1G:** 4.85 / 5.10 / 5.36 V, $`Z_{ZT}`$ = 60 Ω (onsemi MMSZ2V4T1/D Rev. 11).
- **MCR706A:** $`V_{GT}`$ ≤ 0.8 V at 25 °C and ≤ 1.0 V at −40 °C; $`I_{GT}`$ ≤ 75 µA; $`V_{GD}`$ (guaranteed non-trigger) ≥ 0.2 V at 110 °C; $`I_H`$ ≤ 5 mA (onsemi MCR703A/D Rev. 7).

| Corner | 2.5 V rail | 3.3 V rail |
|---|---|---|
| Low ($`V_{GT}`$ ≈ 0.5 V hot, $`V_Z`$ min; estimate) | 3.64 V | 5.35 V |
| Typical ($`V_{GT}`$ 0.6 V, $`V_Z`$ nom) | 4.00 V | 5.76 V |
| High ($`V_{GT}`$ 1.0 V at −40 °C, $`V_Z`$ max) | 4.95 V | 6.66 V |
| Most sensitive load abs max | TPS7A83A IN: 7.0 V (SBVS304B §7.1) | TPS23861 VDD: **4.0 V** (SLUSBX9J §5.1) |
| Result | ✅ protected | ⚠️ crowbar fires above the load's abs max |

Filter: $`\tau = R_{GK}C_{GK}`$ = 10 µs. Soft-start ramps the rail at about $`V_{OUT}/4.4\text{ ms}`$ ≈ 0.75 V/ms, far below the SCR's 10 V/µs dv/dt rating, so start-up cannot falsely trigger it.

**Hot nuisance-trip margin (2.5 V rail).** A worst-case MMSZ3V3 can pass 1–2 mA at the 2.57 V maximum rail, which puts 0.1–0.2 V on the gate. The MCR706A guarantees non-triggering only below 0.2 V at 110 °C, so the margin at high temperature is small. Bring-up test 13 checks it.

---

## 12. Summary of datasheet compliance

| Item | Requirement | 2.5 V | 3.3 V |
|---|---|---|---|
| $`R_{FBT}`$ | 100 kΩ recommended | ✅ | ✅ |
| Inductor ripple | 20–40 % of $`I_{OUT}`$, ≥ 10 % of device rating | ✅ 23 % | ✅ 20 % |
| $`I_{SAT}`$ | ≥ $`I_{LIMIT}`$; ideally ≥ $`I_{SC}`$ | ✅ (soft-sat) | ✅ (soft-sat) |
| $`C_{OUT}`$ | Eq. 5 effective value | ⚠️ MPN pending | ✅ (likely) |
| $`C_{FF}`$ | < Eq. 8 bound | ✅ | ✅ |
| $`C_{IN}`$ | ≥ 10 µF effective, 220 nF HF per pair | ⚠️ < 10 µF effective at 24 V | ⚠️ < 10 µF effective at 24 V |
| CBOOT / CVCC / PG | 100 nF / 1 µF / 100 kΩ | ✅ | ✅ |
| Min on-time at 24 V | Eq. 2 | ✅ (foldback > 27 V) | ✅ |
| Crowbar vs load abs max | trip < abs max | ✅ | ⚠️ trips above 4 V abs max |
