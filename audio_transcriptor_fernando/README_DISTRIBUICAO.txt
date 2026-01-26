===================================================
  Audio Transcriptor - Instruções de Instalação
===================================================

SOBRE ESTE APLICATIVO:
Este aplicativo monitora automaticamente uma pasta em busca de 
novos arquivos de áudio e os transcreve usando a API Deepgram
com separação de locutores (diarização).

===================================================
  INSTALAÇÃO
===================================================

1. EXTRAIA TODOS OS ARQUIVOS
   - Descompacte o arquivo ZIP para uma pasta no seu computador
   - Exemplo: C:\AudioTranscriptor

2. CONFIGURE SUA CHAVE DA API DEEPGRAM
   
   a) Se você NÃO tem uma chave API:
      - Acesse: https://console.deepgram.com
      - Crie uma conta gratuita
      - Obtenha sua chave API
   
   b) Configure a chave no aplicativo:
      - Renomeie o arquivo ".env.example" para ".env"
      - Abra o arquivo ".env" com o Bloco de Notas
      - Substitua "YOUR_DEEPGRAM_API_KEY_HERE" pela sua chave
      - Exemplo: DEEPGRAM_API_KEY="a1b2c3d4e5f6..."
      - Salve e feche o arquivo

3. CONFIGURE A PASTA MONITORADA (IMPORTANTE!)
   
   Por padrão, o aplicativo monitora:
   C:\Users\ferna\OneDrive\Documentos\Gravacoes Som Audio Recorder Free
   
   VOCÊ PRECISA ALTERAR ISSO PARA SEU COMPUTADOR!
   
   Opção A - Editar o arquivo .env (mais fácil):
      - Abra o arquivo ".env" com Bloco de Notas
      - Adicione uma nova linha:
        WATCH_DIRECTORY=C:\Caminho\Para\Sua\Pasta
      - Substitua pelo caminho da sua pasta de gravações
      - Salve o arquivo
   
   Opção B - Solicitar versão customizada:
      - Entre em contato para uma versão com seu caminho

4. EXECUTE O APLICATIVO
   - Dê duplo clique em "AudioTranscriptor.exe"
   - Uma janela será aberta mostrando o status do monitoramento

===================================================
  COMO USAR
===================================================

MÉTODO 1: Gravação Automática
   - Grave ou salve arquivos de áudio na pasta monitorada
   - O aplicativo detectará automaticamente
   - A transcrição aparecerá em segundos

MÉTODO 2: Arrastar e Soltar
   - Arraste um arquivo de áudio para a janela do aplicativo
   - A transcrição será processada imediatamente

FORMATOS SUPORTADOS:
   - MP3
   - WAV
   - M4A
   - FLAC
   - OGG

RECURSOS:
   - Separação automática de locutores (Speaker 0, Speaker 1, etc.)
   - Formatação inteligente de texto
   - Botão para copiar texto
   - Contador de uso e saldo da API

===================================================
  REQUISITOS DO SISTEMA
===================================================

✓ Windows 7 ou superior (64-bit)
✓ Conexão com a Internet
✓ Conta Deepgram ativa com créditos
✓ Espaço em disco: ~200 MB

NÃO É NECESSÁRIO:
✗ Python
✗ Instalação de bibliotecas
✗ Configurações avançadas

===================================================
  SOLUÇÃO DE PROBLEMAS
===================================================

PROBLEMA: "ERRO: API Key não encontrada no .env"
SOLUÇÃO: Verifique se o arquivo .env existe e contém a chave

PROBLEMA: "ERRO: Pasta não encontrada"
SOLUÇÃO: Verifique se a pasta monitorada existe ou configure
         o caminho correto no arquivo .env

PROBLEMA: Antivírus bloqueia o aplicativo
SOLUÇÃO: Adicione uma exceção no antivírus para o executável

PROBLEMA: Aplicativo demora para iniciar
RESPOSTA: Isso é normal na primeira execução. O PyInstaller
          descompacta arquivos temporários.

PROBLEMA: "Erro ao transcrever"
SOLUÇÕES:
   - Verifique sua conexão com a Internet
   - Verifique se tem créditos na conta Deepgram
   - Verifique se a chave API está correta
   - Tente com um arquivo de áudio menor

===================================================
  INICIAR COM O WINDOWS (OPCIONAL)
===================================================

Para o aplicativo iniciar automaticamente com o Windows:

1. Pressione Win + R
2. Digite: shell:startup
3. Pressione Enter
4. Copie um atalho do AudioTranscriptor.exe para esta pasta

===================================================
  PRIVACIDADE E SEGURANÇA
===================================================

- Os arquivos de áudio são enviados para os servidores Deepgram
  para processamento
- A transcrição é feita via API segura (HTTPS)
- Nenhum dado é armazenado localmente além da transcrição
- Sua chave API é armazenada apenas no arquivo .env local

===================================================
  INFORMAÇÕES TÉCNICAS
===================================================

Versão: 1.0
Desenvolvedor: [Seu Nome]
Email: [Seu Email]
GitHub: [Seu Repositório]

Tecnologias:
- Python 3.x
- Deepgram SDK (API Nova-3)
- CustomTkinter (Interface)
- Watchdog (Monitoramento de arquivos)

Compilado com PyInstaller

===================================================
  LICENÇA E CRÉDITOS
===================================================

Este aplicativo utiliza:
- Deepgram API para transcrição
- Bibliotecas Python open-source

Para uso pessoal e comercial conforme termos de uso
das bibliotecas utilizadas.

===================================================

Obrigado por usar o Audio Transcriptor!

Para suporte: [seu_email]

===================================================
