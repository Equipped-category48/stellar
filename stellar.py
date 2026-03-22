"""
stellar.py — High-quality image upscaling CLI tool.

Author  : Soumalya Das <geniussantu1983@gmail.com>
Project : https://github.com/pro-grammer-SD/stellar
License : MIT
"""

from __future__ import annotations

import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
import typer
from PIL import Image
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logger = logging.getLogger("stellar")
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter("[stellar] %(levelname)s — %(message)s"))
logger.addHandler(_handler)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUPPORTED_FORMATS: tuple[str, ...] = (".png", ".jpg", ".jpeg")
UPSCALED_SUFFIX = "_upscaled"

# ---------------------------------------------------------------------------
# Typer app
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="stellar",
    help="🌟 stellar — high-quality image upscaling from the command line.",
    add_completion=False,
    pretty_exceptions_show_locals=False,
)


# ---------------------------------------------------------------------------
# Core image helpers
# ---------------------------------------------------------------------------


def load_image(path: Path) -> Tuple[np.ndarray, str]:
    """
    Load an image from *path* and return it as a NumPy array together with
    its detected format (e.g. ``"PNG"``).

    Parameters
    ----------
    path:
        Absolute or relative path to the source image file.

    Returns
    -------
    (array, format_string)
        BGR NumPy array as returned by OpenCV, and the Pillow format string.

    Raises
    ------
    FileNotFoundError
        If *path* does not point to an existing file.
    ValueError
        If the file cannot be decoded as an image.
    """
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    # Use Pillow to reliably detect the original format.
    with Image.open(path) as pil_img:
        fmt = pil_img.format or path.suffix.lstrip(".").upper()

    arr = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if arr is None:
        raise ValueError(f"OpenCV could not decode image: {path}")

    return arr, fmt


def upscale_image(
    image: np.ndarray,
    scale: float = 2.0,
    target_width: Optional[int] = None,
    target_height: Optional[int] = None,
) -> np.ndarray:
    """
    Upscale *image* using Lanczos interpolation via OpenCV.

    Lanczos (``cv2.INTER_LANCZOS4``) consistently produces sharper,
    more artefact-free results than bicubic/bilinear for photographic
    content.  A mild unsharp-mask sharpening pass is applied afterwards
    to recover high-frequency detail smoothed over by interpolation.

    Parameters
    ----------
    image:
        Source image as a NumPy array (BGR or BGRA, any bit depth).
    scale:
        Multiplicative scale factor (ignored when *target_width* /
        *target_height* are provided).
    target_width:
        Explicit output width in pixels.
    target_height:
        Explicit output height in pixels.

    Returns
    -------
    np.ndarray
        Upscaled image array.
    """
    src_h, src_w = image.shape[:2]

    if target_width or target_height:
        if target_width and not target_height:
            ratio = target_width / src_w
            dst_w, dst_h = target_width, int(src_h * ratio)
        elif target_height and not target_width:
            ratio = target_height / src_h
            dst_w, dst_h = int(src_w * ratio), target_height
        else:
            dst_w, dst_h = target_width, target_height  # type: ignore[assignment]
    else:
        dst_w = int(src_w * scale)
        dst_h = int(src_h * scale)

    upscaled = cv2.resize(image, (dst_w, dst_h), interpolation=cv2.INTER_LANCZOS4)

    # Post-processing: mild unsharp-mask sharpening.
    upscaled = _sharpen(upscaled)

    return upscaled


def _sharpen(image: np.ndarray) -> np.ndarray:
    """
    Apply a conservative unsharp-mask sharpening pass to *image*.

    Uses the formula:  sharpened = original + amount * (original - blurred)
    The amount (0.4) and sigma (1.5) are tuned to recover detail without
    amplifying noise on already-noisy sources.

    Parameters
    ----------
    image:
        Input array (any channel count, uint8 or uint16).

    Returns
    -------
    np.ndarray
        Sharpened array of identical dtype and shape.
    """
    amount = 0.4
    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=1.5)
    return cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)


def save_image(image: np.ndarray, dest: Path, fmt: str) -> None:
    """
    Write *image* to *dest* using *fmt* as the output container format.

    PNG images are written losslessly (compression level 3).
    JPEG images are written at quality 95.

    Parameters
    ----------
    image:
        NumPy array to persist.
    dest:
        Full destination path including filename and extension.
    fmt:
        Target format string (e.g. ``"PNG"``, ``"JPEG"``).
    """
    dest.parent.mkdir(parents=True, exist_ok=True)

    if fmt.upper() == "PNG":
        cv2.imwrite(str(dest), image, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    else:
        cv2.imwrite(str(dest), image, [cv2.IMWRITE_JPEG_QUALITY, 95])

    logger.debug("Saved → %s", dest)


# ---------------------------------------------------------------------------
# Single-image pipeline
# ---------------------------------------------------------------------------


def _process_one(
    src: Path,
    out_dir: Path,
    scale: float,
    out_fmt: Optional[str],
    verbose: bool,
) -> Tuple[Path, float]:
    """
    Full load → upscale → save pipeline for a single image file.

    Returns the destination path and wall-clock time taken (seconds).
    """
    t0 = time.perf_counter()

    image, detected_fmt = load_image(src)

    target_fmt = (out_fmt or detected_fmt).upper()
    ext = ".jpg" if target_fmt == "JPEG" else f".{target_fmt.lower()}"

    dest = out_dir / (src.stem + UPSCALED_SUFFIX + ext)

    upscaled = upscale_image(image, scale=scale)
    save_image(upscaled, dest, target_fmt)

    elapsed = time.perf_counter() - t0

    if verbose:
        src_h, src_w = image.shape[:2]
        dst_h, dst_w = upscaled.shape[:2]
        logger.info(
            "%s  [%dx%d → %dx%d]  %.2fs",
            src.name, src_w, src_h, dst_w, dst_h, elapsed,
        )

    return dest, elapsed


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------


@app.command()
def upscale(
    input_dir: Path = typer.Option(
        ...,
        "--input", "-i",
        help="📂 Input folder containing images to upscale.",
        show_default=False,
    ),
    output_dir: Path = typer.Option(
        Path("upscaled"),
        "--output", "-o",
        help="📁 Output folder for upscaled images.",
    ),
    scale: float = typer.Option(
        2.0,
        "--scale", "-s",
        help="🔍 Scale factor (e.g. 2 doubles the resolution).",
        min=1.0,
        max=16.0,
    ),
    fmt: Optional[str] = typer.Option(
        None,
        "--format", "-f",
        help="🖼  Output format override: PNG, JPG, JPEG. Defaults to original.",
    ),
    workers: int = typer.Option(
        4,
        "--workers", "-w",
        help="⚡ Number of parallel worker threads.",
        min=1,
        max=32,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="🔊 Print per-image resolution and timing details.",
        is_flag=True,
    ),
) -> None:
    """
    🌟 Upscale all images in INPUT_DIR and write them to OUTPUT_DIR.

    Supported source formats: PNG, JPG, JPEG.

    \b
    Examples
    --------
    stellar --input ./photos --scale 3
    stellar -i ./shots -o ./hd --scale 4 --format PNG --verbose
    stellar -i ./raw -o ./out -s 2 -w 8
    """
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # ── validate input directory ──────────────────────────────────────────
    if not input_dir.exists() or not input_dir.is_dir():
        typer.echo(
            typer.style(
                f"❌  Input folder does not exist: {input_dir}",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)

    images = [
        p for p in sorted(input_dir.iterdir())
        if p.is_file() and p.suffix.lower() in SUPPORTED_FORMATS
    ]

    if not images:
        typer.echo(
            typer.style(
                f"⚠️  No supported images found in: {input_dir}",
                fg=typer.colors.YELLOW,
            ),
        )
        raise typer.Exit(code=0)

    output_dir.mkdir(parents=True, exist_ok=True)

    # ── banner ────────────────────────────────────────────────────────────
    typer.echo(
        typer.style(
            f"\n🌟 stellar — upscaling {len(images)} image(s)  "
            f"|  scale ×{scale}  |  → {output_dir}\n",
            fg=typer.colors.CYAN,
            bold=True,
        )
    )

    # ── threaded batch processing ─────────────────────────────────────────
    errors: list[tuple[Path, str]] = []
    total_time = 0.0

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_process_one, img, output_dir, scale, fmt, verbose): img
            for img in images
        }

        with tqdm(
            total=len(images),
            desc="  Upscaling",
            unit="img",
            colour="cyan",
            dynamic_ncols=True,
        ) as bar:
            for future in as_completed(futures):
                src_path = futures[future]
                try:
                    _, elapsed = future.result()
                    total_time += elapsed
                except Exception as exc:  # noqa: BLE001
                    errors.append((src_path, str(exc)))
                    logger.error("Failed: %s — %s", src_path.name, exc)
                finally:
                    bar.update(1)

    # ── summary ───────────────────────────────────────────────────────────
    success = len(images) - len(errors)
    typer.echo(
        typer.style(
            f"\n✅  Done!  {success}/{len(images)} images upscaled in {total_time:.1f}s",
            fg=typer.colors.GREEN,
            bold=True,
        )
    )

    if errors:
        typer.echo(
            typer.style(f"⚠️  {len(errors)} error(s):", fg=typer.colors.YELLOW, bold=True)
        )
        for p, msg in errors:
            typer.echo(f"   • {p.name}: {msg}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
    