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


def test_export_embedded_preview_compiles_with_latexmk(tmp_path):
    # Arrange: a documented alternate compiler and a real preview image.
    from matplotlib import pyplot as plt
    from scitex_tex import compile_tex, export_tex, preview

    if not shutil.which("latexmk"):
        raise RuntimeError("Owning alternate-engine tests require real latexmk")
    figure = preview([r"x^2", r"\alpha + \beta"], enable_fallback=False)
    image_file = tmp_path / "preview.png"
    try:
        figure.savefig(image_file)
    finally:
        plt.close(figure)
    image_bytes = image_file.read_bytes()
    document = {
        "metadata": {"title": "Synthetic illustrated control", "author": "Public test"},
        "blocks": [
            {"type": "heading", "level": 1, "text": "Synthetic methods"},
            {"type": "paragraph", "text": "An illustrated document with 3 samples."},
            {"type": "equation", "latex": r"x^2 + y^2 = 1"},
            {"type": "caption", "caption_type": "figure", "number": 1,
             "caption_text": "Real math preview", "image_hash": "synthetic-preview"},
            {"type": "table", "rows": [["Sample", "Value"], ["A", "3"]]},
            {"type": "list-item", "text": "Public synthetic observation"},
        ],
        "references": [{"number": 1, "text": "Public synthetic reference, 2026"}],
        "images": [{"hash": "synthetic-preview", "extension": ".png", "data": image_bytes}],
    }
    output_dir = tmp_path / "compiled"
    # Act: export the embedded image and compile through real automatic passes.
    source = export_tex(document, tmp_path / "illustrated.tex", image_dir=tmp_path / "images")
    result = compile_tex(source, compiler="latexmk", output_dir=output_dir)
    # Assert: the published writer/image/compiler contract produces actual
    # artifacts in the requested directory and removes native auxiliary files.
    assert (
        result.success,
        result.exit_code,
        result.pdf_path.parent if result.pdf_path else None,
        result.pdf_path.read_bytes()[:5] if result.pdf_path else b"",
        (tmp_path / "images" / "fig_1.png").read_bytes(),
        any(output_dir.glob("*.aux")) or any(output_dir.glob("*.fdb_latexmk")),
    ) == (True, 0, output_dir, b"%PDF-", image_bytes, False), result.stderr
