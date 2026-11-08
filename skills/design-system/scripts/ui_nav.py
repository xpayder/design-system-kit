#!/usr/bin/env python3
"""
ui_nav.py — accessibility-tree driven Android navigation, no coordinates, no LLM.

This is the one idea worth keeping from evaluating github.com/google/artemis for this project:
locate elements by what they ARE (text / content-desc / resource-id), not by where they happen
to sit in a screenshot. A hand-measured pixel coordinate breaks the moment a screen's layout
changes or a screenshot gets scaled (we hit this class of bug repeatedly: half-resolution
screenshots tapped at full-resolution coordinates, spacing changes shifting a button a few
dp). Reading `adb shell uiautomator dump` and tapping the centre of a matched node's `bounds`
sidesteps all of that — it is exactly the mechanism Artemis's "perception" layer uses
(accessibility hierarchy first, OCR/vision only as a fallback), minus the hosted LLM planner,
the Angular console, and the paid Gemini/OpenAI key Artemis's own CLI requires to run at all.

No third-party dependencies beyond the Python standard library and a connected `adb`.

Usage:
  ui_nav.py devices
  ui_nav.py dump [--serial S]                          # raw XML to stdout
  ui_nav.py find QUERY [--serial S] [--role text|desc|id|any] [--index N]
  ui_nav.py tap QUERY [--serial S] [--role ...] [--index N] [--long]
  ui_nav.py tap-xy X Y [--serial S]
  ui_nav.py type TEXT [--serial S]
  ui_nav.py key KEYCODE [--serial S]                    # e.g. back, home, enter, 4, 3, 66
  ui_nav.py swipe X1 Y1 X2 Y2 [--serial S] [--duration-ms 300]
  ui_nav.py scroll-to QUERY [--serial S] [--role ...] [--max-swipes 8] [--tap]
  ui_nav.py wait-for QUERY [--serial S] [--role ...] [--timeout 10]
  ui_nav.py wait-idle [--serial S] [--timeout 8] [--quiet-ms 600]
  ui_nav.py screenshot PATH [--serial S]                # always native resolution, no scaling

QUERY matching: case-insensitive substring by default. Prefix with `=` for an exact match
(`=OK` matches the node whose text/content-desc is exactly "OK", not every node containing it —
use this whenever a short label like "OK" or a locale's "Да" would otherwise match a dozen
unrelated nodes).

--role restricts which attribute QUERY is matched against: text (visible label), desc
(content-description, including icon-only buttons), id (resource-id suffix), or any (default:
text OR desc).

Exit codes: 0 success, 2 no element matched, 3 adb/device error, 4 ambiguous match the caller
should disambiguate (use --index or a longer QUERY).
"""
import argparse
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

BOUNDS_RE = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")

KEYCODES = {
    "back": "4", "home": "3", "enter": "66", "tab": "61",
    "up": "19", "down": "20", "left": "21", "right": "22",
    "del": "67", "backspace": "67", "appswitch": "187",
}


def adb(serial, *args, capture=True, check=True):
    cmd = ["adb"] + (["-s", serial] if serial else []) + list(args)
    return subprocess.run(cmd, capture_output=capture, text=True, check=check)


def get_serial(explicit):
    if explicit:
        return explicit
    out = subprocess.run(["adb", "devices"], capture_output=True, text=True).stdout
    lines = [l.split("\t")[0] for l in out.splitlines()[1:] if l.strip().endswith("\tdevice")]
    if not lines:
        print("no adb device attached (or device unauthorized/offline)", file=sys.stderr)
        sys.exit(3)
    if len(lines) > 1:
        print(f"multiple devices attached ({', '.join(lines)}); pass --serial", file=sys.stderr)
        sys.exit(3)
    return lines[0]


def dump_xml(serial):
    # /dev/tty avoids a world-writable /sdcard file and an extra pull round-trip.
    r = subprocess.run(
        ["adb"] + (["-s", serial] if serial else []) + ["exec-out", "uiautomator", "dump", "/dev/tty"],
        capture_output=True, text=True,
    )
    xml_text = r.stdout
    start = xml_text.find("<?xml")
    if start < 0:
        print("uiautomator dump returned no XML (screen off? keyguard up? app ANR?)", file=sys.stderr)
        print(r.stdout[-500:] + r.stderr[-500:], file=sys.stderr)
        sys.exit(3)
    end = xml_text.rfind(">") + 1
    return xml_text[start:end]


def iter_nodes(xml_text):
    root = ET.fromstring(xml_text)
    for node in root.iter("node"):
        yield node.attrib


def center_of(bounds_str):
    m = BOUNDS_RE.match(bounds_str)
    if not m:
        return None
    x1, y1, x2, y2 = map(int, m.groups())
    return (x1 + x2) // 2, (y1 + y2) // 2, (x1, y1, x2, y2)


def matches(attrib, query, role):
    text = attrib.get("text", "")
    desc = attrib.get("content-desc", "")
    rid = attrib.get("resource-id", "")
    exact = query.startswith("=")
    q = query[1:] if exact else query
    qlow = q.lower()

    def hit(field):
        return (field == q) if exact else (qlow in field.lower())

    if role == "text":
        return hit(text)
    if role == "desc":
        return hit(desc)
    if role == "id":
        return q.lower() in rid.lower()
    return hit(text) or hit(desc)


def find_matches(xml_text, query, role, clickable_only=True):
    out = []
    for attrib in iter_nodes(xml_text):
        if not matches(attrib, query, role):
            continue
        b = attrib.get("bounds", "")
        c = center_of(b)
        if not c:
            continue
        cx, cy, rect = c
        if rect[2] <= rect[0] or rect[3] <= rect[1]:
            continue  # zero-area node (off-screen / collapsed) — never a real tap target
        out.append({
            "text": attrib.get("text", ""),
            "desc": attrib.get("content-desc", ""),
            "resource-id": attrib.get("resource-id", ""),
            "class": attrib.get("class", ""),
            "clickable": attrib.get("clickable", "false") == "true",
            "enabled": attrib.get("enabled", "true") == "true",
            "x": cx, "y": cy, "bounds": rect,
        })
    if clickable_only and any(m["clickable"] for m in out):
        out = [m for m in out if m["clickable"]]
    return out


def pick(matches_, index):
    if not matches_:
        return None, "no element matched"
    if index is not None:
        if index >= len(matches_):
            return None, f"--index {index} out of range ({len(matches_)} match(es))"
        return matches_[index], None
    if len(matches_) > 1:
        # Prefer the smallest matching node (an icon button over its containing row/card).
        matches_ = sorted(matches_, key=lambda m: (m["bounds"][2]-m["bounds"][0])*(m["bounds"][3]-m["bounds"][1]))
        smallest_area = (matches_[0]["bounds"][2]-matches_[0]["bounds"][0])*(matches_[0]["bounds"][3]-matches_[0]["bounds"][1])
        tied = [m for m in matches_ if (m["bounds"][2]-m["bounds"][0])*(m["bounds"][3]-m["bounds"][1]) == smallest_area]
        if len(tied) == 1:
            return tied[0], None
        return None, f"{len(matches_)} elements matched ambiguously; pass --index or a longer/=-exact query"
    return matches_[0], None


def cmd_devices(_args):
    out = subprocess.run(["adb", "devices", "-l"], capture_output=True, text=True).stdout
    print(out.strip())


def cmd_dump(args):
    serial = get_serial(args.serial)
    print(dump_xml(serial))


def cmd_find(args):
    serial = get_serial(args.serial)
    xml_text = dump_xml(serial)
    ms = find_matches(xml_text, args.query, args.role, clickable_only=False)
    if not ms:
        print(f"no element matched {args.query!r} (role={args.role})", file=sys.stderr)
        sys.exit(2)
    for i, m in enumerate(ms):
        tag = "CLICK" if m["clickable"] else "     "
        dis = "" if m["enabled"] else " DISABLED"
        print(f"[{i}] {tag}{dis} ({m['x']},{m['y']}) text={m['text']!r} desc={m['desc']!r} id={m['resource-id']!r} class={m['class']}")


def cmd_tap(args):
    serial = get_serial(args.serial)
    xml_text = dump_xml(serial)
    ms = find_matches(xml_text, args.query, args.role)
    target, err = pick(ms, args.index)
    if err:
        print(err, file=sys.stderr)
        all_ms = find_matches(xml_text, args.query, args.role, clickable_only=False)
        for i, m in enumerate(all_ms):
            print(f"  [{i}] ({m['x']},{m['y']}) text={m['text']!r} desc={m['desc']!r} id={m['resource-id']!r}", file=sys.stderr)
        sys.exit(2 if "no element" in err else 4)
    if not target["enabled"]:
        print(f"matched element is disabled: text={target['text']!r} desc={target['desc']!r}", file=sys.stderr)
        sys.exit(2)
    if args.long:
        x, y = target["x"], target["y"]
        adb(serial, "shell", "input", "swipe", str(x), str(y), str(x), str(y), "700")
    else:
        adb(serial, "shell", "input", "tap", str(target["x"]), str(target["y"]))
    print(f"tapped {target['text'] or target['desc'] or target['resource-id']} at ({target['x']},{target['y']})")


def cmd_tap_xy(args):
    serial = get_serial(args.serial)
    adb(serial, "shell", "input", "tap", str(args.x), str(args.y))
    print(f"tapped ({args.x},{args.y}) — raw coordinate, prefer `tap QUERY` when the element has text/desc")


def cmd_type(args):
    serial = get_serial(args.serial)
    # adb's shell input text needs spaces escaped; %s keeps it simple and handles unicode fine on API 24+.
    escaped = args.text.replace(" ", "%s")
    adb(serial, "shell", "input", "text", escaped)
    print(f"typed {args.text!r}")


def cmd_key(args):
    serial = get_serial(args.serial)
    code = KEYCODES.get(args.keycode.lower(), args.keycode)
    adb(serial, "shell", "input", "keyevent", code)
    print(f"sent keyevent {code}")


def cmd_swipe(args):
    serial = get_serial(args.serial)
    adb(serial, "shell", "input", "swipe", str(args.x1), str(args.y1), str(args.x2), str(args.y2), str(args.duration_ms))
    print(f"swiped ({args.x1},{args.y1}) -> ({args.x2},{args.y2})")


def cmd_scroll_to(args):
    serial = get_serial(args.serial)
    for attempt in range(args.max_swipes + 1):
        xml_text = dump_xml(serial)
        ms = find_matches(xml_text, args.query, args.role, clickable_only=False)
        if ms:
            if args.tap:
                target, err = pick(ms, args.index)
                if err:
                    print(err, file=sys.stderr)
                    sys.exit(4)
                adb(serial, "shell", "input", "tap", str(target["x"]), str(target["y"]))
                print(f"found after {attempt} swipe(s), tapped at ({target['x']},{target['y']})")
            else:
                print(f"found after {attempt} swipe(s): {ms[0]['text'] or ms[0]['desc']}")
            return
        if attempt == args.max_swipes:
            break
        # swipe over the middle 60% of the screen height so we don't catch a status bar or a floating dock
        wh = adb(serial, "shell", "wm", "size").stdout.strip()
        w, h = 1080, 2340
        m = re.search(r"(\d+)x(\d+)", wh)
        if m:
            w, h = int(m.group(1)), int(m.group(2))
        y1, y2 = int(h * 0.75), int(h * 0.3)
        adb(serial, "shell", "input", "swipe", str(w // 2), str(y1), str(w // 2), str(y2), "300")
        time.sleep(0.6)
    print(f"'{args.query}' not found after {args.max_swipes} swipe(s)", file=sys.stderr)
    sys.exit(2)


def cmd_wait_for(args):
    serial = get_serial(args.serial)
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        xml_text = dump_xml(serial)
        ms = find_matches(xml_text, args.query, args.role, clickable_only=False)
        if ms:
            print(f"appeared: {ms[0]['text'] or ms[0]['desc']} at ({ms[0]['x']},{ms[0]['y']})")
            return
        time.sleep(0.4)
    print(f"timed out after {args.timeout}s waiting for {args.query!r}", file=sys.stderr)
    sys.exit(2)


def cmd_wait_idle(args):
    """Poll the hierarchy until two consecutive dumps are identical for --quiet-ms — i.e. an
    animation/transition/network load has settled. Cheaper and more reliable than a fixed sleep,
    and it is what lets a navigation script survive a glass-crossfade whose duration changes."""
    serial = get_serial(args.serial)
    deadline = time.time() + args.timeout
    last, last_change = None, time.time()
    while time.time() < deadline:
        cur = dump_xml(serial)
        if cur != last:
            last, last_change = cur, time.time()
        elif (time.time() - last_change) * 1000 >= args.quiet_ms:
            print(f"idle after {time.time() - deadline + args.timeout:.1f}s")
            return
        time.sleep(0.25)
    print(f"did not settle within {args.timeout}s (still animating or polling itself)", file=sys.stderr)
    sys.exit(2)


def cmd_screenshot(args):
    serial = get_serial(args.serial)
    r = subprocess.run(
        ["adb"] + (["-s", serial] if serial else []) + ["exec-out", "screencap", "-p"],
        capture_output=True, check=True,
    )
    with open(args.path, "wb") as f:
        f.write(r.stdout)
    print(f"saved native-resolution screenshot to {args.path}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp):
        sp.add_argument("--serial", default=None)

    sp = sub.add_parser("devices"); sp.set_defaults(func=cmd_devices)

    sp = sub.add_parser("dump"); add_common(sp); sp.set_defaults(func=cmd_dump)

    sp = sub.add_parser("find"); add_common(sp)
    sp.add_argument("query"); sp.add_argument("--role", choices=["text", "desc", "id", "any"], default="any")
    sp.set_defaults(func=cmd_find)

    sp = sub.add_parser("tap"); add_common(sp)
    sp.add_argument("query"); sp.add_argument("--role", choices=["text", "desc", "id", "any"], default="any")
    sp.add_argument("--index", type=int, default=None)
    sp.add_argument("--long", action="store_true", help="long-press instead of a tap")
    sp.set_defaults(func=cmd_tap)

    sp = sub.add_parser("tap-xy"); add_common(sp)
    sp.add_argument("x", type=int); sp.add_argument("y", type=int)
    sp.set_defaults(func=cmd_tap_xy)

    sp = sub.add_parser("type"); add_common(sp)
    sp.add_argument("text"); sp.set_defaults(func=cmd_type)

    sp = sub.add_parser("key"); add_common(sp)
    sp.add_argument("keycode"); sp.set_defaults(func=cmd_key)

    sp = sub.add_parser("swipe"); add_common(sp)
    sp.add_argument("x1", type=int); sp.add_argument("y1", type=int)
    sp.add_argument("x2", type=int); sp.add_argument("y2", type=int)
    sp.add_argument("--duration-ms", type=int, default=300)
    sp.set_defaults(func=cmd_swipe)

    sp = sub.add_parser("scroll-to"); add_common(sp)
    sp.add_argument("query"); sp.add_argument("--role", choices=["text", "desc", "id", "any"], default="any")
    sp.add_argument("--max-swipes", type=int, default=8)
    sp.add_argument("--index", type=int, default=None)
    sp.add_argument("--tap", action="store_true")
    sp.set_defaults(func=cmd_scroll_to)

    sp = sub.add_parser("wait-for"); add_common(sp)
    sp.add_argument("query"); sp.add_argument("--role", choices=["text", "desc", "id", "any"], default="any")
    sp.add_argument("--timeout", type=float, default=10)
    sp.set_defaults(func=cmd_wait_for)

    sp = sub.add_parser("wait-idle"); add_common(sp)
    sp.add_argument("--timeout", type=float, default=8)
    sp.add_argument("--quiet-ms", type=int, default=600)
    sp.set_defaults(func=cmd_wait_idle)

    sp = sub.add_parser("screenshot"); add_common(sp)
    sp.add_argument("path"); sp.set_defaults(func=cmd_screenshot)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
