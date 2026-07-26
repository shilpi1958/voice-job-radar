#!/usr/bin/env python3
"""Generate one-page sample CV PDFs with extractable text (no deps).

Outputs:
  docs/sample-cv-backend.pdf   — Rahul Sharma (backend)
  docs/sample-cv-robotics.pdf  — Arjun Mehra (robotics / perception)

Usage:
  python3 docs/generate-sample-cv.py
  python3 docs/generate-sample-cv.py --only robotics
  python3 docs/generate-sample-cv.py --only backend
"""

from __future__ import annotations

import argparse
from pathlib import Path

DOCS = Path(__file__).resolve().parent

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


class PageBuilder:
    def __init__(self, *, body: float = 9.5, bullet_gap: float = 12, after_bullet: float = 2):
        self.ops: list[str] = []
        self.y = H - 52
        self.body = body
        self.bullet_gap = bullet_gap
        self.after_bullet = after_bullet
        self.max_chars = 92

    def text(self, size: float, x: float, yy: float, s: str) -> None:
        self.ops.append("BT")
        self.ops.append(f"/F1 {size} Tf")
        self.ops.append(f"1 0 0 1 {x:.2f} {yy:.2f} Tm")
        self.ops.append(f"({esc(s)}) Tj")
        self.ops.append("ET")

    def rule(self, yy: float) -> None:
        self.ops.append("0.75 w")
        self.ops.append(f"{MARGIN_L:.2f} {yy:.2f} m")
        self.ops.append(f"{W - MARGIN_R:.2f} {yy:.2f} l")
        self.ops.append("S")

    def section(self, title: str, *, before: float = 18, after_rule: float = 14) -> None:
        self.y -= before
        self.text(11, MARGIN_L, self.y, title.upper())
        self.y -= 6
        self.rule(self.y)
        self.y -= after_rule

    def header(self, name: str, subtitle: str, contact: str) -> None:
        self.text(20, MARGIN_L, self.y, name)
        self.y -= 16
        self.text(10, MARGIN_L, self.y, subtitle)
        self.y -= 13
        self.text(9, MARGIN_L, self.y, contact)
        self.y -= 8
        self.rule(self.y)

    def para(self, text: str, *, size: float | None = None, gap: float | None = None) -> None:
        size = self.body if size is None else size
        gap = self.bullet_gap if gap is None else gap
        for row in lines_for(text, self.max_chars):
            self.text(size, MARGIN_L, self.y, row)
            self.y -= gap

    def job(self, title: str, dates: str, bullets: list[str]) -> None:
        self.text(10.5, MARGIN_L, self.y, title)
        self.y -= 12
        self.text(9, MARGIN_L, self.y, dates)
        self.y -= 13
        for b in bullets:
            for i, row in enumerate(lines_for("- " + b, self.max_chars)):
                self.text(self.body, MARGIN_L + (0 if i == 0 else 10), self.y, row)
                self.y -= self.bullet_gap
            self.y -= self.after_bullet

    def skill_lines(self, skills: list[str]) -> None:
        for s in skills:
            self.text(self.body, MARGIN_L, self.y, "- " + s)
            self.y -= self.bullet_gap

    def footer_note(self, note: str) -> None:
        self.y -= 10
        self.text(8.5, MARGIN_L, self.y, note)

    def content(self) -> bytes:
        return ("\n".join(self.ops) + "\n").encode("latin-1")


def build_backend() -> bytes:
    p = PageBuilder()
    p.header(
        "Rahul Sharma",
        "Backend / Full-Stack Developer  |  Bangalore / Remote  |  No night shifts",
        "rahul.sharma.dev@email.com  |  +91 98765 43210  |  linkedin.com/in/rahulsharma-backend",
    )
    p.section("Summary")
    p.para(
        "Backend developer with ~3 years of experience building Node.js and PostgreSQL services. "
        "Strong interest in fintech and deep-tech products. Comfortable owning APIs end-to-end, "
        "improving reliability under load, and collaborating with product teams. Currently leveling up "
        "in system design and AWS. Past exposure to Android basics."
    )
    p.section("Experience")
    p.job(
        "Backend Engineer  -  PayFlow Technologies, Bangalore",
        "Jan 2023 - Present",
        [
            "Designed and operated a payments API serving high transaction volume with zero planned downtime.",
            "Built Node.js services on PostgreSQL with idempotent payment flows, retries, and audit logging.",
            "Reduced p95 latency on checkout endpoints by optimizing queries and connection pooling.",
            "Partnered with product and mobile on mid-level backend and full-stack merchant dashboard features.",
            "Added monitoring and runbooks so on-call could recover from provider outages without night shifts.",
        ],
    )
    p.y -= 4
    p.job(
        "Software Engineer (Backend)  -  Nimbus Soft, Hyderabad",
        "Jul 2021 - Dec 2022",
        [
            "Developed REST APIs in Node.js for internal tools and customer-facing workflows.",
            "Modeled relational data in PostgreSQL; wrote migrations and indexes for growing datasets.",
            "Contributed early Android prototypes (Java/Kotlin basics) before focusing fully on backend.",
        ],
    )
    p.section("Skills")
    p.skill_lines(
        [
            "Languages & runtime: JavaScript, TypeScript, Node.js",
            "Data: PostgreSQL, Redis (basic), SQL query tuning",
            "APIs & practices: REST, webhooks, idempotency, logging, testing",
            "Cloud & learning: AWS (in progress), system design fundamentals",
            "Other: Git, CI basics; Android fundamentals (past)",
            "Preferences: Bangalore or remote; daytime IST hours; fintech / deep-tech domains",
        ]
    )
    p.section("Education")
    p.text(10.5, MARGIN_L, p.y, "B.Tech, Computer Science  -  VIT University")
    p.y -= 12
    p.text(9.5, MARGIN_L, p.y, "2017 - 2021")
    p.footer_note(
        "This document is a fictional sample CV for product demos. All names and employers are made up."
    )
    return p.content()


def build_robotics() -> bytes:
    # Slightly tighter spacing so three roles + projects fit on one A4 page.
    p = PageBuilder(body=9, bullet_gap=11, after_bullet=1)
    p.max_chars = 95
    p.y = H - 48
    p.header(
        "Arjun Mehra",
        "Robotics / Perception Engineer  |  Bangalore / Hyderabad / Remote IST  |  Daytime preferred",
        "arjun.mehra.robotics@email.com  |  +91 98123 45670  |  linkedin.com/in/arjunmehra-robotics",
    )
    p.section("Summary", before=14, after_rule=12)
    p.para(
        "Robotics engineer with ~2.5 years building perception and ROS2 software for mobile robots. "
        "Strong in Python, C++, OpenCV, and embedded (STM32). Experience shipping camera + ranging "
        "obstacle avoidance on warehouse AMRs, validated in Gazebo before field trials. Seeking "
        "Robotics Engineer roles in perception, control, ROS, or embedded - warehouse, industrial "
        "automation, or deep-tech hardware+software teams in India.",
        gap=11,
    )
    p.section("Experience", before=14, after_rule=12)
    p.job(
        "Robotics Software Engineer  -  NovaBot Labs, Bangalore",
        "Mar 2024 - Present",
        [
            "Owned ROS2 perception nodes for warehouse AMRs: camera + ultrasonic fusion for obstacle avoidance.",
            "Cut end-to-end perception latency via node graph and QoS changes; validated in Gazebo before field trials.",
            "Improved aisle-trial collision rate after tuning costmap inflation and safety margins with controls.",
            "Wrote Python tooling for bag replay and regression checks on perception pipelines.",
            "Collaborated with mechanical and embedded on sensor mounting, calibration, and bring-up.",
        ],
    )
    p.y -= 2
    p.job(
        "Junior Robotics Engineer  -  MechNest Automation, Bangalore",
        "Aug 2022 - Feb 2024",
        [
            "Developed ROS (ROS1 to early ROS2) packages for conveyor-adjacent mobile bases.",
            "Implemented OpenCV line/marker detection for docking assist; C++ nodes for tighter loops.",
            "Brought up STM32 firmware for motor drivers and basic telemetry over UART/CAN.",
            "Supported on-site commissioning for two factory pilot deployments (daytime IST).",
        ],
    )
    p.y -= 2
    p.job(
        "Embedded Systems Intern  -  MechNest Automation, Bangalore",
        "Jan 2022 - Jul 2022",
        [
            "Prototyped sensor drivers (IMU, ultrasonic) and logging utilities on STM32 / Arduino-class boards.",
            "Assisted senior engineers with hardware bring-up checklists and lab test scripts.",
        ],
    )
    p.section("Skills", before=12, after_rule=11)
    p.skill_lines(
        [
            "Robotics middleware: ROS2 (nodes, launch, tf, bags), Gazebo simulation",
            "Perception: OpenCV, camera calibration basics, obstacle detection, basic SLAM exposure",
            "Languages: Python, C++, C (embedded)",
            "Embedded: STM32, UART/CAN basics, motor driver bring-up",
            "Controls / planning: PID tuning support, costmaps & planners (deepening motion planning)",
            "Tools: Git, Linux, basic CI for package builds",
            "Preferences: Bangalore, Hyderabad, or remote IST daytime; lab/field OK; no night-only roles",
        ]
    )
    p.section("Education", before=12, after_rule=11)
    p.text(10.5, MARGIN_L, p.y, "B.Tech, Electronics & Communication  -  RV College of Engineering, Bangalore")
    p.y -= 11
    p.text(9, MARGIN_L, p.y, "2018 - 2022  |  Coursework: control systems, embedded, computer vision; ROS line-follower project")
    p.section("Projects", before=12, after_rule=11)
    p.skill_lines(
        [
            "Gazebo sim stack for AMR aisle navigation demos (costmap + simple planner configs)",
            "STM32 + ROS bridge prototype for wheel odometry telemetry",
        ]
    )
    p.footer_note(
        "This document is a fictional sample CV for product demos. All names and employers are made up."
    )
    return p.content()


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


CVS = {
    "backend": ("sample-cv-backend.pdf", build_backend),
    "robotics": ("sample-cv-robotics.pdf", build_robotics),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate demo sample CV PDFs (no deps).")
    parser.add_argument(
        "--only",
        choices=sorted(CVS),
        help="Generate only one persona PDF (default: both).",
    )
    args = parser.parse_args()
    targets = [args.only] if args.only else list(CVS)
    for key in targets:
        name, builder = CVS[key]
        path = DOCS / name
        write_pdf(path, builder())
        print(path)


if __name__ == "__main__":
    main()
