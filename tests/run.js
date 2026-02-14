import assert from "node:assert/strict";
import { auditHtml } from "../src/audit.js";

function wrapHtml(innerBody) {
  return `
    <html lang="it">
      <body>
        ${innerBody}
        <footer>
          <a href="/accessibilita/dichiarazione">Dichiarazione di accessibilita</a>
          <a href="mailto:accessibilita@esempio.it">Segnala un problema di accessibilita</a>
        </footer>
      </body>
    </html>
  `;
}

function testImgAlt() {
  const html = wrapHtml(`<h1>Titolo</h1><img src="x.png">`);
  const report = auditHtml(html);
  assert.equal(report.issueCount, 1);
  assert.equal(report.issues[0].rule, "img-alt");
}

function testInputLabel() {
  const html = wrapHtml(`<h1>Titolo</h1><label for="email">Email</label><input id="email" type="email">`);
  const report = auditHtml(html);
  assert.equal(report.issueCount, 0);
}

function testButtonName() {
  const html = wrapHtml(`<h1>Titolo</h1><button><span></span></button>`);
  const report = auditHtml(html);
  assert.equal(report.issueCount, 1);
  assert.equal(report.issues[0].rule, "button-name");
}

function testMissingLangAndH1() {
  const html = `<html><body><p>ciao</p><footer>
    <a href="/accessibilita/dichiarazione">Dichiarazione di accessibilita</a>
    <a href="mailto:accessibilita@esempio.it">Segnala un problema di accessibilita</a>
  </footer></body></html>`;
  const report = auditHtml(html);
  const rules = report.issues.map((i) => i.rule);
  assert.equal(rules.includes("page-lang"), true);
  assert.equal(rules.includes("heading-h1"), true);
}

function testLinkName() {
  const html = wrapHtml(`<h1>Titolo</h1><a href="/x"><span></span></a>`);
  const report = auditHtml(html);
  const rules = report.issues.map((i) => i.rule);
  assert.equal(rules.includes("link-name"), true);
}

function testDichiarazioneEFeedbackOk() {
  const html = `
    <html lang="it">
      <body>
        <h1>Titolo</h1>
        <p>Contenuto</p>
        <footer>
          <a href="/accessibilita/dichiarazione">Dichiarazione di accessibilita</a>
          <a href="mailto:accessibilita@esempio.it">Segnala un problema di accessibilita</a>
        </footer>
      </body>
    </html>
  `;
  const report = auditHtml(html);
  const rules = report.issues.map((i) => i.rule);
  assert.equal(rules.includes("dichiarazione-accessibilita"), false);
  assert.equal(rules.includes("feedback-accessibilita"), false);
}

try {
  testImgAlt();
  testInputLabel();
  testButtonName();
  testMissingLangAndH1();
  testLinkName();
  testDichiarazioneEFeedbackOk();
  console.log("OK: 6/6 test passati");
} catch (err) {
  console.error("ERRORE TEST:", err.message);
  process.exit(1);
}
