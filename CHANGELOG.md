# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

Il formato segue, in modo semplificato, le categorie: `Aggiunto`, `Modificato`, `Corretto`.

## [Unreleased]
### Aggiunto
- Pagina supporto progetto: `docs/sostieni-il-progetto.md`.
- Script `npm run setup` con creazione configurazione base e cartella report.
- Script `npm run audit` per eseguire audit da `conforme.config.json`.

### Modificato
- Configurazione finanziamento aggiornata in `.github/FUNDING.yml`.
- Link Discussions corretto in `.github/ISSUE_TEMPLATE/config.yml`.
- Sezione finanziamento aggiornata nel `README.md`.
- Rimossi riferimenti diretti a GitHub Sponsors non ancora approvato.
- Documentazione aggiornata con flusso setup/audit.

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
