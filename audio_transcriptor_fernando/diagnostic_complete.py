"""
DIAGNÓSTICO COMPLETO - Qual arquivo está causando o erro?
"""
import os
import sys
from dotenv import load_dotenv

print("=" * 80)
print("DIAGNÓSTICO COMPLETO")
print("=" * 80)

# 1. Verificar qual script está rodando
print(f"\n1. Script sendo executado: {sys.argv[0]}")

# 2. ANTES de load_dotenv
key_before = os.getenv("DEEPGRAM_API_KEY")
print(f"\n2. Chave ANTES de load_dotenv():")
print(f"   Primeiros 15 chars: {key_before[:15] if key_before else 'None'}...")
print(f"   Tamanho: {len(key_before) if key_before else 0} caracteres")

# 3. Carregar com override
load_dotenv(override=True)

# 4. DEPOIS de load_dotenv
key_after = os.getenv("DEEPGRAM_API_KEY")
print(f"\n3. Chave DEPOIS de load_dotenv(override=True):")
print(f"   Primeiros 15 chars: {key_after[:15] if key_after else 'None'}...")
print(f"   Tamanho: {len(key_after) if key_after else 0} caracteres")
print(f"   Chave completa: {key_after}")

# 5. Verificar se é a chave correta
OLD_KEY_START = "31c7080cdcc03e3"
NEW_KEY_START = "37519b01180d3d5"

print(f"\n4. Verificação:")
if key_after and key_after.startswith(NEW_KEY_START):
    print(f"   ✅ CORRETO! Usando a chave NOVA (37519b...)")
elif key_after and key_after.startswith(OLD_KEY_START):
    print(f"   ❌ ERRO! Ainda usando a chave ANTIGA (31c708...)")
    print(f"   ⚠️ O arquivo .env NÃO está sendo carregado corretamente!")
else:
    print(f"   ⚠️ DESCONHECIDA! Chave não corresponde a nenhuma conhecida.")

# 6. Verificar se arquivo .env existe
env_path = os.path.join(os.getcwd(), ".env")
print(f"\n5. Arquivo .env:")
print(f"   Caminho: {env_path}")
print(f"   Existe: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
        if "DEEPGRAM_API_KEY" in content:
            for line in content.split('\n'):
                if line.startswith("DEEPGRAM_API_KEY"):
                    key_in_file = line.split('=', 1)[1].strip()
                    print(f"   Chave no arquivo: {key_in_file[:15]}...")
                    break
        else:
            print(f"   ⚠️ DEEPGRAM_API_KEY NÃO encontrada no .env!")

print("\n" + "=" * 80)
print("\nSE O ERRO CONTINUAR:")
print("1. Mostre QUAL arquivo/aplicação você está executando quando vê o erro")
print("2. É o .exe ou um script Python?")
print("3. Cole a saída COMPLETA deste diagnóstico")
print("=" * 80)
