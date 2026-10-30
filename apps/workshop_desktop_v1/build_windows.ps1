# Build from a clean Windows Python 3.11 environment. Requires Git and network for PyInstaller.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python -m pip install --disable-pip-version-check "pyinstaller==6.16.0"
if ($LASTEXITCODE -ne 0) { throw "PyInstaller install failed" }
python -m PyInstaller --noconfirm --clean --onedir --windowed --name WORKSHOPDesktopV1 --paths "..\workshop_g1" --add-data "..\workshop_g1\workshop_g1\trusted;workshop_g1\trusted" main.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }
$compiler = Get-Command ISCC.exe -ErrorAction SilentlyContinue
if ($compiler) {
  & $compiler.Source (Join-Path $PSScriptRoot "installer.iss")
  if ($LASTEXITCODE -ne 0) { throw "Inno Setup build failed" }
} else {
  Write-Output "ONEDIR_CREATED; INNO_INSTALLER_NOT_BUILT (ISCC.exe unavailable)"
}
