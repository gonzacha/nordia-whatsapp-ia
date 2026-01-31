#!/usr/bin/env python3
"""
Helper para usar prompts de Nordia.

Uso:
    python .nordia/prompt_helper.py qa-lead
    python .nordia/prompt_helper.py pre-demo
    python .nordia/prompt_helper.py failure-analysis
    python .nordia/prompt_helper.py list
"""

import sys
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"

# Mapeo de comandos a archivos
PROMPT_MAP = {
    # Meta
    "qa-lead": "META_PROMPT_QA_LEAD.md",

    # Architecture
    "arch-audit": "01_architecture_review/auditoria_defensiva.md",
    "kiss": "01_architecture_review/validacion_kiss.md",

    # Failure Analysis
    "failure-modes": "02_failure_analysis/modos_de_falla.md",
    "chaos": "02_failure_analysis/simulacion_caos.md",

    # Input Validation
    "input-validation": "05_input_validation/hardening_validacion.md",

    # Defensive Programming
    "defensive": "06_defensive_programming/patrones_defensivos.md",

    # Feature Checklist
    "pre-feature": "08_feature_checklist/pre_feature_checklist.md",

    # Pre-Demo
    "pre-demo": "09_pre_demo/checklist_pre_demo.md",
    "smoke-test": "09_pre_demo/smoke_test_manual.md",

    # Post-Bug
    "post-mortem": "10_post_bug/post_mortem.md",
}

# Aliases comunes
ALIASES = {
    "qal": "qa-lead",
    "demo": "pre-demo",
    "bug": "post-mortem",
    "validate": "input-validation",
    "fail": "failure-modes",
}


def list_prompts():
    """Lista todos los prompts disponibles"""
    print("\n📚 Prompts disponibles:\n")
    print("🎖️  Meta:")
    print("  qa-lead        - Modo QA Lead (⭐ MÁS IMPORTANTE)")
    print("\n🏗️  Architecture:")
    print("  arch-audit     - Auditoría de arquitectura defensiva")
    print("  kiss           - Validación de principios KISS")
    print("\n💥 Failure Analysis:")
    print("  failure-modes  - Análisis de modos de falla")
    print("  chaos          - Simulación de caos")
    print("\n✅ Input Validation:")
    print("  input-validation - Hardening de validación")
    print("\n🛡️  Defensive Programming:")
    print("  defensive      - Patrones defensivos")
    print("\n➕ Feature Addition:")
    print("  pre-feature    - Checklist pre-feature")
    print("\n🎬 Pre-Demo:")
    print("  pre-demo       - Checklist pre-demo")
    print("  smoke-test     - Smoke test manual")
    print("\n🔍 Post-Bug:")
    print("  post-mortem    - Autopsia post-mortem")
    print("\n💡 Aliases:")
    print("  qal → qa-lead")
    print("  demo → pre-demo")
    print("  bug → post-mortem")
    print()


def show_prompt(command: str):
    """Muestra el contenido de un prompt"""
    # Resolver alias
    if command in ALIASES:
        command = ALIASES[command]

    prompt_file = PROMPT_MAP.get(command)

    if not prompt_file:
        print(f"❌ Prompt '{command}' no encontrado")
        print("\nUsa: python .nordia/prompt_helper.py list")
        sys.exit(1)

    prompt_path = PROMPTS_DIR / prompt_file

    if not prompt_path.exists():
        print(f"❌ Archivo no encontrado: {prompt_path}")
        sys.exit(1)

    # Mostrar contenido
    content = prompt_path.read_text()
    print(content)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["list", "ls", "-l", "--list"]:
        list_prompts()
        sys.exit(0)

    command = sys.argv[1]
    show_prompt(command)


if __name__ == "__main__":
    main()
