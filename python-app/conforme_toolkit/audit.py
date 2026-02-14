import re


def _line_of(text: str, index: int) -> int:
    return text[:index].count("\n") + 1


def _norm(s: str) -> str:
    s = (s or "").lower()
    s = (
        s.replace("à", "a")
        .replace("á", "a")
        .replace("â", "a")
        .replace("ä", "a")
        .replace("è", "e")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("ë", "e")
        .replace("ì", "i")
        .replace("í", "i")
        .replace("î", "i")
        .replace("ï", "i")
        .replace("ò", "o")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("ö", "o")
        .replace("ù", "u")
        .replace("ú", "u")
        .replace("û", "u")
        .replace("ü", "u")
    )
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _footer_or_all(html: str) -> str:
    m = re.search(r"<footer\b[^>]*>[\s\S]*?</footer>", html, flags=re.IGNORECASE)
    return m.group(0) if m else html


def audit_html(html: str) -> dict:
    issues = []

    html_tag_match = re.search(r"<html\b[^>]*>", html, flags=re.IGNORECASE)
    if html_tag_match:
        has_lang = re.search(r'\blang\s*=\s*["\'][^"\']+["\']', html_tag_match.group(0), flags=re.IGNORECASE)
        if not has_lang:
            issues.append(
                {
                    "rule": "page-lang",
                    "severity": "medium",
                    "message": "Tag <html> senza attributo lang.",
                    "line": _line_of(html, html_tag_match.start()),
                }
            )

    h1_count = len(re.findall(r"<h1\b[^>]*>[\s\S]*?</h1>", html, flags=re.IGNORECASE))
    if h1_count == 0:
        issues.append(
            {
                "rule": "heading-h1",
                "severity": "medium",
                "message": "Pagina senza heading principale <h1>.",
                "line": 1,
            }
        )

    for match in re.finditer(r"<img\b[^>]*>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        has_alt = re.search(r'\balt\s*=\s*["\'][^"\']*["\']', tag, flags=re.IGNORECASE)
        if not has_alt:
            issues.append(
                {
                    "rule": "img-alt",
                    "severity": "high",
                    "message": "Immagine senza attributo alt.",
                    "line": _line_of(html, match.start()),
                }
            )

    for match in re.finditer(r"<input\b[^>]*>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        id_match = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', tag, flags=re.IGNORECASE)
        has_aria_label = re.search(r'\baria-label\s*=\s*["\'][^"\']+["\']', tag, flags=re.IGNORECASE)
        has_label = False

        if id_match:
            field_id = re.escape(id_match.group(1))
            label_regex = rf"<label\b[^>]*for\s*=\s*['\"]{field_id}['\"][^>]*>"
            has_label = re.search(label_regex, html, flags=re.IGNORECASE) is not None

        if not has_label and not has_aria_label:
            issues.append(
                {
                    "rule": "input-label",
                    "severity": "high",
                    "message": "Input senza label associata o aria-label.",
                    "line": _line_of(html, match.start()),
                }
            )

    for match in re.finditer(r"<button\b[^>]*>([\s\S]*?)</button>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        inner_text = re.sub(r"<[^>]*>", "", match.group(1)).strip()
        has_aria_label = re.search(r'\baria-label\s*=\s*["\'][^"\']+["\']', tag, flags=re.IGNORECASE)
        if not inner_text and not has_aria_label:
            issues.append(
                {
                    "rule": "button-name",
                    "severity": "medium",
                    "message": "Button senza testo leggibile o aria-label.",
                    "line": _line_of(html, match.start()),
                }
            )

    for match in re.finditer(r"<a\b[^>]*>([\s\S]*?)</a>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        inner_text = re.sub(r"<[^>]*>", "", match.group(1)).strip()
        has_aria_label = re.search(r'\baria-label\s*=\s*["\'][^"\']+["\']', tag, flags=re.IGNORECASE)
        if not inner_text and not has_aria_label:
            issues.append(
                {
                    "rule": "link-name",
                    "severity": "medium",
                    "message": "Link senza testo leggibile o aria-label.",
                    "line": _line_of(html, match.start()),
                }
            )

    footer_html = _footer_or_all(html)
    footer_text = _norm(re.sub(r"<[^>]*>", " ", footer_html))

    # Dichiarazione di accessibilita (controllo indicativo)
    has_dichiarazione = False
    for m in re.finditer(r"<a\b[^>]*href\s*=\s*['\"]([^'\"]+)['\"][^>]*>([\s\S]*?)</a>", footer_html, re.IGNORECASE):
        href = m.group(1) or ""
        text = _norm(re.sub(r"<[^>]*>", " ", m.group(2) or ""))
        href_n = _norm(href)
        ok_text = ("dichiarazione" in text and ("accessibilita" in text or "accessibility" in text)) or (
            "accessibility statement" in text
        )
        ok_href = ("dichiarazione" in href_n and "accessibil" in href_n) or ("accessibility-statement" in href.lower())
        if ok_text or ok_href:
            has_dichiarazione = True
            break

    if not has_dichiarazione:
        issues.append(
            {
                "rule": "dichiarazione-accessibilita",
                "severity": "medium",
                "message": "Non trovato un link/testo riconoscibile alla Dichiarazione di accessibilita (es. nel footer).",
                "line": 1,
            }
        )

    # Feedback accessibilita (controllo indicativo)
    has_feedback = False
    for m in re.finditer(r"<a\b[^>]*href\s*=\s*['\"]mailto:([^'\">\\s]+)[^'\"]*['\"][^>]*>", footer_html, re.IGNORECASE):
        addr = _norm(m.group(1) or "")
        if "access" in addr or "disabil" in addr or "support" in addr or "urp" in addr:
            has_feedback = True
            break

    if not has_feedback:
        has_words = (
            "feedback accessibil" in footer_text
            or "segnala" in footer_text
            or "segnalazione" in footer_text
            or "problemi di accessibil" in footer_text
            or ("contatta" in footer_text and "accessibil" in footer_text)
        )
        has_form_like = re.search(
            r"<form\b[^>]*(id|class|action)\s*=\s*['\"][^'\"]*(feedback|accessibil|segnal)[^'\"]*['\"][^>]*>",
            footer_html,
            flags=re.IGNORECASE,
        )
        if has_words or has_form_like:
            has_feedback = True

    if not has_feedback:
        issues.append(
            {
                "rule": "feedback-accessibilita",
                "severity": "medium",
                "message": "Non trovato un meccanismo di feedback per segnalazioni accessibilita (email dedicata o form/pagina).",
                "line": 1,
            }
        )

    return {
        "score": max(0, 100 - len(issues) * 15),
        "issueCount": len(issues),
        "issues": issues,
    }
