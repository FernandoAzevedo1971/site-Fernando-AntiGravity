import os
from dotenv import load_dotenv

print("=" * 80)
print("DIAGNÓSTICO DE VARIÁVEIS DE AMBIENTE")
print("=" * 80)

# 1. Verificar variável ANTES de carregar .env
env_before = os.getenv("DEEPGRAM_API_KEY")
print(f"\n1. DEEPGRAM_API_KEY ANTES do load_dotenv():")
if env_before:
    print(f"   Existe! Valor: {env_before[:10]}...")
    print(f"   ⚠️  PROBLEMA: Variável está definida no Sistema Windows!")
else:
    print(f"   Não existe (OK)")

# 2. Carregar .env
load_dotenv()
env_after = os.getenv("DEEPGRAM_API_KEY")
print(f"\n2. DEEPGRAM_API_KEY DEPOIS do load_dotenv():")
if env_after:
    print(f"   Valor: {env_after[:10]}...")
else:
    print(f"   Não encontrada!")

# 3. Forçar override do .env
print(f"\n3. Forçando override do .env...")
load_dotenv(override=True)
env_override = os.getenv("DEEPGRAM_API_KEY")
print(f"   Valor com override=True: {env_override[:10]}...")

# 4. Ler diretamente do arquivo .env
print(f"\n4. Lendo DIRETAMENTE do arquivo .env:")
try:
    with open(".env", "r") as f:
        for line in f:
            if line.strip().startswith("DEEPGRAM_API_KEY"):
                key_from_file = line.split("=")[1].strip().strip('"')
                print(f"   Valor no arquivo: {key_from_file[:10]}...")
                
                # Comparar
                if key_from_file == env_override:
                    print(f"   ✅ MATCH! O .env está sendo usado corretamente com override=True")
                else:
                    print(f"   ❌ DIFERENTE! Variável do sistema está sobrescrevendo!")
                    print(f"\n   SOLUÇÃO:")
                    print(f"   1. Use load_dotenv(override=True) em todos os scripts")
                    print(f"   2. OU remova a variável do sistema Windows")
except Exception as e:
    print(f"   Erro ao ler .env: {e}")

print("\n" + "=" * 80)
print("RECOMENDAÇÃO")
print("=" * 80)
print("Use sempre: load_dotenv(override=True)")
print("Isso garante que o arquivo .env seja prioritário sobre variáveis do sistema")
print("=" * 80)
