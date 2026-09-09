# Wires Manim Trial setup into electron-toolbar Launcher Panel (📚 grid).
# Idempotent — run via Wire Manim Toolbar.vbs or setup.ps1 after deps install.

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
    @(
        '@echo off',
        'wscript.exe //B "%~dp0..\..\Manim Trial\Setup Manim Trial.vbs"',
        'exit /b 0'
    ) | Set-Content -Path $batPath -Encoding ascii
    Write-Log "Wrote $batPath"
}

function Add-Tile-To-TextFile {
    param(
        [string]$FilePath,
        [string[]]$Exemplars
    )

    $text = Get-Content -Path $FilePath -Raw -Encoding utf8
    if ($text -match [regex]::Escape($tileId)) {
        Write-Log "$(Split-Path $FilePath -Leaf) already lists $tileId"
        return $false
    }

    $exemplar = $Exemplars | Where-Object {
        $text -match [regex]::Escape("'$_'") -or $text -match [regex]::Escape('"$_"')
    } | Select-Object -First 1
    if (-not $exemplar) {
        throw "Could not find launcher exemplar in $(Split-Path $FilePath -Leaf)"
    }

    $changed = $false

    if ($text -match "(?m)^(?<indent>\s*)\{\s*id:\s*['""]$exemplar['""]") {
        $indent = $Matches['indent']
        $objectLine = "${indent}{ id: '$tileId', label: '$tileLabel' },"
        $pattern = "(?m)^$([regex]::Escape($indent))\{\s*id:\s*['""]$exemplar['""][^\n]*\n"
        $text = [regex]::Replace($text, $pattern, { param($m) "$m`n$objectLine" }, 1)
        $changed = $true
    }

    if ($text -match "(?m)^(?<indent>\s*)['""]$exemplar['""],\s*$") {
        $indent = $Matches['indent']
        $idLine = "${indent}'$tileId',"
        $pattern = "(?m)^$([regex]::Escape($indent))['""]$exemplar['""],\s*$"
        $text = [regex]::Replace($text, $pattern, { param($m) "$m`n$idLine" }, 1)
        $changed = $true
    } elseif ($text -match "requiredIds\s*=\s*\[") {
        $text = [regex]::Replace($text, "(['""]$exemplar['""])", "`$1, '$tileId'", 1)
        $changed = $true
    }

    if (-not $changed) {
        throw "Could not patch $(Split-Path $FilePath -Leaf) using exemplar $exemplar"
    }

    Set-Content -Path $FilePath -Value $text -Encoding utf8 -NoNewline
    Write-Log "Added $tileId to $(Split-Path $FilePath -Leaf) (cloned from $exemplar)"
    return $true
}

function Add-Tile-To-ScriptsPanel {
    $panelPath = Resolve-ToolbarFile 'electron-app/src/scripts-panel.html'
    return Add-Tile-To-TextFile -FilePath $panelPath -Exemplars @(
        'guildrun-stats', 'video-player', 'agent-browser', 'quasimorph-tracker'
    )
}

function Add-Tile-To-Profiles {
    $profileDir = Join-Path $toolbarRoot 'config/profiles'
    if (-not (Test-Path $profileDir)) { return $false }

    $any = $false
    Get-ChildItem -Path $profileDir -Filter '*.json' | ForEach-Object {
        $raw = Get-Content -Path $_.FullName -Raw -Encoding utf8
        if ($raw -notmatch 'requiredIds|guildrun-stats|video-player') { return }
        if ($raw -match [regex]::Escape($tileId)) { return }
        try {
            if (Add-Tile-To-TextFile -FilePath $_.FullName -Exemplars @(
                'guildrun-stats', 'video-player', 'agent-browser', 'quasimorph-tracker'
            )) {
                $any = $true
            }
        } catch {
            Write-Log "Skipped profile $($_.Name): $($_.Exception.Message)"
        }
    }
    return $any
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
    $exemplar = $exemplars | Where-Object {
        $raw -match [regex]::Escape('"$_"') -or $raw -match [regex]::Escape("'$_'")
    } | Select-Object -First 1
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

try {
    if (-not (Test-Path $toolbarRoot)) {
        throw "electron-toolbar not found at $toolbarRoot"
    }

    Write-Log 'Starting Manim Trial launcher wiring'
    Ensure-LauncherBat
    $panelChanged = Add-Tile-To-ScriptsPanel
    $profileChanged = Add-Tile-To-Profiles
    $packagedChanged = Add-Tile-To-PackagedLaunchers
    if ($panelChanged -or $profileChanged -or $packagedChanged) {
        Commit-ToolbarRepo
    }
    Write-Log 'Launcher Panel wiring complete — restart electron-toolbar if the tile is not visible'
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    throw
}
