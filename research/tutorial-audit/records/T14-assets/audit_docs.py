"""Static audit of docs code blocks against the live package. Prints observations only."""

import ast
import importlib
import re
import shlex
import sys
from collections import defaultdict
from pathlib import Path

root = Path(sys.argv[1])
from ultralytics.cfg import CFG_BOOL_KEYS, CFG_FLOAT_KEYS, CFG_FRACTION_KEYS, CFG_INT_KEYS, DEFAULT_CFG_DICT, MODES, TASKS

KEYS = set(DEFAULT_CFG_DICT) | set(CFG_BOOL_KEYS) | set(CFG_FLOAT_KEYS) | set(CFG_FRACTION_KEYS) | set(CFG_INT_KEYS)
EXTRA = {"cfg", "data", "model", "source", "tracker", "stream", "embed", "bboxes", "points", "labels", "masks", "texts", "prompts"}
CALLS = {"train", "val", "predict", "track", "export", "benchmark"}
SKIP = ("reference/", "compare/", "platform/")

fence = re.compile(r"^([ \t]*)```(\w+)[^\n]*\n(.*?)^\1```", re.S | re.M)
imports, kwargs, clis, syntax = defaultdict(list), defaultdict(list), defaultdict(list), []
files = [p for d in ("docs/en", "docs/macros") for p in (root / d).rglob("*.md")]
for p in files:
    rel = p.relative_to(root).as_posix()
    if any(s in rel for s in SKIP):
        continue
    text = p.read_text(encoding="utf-8")
    for m in fence.finditer(text):
        indent, lang, body = m.groups()
        line = text[: m.start()].count("\n") + 1
        import textwrap; body = textwrap.dedent(body)
        if lang in {"python", "py"}:
            try:
                tree = ast.parse(body)
            except SyntaxError as e:
                syntax.append(f"{rel}:{line + (e.lineno or 0)} {e.msg}")
                continue
            for n in ast.walk(tree):
                if isinstance(n, ast.ImportFrom) and n.module and n.module.split(".")[0] == "ultralytics":
                    for a in n.names:
                        imports[(n.module, a.name)].append(f"{rel}:{line + n.lineno}")
                elif isinstance(n, ast.Import):
                    for a in n.names:
                        if a.name.split(".")[0] == "ultralytics" and a.name != "ultralytics":
                            imports[(a.name, None)].append(f"{rel}:{line + n.lineno}")
                elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in CALLS:
                    base = ast.unparse(n.func.value)
                    if "model" not in base.lower() and base not in {"yolo"}:
                        continue
                    for k in n.keywords:
                        if k.arg and k.arg not in KEYS | EXTRA:
                            kwargs[(n.func.attr, k.arg)].append(f"{rel}:{line + n.lineno}")
        elif lang in {"bash", "sh", "shell"}:
            for i, raw in enumerate(body.replace("\\\n", " ").splitlines()):
                s = raw.strip()
                if not s.startswith("yolo "):
                    continue
                try:
                    toks = shlex.split(s, comments=True)[1:]
                except ValueError:
                    continue
                for t in toks:
                    if "=" in t:
                        k = t.split("=", 1)[0].lstrip("-")
                        if k not in KEYS | EXTRA:
                            clis[k].append(f"{rel}:{line + i + 1}")
                    elif t not in set(TASKS) | set(MODES) | {"help", "checks", "version", "settings", "cfg", "copy-cfg", "solutions", "explorer", "login", "logout", "hub", "install", "copy", "reset", "streamlit-predict", "analytics"}:
                        clis[f"[token] {t}"].append(f"{rel}:{line + i + 1}")

print("== syntax errors in python fences")
print(*syntax, sep="\n")
print("\n== unresolved imports")
for (mod, name), where in sorted(imports.items(), key=str):
    try:
        m = importlib.import_module(mod)
        if name and name != "*" and not hasattr(m, name):
            importlib.import_module(f"{mod}.{name}")
    except Exception as e:
        print(f"{mod} :: {name}  {type(e).__name__}: {str(e)[:90]}  x{len(where)} {where[:3]}")
print("\n== unknown kwargs on mode calls")
for (c, k), where in sorted(kwargs.items()):
    print(f"{c}({k}=)  x{len(where)} {where[:3]}")
print("\n== unknown CLI tokens/keys")
for k, where in sorted(clis.items()):
    print(f"{k}  x{len(where)} {where[:3]}")
print(f"\nimports checked: {len(imports)}")
