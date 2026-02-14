# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

Il formato segue, in modo semplificato, le categorie: `Aggiunto`, `Modificato`, `Corretto`.

## [Unreleased]
### Aggiunto
_Niente di rilevante ancora._

### Modificato
_Niente di rilevante ancora._

## [0.2.1] - 2026-02-14
### Aggiunto
- Preparazione pubblicazione npm (pacchetto scoped) con comando `conforme-digitale`.
- Preparazione pubblicazione PyPI (pacchetto Python) con comandi `conforme-digitale` e `conforme-digitale-gui`.

### Modificato
- Metadati pacchetto npm aggiornati (repository, homepage, publishConfig).
- Metadati pacchetto Python aggiornati (`pyproject.toml`).
- Nomi exe/script aggiornati in `python-app/` per allineamento comandi.

## [0.2.2] - 2026-02-14
### Modificato
- Fix campo `bin` in `package.json` (niente warning "script name was cleaned" in publish).
- Workflow npm con diagnostica (`npm whoami`) per risolvere errori 403 in modo chiaro.

## [0.2.0] - 2026-02-14
### Aggiunto
- Supporto CLI per analisi URL con `--url`.
- `package-lock.json` per installazioni riproducibili.

### Modificato
- Documentazione aggiornata con esempi `--url`.
- Guida rapida estesa con uso su siti reali.

## [0.1.1] - 2026-02-14
### Aggiunto
- Nuove regole audit:
  - `page-lang` per verifica attributo `lang` su `<html>`
  - `heading-h1` per verifica presenza `<h1>`
  - `link-name` per link senza nome accessibile
- Esempi HTML pronti in `examples/sample.html` e `examples/sample-good.html`.
- File `.gitignore` con esclusioni base.
- Guida rapida in italiano: `docs/getting-started-it.md`.

### Modificato
- CLI ora supporta `--help`.
- Output CLI con conteggio problemi per severita (`Alta`, `Media`).
- Test aggiornati a 5 casi.
- README con sezione di avvio rapido e problemi comuni.

## [0.1.0] - 2026-02-14
### Aggiunto
- CLI iniziale (`a11y-it`) per audit HTML locale.
- Regole base:
  - immagini senza `alt`
  - input senza `label` o `aria-label`
  - button senza nome accessibile
- Output report JSON con score e lista issue.
- Test automatici minimi (`tests/run.js`).
- CI GitHub Actions (`.github/workflows/ci.yml`).
- Configurazione funding (`.github/FUNDING.yml`).
- Template issue e PR.
- Documentazione iniziale e roadmap (`README.md`, `docs/roadmap.md`).
- File di governance (`LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`).
