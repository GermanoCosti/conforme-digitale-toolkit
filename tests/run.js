import assert from "node:assert/strict";
import { auditHtml } from "../src/audit.js";

function testImgAlt() {
  const html = `<html lang="it"><body><h1>Titolo</h1><img src="x.png"></body></html>`;
  const report = auditHtml(html);
  assert.equal(report.issueCount, 1);
  assert.equal(report.issues[0].rule, "img-alt");
}

function testInputLabel() {
  const html = `<html lang="it"><body><h1>Titolo</h1><label for="email">Email</label><input id="email" type="email"></body></html>`;
  const report = auditHtml(html);
  assert.equal(report.issueCount, 0);
}

function testButtonName() {
  const html = `<html lang="it"><body><h1>Titolo</h1><button><span></span></button></body></html>`;
  const report = auditHtml(html);
  assert.equal(report.issueCount, 1);
  assert.equal(report.issues[0].rule, "button-name");
}

function testMissingLangAndH1() {
  const html = `<html><body><p>ciao</p></body></html>`;
  const report = auditHtml(html);
  const rules = report.issues.map((i) => i.rule);
  assert.equal(rules.includes("page-lang"), true);
  assert.equal(rules.includes("heading-h1"), true);
}

function testLinkName() {
  const html = `<html lang="it"><body><h1>Titolo</h1><a href="/x"><span></span></a></body></html>`;
  const report = auditHtml(html);
  assert.equal(report.issueCount, 1);
  assert.equal(report.issues[0].rule, "link-name");
}

try {
  testImgAlt();
  testInputLabel();
  testButtonName();
  testMissingLangAndH1();
  testLinkName();
  console.log("OK: 5/5 test passati");
} catch (err) {
  console.error("ERRORE TEST:", err.message);
  process.exit(1);
}
