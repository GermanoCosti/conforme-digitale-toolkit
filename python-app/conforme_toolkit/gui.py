import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from conforme_toolkit.service import run_audit, write_report, write_report_md
except ModuleNotFoundError:
    from service import run_audit, write_report, write_report_md


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conforme Digitale - Audit Accessibilita")
        self.geometry("860x620")
        self.minsize(760, 520)

        self.source_type = tk.StringVar(value="file")
        self.source_value = tk.StringVar(value="")
        self.output_value = tk.StringVar(value=str(pathlib.Path("report-python.json").resolve()))
        self.output_md_value = tk.StringVar(value=str(pathlib.Path("report-python.md").resolve()))

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        source_frame = ttk.LabelFrame(frame, text="Sorgente")
        source_frame.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(
            source_frame, text="File HTML", value="file", variable=self.source_type, command=self._refresh_placeholder
        ).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ttk.Radiobutton(
            source_frame, text="URL", value="url", variable=self.source_type, command=self._refresh_placeholder
        ).grid(row=0, column=1, sticky="w", padx=8, pady=6)

        ttk.Entry(source_frame, textvariable=self.source_value).grid(row=1, column=0, columnspan=2, sticky="ew", padx=8)
        self.source_btn = ttk.Button(source_frame, text="Sfoglia file", command=self._choose_source)
        self.source_btn.grid(row=1, column=2, padx=8)
        source_frame.columnconfigure(0, weight=1)
        source_frame.columnconfigure(1, weight=1)

        out_frame = ttk.LabelFrame(frame, text="Output")
        out_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(out_frame, text="JSON").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 0))
        ttk.Entry(out_frame, textvariable=self.output_value).grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ttk.Button(out_frame, text="Scegli file", command=self._choose_output).grid(row=1, column=1, padx=8, pady=(0, 8))

        ttk.Label(out_frame, text="Markdown (opzionale)").grid(row=2, column=0, sticky="w", padx=8, pady=(8, 0))
        ttk.Entry(out_frame, textvariable=self.output_md_value).grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 8))
        ttk.Button(out_frame, text="Scegli file", command=self._choose_output_md).grid(row=3, column=1, padx=8, pady=(0, 8))
        out_frame.columnconfigure(0, weight=1)

        actions = ttk.Frame(frame)
        actions.pack(fill="x", pady=(0, 10))
        ttk.Button(actions, text="Analizza", command=self._run).pack(side="left")

        self.summary = ttk.Label(frame, text="Nessuna analisi eseguita.")
        self.summary.pack(anchor="w", pady=(0, 6))

        issue_box = ttk.LabelFrame(frame, text="Problemi rilevati")
        issue_box.pack(fill="both", expand=True)
        self.output_text = tk.Text(issue_box, wrap="word", height=22)
        self.output_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.output_text.configure(state="disabled")

        self._refresh_placeholder()

    def _refresh_placeholder(self):
        if self.source_type.get() == "file":
            self.source_btn.configure(state="normal", text="Sfoglia file")
            if not self.source_value.get():
                self.source_value.set(str(pathlib.Path("..", "examples", "sample.html").resolve()))
        else:
            self.source_btn.configure(state="disabled", text="Sfoglia disattivato")
            if self.source_value.get().endswith("sample.html"):
                self.source_value.set("https://example.com")

    def _choose_source(self):
        path = filedialog.askopenfilename(
            title="Seleziona file HTML", filetypes=[("File HTML", "*.html;*.htm"), ("Tutti i file", "*.*")]
        )
        if path:
            self.source_value.set(path)

    def _choose_output(self):
        path = filedialog.asksaveasfilename(
            title="Salva report JSON",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Tutti i file", "*.*")],
            initialfile="report-python.json",
        )
        if path:
            self.output_value.set(path)

    def _choose_output_md(self):
        path = filedialog.asksaveasfilename(
            title="Salva report Markdown",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Tutti i file", "*.*")],
            initialfile="report-python.md",
        )
        if path:
            self.output_md_value.set(path)

    def _set_output(self, text: str):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state="disabled")

    def _run(self):
        source_type = self.source_type.get()
        source_value = self.source_value.get().strip()
        out_path = self.output_value.get().strip()
        out_md_path = self.output_md_value.get().strip()

        if not source_value:
            messagebox.showerror("Errore", "Indica una sorgente valida.")
            return
        if not out_path:
            messagebox.showerror("Errore", "Indica il file di output.")
            return

        try:
            report = run_audit(source_type, source_value)
            saved = write_report(report, out_path)
            saved_md = None
            if out_md_path:
                saved_md = write_report_md(report, out_md_path, sorgente=f"{source_type}:{source_value}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Errore analisi", str(exc))
            return

        high = sum(1 for i in report["issues"] if i["severity"] == "high")
        medium = sum(1 for i in report["issues"] if i["severity"] == "medium")
        self.summary.configure(
            text=f"Punteggio: {report['score']} | Problemi: {report['issueCount']} | Alta: {high} | Media: {medium}"
        )

        lines = []
        if report["issues"]:
            for item in report["issues"]:
                lines.append(f"[{item['severity']}] {item['rule']} - riga {item['line']}: {item['message']}")
        else:
            lines.append("Nessun problema rilevato.")
        lines.append("")
        lines.append(f"Report salvato in: {saved}")
        if saved_md:
            lines.append(f"Report Markdown salvato in: {saved_md}")
        self._set_output("\n".join(lines))
        msg = f"Report salvato in:\n{saved}"
        if saved_md:
            msg += f"\n\nReport Markdown salvato in:\n{saved_md}"
        messagebox.showinfo("Analisi completata", msg)


def main() -> int:
    app = App()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
