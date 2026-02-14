import json
import pathlib
import datetime
import urllib.error
import urllib.request

try:
    from conforme_toolkit.audit import audit_html
except ModuleNotFoundError:
    from audit import audit_html


def read_from_file(file_path: str) -> str:
    path = pathlib.Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {path}")
    return path.read_text(encoding="utf-8")


def read_from_url(url: str) -> str:
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("URL non valido. Usa un indirizzo che inizi con http:// o https://")
    req = urllib.request.Request(url, headers={"User-Agent": "conforme-toolkit/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Download fallito: HTTP {resp.status}")
            data = resp.read()
            return data.decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Errore durante il download URL: {exc}") from exc


def run_audit(source_type: str, source_value: str) -> dict:
    html = read_from_file(source_value) if source_type == "file" else read_from_url(source_value)
    return audit_html(html)


def write_report(report: dict, out_path: str) -> pathlib.Path:
    path = pathlib.Path(out_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_report_md(report: dict, out_path: str, sorgente: str | None = None) -> pathlib.Path:
    issues = report.get("issues", [])
    high = sum(1 for i in issues if i.get("severity") == "high")
    medium = sum(1 for i in issues if i.get("severity") == "medium")

    per_rule: dict[str, int] = {}
    for i in issues:
        rule = i.get("rule") or "unknown"
        per_rule[rule] = per_rule.get(rule, 0) + 1

    rule_help = {
        "img-alt": (
            "Immagini senza testo alternativo (alt)",
            "Le immagini senza alt non vengono descritte agli screen reader.",
            'Aggiungi alt descrittivo (o alt="" se l\'immagine e\' puramente decorativa).',
        ),
        "input-label": (
            "Campi input senza etichetta",
            "Senza label/aria-label, chi usa tecnologie assistive non capisce cosa inserire.",
            'Collega un <label for="id"> oppure usa aria-label/aria-labelledby.',
        ),
        "button-name": (
            "Pulsanti senza nome accessibile",
            "Un button senza testo/aria-label risulta 'vuoto' per screen reader.",
            "Inserisci testo visibile o aria-label.",
        ),
        "link-name": (
            "Link senza nome accessibile",
            "Un link senza testo/aria-label risulta non comprensibile.",
            "Aggiungi testo leggibile o aria-label significativo.",
        ),
        "page-lang": (
            "Manca lang su <html>",
            "Senza lang, screen reader e traduttori possono usare la lingua sbagliata.",
            'Aggiungi lang="it" (o la lingua corretta) nel tag <html>.',
        ),
        "heading-h1": (
            "Manca un <h1> principale",
            "Senza un titolo principale, la pagina e' piu' difficile da navigare.",
            "Aggiungi un <h1> che descriva la pagina.",
        ),
        "dichiarazione-accessibilita": (
            "Link alla Dichiarazione di accessibilita non trovato",
            "In Italia spesso e' richiesto pubblicare e rendere facilmente raggiungibile la dichiarazione.",
            "Aggiungi nel footer un link chiaro tipo 'Dichiarazione di accessibilita' verso la pagina dedicata.",
        ),
        "feedback-accessibilita": (
            "Canale di feedback accessibilita non trovato",
            "Gli utenti devono poter segnalare problemi di accessibilita in modo semplice.",
            "Aggiungi un contatto dedicato (email/form) e rendilo visibile (es. nel footer).",
        ),
    }

    lines: list[str] = []
    lines.append("# Report accessibilita (Conforme Digitale)")
    lines.append("")
    if sorgente:
        lines.append(f"- Sorgente: `{sorgente}`")
    lines.append(f"- Data: `{datetime.datetime.utcnow().isoformat()}Z`")
    lines.append("")
    lines.append("## Sintesi")
    lines.append("")
    lines.append(f"- Punteggio: **{report.get('score')}** / 100")
    lines.append(f"- Problemi: **{report.get('issueCount')}** (Alta: **{high}**, Media: **{medium}**)")
    lines.append("")
    lines.append("## Priorita e correzioni consigliate")
    lines.append("")

    for rule, count in sorted(per_rule.items(), key=lambda kv: kv[1], reverse=True):
        if rule in rule_help:
            titolo, cosa, fix = rule_help[rule]
            lines.append(f"- `{rule}` ({count}): {titolo}")
            lines.append(f"  Cosa significa: {cosa}")
            lines.append(f"  Come correggere: {fix}")
        else:
            lines.append(f"- `{rule}` ({count})")

    lines.append("")
    lines.append("## Dettaglio problemi")
    lines.append("")
    for i in issues:
        sev = str(i.get("severity", "")).strip()
        rule = str(i.get("rule", "")).strip()
        msg = str(i.get("message", "")).replace("\n", " ").strip()
        ln = i.get("line")
        ln_txt = f" (riga {ln})" if ln else ""
        lines.append(f"- [{sev}] `{rule}`{ln_txt}: {msg}")

    path = pathlib.Path(out_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
