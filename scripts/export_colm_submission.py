#!/usr/bin/env python
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


COLM_PREAMBLE = r"""\documentclass{article}

\usepackage[submission]{colm2026_conference}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{float}
\usepackage{hyperref}
\usepackage{url}
\usepackage{xcolor}
\usepackage{lineno}

\emergencystretch=2em

\definecolor{darkblue}{rgb}{0,0,0.5}
\hypersetup{colorlinks=true, citecolor=darkblue, linkcolor=darkblue, urlcolor=darkblue}

"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="paper/main.tex")
    parser.add_argument("--out", default="paper/colm2026_submission.tex")
    args = parser.parse_args()

    source = Path(args.source)
    text = source.read_text(encoding="utf-8")
    title_start = text.find(r"\title")
    if title_start < 0:
        raise SystemExit(f"{source} has no title block")

    body = text[title_start:]
    body = body.replace(r"\author{Anonymous}", r"\author{}")
    body = body.replace(
        "\\begin{document}\n\\maketitle",
        "\\begin{document}\n\\ifcolmsubmission\n\\linenumbers\n\\fi\n\\maketitle",
    )
    body = body.replace(r"\bibliographystyle{plain}", r"\bibliographystyle{colm2026_conference}")
    body = re.sub(r"\\begin\{table\}\[H\]", r"\\begin{table}[t]", body)
    body = re.sub(r"\\begin\{figure\}\[H\]", r"\\begin{figure}[t]", body)

    Path(args.out).write_text(COLM_PREAMBLE + body, encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
