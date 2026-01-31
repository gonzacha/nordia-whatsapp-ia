# Validación de Principios KISS

## Cuándo usar
- Cuando sientas que el código se está complicando
- Antes de mergear refactors grandes
- Cuando agregaste >3 clases nuevas en una feature

## Severidad
🟡 **MEDIUM** - Ejecutar cuando el código "huele" complejo

---

## Prompt

```
ROLE: Sos un consultor de arquitectura que odia la complejidad innecesaria.

TAREA: Revisá el código actual de Nordia WhatsApp IA y detectá violaciones al principio KISS (Keep It Simple, Stupid).

BUSCAR:

1. ABSTRACCIONES PREMATURAS
   - ¿Hay clases/interfaces que solo tienen una implementación?
   - ¿Hay "frameworks internos" con <3 casos de uso?

2. SOBRE-INGENIERÍA
   - ¿Hay patrones de diseño aplicados "por las dudas"?
   - ¿Hay configuración para casos que todavía no existen?

3. DEPENDENCIAS INNECESARIAS
   - ¿Hay librerías que se usan solo para 1-2 funciones?
   - ¿Se puede reemplazar X librería con 10 líneas de código?

4. CÓDIGO "PARA EL FUTURO"
   - ¿Hay código comentado "por si acaso"?
   - ¿Hay features implementadas que ningún usuario pidió?

OUTPUT:
Para cada violación:
1. Ubicación exacta (archivo:línea)
2. Por qué es complejidad innecesaria
3. Alternativa más simple (con código)
4. Tiempo de ahorro si se simplifica
```

---

## Output esperado

Lista de refactors para simplificar:

```markdown
## VIOLACIONES KISS DETECTADAS

### 1. Abstracción prematura: clase MessageValidator
**Ubicación:** app/validators.py:15-45
**Problema:** Solo tiene 1 implementación, 30 líneas
**Solución simple:**
```python
# ANTES (sobre-ingeniería)
class MessageValidator:
    def __init__(self, max_length=500):
        self.max_length = max_length

    def validate(self, text: str) -> ValidationResult:
        # 30 líneas...

# DESPUÉS (simple)
def validate_message(text: str) -> tuple[bool, str]:
    if len(text) > 500:
        return False, "Muy largo"
    return True, ""
```
**Tiempo ahorrado:** 15 minutos menos de mantenimiento

### 2. Dependencia innecesaria: biblioteca XYZ
...
```

---

## Ejemplo de uso

```bash
# Después de agregar varias clases
cat .nordia/prompts/01_architecture_review/validacion_kiss.md

# Claude detecta:
# - Clase con 1 sola implementación → función simple
# - Librería pesada usada para 1 función → reemplazar
# - Configuración de features futuras → borrar
```
