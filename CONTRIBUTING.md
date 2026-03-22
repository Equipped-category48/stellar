# 🤝 Contributing to stellar

First off — thank you for taking the time to contribute! 🎉  
Every bug report, feature idea, and line of code helps make **stellar** better.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Running Tests](#running-tests)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by the
[Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.

---

## 💡 How Can I Contribute?

### 🐛 Reporting Bugs

- Check the [existing issues](https://github.com/pro-grammer-SD/stellar/issues) first.
- Use the **Bug Report** template and fill in all required sections.
- Attach minimal reproducible examples where possible.

### ✨ Suggesting Features

- Open a [Feature Request](https://github.com/pro-grammer-SD/stellar/issues/new?template=feature_request.md).
- Describe the use-case and why it would benefit other users.

### 🔧 Submitting Code

- Fork the repo and create a branch from `main`.
- Keep PRs focused — one feature or fix per PR.
- Add or update tests to cover your changes.
- Run the full test suite before opening a PR.

---

## 🛠 Development Setup

```bash
# 1. Fork & clone
git clone https://github.com/<your-username>/stellar.git
cd stellar

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install in editable mode with all dev + optional deps
pip install -e ".[dev,enhance]"
```

---

## 🎨 Code Style

**stellar** uses [Black](https://black.readthedocs.io/) for formatting and
[Ruff](https://docs.astral.sh/ruff/) for linting.

```bash
# Format
black .

# Lint
ruff check .

# Type check
mypy stellar.py
```

Key conventions:

- **Line length:** 99 characters.
- **Type hints** on all public functions.
- **Docstrings** in NumPy/Google style for all public symbols.
- No bare `except:` — always catch specific exceptions.
- Keep functions small and single-purpose (`load_image`, `upscale_image`, `save_image`).

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=stellar --cov-report=term-missing
```

Please add tests under `tests/` for any new feature or bug fix.

---

## 🔀 Pull Request Process

1. Ensure your branch is up to date with `main`.
2. Run `black .`, `ruff check .`, and `mypy stellar.py` — fix any issues.
3. Run `pytest` — all tests must pass.
4. Open a PR against `main` using the PR template.
5. Describe **what** changed and **why**.
6. A maintainer will review within a few days.
7. After approval and CI green, your PR will be merged. 🎉

---

## ✍️ Commit Message Guidelines

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:

```
feat(cli): add --workers option for multithreaded batch processing
fix(upscale): handle BGRA images without alpha channel strip
docs(readme): add wheel build & install instructions
```

---

Thank you again for contributing — your effort is genuinely appreciated! 🌟
