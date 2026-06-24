$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
if (-not (Test-Path ".venv")) {
  & "$PSScriptRoot\install_dev.ps1"
}
& ".\.venv\Scripts\python.exe" -m liveos_community.cli demo --minutes 5

