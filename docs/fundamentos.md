# Fundamentos de la simulación

Este documento explica **por qué** cada variable se simuló como se simuló, qué fuente la respalda y
cuánta confianza tiene cada parámetro. Los valores programados ("verdad conocida") están en las
columnas *Parámetro programado*.

**Nivel de respaldo**
- 🟢 **Alto**: rango o tendencia reportada directamente en la literatura citada.
- 🟡 **Medio**: la tendencia está en la literatura, pero la magnitud exacta es un supuesto mío.
- 🔴 **Supuesto**: sin fuente directa; es un valor plausible para que el dato "tenga sentido".

Las referencias marcadas con (*) las verifiqué en resúmenes o fichas en línea; conviene revisar el texto
completo y los datos de cada artículo antes de usarlas en la tesis.

---

## 1. Protocolo y ambiente de almacenamiento

| Aspecto | Parámetro programado | Respaldo |
|---|---|---|
| Secuencia 35 d a 0 °C en AC + 2 d a 5 °C + 2 d a 10 °C | tal como en el proyecto | 🟢 Neira *et al.* (*Acta Hortic.* 1456:369–376)(*) usaron la misma secuencia con ‘Blue Ribbon’ (AC 6 % O₂ y 14 % CO₂) |
| T de cámara 0 °C, O₂ 6 %, CO₂ 12 % | ruido de sensor pequeño, desescarche cada 12 h (+0,5 °C), apertura de puerta el día 17 | 🟡 Rangos del proyecto; los eventos son ilustrativos |
| Fumigación BM | 64 g m⁻³, 3 h, 4,5–9,8 °C | 🟢 Proyecto y USDA-APHIS (2017) |

## 2. Pérdida de peso

| Cultivar | P1: 35 d a 0 °C | P2: 2 d a 5 °C | P3: 2 d a 10 °C | Acumulada aprox. |
|---|---|---|---|---|
| Sekoya Grande | 0,55 % | 0,14 % | 0,30 % | ≈ 1,0 % |
| Luna | 0,75 % | 0,18 % | 0,38 % | ≈ 1,3–1,4 % |

- **Orden de magnitud (🟢):** Neira *et al.*(*) informan pérdidas < 1,5 % bajo AC con SO₂ y menos de 5 % de fruta con deshidratación visible. Rodriguez y Zoffoli (2016) muestran que una bolsa perforada de polietileno con 0,3 % de ventilación, junto con SO₂, reduce la pérdida de peso y la fruta deshidratada.
- **Cultivar (🟡):** las bayas más grandes pierden menos peso (Oh *et al.*, 2024a, citado en el proyecto; hipótesis 1). Sekoya Grande es de mayor calibre que Luna (16–17 mm), así que pierde menos. La diferencia de 0,2–0,4 puntos es mi supuesto.
- **Efecto del BM (🟡):** prácticamente nulo. Ortiz *et al.* (2018) no encontraron efecto en la pérdida de peso con 1-MCP + BM. Como ese resultado corresponde a una combinación, extrapolé que el BM solo tampoco la altera. Agregué un aumento mínimo (+0,03 y +0,05 puntos en P2 y P3) en BM destino por el calentamiento durante la fumigación.
- **Periodos cortos a temperatura mayor (🟡):** la pérdida diaria sube con la temperatura (tendencia general conocida), pero las magnitudes son supuestos míos: ≈ 0,02 %/d a 0 °C, ≈ 0,08 %/d a 5 °C y ≈ 0,15–0,19 %/d a 10 °C.
- **Variabilidad (🔴):** entre cajas (log-sd 0,10) y entre clamshells (log-sd 0,18).
- **Resolución de balanza (🔴):** supuse 0,1 g. Verifica la de tu equipo (Ohaus SC 6010) y cambia `BALANZA_RESOL_G`.

## 3. Firmeza

| Cultivar | FirmPro testigo | Baxlo testigo | Efecto BM origen | Efecto BM destino |
|---|---|---|---|---|
| Sekoya Grande | 1,80 N mm⁻¹ (≈ 183 gf mm⁻¹) | 76 °Ush | −7 % | −3 % |
| Luna | 1,48 N mm⁻¹ (≈ 151 gf mm⁻¹) | 72 °Ush | −12 % | −5 % |

(en Baxlo se aplicó la mitad del efecto relativo)

- **Luna (🟢):** el proyecto cita para Luna a cosecha 138–156 gf mm⁻¹ y 70–83 °Ush (Frutas de Chile, 2025). Tras 39 días bajo AC la programé en el tramo medio de ese rango.
- **Sekoya Grande (🔴):** se la describe como muy firme y de excelente comportamiento en frío prolongado (Brazelton *et al.*, 2020), pero no encontré valores numéricos. Programé un valor mayor que Luna.
- **Referencia de umbral (🟢):** Neira *et al.*(*) usan 150 gf mm⁻¹ como mínimo de exportación; el testigo de Luna queda en el borde y Luna con BM en origen queda bajo ese umbral, lo que da una historia comercial interesante.
- **Efecto de la atmósfera (🟢):** Forney *et al.* (2022) muestran que el CO₂ alto reduce la firmeza respecto de otras atmósferas, con diferencias entre cultivares. Esto no se incluye como factor (todos están en AC), pero justifica que los valores no sean mayores.
- **Efecto del BM (🟢/🟡):** Thang *et al.* (2016)(*) observaron que la fruta fumigada se ablandó 11–14 % durante el almacenamiento, sin efecto inicial. Ortiz *et al.* (2018) reportan más ablandamiento y deterioro por BM.
  - *Origen > destino (🔴):* el daño se manifiesta con el tiempo, y la fruta fumigada en origen tiene ~39 días para expresarlo, mientras que la de destino solo ~4. Es mi supuesto, no un resultado publicado.
  - *Interacción cultivar × BM (🔴):* Luna más sensible, porque su vida de almacenamiento declarada (35–42 d) está en el límite del ensayo (hipótesis 3).
  - Como solo se miden frutos sanos y los blandos se excluyen, el efecto es menor que el reportado para la fruta completa.
- **Variabilidad (🟡):** CV entre frutos 11 %, entre cajas 4 %.
- **Correlación FirmPro–Baxlo (🟡):** r ≈ 0,6–0,7 a nivel de fruto, porque ambos miden aspectos de la textura.
- **Temperatura de pulpa (🟡):** 15 ± 1 °C. La firmeza baja al subir la temperatura (Bourne, 1980, citado en Chiabrando *et al.*); el −1,5 % por °C es un supuesto.

## 4. Condición (blandos, pudriciones, aceptables)

Probabilidades por fruto antes del efecto aleatorio de caja (logit-normal, sd 0,22):

| Cultivar | Tratamiento | Blandos | Pudriciones |
|---|---|---|---|
| Sekoya Grande | Testigo | 3,0 % | 0,3 % |
| Sekoya Grande | BM origen | 8,0 % | 1,8 % |
| Sekoya Grande | BM destino | 5,0 % | 1,0 % |
| Luna | Testigo | 6,0 % | 0,5 % |
| Luna | BM origen | 15,0 % | 3,0 % |
| Luna | BM destino | 9,0 % | 1,5 % |

- **Pudrición muy baja en el testigo (🟢):** SO₂ a granel + AC + bolsa con ventilación controla la pudrición; Neira *et al.*(*) informan inhibición completa con SO₂ + AC, y Rodriguez y Zoffoli (2016) y Cantín *et al.* (2012) muestran control con SO₂.
- **BM aumenta ablandamiento y pudrición (🟢):** Thang *et al.* (2016)(*) y Ortiz *et al.* (2018). La magnitud y el orden origen > destino son supuestos (🔴), como en la firmeza.
- **Luna con más blandos (🟡):** menor firmeza de base y mayor sensibilidad al BM (supuesto de interacción).

## 5. Pruina (niveles 1–4) y deshidratación visual (niveles 1–5)

Se simularon con un modelo logístico acumulado (ordinal) con efecto aleatorio de caja (sd 0,20), de modo que son consistentes con el GLMM del proyecto.

| Variable | Efectos en escala logit del "deterioro" (positivo = peor) |
|---|---|
| Pruina | Sekoya Grande +0,30 (vs Luna); BM origen +0,35; BM destino +0,15 |
| Deshidratación | Sekoya Grande −0,35 (vs Luna); BM origen +0,20; BM destino +0,30 |

- **Deshidratación (🟢):** que la fruta no aceptable (niveles 3–5) sea ≈ 2–7 % concuerda con Neira *et al.*(*) (< 5 % de deshidratación) y con Moggia *et al.* (2014, citado en el proyecto), que reportan 4–10 % de fruta deshidratada con bolsa.
- **Vínculo con pérdida de peso (🟡):** la deshidratación del fruto aumenta con la pérdida de peso de su caja; los frutos blandos tienen más deshidratación.
- **Pruina (🔴):** no hallé magnitudes publicadas para estos cultivares. Luna es descrita con excelente pruina (Frutas de Chile, 2025); el efecto del BM sobre la pruina es **débil a propósito**, así que puede no ser significativo con n = 3: es un buen caso de "resultado nulo".

## 6. Color interno (CIELAB)

| Cultivar | L* | C* | h° | Efecto BM origen (ΔL*, ΔC*, Δh°) | Efecto BM destino |
|---|---|---|---|---|---|
| Sekoya Grande | 56 | 17 | 335 | −1,5, +1,0, −2,0 | −0,6, +0,4, −1,0 |
| Luna | 53 | 19 | 338 | idem | idem |

- 🔴 **No encontré valores publicados del color interno medido con espectrofotómetro en estos cultivares.** Los valores son plausibles (pulpa clara con tinte violáceo, h° en el cuadrante púrpura-rosado), pero no tienen fuente.
- **Efecto del BM (🔴):** no hay fuente que cuantifique el efecto del BM sobre el color interno. Programé un leve oscurecimiento (L* menor), mayor en BM origen, por analogía con el daño de tejido que se asocia al BM en otros atributos. Forney *et al.* (2022) documentan decoloración de la pulpa, pero causada por CO₂ alto, que aquí es igual para todos los tratamientos (solo respalda que la pulpa es un atributo sensible).
- Correlación entre L*, C* y h° dentro de fruto (🔴): L*–C* ≈ −0,45; el resto, débil.
- **Recomendación:** reemplaza estos valores por los de tu ensayo piloto cuando los tengas.

## 7. SST, AT y relación SST/AT

| Cultivar | SST (%) | AT (% ác. cítrico) | SST/AT |
|---|---|---|---|
| Sekoya Grande | 12,0 | 0,62 | ≈ 19 |
| Luna | 12,8 | 0,55 | ≈ 23 |

- **Rangos (🟢):** fichas de cultivares chilenos del programa Berry Blue (patente PP34620)(*) listan SST de 12,4–14,2 %, AT de 0,48–0,68 % y relaciones de 20–30. Neira *et al.*(*) reportan SST ≈ 11,3 % y acidez estable tras el almacenamiento.
- **Diferencias entre cultivares (🔴):** supuestas; no hay valores publicados para Luna ni Sekoya Grande en esta secuencia.
- **Efecto del BM (🟡):** ninguno directo (Ortiz *et al.*, 2018, no hallan efecto en SST ni acidez con 1-MCP + BM).
- **Pérdida de peso → SST (🟡):** +0,35 puntos de SST por cada 1 % de pérdida de peso sobre la media, por concentración de solutos. Esto genera diferencias pequeñas e incidentales entre cajas.
- **Efecto de la atmósfera (🟢):** Forney *et al.* (2022) indican que azúcares y ácidos tienden a subir con CO₂ alto y que la relación baja; por eso la relación quedó en la parte baja del rango.
- **AT (cálculo exacto):** el volumen de NaOH se registra con resolución de bureta de 0,05 mL; AT = V × 0,1 × 0,064 × 100 / 5 = V × 0,128 (fórmula del proyecto). SST con resolución de 0,1 %.

## 8. Qué NO debe interpretarse

- Los efectos son los que yo programé; no son hallazgos. En particular, **origen > destino** y **la interacción cultivar × BM** son supuestos de trabajo.
- Las pruebas estadísticas con n = 3 cajas por combinación tienen poca potencia: algunos efectos programados saldrán no significativos o con el signo cambiado por azar (eso es parte del aprendizaje).
- Antes de usar cualquier cifra en la tesis, verifica la fuente original: las marcadas con (*) las consulté solo en resúmenes o fichas en línea.

## Referencias usadas para fundamentar

- Brazelton *et al.* 2020. Plant Patent USPP31822 (Sekoya Grande™). *(citado en el proyecto)*
- Cantín *et al.* 2012. *Postharvest Biol. Technol.* 67:84–91. *(citado en el proyecto)*
- Forney *et al.* 2022. *Postharvest Biol. Technol.* 194:112073. *(en el proyecto; resumen revisado)*
- Frutas de Chile 2025. Ficha técnica Luna Blue® ‘FC12-205’. *(citado en el proyecto)*
- Moggia *et al.* 2014. *Acta Hortic.* 1017:153–158. *(citado en el proyecto)*
- Neira, R., V. Muñoz, M. Piña, J. Villegas, F. Hernández, J. Pinto y V.H. Escalona. SO₂ gasification and generators combined with controlled atmosphere on postharvest quality of ‘Blue Ribbon’ blueberries. *Acta Hortic.* 1456:369–376. (*)
- Ortiz *et al.* 2018. *Postharvest Biol. Technol.* 146:90–98. *(en el proyecto; resumen revisado)*
- Plant Patent PP34620 (cultivar ‘BB14-321NA-1’), tabla comparativa de cultivares chilenos. (*)
- Rodriguez y Zoffoli 2016. *Postharvest Biol. Technol.* 117:230–238. *(en el proyecto; resumen revisado)*
- Thang *et al.* 2016. *J. Sci. Food Agric.* 96(13):4382–4389. *(en el proyecto; resumen revisado)*
