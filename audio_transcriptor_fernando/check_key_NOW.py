import os
from dotenv import load_dotenv

print("=" * 80)
print("TESTE RÁPIDO - Qual chave está sendo usada?")
print("=" * 80)

# ANTES de carregar .env
key_before = os.getenv("DEEPGRAM_API_KEY")
print(f"\n1. ANTES load_dotenv(): {key_before[:15] if key_before else 'None'}...")

# DEPOIS com override=True
load_dotenv(override=True)
key_after = os.getenv("DEEPGRAM_API_KEY")
print(f"2. DEPOIS load_dotenv(override=True): {key_after[:15] if key_after else 'None'}...")

# Esperado do arquivo .env
expected = "37519b01180d3d5"
if key_after and key_after.startswith(expected):
    print(f"\n✅ CORRETO! Usando a chave do .env")
    print(f"   Chave completa: {key_after}")
else:
    print(f"\n❌ ERRO! Não está usando a chave do .env")
    print(f"   Esperado começar com: {expected}")
    print(f"   Mas começou com: {key_after[:15] if key_after else 'None'}")

print("\n" + "=" * 80)
