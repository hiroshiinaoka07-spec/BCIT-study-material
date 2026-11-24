"""Formatting helpers for the Windows Server Admin cheat sheet (python-docx)."""
import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BODY_FONT = "Calibri"
MONO_FONT = "Consolas"
BODY_PT = 9.5

NAVY = "1F3864"
BLUE = "1F4E79"
TEAL = "0E6E6E"
GRAY_TEXT = "595959"

SUPP_TAG = "[Instructor Material Not Yet Released — Supplemental Reference]"
EXTRA_TAG = "[Supplemental Reference]"
MODEL_TAG = "[Model Answer]"

BOX_STYLES = {
    "trap": ("EXAM TRAP", "FDECEA", "C0392B"),
    "instructor": ("INSTRUCTOR CALLOUT", "E8F1FB", "1F4E79"),
    "trouble": ("TROUBLESHOOTING", "FFF4E0", "C77700"),
    "key": ("KEY TAKEAWAY", "E9F6EC", "2E7D32"),
    "memory": ("MEMORY AID", "F3ECFA", "6A3D9A"),
    "note": ("NOTE", "F2F2F2", "595959"),
}

_INLINE = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*\s](?:[^*]*[^*\s])?\*)")


def _hex(color):
    return RGBColor.from_string(color)


def _set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def _set_cell_borders(cell, **edges):
    """edges: top/left/bottom/right = (size_eighths, color) or None for nil."""
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        spec = edges.get(edge)
        if spec is None:
            el.set(qn("w:val"), "nil")
        else:
            size, color = spec
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(size))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), color)
        borders.append(el)
    tc_pr.append(borders)


def _set_cell_margins(table, top=40, bottom=40, left=80, right=80):
    tbl_pr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for name, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{name}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tbl_pr.append(mar)


def _para_shading(paragraph, fill):
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    p_pr.append(shd)


def _para_border(paragraph, color="A6A6A6", sides=("top", "left", "bottom", "right"), size=4, space=2):
    p_pr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    for side in sides:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), str(space))
        el.set(qn("w:color"), color)
        pbdr.append(el)
    p_pr.append(pbdr)


def _run_shading(run, fill="E7E6E6"):
    r_pr = run._r.get_or_add_rPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    r_pr.append(shd)


def _mono(run, size=None):
    run.font.name = MONO_FONT
    r_pr = run._r.get_or_add_rPr()
    fonts = r_pr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        r_pr.append(fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), MONO_FONT)
    if size:
        run.font.size = Pt(size)


def add_inline(paragraph, text, size=None, color=None, bold=False, italic=False):
    """Add text with `code` and **bold** markup to a paragraph."""
    for part in _INLINE.split(text):
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            _mono(run, (size or BODY_PT) - 0.5)
            _run_shading(run)
            run.font.color.rgb = _hex("1A1A1A")
            run.bold = bold
        elif part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
            run.italic = italic
            if size:
                run.font.size = Pt(size)
            if color:
                run.font.color.rgb = _hex(color)
        elif len(part) > 2 and part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
            run.bold = bold
            if size:
                run.font.size = Pt(size)
            if color:
                run.font.color.rgb = _hex(color)
        else:
            run = paragraph.add_run(part)
            run.bold = bold
            run.italic = italic
            if size:
                run.font.size = Pt(size)
            if color:
                run.font.color.rgb = _hex(color)
    return paragraph


def _add_field(paragraph, instr, size=None):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    run._r.append(begin)
    run2 = paragraph.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    run2._r.append(it)
    run3 = paragraph.add_run()
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    run3._r.append(sep)
    run4 = paragraph.add_run("1" if "PAGE" in instr else "Right-click and choose Update Field to build the table of contents.")
    run5 = paragraph.add_run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run5._r.append(end)
    if size:
        for r in (run, run2, run3, run4, run5):
            r.font.size = Pt(size)


class Sheet:
    """Thin wrapper around a python-docx Document with cheat-sheet building blocks."""

    def __init__(self):
        self.doc = Document()
        self._setup_page()
        self._setup_styles()
        self._setup_footer()

    # ---------- setup ----------
    def _setup_page(self):
        sec = self.doc.sections[0]
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(sec, side, Inches(0.5))
        sec.footer_distance = Inches(0.3)
        sec.header_distance = Inches(0.3)

    def _setup_styles(self):
        st = self.doc.styles
        normal = st["Normal"]
        normal.font.name = BODY_FONT
        normal.font.size = Pt(BODY_PT)
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
        pf = normal.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.0

        specs = {
            "Heading 1": (15, NAVY, True, 10, 4),
            "Heading 2": (12, BLUE, True, 8, 3),
            "Heading 3": (10.5, TEAL, True, 6, 2),
            "Heading 4": (9.5, "7F4F24", True, 4, 1),
        }
        for name, (size, color, bold, before, after) in specs.items():
            s = st[name]
            s.font.name = BODY_FONT
            rfonts = s.element.rPr.find(qn("w:rFonts"))
            if rfonts is not None:
                for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                    if rfonts.get(qn(attr)) is not None:
                        del rfonts.attrib[qn(attr)]
                for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
                    rfonts.set(qn(attr), BODY_FONT)
            s.font.size = Pt(size)
            s.font.bold = bold
            s.font.italic = False
            s.font.color.rgb = _hex(color)
            s.paragraph_format.space_before = Pt(before)
            s.paragraph_format.space_after = Pt(after)
            s.paragraph_format.keep_with_next = True

        for lst in ("List Bullet", "List Bullet 2", "List Bullet 3"):
            s = st[lst]
            s.font.name = BODY_FONT
            s.font.size = Pt(BODY_PT)
            s.paragraph_format.space_after = Pt(1)
            s.paragraph_format.line_spacing = 1.0

    def _setup_footer(self):
        sec = self.doc.sections[0]
        p = sec.footer.paragraphs[0]
        p.alignment = 1
        r = p.add_run("ACIT 3420 Windows Server Administration — Final Exam Cheat Sheet    |    Page ")
        r.font.size = Pt(8)
        r.font.color.rgb = _hex(GRAY_TEXT)
        _add_field(p, "PAGE", size=8)
        r = p.add_run(" of ")
        r.font.size = Pt(8)
        r.font.color.rgb = _hex(GRAY_TEXT)
        _add_field(p, "NUMPAGES", size=8)

    def enable_update_fields_on_open(self):
        settings = self.doc.settings.element
        el = OxmlElement("w:updateFields")
        el.set(qn("w:val"), "true")
        settings.append(el)

    # ---------- headings ----------
    def part(self, text, page_break=True):
        if page_break and len(self.doc.paragraphs) > 3:
            self.page_break()
        h = self.doc.add_heading(level=1)
        r = h.add_run(text)
        r.font.color.rgb = _hex("FFFFFF")
        _para_shading(h, NAVY)
        return h

    def h2(self, text):
        h = self.doc.add_heading(level=2)
        h.add_run(text)
        _para_border(h, color=BLUE, sides=("bottom",), size=8, space=1)
        return h

    def h3(self, text):
        h = self.doc.add_heading(level=3)
        add_inline(h, text)
        return h

    def h4(self, text):
        h = self.doc.add_heading(level=4)
        add_inline(h, text)
        return h

    def page_break(self):
        p = self.doc.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)
        p.paragraph_format.space_after = Pt(0)

    # ---------- text ----------
    def p(self, text, size=None, italic=False, color=None, bold=False, after=None):
        para = self.doc.add_paragraph()
        add_inline(para, text, size=size, color=color, italic=italic, bold=bold)
        if after is not None:
            para.paragraph_format.space_after = Pt(after)
        return para

    def src(self, text):
        """Small gray line naming the course files a section was built from."""
        para = self.doc.add_paragraph()
        r = para.add_run("Sources: " + text)
        r.italic = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = _hex("7F7F7F")
        para.paragraph_format.space_after = Pt(2)
        return para

    def tag(self, kind="supp", note=None):
        label = {"supp": SUPP_TAG, "extra": EXTRA_TAG, "model": MODEL_TAG}[kind]
        color = {"supp": "B03A2E", "extra": "8E5B00", "model": "5B3C88"}[kind]
        fill = {"supp": "FBE5E1", "extra": "FFF2CC", "model": "EDE4F7"}[kind]
        para = self.doc.add_paragraph()
        r = para.add_run(label)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = _hex(color)
        _run_shading(r, fill)
        if note:
            r2 = para.add_run("  " + note)
            r2.italic = True
            r2.font.size = Pt(7.5)
            r2.font.color.rgb = _hex(color)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.keep_with_next = True
        return para

    def bullets(self, items, level=1):
        """items: strings, or (string, [sub-items]) tuples for nesting."""
        style = {1: "List Bullet", 2: "List Bullet 2", 3: "List Bullet 3"}[level]
        for it in items:
            if isinstance(it, tuple):
                text, subs = it
                para = self.doc.add_paragraph(style=style)
                add_inline(para, text)
                self.bullets(subs, level=min(level + 1, 3))
            else:
                para = self.doc.add_paragraph(style=style)
                add_inline(para, it)

    def steps(self, items, start=1):
        for i, it in enumerate(items, start):
            para = self.doc.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.28)
            para.paragraph_format.first_line_indent = Inches(-0.2)
            para.paragraph_format.space_after = Pt(1)
            r = para.add_run(f"{i}. ")
            r.bold = True
            r.font.color.rgb = _hex(TEAL)
            add_inline(para, it)

    def code(self, text, title=None):
        if title:
            t = self.doc.add_paragraph()
            r = t.add_run(title)
            r.bold = True
            r.font.size = Pt(8)
            r.font.color.rgb = _hex(GRAY_TEXT)
            t.paragraph_format.space_after = Pt(0)
            t.paragraph_format.keep_with_next = True
        lines = text.strip("\n").split("\n")
        for i, line in enumerate(lines):
            para = self.doc.add_paragraph()
            run = para.add_run(line if line else " ")
            _mono(run, 8.5)
            run.font.color.rgb = _hex("1A1A1A")
            _para_shading(para, "F2F2F2")
            _para_border(para, color="BFBFBF", size=4, space=3)
            pf = para.paragraph_format
            pf.space_after = Pt(0) if i < len(lines) - 1 else Pt(4)
            pf.left_indent = Inches(0.06)
            pf.right_indent = Inches(0.06)
            pf.keep_with_next = i < len(lines) - 1 and len(lines) < 14
        return self

    # ---------- tables ----------
    def table(self, headers, rows, widths=None, size=8.5, header_fill=NAVY, zebra="F3F6FA", first_col_bold=True):
        t = self.doc.add_table(rows=1, cols=len(headers))
        t.style = self.doc.styles["Table Grid"]
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        _set_cell_margins(t)
        hdr = t.rows[0]
        tr_pr = hdr._tr.get_or_add_trPr()
        rep = OxmlElement("w:tblHeader")
        rep.set(qn("w:val"), "true")
        tr_pr.append(rep)
        for i, h in enumerate(headers):
            cell = hdr.cells[i]
            cell.text = ""
            para = cell.paragraphs[0]
            add_inline(para, h, size=size, color="FFFFFF", bold=True)
            para.paragraph_format.space_after = Pt(0)
            _set_cell_shading(cell, header_fill)
        for ri, row in enumerate(rows):
            cells = t.add_row().cells
            for ci, val in enumerate(row):
                cell = cells[ci]
                cell.text = ""
                chunks = str(val).split("\n")
                for k, chunk in enumerate(chunks):
                    para = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
                    add_inline(para, chunk, size=size, bold=(first_col_bold and ci == 0))
                    para.paragraph_format.space_after = Pt(0)
                if zebra and ri % 2 == 1:
                    _set_cell_shading(cell, zebra)
        for row in t.rows:
            cant = OxmlElement("w:cantSplit")
            cant.set(qn("w:val"), "true")
            row._tr.get_or_add_trPr().append(cant)
        if widths:
            for row in t.rows:
                for i, w in enumerate(widths):
                    row.cells[i].width = Inches(w)
        self._gap()
        return t

    def qa(self, pairs, title="Lab Questions & Answers", widths=(2.9, 4.6)):
        """Question/answer table with purple header."""
        if title:
            self.h4(title)
        return self.table(["Question", "Answer"], pairs, widths=widths, header_fill="5B3C88", zebra="F6F1FB",
                          first_col_bold=True)

    def box(self, kind, lines, title=None):
        label, fill, edge = BOX_STYLES[kind]
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        _set_cell_margins(t, top=50, bottom=50, left=110, right=90)
        cell = t.rows[0].cells[0]
        cell.width = Inches(7.5)
        _set_cell_shading(cell, fill)
        _set_cell_borders(cell, top=(4, edge), bottom=(4, edge), right=(4, edge), left=(24, edge))
        para = cell.paragraphs[0]
        r = para.add_run(label + (f" — {title}" if title else ""))
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = _hex(edge)
        para.paragraph_format.space_after = Pt(1)
        if isinstance(lines, str):
            lines = [lines]
        for line in lines:
            para = cell.add_paragraph()
            para.paragraph_format.space_after = Pt(1)
            if line.startswith("- "):
                para.paragraph_format.left_indent = Inches(0.15)
                para.paragraph_format.first_line_indent = Inches(-0.1)
                rr = para.add_run("• ")
                rr.font.color.rgb = _hex(edge)
                add_inline(para, line[2:], size=9)
            else:
                add_inline(para, line, size=9)
        self._gap()
        return t

    def _gap(self, pts=3):
        para = self.doc.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        fmt = para.paragraph_format
        fmt.line_spacing = Pt(pts)
        return para

    def toc(self):
        para = self.doc.add_paragraph()
        _add_field(para, 'TOC \\o "1-2" \\h \\z \\u', size=9)

    def save(self, path):
        self.doc.save(path)
