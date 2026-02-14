# Conforme Digitale Toolkit v0.1.1

Rilascio di miglioramento orientato a chiarezza, onboarding e copertura dei controlli.

## Novita principali
- Aggiunti nuovi controlli:
  - presenza `lang` su `<html>`
  - presenza `<h1>`
  - link senza nome accessibile
- Migliorata la CLI:
  - supporto `--help`
  - riepilogo severita in italiano (`Alta`, `Media`)
- Aggiunti esempi pronti:
  - `examples/sample.html` (con problemi)
  - `examples/sample-good.html` (corretto)
- Documentazione migliorata:
  - `README.md` con avvio rapido in 2 minuti
  - `docs/getting-started-it.md` con guida passo-passo in italiano

## Verifica rapida
```bash
npm test
node src/cli.js --file ./examples/sample.html --out ./report.json
```

## Nota
Questa versione resta una base tecnica iniziale: non sostituisce una verifica manuale completa WCAG.
