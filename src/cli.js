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
const out = getArg("--out");
const help = process.argv.includes("--help") || process.argv.includes("-h");

if (help) {
  console.log("Uso: node src/cli.js --file ./pagina.html [--out ./report.json]");
  process.exit(0);
}

if (!file) {
  console.error("Uso: node src/cli.js --file ./pagina.html [--out ./report.json]");
  process.exit(1);
}

const inputPath = path.resolve(process.cwd(), file);
if (!fs.existsSync(inputPath)) {
  console.error(`File non trovato: ${inputPath}`);
  process.exit(1);
}

const html = fs.readFileSync(inputPath, "utf8");
const report = auditHtml(html);

console.log("Audit completato.");
console.log(`Score: ${report.score}`);
console.log(`Issue: ${report.issueCount}`);
const highCount = report.issues.filter((i) => i.severity === "high").length;
const mediumCount = report.issues.filter((i) => i.severity === "medium").length;
console.log(`High: ${highCount} | Medium: ${mediumCount}`);

if (out) {
  const outPath = path.resolve(process.cwd(), out);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2), "utf8");
  console.log(`Report salvato in: ${outPath}`);
}
