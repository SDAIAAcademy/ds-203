# %% [markdown]
# # Lab 1.2 · Profile the stay register
#
# Day 1 · Session 2 (Profiling a table) · 25 min.
#
# The stay register is the board's visitor table: one row for each visiting party. Before it answers question 1 you find out what is in it. You check its grain and its key, where values are missing, which values cannot be true, and you log three data issues with the evidence and a decision for each. Nothing is repaired silently.
#
# **AI policy.** The tutor may hint at dataframe syntax. The issue log and the reading are your own first draft, assistant off.
#
# **Reference state.** `data/stays.csv.gz`, exactly as exported (`U.stays_raw()`). Nothing from lab 1.1 is needed.
#
# **Tasks**
# - [ ] 1 · Shape, grain and key: is one row one stay? (5 min)
# - [ ] 2 · Types and missing values: where spend is missing (6 min)
# - [ ] 3 · Ranges and categories: values that cannot be true (6 min)
# - [ ] 4 · Log three issues with evidence and a decision (6 min)
# - [ ] 5 · Write the reading (2 min)
# - [ ] ✱ Stretch · Find the fifth issue, in the dates

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
import duckdb
alt = U.alt()
pd.set_option("display.width", 160)
print("mode:", U.MODE)

# %%
raw = U.stays_raw()
print(raw.shape)
print(raw.head(5).to_string())

# %% [markdown]
# One statement profiles every column: DuckDB's `SUMMARIZE` gives type, range, distinct values and the share of missing values. Read it before you write any code of your own.

# %%
print(duckdb.sql("SUMMARIZE SELECT * FROM raw").df()[["column_name", "column_type", "min", "max", "approx_unique", "null_percentage"]].to_string(index=False))

# %% [markdown]
# ## 1 · Shape, grain and key (5 min)
#
# The dictionary says one row is one stay and `stay_id` is its key. A key is unique. Test the claim.
#
# ✏️ **Exercise** · Write `grain(df)` returning `(rows, distinct stay_id values, rows that repeat an earlier row in every column)`.

# %%
def grain(df):
    # BEGIN SOLUTION
    return len(df), int(df["stay_id"].nunique()), int(df.duplicated().sum())
    # END SOLUTION


# %%
try:
    ROWS, IDS, DUPES = grain(raw)
except NotImplementedError:
    ROWS, IDS, DUPES = U.reference("d1_2", "grain")
U.keep("d1_2", "grain", [ROWS, IDS, DUPES])
print(f"{ROWS:,} rows, {IDS:,} distinct keys, {DUPES:,} rows that repeat an earlier row exactly")
U.check((ROWS, IDS, DUPES) == (40600, 40000, 600), "600 rows were entered twice: 40,600 rows hold 40,000 stays")

# %% [markdown]
# **Look at.** Every repeated key is a repeated row: the same stay entered twice, not two stays sharing a key. That decides the repair (drop the copies). Had the rows differed, the decision would be someone else's.

# %% [markdown]
# ## 2 · Types and missing values (6 min)
#
# A share of missing values is one number. Where the missing values sit is the finding.
#
# ✏️ **Exercise** · Write `missing_spend(df)` returning the share of rows with `spend_sar` missing, for day visits (`nights == 0`) and for overnight stays (`nights > 0`), as a pair. Work on the rows without the exact copies.

# %%
def missing_spend(df):
    # BEGIN SOLUTION
    d = df.drop_duplicates()
    miss = d["spend_sar"].isna()
    return float(miss[d["nights"] == 0].mean()), float(miss[d["nights"] > 0].mean())
    # END SOLUTION


# %%
try:
    MISS_DAY, MISS_NIGHT = missing_spend(raw)
except NotImplementedError:
    MISS_DAY, MISS_NIGHT = U.reference("d1_2", "missing")
U.keep("d1_2", "missing", [MISS_DAY, MISS_NIGHT])
total_missing = int(raw.drop_duplicates()["spend_sar"].isna().sum())
print(f"spend is missing in {total_missing:,} stays: {MISS_DAY:.1%} of day visits and {MISS_NIGHT:.1%} of overnight stays")
U.check(0.20 < MISS_DAY < 0.24 and 0.015 < MISS_NIGHT < 0.03, "spend is missing for about one day visit in five and one overnight stay in fifty")

# %% [markdown]
# **Look at.** Day visitors spend least and answer least. Mean spend over the rows that have a value therefore describes overnight visitors more than all visitors, and it is too high for the region as a whole.

# %% [markdown]
# ## 3 · Ranges and categories (6 min)
#
# ✏️ **Exercise** · Write `odd_values(df)` on the rows without copies, returning a dictionary with
# `"nights_max"` (the largest value of nights), `"nights_at_max"` (how many rows hold it) and `"origins"` (the sorted list of distinct origin values, exactly as stored).

# %%
def odd_values(df):
    # BEGIN SOLUTION
    d = df.drop_duplicates()
    top = int(d["nights"].max())
    return {"nights_max": top, "nights_at_max": int((d["nights"] == top).sum()), "origins": sorted(d["origin"].unique())}
    # END SOLUTION


# %%
try:
    ODD = odd_values(raw)
except NotImplementedError:
    ODD = U.reference("d1_2", "odd")
U.keep("d1_2", "odd", ODD)
print(ODD)
d = raw.drop_duplicates()
print(d["origin"].value_counts().to_string())
SPELL = int(d["origin"].isin(["GCC", "gulf "]).sum())
U.check(ODD["nights_max"] == 999 and ODD["nights_at_max"] == 320, "320 stays have 999 nights: a code for 'not recorded', not a length of stay")
U.check(len(ODD["origins"]) == 7 and SPELL == 586, "the Gulf market is stored under three spellings; 586 stays use the two odd ones")

# %% [markdown]
# **Look at.** With the 999s left in, the mean length of stay is `d["nights"].mean()`; print it. One code in 0.8% of the rows more than triples the mean. `"gulf "` ends with a space that no printed table shows.

# %%
print(f"mean nights with the 999s: {d['nights'].mean():.2f}; without them: {d.loc[d['nights'] != 999, 'nights'].mean():.2f}")

# %% [markdown]
# ## 4 · The issue log (6 min)
#
# An issue log entry has what is wrong, the evidence as a number of rows, and a decision someone can disagree with.
#
# ✏️ **Exercise** · Return three entries (or more): `{"issue": ..., "rows": ..., "decision": ...}`. The decision is one of `"drop the copies"`, `"set to missing"`, `"recode to one spelling"`, `"keep and report the share"`, `"ask the owner"`.

# %%
def issue_log():
    # BEGIN SOLUTION
    return [
        {"issue": "600 rows repeat an earlier row in every column", "rows": 600, "decision": "drop the copies"},
        {"issue": "nights is 999 where the length of stay was not recorded", "rows": 320, "decision": "set to missing"},
        {"issue": "the Gulf market is spelled Gulf, GCC and 'gulf ' with a trailing space", "rows": 586, "decision": "recode to one spelling"},
        {"issue": "spend is missing, far more often for day visits than for overnight stays", "rows": total_missing, "decision": "keep and report the share"},
    ]
    # END SOLUTION


# %%
try:
    LOG = issue_log()
except NotImplementedError:
    LOG = U.reference("d1_2", "log")
U.keep("d1_2", "log", LOG)
KNOWN = {600: "copies", 320: "the 999 code", 586: "spellings", total_missing: "missing spend", 14: "impossible dates"}
DECISIONS = {"drop the copies", "set to missing", "recode to one spelling", "keep and report the share", "ask the owner"}
for e in LOG:
    print(f" · {e['rows']:>6,} rows · {e['issue']} → {e['decision']}")
found = {KNOWN[e["rows"]] for e in LOG if e["rows"] in KNOWN and e["decision"] in DECISIONS}
U.check(len(found) >= 3, f"the log holds at least three planted issues with the right row counts and a decision ({len(found)} found)")
clean = U.stays()
U.check(len(clean) == 40000 and clean["origin"].nunique() == 5 and clean["nights"].max() < 100, "the supplied clean table, U.stays(), applies the same decisions: 40,000 stays, five origins, no 999")

# %% [markdown]
# ## 5 · The reading (2 min)
#
# ✏️ **Exercise** · Two sentences for Aws Al-Hudaif, who owns the register: what you found and what it changes. Use the numbers. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("The register holds 40,000 stays in 40,600 rows: 600 rows were entered twice, 320 stays carry 999 nights as a code for not recorded, and the Gulf market is spelled three ways. "
            "Spend is missing for about 22% of day visits and 2% of overnight stays, so any average spend from this table describes overnight visitors better than day visitors.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d1_2", "reading")
U.keep("d1_2", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["600", "999", ["day visit", "day-visit"]])

# %% [markdown]
# ## ✱ Stretch · The fifth issue
#
# `arrival_date` is text in the export. Parse it and look at the range.

# %%
def stretch():
    # BEGIN SOLUTION
    dates = pd.to_datetime(raw.drop_duplicates()["arrival_date"])
    late = int((dates > "2025-12-31").sum())
    print(f"dates run from {dates.min().date()} to {dates.max().date()}; {late} stays arrive after the data ends, all in 2032")
    return late
    # END SOLUTION


try:
    U.keep("d1_2", "late", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why did you test for exact copies and not only for repeated keys?
#    <details><summary>Answer</summary>A repeated key with different values is a conflict that needs the owner. An exact copy is a double entry that can be dropped.</details>
# 2. Spend is missing in about 8% of stays. Why is that number not enough?
#    <details><summary>Answer</summary>The missing values sit with day visitors. A summary of the rows that remain is not a summary of all visitors.</details>
# 3. Why set 999 to missing and not to the median?
#    <details><summary>Answer</summary>Nobody knows those stays' length. A filled-in median would hide 320 unknowns inside the most common value.</details>
#
# ## Carry forward
#
# Labs 1.3 and 1.4 start from `U.stays()`, the register after these decisions. They do not need your notebook. Assembling and repairing data from several sources is the subject of DS-202.
