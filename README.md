# Accessibility Compliance Toolkit

Toolkit open source per controlli accessibilita web di base, pensato per il contesto Italia/EU.

## Avvio rapido (2 minuti)
1. Installa Node.js (versione 18+ consigliata).
2. Apri terminale nella cartella progetto.
3. Esegui:

```bash
npm install
npm test
node src/cli.js --file ./examples/sample.html --out ./report.json
```

4. Apri `report.json` per vedere i problemi trovati.

## Avvio con configurazione (consigliato)
```bash
npm run setup
npm run audit
```

Questo crea:
- `conforme.config.json` (configurazione audit)
- `report/report.json` (risultato)

Nel repository trovi anche un esempio:
- `conforme.config.example.json`

## Perche esiste
Molte PMI hanno siti con problemi evidenti di accessibilita e nessun processo minimo di controllo.
Questo progetto offre un primo audit automatico ripetibile da CLI.

## Cosa fa (versione minima)
- Cerca immagini senza `alt`.
- Cerca campi input senza label associata.
- Cerca pulsanti senza testo o `aria-label`.
- Controlla presenza attributo `lang` nel tag `<html>`.
- Controlla presenza heading principale `<h1>`.
- Cerca link senza testo o `aria-label`.
- Esporta report JSON con riepilogo problemi.

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
node src/cli.js --url https://example.com --out ./report.json
```

```bash
node src/cli.js --help
```

```bash
npm run setup
npm run audit
```

Risultato atteso:
- riepilogo in console
- file JSON con issue trovate

Esempio risultato console:
```text
Audit completato.
Punteggio: 10
Problemi: 6
Alta: 2 | Media: 4
Report salvato in: .../report.json
```

## Demo rapida
```bash
node src/cli.js --file ./examples/sample.html --out ./report.json
node src/cli.js --file ./examples/sample-good.html
node src/cli.js --url https://example.com --out ./report.json
```

## Struttura
- `src/audit.js`: logica audit HTML
- `src/cli.js`: interfaccia comando
- `tests/run.js`: test base
- `docs/roadmap.md`: piano evolutivo prodotto
- `docs/getting-started-it.md`: guida rapida in italiano
- `docs/sostieni-il-progetto.md`: modalita di supporto
- `python-app/`: prototipo Python CLI + interfaccia grafica con build `.exe`

## Monetizzazione consigliata (ibrida)
1. OSS gratuito per acquisizione utenti.
2. Versione Pro: scansione multipagina, pannello, esportazione PDF.
3. Servizio fatto-per-te: configurazione + correzioni per agenzie/PMI.
4. Setup assistito su contributo volontario (il tool base resta gratuito).

## Finanziamento
Se il progetto ti e utile, puoi sostenerlo qui:
- Pagina supporto: `docs/sostieni-il-progetto.md`

## Community e governance
- `LICENSE`: licenza MIT
- `CONTRIBUTING.md`: regole contributi
- `CODE_OF_CONDUCT.md`: regole comportamento
- `.github/ISSUE_TEMPLATE/`: template issue
- `.github/pull_request_template.md`: template PR

## Stato
Versione iniziale `0.1.0` pronta per primo rilascio pubblico.

## Per chi lo scarica per la prima volta
Se sei un developer:
1. Lancia i test (`npm test`).
2. Prova il file con errori (`examples/sample.html`).
3. Prova il file corretto (`examples/sample-good.html`).
4. Confronta i risultati e poi analizza il tuo HTML.

Se sei un consulente/agenzia:
1. Chiedi al cliente una pagina HTML export oppure analizza file statici.
2. Esegui il comando CLI e genera `report.json`.
3. Trasforma le issue in checklist di correzione.
4. Ripeti l'audit dopo le modifiche.

## Problemi comuni
1. `npm` non riconosciuto:
   verifica che Node.js sia installato e riapri il terminale.
2. `File non trovato`:
   controlla percorso passato a `--file`.
3. `URL non valido`:
   usa un indirizzo completo con `http://` o `https://`.
4. Nessun output JSON:
   aggiungi `--out ./report.json`.
