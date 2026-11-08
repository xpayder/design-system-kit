#!/usr/bin/env bash
# Locale key-parity check.
#  - As a PostToolUse hook: reads the edited file path from stdin JSON; checks only if it is a locale file.
#  - With --all: scans the project for every locale set (used by /ds-verify).
# Supports Android res/values*/strings.xml and JSON message files
# (locales|messages|i18n|lang|translations/<code>.json or .../<code>/<namespace>.json).
# A project's own scripts/validate_strings.py takes precedence.
root="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$root" || exit 0

if [ "$1" = "--all" ]; then
  target="--all"
else
  target=$(python3 -c 'import sys,json
try: print((json.load(sys.stdin).get("tool_input") or {}).get("file_path") or "")
except Exception: pass' 2>/dev/null)
  case "$target" in
    */res/values*/strings.xml|*/locales/*.json|*/messages/*.json|*/i18n/*.json|*/lang/*.json|*/translations/*.json) ;;
    *) exit 0 ;;
  esac
  case "$target" in
    */strings.xml)
      if [ -f scripts/validate_strings.py ]; then
        out=$(python3 scripts/validate_strings.py 2>&1) || { echo "Locale parity failed after editing $target:" >&2; echo "$out" | tail -25 >&2; exit 2; }
        exit 0
      fi ;;
  esac
fi

python3 - "$target" <<'PYEOF' >&2 || exit 2
import sys, os, glob, json, re
import xml.etree.ElementTree as ET

target = sys.argv[1]
SKIP = {"node_modules", ".git", "build", "dist", ".next", ".gradle", "Pods", ".venv", "out"}
LOCALE = re.compile(r"^[a-z]{2,3}([-_][A-Za-z0-9]{2,8})*$")
problems = []

def xml_keys(p):
    root = ET.parse(p).getroot()
    return {f"{el.tag}:{el.get('name')}" for el in root if el.tag in ("string", "plurals", "string-array")}

def json_keys(p, prefix=""):
    def walk(o, pre):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from walk(v, f"{pre}.{k}" if pre else k)
        else:
            yield pre
    with open(p, encoding="utf-8") as f:
        return set(walk(json.load(f), prefix))

def compare(group, loader, label):
    # group: {locale_code: path}; base = en if present, else the largest
    keys = {}
    for code, p in group.items():
        try:
            keys[code] = loader(p)
        except Exception as e:
            problems.append(f"[unparsable] {p}: {e}")
    if len(keys) < 2:
        return
    base = "en" if "en" in keys else ("" if "" in keys else max(keys, key=lambda c: len(keys[c])))
    for code, k in keys.items():
        if code == base:
            continue
        missing, extra = keys[base] - k, k - keys[base]
        if missing or extra:
            problems.append(f"{group[code]} vs {group[base]} ({label}): missing={sorted(missing)[:8]}{'…' if len(missing)>8 else ''} extra={sorted(extra)[:8]}{'…' if len(extra)>8 else ''}")

def android_group(res_dir):
    g = {}
    for p in glob.glob(os.path.join(res_dir, "values*", "strings.xml")):
        q = os.path.basename(os.path.dirname(p))[len("values"):].lstrip("-")
        if q == "" or re.match(r"^[a-z]{2,3}(-r[A-Z]{2})?$|^b\+", q):
            g[q] = p
    return g

def json_group(path):
    d, name = os.path.split(path)
    stem = name[:-5]
    if LOCALE.match(stem):                      # locales/en.json
        return {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(d, "*.json")) if LOCALE.match(os.path.basename(p)[:-5])}, stem
    parent = os.path.dirname(d)                 # locales/en/common.json
    if LOCALE.match(os.path.basename(d)):
        return {os.path.basename(os.path.dirname(p)): p for p in glob.glob(os.path.join(parent, "*", name)) if LOCALE.match(os.path.basename(os.path.dirname(p)))}, name
    return {}, None

if target == "--all":
    seen = set()
    for dp, dns, fns in os.walk("."):
        dns[:] = [x for x in dns if x not in SKIP]
        if os.path.basename(dp) == "res" and os.path.isfile(os.path.join(dp, "values", "strings.xml")):
            compare(android_group(dp), xml_keys, "android strings")
        if os.path.basename(dp) in ("locales", "messages", "i18n", "lang", "translations") or os.path.basename(os.path.dirname(dp)) in ("locales", "messages", "i18n", "lang", "translations"):
            for fn in fns:
                if fn.endswith(".json"):
                    g, label = json_group(os.path.join(dp, fn))
                    sig = tuple(sorted(g.values()))
                    if len(g) > 1 and sig not in seen:
                        seen.add(sig)
                        compare(g, json_keys, f"json {label}")
elif target.endswith("strings.xml"):
    compare(android_group(os.path.dirname(os.path.dirname(target))), xml_keys, "android strings")
else:
    g, label = json_group(target)
    compare(g, json_keys, f"json {label}")

if problems:
    print("Locale parity check failed:")
    for p in problems[:30]:
        print("  " + p)
    sys.exit(1)
PYEOF
exit 0
