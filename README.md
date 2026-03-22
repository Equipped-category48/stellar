<div align="center">

# 🌟 stellar

**High-quality image upscaling from the command line.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/stellar/)
[![GitHub](https://img.shields.io/badge/GitHub-pro--grammer--SD%2Fstellar-181717?logo=github)](https://github.com/pro-grammer-SD/stellar)

*Lanczos interpolation · Unsharp-mask sharpening · Parallel batch processing · tqdm progress bars*

</div>

---

## ✨ Features

- 🔍 **Scale images** by any factor (1×–16×) using Lanczos interpolation
- 🖼  **Supports** PNG, JPG, JPEG input and output formats
- ⚡ **Multithreaded** batch processing for large image sets
- 📊 **tqdm** progress bar with per-image resolution and timing stats
- 🔧 **Modular code** — clean `load_image()`, `upscale_image()`, `save_image()` API
- 🛡  **Graceful error handling** — bad files are logged and skipped, not crashes
- 📦 **Installable as a global CLI tool** via pip or wheel

---

## 📦 Installation

### Option 1 — Install from PyPI *(recommended)*

```bash
pip install stellar
```

### Option 2 — Install from source

```bash
git clone https://github.com/pro-grammer-SD/stellar.git
cd stellar
pip install .
```

### Option 3 — Build & install a wheel locally

#### Prerequisites

```bash
pip install build
```

#### Build the wheel

```bash
# From the repository root:
python -m build
```

This produces two distribution artefacts inside `dist/`:

```
dist/
├── stellar-1.0.0-py3-none-any.whl   ← wheel (preferred)
└── stellar-1.0.0.tar.gz             ← sdist
```

#### Install the wheel

```bash
pip install dist/stellar-1.0.0-py3-none-any.whl
```

Or use a glob to pick up whichever version was built:

```bash
pip install dist/stellar-*.whl
```

#### Upgrade an existing install from a new wheel

```bash
pip install --upgrade dist/stellar-*.whl
```

#### Uninstall

```bash
pip uninstall stellar
```

After installation the `stellar` command will be available on your `PATH`.

---

## 🚀 Usage

### Basic upscale (2× default)

```bash
stellar --input ./photos
```

### Custom scale factor

```bash
stellar --input ./photos --scale 4
```

### Custom output folder

```bash
stellar --input ./raw --output ./hd
```

### Force PNG output format

```bash
stellar -i ./shots -o ./out --format PNG
```

### Verbose mode (per-image resolution + timing)

```bash
stellar -i ./photos --verbose
```

### Use 8 parallel workers for large batches

```bash
stellar -i ./large_batch -o ./upscaled -s 2 -w 8
```

### All options at once

```bash
stellar \
  --input  ./raw_photos \
  --output ./upscaled \
  --scale  3 \
  --format PNG \
  --workers 6 \
  --verbose
```

---

## 📖 CLI Reference

```
Usage: stellar [OPTIONS]

  🌟 Upscale all images in INPUT_DIR and write them to OUTPUT_DIR.

  Supported source formats: PNG, JPG, JPEG.

Options:
  -i, --input   PATH     📂 Input folder containing images to upscale. [required]
  -o, --output  PATH     📁 Output folder for upscaled images. [default: upscaled]
  -s, --scale   FLOAT    🔍 Scale factor (e.g. 2 doubles the resolution). [default: 2.0]
  -f, --format  TEXT     🖼  Output format override: PNG, JPG, JPEG.
  -w, --workers INTEGER  ⚡ Number of parallel worker threads. [default: 4]
  -v, --verbose          🔊 Print per-image resolution and timing details.
      --help             Show this message and exit.
```

Output filenames are the original name with `_upscaled` appended:

```
photos/sunset.jpg  →  upscaled/sunset_upscaled.jpg
```

---

## 🧰 Dependencies

| Package | Purpose |
|---|---|
| [Pillow](https://python-pillow.org/) | Image format detection |
| [opencv-python](https://pypi.org/project/opencv-python/) | Image I/O and Lanczos resize |
| [scikit-learn](https://scikit-learn.org/) | Optional interpolation utilities |
| [typer](https://typer.tiangolo.com/) | CLI framework |
| [tqdm](https://tqdm.github.io/) | Progress bars |
| [numpy](https://numpy.org/) | Array operations |

---

## 🗂 Project Structure

```
stellar/
├── stellar.py            # Main script (load / upscale / save / CLI)
├── pyproject.toml        # Build config & metadata
├── README.md
├── LICENSE               # MIT
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── PULL_REQUEST_TEMPLATE.md
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

---

## 🔒 Security

To report a security vulnerability, please see [SECURITY.md](./SECURITY.md).

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).  
Copyright © 2025 Soumalya Das

---

<div align="center">
Made with ❤️ by <a href="https://github.com/pro-grammer-SD">Soumalya Das</a>
</div>
