# Starts scripts/serve-programs-docs.js on port 8765 if it is not already up.
# No window. Safe to call repeatedly from launchers (Guildrun Stats, etc.).

$ErrorActionPreference = 'SilentlyContinue'
$uri = 'http://127.0.0.1:8765/'

try {
    $r = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 2
    if ($r.StatusCode -eq 200) { exit 0 }
} catch {}

$programsRoot = Split-Path -Parent $PSScriptRoot
$script = Join-Path $PSScriptRoot 'serve-programs-docs.js'

if (-not (Test-Path -LiteralPath $script)) {
    exit 1
}

$node = (Get-Command node.exe -ErrorAction SilentlyContinue).Source
if (-not $node) {
    exit 1
}

Start-Process -FilePath $node -ArgumentList @("`"$script`"") -WorkingDirectory $programsRoot -WindowStyle Hidden | Out-Null

for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 250
    try {
        $r = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 1
        if ($r.StatusCode -eq 200) { exit 0 }
    } catch {}
}

exit 0
