import json
import pathlib
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
