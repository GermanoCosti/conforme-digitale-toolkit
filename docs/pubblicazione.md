# Pubblicazione (npm, PyPI, EXE)

Questo repository contiene 2 distribuzioni separate:

- **npm** (Node.js): pacchetto `@germanocosti/conforme-digitale-toolkit` (CLI)
- **PyPI** (Python): pacchetto `conforme-digitale-toolkit-germanocosti` (CLI + GUI) dentro `python-app/`

In piu, puoi pubblicare una **Release GitHub** con allegati Windows `.exe`.

## 1) Pubblicare su npm (CLI Node)

Prerequisiti:
- account npm
- 2FA attiva (consigliato)
- token per automazione (`Automation token`)

Passi:
1. In GitHub vai su `Settings -> Secrets and variables -> Actions` e aggiungi:
   - secret `NPM_TOKEN` = token npm
2. Aggiorna la versione in `package.json` (es. `0.2.1`) e fai push su `main`.
3. Crea un tag Git (es. `v0.2.1`) e push del tag.
4. Il workflow `Publish npm` pubblichera il pacchetto.

Comando installazione per gli utenti:
```bash
npm i -g @germanocosti/conforme-digitale-toolkit
conforme-digitale --help
```

## 2) Pubblicare su PyPI (Python)

Prerequisiti:
- account PyPI
- token API di PyPI

Passi:
1. In GitHub vai su `Settings -> Secrets and variables -> Actions` e aggiungi:
   - secret `PYPI_API_TOKEN` = token PyPI
2. Aggiorna la versione in `python-app/pyproject.toml` (es. `0.2.1`) e fai push su `main`.
3. Crea un tag Git (es. `v0.2.1`) e push del tag.
4. Il workflow `Publish PyPI` pubblichera il pacchetto.

Comando installazione per gli utenti:
```bash
python -m pip install conforme-digitale-toolkit-germanocosti
conforme-digitale --help
conforme-digitale-gui
```

## 3) Release GitHub con EXE Windows

Quando pubblichi una Release (GitHub -> Releases -> Create a new release),
il workflow `Build Windows EXE` compila e allega:
- `conforme-digitale.exe`
- `conforme-digitale-gui.exe`

Nota: l'eseguibile potrebbe essere segnalato da SmartScreen (normale per exe non firmati).

