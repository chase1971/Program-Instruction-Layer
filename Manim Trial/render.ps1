$ErrorActionPreference = 'Stop'
$texBin = Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64'
$env:PATH = "$texBin;$env:PATH"
Push-Location $PSScriptRoot
try {
    & '.\.venv\Scripts\python.exe' -m manim -ql --disable_caching verify_render.py DivisionCheck
    if ($LASTEXITCODE -ne 0) { throw 'Manim render failed.' }
} finally {
    Pop-Location
}
