# 🚀 Guia Rápido de Exportação

## Para Criar o Pacote Completo (Recomendado):

```powershell
# 1. Instalar PyInstaller (se ainda não tiver)
pip install pyinstaller

# 2. Criar o executável
python build_exe.py

# 3. Criar o pacote completo automaticamente
.\create_package.ps1
```

O script `create_package.ps1` irá:
- ✅ Verificar se o executável existe
- ✅ Criar pasta de distribuição
- ✅ Copiar todos os arquivos necessários
- ✅ Criar arquivo ZIP pronto para distribuir

---

## Método Manual (Passo a Passo):

### 1️⃣ Criar o Executável

```powershell
python build_exe.py
```

Ou para versão com console de debug:
```powershell
python build_exe_debug.py
```

### 2️⃣ Preparar Arquivos para Distribuição

Crie uma pasta e copie:

```
AudioTranscriptor_Package/
├── AudioTranscriptor.exe     (de dist/)
├── .env.example             (do projeto)
└── LEIA-ME.txt             (README_DISTRIBUICAO.txt renomeado)
```

### 3️⃣ Compactar em ZIP

```powershell
Compress-Archive -Path "AudioTranscriptor_Package\*" -DestinationPath "AudioTranscriptor_v1.0.zip"
```

### 4️⃣ Distribuir

Envie o arquivo `.zip` para o usuário final!

---

## 📝 Checklist para o Usuário Final

O computador de destino precisa:
- ✅ Windows 7+ (64-bit)
- ✅ Conexão com Internet
- ✅ Chave API Deepgram

O computador de destino NÃO precisa:
- ❌ Python
- ❌ Pip ou bibliotecas
- ❌ Nada além do executável!

---

## ⚙️ Configuração no Computador de Destino

1. **Extrair o ZIP**

2. **Renomear `.env.example` → `.env`**

3. **Editar `.env` com Bloco de Notas:**
   ```
   DEEPGRAM_API_KEY="sua_chave_aqui"
   WATCH_DIRECTORY="C:\Sua\Pasta\De\Gravacoes"
   ```

4. **Executar `AudioTranscriptor.exe`**

---

## 🐛 Problemas Comuns

### "API Key não encontrada"
→ Verifique se arquivo `.env` existe na mesma pasta do `.exe`

### "Pasta não encontrada"  
→ Configure `WATCH_DIRECTORY` no arquivo `.env`

### Antivírus bloqueia
→ Adicione exceção para o executável

---

## 📖 Documentação Completa

Para instruções detalhadas, consulte:
- **guia_exportacao.md** - Guia completo de exportação
- **README_DISTRIBUICAO.txt** - Manual para o usuário final

---

## 💡 Dicas

- Teste o executável em outro computador antes de distribuir
- Use uma VM Windows para testar se funciona "do zero"
- Mantenha backups do código fonte
- Nunca compartilhe sua chave API no `.env`

---

## 🎯 Próximos Passos

Após distribuir:
1. Instrua o usuário a seguir o LEIA-ME.txt
2. Ajude-o a obter uma chave API Deepgram
3. Configure o caminho da pasta monitorada
