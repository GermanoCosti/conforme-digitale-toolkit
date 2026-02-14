# Accessibility Compliance Toolkit

Toolkit open source per controlli accessibilita web di base, pensato per il contesto Italia/EU.

## Perche esiste
Molte PMI hanno siti con problemi evidenti di accessibilita e nessun processo minimo di controllo.
Questo progetto offre un primo audit automatico ripetibile da CLI.

## Cosa fa (MVP)
- Cerca immagini senza `alt`.
- Cerca campi input senza label associata.
- Cerca pulsanti senza testo o `aria-label`.
- Controlla presenza attributo `lang` nel tag `<html>`.
- Controlla presenza heading principale `<h1>`.
- Cerca link senza testo o `aria-label`.
- Esporta report JSON con riepilogo issue.

## Cosa non fa (ancora)
- Non sostituisce audit manuale WCAG completo.
- Non emette certificazioni legali.

## Installazione locale
```bash
npm install
```

## Uso
```bash
node src/cli.js --file ./examples/sample.html --out ./report.json
```

```bash
node src/cli.js --help
```

Output atteso:
- riepilogo in console
- file JSON con issue trovate

## Demo rapida
```bash
node src/cli.js --file ./examples/sample.html --out ./report.json
node src/cli.js --file ./examples/sample-good.html
```

## Struttura
- `src/audit.js`: logica audit HTML
- `src/cli.js`: interfaccia comando
- `tests/run.js`: test base
- `docs/roadmap.md`: roadmap prodotto

## Monetizzazione consigliata (ibrida)
1. OSS gratuito per acquisizione utenti.
2. Versione Pro: scansione multi pagina, dashboard, PDF export.
3. Servizio done-for-you: setup + remediation per agenzie/PMI.

## Funding
Configura `.github/FUNDING.yml` con il tuo username GitHub Sponsors.

## Community e governance
- `LICENSE`: licenza MIT
- `CONTRIBUTING.md`: regole contributi
- `CODE_OF_CONDUCT.md`: regole comportamento
- `.github/ISSUE_TEMPLATE/`: template issue
- `.github/pull_request_template.md`: template PR

## Stato
Versione iniziale `0.1.0` pronta per primo rilascio pubblico.
