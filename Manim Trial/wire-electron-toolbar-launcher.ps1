# Wires Manim Trial setup into electron-toolbar Launcher Panel (📚 grid).
# Idempotent — safe to rerun from setup.ps1 or on its own.

$ErrorActionPreference = 'Stop'

$manimRoot = $PSScriptRoot
$programsRoot = Split-Path $manimRoot -Parent
$toolbarRoot = Join-Path $programsRoot 'electron-toolbar'
$tileId = 'manim-trial-setup'
$tileLabel = 'Manim Setup'
$launcherBatName = 'Launch-Manim-Setup.bat'
$setupVbs = Join-Path $manimRoot 'Setup Manim Trial.vbs'
$logPath = Join-Path $manimRoot 'wire-launcher.log'

function Write-Log($Message) {
    "$(Get-Date -Format 's')  $Message" | Add-Content -Path $logPath -Encoding utf8
    Write-Host $Message
}

function Resolve-ToolbarFile($RelativePath) {
    $path = Join-Path $toolbarRoot $RelativePath
    if (-not (Test-Path $path)) {
        throw "Missing electron-toolbar file: $RelativePath"
    }
    return $path
}

function Ensure-LauncherBat {
    $launcherDir = Join-Path $toolbarRoot 'launcher'
    if (-not (Test-Path $launcherDir)) {
        New-Item -ItemType Directory -Path $launcherDir | Out-Null
    }
    if (-not (Test-Path $setupVbs)) {
        throw "Missing setup VBS: $setupVbs"
    }
    $batPath = Join-Path $launcherDir $launcherBatName
    $vbsRelative = '..\..\Manim Trial\Setup Manim Trial.vbs'
    @(
        '@echo off',
        "wscript.exe //B ""%~dp0$vbsRelative""",
        'exit /b 0'
    ) | Set-Content -Path $batPath -Encoding ascii
    Write-Log "Wrote $batPath"
}

function Add-Tile-To-ScriptsPanel {
    $panelPath = Resolve-ToolbarFile 'electron-app/src/scripts-panel.html'
    $text = Get-Content -Path $panelPath -Raw -Encoding utf8
    if ($text -match [regex]::Escape($tileId)) {
        Write-Log "scripts-panel.html already lists $tileId"
        return $false
    }

    $exemplars = @('guildrun-stats', 'video-player', 'agent-browser', 'quasimorph-tracker')
    $exemplar = $exemplars | Where-Object { $text -match [regex]::Escape("'$_'") -or $text -match [regex]::Escape('"$_"') } | Select-Object -First 1
    if (-not $exemplar) {
        throw 'Could not find a non-school launcher exemplar in scripts-panel.html'
    }

    if ($text -match "(?m)^(?<indent>\s*)\{\s*id:\s*['""]$exemplar['""]") {
        $indent = $Matches['indent']
        $objectLine = "${indent}{ id: '$tileId', label: '$tileLabel' },"
        $pattern = "(?m)^$([regex]::Escape($indent))\{\s*id:\s*['""]$exemplar['""][^\n]*\n"
        $text = [regex]::Replace($text, $pattern, { param($m) "$m`n$objectLine" }, 1)
    }

    if ($text -match "(?m)^(?<indent>\s*)['""]$exemplar['""],\s*$") {
        $indent = $Matches['indent']
        $idLine = "${indent}'$tileId',"
        $pattern = "(?m)^$([regex]::Escape($indent))['""]$exemplar['""],\s*$"
        $text = [regex]::Replace($text, $pattern, { param($m) "$m`n$idLine" }, 1)
    } elseif ($text -match "requiredIds\s*=\s*\[") {
        $text = [regex]::Replace(
            $text,
            "(['""]$exemplar['""])",
            "`$1, '$tileId'",
            1
        )
    } else {
        throw 'Could not locate requiredIds entry point in scripts-panel.html'
    }

    Set-Content -Path $panelPath -Value $text -Encoding utf8 -NoNewline
    Write-Log "Added $tileId to scripts-panel.html (cloned from $exemplar)"
    return $true
}

function Add-Tile-To-PackagedLaunchers {
    $candidates = Get-ChildItem -Path $toolbarRoot -Recurse -Filter 'packaged-launchers.json' -ErrorAction SilentlyContinue
    if (-not $candidates) {
        throw 'packaged-launchers.json not found under electron-toolbar'
    }
    $jsonPath = ($candidates | Sort-Object FullName | Select-Object -First 1).FullName
    $raw = Get-Content -Path $jsonPath -Raw -Encoding utf8
    if ($raw -match [regex]::Escape($tileId)) {
        Write-Log "packaged-launchers.json already lists $tileId"
        return $false
    }

    $exemplars = @('guildrun-stats', 'video-player', 'agent-browser', 'quasimorph-tracker')
    $exemplar = $exemplars | Where-Object { $raw -match [regex]::Escape('"$_"') -or $raw -match [regex]::Escape("'$_'") } | Select-Object -First 1
    if (-not $exemplar) {
        throw 'Could not find a packaged launcher exemplar in packaged-launchers.json'
    }

    if ($raw -match "(?ms)(?<block>\s*""$exemplar""\s*:\s*\{.*?\}\s*,?)") {
        $block = $Matches['block']
        $newBlock = $block -replace [regex]::Escape($exemplar), $tileId
        $newBlock = $newBlock -replace 'Launch-[^"\\]+\\.bat', $launcherBatName
        $newBlock = $newBlock -replace 'Guildrun Stats|Video Player|Agent Browser|Quasimorph Tracker', $tileLabel
        $text = $raw -replace [regex]::Escape($block), ($block + $newBlock)
        Set-Content -Path $jsonPath -Value $text -Encoding utf8 -NoNewline
        Write-Log "Added $tileId to $jsonPath (cloned from $exemplar)"
        return $true
    }

    throw 'Could not clone packaged launcher block in packaged-launchers.json'
}

function Commit-ToolbarRepo {
    Push-Location $toolbarRoot
    try {
        $status = git status --short 2>$null
        if (-not $status) {
            Write-Log 'electron-toolbar: no git changes to commit'
            return
        }
        git add -A
        git commit -m "Add Manim Trial setup tile to Launcher Panel ($tileId)"
        git push
        Write-Log 'electron-toolbar: committed and pushed launcher tile'
    } finally {
        Pop-Location
    }
}

if (-not (Test-Path $toolbarRoot)) {
    throw "electron-toolbar not found at $toolbarRoot"
}

Write-Log 'Starting Manim Trial launcher wiring'
Ensure-LauncherBat
$panelChanged = Add-Tile-To-ScriptsPanel
$packagedChanged = Add-Tile-To-PackagedLaunchers
if ($panelChanged -or $packagedChanged) {
    Commit-ToolbarRepo
}
Write-Log 'Launcher Panel wiring complete'
