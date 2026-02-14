python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m PyInstaller --onefile --name conforme-audit .\conforme_toolkit\cli.py
python -m PyInstaller --onefile --windowed --name conforme-gui .\conforme_toolkit\gui.py
Write-Host "Build completata."
Write-Host "CLI: .\dist\conforme-audit.exe"
Write-Host "GUI: .\dist\conforme-gui.exe"
