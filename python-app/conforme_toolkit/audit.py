import re


def _line_of(text: str, index: int) -> int:
    return text[:index].count("\n") + 1


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

    return {
        "score": max(0, 100 - len(issues) * 15),
        "issueCount": len(issues),
        "issues": issues,
    }
