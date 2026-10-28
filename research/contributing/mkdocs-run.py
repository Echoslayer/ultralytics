# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mkdocs>=1.6",
#   "mkdocs-material>=9.5",
#   "pymdown-extensions>=10.0",
#   "jieba>=0.42.1",
# ]
# ///
"""uv script wrapper for mkdocs: `uv run mkdocs-run.py build -f configs/x.yml`.
Keeps deps in an ephemeral uv-managed env (no project .venv/)."""
from mkdocs.__main__ import cli

if __name__ == "__main__":
    cli()
