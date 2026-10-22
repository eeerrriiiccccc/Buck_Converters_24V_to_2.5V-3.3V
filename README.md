# 24V to 2.5V & 24V to 3.3V Buck Converters (PN Controller Subsystem)

## One-Paragraph Summary

2.5V Rail: A high-efficiency synchronous step-down regulator utilizing the TI LM60430 controller, designed to step down a 24V industrial bus to 2.5V at up to 3A to power the Microchip KSZ9897S managed Ethernet switch. It features a precision feedback network and an active SCR crowbar overvoltage protection circuit to safeguard sensitive downstream logic.

3.3V Rail: A companion synchronous buck regulator using the same TI LM60430 architecture, converting 24V to 3.3V at 3A to supply the Microchip KSZ8995XA 5-port switch, the TI TPS23861 PoE PSE controller, and a downstream 3.3V to 1.8V LDO.

## Specifications
<img width="1103" height="619" alt="image" src="https://github.com/user-attachments/assets/d2ac2e80-bcbf-4b76-93db-7e5ed0cbe572" />

## Why I Built This

This power supply subsystem forms the core conversion stage of a Power and Network Controller (PN Controller) PCB built for robust avionics and networking applications. The PN Controller distributes power, manages Ethernet and fiber communications, and handles PoE routing for downstream equipment. Designing these custom dual buck converters ensures stable, high-efficiency power delivery under harsh thermal conditions while incorporating hardware-level safety mechanisms like an overvoltage crowbar circuit.

## Design

### Topology and Component Selection
Both rails utilize the Texas Instruments LM60430 synchronous step-down DC/DC converter, chosen for its wide input voltage range, high efficiency, and robust thermal performance in demanding environments.

Feedback Resistors (FBB):
2.5V Rail: Bottom feedback resistor set to 66.5k.
3.3V Rail: Bottom feedback resistor set to 43.2k.

Inductor Design (K=0.3, fsw=400kHz, Iout(max)=3A): Sized to maintain low core/copper losses while limiting current ripple across the 24V input range.

Decoupling and Bootstrap:
Cboot: High-quality ceramic capacitor of 100nF (10V).
VCC Internal LDO Output: 1Microfarads, 16V ceramic capacitor connected from VCC to GND.

Feedforward Capacitor (CFF) Limits:
3.3V Rail: CFF < 100pF.
2.5V Rail: CFF < 65.9pF.

### Crowbar Overvoltage Protection Circuit (2.5V and 3.3V Rail)
To protect sensitive downstream logic on the both rails (Microchip KSZ9897S, KSZ8995XA 5-port switch, et al ) against catastrophic regulator runaway, a hardware crowbar circuit was implemented using components Zener diode, Resistors, capacitors, Silicon Controlled Rectifier(SCR), and a replaceable fuse holder:

  - Detection: Zener diode is used across the rail with a breakdown voltage set slightly above nominal. Under normal operation, it does not conduct. If the regulator fails and voltage runs away, the diode breaks down in reverse.

  - Filtering: Current flows through a resistor into the gate of the SCR. Capacitor (gate-to-cathode) charges up, filtering transient glitches and providing noise immunity against false triggers during load spikes.

  - Triggering and Latching: Once the gate threshold is crossed, SCR latches into full conduction (anode-to-cathode), creating an active dead short from the 2.5V rail to GND downstream of the fuse.

  - Fuse Clearing: The resulting massive surge current exceeds the I2t rating of the fuse, safely opening the upstream connection before the downstream ICs or output capacitors suffer overvoltage damage. The SCR remains latched until the upstream 24V power is cycled.


## Simulation
Simulations verified switch-node ringing behavior, startup inrush current, and transient load response under 3A step loads. Minor discrepancies with hand calculations were observed due to parasitic trace inductance and MOSFET switching losses at 400kHz.


## Schematic
2.5V
<img width="2180" height="1029" alt="image" src="https://github.com/user-attachments/assets/7d6c42d1-0eb6-4858-b97f-6787b9137c77" />

3.3V
<img width="2270" height="981" alt="image" src="https://github.com/user-attachments/assets/3eb01d65-89ec-4f97-8102-e135a4434be9" />

  * Power Stage: Input bulk capacitance, LM60430 synchronous switchers, and shielded inductors.
  * Feedback & Compensation: Precision resistor dividers and feedforward capacitors ensuring phase margin stability.
  * Protection Stage: Fuse  and crowbar network on both rails.

## PCB Layout

<img width="1005" height="1050" alt="image" src="https://github.com/user-attachments/assets/c33bf99d-3ac2-4aa0-a2f0-f1290a6bd356" />


<img width="1024" height="1061" alt="image" src="https://github.com/user-attachments/assets/a53f76fb-5a0b-4561-a24f-5f386fb67d81" />



3D view

<img width="773" height="791" alt="image" src="https://github.com/user-attachments/assets/595d9a4e-8a1b-40a3-a3ee-af06cb04a0ec" />
<img width="625" height="633" alt="image" src="https://github.com/user-attachments/assets/50f73dd5-b5ce-470e-82b5-8e170fbaf75e" />


Key layout decisions include:

Hot Loop Optimization: Placing input ceramic capacitors directly adjacent to the VIN and PGND pins of the LM60430 to minimize high-frequency electromagnetic interference (EMI). 

Kelvin Feedback Routing: Routing feedback traces away from high-dv/dt switch nodes to prevent noise coupling into the error amplifier.

Thermal Management: Using extensive copper pours and thermal vias underneath the IC package to dissipate heat effectively across the (high) temperature operating range.


## Results
Coming soon. 


## What I Learned

Balancing inductor ripple factor selection with core saturation constraints at higher switching frequencies (400kHz).
The critical role of layout hygiene around high-speed synchronous switching loops to maintain low output ripple.

Designing hardware-level safety interlocks (crowbar protection) to protect expensive multi-port Ethernet switch ICs.


## Rev 2 Ideas

Evaluate transitioning to a dual-phase or integrated power module solution if board space constraints tighten further.

Add test points directly on the feedback node for easier loop stability (Bode plot) measurements during bring-up.
Repo Contents

## 

#### schematics/: Altium schematic and project files.
#### layout/: PCB layout source files and Gerbers.
#### sim/: LTspice simulation files. (coming soon)
#### docs/: Calculations, datasheets, and layout notes.


