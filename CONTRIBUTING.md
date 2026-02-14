# Contributing Guide

Grazie per il tuo interesse nel contribuire.

## Come iniziare
1. Fai fork del repository.
2. Crea un branch dedicato: `feat/nome-breve` o `fix/nome-breve`.
3. Installa dipendenze: `npm install`.
4. Esegui test: `npm test`.
5. Apri una Pull Request verso `main`.

## Standard minimi
- Mantieni il codice semplice e leggibile.
- Aggiungi o aggiorna test quando introduci logica nuova.
- Evita breaking change non discusse prima.
- Mantieni messaggi commit chiari.

## Convenzioni suggerite
- `feat:` nuove funzionalita
- `fix:` bugfix
- `docs:` documentazione
- `refactor:` refactoring senza cambio comportamento
- `test:` test

## Aprire issue utili
Includi sempre:
- comportamento atteso
- comportamento attuale
- passaggi per riprodurre
- file HTML minimo di esempio (se rilevante)

## Processo review
- Almeno una review prima del merge.
- CI verde obbligatoria per merge.
