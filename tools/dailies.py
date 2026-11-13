"""Freeze Daily Bookle puzzles into dailies.js.

Every Daily is generated once and then stored as data, so later changes to
the generator, titles or wish lines can never change a puzzle people played.

  python tools/dailies.py extend --to 500   # append missing days up to #500
  python tools/dailies.py check             # fail if a committed day changed

The file is append-only: `extend` only adds day numbers that are not in it
yet, and `check` compares every day against the last commit (git HEAD).
Generation runs the real game in headless Edge/Chrome (index.html?export=A-B).
"""
import argparse, html, json, os, re, shutil, socket, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(ROOT, "dailies.js")
HEAD = ("// Frozen Daily Bookle puzzles, one per line. APPEND-ONLY: never edit or regenerate\n"
        "// an existing day. Add days with: python tools/dailies.py extend --to N\n"
        "window.BOOKLE_DAILIES={\n")
LINE = re.compile(r'^"(\d+)":(\{.*\}),?$')


def parse(text):
    days = {}
    for ln in text.splitlines():
        m = LINE.match(ln.strip())
        if m:
            days[int(m.group(1))] = json.loads(m.group(2))
    return days


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, encoding="utf-8") as f:
        return parse(f.read())


def dump(days):
    rows = [f'"{n}":{json.dumps(days[n], ensure_ascii=False, separators=(",", ":"))}' for n in sorted(days)]
    with open(FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(HEAD + ",\n".join(rows) + "\n};\n")


def browser():
    for c in [os.environ.get("BOOKLE_BROWSER"),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              shutil.which("chromium"), shutil.which("google-chrome"), shutil.which("msedge")]:
        if c and os.path.exists(c):
            return c
    sys.exit("No Edge/Chrome found. Set BOOKLE_BROWSER to a Chromium browser.")


def render(a, b):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", ROOT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        out = subprocess.run([browser(), "--headless=new", "--disable-gpu", "--virtual-time-budget=20000", "--dump-dom",
                              f"http://127.0.0.1:{port}/index.html?export={a}-{b}"],
                             capture_output=True, text=True, encoding="utf-8", timeout=300).stdout
    finally:
        srv.terminate()
    m = re.search(r'<pre id="bookle-export">(.*?)</pre>', out, re.S)
    if not m:
        sys.exit("Export failed: the page did not produce puzzles.")
    return {int(k): v for k, v in json.loads(html.unescape(m.group(1))).items()}


def extend(to):
    days = load()
    start = max(days, default=0) + 1
    if start > to:
        print(f"Nothing to do: days 1-{start - 1} are already frozen."); return
    new = render(start, to)
    for n, p in new.items():
        if n not in days:          # never overwrite a frozen day
            days[n] = p
    dump(days)
    print(f"Froze days {start}-{to}. dailies.js now holds 1-{max(days)}.")


def check():
    try:
        old = subprocess.run(["git", "show", "HEAD:dailies.js"], cwd=ROOT, capture_output=True,
                             text=True, encoding="utf-8", check=True).stdout
    except subprocess.CalledProcessError:
        print("No committed dailies.js yet, nothing to compare."); return
    before, now = parse(old), load()
    bad = [n for n in before if now.get(n) != before[n]]
    gaps = [n for n in range(1, max(now, default=0) + 1) if n not in now]
    if bad or gaps:
        sys.exit(f"dailies.js broke the append-only rule. Changed/removed: {bad[:20]} Missing: {gaps[:20]}")
    print(f"OK: all {len(before)} committed days unchanged, {len(now) - len(before)} new.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extend"); e.add_argument("--to", type=int, required=True)
    sub.add_parser("check")
    a = ap.parse_args()
    extend(a.to) if a.cmd == "extend" else check()
