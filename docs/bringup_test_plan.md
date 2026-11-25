# Bring-up & Verification Plan

The board has not been fabricated yet. This plan defines what will be measured and the pass criteria, which come from the [design calculations](design_calculations.md). Results will be added to this file as they are collected.

[← Back to project page](../README.md)

## Equipment

Bench supply (current-limited, 0–36 V), electronic load (≥ 5 A, transient mode), oscilloscope with ≥ 200 MHz bandwidth and tip-and-barrel probe adapter, DMM, frequency-response analyzer (or scope with Bode function) with a 10–50 Ω injection resistor, thermal camera, and a second bench supply for crowbar injection.

## Tests

| # | Test | Method | Pass criteria |
|---|---|---|---|
| 1 | First power-up | 24 V, 100 mA current limit, no load. Check for shorts, then raise the limit. | No current-limit hit. VOUT within worst-case window. PG high about 4 ms after EN. |
| 2 | Regulation | Sweep VIN 18 / 24 / 30 V × IOUT 0 / 1.5 / 3 A | 2.5 V: 2.437–2.572 V; 3.3 V: 3.220–3.412 V (measured before the fuse) |
| 3 | Output ripple | Tip-and-barrel probe across the output cap at 3 A, 20 MHz BW limit | < 10 mV p-p (calculated about 1 mV) |
| 4 | Switching frequency / foldback | SW node at 24 V and 3 A. Repeat at 30 V on the 2.5 V rail. | 0.85–1.15 MHz at 24 V. Document onset of foldback (predicted > 27 V worst case). |
| 5 | Load transient | 0 → 3 A and 1.5 → 3 A steps, ≥ 1 A/µs | Deviation ≤ ±5 % (125 mV / 165 mV), no ringing beyond 2 cycles |
| 6 | Loop stability | Inject across a resistor in series with R_FBT at 3 A | Phase margin ≥ 45°, gain margin ≥ 10 dB. Repeat with C_FF removed to quantify its effect. |
| 7 | Switch-node ringing | SW to PGND with the shortest ground spring | Overshoot < 38 V abs max with margin (SW < VIN + 0.3 V DC, −3.5 V for < 100 ns) |
| 8 | Efficiency | Input and output power at 0.1 / 0.5 / 1 / 2 / 3 A | Record. Use the measured η to update the Eq. 10 thermal estimate. |
| 9 | Thermal soak | 3 A, 30 min, thermal camera | Extrapolated T_J ≤ 125 °C at 85 °C ambient (25 °C margin to 150 °C) |
| 10 | Current limit / short | Short the output before the fuse | Hiccup mode (about 94 ms period). No damage. Recovers on release. |
| 11 | Crowbar trip point | Unpowered regulator. Ramp an external supply (current-limited to 1 A) onto the rail after the fuse. | Record V_TRIP. Expect 3.6–5.0 V (2.5 V rail) and 5.4–6.7 V (3.3 V rail). |
| 12 | Crowbar + fuse clearing | Spare board, sacrificial fuse. Trigger the crowbar with the rail powered from a 24 V supply through the fuse. | Fuse opens, the LED extinguishes, and the SCR survives (inspect, then retest its blocking). |
| 13 | Nuisance-trip margin | Hot-air the crowbar area to about 100 °C at max VOUT | No SCR trigger (checks the 2.5 V hot-margin limitation) |

## Results

| # | Date | Result | Notes |
|---|---|---|---|
| — | — | Pending fabrication | |
