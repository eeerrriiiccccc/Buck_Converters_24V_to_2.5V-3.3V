"""
Reproducible design calculations for the 24 V -> 2.5 V / 3.3 V buck converters.

Every equation number refers to TI LM604x0 datasheet SNVSBN5A (Rev. A, June 2020):
https://www.ti.com/lit/ds/symlink/lm60430.pdf
Run:  python calc/buck_calcs.py
"""
from math import sqrt, pi

# ---- LM60440D limits (SNVSBN5A Sec 7.5 / 7.6) ----------------------------
VREF_MIN, VREF_TYP, VREF_MAX = 0.985, 1.000, 1.015      # V
FSW_MIN, FSW_TYP, FSW_MAX = 0.85e6, 1.0e6, 1.15e6       # "D" version
TON_MIN_TYP, TON_MIN_MAX = 55e-9, 80e-9                  # s
ISC_MIN, ISC_TYP, ISC_MAX = 4.7, 5.5, 6.0                # A, high-side (LM60440)
ILIM_MIN, ILIM_TYP, ILIM_MAX = 4.0, 4.5, 4.9             # A, low-side  (LM60440)
I_DEVICE = 4.0                                           # A, LM60440 rating

VIN, IOUT = 24.0, 3.0
RFBT = 100e3
TA_DESIGN, TJ_MAX = 85.0, 150.0

RAILS = {
    #        VOUT  RFBB     L       L_part         Isat10 Isat30 DCRmax  CFF     Z(V@5mA min/nom/max, ZZT)   R_GK
    "2.5V": dict(vout=2.5, rfbb=66.5e3, L=3.3e-6, lpart="WE 74439324033 (WE-XHMI 4030)",
                 isat10=3.9, isat30=8.2, dcr=25.5e-3, cff=10e-12,
                 zener="MMSZ3V3T1G", vz=(3.14, 3.30, 3.47), zzt=95.0, rgk=100.0),
    "3.3V": dict(vout=3.3, rfbb=43.2e3, L=4.7e-6, lpart="WE 74439384047 (WE-XHMI 7030)",
                 isat10=4.9, isat30=11.0, dcr=24.96e-3, cff=15e-12,
                 zener="SZMMSZ5V1T1G", vz=(4.85, 5.10, 5.36), zzt=60.0, rgk=100.0),
}
COUT_NOM = 2 * 100e-6          # 2 x 100 uF 1210 MLCC
COUT_DERATE = 0.5              # assumed effective fraction under DC bias + temp (confirm with MPN)
DI_STEP, DV_PCT = 3.0, 0.05    # load-step spec used for Eq 5: 0 -> 3 A, 5 % deviation

# MCR706A SCR (onsemi MCR703A/D Rev 7)
SCR_VGT_TYP, SCR_VGT_MAX25, SCR_VGT_MAXM40 = 0.6, 0.8, 1.0   # V (typ is an assumption)
SCR_I2T = 2.6                                                   # A^2 s (8.3 ms)
# Littelfuse 217 series, 4 A (0217004.)
FUSE_IN, FUSE_R, FUSE_I2T = 4.0, 0.016, 29.164


def p(label, val, unit="", fmt="{:.3g}"):
    print(f"  {label:<46} {fmt.format(val)} {unit}")


for name, r in RAILS.items():
    vout = r["vout"]
    print(f"\n=================== {name} rail ===================")
    # Eq 3 - feedback divider
    p("RFBB ideal (Eq 3)", RFBT / (vout / VREF_TYP - 1) / 1e3, "kOhm")
    vnom = VREF_TYP * (1 + RFBT / r["rfbb"])
    vlo = VREF_MIN * (1 + RFBT * 0.99 / (r["rfbb"] * 1.01))
    vhi = VREF_MAX * (1 + RFBT * 1.01 / (r["rfbb"] * 0.99))
    p("VOUT nominal", vnom, "V", "{:.4f}")
    p("VOUT worst case low / high (VREF, 1% R)", vlo, "V", "{:.3f}"); p("", vhi, "V", "{:.3f}")

    # Eq 2 - minimum on-time
    D = vout / VIN
    p("Duty cycle D", D, "", "{:.4f}")
    p("On-time at 24 V, 1 MHz", D / FSW_TYP * 1e9, "ns", "{:.1f}")
    p("Eq 2 VIN before foldback (typ tON, typ fsw)", vout / (TON_MIN_TYP * FSW_TYP), "V", "{:.1f}")
    p("Eq 2 VIN before foldback (max tON, max fsw)", vout / (TON_MIN_MAX * FSW_MAX), "V", "{:.1f}")

    # Eq 4 - inductor
    for K in (0.2, 0.3, 0.4):
        p(f"Eq 4 L for K={K}, IOUT=3 A", (VIN - vout) / (FSW_TYP * K * IOUT) * vout / VIN * 1e6, "uH")
    dIL = (VIN - vout) * vout / (VIN * FSW_TYP * r["L"])
    dIL_worst = (VIN - vout) * vout / (VIN * FSW_MIN * r["L"] * 0.8)   # fsw min, L -20 %
    p(f"Ripple dIL with {r['L']*1e6:.1f} uH (nom)", dIL, "A")
    p("Ripple dIL worst (fsw min, L -20%)", dIL_worst, "A")
    p("K = dIL / 3 A", dIL / IOUT, "", "{:.3f}")
    p("10% floor (0.1 x 4 A device rating)", 0.1 * I_DEVICE, "A")
    ipk = IOUT + dIL / 2
    p("Peak inductor current @ 3 A", ipk, "A")
    p("Peak worst case", IOUT + dIL_worst / 2, "A")
    p(f"{r['lpart']} ISAT(10%) / ISAT(30%)", r["isat10"], "A"); p("", r["isat30"], "A")
    p("Inductor copper loss (DCR max)", IOUT**2 * r["dcr"], "W")

    # Eq 1 - output current capability
    p("Eq 1 IOUT(max) = (ILIMIT+ISC)/2, min", (ILIM_MIN + ISC_MIN) / 2, "A")

    # Eq 5 / 6 - output capacitor
    K = dIL / IOUT
    dV = DV_PCT * vout
    cmin = DI_STEP / (FSW_TYP * dV * K) * ((1 - D) * (1 + K) + K**2 / 12 * (2 - D))
    esr = (2 + K) * dV / (2 * DI_STEP * (1 + K + K**2 / 12 * (1 + 1 / (1 - D))))
    ceff = COUT_NOM * COUT_DERATE
    p(f"Eq 5 COUT min for {DI_STEP} A step, {DV_PCT*100:.0f}% dV", cmin * 1e6, "uF")
    p("Eq 5 ESR max", esr * 1e3, "mOhm")
    p("COUT effective assumed (50% of 2x100uF)", ceff * 1e6, "uF")
    vr = dIL * sqrt((2e-3 / 2) ** 2 + (1 / (8 * FSW_TYP * ceff)) ** 2)
    p("Eq 6 output ripple (ESR 1 mOhm total)", vr * 1e3, "mV")

    # Eq 8 - feedforward capacitor
    for c, lbl in ((COUT_NOM, "nominal"), (ceff, "effective")):
        p(f"Eq 8 CFF upper bound, COUT {lbl}", vout * c / (120 * RFBT * sqrt(VREF_TYP / vout)) * 1e12, "pF")
    p(f"CFF chosen {r['cff']*1e12:.0f} pF -> zero 1/(2 pi RFBT CFF)", 1 / (2 * pi * RFBT * r["cff"]) / 1e3, "kHz")

    # Eq 7, 11 - input
    p("Eq 7 input cap RMS current ~ IOUT/2", IOUT / 2, "A")
    for eta in (0.85,):
        p(f"Eq 11 average input current (eta={eta})", vout * IOUT / (VIN * eta), "A")

    # Eq 10 - thermal (efficiency is an ASSUMPTION until measured)
    for eta in (0.80, 0.85, 0.90):
        ploss = vout * IOUT * (1 - eta) / eta
        pic = ploss - IOUT**2 * r["dcr"]
        p(f"eta={eta:.2f}: total loss / IC loss", ploss, "W"); p("", pic, "W")
        p(f"   max RthJA for TJ<=150C at TA={TA_DESIGN:.0f}C", (TJ_MAX - TA_DESIGN) / pic, "C/W")

    # Power-good thresholds (Sec 7.5)
    p("PG OV trip (107% typ)", 1.07 * vout, "V"); p("PG UV trip falling (92% typ)", 0.92 * vout, "V")

    # Crowbar trip window: Vtrip = VZ(Iz) + VGT, with Iz = VGT/RGK
    vzmin, vznom, vzmax = r["vz"]
    def vz_at(i, vz5):  # linearise around IZT = 5 mA with ZZT
        return vz5 + (i - 5e-3) * r["zzt"]
    for lbl, vgt, vz5 in (("low  (VGT 0.5 V hot, VZ min)", 0.5, vzmin),
                          ("typ  (VGT 0.6 V, VZ nom)", SCR_VGT_TYP, vznom),
                          ("high (VGT 1.0 V @ -40C, VZ max)", SCR_VGT_MAXM40, vzmax)):
        iz = vgt / r["rgk"]
        p(f"Crowbar trip {lbl}", vz_at(iz, vz5) + vgt, "V", "{:.2f}")
    p("Gate filter tau = RGK * 100 nF", r["rgk"] * 100e-9 * 1e6, "us")

    # Fuse
    p("Fuse loading 3 A / 4 A", IOUT / FUSE_IN * 100, "%", "{:.0f}")
    p("Fuse voltage drop at 3 A (cold R)", IOUT * FUSE_R * 1e3, "mV")
    p("Fuse dissipation at 3 A", IOUT**2 * FUSE_R, "W")

print("\nFuse vs SCR coordination: fuse melting I2t", FUSE_I2T, "A2s vs SCR I2t", SCR_I2T, "A2s")
# Rev 2: TL431 crowbar trigger at 3.8 V
print("Rev2 TL431 divider for 3.8 V trip: Rtop/Rbot =", 3.8 / 2.495 - 1)
# Rev 2: EN UVLO (Eq 9) for VON = 18 V, RENB = 10k
RENB, VON = 10e3, 18.0
print("Rev2 Eq 9: RENT =", (VON / 1.231 - 1) * RENB, " VOFF =", VON * (1 - 0.1 / 1.231))
