# Starts the personal "My Machines" Cloud Agent worker so this tree is reachable
# from cursor.com/agents on a phone while the desktop is left running.
#
# Two things this handles that a bare `agent worker start` does not:
#   1. --idle-release-timeout 0 - the CLI default of 3600 drops the worker after an
#      hour idle, which would silently remove the machine from the phone's picker.
#   2. Node ABI selection - build 2026.09.02-c22c1a3 bundles node 24 (ABI 137) but
#      ships better_sqlite3.node built for ABI 127, so the bundled runtime cannot
#      start the exec-daemon. The probe below prefers the bundled node and falls
#      back to system node, so this self-corrects once the bundle is fixed.

# Not 'Stop': the runtime probe below deliberately provokes stderr from node, which
# PowerShell surfaces as a terminating NativeCommandError. This loop logs its own errors.
$ErrorActionPreference = 'Continue'

$agentRoot  = Join-Path $env:LOCALAPPDATA 'cursor-agent'
$logPath    = Join-Path $agentRoot 'worker-launcher.log'
$workerName = 'desktop'

$workerDirs = @(
    'C:\Users\chase\Documents\Programs',
    'C:\Users\chase\Documents\Programs\School Scrips\Macro App',
    'C:\Users\chase\Documents\Programs\School Scrips\App Dashboard',
    'C:\Users\chase\Documents\Programs\electron-toolbar'
)

function Write-Log {
    param([string]$Message)
    if ((Test-Path $logPath) -and ((Get-Item $logPath).Length -gt 1MB)) {
        Remove-Item $logPath -Force -ErrorAction SilentlyContinue
    }
    "$(Get-Date -Format 's')  $Message" | Add-Content -Path $logPath -Encoding utf8
}

function Get-LatestVersionDir {
    $versions = Join-Path $agentRoot 'versions'
    if (-not (Test-Path $versions)) { return $null }
    Get-ChildItem $versions -Directory |
        Where-Object { $_.Name -match '^\d{4}\.\d{1,2}\.\d{1,2}(-\d{2}-\d{2}-\d{2})?-[a-f0-9]+$' } |
        Sort-Object {
            $p = $_.Name.Split('-')[0].Split('.')
            [int]("$($p[0])$($p[1].PadLeft(2,'0'))$($p[2].PadLeft(2,'0'))")
        } -Descending |
        Select-Object -First 1
}

# A runtime is usable only if it can dlopen the ABI-specific sqlite binding.
function Test-NodeRuntime {
    param([string]$NodeExe, [string]$VersionDir)
    if (-not $NodeExe) { return $false }
    $binding = Join-Path $VersionDir 'node_modules\better-sqlite3\build\Release\better_sqlite3.node'
    if (-not (Test-Path $binding)) { return $true }
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    try {
        & $NodeExe -e "require(process.argv[1])" $binding 2>&1 | Out-Null
        return ($LASTEXITCODE -eq 0)
    } finally {
        $ErrorActionPreference = $prev
    }
}

function Resolve-NodeExe {
    param([string]$VersionDir)
    $bundled = Join-Path $VersionDir 'node.exe'
    if ((Test-Path $bundled) -and (Test-NodeRuntime -NodeExe $bundled -VersionDir $VersionDir)) {
        Write-Log 'runtime: bundled node.exe'
        return $bundled
    }
    $system = (Get-Command node.exe -ErrorAction SilentlyContinue).Source
    if ($system -and (Test-NodeRuntime -NodeExe $system -VersionDir $VersionDir)) {
        Write-Log "runtime: system node ($system) - bundled node rejected the sqlite binding"
        return $system
    }
    return $null
}

$env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' +
            [Environment]::GetEnvironmentVariable('Path', 'Machine')
if (-not $env:CURSOR_INVOKED_AS) { $env:CURSOR_INVOKED_AS = 'cursor-agent' }

$workerArgs = @('worker', 'start', '--name', $workerName, '--idle-release-timeout', '0', '--wait', '60')
foreach ($d in $workerDirs) {
    if (Test-Path $d) { $workerArgs += @('--worker-dir', $d) } else { Write-Log "skipped missing dir: $d" }
}

# A released worker exits 0 expecting a supervisor to restart it, so supervise here.
# Back off on repeated fast failures instead of hammering a broken install.
$consecutiveFastExits = 0

while ($true) {
    $versionDir = Get-LatestVersionDir
    if (-not $versionDir) { Write-Log 'no agent version directory found; giving up'; break }

    $nodeExe = Resolve-NodeExe -VersionDir $versionDir.FullName
    if (-not $nodeExe) { Write-Log 'no usable node runtime found; giving up'; break }

    $entry   = Join-Path $versionDir.FullName 'index.js'
    $started = Get-Date
    Write-Log "starting worker '$workerName' from $($versionDir.Name)"

    & $nodeExe $entry @workerArgs 2>&1 | Add-Content -Path $logPath -Encoding utf8
    $code    = $LASTEXITCODE
    $ranFor  = (Get-Date) - $started
    Write-Log "worker exited code=$code after $([int]$ranFor.TotalSeconds)s"

    if ($ranFor.TotalSeconds -lt 30) { $consecutiveFastExits++ } else { $consecutiveFastExits = 0 }
    if ($consecutiveFastExits -ge 5) { Write-Log 'five fast exits in a row; giving up'; break }

    Start-Sleep -Seconds ([Math]::Min(300, 10 * [Math]::Max(1, $consecutiveFastExits)))
}
