python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m PyInstaller --onefile --name conforme-audit .\conforme_toolkit\cli.py
Write-Host "Build completata. Eseguibile in: .\dist\conforme-audit.exe"
