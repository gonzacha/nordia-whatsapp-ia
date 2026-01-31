# ⚡ LAS 3 REGLAS SAGRADAS DE NORDIA

Estas reglas son **NO NEGOCIABLES**.
Violarlas significa deuda técnica consciente.

---

## 🔴 REGLA 1: No Checklist → No Código

**Qué significa:**

Antes de escribir una sola línea de código para una feature nueva,
DEBES ejecutar:

```bash
python .nordia/prompt_helper.py qa-lead
```

Y completar el checklist QA Lead completo (6 pasos).

**Sin excepciones. Ni bajo presión. Ni "es muy simple". Ni "ya sé cómo hacerlo".**

### Por qué existe esta regla:

El 80% de los bugs se introducen por no pensar ANTES de codear.

5 minutos en checklist previenen 30+ minutos de debugging.

### Cómo validar cumplimiento:

Al final de cada semana:
```bash
# ¿Cuántas features implementaste?
# ¿Cuántas pasaron por QA Lead checklist?
# Ratio objetivo: 100%
```

### Cuándo vas a querer romperla:

> "Estoy cansado, es tarde, esto es obvio, lo salteo"

**Respuesta correcta:**
```bash
# Respira
# Tomá agua
# Ejecutá:
python .nordia/prompt_helper.py qa-lead
```

**Toma 5 minutos. Un bug toma 30.**

---

## 🔴 REGLA 2: Todo Bug Tiene Post-Mortem

**Qué significa:**

Cualquier bug que llegue a:
- Demo (grabada o en vivo)
- Producción
- Usuario real (incluso 1 usuario)

REQUIERE post-mortem escrito:

```bash
python .nordia/prompt_helper.py post-mortem
```

Y guardado en `.nordia/postmortems/YYYY-MM-DD-titulo.md`

**Sin excepciones. Incluso si "ya sabés qué pasó". Incluso si "fue un typo".**

### Por qué existe esta regla:

Los bugs no se repiten por azar.
Se repiten porque no aprendimos la lección.

Post-mortem convierte bug en conocimiento sistemático.

### Estructura del post-mortem:

1. Timeline (cuándo se introdujo, cuándo se detectó)
2. Root Cause (5 Whys hasta causa raíz real)
3. Impacto (usuarios afectados, datos perdidos)
4. Por qué no lo detectamos antes
5. Fix aplicado
6. Prevención (tests/validaciones agregadas)
7. Learning (qué aprendimos)
8. Action items

### Cuándo vas a querer romperla:

> "Fue un bug chiquito, no vale la pena documentar"

**Respuesta correcta:**

Los bugs "chiquitos" sin post-mortem se vuelven bugs grandes recurrentes.

15 minutos de post-mortem previenen el mismo bug 3 veces.

---

## 🔴 REGLA 3: Toda Demo Pasa Pre-Demo

**Qué significa:**

24 horas antes de CUALQUIER demo (grabada, en vivo, interna, externa),
DEBES ejecutar:

```bash
python .nordia/prompt_helper.py pre-demo
```

Y completar el checklist de 8 puntos.

Si hay ❌ en el checklist → **NO DEMO** hasta fix.

**Sin excepciones. Incluso si "estás seguro que funciona". Incluso si "ya lo probaste 10 veces".**

### Por qué existe esta regla:

Una demo fallida:
- Quema credibilidad (irrecuperable)
- Pierde cliente potencial (costo real)
- Genera vergüenza pública (costo emocional)

Pre-demo checklist previene el 95% de las fallas de demo.

### Checklist pre-demo (8 puntos):

1. ☐ Persistencia (restart no pierde datos)
2. ☐ Validación (inputs extremos manejados)
3. ☐ Errores externos (token expirado detectado)
4. ☐ Estados (transiciones validadas)
5. ☐ Observabilidad (logs claros)
6. ☐ Testing (flujo end-to-end probado)
7. ☐ Performance (<5s respuestas)
8. ☐ Seguridad (credentials en .env)

### Después del checklist:

```bash
python .nordia/prompt_helper.py smoke-test
```

Ejecutar smoke test manual completo.

Solo si 14/15 tests ✅ → GO para demo.

### Cuándo vas a querer romperla:

> "Ya lo probé varias veces, anda perfecto"

**Respuesta correcta:**

Murphy's Law ama las demos.
Lo que puede fallar, fallará.
Justamente cuando más importa.

Pre-demo checklist es tu seguro.

---

## 💡 Por Qué Estas 3 Reglas

### Regla 1 previene el 80% de bugs
Pensando ANTES de codear.

### Regla 2 previene recurrencia
Aprendiendo de cada falla sistemáticamente.

### Regla 3 previene vergüenza pública
Validando antes de mostrar.

---

## 🎯 Cómo Medir Cumplimiento

### Al final de cada semana, preguntate:

**Regla 1:**
- [ ] ¿Cuántas features nuevas escribí? ___
- [ ] ¿Cuántas pasaron por QA Lead checklist? ___
- [ ] Ratio: ___% (meta: 100%)

**Regla 2:**
- [ ] ¿Cuántos bugs encontré? ___
- [ ] ¿Cuántos tienen post-mortem? ___
- [ ] Ratio: ___% (meta: 100%)

**Regla 3:**
- [ ] ¿Cuántas demos hice? ___
- [ ] ¿Cuántas pasaron pre-demo checklist? ___
- [ ] Ratio: ___% (meta: 100%)

**Si algún ratio < 100% → Reflexionar honestamente por qué.**

---

## ⚠️ Registro de Overrides

Si alguna vez NECESITAS romper una regla conscientemente,
documentalo:

```bash
echo "$(date): Override [REGLA X] - Razón: [explicar emergencia real]" >> .nordia/playbook_overrides.log
```

**Esto NO es para uso regular.**
**Es para emergencias documentadas.**

Si tenés >3 overrides en un mes → el playbook está mal o estás haciendo trampa.

---

## 🔥 Consecuencias de Violar las Reglas

### A corto plazo:
- Bugs en producción
- Demos fallidas
- Tiempo perdido debuggeando

### A mediano plazo:
- Deuda técnica acumulada
- Sistema frágil
- Pérdida de confianza (tuya y de usuarios)

### A largo plazo:
- MVP se vuelve unmaintainable
- Rewrites necesarios
- Proyecto muere

---

## ✅ Beneficios de Cumplir las Reglas

### A corto plazo:
- Menos bugs
- Demos exitosas
- Código más limpio

### A mediano plazo:
- Sistema robusto
- Confianza en el código
- Velocidad sostenible

### A largo plazo:
- Producto sólido
- Escalabilidad real
- Ventaja competitiva

---

## 🎓 Mindset Correcto

Estas reglas NO son:
- ❌ Burocracia
- ❌ Pérdida de tiempo
- ❌ Para "proyectos grandes"

Estas reglas SON:
- ✅ Inversión
- ✅ Seguro contra bugs
- ✅ Diferencia entre frágil y sólido

**MVP rápido ≠ MVP frágil**

Podés ir rápido Y hacer las cosas bien.
Las reglas te ayudan a ambas.

---

## 🤝 Firma del Compromiso

**Gonzalo Haedo** (Founder)
Fecha: 2026-01-31

Estas reglas no son sugerencias.
Son la diferencia entre MVP frágil y producto sólido.

Acepto seguirlas.
Acepto medirme con ellas.
Acepto que cuando las rompa, fue mi decisión consciente.

---

**Reglas Sagradas v1.0**
**Parte del Nordia Engineering Playbook v1**
