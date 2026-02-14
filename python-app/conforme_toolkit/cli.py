import argparse
import sys

try:
    from conforme_toolkit.service import run_audit, write_report
except ModuleNotFoundError:
    from service import run_audit, write_report


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="conforme-digitale",
        description="Audit accessibilita base su file HTML o URL.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Percorso file HTML locale")
    source.add_argument("--url", help="URL pagina web da analizzare")
    parser.add_argument("--out", help="Percorso file JSON output")
    args = parser.parse_args()

    try:
        report = run_audit("file" if args.file else "url", args.file or args.url)
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
        out_path = write_report(report, args.out)
        print(f"Report salvato in: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
