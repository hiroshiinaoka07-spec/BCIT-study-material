"""Build Windows_Server_Admin_Final_Cheat_Sheet.docx (python-docx).

Usage:  .\\.venv\\Scripts\\python tools\\build_wsa_cheatsheet.py
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent / "wsa_cheatsheet"))

from lib import Sheet  # noqa: E402

OUT = ROOT / "Windows_Server_Admin_Final_Cheat_Sheet.docx"

SECTIONS = [
    ("part01_platform", ["front_matter", "part1", "part2"]),
    ("part03_adds", ["part3"]),
    ("part04_files", ["part4"]),
    ("part05_storage", ["part5", "part6"]),
    ("part07_gpo", ["part7"]),
    ("part08_dhcp_dns", ["part8", "part9"]),
    ("part10_hyperv", ["part10", "part11"]),
    ("part12_extra", ["part12", "appendices"]),
]


def main(only=None):
    s = Sheet()
    for module_name, funcs in SECTIONS:
        if only and module_name not in only:
            continue
        mod = importlib.import_module(module_name)
        for fn in funcs:
            getattr(mod, fn)(s)
    s.enable_update_fields_on_open()
    s.save(OUT)
    d = s.doc
    print(f"Saved {OUT}")
    print(f"Paragraphs: {len(d.paragraphs)}  Tables: {len(d.tables)}  "
          f"Headings: {sum(1 for p in d.paragraphs if p.style.name.startswith('Heading'))}")


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
