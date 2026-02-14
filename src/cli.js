#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { auditHtml } from "./audit.js";

function getArg(name) {
  const index = process.argv.findIndex((a) => a === name);
  if (index === -1) {
    return null;
  }
  return process.argv[index + 1] ?? null;
}

const file = getArg("--file");
const url = getArg("--url");
const out = getArg("--out");
const help = process.argv.includes("--help") || process.argv.includes("-h");

if (help) {
  console.log("Utilizzo: node src/cli.js --file ./pagina.html [--out ./report.json]");
  console.log("      oppure: node src/cli.js --url https://esempio.it [--out ./report.json]");
  process.exit(0);
}

if (!file && !url) {
  console.error("Errore: devi indicare --file oppure --url.");
  process.exit(1);
}

if (file && url) {
  console.error("Errore: usa solo una sorgente per volta (--file oppure --url).");
  process.exit(1);
}

let html = "";

if (file) {
  const inputPath = path.resolve(process.cwd(), file);
  if (!fs.existsSync(inputPath)) {
    console.error(`File non trovato: ${inputPath}`);
    process.exit(1);
  }
  html = fs.readFileSync(inputPath, "utf8");
}

if (url) {
  if (!/^https?:\/\//i.test(url)) {
    console.error("URL non valido. Usa un indirizzo che inizi con http:// o https://");
    process.exit(1);
  }
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timer);
    if (!response.ok) {
      console.error(`Download fallito: HTTP ${response.status}`);
      process.exit(1);
    }
    html = await response.text();
  } catch (error) {
    console.error(`Errore durante il download URL: ${error.message}`);
    process.exit(1);
  }
}

const report = auditHtml(html);

console.log("Audit completato.");
console.log(`Punteggio: ${report.score}`);
console.log(`Problemi: ${report.issueCount}`);
const highCount = report.issues.filter((i) => i.severity === "high").length;
const mediumCount = report.issues.filter((i) => i.severity === "medium").length;
console.log(`Alta: ${highCount} | Media: ${mediumCount}`);

if (out) {
  const outPath = path.resolve(process.cwd(), out);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2), "utf8");
  console.log(`Report salvato in: ${outPath}`);
}
