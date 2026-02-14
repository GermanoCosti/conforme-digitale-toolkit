import unittest
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conforme_toolkit.audit import audit_html


class AuditTests(unittest.TestCase):
    def test_img_senza_alt(self):
        html = '<html lang="it"><body><h1>Titolo</h1><img src="x.png"></body></html>'
        report = audit_html(html)
        self.assertEqual(report["issueCount"], 1)
        self.assertEqual(report["issues"][0]["rule"], "img-alt")

    def test_input_con_label(self):
        html = '<html lang="it"><body><h1>Titolo</h1><label for="e">Email</label><input id="e"></body></html>'
        report = audit_html(html)
        self.assertEqual(report["issueCount"], 0)

    def test_link_senza_nome(self):
        html = '<html lang="it"><body><h1>Titolo</h1><a href="/x"><span></span></a></body></html>'
        report = audit_html(html)
        self.assertEqual(report["issueCount"], 1)
        self.assertEqual(report["issues"][0]["rule"], "link-name")


if __name__ == "__main__":
    unittest.main()
