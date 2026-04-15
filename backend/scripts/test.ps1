param(
    [ValidateSet('all', 'unit', 'integration', 'cov-html')]
    [string]$Mode = 'all'
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Split-Path -Parent $scriptDir
Set-Location $backendDir

$python = Join-Path (Split-Path -Parent $backendDir) '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    throw "Python executable not found at $python"
}

switch ($Mode) {
    'all' { & $python -m pytest }
    'unit' { & $python -m pytest -m unit --no-cov }
    'integration' { & $python -m pytest -m integration --no-cov }
    'cov-html' { & $python -m pytest --cov-report=html }
}
