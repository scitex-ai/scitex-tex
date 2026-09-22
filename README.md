# scitex-tex

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>LaTeX helpers — export to .tex, compile to PDF, preview images, vector formatting.</b></p>

<p align="center">
  <a href="https://scitex-tex.readthedocs.io/">Full Documentation</a> · <code>uv pip install scitex-tex[all]</code>
</p>

<!-- scitex-badges:start -->
<p align="center">
  <a href="https://pypi.org/project/scitex-tex/"><img src="https://img.shields.io/pypi/v/scitex-tex?label=pypi" alt="pypi"></a>
  <a href="https://pypi.org/project/scitex-tex/"><img src="https://img.shields.io/pypi/pyversions/scitex-tex?label=python" alt="python"></a>
  <a href="https://github.com/scitex-ai/scitex-tex/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/scitex-ai/scitex-tex/ci.yml?branch=develop&label=docs" alt="docs"></a>
  <a href="https://scitex-tex.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/scitex-tex?label=docs" alt="docs-rtd"></a>
</p>
<p align="center">
  <a href="https://github.com/scitex-ai/scitex-tex/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/scitex-ai/scitex-tex/ci.yml?branch=develop&label=tests" alt="tests"></a>
  <a href="https://github.com/scitex-ai/scitex-tex/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/scitex-ai/scitex-tex/ci.yml?branch=develop&label=install-check" alt="install-check"></a>
  <a href="https://codecov.io/gh/scitex-ai/scitex-tex"><img src="https://img.shields.io/codecov/c/github/scitex-ai/scitex-tex/develop?label=cov" alt="cov"></a>
</p>
<!-- scitex-badges:end -->

---

## Problem and Solution

| # | Problem | Solution |
|---|---------|----------|
| 1 | **Brittle authoring** — hand-written `.tex` needs manual escaping of `_` / `&` / `%` plus the right `pdflatex` flags | **Two calls** — `export_tex` writes `.tex`, `compile_tex` builds `.pdf`; `CompileResult` holds the pdf path + log |
| 2 | **Slow previews** — checking one math snippet means opening a full LaTeX project | **One call** — `preview` renders snippets to a matplotlib `Figure`, no system TeX needed |
| 3 | **Manual vectors** — wrapping labels in vector notation by hand is error-prone | **One call** — `to_vec("AB")` returns vector form with automatic fallback |

## Quick Start

```python
import scitex_tex as tx

# Convert a SciTeX-style writer doc → .tex
tx.export_tex(doc, "manuscript.tex")

# Compile .tex → .pdf (returns CompileResult)
result = tx.compile_tex("manuscript.tex")

# Render LaTeX snippets to a matplotlib Figure
fig = tx.preview([r"$\sum_{i=1}^N x_i$", r"$\alpha + \beta$"])

# Convert a string to LaTeX vector notation
tx.to_vec("AB")  # → \overrightarrow{\mathrm{AB}}
```

## Demo

```python
import scitex_tex as tx

# 1) Render a math preview to a matplotlib Figure (no system TeX required)
fig = tx.preview([r"$\hat{\beta} = (X^\top X)^{-1} X^\top y$"])
fig.savefig("preview.png")

# 2) Export + compile a manuscript end-to-end
tx.export_tex(doc, "manuscript.tex")
result = tx.compile_tex("manuscript.tex")
print(result.pdf_path)   # → manuscript.pdf
```

```mermaid
flowchart LR
    A[Python writer doc] -->|export_tex| B[manuscript.tex]
    B -->|compile_tex| C[manuscript.pdf]
    D["r'\$\\hat\\beta\$'"] -->|preview| E[matplotlib Figure]
    style C fill:#27ae60,stroke:#2c3e50,color:#fff
    style E fill:#27ae60,stroke:#2c3e50,color:#fff
```

<p align="center"><sub><b>Figure 2.</b> Demo flow. <code>preview</code> is matplotlib-only; <code>compile_tex</code> shells out to <code>pdflatex</code>/<code>xelatex</code>.</sub></p>

## Installation

```bash
uv pip install "scitex-tex[all]"
```

<details>
<summary><b>Per-module extras</b></summary>

<br>

| Extra | Pulls in |
|---|---|
| `all` | `dev` + `docs` (recommended) |
| `dev` | pytest, pytest-cov, ruff |
| `docs` | Sphinx + RTD theme + myst-parser (docs build only) |

```bash
uv pip install -e ".[dev]"               # editable install for contributors
```

</details>
## Architecture

```
scitex_tex/
├── _export.py        # writer doc  → .tex string + file; .tex → .pdf via pdflatex/xelatex
├── _preview.py       # snippet     → matplotlib Figure (no system TeX needed)
└── _to_vec.py        # string      → LaTeX \overrightarrow form
```

```mermaid
flowchart LR
    Doc[Writer Doc<br/>Python dict/object] --> Exp[export_tex]
    Exp --> Tex[manuscript.tex]
    Tex --> Cmp[compile_tex]
    Cmp --> Pdf[manuscript.pdf]
    Snip[r'\$\\sum x_i\$'] --> Prv[preview]
    Prv --> Fig[matplotlib Figure]
    Label[AB] --> Vec[to_vec]
    Vec --> Latex[r'\overrightarrow{\mathrm{AB}}']
```

<p align="center"><sub><b>Figure 1.</b> Module layout. Three modules — export+compile, preview, vector notation — each callable independently.</sub></p>

## 1 Interfaces

<details open>
<summary><strong>Python API</strong></summary>

<br>

```python
import scitex_tex as tx

# Export — writer doc → .tex string + file
tx.export_tex(doc, "manuscript.tex")

# Compile — .tex → .pdf via pdflatex/xelatex; returns CompileResult
res = tx.compile_tex("manuscript.tex")
print(res.pdf_path, res.stdout)

# Preview — render LaTeX strings to a matplotlib Figure
fig = tx.preview([r"$\frac{1}{2}\sum x_i$", r"$\hat{\beta}$"])
fig.savefig("preview.png")

# Convert a string to LaTeX vector notation
tx.to_vec("AB")  # → \overrightarrow{\mathrm{AB}}
```

</details>

## Status

Standalone module from the SciTeX ecosystem. Dependencies: numpy, matplotlib,
scitex-plt, and scitex-dev (for optional imports). The umbrella package's `scitex.tex` import path
is preserved via a `sys.modules`-alias bridge.

## Part of SciTeX

`scitex-tex` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[tex]` to use as
`scitex.tex` (Python) or `scitex tex ...` (CLI).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
