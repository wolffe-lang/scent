#!/usr/bin/env python3
# Adapted from wolffe-lang/aspen 476edee3 ci/tiers-test.py; own code.
"""ci/tiers-test.py — the planner's own proof (wolf-lang's tl21 test, as
lope cut it, cut again to scent's workflow). python3 only.

  T1  the tiers by event: a trunk push, the nightly, a dispatch with no
      jobs and the `full-matrix` label are full; another label's
      `labeled` event is a noop; a dispatch naming jobs is partial, and
      refuses a job the workflow does not have.
  T2  the pull-request tiers by path: code is pr (linux, plan-test);
      prose alone is noop; prose beside code is pr.
  T3  full wins: a path no rule names; changed paths that cannot be read.
  T4  the wiring of .github/workflows/ci.yml: every job but `plan` needs
      it and runs only when the plan names it; `tier` needs every job,
      runs on `!cancelled()` and calls the verdict; cancel-in-progress is
      for pull requests only; the trunk push, the nightly, the label and
      the dispatch input are there; macos is no pull-request job.
  T6  the verdict: green for a full, a pr, a noop and a partial run; red
      for a chosen job failed or skipped, a job that ran unasked, a failed
      plan, a plan with no tier, a full that chose less.
  T8  ci/nightly-red.sh against a stand-in `gh` (boreutils' T8): no open
      issue opens one; an open one is commented on; a label that exists is
      no failure; the script refuses without its environment; the
      nightly-red job runs on a failed schedule only, after the verdict.
  T9  the plain rule for current text: no file outside notes/ names a
      ruling, by number or by tag.
  T10 one version: the binary's --version line, the newest CHANGELOG
      section and both packaging recipes name the same release.
  T11 tools/field-report over the macOS field leg's five ends: completed,
      cut at the step's limit, a stale review, an early end without a
      summary, and a leg that never started; and a summary older than the
      leg's start, which is not the leg's and reads as no summary.

Exit 0 when every check passes, 1 otherwise.
"""
import json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "ci", "tiers.py")
WF = open(os.path.join(ROOT, ".github", "workflows", "ci.yml"), encoding="utf-8").read()
KEYS = ("EVENT", "ACTION", "LABEL", "LABELS", "HEAD_SHA", "IN_JOBS", "NEEDS")
fails = 0
ALL = ["plan-test", "linux", "macos"]
PR = ["plan-test", "linux"]


def say(ok, what):
    global fails
    print("tiers-test: %s %s" % ("PASS" if ok else "FAIL", what))
    fails += not ok


def env(**more):
    e = {k: v for k, v in os.environ.items() if k not in KEYS}
    e.update(more)
    return e


def plan(paths=None, **kw):
    args = [sys.executable, PLAN, "plan", "--json"]
    for k, v in kw.items():
        args += ["--" + k.replace("_", "-"), v]
    if paths is not None:
        args += ["--paths-from", "-"]
    r = subprocess.run(args, input="\n".join(paths or []) + "\n", capture_output=True, text=True, env=env())
    if r.returncode != 0:
        return {"tier": "ERROR %d" % r.returncode, "jobs": []}
    return json.loads(r.stdout)


def verdict(needs):
    r = subprocess.run([sys.executable, PLAN, "verdict"], capture_output=True, text=True,
                       env=env(NEEDS=json.dumps(needs)))
    return r.returncode


def needs_for(tier, chosen, results=None):
    n = {"plan": {"result": "success", "outputs": {"tier": tier, "jobs": json.dumps(chosen)}}}
    for j in ALL:
        n[j] = {"result": (results or {}).get(j, "success" if j in chosen else "skipped")}
    return n


# T1
for ev in ("push", "schedule", "workflow_dispatch"):
    p = plan(event=ev)
    say(p["tier"] == "full" and p["jobs"] == ALL, "T1 %s is full" % ev)
p = plan(["src/scent.lu"], event="pull_request", action="labeled", label="full-matrix", labels="full-matrix")
say(p["tier"] == "full" and p["jobs"] == ALL, "T1 the full-matrix label is full")
p = plan(["src/scent.lu"], event="pull_request", action="labeled", label="docs", labels="docs")
say(p["tier"] == "noop" and p["jobs"] == [], "T1 another label is a noop")
p = plan(event="workflow_dispatch", jobs="linux")
say(p["tier"] == "partial" and p["jobs"] == ["linux"], "T1 a dispatch naming linux is partial")
p = plan(event="workflow_dispatch", jobs="windows")
say(p["tier"].startswith("ERROR"), "T1 a dispatch naming no job of the workflow is refused")
# T2
p = plan(["src/walk/walk.lu", "tests/oracle/sets.tsv"], event="pull_request", action="synchronize")
say(p["tier"] == "pr" and p["jobs"] == PR, "T2 code is pr")
p = plan(["README.md", "notes/ap00-the-first-light.md", "CHANGELOG.md", "docs/MAP.md"], event="pull_request", action="opened")
say(p["tier"] == "noop", "T2 prose alone is a noop")
p = plan(["README.md", "src/scent.lu"], event="pull_request", action="opened")
say(p["tier"] == "pr", "T2 prose beside code is pr")
# T3
p = plan(["somewhere/new"], event="pull_request", action="opened")
say(p["tier"] == "full", "T3 a path no rule names is full")
r = subprocess.run([sys.executable, PLAN, "plan", "--json", "--event", "pull_request", "--action", "opened"],
                   capture_output=True, text=True, env=env())
say(json.loads(r.stdout)["tier"] == "full", "T3 unreadable paths are full")
# T4
jobs = re.findall(r"^  ([a-z-]+):\s*$", WF.split("\njobs:\n", 1)[1], re.M)
say(jobs == ["plan", "plan-test", "linux", "macos", "tier", "nightly-red"], "T4 the jobs, in order: %s" % jobs)
for j in ALL:
    blk = WF.split("\n  %s:\n" % j, 1)[1].split("\n  ", 1)[0] + WF.split("\n  %s:\n" % j, 1)[1].split("\n\n  ", 1)[0]
    say("needs: plan" in blk and "contains(fromJSON(needs.plan.outputs.jobs || '[]'), '%s')" % j in blk,
        "T4 %s needs the plan and runs only when it is named" % j)
tblk = WF.split("\n  tier:\n", 1)[1]
say(all("- %s" % j in tblk for j in ["plan"] + ALL) and "!cancelled()" in tblk and "ci/tiers.py verdict" in tblk,
    "T4 tier needs every job, runs unless cancelled, checks the verdict")
say("cancel-in-progress: ${{ github.event_name == 'pull_request' }}" in WF, "T4 cancel-in-progress for pull requests only")
say("branches: [trunk]" in WF and "schedule:" in WF and "labeled" in WF and "inputs:" in WF,
    "T4 the trunk push, the nightly, the label and the dispatch input")
# T4, the macOS field leg cannot fail a run by its length. Its step has its own limit
# under the job's and continues on error; the step after it always runs
# tools/field-report, which is the leg's verdict (a stale review, an early end or a leg
# that never started is red; a cut at the step's limit is reported, not red).
mblk = WF.split("\n  macos:\n", 1)[1].split("\n  tier:\n", 1)[0]
msteps = re.split(r"\n(?=      - )", mblk)
fi = next((i for i, t in enumerate(msteps) if "Distribution field leg" in t), None)
fstep = msteps[fi] if fi is not None else ""
rstep = msteps[fi + 1] if fi is not None and fi + 1 < len(msteps) else ""
wiring = [
    ("timeout-minutes: 40" in msteps[0], "the job's limit is 40"),
    ("id: field" in fstep, "the field step has id field"),
    ("timeout-minutes: 35" in fstep, "the field step's limit is 35"),
    ("continue-on-error: true" in fstep, "the field step continues on error"),
    ("date +%s > target/field-step-start" in fstep, "the field step writes its start first"),
    ("if: always()" in rstep and "python3 -I tools/field-report --limit-minutes 35" in rstep,
     "the next step always runs tools/field-report --limit-minutes 35"),
]
missing = [what for ok, what in wiring if not ok]
say(not missing, "T4 the macOS field leg's limits and its report%s" % (": missing " + "; ".join(missing) if missing else ""))
if missing:
    print("FAIL macos-field-wiring " + "; ".join(missing))  # by name, for a record's plant evidence
# T6
say(verdict(needs_for("full", ALL)) == 0, "T6 a green full")
say(verdict(needs_for("pr", PR)) == 0, "T6 a green pr")
say(verdict(needs_for("noop", [])) == 0, "T6 a green noop")
say(verdict(needs_for("partial", ["linux"])) == 0, "T6 a green partial")
say(verdict(needs_for("pr", PR, {"linux": "failure"})) == 1, "T6 a chosen job failed")
say(verdict(needs_for("pr", PR, {"linux": "skipped"})) == 1, "T6 a chosen job skipped")
say(verdict(needs_for("pr", PR, {"macos": "success"})) == 1, "T6 a job that ran unasked")
say(verdict(needs_for("full", PR)) == 1, "T6 a full that chose less")
n = needs_for("pr", PR)
n["plan"]["result"] = "failure"
say(verdict(n) == 1, "T6 a failed plan")
n = needs_for("pr", PR)
n["plan"]["outputs"]["tier"] = ""
say(verdict(n) == 1, "T6 a plan with no tier")
# T8
RED = os.path.join(ROOT, "ci", "nightly-red.sh")
WORKFLOW_NAME = "ci"
FAKE_GH = r"""#!/usr/bin/env bash
printf '%s\n' "$*" >> "$FAKE_LOG"
case "$1 $2" in
  "label create") exit "${FAKE_LABEL_RC:-0}" ;;
  "issue list") printf '%s' "${FAKE_EXISTING:-}"; [ -n "${FAKE_EXISTING:-}" ] && echo; exit 0 ;;
esac
exit 0
"""


def nightly_red(existing="", label_rc=0):
    d = tempfile.mkdtemp(prefix="tiers-test-gh-")
    try:
        with open(os.path.join(d, "gh"), "w") as f:
            f.write(FAKE_GH)
        os.chmod(os.path.join(d, "gh"), 0o755)
        log = os.path.join(d, "log")
        e = env(PATH=d + os.pathsep + os.environ.get("PATH", ""), FAKE_LOG=log, FAKE_EXISTING=existing,
                FAKE_LABEL_RC=str(label_rc), REPO="wolffe-lang/scent", WORKFLOW=WORKFLOW_NAME,
                RUN_URL="https://github.com/wolffe-lang/scent/actions/runs/1")
        r = subprocess.run(["bash", RED], capture_output=True, text=True, env=e)
        calls = open(log).read().splitlines() if os.path.exists(log) else []
        return r.returncode, calls
    finally:
        shutil.rmtree(d, ignore_errors=True)


TITLE = "nightly red: %s on trunk" % WORKFLOW_NAME
rc, calls = nightly_red()
creates = [c for c in calls if c.startswith("issue create")]
say(rc == 0 and len(creates) == 1 and "--title %s" % TITLE in creates[0] and "--label nightly-red" in creates[0]
    and not [c for c in calls if c.startswith("issue comment")],
    "T8 no open issue: one is opened, labelled nightly-red, titled '%s'" % TITLE)
rc, calls = nightly_red(existing="41")
say(rc == 0 and [c for c in calls if c.startswith("issue comment 41 ")] and not [c for c in calls if c.startswith("issue create")],
    "T8 an open issue: a comment on it, no new issue")
rc, calls = nightly_red(label_rc=1)
say(rc == 0 and [c for c in calls if c.startswith("issue create")], "T8 a label that already exists is no failure")
r = subprocess.run(["bash", RED], capture_output=True, text=True, env=env())
say(r.returncode != 0, "T8 the script refuses to run without REPO, WORKFLOW and RUN_URL")
say(re.search(r"^name: %s$" % re.escape(WORKFLOW_NAME), WF, re.M) is not None, "T8 the workflow's name is %s, the title's" % WORKFLOW_NAME)
nblk = WF.split("\n  nightly-red:\n", 1)[1]
say("needs: tier" in nblk and "failure() && github.event_name == 'schedule'" in nblk and "issues: write" in nblk
    and "ci/nightly-red.sh" in nblk, "T8 nightly-red runs after the verdict, on a red schedule only, may write issues")
# T8, what the reporter writes is public: the issue's title and body, a comment,
# the label's description. The plain rule holds in every run: no lane, ruling,
# crawl or sprint word and no internal tag (two letters and two or three digits). A
# local record also passes PUBLIC_TEXT_REFUSE, a file of further words kept outside
# this repository; a word from that file is reported by its line number, never spelt.
PLAIN = re.compile(r"\b(?:lanes?|rulings?|crawls?|sprints?)\b|\b[a-z]{2}\d{2,3}[a-z]?\b", re.I)
LISTED = []
if os.environ.get("PUBLIC_TEXT_REFUSE"):
    with open(os.environ["PUBLIC_TEXT_REFUSE"], encoding="utf-8") as fh:
        LISTED = [(n, re.compile(r"(?<![A-Za-z0-9_-])%s(?![A-Za-z0-9_-])" % re.escape(w.strip()), re.I))
                  for n, w in enumerate(fh, 1) if w.strip() and not w.startswith("#")]


def _log_lines(x):
    return x.splitlines() if isinstance(x, str) else list(x)


written = "\n".join(c for e in ("", "41") for c in _log_lines(nightly_red(existing=e)[1]) if not c.startswith("issue list"))
said = sorted({m.group(0) for m in PLAIN.finditer(written)}) + ["listed word %d" % n for n, rx in LISTED if rx.search(written)]
say(bool(written) and not said, "T8 nothing the reporter writes in public carries an internal word (%s)%s" % (
    "the plain rule and %d listed words" % len(LISTED) if LISTED else "the plain rule", ": " + ", ".join(said) if said else ""))

# T9, current text is public too: no file outside notes/ names a ruling, by number
# or by tag; each published difference is named by its rule in words. notes/ keeps
# the historical notes and the recorded evidence logs as they were recorded (their
# digests are cited), and build outputs and dot-directories are not the tree's text.
RULED = re.compile(r"(?<![A-Za-z])rulings?(?![A-Za-z])|(?<![A-Za-z0-9])R-[a-z]{2}\d{2}-\d+", re.I)
named = []
for top in sorted(os.listdir(ROOT)):
    if top in ("notes", "target") or (top.startswith(".") and top not in (".github", ".gitignore")):
        continue
    start = os.path.join(ROOT, top)
    paths = [start] if not os.path.isdir(start) else [
        os.path.join(d, f) for d, subdirs, files in os.walk(start)
        for f in files if "__pycache__" not in d.split(os.sep)]
    for path in sorted(paths):
        if os.path.abspath(path) == os.path.abspath(__file__):
            continue  # this check's own pattern
        try:
            with open(path, encoding="utf-8") as fh:
                count = len(RULED.findall(fh.read()))
        except (UnicodeDecodeError, OSError):
            continue
        if count:
            named.append("%s (%d)" % (os.path.relpath(path, ROOT), count))
say(not named, "T9 no current text outside notes/ names a ruling%s" % (": " + ", ".join(named) if named else ""))
for n in named:
    print("FAIL plain-rule " + n)  # by name, for a record's plant evidence

# T10, one version: what `scent --version` prints, the newest CHANGELOG section
# (`## Unreleased — X` while X is being made, `## X — YYYY-MM-DD` once tagged) and
# both packaging recipes name the same X.
def _read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


VERSION = r"(\d+\.\d+\.\d+)"
named = {}
m = re.search(r'print\("scent %s"\)' % VERSION, _read("src", "scent.lu"))
named["--version"] = m and m.group(1)
top = next((line for line in _read("CHANGELOG.md").splitlines() if line.startswith("## ")), "")
m = re.fullmatch(r"## (?:Unreleased — %s|%s — \d{4}-\d{2}-\d{2})" % (VERSION, VERSION), top)
named["CHANGELOG"] = m and (m.group(1) or m.group(2))
m = re.search(r"^pkgver=%s$" % VERSION, _read("packaging", "PKGBUILD"), re.M)
named["PKGBUILD"] = m and m.group(1)
m = re.search(r"/archive/refs/tags/v%s\.tar\.gz" % VERSION, _read("packaging", "scent.rb"))
named["scent.rb"] = m and m.group(1)
one = None not in named.values() and len(set(named.values())) == 1
listed = ", ".join("%s %s" % (k, v) for k, v in named.items())
say(one, "T10 one version: %s" % listed)
if not one:
    print("FAIL one-version " + listed)  # by name, for a record's plant evidence

# T11, tools/field-report over the field leg's five ends, each in its own directory: the
# start marker the field step writes first, and the oracle's own summary, written last.
FIELD_REPORT = os.path.join(ROOT, "tools", "field-report")


def field_end(started_min_ago, summary, summary_before_start=False):
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, "target", "oracle"))
    start = int(time.time() - (started_min_ago or 0) * 60)
    if started_min_ago is not None:
        with open(os.path.join(root, "target", "field-step-start"), "w") as fh:
            fh.write("%d\n" % start)
    if summary is not None:
        path = os.path.join(root, "target", "oracle", "summary.json")
        with open(path, "w") as fh:
            json.dump(summary, fh, sort_keys=True)
        if summary_before_start:  # left by something before the leg began
            os.utime(path, (start - 120, start - 120))
    try:
        if not os.path.isfile(FIELD_REPORT):
            return None, "tools/field-report is absent"
        r = subprocess.run([sys.executable, "-I", FIELD_REPORT, "--limit-minutes", "35", "--root", root],
                           capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()
    finally:
        shutil.rmtree(root)


counts = {"agree": 47000, "differ": 120, "reviewed": 2, "field-unavailable": 3, "stale-review": 0}
for name, ago, summary, old, want_rc, want in [
        ("completed", 22, counts, False, 0, "REPORT field leg: completed"),
        ("cut", 35.2, None, False, 0, "REPORT field leg: cut at 35 min"),
        ("stale", 22, dict(counts, **{"stale-review": 2}), False, 1, "FAIL field leg: 2 stale field review(s)"),
        ("early", 3, None, False, 1, "FAIL field leg: ended early without a summary after 3 min"),
        ("never-started", None, None, False, 1, "FAIL field leg: never started"),
        ("old-summary", 3, counts, True, 1, "FAIL field leg: ended early without a summary after 3 min")]:
    rc, out = field_end(ago, summary, old)
    ok = rc == want_rc and out.startswith(want)
    say(ok, "T11 field-report %s: exit %s, %s" % (name, rc, out.splitlines()[0] if out else "no output"))
    if not ok:
        print("FAIL field-report-%s want exit %d and %r" % (name, want_rc, want))  # by name, for a plant

print("tiers-test: %s" % ("every check passes" if not fails else "%d check(s) FAILED" % fails))
sys.exit(1 if fails else 0)
