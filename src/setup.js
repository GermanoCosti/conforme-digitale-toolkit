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
    output: "./report/report.json"
  };
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), "utf8");
  console.log(`Creato file configurazione: ${configPath}`);
} else {
  console.log(`Configurazione gia presente: ${configPath}`);
}

console.log("Setup completato.");
