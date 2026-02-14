# Prototipo Python Scaricabile

Questa cartella contiene una versione Python del toolkit, pronta per diventare `.exe`.

## Funzioni
- Audit da file HTML (`--file`)
- Audit da URL (`--url`)
- Output JSON (`--out`)

## Avvio rapido
```bash
cd python-app
python .\conforme_toolkit\cli.py --file ..\examples\sample.html --out .\report.json
```

## Test
```bash
python .\tests\run_tests.py
```

Se vuoi installazione pacchetto:
```bash
python -m pip install -e .
conforme-audit --file ..\examples\sample.html --out .\report.json
```

## Build eseguibile Windows
```powershell
cd python-app
.\build_exe.ps1
```

Dopo la build trovi:
- `python-app\dist\conforme-audit.exe`

## Uso eseguibile
```powershell
.\dist\conforme-audit.exe --url https://example.com --out .\report.json
```
