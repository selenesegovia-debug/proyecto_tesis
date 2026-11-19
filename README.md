# Datos simulados – Tesis: postcosecha de arándanos con bromuro de metilo y atmósfera controlada

> ⚠️ **Todos los datos de este repositorio son SIMULADOS.** No son mediciones reales. Sirven para practicar el flujo de trabajo (limpieza, ANOVA, modelos mixtos, GLMM,
> control de versiones en GitHub) antes de tener los datos reales.

Basado en el *Proyecto de Tesis* de Selene Segovia Gregoratti (Universidad de Chile, 2026).
Los parámetros de la simulación se apoyan en literatura y en supuestos explícitos: ver
[`docs/fundamentos.md`](docs/fundamentos.md).

## Diseño simulado

- DCA factorial 2 × 3: **cultivar** (Sekoya Grande, Luna) × **tratamiento** (Testigo, BM origen, BM destino).
- 3 cajas por combinación → **18 cajas** (unidad experimental). Cada caja: 12 clamshells de 125 g.
- Evaluación única a los 35 d a 0 °C en AC (6 % O₂, 12 % CO₂) + 2 d a 5 °C + 2 d a 10 °C.
- Fechas hipotéticas: recepción 2026-12-14, fin de evaluación 2027-01-22 (el Gantt real está pendiente).

## Estructura

```
data/
  cajas.csv                  1 fila por caja (18): diseño y aleatorización
  fumigaciones.csv           1 fila por tanda de fumigación (6)
  registro_ambiental.csv     registro horario de T, O2 y CO2 (936 filas)
  peso_clamshells.csv        1 fila por clamshell (108): 4 pesadas + % de pérdida
  condicion_frutos.csv       1 fila por fruto (900): pruina, deshidratación, condición
  firmeza_frutos.csv         1 fila por fruto (900): FirmPro y Baxlo
  color_interno_frutos.csv   1 fila por fruto (897): L*, C*, h°
  jugo_SST_AT.csv            1 fila por caja (18): SST, volumen de NaOH, AT, SST/AT
scripts/simular_datos.py     generador (semilla fija, reproducible)
docs/fundamentos.md          justificación y fuentes de cada parámetro
```

Todas las tablas se unen por **`caja_id`**. Formato: CSV UTF-8, separador coma, **punto decimal**
(si abres los archivos en Excel o InfoStat con configuración regional chilena, importa indicando punto decimal).

## Diccionario de datos

### `cajas.csv`
| Columna | Descripción |
|---|---|
| `caja_id` | Identificador de caja (C01–C18) |
| `cultivar`, `tratamiento`, `repeticion` | Factores y repetición (1–3) |
| `huerto_origen` | Huerto de procedencia (confundido con cultivar) |
| `tanda_fumigacion` | Tanda a la que pertenece (T1–T6); ver `fumigaciones.csv` |
| `fecha_fumigacion` | Fecha de la fumigación (o del manejo equivalente en el testigo) |
| `camara_AC`, `posicion_camara_AC` | Cámara y posición aleatoria (1–18) |
| `orden_evaluacion` | Orden aleatorio de evaluación (1–18) |

### `fumigaciones.csv`
`tanda_id`, `cultivar`, `tratamiento`, `fecha`, `hora_inicio`, `duracion_h` (3), `conc_BM_objetivo_g_m3` (64; 0 en testigo),
`conc_BM_medida_g_m3`, `temp_min_C`, `temp_max_C` (dentro de 4,5–9,8 °C).

### `registro_ambiental.csv`
`fecha_hora`, `dia_experimento`, `fase` (`AC_0C`, `5C`, `10C`), `temp_C`, `O2_pct`, `CO2_pct`.
Incluye ciclos de desescarche cada 12 h y una apertura de puerta el día 17 (O₂ sube y CO₂ baja unas horas).

### `peso_clamshells.csv`
`caja_id`, `clamshell` (1–6), pesos en g (`peso_inicial_g`, `peso_35d_0C_g`, `peso_35d_mas_2d_5C_g`,
`peso_35d_mas_2d_5C_mas_2d_10C_g`) y pérdida de peso (%) por periodo (`perdida_pct_P1_35d_0C`, `_P2_2d_5C`, `_P3_2d_10C`)
más `perdida_pct_acumulada`. Peso neto (balanza tarada), resolución 0,1 g (supuesto).

### `condicion_frutos.csv` (grupo 1, 50 frutos/caja)
`pruina_nivel` (1–4; 1–2 aceptable), `deshidratacion_nivel` (1–5; 1–2 aceptable),
`condicion` (`aceptable`, `blando`, `pudricion`) y los indicadores binarios `pruina_aceptable`, `deshidratacion_aceptable`.

### `firmeza_frutos.csv` (grupo 2, frutos sanos)
`temp_pulpa_C`, `fruto_reemplazo` (1 = reemplazó a un fruto blando/podrido), `firmpro_N_mm`, `firmpro_gf_mm`,
`baxlo_mejilla1_Ush`, `baxlo_mejilla2_Ush`, `baxlo_prom_Ush`.

### `color_interno_frutos.csv` (grupo 3, frutos sanos)
`L_star`, `C_star`, `h_deg` (CIELAB, cara transversal).

### `jugo_SST_AT.csv` (un jugo compuesto por caja)
`SST_pct`, `vol_NaOH_mL`, `AT_pct_acido_citrico` (= V × 0,128), `SST_AT`.

## Imperfecciones incluidas a propósito (para practicar limpieza de datos)

- **4 lecturas fallidas del FirmPro** → `NA` en `firmpro_N_mm` y `firmpro_gf_mm`.
- **1 caja (Luna, BM origen) con 47 frutos** en color interno en vez de 50 (modelos mixtos con datos no balanceados).
- Pesos cuantizados a 0,1 g y Baxlo en pasos de 0,5 °Ush (promedio de dos mejillas enteras).
- Valores de fecha y hora como texto ISO (hay que convertirlos a fecha).

## Sugerencias de análisis (siguiendo el proyecto)

| Variables | Nivel de dato | Modelo del proyecto |
|---|---|---|
| Pérdida de peso, SST, AT, SST/AT | 1 valor por caja (promediar clamshells en pérdida de peso) | ANOVA 2 vías cultivar × tratamiento |
| FirmPro, Baxlo, L*, C*, h° | por fruto | Modelo lineal mixto, caja como efecto aleatorio |
| Pruina, deshidratación, condición | proporción de frutos | GLMM binomial (logit) con caja aleatoria; beta-binomial si hay sobredispersión |

Un buen ejercicio: calcular primero el resumen por caja y luego comparar tu estimación con los
efectos programados que figuran en `docs/fundamentos.md` (con solo 3 cajas por combinación, no se recuperarán exactos).

## Reproducir

```bash
pip install numpy pandas
python scripts/simular_datos.py   # regenera data/*.csv (semilla fija)
```

Cambiar `SEED` en el script genera una realización distinta con los mismos efectos programados.
