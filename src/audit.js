function lineOf(text, index) {
  return text.slice(0, index).split(/\r?\n/).length;
}

export function auditHtml(html) {
  const issues = [];

  const htmlTagMatch = html.match(/<html\b[^>]*>/i);
  if (htmlTagMatch) {
    const hasLang = /\blang\s*=\s*["'][^"']+["']/i.test(htmlTagMatch[0]);
    if (!hasLang) {
      issues.push({
        rule: "page-lang",
        severity: "medium",
        message: "Tag <html> senza attributo lang.",
        line: lineOf(html, htmlTagMatch.index ?? 0)
      });
    }
  }

  const h1Regex = /<h1\b[^>]*>[\s\S]*?<\/h1>/gi;
  const h1Count = [...html.matchAll(h1Regex)].length;
  if (h1Count === 0) {
    issues.push({
      rule: "heading-h1",
      severity: "medium",
      message: "Pagina senza heading principale <h1>.",
      line: 1
    });
  }

  const imgRegex = /<img\b[^>]*>/gi;
  for (const match of html.matchAll(imgRegex)) {
    const tag = match[0];
    const hasAlt = /\balt\s*=\s*["'][^"']*["']/i.test(tag);
    if (!hasAlt) {
      issues.push({
        rule: "img-alt",
        severity: "high",
        message: "Immagine senza attributo alt.",
        line: lineOf(html, match.index ?? 0)
      });
    }
  }

  const inputRegex = /<input\b[^>]*>/gi;
  for (const match of html.matchAll(inputRegex)) {
    const tag = match[0];
    const idMatch = tag.match(/\bid\s*=\s*["']([^"']+)["']/i);
    const hasAriaLabel = /\baria-label\s*=\s*["'][^"']+["']/i.test(tag);
    let hasLabel = false;

    if (idMatch?.[1]) {
      const id = idMatch[1].replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const labelRegex = new RegExp(`<label\\b[^>]*for\\s*=\\s*["']${id}["'][^>]*>`, "i");
      hasLabel = labelRegex.test(html);
    }

    if (!hasLabel && !hasAriaLabel) {
      issues.push({
        rule: "input-label",
        severity: "high",
        message: "Input senza label associata o aria-label.",
        line: lineOf(html, match.index ?? 0)
      });
    }
  }

  const buttonRegex = /<button\b[^>]*>([\s\S]*?)<\/button>/gi;
  for (const match of html.matchAll(buttonRegex)) {
    const tag = match[0];
    const innerText = (match[1] || "").replace(/<[^>]*>/g, "").trim();
    const hasAriaLabel = /\baria-label\s*=\s*["'][^"']+["']/i.test(tag);
    if (!innerText && !hasAriaLabel) {
      issues.push({
        rule: "button-name",
        severity: "medium",
        message: "Button senza testo leggibile o aria-label.",
        line: lineOf(html, match.index ?? 0)
      });
    }
  }

  const anchorRegex = /<a\b[^>]*>([\s\S]*?)<\/a>/gi;
  for (const match of html.matchAll(anchorRegex)) {
    const tag = match[0];
    const innerText = (match[1] || "").replace(/<[^>]*>/g, "").trim();
    const hasAriaLabel = /\baria-label\s*=\s*["'][^"']+["']/i.test(tag);
    if (!innerText && !hasAriaLabel) {
      issues.push({
        rule: "link-name",
        severity: "medium",
        message: "Link senza testo leggibile o aria-label.",
        line: lineOf(html, match.index ?? 0)
      });
    }
  }

  return {
    score: Math.max(0, 100 - issues.length * 15),
    issueCount: issues.length,
    issues
  };
}
