python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m PyInstaller --onefile --name conforme-digitale .\conforme_toolkit\cli.py
python -m PyInstaller --onefile --windowed --name conforme-digitale-gui .\conforme_toolkit\gui.py
Write-Host "Build completata."
Write-Host "CLI: .\dist\conforme-digitale.exe"
Write-Host "GUI: .\dist\conforme-digitale-gui.exe"
