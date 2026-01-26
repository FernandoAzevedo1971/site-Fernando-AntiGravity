# Script PowerShell para criar pacote de distribuição
# Execute com: .\create_package.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Audio Transcriptor - Criador de Pacote" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurações
$projectDir = $PSScriptRoot
$packageDir = Join-Path $projectDir "AudioTranscriptor_Package"
$distDir = Join-Path $projectDir "dist"
$exeName = "AudioTranscriptor.exe"
$zipName = "AudioTranscriptor_v1.0.zip"

# Passo 1: Verificar se o executável existe
Write-Host "[1/5] Verificando executável..." -ForegroundColor Yellow

if (-not (Test-Path (Join-Path $distDir $exeName))) {
    Write-Host "ERRO: Executável não encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: python build_exe.py" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Executável encontrado" -ForegroundColor Green

# Passo 2: Criar pasta de pacote
Write-Host "[2/5] Criando pasta de pacote..." -ForegroundColor Yellow

if (Test-Path $packageDir) {
    Remove-Item $packageDir -Recurse -Force
}

New-Item -ItemType Directory -Path $packageDir | Out-Null
Write-Host "✓ Pasta criada: $packageDir" -ForegroundColor Green

# Passo 3: Copiar arquivos necessários
Write-Host "[3/5] Copiando arquivos..." -ForegroundColor Yellow

# Copiar executável
Copy-Item (Join-Path $distDir $exeName) $packageDir
Write-Host "  ✓ Copiado: $exeName" -ForegroundColor Green

# Copiar .env.example
Copy-Item (Join-Path $projectDir ".env.example") $packageDir
Write-Host "  ✓ Copiado: .env.example" -ForegroundColor Green

# Copiar README
Copy-Item (Join-Path $projectDir "README_DISTRIBUICAO.txt") (Join-Path $packageDir "LEIA-ME.txt")
Write-Host "  ✓ Copiado: LEIA-ME.txt" -ForegroundColor Green

# Passo 4: Criar arquivo ZIP
Write-Host "[4/5] Comprimindo pacote..." -ForegroundColor Yellow

$zipPath = Join-Path $projectDir $zipName

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path "$packageDir\*" -DestinationPath $zipPath
Write-Host "✓ Arquivo ZIP criado: $zipName" -ForegroundColor Green

# Passo 5: Informações finais
Write-Host "[5/5] Resumo do pacote:" -ForegroundColor Yellow
Write-Host ""

$zipSize = (Get-Item $zipPath).Length / 1MB
Write-Host "  Localização: $zipPath" -ForegroundColor Cyan
Write-Host "  Tamanho: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " PACOTE CRIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "1. Envie o arquivo $zipName para o usuário final"
Write-Host "2. Instrua-o a seguir o arquivo LEIA-ME.txt"
Write-Host "3. Certifique-se de que ele configure o arquivo .env"
Write-Host ""
Write-Host "NOTA IMPORTANTE:" -ForegroundColor Red
Write-Host "Lembre o usuário de configurar:" -ForegroundColor Red
Write-Host "  - DEEPGRAM_API_KEY (obrigatório)"
Write-Host "  - WATCH_DIRECTORY (caminho da pasta a monitorar)"
Write-Host ""

# Abrir pasta do pacote
$openFolder = Read-Host "Deseja abrir a pasta do pacote? (S/N)"
if ($openFolder -eq "S" -or $openFolder -eq "s") {
    Invoke-Item $projectDir
}
