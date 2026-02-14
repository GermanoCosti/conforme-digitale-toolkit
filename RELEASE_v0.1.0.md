# Accessibility Compliance Toolkit v0.1.0

Prima release pubblica del progetto.

## Cosa include
- CLI per audit accessibilita base su file HTML locale.
- Rilevazione automatica di:
  - immagini senza `alt`
  - input senza `label`/`aria-label`
  - button senza testo o `aria-label`
- Report JSON esportabile (`--out`).
- Test automatici iniziali.
- Pipeline CI su GitHub Actions.

## Comando rapido
```bash
node src/cli.js --file ./pagina.html --out ./report.json
```

## Note importanti
- Questa versione e un MVP tecnico, non sostituisce audit manuale WCAG completo.
- Obiettivo: fornire un controllo iniziale rapido e ripetibile.

## Prossimi step (roadmap breve)
1. Regole aggiuntive (contrasto, heading order, link name).
2. Scansione multipagina.
3. Report PDF e dashboard Pro.
