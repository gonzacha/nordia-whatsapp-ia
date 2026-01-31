# Hardening de Validación de Input

## Cuándo usar
- Antes de cada demo o release
- Después de agregar feature que acepta input de usuario
- Antes de producción

## Severidad
🔴 **CRITICAL** - Obligatorio antes de release

---

## Prompt

```
ROLE: Sos un pen-tester que intenta romper validaciones.

TAREA: Auditá y reforzá la validación de inputs en Nordia.

CASOS DE ATAQUE:

1. INPUTS EXTREMOS
   - Mensaje vacío: ""
   - Mensaje de 1 carácter: "a"
   - Mensaje de 10,000 caracteres
   - Solo espacios: "     "
   - Solo emojis: "😀😀😀😀"

2. CARACTERES ESPECIALES
   - SQL injection: "'; DROP TABLE businesses; --"
   - JSON injection: {"test": "value"}
   - HTML injection: "<script>alert('xss')</script>"
   - Path traversal: "../../etc/passwd"

3. FORMATO INCORRECTO
   - Precio sin números: "Corte gratis barba también"
   - Precio con formato raro: "Corte $8.000,50"
   - Horarios ambiguos: "de mañana a tarde"
   - Fecha inválida: "32 de febrero"

4. MENSAJES DUPLICADOS
   - Usuario envía "setup" 5 veces en 1 segundo
   - WhatsApp reenvía mismo mensaje (duplicate webhook)

PARA CADA CASO:
1. Input exacto a probar
2. Comportamiento actual (ejecutar y reportar)
3. Comportamiento esperado
4. Código de validación faltante

CÓDIGO ESPERADO:
```python
def validate_price_input(text: str) -> Tuple[bool, str]:
    """Retorna (es_válido, mensaje_error)"""
    # Límite de longitud
    if len(text) > 500:
        return False, "Mensaje muy largo (máx 500 caracteres)"

    # Debe tener al menos un número
    if not any(c.isdigit() for c in text):
        return False, "No detecté precios. Ejemplo: Corte 8000"

    # ... más validaciones

    return True, ""
```

OUTPUT:
- Tabla de casos de prueba con resultados
- Código de validación completo
- Tests automatizados
```

---

## Output esperado

Suite completa de validación:

```python
# app/validation.py

MAX_MESSAGE_LENGTH = 500

def validate_message(text: str) -> tuple[bool, str]:
    """Valida mensaje de usuario"""
    if not text or not text.strip():
        return False, "Mensaje vacío"

    if len(text) > MAX_MESSAGE_LENGTH:
        return False, f"Mensaje muy largo (máx {MAX_MESSAGE_LENGTH})"

    return True, ""

def sanitize_text(text: str) -> str:
    """Sanitiza texto para DB"""
    import re
    # Remover HTML/JS
    clean = re.sub(r'<[^>]+>', '', text)
    # Normalizar espacios
    clean = ' '.join(clean.split())
    return clean[:MAX_MESSAGE_LENGTH]

def validate_prices(text: str) -> tuple[bool, str]:
    """Valida input de precios"""
    if not any(c.isdigit() for c in text):
        return False, "No detecté precios. Ej: Corte 8000"

    # Extraer números
    import re
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return False, "Formato de precios inválido"

    return True, ""
```

Tests automatizados incluidos.
