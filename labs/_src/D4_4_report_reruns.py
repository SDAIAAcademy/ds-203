# %% [markdown]
# # Lab 4.4 · A report that reruns
#
# Day 4 · Session 4 (The exploratory report) · 25 min.
#
# A draft of the note for the director exists: `report/board_note.py`. It is a report written as code, so every number in it is computed when it is rendered. That is the promise; the draft breaks it in three ways. You render it twice and compare, repair it until two runs agree and the numbers come from the raw data, check its table of findings, and then choose the dataset of your capstone.
#
# **AI policy.** The tutor may hint at syntax. Checking the findings table and writing your capstone questions are your own work, assistant off.
#
# **Reference state.** `report/board_note.py`, `report/cache/stays_summary.json` and `report/findings_draft.json`, as supplied. `U.render_report(params)` runs the report from top to bottom in a fresh process, writes `out/<name>.html` and returns the numbers it printed with a short digest of them. Each render takes about half a minute on a laptop.
#
# **Tasks**
# - [ ] 1 · Render the draft twice and compare (5 min)
# - [ ] 2 · Fix the seed (4 min)
# - [ ] 3 · Read the raw data, not the cache (5 min)
# - [ ] 4 · Check the findings table: status, check and limit (4 min)
# - [ ] 5 · Choose the capstone dataset and write two questions (7 min)
# - [ ] ✱ Stretch · Add a "what changed" line between two renders

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-203.git"
    if not Path("/content/ds-203").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-203"], check=True)
    os.chdir("/content/ds-203/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("tilal.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import tilal as U
import json
alt = U.alt()
pd.set_option("display.width", 160)
print("mode:", U.MODE)

# %%
DRAFT = {"seed": None, "source": "cache", "findings": None}
run_a = U.render_report(DRAFT, "draft_a")
run_b = U.render_report(DRAFT, "draft_b")
print(f"first render : {run_a['path']} ({run_a['kilobytes']} KB), digest {run_a['digest']}")
print(f"second render: {run_b['path']} ({run_b['kilobytes']} KB), digest {run_b['digest']}")

# %% [markdown]
# Open `out/draft_a.html` in a browser: this is what the director would receive. Nothing was changed between the two renders, and the digests differ.
#
# ## 1 · Compare two renders (5 min)
#
# ✏️ **Exercise** · Write `differences(a, b)`: the sorted list of keys whose values differ between two dictionaries of numbers.

# %%
def differences(a, b):
    # BEGIN SOLUTION
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    # END SOLUTION


# %%
try:
    DIFF = differences(run_a["numbers"], run_b["numbers"])
except NotImplementedError:
    DIFF = U.reference("d4_4", "diff")
U.keep("d4_4", "diff", DIFF)
for k in DIFF:
    print(f"  {k}: {run_a['numbers'][k]} then {run_b['numbers'][k]}")
U.check(len(DIFF) >= 1 and set(DIFF) <= {"correlation_low", "correlation_high"}, "the ends of the bootstrap interval change from one render to the next; nothing else does")

# %% [markdown]
# **Look at.** The change is in the third decimal. That is enough for two people to hold two versions of "the" report, and for nobody to know which one the director signed.

# %% [markdown]
# ## 2 · Fix the seed (4 min)
#
# The report draws its resamples from `np.random.default_rng(PARAMS["seed"])`, and the draft leaves the seed empty.
#
# ✏️ **Exercise** · Write `with_seed(params)`: a copy of the parameters with an integer seed.

# %%
def with_seed(params):
    # BEGIN SOLUTION
    return {**params, "seed": 203}
    # END SOLUTION


# %%
try:
    SEEDED = with_seed(DRAFT)
except NotImplementedError:
    SEEDED = U.reference("d4_4", "seeded")
U.keep("d4_4", "seeded", SEEDED)
run_c = U.render_report(SEEDED, "seeded_a")
run_d = U.render_report(SEEDED, "seeded_b")
print(f"digests: {run_c['digest']} and {run_d['digest']}")
U.check(isinstance(SEEDED.get("seed"), int) and run_c["digest"] == run_d["digest"] and DRAFT["seed"] is None, "with a seed, two renders give the same numbers; the draft's parameters were copied, not changed")

# %% [markdown]
# ## 3 · Raw data, not the cache (5 min)
#
# Section 1 of the draft does not compute its numbers. It reads `report/cache/stays_summary.json`, saved once, before lab 1.2 found the duplicate rows, the 999 nights and the three spellings of "Gulf".
#
# ✏️ **Exercise** · Write `from_raw(params)`: a copy with `source` set to `"raw"`. The cell below renders it and lists what changes with your `differences`.

# %%
def from_raw(params):
    # BEGIN SOLUTION
    return {**params, "source": "raw"}
    # END SOLUTION


# %%
try:
    RAW = from_raw(SEEDED)
except NotImplementedError:
    RAW = U.reference("d4_4", "raw")
U.keep("d4_4", "raw", RAW)
run_e = U.render_report(RAW, "from_raw")
stale = sorted(k for k in run_c["numbers"] if run_c["numbers"][k] != run_e["numbers"][k])
U.table(["number", "from the cache", "from the raw data"], [[k, run_c["numbers"][k], run_e["numbers"][k]] for k in stale], "{}")
N = run_e["numbers"]
U.check(RAW.get("source") == "raw" and N["stays"] == 40000 and abs(N["mean_nights"] - 3.3) < 0.01 and "mean_nights" in stale, "from the raw data: 40,000 stays and a mean of 3.3 nights, not 40,600 and 11.27")
U.check(N["gulf_stays"] > 6000, "and about 500 more Gulf stays than the cache knew of, once the three spellings are one")

# %% [markdown]
# **Look at.** A cache is a number with no code behind it. It was right on the day it was saved. The rule of the report: every number is computed from the raw files by the render that prints it, or it is marked as taken from elsewhere, with its date.

# %% [markdown]
# ## 4 · The findings table (4 min)
#
# The report ends with a table: each finding with its `status`, the `check` that was run and the `limit` that goes with it. `planned` records whether the question was written down before the data that answers it was looked at.
#
# ✏️ **Exercise** · Write `problems(findings)`: a list of `(row number, problem)` pairs, rows numbered from 1, with the problem `"no limit"` when the limit is empty, `"no check"` when the check is empty, and `"confirmed without a plan"` when the status is `"confirmed"` and `planned` is false. Then write `repaired(findings)`: a corrected copy of the table.

# %%
findings = json.loads((U.LABS / "report" / "findings_draft.json").read_text(encoding="utf-8"))
print(pd.DataFrame(findings)[["finding", "status", "planned", "limit"]].to_string(max_colwidth=58))


def problems(findings):
    # BEGIN SOLUTION
    out = []
    for i, f in enumerate(findings, start=1):
        if not f["check"].strip():
            out.append((i, "no check"))
        if not f["limit"].strip():
            out.append((i, "no limit"))
        if f["status"] == "confirmed" and not f["planned"]:
            out.append((i, "confirmed without a plan"))
    return out
    # END SOLUTION


def repaired(findings):
    # BEGIN SOLUTION
    out = [dict(f) for f in findings]
    out[2]["limit"] = "Survey respondents choose to answer; the mix is taken from the respondents, not from all visitors."
    out[3]["status"] = "exploratory"
    return out
    # END SOLUTION


# %%
try:
    PROBLEMS = [tuple(p) for p in problems(findings)]
except NotImplementedError:
    PROBLEMS = [tuple(p) for p in U.reference("d4_4", "problems")]
U.keep("d4_4", "problems", [list(p) for p in PROBLEMS])
print(PROBLEMS)
U.check(sorted(PROBLEMS) == [(3, "no limit"), (4, "confirmed without a plan")], "row 3 has no limit; row 4 is marked confirmed and came from a search")
try:
    FIXED = repaired(findings)
    left = [tuple(p) for p in problems(FIXED)]
except NotImplementedError:
    FIXED = U.reference("d4_4", "fixed")
    left = []
U.keep("d4_4", "fixed", FIXED)
U.check(len(FIXED) == len(findings) and not left and FIXED[3]["status"] == "exploratory" and len(FIXED[2]["limit"].split()) >= 5, "five rows, each with a check and a limit, and nothing marked confirmed without a plan")
final = U.render_report({**RAW, "findings": FIXED}, "board_note")
print(f"final render: {final['path']} ({final['kilobytes']} KB), digest {final['digest']}")
U.check(final["digest"] == run_e["digest"], "the final report holds the same numbers as the render from raw data: only the table changed")

# %% [markdown]
# ## 5 · Your capstone dataset (7 min)
#
# On the capstone day you take one of three datasets you have not seen, explore it and present an exploratory report. Choose now, so that tonight you can read its data dictionary.
#
# ✏️ **Exercise** · Read the three descriptions, then return your choice and two questions you would put to the data. A question names a quantity and a comparison, and ends with a question mark. Assistant off.

# %%
datasets = json.loads((U.LABS / "capstone" / "datasets.json").read_text(encoding="utf-8"))
for key, d in datasets.items():
    print(f"{key}: {d['organisation']} · unit: {d['unit']} · for {d['audience']}")
    print("    columns:", ", ".join(d["columns"]))


def capstone_choice():
    # BEGIN SOLUTION
    return {"dataset": "awan_parks",
            "questions": ["How many days does a maintenance request take to close in each park, and how far do the parks differ once the category of request is the same?",
                          "Do requests that needed more crew visits get lower ratings from the resident who reported them?"]}
    # END SOLUTION


# %%
try:
    CHOICE = capstone_choice()
except NotImplementedError:
    CHOICE = U.reference("d4_4", "choice")
U.keep("d4_4", "choice", CHOICE)
print(CHOICE["dataset"])
for q in CHOICE["questions"]:
    print("  ·", q)
U.check(CHOICE["dataset"] in datasets and len(CHOICE["questions"]) == 2 and all(q.strip().endswith("?") and len(q.split()) >= 8 for q in CHOICE["questions"]), "one of the three datasets and two full questions")

# %% [markdown]
# ## ✱ Stretch · What changed
#
# Write a function that takes two renders and returns one line for a change log, such as "3 numbers changed: gulf_stays, mean_nights, stays".

# %%
def stretch():
    # BEGIN SOLUTION
    d = differences(run_c["numbers"], run_e["numbers"])
    line = f"{len(d)} numbers changed: {', '.join(d)}"
    print(line)
    return line
    # END SOLUTION


try:
    U.keep("d4_4", "changelog", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Two renders of the same report differ in the third decimal. Does it matter?
#    <details><summary>Answer</summary>Yes. A report that cannot be reproduced cannot be checked, and nobody can say which version was approved.</details>
# 2. Why is a cached summary a risk?
#    <details><summary>Answer</summary>It keeps the numbers of the day it was saved. Later decisions about the data never reach it.</details>
# 3. What are the three columns every finding carries?
#    <details><summary>Answer</summary>Its status (exploratory or confirmed), the check that was run and the limit of what it shows.</details>
#
# ## Carry forward
#
# Your capstone report uses this structure: parameters at the top, numbers computed at render, charts with their uncertainty, and a table of findings with status, check and limit.
