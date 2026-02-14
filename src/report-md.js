function esc(s) {
  return String(s ?? "").replace(/\r?\n/g, " ").trim();
}

const RULE_HELP = {
  "img-alt": {
    titolo: "Immagini senza testo alternativo (alt)",
    cosa: "Le immagini senza alt non vengono descritte agli screen reader.",
    fix: "Aggiungi alt descrittivo (o alt=\"\" se l'immagine e' puramente decorativa)."
  },
  "input-label": {
    titolo: "Campi input senza etichetta",
    cosa: "Senza label/aria-label, chi usa tecnologie assistive non capisce cosa inserire.",
    fix: "Collega un <label for=\"id\"> oppure usa aria-label/aria-labelledby."
  },
  "button-name": {
    titolo: "Pulsanti senza nome accessibile",
    cosa: "Un button senza testo/aria-label risulta 'vuoto' per screen reader.",
    fix: "Inserisci testo visibile o aria-label."
  },
  "link-name": {
    titolo: "Link senza nome accessibile",
    cosa: "Un link senza testo/aria-label risulta non comprensibile.",
    fix: "Aggiungi testo leggibile o aria-label significativo."
  },
  "page-lang": {
    titolo: "Manca lang su <html>",
    cosa: "Senza lang, screen reader e traduttori possono usare la lingua sbagliata.",
    fix: "Aggiungi lang=\"it\" (o la lingua corretta) nel tag <html>."
  },
  "heading-h1": {
    titolo: "Manca un <h1> principale",
    cosa: "Senza un titolo principale, la pagina e' piu' difficile da navigare.",
    fix: "Aggiungi un <h1> che descriva la pagina."
  },
  "dichiarazione-accessibilita": {
    titolo: "Link alla Dichiarazione di accessibilita non trovato",
    cosa: "In Italia spesso e' richiesto pubblicare e rendere facilmente raggiungibile la dichiarazione.",
    fix: "Aggiungi nel footer un link chiaro tipo 'Dichiarazione di accessibilita' verso la pagina dedicata."
  },
  "feedback-accessibilita": {
    titolo: "Canale di feedback accessibilita non trovato",
    cosa: "Gli utenti devono poter segnalare problemi di accessibilita in modo semplice.",
    fix: "Aggiungi un contatto dedicato (email/form) e rendilo visibile (es. nel footer)."
  }
};

export function renderReportMarkdown({ report, sorgente }) {
  const issues = report.issues ?? [];
  const high = issues.filter((i) => i.severity === "high").length;
  const medium = issues.filter((i) => i.severity === "medium").length;

  const perRule = new Map();
  for (const i of issues) {
    const key = i.rule || "unknown";
    perRule.set(key, (perRule.get(key) || 0) + 1);
  }

  const lines = [];
  lines.push("# Report accessibilita (Conforme Digitale)");
  lines.push("");
  if (sorgente) {
    lines.push(`- Sorgente: \`${esc(sorgente)}\``);
  }
  lines.push(`- Data: \`${new Date().toISOString()}\``);
  lines.push("");
  lines.push("## Sintesi");
  lines.push("");
  lines.push(`- Punteggio: **${report.score}** / 100`);
  lines.push(`- Problemi: **${report.issueCount}** (Alta: **${high}**, Media: **${medium}**)`);
  lines.push("");
  lines.push("## Priorita e correzioni consigliate");
  lines.push("");

  const sortedRules = [...perRule.entries()].sort((a, b) => b[1] - a[1]);
  for (const [rule, count] of sortedRules) {
    const help = RULE_HELP[rule];
    if (!help) {
      lines.push(`- \`${rule}\` (${count})`);
      continue;
    }
    lines.push(`- \`${rule}\` (${count}): ${help.titolo}`);
    lines.push(`  Cosa significa: ${help.cosa}`);
    lines.push(`  Come correggere: ${help.fix}`);
  }

  lines.push("");
  lines.push("## Dettaglio problemi");
  lines.push("");
  for (const i of issues) {
    const line = i.line ? ` (riga ${i.line})` : "";
    lines.push(`- [${esc(i.severity)}] \`${esc(i.rule)}\`${line}: ${esc(i.message)}`);
  }

  lines.push("");
  return lines.join("\n");
}

