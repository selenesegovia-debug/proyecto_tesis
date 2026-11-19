#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulación de datos del proyecto de tesis:
"Evaluación de postcosecha en distintos cultivares de arándanos sometidos a
bromuro de metilo y atmósfera controlada" (S. Segovia G., U. de Chile, 2026).

DATOS SIMULADOS: no son mediciones reales. Sirven para practicar flujo de
trabajo (limpieza, ANOVA, modelos mixtos, GLMM, control de versiones).

Diseño: DCA factorial 2 x 3 (cultivar x tratamiento), 3 cajas por combinación
(18 cajas). Unidad experimental = caja. Submuestras = frutos / clamshells.

Uso:
    python scripts/simular_datos.py            # escribe en ../data
Semilla fija -> resultados reproducibles.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20261119
rng = np.random.default_rng(SEED)

OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

# --------------------------------------------------------------------------
# 0. PARÁMETROS (ver docs/fundamentos.md para la justificación de cada uno)
# --------------------------------------------------------------------------
CULTIVARES = ["Sekoya Grande", "Luna"]
TRATAMIENTOS = ["Testigo", "BM origen", "BM destino"]
N_REP = 3
N_CLAMSHELL = 6          # clamshells pesados por caja
N_FRUTOS = 50            # frutos por grupo de evaluación
BALANZA_RESOL_G = 0.1    # ASUMIDO: ajustar a la resolución real de la balanza

# fechas hipotéticas (el Gantt real está pendiente de confirmar)
F_RECEPCION = pd.Timestamp("2026-12-14")
F_FIN_AC = F_RECEPCION + pd.Timedelta(days=35)   # 2027-01-18
F_FIN_5C = F_FIN_AC + pd.Timedelta(days=2)
F_FIN_10C = F_FIN_5C + pd.Timedelta(days=2)

# ---- Pérdida de peso (% por periodo, media por cultivar) ------------------
# periodo: 35 d a 0 °C en AC | 2 d a 5 °C | 2 d a 10 °C
PP_BASE = {
    "Sekoya Grande": [0.55, 0.14, 0.30],
    "Luna":          [0.75, 0.18, 0.38],
}
PP_BM_DESTINO_EXTRA = [0.00, 0.03, 0.05]   # leve efecto de la fumigación a 4,5-9,8 °C
PP_SD_CAJA = 0.10      # CV entre cajas (efecto aleatorio multiplicativo, log-sd)
PP_SD_CLAM = 0.18      # CV entre clamshells dentro de caja (log-sd)

# ---- Firmeza -------------------------------------------------------------
# FirmPro (N/mm), frutos sanos, a 15 °C. 1 gf/mm = 0.00981 N/mm
FIRMPRO_MEDIA = {"Sekoya Grande": 1.80, "Luna": 1.48}      # testigo
BAXLO_MEDIA = {"Sekoya Grande": 76.0, "Luna": 72.0}        # °Ush, testigo
# efecto relativo del BM sobre la firmeza de frutos sanos (fracción)
EFECTO_BM_FIRMEZA = {
    ("Sekoya Grande", "BM origen"): -0.07, ("Sekoya Grande", "BM destino"): -0.03,
    ("Luna", "BM origen"): -0.12,          ("Luna", "BM destino"): -0.05,
}
FIRMPRO_CV_FRUTO = 0.11
FIRMPRO_SD_CAJA = 0.04   # CV entre cajas
BAXLO_SD_FRUTO = 3.0
BAXLO_SD_CAJA = 1.2
EFECTO_TEMP_PULPA = -0.015  # -1.5 % de firmeza por °C sobre 15 °C

# ---- Condición (probabilidades por fruto) ---------------------------------
# (blando, pudrición) por cultivar x tratamiento
P_COND = {
    ("Sekoya Grande", "Testigo"):    (0.030, 0.003),
    ("Sekoya Grande", "BM origen"):  (0.080, 0.018),
    ("Sekoya Grande", "BM destino"): (0.050, 0.010),
    ("Luna", "Testigo"):             (0.060, 0.005),
    ("Luna", "BM origen"):           (0.150, 0.030),
    ("Luna", "BM destino"):          (0.090, 0.015),
}
COND_SD_CAJA = 0.22      # sd (escala logit) del efecto aleatorio de caja

# ---- Pruina (logit acumulado; niveles 1..4; 1 = mejor) --------------------
# umbrales y efectos en escala logit del "deterioro" latente
UMBRAL_PRUINA = np.array([-0.30, 1.90, 3.40])
EFECTO_PRUINA = {"Sekoya Grande": 0.30, "Luna": 0.00,
                 "Testigo": 0.0, "BM origen": 0.35, "BM destino": 0.15}
# ---- Deshidratación (niveles 1..5; 1 = sin deshidratación) ----------------
UMBRAL_DESH = np.array([0.80, 2.90, 4.30, 5.30])
EFECTO_DESH = {"Sekoya Grande": -0.35, "Luna": 0.00,
               "Testigo": 0.0, "BM origen": 0.20, "BM destino": 0.30}
SD_CAJA_ORD = 0.20

# ---- Color interno (CIELAB) ----------------------------------------------
# ASUMIDO (sin fuente directa): media testigo por cultivar
COLOR_MEDIA = {"Sekoya Grande": (56.0, 17.0, 335.0),   # L*, C*, h°
               "Luna":          (53.0, 19.0, 338.0)}
COLOR_SD_FRUTO = (3.5, 3.0, 9.0)
COLOR_SD_CAJA = (1.0, 0.8, 2.5)
# efecto BM (delta L*, delta C*, delta h°)
COLOR_EFECTO_BM = {"BM origen": (-1.5, 1.0, -2.0), "BM destino": (-0.6, 0.4, -1.0)}
COLOR_CORR = np.array([[1.0, -0.45, -0.20],
                       [-0.45, 1.0, 0.25],
                       [-0.20, 0.25, 1.0]])

# ---- SST y AT (valores por caja, jugo compuesto) --------------------------
SST_MEDIA = {"Sekoya Grande": 12.0, "Luna": 12.8}   # %
AT_MEDIA = {"Sekoya Grande": 0.62, "Luna": 0.55}    # % ác. cítrico
SST_SD_CAJA = 0.30
AT_SD_CAJA = 0.030
SST_POR_PP = 0.35    # +0,35 °Brix por cada 1 % de pérdida de peso total sobre la media

# --------------------------------------------------------------------------
# 1. Cajas, tandas de fumigación y asignación aleatoria
# --------------------------------------------------------------------------
filas = []
for cv in CULTIVARES:
    for tr in TRATAMIENTOS:
        for r in range(1, N_REP + 1):
            filas.append({"cultivar": cv, "tratamiento": tr, "repeticion": r})
cajas = pd.DataFrame(filas)
n = len(cajas)

# aleatorización: orden de evaluación y posición en cámara AC (1..18)
cajas["posicion_camara_AC"] = rng.permutation(np.arange(1, n + 1))
cajas["orden_evaluacion"] = rng.permutation(np.arange(1, n + 1))
cajas.insert(0, "caja_id", [f"C{i:02d}" for i in range(1, n + 1)])
cajas["tanda_fumigacion"] = [
    f"T{CULTIVARES.index(c) * 3 + TRATAMIENTOS.index(t) + 1}"
    for c, t in zip(cajas.cultivar, cajas.tratamiento)
]
cajas["camara_AC"] = "AC1"
cajas["huerto_origen"] = cajas.cultivar.map(
    {"Sekoya Grande": "Volcan Sauerburger", "Luna": "Nancul, Villarrica"})
cajas["masa_caja_kg"] = 1.5
cajas["n_clamshells_caja"] = 12

# Tandas de fumigación (una por cultivar x tratamiento; testigo = manejo equivalente sin BM)
tandas = []
for cv in CULTIVARES:
    for tr in TRATAMIENTOS:
        tid = f"T{CULTIVARES.index(cv) * 3 + TRATAMIENTOS.index(tr) + 1}"
        if tr == "BM destino":
            fecha = F_FIN_AC
        elif tr == "BM origen":
            fecha = F_RECEPCION - pd.Timedelta(days=1)
        else:
            fecha = F_FIN_AC  # manejo equivalente en el momento de la fumigación de destino
        tmin = round(rng.uniform(4.6, 6.0), 1)
        tmax = round(min(9.8, tmin + rng.uniform(2.0, 3.8)), 1)
        tandas.append({
            "tanda_id": tid, "cultivar": cv, "tratamiento": tr,
            "fecha": fecha.date().isoformat(),
            "hora_inicio": f"{int(rng.integers(8, 15)):02d}:{int(rng.choice([0, 15, 30, 45])):02d}",
            "duracion_h": 3.0,
            "conc_BM_objetivo_g_m3": 64.0 if tr != "Testigo" else 0.0,
            "conc_BM_medida_g_m3": round(float(rng.normal(64.0, 1.2)), 1) if tr != "Testigo" else 0.0,
            "temp_min_C": tmin, "temp_max_C": tmax,
        })
tandas = pd.DataFrame(tandas)
cajas = cajas.merge(tandas[["tanda_id", "fecha"]].rename(
    columns={"tanda_id": "tanda_fumigacion", "fecha": "fecha_fumigacion"}),
    on="tanda_fumigacion")
cajas = cajas[["caja_id", "cultivar", "tratamiento", "repeticion", "huerto_origen",
               "tanda_fumigacion", "fecha_fumigacion", "camara_AC",
               "posicion_camara_AC", "orden_evaluacion", "masa_caja_kg", "n_clamshells_caja"]]

# efectos aleatorios de caja compartidos entre variables
cajas["u_caja_ord"] = rng.normal(0, SD_CAJA_ORD, n)    # pruina/deshidratación
cajas["u_caja_pp"] = rng.normal(0, PP_SD_CAJA, n)      # pérdida de peso (log)
cajas["u_caja_firm"] = rng.normal(0, 1, n)

# --------------------------------------------------------------------------
# 2. Registro ambiental (cámara AC y fase de comercialización simulada)
# --------------------------------------------------------------------------
horas = pd.date_range(F_RECEPCION, F_FIN_10C, freq="h", inclusive="left")
amb = pd.DataFrame({"fecha_hora": horas})
amb["dia_experimento"] = ((amb.fecha_hora - F_RECEPCION).dt.total_seconds() / 86400).round(3)
amb["fase"] = np.where(amb.fecha_hora < F_FIN_AC, "AC_0C",
                np.where(amb.fecha_hora < F_FIN_5C, "5C", "10C"))
t = np.arange(len(amb))
temp = np.where(amb.fase == "AC_0C", 0.0, np.where(amb.fase == "5C", 5.0, 10.0)).astype(float)
temp += rng.normal(0, 0.12, len(amb))
# desescarche cada 12 h en la cámara: +0,5 °C durante 1 h
desesc = (amb.fase == "AC_0C") & (t % 12 == 0) & (t > 0)
temp[desesc] += 0.5
o2 = np.where(amb.fase == "AC_0C", 6.0, 20.9) + rng.normal(0, 0.12, len(amb))
co2 = np.where(amb.fase == "AC_0C", 12.0, 0.04) + np.where(
    amb.fase == "AC_0C", rng.normal(0, 0.18, len(amb)), 0.0)
# evento: apertura de puerta el día 17 (O2 sube, CO2 cae durante ~6 h)
ev = (amb.fecha_hora >= F_RECEPCION + pd.Timedelta(days=17, hours=9)) & \
     (amb.fecha_hora < F_RECEPCION + pd.Timedelta(days=17, hours=15))
o2[ev] += np.linspace(2.2, 0.3, ev.sum())
co2[ev] -= np.linspace(1.8, 0.2, ev.sum())
amb["temp_C"] = temp.round(2)
amb["O2_pct"] = o2.round(2)
amb["CO2_pct"] = np.clip(co2, 0, None).round(2)
amb.to_csv(OUT / "registro_ambiental.csv", index=False)

# --------------------------------------------------------------------------
# 3. Pérdida de peso por clamshell (6 por caja, 4 pesadas)
# --------------------------------------------------------------------------
reg_peso = []
for i, c in cajas.iterrows():
    base = np.array(PP_BASE[c.cultivar], dtype=float)
    if c.tratamiento == "BM destino":
        base = base + np.array(PP_BM_DESTINO_EXTRA)
    for k in range(1, N_CLAMSHELL + 1):
        p0 = rng.normal(125.0 + (4.0 if c.cultivar == "Sekoya Grande" else 0.0), 1.8)
        p0 = max(p0, 118.0)
        pesos = [p0]
        for j in range(3):
            pct = base[j] * np.exp(c.u_caja_pp + rng.normal(0, PP_SD_CLAM))
            pesos.append(pesos[-1] * (1 - pct / 100.0))
        pesos = [round(round(p / BALANZA_RESOL_G) * BALANZA_RESOL_G, 2) for p in pesos]
        reg_peso.append({"caja_id": c.caja_id, "clamshell": k,
                         "peso_inicial_g": pesos[0], "peso_35d_0C_g": pesos[1],
                         "peso_35d_mas_2d_5C_g": pesos[2], "peso_35d_mas_2d_5C_mas_2d_10C_g": pesos[3]})
peso = pd.DataFrame(reg_peso)
# % de pérdida por periodo (fórmula del proyecto) y acumulada
cols = ["peso_inicial_g", "peso_35d_0C_g", "peso_35d_mas_2d_5C_g", "peso_35d_mas_2d_5C_mas_2d_10C_g"]
peso["perdida_pct_P1_35d_0C"] = ((peso[cols[0]] - peso[cols[1]]) / peso[cols[0]] * 100).round(3)
peso["perdida_pct_P2_2d_5C"] = ((peso[cols[1]] - peso[cols[2]]) / peso[cols[1]] * 100).round(3)
peso["perdida_pct_P3_2d_10C"] = ((peso[cols[2]] - peso[cols[3]]) / peso[cols[2]] * 100).round(3)
peso["perdida_pct_acumulada"] = ((peso[cols[0]] - peso[cols[3]]) / peso[cols[0]] * 100).round(3)
peso.to_csv(OUT / "peso_clamshells.csv", index=False)
pp_caja = peso.groupby("caja_id")["perdida_pct_acumulada"].mean()

# --------------------------------------------------------------------------
# 4. Condición, pruina y deshidratación (grupo 1: 50 frutos por caja)
# --------------------------------------------------------------------------
def ordinal_logit(latente, umbrales):
    """Nivel 1..K con cut-points; 'latente' alto = peor (nivel mayor)."""
    u = rng.logistic(size=latente.shape)
    z = latente + u
    return 1 + np.searchsorted(umbrales, z)

reg_cond = []
for i, c in cajas.iterrows():
    pb, pr = P_COND[(c.cultivar, c.tratamiento)]
    # efecto aleatorio de caja sobre log-odds (mismo desplazamiento a ambos defectos)
    z = rng.normal(0, COND_SD_CAJA)
    def inv(p, z): return 1 / (1 + np.exp(-(np.log(p / (1 - p)) + z)))
    pb_c, pr_c = inv(pb, z), inv(pr, z)
    pa_c = max(1 - pb_c - pr_c, 0)
    probs = np.array([pb_c, pr_c, pa_c]); probs /= probs.sum()
    cond = rng.choice(["blando", "pudricion", "aceptable"], size=N_FRUTOS, p=probs)
    # latentes de pruina y deshidratación (con efectos de cultivar, tratamiento y caja)
    base_p = EFECTO_PRUINA[c.cultivar] + EFECTO_PRUINA[c.tratamiento] + c.u_caja_ord
    base_d = EFECTO_DESH[c.cultivar] + EFECTO_DESH[c.tratamiento] + c.u_caja_ord \
             + 0.9 * (pp_caja[c.caja_id] - pp_caja.mean())
    lat_p = np.full(N_FRUTOS, base_p) + np.where(cond == "pudricion", 0.9, np.where(cond == "blando", 0.4, 0.0))
    lat_d = np.full(N_FRUTOS, base_d) + np.where(cond == "pudricion", 0.6, np.where(cond == "blando", 1.1, 0.0))
    pru = ordinal_logit(lat_p, UMBRAL_PRUINA)
    des = ordinal_logit(lat_d, UMBRAL_DESH)
    for f in range(N_FRUTOS):
        reg_cond.append({"caja_id": c.caja_id, "fruto": f + 1,
                         "pruina_nivel": int(pru[f]), "deshidratacion_nivel": int(des[f]),
                         "condicion": cond[f]})
condicion = pd.DataFrame(reg_cond)
condicion["pruina_aceptable"] = (condicion.pruina_nivel <= 2).astype(int)
condicion["deshidratacion_aceptable"] = (condicion.deshidratacion_nivel <= 2).astype(int)
condicion.to_csv(OUT / "condicion_frutos.csv", index=False)
prop_def = condicion.groupby("caja_id").condicion.apply(lambda s: (s != "aceptable").mean())

# --------------------------------------------------------------------------
# 5. Firmeza (grupo 2): FirmPro y luego Baxlo, frutos sanos
# --------------------------------------------------------------------------
reg_firm = []
for i, c in cajas.iterrows():
    efecto = EFECTO_BM_FIRMEZA.get((c.cultivar, c.tratamiento), 0.0)
    media_fp = FIRMPRO_MEDIA[c.cultivar] * (1 + efecto) * (1 + FIRMPRO_SD_CAJA * c.u_caja_firm)
    media_bx = BAXLO_MEDIA[c.cultivar] * (1 + 0.5 * efecto) + BAXLO_SD_CAJA * c.u_caja_firm
    # frutos de reemplazo (los blandos/pudriciones se descartaron)
    p_reemp = prop_def[c.caja_id]
    for f in range(1, N_FRUTOS + 1):
        z_comun = rng.normal()                     # factor común FirmPro-Baxlo (r ~ 0,6)
        z_fp = 0.77 * z_comun + 0.64 * rng.normal()
        z_bx = 0.77 * z_comun + 0.64 * rng.normal()
        tpulpa = round(float(np.clip(rng.normal(15.0, 0.45), 13.8, 16.2)), 1)
        corr_t = 1 + EFECTO_TEMP_PULPA * (tpulpa - 15.0)
        fp = media_fp * np.exp(FIRMPRO_CV_FRUTO * z_fp) * corr_t
        bx_m1 = int(round(media_bx * corr_t + BAXLO_SD_FRUTO * z_bx + rng.normal(0, 1.5)))
        bx_m2 = int(round(media_bx * corr_t + BAXLO_SD_FRUTO * z_bx + rng.normal(0, 1.5)))
        reg_firm.append({
            "caja_id": c.caja_id, "fruto": f, "temp_pulpa_C": tpulpa,
            "fruto_reemplazo": int(rng.random() < p_reemp),
            "firmpro_N_mm": round(float(fp), 3),
            "baxlo_mejilla1_Ush": min(bx_m1, 100), "baxlo_mejilla2_Ush": min(bx_m2, 100),
        })
firmeza = pd.DataFrame(reg_firm)
firmeza["baxlo_prom_Ush"] = (firmeza.baxlo_mejilla1_Ush + firmeza.baxlo_mejilla2_Ush) / 2
firmeza["firmpro_gf_mm"] = (firmeza.firmpro_N_mm / 0.00980665).round(1)
# imperfecciones realistas (documentadas en el README): lecturas fallidas del FirmPro
fallas = rng.choice(firmeza.index, size=4, replace=False)
firmeza.loc[fallas, ["firmpro_N_mm", "firmpro_gf_mm"]] = np.nan
firmeza.to_csv(OUT / "firmeza_frutos.csv", index=False)

# --------------------------------------------------------------------------
# 6. Color interno (grupo 3): L*, C*, h°
# --------------------------------------------------------------------------
L = np.linalg.cholesky(COLOR_CORR)
reg_col = []
for i, c in cajas.iterrows():
    mL, mC, mH = COLOR_MEDIA[c.cultivar]
    dL, dC, dH = COLOR_EFECTO_BM.get(c.tratamiento, (0.0, 0.0, 0.0))
    ucaja = [rng.normal(0, s) for s in COLOR_SD_CAJA]
    for f in range(1, N_FRUTOS + 1):
        z = L @ rng.normal(size=3)
        Lv = mL + dL + ucaja[0] + COLOR_SD_FRUTO[0] * z[0]
        Cv = mC + dC + ucaja[1] + COLOR_SD_FRUTO[1] * z[1]
        Hv = mH + dH + ucaja[2] + COLOR_SD_FRUTO[2] * z[2]
        reg_col.append({"caja_id": c.caja_id, "fruto": f,
                        "L_star": round(float(np.clip(Lv, 20, 90)), 2),
                        "C_star": round(float(max(Cv, 2.0)), 2),
                        "h_deg": round(float(Hv % 360), 1)})
color = pd.DataFrame(reg_col)
# una caja con menos frutos medidos (cortes inservibles): n < 50
c_menos = cajas.loc[(cajas.cultivar == "Luna") & (cajas.tratamiento == "BM origen")].caja_id.iloc[1]
borrar = color[color.caja_id == c_menos].sample(3, random_state=SEED).index
color = color.drop(borrar)
color.to_csv(OUT / "color_interno_frutos.csv", index=False)

# --------------------------------------------------------------------------
# 7. SST y AT (un jugo compuesto por caja)
# --------------------------------------------------------------------------
reg_jugo = []
for i, c in cajas.iterrows():
    sst = SST_MEDIA[c.cultivar] + SST_SD_CAJA * rng.normal() \
          + SST_POR_PP * (pp_caja[c.caja_id] - pp_caja.mean())
    at = AT_MEDIA[c.cultivar] + AT_SD_CAJA * rng.normal()
    sst = round(sst, 1)                      # refractómetro, resolución 0,1 %
    v_naoh = round(at / 0.128 / 0.05) * 0.05  # bureta, resolución 0,05 mL
    at_calc = v_naoh * 0.1 * 0.064 * 100 / 5
    reg_jugo.append({"caja_id": c.caja_id, "SST_pct": sst,
                     "vol_NaOH_mL": round(v_naoh, 2),
                     "AT_pct_acido_citrico": round(at_calc, 3),
                     "SST_AT": round(sst / at_calc, 2)})
jugo = pd.DataFrame(reg_jugo)
jugo.to_csv(OUT / "jugo_SST_AT.csv", index=False)

# --------------------------------------------------------------------------
# 8. Guardar tablas de diseño
# --------------------------------------------------------------------------
cajas.drop(columns=["u_caja_ord", "u_caja_pp", "u_caja_firm"], errors="ignore").to_csv(
    OUT / "cajas.csv", index=False)
tandas.to_csv(OUT / "fumigaciones.csv", index=False)

print("Archivos escritos en:", OUT)
for f in sorted(OUT.glob("*.csv")):
    print(f"  {f.name:28s} {len(pd.read_csv(f)):>5d} filas")
