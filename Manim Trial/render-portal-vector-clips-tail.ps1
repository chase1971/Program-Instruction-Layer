# Finish white PAPER renders for portal clips 5–7 (batch job died mid clip 6).
$ErrorActionPreference = 'Stop'
$texBin = Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64'
$env:PATH = "$texBin;$env:PATH"
$dest = Join-Path $PSScriptRoot '..\School Scrips\student-portal\src\assets\video-examples\vector-projections'
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$clips = @(
    @{ File = 'force_decomposition.py'; Class = 'ForceDecomposition'; Out = 'clip-05-force-decomposition.mp4' },
    @{ File = 'ramp_force.py'; Class = 'RampForce'; Out = 'clip-06-ramp-force.mp4' },
    @{ File = 'work_wagon.py'; Class = 'WorkWagon'; Out = 'clip-07-work-wagon.mp4' }
)
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    foreach ($clip in $clips) {
        Write-Host "Rendering $($clip.Class)..."
        & $python -m manim -qh --disable_caching $clip.File $clip.Class
        if ($LASTEXITCODE -ne 0) { throw "Manim failed on $($clip.Class)" }
        $found = Get-ChildItem -Path 'media\videos' -Recurse -Filter "$($clip.Class).mp4" |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if (-not $found) { throw "No MP4 for $($clip.Class)" }
        Copy-Item -LiteralPath $found.FullName -Destination (Join-Path $dest $clip.Out) -Force
        Write-Host "Copied $($clip.Out)"
    }
    Write-Host 'Portal clips 5–7 updated.'
} finally {
    Pop-Location
}
