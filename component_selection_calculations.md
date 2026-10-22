# Component Selection & Circuit Calculations

This document details the analytical calculations used to select components for both the $2.5\text{ V}$ and $3.3\text{ V}$ buck converters based on the Texas Instruments **LM60430** synchronous step-down regulator.

## 1. Operating Parameters & Targets

| Parameter | Symbol | 2.5V Rail Value | 3.3V Rail Value | 
| ----- | ----- | ----- | ----- | 
| **Input Voltage (Nominal)** | $V_{\text{IN}}$ | $24\text{ V}$ | $24\text{ V}$ | 
| **Output Voltage** | $V_{\text{OUT}}$ | $2.5\text{ V}$ | $3.3\text{ V}$ | 
| **Maximum Load Current** | $I_{\text{OUT(MAX)}}$ | $3.0\text{ A}$ | $3.0\text{ A}$ | 
| **Switching Frequency** | $f_{\text{SW}}$ | $400\text{ kHz}$ | $400\text{ kHz}$ | 
| **Inductor Ripple Coefficient** | $K$ | $0.3$ ($30\%$) | $0.3$ ($30\%$) | 
| **LM60430 Feedback Reference** | $V_{\text{FB}}$ | $1.0\text{ V}$ | $1.0\text{ V}$ | 

## 2. Feedback Resistor Divider Selection

The output voltage is set by the feedback resistor divider ($R_{\text{FBT}}$ top and $R_{\text{FBB}}$ bottom) using the equation:

$$
V_{\text{OUT}} = V_{\text{FB}} \times \left(1 + \frac{R_{\text{FBT}}}{R_{\text{FBB}}}\right)
$$

Setting the top resistor $R_{\text{FBT}} = 100\text{ k}\Omega$:

### 2.5V Rail Calculation

$$
\frac{R_{\text{FBT}}}{R_{\text{FBB}}} = \frac{V_{\text{OUT}}}{V_{\text{FB}}} - 1 = \frac{2.5\text{ V}}{1.0\text{ V}} - 1 = 1.5
$$

$$
R_{\text{FBB}} = \frac{R_{\text{FBT}}}{1.5} = \frac{100\text{ k}\Omega}{1.5} \approx 66.67\text{ k}\Omega
$$

* **Standard Standard Value Selected:** $R_{\text{FBB}} = \mathbf{66.5\text{ k}\Omega}$ (1% standard E96 value).

### 3.3V Rail Calculation

$$
\frac{R_{\text{FBT}}}{R_{\text{FBB}}} = \frac{V_{\text{OUT}}}{V_{\text{FB}}} - 1 = \frac{3.3\text{ V}}{1.0\text{ V}} - 1 = 2.3
$$

$$
R_{\text{FBB}} = \frac{R_{\text{FBT}}}{2.3} = \frac{100\text{ k}\Omega}{2.3} \approx 43.48\text{ k}\Omega
$$

* **Standard Value Selected:** $R_{\text{FBB}} = \mathbf{43.2\text{ k}\Omega}$ (1% standard E96 value).

## 3. Inductor Selection

The target inductor ripple current is defined as $\Delta I_{\text{L}} = K \times I_{\text{OUT(MAX)}} = 0.3 \times 3.0\text{ A} = 0.9\text{ A}$.

The required inductance is calculated using:

$$
L = \frac{V_{\text{OUT}} \times (V_{\text{IN}} - V_{\text{OUT}})}{V_{\text{IN}} \times f_{\text{SW}} \times \Delta I_{\text{L}}}
$$

### 2.5V Rail Calculation

$$
L_{2.5\text{V}} = \frac{2.5 \times (24 - 2.5)}{24 \times 400 \times 10^3 \times 0.9} = \frac{53.75}{8,640,000} \approx 6.22\text{ }\mu\text{H}
$$

* **Chosen Inductor:** $\mathbf{6.8\text{ }\mu\text{H}}$ standard power inductor.

* **Peak Inductor Current:** $I_{\text{PK}} = I_{\text{OUT}} + \frac{\Delta I_{\text{L}}}{2} = 3.0\text{ A} + 0.45\text{ A} = \mathbf{3.45\text{ A}}$. (Inductor saturation current rating $I_{\text{SAT}}$ must exceed $4.5\text{ A}$ for safety).

### 3.3V Rail Calculation

$$
L_{3.3\text{V}} = \frac{3.3 \times (24 - 3.3)}{24 \times 400 \times 10^3 \times 0.9} = \frac{68.31}{8,640,000} \approx 7.91\text{ }\mu\text{H}
$$

* **Chosen Inductor:** $\mathbf{8.2\text{ }\mu\text{H}}$ or $\mathbf{10.0\text{ }\mu\text{H}}$ standard power inductor.

* **Peak Inductor Current:** $I_{\text{PK}} = 3.0\text{ A} + 0.45\text{ A} = \mathbf{3.45\text{ A}}$.

## 4. Feedforward Capacitor ($C_{\text{FF}}$) Upper Limit

A feedforward capacitor $C_{\text{FF}}$ placed across $R_{\text{FBT}}$ adds a zero to improve phase margin. To maintain loop stability without injecting excess noise, $C_{\text{FF}}$ must remain below the upper threshold limit determined by the pole frequency:

### 3.3V Rail Calculation

$$
C_{\text{FF(MAX)}} < \frac{1}{2\pi \times R_{\text{FBT}} \times f_{\text{SW}} \times \sqrt{\frac{V_{\text{FB}}}{V_{\text{OUT}}}}}
$$

$$
C_{\text{FF(MAX)}} < \frac{1}{2\pi \times 100\text{ k}\Omega \times 400\text{ kHz} \times \sqrt{\frac{1.0}{3.3}}} \approx 66.6\text{ pF}
$$

* **Selected Value:** $\mathbf{100\text{ pF}}$ max bound set (standard decoupling design uses $22\text{ pF}$ to $47\text{ pF}$).

### 2.5V Rail Calculation

$$
C_{\text{FF(MAX)}} < \frac{1}{2\pi \times 100\text{ k}\Omega \times 400\text{ kHz} \times \sqrt{\frac{1.0}{2.5}}} \approx 65.9\text{ pF}
$$

## 5. Overvoltage Crowbar Protection

The crowbar circuit safeguards downstream components against excessive rail voltage in the event of an upper FET short circuit in the regulator.

### 2.5V Rail Protection Trip Math

1. **Zener Diode ($Z1$):** Selected with breakdown voltage $V_Z = 3.0\text{ V}$.
2. **Gate Trigger Voltage ($V_{\text{GT}}$):** Typical SCR gate trigger voltage $V_{\text{GT}} \approx 0.7\text{ V}$.
3. **Trip Point Voltage ($V_{\text{TRIP}}$):**
   $$V_{\text{TRIP}} = V_Z + V_{\text{GT}} = 3.0\text{ V} + 0.7\text{ V} = \mathbf{3.7\text{ V}}$$
4. **Filter Time Constant ($R1, C2$):** $R1 = 1\text{ k}\Omega$, $C2 = 100\text{ nF}$ ($\tau = 100\text{ }\mu\text{s}$).

---

### 3.3V Rail Protection Trip Math (Schematic Component Reference)

1. **Zener Breakdown Voltage ($Z2$):** $V_{\text{Z2}} = 5.1\text{ V}$
2. **Gate Trigger Voltage ($D18$ SCR):** $V_{\text{GT}} \approx 0.7\text{ V}$ (typical for small-signal SCRs like MCR100 series).
3. **Trip Threshold Voltage ($V_{\text{TRIP}}$):**
   $$V_{\text{TRIP}} = V_{\text{Z2}} + V_{\text{GT}} = 5.1\text{ V} + 0.7\text{ V} = \mathbf{5.8\text{ V}}$$
   *Under normal operation ($3.3\text{ V}$), $Z2$ does not conduct. If a switcher fault drives the rail above $5.8\text{ V}$, $Z2$ enters reverse breakdown and injects current into the SCR gate.*

4. **Gate Filter Time Constant ($R81, C142$):**
   $$R81 = 100\ \Omega, \quad C142 = 100\text{ nF}$$
   $$\tau = R81 \times C142 = 100\ \Omega \times 100\text{ nF} = \mathbf{10\text{ }\mu\text{s}}$$
   *This $10\text{ }\mu\text{s}$ filter suppresses transient noise and switching spikes on the $3.3\text{ V}$ rail, preventing unintentional triggering of $D18$.*

5. **Fuse Clearing ($XF5$):**
   Once $D18$ triggers, it latches into low-impedance conduction, creating a hard short to GND downstream of fuse $XF5$. The massive short-circuit current clears $XF5$ before downstream ICs (KSZ8995XA, TPS23861) sustain overvoltage damage.
