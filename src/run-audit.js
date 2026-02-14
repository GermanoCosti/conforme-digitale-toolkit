#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const cwd = process.cwd();
const configPath = path.join(cwd, "conforme.config.json");

if (!fs.existsSync(configPath)) {
  console.error("Configurazione non trovata. Esegui prima: npm run setup");
  process.exit(1);
}

const raw = fs.readFileSync(configPath, "utf8");
let config;
try {
  config = JSON.parse(raw);
} catch {
  console.error("File conforme.config.json non valido (JSON).");
  process.exit(1);
}

const sourceType = config?.sorgente?.tipo;
const sourceValue = config?.sorgente?.valore;
const out = config?.output || "./report/report.json";
const outMd = config?.outputMarkdown || null;

if (!sourceType || !sourceValue) {
  console.error("Configurazione incompleta: servono sorgente.tipo e sorgente.valore.");
  process.exit(1);
}

const cliPath = path.join(cwd, "src", "cli.js");
const args = [cliPath];

if (sourceType === "file") {
  args.push("--file", sourceValue);
} else if (sourceType === "url") {
  args.push("--url", sourceValue);
} else {
  console.error("sorgente.tipo deve essere 'file' oppure 'url'.");
  process.exit(1);
}

args.push("--out", out);
if (outMd) {
  args.push("--out-md", outMd);
}

const outDir = path.dirname(path.resolve(cwd, out));
fs.mkdirSync(outDir, { recursive: true });

const result = spawnSync(process.execPath, args, { stdio: "inherit" });
process.exit(result.status ?? 1);
