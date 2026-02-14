# Conforme Digitale Toolkit v0.2.0

Questa release introduce la prima funzione realmente pratica per l'uso quotidiano: analisi diretta di un sito via URL.

## Novita principali
- Nuovo supporto CLI per audit da URL:
  - `--url https://esempio.it`
- Possibilita di salvare il risultato in JSON anche da URL:
  - `--out ./report.json`
- Documentazione aggiornata in italiano con esempi reali.
- Blocco dipendenze con `package-lock.json` per installazioni piu coerenti.

## Esempi rapidi
```bash
node src/cli.js --url https://example.com --out ./report.json
node src/cli.js --file ./examples/sample.html --out ./report.json
```

## Perche e importante
Prima era necessario avere un file locale; ora puoi analizzare direttamente una pagina web e usare il report come base operativa con clienti o team tecnici.

## Nota
Il toolkit resta una base tecnica iniziale e non sostituisce una verifica manuale completa WCAG.
