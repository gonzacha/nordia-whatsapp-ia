# Patrones de Programación Defensiva

## Cuándo usar
- Al revisar cualquier PR
- Después de encontrar un bug
- Antes de mergear feature importante

## Severidad
🔴 **HIGH** - Ejecutar en code reviews

---

## Prompt

```
ROLE: Sos un ingeniero de software defensivo extremadamente paranoico.

TAREA: Revisá el código actual y aplicá patrones de programación defensiva.

PATRONES A APLICAR:

1. FAIL-FAST
   - Validar precondiciones al inicio de cada función
   - Lanzar excepciones claras si input inválido
   - No asumir nada

```python
# MAL
def create_booking(business_id, date, time):
    # Asume que business existe
    business = db.get(business_id)
    # Procesa...

# BIEN
def create_booking(business_id, date, time):
    if not business_id:
        raise ValueError("business_id requerido")

    business = db.get(business_id)
    if not business:
        raise ValueError(f"Business {business_id} no existe")

    # Ahora sí procesa...
```

2. DEFENSIVE COPIES
   - No modificar estructuras mutables directamente
   - Copiar antes de mutar

3. INVARIANTES EXPLÍCITAS
   - Documentar y validar invariantes de clase/función
   - Agregar asserts

4. NULL SAFETY
   - Siempre manejar None/null
   - Usar Optional[] en type hints

5. IDEMPOTENCIA
   - Operaciones repetidas = mismo resultado
   - Crítico para webhooks duplicados

REVISAR CADA FUNCIÓN Y:
1. Identificar precondiciones faltantes
2. Agregar validaciones
3. Documentar invariantes
4. Hacer operaciones idempotentes

OUTPUT:
- Lista de funciones con validaciones faltantes
- Refactor con precondiciones
- Tests de edge cases
```

---

## Output esperado

Código refactorizado con validaciones:

```python
# ANTES
def handle_message(sender: str, text: str) -> str:
    text = text.strip().lower()
    # ... procesa

# DESPUÉS
def handle_message(sender: str, text: str) -> str:
    """
    Procesa mensaje de usuario.

    Precondiciones:
    - sender no vacío
    - text no None

    Postcondiciones:
    - Retorna string no vacío
    """
    # Fail-fast
    if not sender:
        raise ValueError("sender requerido")
    if text is None:
        raise ValueError("text no puede ser None")

    # Defensive copy
    text = str(text).strip().lower()

    # Invariante: text validado
    assert isinstance(text, str)

    # ... procesa
```
