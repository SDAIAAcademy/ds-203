# %% [markdown]
# # Lab 4.2 · Intervals on the satisfaction chart
#
# Day 4 · Session 2 (Showing uncertainty) · 25 min.
#
# The earlier report ranked the nine sites by mean satisfaction in 2025 under the caption "Terrace Farms is our best-rated site". The bars rest on 59 to 510 responses each, and nothing on the chart says so. You put an interval on every site, redraw the chart so that a reader can see which sites can be told apart, check one difference the board may report, and rewrite the caption.
#
# **AI policy.** The tutor may hint at plotting syntax. The caption is your own first draft, assistant off.
#
# **Reference state.** `U.survey()`, the 2,200 responses of 2025. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · The chart as published, and the responses behind each bar (3 min)
# - [ ] 2 · A bootstrap interval for each site (7 min)
# - [ ] 3 · Points with intervals, sorted, with the sample size (7 min)
# - [ ] 4 · The interval of a difference: guided against unguided visits (4 min)
# - [ ] 5 · Rewrite the caption (4 min)
# - [ ] ✱ Stretch · Draw the 2025 intervals by origin market inside one site

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
s25 = U.survey().query("year == 2025")[["site", "origin", "guided", "satisfaction"]]
means = s25.groupby("site")["satisfaction"].mean().rename("mean").reset_index()
published = alt.Chart(means).mark_bar().encode(
    y=alt.Y("site:N", sort="-x", title=None), x=alt.X("mean:Q", title="Mean satisfaction, 2025", scale=alt.Scale(domain=[3.8, 4.3], clamp=True)),
).properties(title="Terrace Farms is our best-rated site")
U.show(published, "d4_2_published")

# %% [markdown]
# ## 1 · What is behind each bar (3 min)
#
# ✏️ **Exercise** · Write `site_table(s)`: one row per site with `n` (responses) and `mean`, sorted by the mean, highest first.

# %%
def site_table(s):
    # BEGIN SOLUTION
    return s.groupby("site")["satisfaction"].agg(n="size", mean="mean").sort_values("mean", ascending=False).reset_index()
    # END SOLUTION


# %%
try:
    T = site_table(s25)
except NotImplementedError:
    T = U.reference("d4_2", "table")
U.keep("d4_2", "table", T)
print(T.round(3).to_string(index=False))
U.check(T["site"].iloc[0] == "Terrace Farms" and int(T["n"].iloc[0]) == 59 and int(T["n"].max()) == 510, "the top site rests on 59 responses, the Cable Car on 510")

# %% [markdown]
# ## 2 · An interval for each site (7 min)
#
# ✏️ **Exercise** · Write `boot_interval(values, B, gen)`: resample the values with replacement `B` times, take the mean each time, and return the 2.5th and 97.5th percentiles of the means.

# %%
def boot_interval(values, B, gen):
    # BEGIN SOLUTION
    v = np.asarray(values, float)
    means = v[gen.integers(0, len(v), size=(B, len(v)))].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi)
    # END SOLUTION


# %%
B = U.pick(4000, 800)
gen = U.rng(44)
try:
    rows = []
    for site in T["site"]:
        lo, hi = boot_interval(s25.loc[s25["site"] == site, "satisfaction"], B, gen)
        rows.append({"site": site, "lo": lo, "hi": hi})
    CI = T.merge(pd.DataFrame(rows), on="site")
except NotImplementedError:
    CI = U.reference("d4_2", "ci")
U.keep("d4_2", "ci", CI)
CI["width"] = CI["hi"] - CI["lo"]
print(CI.round(3).to_string(index=False))
top = CI.set_index("site").loc["Terrace Farms"]
U.check(abs(top["lo"] - 4.02) < 0.04 and abs(top["hi"] - 4.44) < 0.04, "Terrace Farms: mean 4.24, interval about 4.02 to 4.44")
U.check(CI.sort_values("n")["width"].is_monotonic_decreasing or CI["width"].corr(1 / np.sqrt(CI["n"])) > 0.95, "the fewer the responses, the wider the interval")
overlap = CI[(CI["lo"] <= top["hi"]) & (CI["hi"] >= top["lo"]) & (CI["site"] != "Terrace Farms")]
N_OVERLAP = int(len(overlap))
print(f"sites whose interval overlaps that of Terrace Farms: {N_OVERLAP} of the other 8")

# %% [markdown]
# **Look at.** The site at the top has the widest interval. That is not a coincidence: small groups reach the top and the bottom of any ranking more easily, because their means move more.

# %% [markdown]
# ## 3 · Points with intervals (7 min)
#
# A bar draws attention to its length from zero. For a mean with an interval, draw a point and a line from the lower to the upper end, on an axis that may start where the data starts, and write the number of responses beside the site.
#
# ✏️ **Exercise** · Write `interval_chart(ci)`: a rule from `lo` to `hi` and a point at `mean` for each site, sites sorted by the mean, and each site's label ending with its number of responses, such as `"Terrace Farms (n = 59)"`. Add a `label` column first.

# %%
def interval_chart(ci):
    # BEGIN SOLUTION
    d = ci.assign(label=ci["site"] + " (n = " + ci["n"].astype(int).astype(str) + ")")
    order = list(d.sort_values("mean", ascending=False)["label"])
    base = alt.Chart(d).encode(y=alt.Y("label:N", sort=order, title=None))
    rule = base.mark_rule(strokeWidth=2.5).encode(x=alt.X("lo:Q", title="Mean satisfaction in 2025, with 95% bootstrap interval", scale=alt.Scale(domain=[3.6, 4.6])), x2="hi:Q")
    point = base.mark_circle(size=110, opacity=1).encode(x="mean:Q")
    return alt.layer(rule, point).properties(title="Most sites cannot be told apart")
    # END SOLUTION


# %%
try:
    c3 = interval_chart(CI)
except NotImplementedError:
    c3 = U.reference("d4_2", "chart")
U.keep("d4_2", "chart", c3)
ch = U.channels(c3)
U.check("rule" in U.marks(c3) and U.marks(c3) & {"circle", "point"} and "bar" not in U.marks(c3), "a rule for the interval and a point for the mean; no bars")
U.check(ch.get("x2", {}).get("field") in ("hi", "lo") and "n = 59" in str(c3.to_dict()["datasets"]), "the rule runs from one end of the interval to the other, and every label carries its n")
U.show(c3, "d4_2_intervals")

# %% [markdown]
# ## 4 · The interval of a difference (4 min)
#
# Overlapping intervals do not prove "no difference", and the honest way to compare two groups is an interval for the difference itself. The board would like to say that guided visits are rated higher.
#
# ✏️ **Exercise** · Write `diff_interval(a, b, B, gen)`: resample each group with replacement, take the difference of the means, `B` times; return the observed difference and the 2.5th and 97.5th percentiles.

# %%
def diff_interval(a, b, B, gen):
    # BEGIN SOLUTION
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a[gen.integers(0, len(a), size=(B, len(a)))].mean(axis=1) - b[gen.integers(0, len(b), size=(B, len(b)))].mean(axis=1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    return float(a.mean() - b.mean()), float(lo), float(hi)
    # END SOLUTION


# %%
g, u = s25.loc[s25["guided"] == 1, "satisfaction"], s25.loc[s25["guided"] == 0, "satisfaction"]
try:
    DIFF, DLO, DHI = diff_interval(g, u, B, U.rng(45))
except NotImplementedError:
    DIFF, DLO, DHI = U.reference("d4_2", "diff")
U.keep("d4_2", "diff", [DIFF, DLO, DHI])
print(f"guided minus unguided, 2025: {DIFF:+.2f} points, interval {DLO:+.2f} to {DHI:+.2f} ({len(g)} guided and {len(u)} unguided responses)")
U.check(DLO > 0.2 and DHI < 0.5, "guided visits score about 0.4 point higher, and the whole interval is well above zero: report it")

# %% [markdown]
# ## 5 · Rewrite the caption (4 min)
#
# ✏️ **Exercise** · Two sentences to stand under the new chart: what can be said about the ranking, and what the interval is and is not. Assistant off.

# %%
def caption():
    # BEGIN SOLUTION
    return ("Mean satisfaction in 2025 by site with 95% bootstrap intervals: the Souq Walk (4.22, n = 442) rates above the Cable Car (3.93, n = 510), but Terrace Farms' 4.24 rests on 59 responses, its interval runs from about 4.0 to 4.4, and it cannot be ranked first. "
            "The intervals show how far each mean could move with another sample of respondents; they do not correct for who chose to answer or for the different mix of visitors at each site.")
    # END SOLUTION


# %%
try:
    CAPTION = caption()
except NotImplementedError:
    CAPTION = U.reference("d4_2", "caption")
U.keep("d4_2", "caption", CAPTION)
U.say("Caption", CAPTION)
U.reading_check(CAPTION, ["59", ["interval"], ["cannot", "not"]], "the caption")

# %% [markdown]
# ## ✱ Stretch · Inside one site
#
# Compute the 2025 mean and interval by origin market at the Cable Car and look at the widths.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(46)
    d = s25[s25["site"] == "Cable Car"]
    rows = []
    for o in U.ORIGINS:
        v = d.loc[d["origin"] == o, "satisfaction"]
        lo, hi = boot_interval(v, U.pick(2000, 500), gen)
        rows.append([o, len(v), float(v.mean()), lo, hi])
    U.table(["origin", "n", "mean", "lo", "hi"], rows, "{:.2f}")
    print("The site's mean hides five means that differ by a full point: the mix of visitors, again.")
    return rows
    # END SOLUTION


try:
    U.keep("d4_2", "inside", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is the top-ranked site so often a small one?
#    <details><summary>Answer</summary>Means of small groups vary more, so they land at both ends of a ranking more often than large groups do.</details>
# 2. Two intervals overlap. Does that show the two sites are equal?
#    <details><summary>Answer</summary>No. It shows this sample cannot order them. For a claim about two groups, compute the interval of their difference.</details>
# 3. What does a 95% bootstrap interval not cover?
#    <details><summary>Answer</summary>Anything other than sampling variation: who answers a survey, how the question was put, a different mix of visitors.</details>
#
# ## Carry forward
#
# The guided-visit difference is the one pattern of the three that the board may report. Lab 4.3 takes the one it found by searching.
