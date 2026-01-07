Write-Host "=== Configurando entorno Python ==="

# Verificar Python
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python no está disponible en el PATH"
    exit 1
}

# Crear entorno virtual
if (!(Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Entorno virtual creado"
}

# Activar entorno
. .\.venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar librerías
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Warning "requirements.txt no encontrado"
}

# Instalar extensiones de VS Code
if (Test-Path "extensions.txt") {
    Get-Content extensions.txt | ForEach-Object {
        Write-Host "Instalando extensión $_"
        code --install-extension $_
    }
} else {
    Write-Warning "extensions.txt no encontrado"
}

Write-Host "=== Entorno listo ==="
