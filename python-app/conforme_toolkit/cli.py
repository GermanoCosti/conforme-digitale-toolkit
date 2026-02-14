import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

try:
    from conforme_toolkit.audit import audit_html
except ModuleNotFoundError:
    from audit import audit_html


def _read_from_file(file_path: str) -> str:
    path = pathlib.Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {path}")
    return path.read_text(encoding="utf-8")


def _read_from_url(url: str) -> str:
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


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="conforme-audit",
        description="Audit accessibilita base su file HTML o URL.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Percorso file HTML locale")
    source.add_argument("--url", help="URL pagina web da analizzare")
    parser.add_argument("--out", help="Percorso file JSON output")
    args = parser.parse_args()

    try:
        html = _read_from_file(args.file) if args.file else _read_from_url(args.url)
        report = audit_html(html)
    except Exception as exc:  # noqa: BLE001
        print(f"Errore: {exc}", file=sys.stderr)
        return 1

    print("Audit completato.")
    print(f"Punteggio: {report['score']}")
    print(f"Problemi: {report['issueCount']}")
    high = sum(1 for i in report["issues"] if i["severity"] == "high")
    medium = sum(1 for i in report["issues"] if i["severity"] == "medium")
    print(f"Alta: {high} | Media: {medium}")

    if args.out:
        out_path = pathlib.Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report salvato in: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
