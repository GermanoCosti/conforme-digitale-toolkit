# Guida rapida

## Obiettivo
Eseguire il primo audit accessibilita su un file HTML in meno di 5 minuti.

## Requisiti
- Node.js installato (18+ consigliato)
- Terminale (PowerShell, cmd, bash)

## Passi
1. Vai nella cartella del progetto:
```bash
cd accessibility-compliance-toolkit
```

2. Installa dipendenze:
```bash
npm install
```

3. Esegui test:
```bash
npm test
```

4. Esegui audit sul file demo con problemi:
```bash
node src/cli.js --file ./examples/sample.html --out ./report.json
```

5. Apri `report.json` e leggi:
- `score`: punteggio complessivo
- `issueCount`: numero totale problemi
- `issues[]`: dettaglio per regola e severita

## Modalita consigliata con configurazione
1. Inizializza:
```bash
npm run setup
```
2. Esegui audit da configurazione:
```bash
npm run audit
```
3. Modifica `conforme.config.json` per scegliere:
- file locale (`"tipo": "file"`)
- sito web (`"tipo": "url"`)

## Regole disponibili nella versione minima
- `img-alt`
- `input-label`
- `button-name`
- `page-lang`
- `heading-h1`
- `link-name`

## Uso sul tuo file
```bash
node src/cli.js --file ./tuo-file.html --out ./report.json
```

## Uso su un sito (URL)
```bash
node src/cli.js --url https://esempio.it --out ./report.json
```
