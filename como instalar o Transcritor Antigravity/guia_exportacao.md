# Guia de Exportação do Audio Transcriptor

Este guia explica como exportar o aplicativo **Audio Transcriptor** para rodar em outros computadores Windows sem precisar instalar Python ou dependências.

## 📋 Pré-requisitos no Computador de Desenvolvimento

O computador onde você está criando o executável precisa ter:

1. **Python 3.8 ou superior** (você já tem)
2. **PyInstaller** instalado
3. **Todas as dependências do projeto** instaladas

### Instalando PyInstaller

Se ainda não estiver instalado, execute:

```powershell
pip install pyinstaller
```

## 🛠️ Como Criar o Executável

### Opção 1: Executável com Console (Recomendado para Debug)

Esta versão mostra uma janela de console com os logs de debug, útil para diagnosticar problemas:

```powershell
python build_exe_debug.py
```

### Opção 2: Executável sem Console (Versão Final)

Esta versão não mostra o console, apenas a interface gráfica (mais limpa para uso final):

```powershell
python build_exe.py
```

### Opção 3: Build Manual com PyInstaller

Você também pode usar o arquivo `.spec` diretamente:

```powershell
pyinstaller AudioTranscriptor.spec
```

## 📁 Onde Encontrar o Executável

Após a compilação, o executável estará em:

```
audio_transcriptor_fernando/dist/AudioTranscriptor.exe
```

## 📦 Preparando para Distribuição

### Arquivos Necessários

Para distribuir o aplicativo para outro computador, você precisa de:

1. **O executável**:
   - `dist/AudioTranscriptor.exe`

2. **Arquivo de configuração** (IMPORTANTE):
   - Crie um arquivo `.env` com a chave da API
   - **OU** instrua o usuário a criar

### Estrutura de Distribuição Recomendada

Crie uma pasta com os seguintes arquivos:

```
AudioTranscriptor_Distribuivel/
├── AudioTranscriptor.exe
├── .env.example          (modelo de configuração)
├── README.txt           (instruções de instalação)
└── pasta_para_monitorar/ (opcional, pasta de exemplo)
```

### Exemplo de `.env.example`

Crie um arquivo `.env.example` com o seguinte conteúdo:

```
DEEPGRAM_API_KEY=sua_chave_aqui
```

### Exemplo de README.txt

```
===================================================
  Audio Transcriptor - Instruções de Instalação
===================================================

1. COPIE TODOS OS ARQUIVOS para uma pasta no seu computador

2. CONFIGURE A CHAVE DA API:
   - Renomeie o arquivo ".env.example" para ".env"
   - Abra o arquivo ".env" com o Bloco de Notas
   - Substitua "sua_chave_aqui" pela sua chave da API Deepgram
   - Salve e feche o arquivo

3. EDITE O CAMINHO DA PASTA MONITORADA (se necessário):
   - Por padrão, o aplicativo monitora:
     C:\Users\ferna\OneDrive\Documentos\Gravacoes Som Audio Recorder Free
   - Se você quer monitorar outra pasta, será necessário 
     modificar o código fonte e recompilar

4. EXECUTE O APLICATIVO:
   - Dê duplo clique em "AudioTranscriptor.exe"
   - O aplicativo irá monitorar automaticamente a pasta configurada

5. USO:
   - Grave ou salve arquivos de áudio (.mp3, .wav, .m4a, .flac, .ogg)
     na pasta monitorada
   - A transcrição aparecerá automaticamente no aplicativo
   - Você também pode arrastar arquivos diretamente para a janela

REQUISITOS DO SISTEMA:
- Windows 7 ou superior
- Conexão com a internet (para API Deepgram)
- Conta ativa no Deepgram com créditos

SUPORTE:
- Email: [seu_email]
- GitHub: [seu_repositorio]
```

## 💻 Requisitos no Computador de Destino

### ✅ O que É NECESSÁRIO:

1. **Sistema Operacional**: Windows 7 ou superior (64-bit)
2. **Conexão com Internet**: Para comunicação com a API Deepgram
3. **Chave API Deepgram**: Conta ativa com créditos

### ❌ O que NÃO é necessário:

- ❌ Python
- ❌ Pip ou qualquer gerenciador de pacotes
- ❌ Bibliotecas ou dependências Python
- ❌ Visual C++ Redistributables (geralmente)
- ❌ .NET Framework

> **Nota**: O executável criado pelo PyInstaller é **totalmente independente** e inclui tudo que precisa!

## 🚀 Passos Completos para Distribuição

### Passo 1: Criar o Executável

No computador de desenvolvimento:

```powershell
cd "c:\Users\ferna\OneDrive\Documentos\Projetos AntiGravity\audio_transcriptor_fernando"
python build_exe.py
```

### Passo 2: Preparar a Pasta de Distribuição

Crie uma pasta nova e copie os arquivos:

```powershell
# Criar pasta de distribuição
mkdir "C:\AudioTranscriptor_Package"

# Copiar executável
copy "dist\AudioTranscriptor.exe" "C:\AudioTranscriptor_Package\"

# Copiar arquivo de exemplo de configuração
copy ".env.example" "C:\AudioTranscriptor_Package\"

# Criar README
# (crie manualmente o README.txt conforme exemplo acima)
```

### Passo 3: Compactar para Distribuição

Você pode compactar a pasta em um arquivo `.zip`:

```powershell
Compress-Archive -Path "C:\AudioTranscriptor_Package\*" -DestinationPath "C:\AudioTranscriptor_v1.0.zip"
```

### Passo 4: Distribuir

Envie o arquivo `.zip` para o outro computador via:
- Email
- Google Drive / OneDrive
- Pendrive
- Qualquer método de transferência

## ⚙️ Configuração no Computador de Destino

### Para o Usuário Final:

1. **Extrair o arquivo ZIP** para uma pasta (ex: `C:\AudioTranscriptor`)

2. **Configurar a chave API**:
   - Renomear `.env.example` para `.env`
   - Editar com Bloco de Notas
   - Adicionar a chave API Deepgram

3. **Executar**: Duplo clique em `AudioTranscriptor.exe`

## 🔧 Customização do Caminho Monitorado

Por padrão, o aplicativo monitora:
```
C:\Users\ferna\OneDrive\Documentos\Gravacoes Som Audio Recorder Free
```

### Para Alterar para Outro Computador:

#### Opção A: Tornar Configurável (Recomendado)

Modifique o `main.py` para ler o caminho do arquivo `.env`:

```python
# No arquivo .env adicione:
WATCH_DIRECTORY=C:\Caminho\Para\Sua\Pasta

# No main.py:
WATCH_DIRECTORY = os.getenv("WATCH_DIRECTORY", r"C:\Users\ferna\OneDrive\Documentos\Gravacoes Som Audio Recorder Free")
```

Depois recompile o executável.

#### Opção B: Criar Executáveis Customizados

Para cada usuário, edite o `main.py` linha 25 e recompile:

```python
WATCH_DIRECTORY = r"C:\Caminho\Especifico\Do\Usuario"
```

## 🐛 Problemas Comuns e Soluções

### Erro: "DEEPGRAM_API_KEY não encontrada"

**Solução**: Certifique-se de que o arquivo `.env` está na mesma pasta que o executável.

### Erro: "Pasta não encontrada"

**Solução**: 
1. Crie a pasta que está sendo monitorada
2. OU altere o caminho no código e recompile

### Antivírus bloqueia o executável

**Solução**: 
1. Adicione exceção no antivírus
2. OU assine o executável digitalmente (requer certificado)

### Executável demora muito para iniciar

**Normal**: PyInstaller descompacta arquivos temporários na primeira execução. Execuções subsequentes serão mais rápidas.

## 📊 Tamanho do Executável

O executável final terá aproximadamente **80-120 MB** porque inclui:
- Python runtime
- Todas as bibliotecas (customtkinter, deepgram-sdk, etc.)
- Assets do customtkinter

## 🔒 Segurança

> ⚠️ **IMPORTANTE**: Nunca distribua o arquivo `.env` com sua chave API real! 
> Sempre use `.env.example` e instrua os usuários a configurarem suas próprias chaves.

## 📝 Checklist de Distribuição

- [ ] Executável criado com sucesso (`dist/AudioTranscriptor.exe`)
- [ ] `.env.example` criado (sem chave API real)
- [ ] README.txt criado com instruções
- [ ] Testado em outro computador ou VM
- [ ] Pasta compactada em ZIP
- [ ] Instruções de configuração documentadas
- [ ] Usuário sabe onde obter chave API Deepgram

## 🎯 Alternativa: Instalador Profissional

Para uma experiência mais profissional, você pode criar um instalador usando:

### Inno Setup (Gratuito)

1. Baixe: https://jrsoftware.org/isinfo.php
2. Crie um script `.iss` que:
   - Copia o executável
   - Cria atalho no Desktop
   - Cria atalho na Inicialização (opcional)
   - Permite configurar pasta monitorada durante instalação

### NSIS (Gratuito)

Alternativa ao Inno Setup: https://nsis.sourceforge.io/

## 📞 Suporte

Se tiver problemas na exportação ou distribuição, verifique:

1. **Build logs**: Procure por erros durante a compilação
2. **Teste local**: Execute o `.exe` no seu computador primeiro
3. **Teste em VM**: Use uma máquina virtual Windows limpa para testar

---

**Dica Final**: Sempre teste o executável em um computador diferente (ou máquina virtual) antes de distribuir para garantir que funciona corretamente!
