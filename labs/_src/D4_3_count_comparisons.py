# %% [markdown]
# # Lab 4.3 · Count the comparisons
#
# Day 4 · Session 3 (Exploratory and confirmatory) · 25 min.
#
# The weekend claim was dropped in lab 4.1. A week later the communications officer, Nayef Al-Jumaah, came back with a headline: "At the Honey Museum, weekend visitors were far more satisfied than weekday visitors in 2025." Taken alone, the gap passes a chance check. You find out how the gap was found, count the comparisons that were looked at, simulate what the largest of that many gaps looks like when the day of the week means nothing, and then mark five findings of the earlier report as exploratory or confirmed.
#
# **AI policy.** The tutor may hint at syntax in steps 1, 2 and 4. Marking the findings and rewriting the headline are your own work, assistant off.
#
# **Reference state.** `U.survey()` and two supplied files: `data/claims.json` (the headline and how it was found) and `data/past_findings.json` (five findings, each with how it was reached). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · The headline gap and its p-value, taken alone (4 min)
# - [ ] 2 · All 27 site-year gaps (5 min)
# - [ ] 3 · The chance of at least one small p-value among 27 (2 min)
# - [ ] 4 · Simulate the most striking of 27 gaps (6 min)
# - [ ] 5 · Mark five past findings: exploratory or confirmed (5 min)
# - [ ] 6 · Rewrite the finding (3 min)
# - [ ] ✱ Stretch · Count again with origin market added

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
alt = U.alt()
pd.set_option("display.width", 160)
print("mode:", U.MODE)

# %%
survey = U.survey()
claim = U.js("claims.json")
print(claim["headline"])
print("How it was found:", claim["how_found"])
SITE, YEAR = claim["headline_site"], claim["headline_year"]


def z_gap(score, flag):
    """Weekend mean minus weekday mean, and the same gap in units of its standard error."""
    a, b = score[flag], score[~flag]
    g = a.mean() - b.mean()
    return float(g), float(g / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


# %% [markdown]
# ## 1 · The headline, taken alone (4 min)
#
# ✏️ **Exercise** · Write `cell_test(s, site, year, B, gen)`: keep the responses of that site and year, compute the weekend gap with `z_gap`, shuffle the weekend labels `B` times inside the cell, and return the gap and the two-sided p-value `(count + 1) / (B + 1)`.

# %%
def cell_test(s, site, year, B, gen):
    # BEGIN SOLUTION
    d = s[(s["site"] == site) & (s["year"] == year)]
    score, flag = d["satisfaction"].to_numpy(float), d["weekend"].to_numpy()
    g, _ = z_gap(score, flag)
    null = np.array([z_gap(score, gen.permutation(flag))[0] for _ in range(B)])
    return g, float((np.sum(np.abs(null) >= abs(g)) + 1) / (B + 1))
    # END SOLUTION


# %%
B1 = U.pick(5000, 1500)
try:
    GAP, P_ALONE = cell_test(survey, SITE, YEAR, B1, U.rng(47))
except NotImplementedError:
    GAP, P_ALONE = U.reference("d4_3", "alone")
U.keep("d4_3", "alone", [GAP, P_ALONE])
cell = survey[(survey["site"] == SITE) & (survey["year"] == YEAR)]
print(f"{SITE}, {YEAR}: {int(cell['weekend'].sum())} weekend and {int((~cell['weekend']).sum())} weekday responses")
print(f"gap {GAP:+.2f} points, p-value taken alone {P_ALONE:.3f}")
U.check(abs(GAP - 0.30) < 0.01 and 0.01 < P_ALONE < 0.05, "a gap of 0.30 with a p-value near 0.03: taken alone, it passes")

# %% [markdown]
# ## 2 · All 27 gaps (5 min)
#
# Nine sites, three years: 27 comparisons were looked at, and one was kept.
#
# A gap of 0.33 on 60 responses is less striking than a gap of 0.30 on 167. `z` divides each gap by its standard error, so that small and large cells can be compared; a small p-value goes with a large `z`.
#
# ✏️ **Exercise** · Write `all_gaps(s)`: one row per site and year with `gap` and `z` (from `z_gap`), sorted by the size of `z`, largest first.

# %%
def all_gaps(s):
    # BEGIN SOLUTION
    rows = []
    for (site, year), d in s.groupby(["site", "year"]):
        g, z = z_gap(d["satisfaction"].to_numpy(float), d["weekend"].to_numpy())
        rows.append({"site": site, "year": int(year), "n": len(d), "gap": g, "z": z})
    out = pd.DataFrame(rows)
    return out.reindex(out["z"].abs().sort_values(ascending=False).index).reset_index(drop=True)
    # END SOLUTION


# %%
try:
    G = all_gaps(survey)
except NotImplementedError:
    G = U.reference("d4_3", "gaps")
U.keep("d4_3", "gaps", G)
print(G.head(5).round(2).to_string(index=False))
Z_TOP = float(abs(G["z"].iloc[0]))
print(f"{len(G)} comparisons; gaps above zero: {int((G['gap'] > 0).sum())}, below zero: {int((G['gap'] < 0).sum())}; |z| above 2: {int((G['z'].abs() > 2).sum())}")
U.check(len(G) == 27 and G["site"].iloc[0] == SITE and int(G["year"].iloc[0]) == YEAR and int((G["z"].abs() > 2).sum()) == 1, "27 comparisons; the headline is the most striking and the only one beyond 2 standard errors")
c2 = alt.Chart(G.assign(cell=G["site"] + " " + G["year"].astype(str), headline=(G["site"] == SITE) & (G["year"] == YEAR))).mark_circle(size=90, opacity=1).encode(
    x=alt.X("z:Q", title="Weekend minus weekday satisfaction, in standard errors, each site and year"),
    y=alt.Y("cell:N", sort=alt.EncodingSortField("z", order="descending"), title=None, axis=alt.Axis(labelLimit=220)),
    color=alt.Color("headline:N", legend=None, scale=alt.Scale(domain=[False, True], range=["#8A8A8A", U.OKABE_ITO[4]])),
).properties(title="The headline is the most striking of 27 gaps that scatter around zero", height=420)
U.show(c2, "d4_3_all_gaps")

# %% [markdown]
# ## 3 · At least one small p-value among 27 (2 min)
#
# ✏️ **Exercise** · Write `at_least_one(k, alpha)`: the chance that `k` independent comparisons with no real difference give at least one p-value below `alpha`.

# %%
def at_least_one(k, alpha=0.05):
    # BEGIN SOLUTION
    return 1 - (1 - alpha) ** k
    # END SOLUTION


# %%
try:
    P_ANY = float(at_least_one(27, 0.05))
except NotImplementedError:
    P_ANY = U.reference("d4_3", "p_any")
U.keep("d4_3", "p_any", P_ANY)
print(f"27 comparisons with nothing in them: {P_ANY:.0%} chance of at least one p-value below 0.05")
U.check(abs(P_ANY - 0.75) < 0.005, "three chances in four of at least one 'finding' among 27 comparisons of nothing")

# %% [markdown]
# ## 4 · Simulate the most striking of 27 (6 min)
#
# The honest question is not "how unusual is a gap of 0.30 at this site" but "how unusual is it that the most striking of 27 gaps, in standard errors, is this striking". Shuffle the weekend labels inside every site and year at once, compute the 27 values of `z`, keep the largest in absolute value, and repeat.
#
# ✏️ **Exercise** · Write `largest_of_all(s, B, gen)`: an array of `B` values, each the largest `|z|` over the 27 cells after one shuffle inside each cell.

# %%
def largest_of_all(s, B, gen):
    # BEGIN SOLUTION
    cells = [(d["satisfaction"].to_numpy(float), d["weekend"].to_numpy()) for _, d in s.groupby(["site", "year"])]
    out = np.empty(B)
    for i in range(B):
        out[i] = max(abs(z_gap(score, gen.permutation(flag))[1]) for score, flag in cells)
    return out
    # END SOLUTION


# %%
B4 = U.pick(1000, 300)
try:
    top = np.asarray(largest_of_all(survey, B4, U.rng(48)))
    P_SEARCH = float((np.sum(top >= Z_TOP) + 1) / (len(top) + 1))
except NotImplementedError:
    top = U.reference("d4_3", "top")
    P_SEARCH = U.reference("d4_3", "p_search")
U.keep("d4_3", "top", top)
U.keep("d4_3", "p_search", P_SEARCH)
print(f"the largest |z| of 27, over {len(top)} shuffles: median {np.median(top):.2f}; the headline's |z| is {Z_TOP:.2f}")
print(f"share of shuffles in which the most striking of 27 is at least that striking: {P_SEARCH:.2f}")
U.check(0.3 < P_SEARCH < 0.7 and 1.9 < float(np.median(top)) < 2.5, "with labels that mean nothing, the most striking of 27 gaps is as striking as the headline about half the time")
c4 = alt.layer(
    alt.Chart(pd.DataFrame({"z": top})).mark_bar().encode(x=alt.X("z:Q", bin=alt.Bin(maxbins=30), title="Most striking gap of 27, in standard errors, under shuffled labels"), y=alt.Y("count():Q", title="Shuffles")),
    alt.Chart(pd.DataFrame({"z": [Z_TOP]})).mark_rule(color=U.OKABE_ITO[4], strokeWidth=2.5).encode(x="z:Q"),
).properties(title="The headline is an ordinary 'most striking of 27'")
U.show(c4, "d4_3_largest")

# %% [markdown]
# **Look at.** The p-value of 0.03 was computed correctly. It answers a question nobody asked. The search is part of the method, and a check that leaves the search out checks a different method.

# %% [markdown]
# ## 5 · Five past findings (5 min)
#
# A finding is **confirmed** when the question was written down before the data that answers it was looked at. It is **exploratory** when the data suggested the question. Exploratory is not an insult: it is where questions come from. It is a label that tells the reader what has and has not been done.
#
# ✏️ **Exercise** · Read how each finding was reached, then return `{"F1": "confirmed" or "exploratory", ...}` for all five.

# %%
past = U.js("past_findings.json")
for f in past:
    print(f"{f['id']} · {f['finding']}\n     {f['how']}")


def mark_findings():
    # BEGIN SOLUTION
    return {"F1": "confirmed", "F2": "exploratory", "F3": "confirmed", "F4": "exploratory", "F5": "exploratory"}
    # END SOLUTION


# %%
try:
    MARKS = mark_findings()
except NotImplementedError:
    MARKS = U.reference("d4_3", "marks")
U.keep("d4_3", "marks", MARKS)
U.check(set(MARKS) == {"F1", "F2", "F3", "F4", "F5"} and set(MARKS.values()) <= {"confirmed", "exploratory"}, "five findings, each marked confirmed or exploratory")
U.check(U.matches("d4_3", "marks_key", dict(sorted(MARKS.items()))), "confirmed only where the question was written before the data was looked at")

# %% [markdown]
# ## 6 · Rewrite the finding (3 min)
#
# ✏️ **Exercise** · Two sentences to replace the headline in the report: what was seen, with its number and how many comparisons it was chosen from, and what would have to happen before it is announced. Assistant off.

# %%
def rewrite():
    # BEGIN SOLUTION
    return ("Exploratory: among 27 comparisons of weekend and weekday satisfaction (nine sites, three years), the most striking gap was 0.30 point at the Honey Museum in 2025 (2.2 standard errors), and shuffled labels produce a gap that striking somewhere among the 27 about half the time. "
            "It is not a finding to announce; the question is now written down and will be tested once on the 2026 survey.")
    # END SOLUTION


# %%
try:
    REWRITE = rewrite()
except NotImplementedError:
    REWRITE = U.reference("d4_3", "rewrite")
U.keep("d4_3", "rewrite", REWRITE)
U.say("In the report", REWRITE)
U.reading_check(REWRITE, ["27", ["exploratory"], ["2026", "new data", "next survey", "fresh data"]], "the rewritten finding")

# %% [markdown]
# ## ✱ Stretch · With origin added
#
# Had the search also split by origin market, how many comparisons would there be, and what would the chance of at least one small p-value become?

# %%
def stretch():
    # BEGIN SOLUTION
    k = 9 * 3 * 5
    cells = survey.groupby(["site", "year", "origin"]).size()
    print(f"{k} comparisons; chance of at least one p below 0.05 with nothing there: {at_least_one(k):.1%}")
    print(f"expected number below 0.05: {k * 0.05:.1f}; and {int((cells < 30).sum())} of the cells hold fewer than 30 responses")
    return [k, float(at_least_one(k))]
    # END SOLUTION


try:
    U.keep("d4_3", "more", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. The p-value of 0.03 is arithmetically right. What is wrong with it?
#    <details><summary>Answer</summary>It treats the comparison as the only one made. It was chosen as the most striking of 27, and the choice is part of the method.</details>
# 2. What turns an exploratory finding into a confirmed one?
#    <details><summary>Answer</summary>Writing the question down, then answering it once with data that did not suggest it.</details>
# 3. Is an exploratory finding worth reporting?
#    <details><summary>Answer</summary>Yes, labelled as such, with the number of comparisons it came from and the check that would confirm it.</details>
#
# ## Carry forward
#
# The findings table of lab 4.4 has a `status` column. The Honey Museum row is in it, wrongly marked.
