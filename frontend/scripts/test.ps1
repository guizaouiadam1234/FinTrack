param(
    [ValidateSet('all', 'unit', 'integration', 'cov-html', 'watch')]
    [string]$Mode = 'all'
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Split-Path -Parent $scriptDir
Set-Location $frontendDir

switch ($Mode) {
    'all' { npm run test }
    'unit' { npm run test:unit }
    'integration' { npm run test:integration }
    'cov-html' { npm run test:cov-html }
    'watch' { npm run test:watch }
}
