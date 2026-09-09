# One-shot laptop setup for Manim Trial.
# Run from this folder: powershell -ExecutionPolicy Bypass -File .\setup.ps1
# Agent-friendly: no prompts unless winget must install system tools.

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

function Write-Step($Message) {
    Write-Host ""
    Write-Host "==> $Message"
}

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Ensure-Python {
    Write-Step 'Checking Python 3.12+'
    if (-not (Test-Command python)) {
        throw 'Python is not on PATH. Install Python 3.12+ from https://www.python.org/downloads/ with Add to PATH checked, then open a new terminal.'
    }
    $versionText = (& python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')").Trim()
    $parts = $versionText.Split('.')
    $major = [int]$parts[0]
    $minor = [int]$parts[1]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
        throw "Python $versionText found; Manim Trial requires Python 3.12 or newer."
    }
    Write-Host "Python $versionText OK"
}

function Ensure-Uv {
    Write-Step 'Checking uv'
    & python -m uv --version *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Installing uv with pip'
        & python -m pip install --upgrade uv
        if ($LASTEXITCODE -ne 0) { throw 'Failed to install uv.' }
    }
    & python -m uv --version
}

function Ensure-WingetPackage($Id, $Label) {
    if (-not (Test-Command winget)) {
        throw "winget is required to install $Label automatically. Install App Installer from the Microsoft Store, then rerun setup.ps1."
    }
    $list = winget list --id $Id -e 2>$null
    if ($LASTEXITCODE -eq 0 -and $list -match [regex]::Escape($Id)) {
        Write-Host "$Label already installed ($Id)"
        return
    }
    Write-Host "Installing $Label via winget ($Id)"
    winget install --id $Id -e --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -ne 0) { throw "winget install failed for $Label ($Id)." }
}

function Ensure-Ffmpeg {
    Write-Step 'Checking FFmpeg'
    if (Test-Command ffmpeg) {
        & ffmpeg -version | Select-Object -First 1
        return
    }
    Ensure-WingetPackage 'Gyan.FFmpeg' 'FFmpeg'
    if (-not (Test-Command ffmpeg)) {
        throw 'FFmpeg was installed but is not on PATH yet. Close this terminal, open a new one, and rerun setup.ps1.'
    }
}

function Ensure-Miktex {
    Write-Step 'Checking MiKTeX'
    $texBin = Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64'
    $miktexExe = Join-Path $texBin 'miktex.exe'
    if (Test-Path $miktexExe) {
        Write-Host "MiKTeX OK at $texBin"
        return $texBin
    }
    if (Test-Command miktex) {
        Write-Host 'MiKTeX OK (on PATH)'
        return $null
    }
    Ensure-WingetPackage 'MiKTeX.MiKTeX' 'MiKTeX'
    if (Test-Path $miktexExe) {
        Write-Host "MiKTeX installed at $texBin"
        return $texBin
    }
    if (Test-Command miktex) {
        return $null
    }
    throw 'MiKTeX was installed but miktex.exe is not available yet. Close this terminal, open a new one, and rerun setup.ps1.'
}

function Sync-ProjectVenv {
    Write-Step 'Creating project virtual environment and installing Manim'
    & python -m uv sync
    if ($LASTEXITCODE -ne 0) { throw 'uv sync failed.' }
}

function Run-HealthCheck($TexBin) {
    Write-Step 'Running manim checkhealth'
    $pythonExe = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
    if (-not (Test-Path $pythonExe)) {
        throw "Missing $pythonExe after uv sync."
    }
    if ($TexBin) {
        $env:PATH = "$TexBin;$env:PATH"
    }
    & $pythonExe -m manim checkhealth
    if ($LASTEXITCODE -ne 0) { throw 'manim checkhealth reported problems.' }
}

function Run-VerifyRender($TexBin) {
    Write-Step 'Rendering verify_render.py (DivisionCheck, low quality)'
    if ($TexBin) {
        $env:PATH = "$TexBin;$env:PATH"
    }
    & (Join-Path $PSScriptRoot 'render.ps1')
}

Ensure-Python
Ensure-Uv
Ensure-Ffmpeg
$texBin = Ensure-Miktex
Sync-ProjectVenv
Run-HealthCheck -TexBin $texBin
Run-VerifyRender -TexBin $texBin

Write-Step 'Setup complete'
Write-Host 'Manim Trial is ready. Scenes live in this folder; use render.ps1 for headless renders.'
Write-Host 'Style guide: ANIMATION_STYLE_RECIPE.md'
