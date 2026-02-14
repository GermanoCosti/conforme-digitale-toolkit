#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const cwd = process.cwd();
const reportDir = path.join(cwd, "report");
const configPath = path.join(cwd, "conforme.config.json");

if (!fs.existsSync(reportDir)) {
  fs.mkdirSync(reportDir, { recursive: true });
  console.log(`Creata cartella: ${reportDir}`);
} else {
  console.log(`Cartella report gia presente: ${reportDir}`);
}

if (!fs.existsSync(configPath)) {
  const config = {
    sorgente: {
      tipo: "file",
      valore: "./examples/sample.html"
    },
    output: "./report/report.json",
    outputMarkdown: "./report/report.md"
  };
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), "utf8");
  console.log(`Creato file configurazione: ${configPath}`);
} else {
  // Se esiste gia, non sovrascrivere. Aggiungi solo chiavi mancanti.
  try {
    const raw = fs.readFileSync(configPath, "utf8");
    const cfg = JSON.parse(raw);
    if (!cfg.outputMarkdown) {
      cfg.outputMarkdown = "./report/report.md";
      fs.writeFileSync(configPath, JSON.stringify(cfg, null, 2), "utf8");
      console.log(`Aggiornata configurazione (aggiunto outputMarkdown): ${configPath}`);
    } else {
      console.log(`Configurazione gia presente: ${configPath}`);
    }
  } catch {
    console.log(`Configurazione gia presente: ${configPath}`);
  }
}

console.log("Setup completato.");
