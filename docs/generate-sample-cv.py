#!/usr/bin/env python3
"""Generate a one-page sample backend CV PDF with extractable text (no deps)."""

from pathlib import Path

OUT = Path(__file__).resolve().parent / "sample-cv-backend.pdf"

# Page: A4 595.28 x 841.89 pt; content uses Helvetica (built-in PDF font).
W, H = 595.28, 841.89
MARGIN_L, MARGIN_R = 48, 48
CONTENT_W = W - MARGIN_L - MARGIN_R


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def lines_for(text: str, max_chars: int) -> list[str]:
    words = text.split()
    rows, cur = [], []
    for w in words:
        trial = (" ".join(cur + [w])).strip()
        if len(trial) <= max_chars:
            cur.append(w)
        else:
            if cur:
                rows.append(" ".join(cur))
            cur = [w]
    if cur:
        rows.append(" ".join(cur))
    return rows or [""]


def build_content() -> bytes:
    """Build PDF content stream (operators) for the CV."""
    ops: list[str] = []
    y = H - 52

    def text(size: float, x: float, yy: float, s: str, leading: float | None = None):
        ops.append("BT")
        ops.append(f"/F1 {size} Tf")
        if leading:
            ops.append(f"{leading} TL")
        ops.append(f"1 0 0 1 {x:.2f} {yy:.2f} Tm")
        ops.append(f"({esc(s)}) Tj")
        ops.append("ET")

    def rule(yy: float):
        ops.append("0.75 w")
        ops.append(f"{MARGIN_L:.2f} {yy:.2f} m")
        ops.append(f"{W - MARGIN_R:.2f} {yy:.2f} l")
        ops.append("S")

    def section(title: str):
        nonlocal y
        y -= 18
        text(11, MARGIN_L, y, title.upper())
        y -= 6
        rule(y)
        y -= 14

    # Header
    text(20, MARGIN_L, y, "Rahul Sharma")
    y -= 16
    text(10, MARGIN_L, y, "Backend / Full-Stack Developer  |  Bangalore / Remote  |  No night shifts")
    y -= 13
    text(
        9,
        MARGIN_L,
        y,
        "rahul.sharma.dev@email.com  |  +91 98765 43210  |  linkedin.com/in/rahulsharma-backend",
    )
    y -= 8
    rule(y)

    # Summary
    section("Summary")
    summary = (
        "Backend developer with ~3 years of experience building Node.js and PostgreSQL services. "
        "Strong interest in fintech and deep-tech products. Comfortable owning APIs end-to-end, "
        "improving reliability under load, and collaborating with product teams. Currently leveling up "
        "in system design and AWS. Past exposure to Android basics."
    )
    for row in lines_for(summary, 92):
        text(9.5, MARGIN_L, y, row)
        y -= 12

    # Experience
    section("Experience")

    text(10.5, MARGIN_L, y, "Backend Engineer  -  PayFlow Technologies, Bangalore")
    y -= 12
    text(9, MARGIN_L, y, "Jan 2023 - Present")
    y -= 13
    bullets = [
        "Designed and operated a payments API serving high transaction volume with zero planned downtime.",
        "Built Node.js services on PostgreSQL with idempotent payment flows, retries, and audit logging.",
        "Reduced p95 latency on checkout endpoints by optimizing queries and connection pooling.",
        "Partnered with product and mobile on mid-level backend and full-stack merchant dashboard features.",
        "Added monitoring and runbooks so on-call could recover from provider outages without night shifts.",
    ]
    for b in bullets:
        for i, row in enumerate(lines_for("- " + b, 92)):
            text(9.5, MARGIN_L + (0 if i == 0 else 10), y, row)
            y -= 12
        y -= 2

    y -= 4
    text(10.5, MARGIN_L, y, "Software Engineer (Backend)  -  Nimbus Soft, Hyderabad")
    y -= 12
    text(9, MARGIN_L, y, "Jul 2021 - Dec 2022")
    y -= 13
    bullets2 = [
        "Developed REST APIs in Node.js for internal tools and customer-facing workflows.",
        "Modeled relational data in PostgreSQL; wrote migrations and indexes for growing datasets.",
        "Contributed early Android prototypes (Java/Kotlin basics) before focusing fully on backend.",
    ]
    for b in bullets2:
        for i, row in enumerate(lines_for("- " + b, 92)):
            text(9.5, MARGIN_L + (0 if i == 0 else 10), y, row)
            y -= 12
        y -= 2

    # Skills
    section("Skills")
    skills = [
        "Languages & runtime: JavaScript, TypeScript, Node.js",
        "Data: PostgreSQL, Redis (basic), SQL query tuning",
        "APIs & practices: REST, webhooks, idempotency, logging, testing",
        "Cloud & learning: AWS (in progress), system design fundamentals",
        "Other: Git, CI basics; Android fundamentals (past)",
        "Preferences: Bangalore or remote; daytime IST hours; fintech / deep-tech domains",
    ]
    for s in skills:
        text(9.5, MARGIN_L, y, "- " + s)
        y -= 12

    # Education
    section("Education")
    text(10.5, MARGIN_L, y, "B.Tech, Computer Science  -  VIT University")
    y -= 12
    text(9.5, MARGIN_L, y, "2017 - 2021")
    y -= 14
    text(
        8.5,
        MARGIN_L,
        y,
        "This document is a fictional sample CV for product demos. All names and employers are made up.",
    )

    return ("\n".join(ops) + "\n").encode("latin-1")


def write_pdf(path: Path, content: bytes) -> None:
    # Minimal PDF 1.4 with one page, Helvetica, extractable text.
    objects: list[bytes] = []

    def obj(n: int, body: bytes) -> None:
        while len(objects) < n:
            objects.append(b"")
        objects[n - 1] = body

    obj(1, b"<< /Type /Catalog /Pages 2 0 R >>")
    obj(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    obj(
        3,
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W} {H}] "
            f"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
        ).encode(),
    )
    obj(4, f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"\nendstream")
    obj(5, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode())
        out.extend(body)
        out.extend(b"\nendobj\n")

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode())
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n".encode()
    )
    path.write_bytes(out)


def main() -> None:
    write_pdf(OUT, build_content())
    print(OUT)


if __name__ == "__main__":
    main()
