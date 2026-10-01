"""Own the synthetic writer-document to actual PDF and preview workflow."""
from __future__ import annotations

import os
import shutil

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(os.environ.get("RUN_E2E") != "1", reason="RUN_E2E=1 required"),
]


def test_export_compile_preview_creates_real_artifacts(tmp_path):
    # Arrange: public synthetic content and a real compiler, never a shim.
    from matplotlib import pyplot as plt
    from matplotlib.figure import Figure
    from scitex_tex import compile_tex, export_tex, preview

    if not shutil.which("pdflatex"):
        raise RuntimeError("Owning PDF tests require real pdflatex")
    document = {
        "metadata": {"title": "Synthetic SciTeX control", "author": "Public test"},
        "blocks": [{"type": "paragraph", "text": "A synthetic document with 3 samples."}],
    }
    # Act: exercise the user-visible export, compilation, and rendering paths.
    source = export_tex(document, tmp_path / "synthetic.tex")
    result = compile_tex(source)
    figure = preview([r"x^2", r"\alpha + \beta"], enable_fallback=False)
    preview_file = tmp_path / "preview.png"
    figure.savefig(preview_file)
    try:
        # Assert: successful compilation produces genuine PDF bytes; the
        # documented Figure carries flat axes and renders genuine PNG bytes.
        assert (
            result.success,
            result.exit_code,
            result.pdf_path.read_bytes()[:5] if result.pdf_path else b"",
            isinstance(figure, Figure),
            len(figure.axes),
            preview_file.read_bytes()[:8],
        ) == (True, 0, b"%PDF-", True, 2, b"\x89PNG\r\n\x1a\n"), result.stderr
    finally:
        plt.close(figure)
