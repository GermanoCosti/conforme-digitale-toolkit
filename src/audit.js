function lineOf(text, index) {
  return text.slice(0, index).split(/\r?\n/).length;
}

function normalizeText(s) {
  return (s || "")
    .toLowerCase()
    .replace(/[àáâä]/g, "a")
    .replace(/[èéêë]/g, "e")
    .replace(/[ìíîï]/g, "i")
    .replace(/[òóôö]/g, "o")
    .replace(/[ùúûü]/g, "u")
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractFooterHtml(html) {
  const m = html.match(/<footer\b[^>]*>[\s\S]*?<\/footer>/i);
  return m ? m[0] : html;
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

  // Controlli "molto italiani": dichiarazione di accessibilita e canale feedback (AGID/PA e soggetti obbligati).
  // Regole volutamente semplici: cercano un link/indicazione, non sostituiscono una verifica legale.
  const footerHtml = extractFooterHtml(html);
  const footerNorm = normalizeText(footerHtml.replace(/<[^>]*>/g, " "));

  // 1) Link alla dichiarazione di accessibilita
  let hasDichiarazione = false;
  for (const match of footerHtml.matchAll(/<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)) {
    const href = match[1] || "";
    const text = normalizeText((match[2] || "").replace(/<[^>]*>/g, " "));
    const hrefNorm = normalizeText(href);
    const okText =
      (text.includes("dichiarazione") && (text.includes("accessibilita") || text.includes("accessibility"))) ||
      text.includes("accessibility statement");
    const okHref =
      (hrefNorm.includes("dichiarazione") && hrefNorm.includes("accessibil")) ||
      hrefNorm.includes("accessibility-statement") ||
      hrefNorm.includes("accessibilitystatement");
    if (okText || okHref) {
      hasDichiarazione = true;
      break;
    }
  }
  if (!hasDichiarazione) {
    issues.push({
      rule: "dichiarazione-accessibilita",
      severity: "medium",
      message:
        "Non trovato un link/testo riconoscibile alla Dichiarazione di accessibilita (es. nel footer).",
      line: 1
    });
  }

  // 2) Meccanismo di feedback per segnalazioni (email dedicata, form, pagina contatti accessibilita)
  let hasFeedback = false;
  const mailtoMatches = [...footerHtml.matchAll(/<a\b[^>]*href\s*=\s*["']mailto:([^"'>\s]+)[^"']*["'][^>]*>/gi)];
  for (const m of mailtoMatches) {
    const addr = normalizeText(m[1] || "");
    if (addr.includes("access") || addr.includes("disabil") || addr.includes("support") || addr.includes("urp")) {
      hasFeedback = true;
      break;
    }
  }
  if (!hasFeedback) {
    const hasFeedbackWords =
      footerNorm.includes("feedback accessibil") ||
      footerNorm.includes("segnala") ||
      footerNorm.includes("segnalazione") ||
      footerNorm.includes("problemi di accessibil") ||
      footerNorm.includes("contatta") && footerNorm.includes("accessibil");
    const hasFormLike = /<form\b[^>]*(id|class|action)\s*=\s*["'][^"']*(feedback|accessibil|segnal)[^"']*["'][^>]*>/i.test(
      footerHtml
    );
    if (hasFeedbackWords || hasFormLike) {
      hasFeedback = true;
    }
  }
  if (!hasFeedback) {
    issues.push({
      rule: "feedback-accessibilita",
      severity: "medium",
      message:
        "Non trovato un meccanismo di feedback per segnalazioni accessibilita (email dedicata o form/pagina).",
      line: 1
    });
  }

  return {
    score: Math.max(0, 100 - issues.length * 15),
    issueCount: issues.length,
    issues
  };
}
