# %% [markdown]
# # Lab 4.1 · Chance checks on two patterns
#
# Day 4 · Session 1 (Could it be chance) · 25 min.
#
# The board wants to announce two things: "weekend visitors are more satisfied than weekday visitors" and "when the sites are busy, the hotels fill". Both come from exploring. Before either is printed you ask what DS-201 taught you to ask: could this arise by chance? You shuffle labels for the first, resample weeks for the second, and decide for each whether to report, qualify or drop it.
#
# **AI policy.** Assistant off for steps 1 to 3 (the day's first check) and for the reading. The tutor may hint at syntax in steps 4 and 5.
#
# **Reference state.** `U.survey()` (6,000 responses with a `weekend` flag) and `U.weekly()` (156 weeks of tickets and hotel occupancy). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · The weekend gap in satisfaction, as claimed (3 min)
# - [ ] 2 · Shuffle the weekend labels: the p-value (7 min)
# - [ ] 3 · Decide: report, qualify or drop (2 min)
# - [ ] 4 · The correlation of weekly tickets and occupancy (3 min)
# - [ ] 5 · Bootstrap the weeks: an interval (7 min)
# - [ ] 6 · Decide, and write the reading (3 min)
# - [ ] ✱ Stretch · Remove the season from both series and bootstrap again

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
score = survey["satisfaction"].to_numpy(float)
is_weekend = survey["weekend"].to_numpy()
print(U.js("claims.json")["weekend_claim"])
print(survey.groupby("weekend")["satisfaction"].agg(["size", "mean"]).round(3).to_string())

# %% [markdown]
# ## 1 · The gap as claimed (3 min)
#
# ✏️ **Exercise** · Write `gap(score, flag)`: the mean of the flagged responses minus the mean of the others.

# %%
def gap(score, flag):
    # BEGIN SOLUTION
    return float(score[flag].mean() - score[~flag].mean())
    # END SOLUTION


# %%
try:
    OBS = gap(score, is_weekend)
except NotImplementedError:
    OBS = U.reference("d4_1", "obs")
U.keep("d4_1", "obs", OBS)
print(f"weekend minus weekday: {OBS:+.3f} points on the 1 to 5 scale ({int(is_weekend.sum()):,} weekend and {int((~is_weekend).sum()):,} weekday responses)")
U.check(abs(OBS - 0.021) < 0.002, "weekend responses score 0.02 point higher")

# %% [markdown]
# ## 2 · Shuffle the labels (7 min)
#
# The rule from DS-201: if the day of the week makes no difference, the label "weekend" is arbitrary, and shuffling it changes nothing that matters. Shuffle, recompute the gap, repeat; the p-value is the share of shuffles with a gap at least as far from zero as the observed one, counting the observed arrangement as one of them.
#
# ✏️ **Exercise** · Write `shuffled_gaps(score, flag, B, gen)`: an array of `B` gaps under shuffled labels. Then `p_value(null, obs)`, two-sided: `(count + 1) / (B + 1)`.

# %%
def shuffled_gaps(score, flag, B, gen):
    # BEGIN SOLUTION
    out = np.empty(B)
    for i in range(B):
        out[i] = gap(score, gen.permutation(flag))
    return out
    # END SOLUTION


def p_value(null, obs):
    # BEGIN SOLUTION
    return float((np.sum(np.abs(null) >= abs(obs)) + 1) / (len(null) + 1))
    # END SOLUTION


# %%
B = U.pick(5000, 1000)
try:
    null = np.asarray(shuffled_gaps(score, is_weekend, B, U.rng(41)))
    P_WEEKEND = p_value(null, OBS)
except NotImplementedError:
    null = U.reference("d4_1", "null")
    P_WEEKEND = U.reference("d4_1", "p_weekend")
U.keep("d4_1", "null", null)
U.keep("d4_1", "p_weekend", P_WEEKEND)
print(f"{len(null)} shuffles: gaps from {null.min():+.3f} to {null.max():+.3f}, spread {null.std(ddof=1):.3f}")
print(f"p-value: {P_WEEKEND:.2f}: with labels that mean nothing, a gap of {abs(OBS):.3f} or more turns up in about {P_WEEKEND * 100:.0f} shuffles of 100")
U.check(abs(null.mean()) < 0.005 and 0.2 < P_WEEKEND < 0.5, "a gap of 0.02 is what shuffled labels produce about one time in three")
hist = pd.DataFrame({"gap": null})
c_null = alt.layer(
    alt.Chart(hist).mark_bar().encode(x=alt.X("gap:Q", bin=alt.Bin(maxbins=40), title="Gap under shuffled labels, weekend minus weekday"), y=alt.Y("count():Q", title="Shuffles")),
    alt.Chart(pd.DataFrame({"gap": [OBS, -OBS]})).mark_rule(color=U.OKABE_ITO[4], strokeWidth=2.5).encode(x="gap:Q"),
).properties(title=f"The observed gap, {OBS:+.3f}, sits inside what chance produces")
U.show(c_null, "d4_1_null")

# %% [markdown]
# ## 3 · Decide (2 min)
#
# Three decisions are open: `"report"` (the pattern stands and matters), `"qualify"` (it stands, with a stated limit) or `"drop"` (the data does not support announcing it).
#
# ✏️ **Exercise** · Return your decision for the weekend claim.

# %%
def decide_weekend():
    # BEGIN SOLUTION
    return "drop"
    # END SOLUTION


# %%
try:
    D_WEEKEND = decide_weekend()
except NotImplementedError:
    D_WEEKEND = U.reference("d4_1", "d_weekend")
U.keep("d4_1", "d_weekend", D_WEEKEND)
U.check(D_WEEKEND == "drop", "drop: the gap is small, and chance alone produces one as large a third of the time")

# %% [markdown]
# **Look at.** "Drop" is not "weekends make no difference". It is "this survey cannot tell". A p-value near 0.35 is not evidence of no effect; it is the absence of evidence for one.

# %% [markdown]
# ## 4 · The correlation, weekly (3 min)
#
# ✏️ **Exercise** · Write `corr(w)`: the Pearson correlation of `tickets` and `occupancy` in a table of weeks.

# %%
def corr(w):
    # BEGIN SOLUTION
    return float(np.corrcoef(w["tickets"].to_numpy(float), w["occupancy"].to_numpy(float))[0, 1])
    # END SOLUTION


# %%
weeks = U.weekly()
try:
    R = corr(weeks)
except NotImplementedError:
    R = U.reference("d4_1", "r")
U.keep("d4_1", "r", R)
print(f"{len(weeks)} weeks: correlation of tickets sold and share of rooms sold: {R:.2f}")
U.check(abs(R - 0.70) < 0.01, "the weekly correlation is 0.70")

# %% [markdown]
# ## 5 · Bootstrap the weeks (7 min)
#
# For an estimate, DS-201's other rule: resample the unit that was sampled, with replacement, and recompute. Here the unit is the week. Days inside a week resemble one another, which is why the table was built by week and not by day.
#
# ✏️ **Exercise** · Write `bootstrap_corr(w, B, gen)`: `B` correlations, each from `len(w)` weeks drawn with replacement. Then `interval(values)`: the 2.5th and 97.5th percentiles.

# %%
def bootstrap_corr(w, B, gen):
    # BEGIN SOLUTION
    x, y = w["tickets"].to_numpy(float), w["occupancy"].to_numpy(float)
    out = np.empty(B)
    for i in range(B):
        k = gen.integers(0, len(x), len(x))
        out[i] = np.corrcoef(x[k], y[k])[0, 1]
    return out
    # END SOLUTION


def interval(values):
    # BEGIN SOLUTION
    lo, hi = np.percentile(values, [2.5, 97.5])
    return float(lo), float(hi)
    # END SOLUTION


# %%
try:
    boot = np.asarray(bootstrap_corr(weeks, B, U.rng(42)))
    LO, HI = interval(boot)
except NotImplementedError:
    LO, HI = U.reference("d4_1", "ci")
U.keep("d4_1", "ci", [LO, HI])
print(f"correlation {R:.2f}, 95% bootstrap interval {LO:.2f} to {HI:.2f} ({B} resamples of {len(weeks)} weeks)")
U.check(0.57 < LO < 0.64 and 0.75 < HI < 0.81, "the interval runs from about 0.60 to 0.78 and stays far from zero")

# %% [markdown]
# ## 6 · Decide, and write the reading (3 min)
#
# The correlation is not chance. Is it what the board means by "the sites fill the hotels"?
#
# ✏️ **Exercise** · Return your decision for the correlation, then two sentences for the director covering both patterns: each with its number, its check and your decision. Assistant off.

# %%
def decide_correlation():
    # BEGIN SOLUTION
    return "qualify"
    # END SOLUTION


def reading():
    # BEGIN SOLUTION
    return ("Drop the weekend claim: weekend responses score 0.02 point higher, and shuffled labels produce a gap that large about one time in three (p about 0.35). "
            "Qualify the hotel claim: weeks with more ticket sales do have fuller hotels (correlation 0.70, interval 0.60 to 0.78 over 156 weeks), which is not chance, but summer and festivals raise both, so the data does not show that visits to the sites fill the hotels.")
    # END SOLUTION


# %%
try:
    D_CORR = decide_correlation()
except NotImplementedError:
    D_CORR = U.reference("d4_1", "d_corr")
U.keep("d4_1", "d_corr", D_CORR)
U.check(D_CORR in ("qualify", "report"), "the correlation stands; it is reported with its limit")
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d4_1", "reading")
U.keep("d4_1", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["0.70", ["drop", "do not announce"], ["season", "summer"], ["not", "does not"]])

# %% [markdown]
# ## ✱ Stretch · Without the season
#
# Subtract from each week's tickets and occupancy the mean of its calendar month over the three years, then bootstrap the correlation of what is left.

# %%
def stretch():
    # BEGIN SOLUTION
    w = weeks.assign(moy=weeks["week_start"].dt.month)
    resid = w[["tickets", "occupancy"]] - w.groupby("moy")[["tickets", "occupancy"]].transform("mean")
    r = corr(resid)
    lo, hi = interval(bootstrap_corr(resid, U.pick(5000, 1000), U.rng(43)))
    print(f"with the month-of-year means removed: correlation {r:.2f}, interval {lo:.2f} to {hi:.2f}")
    print("Part of the 0.70 was the shared season. What remains is smaller and still above zero.")
    return [r, lo, hi]
    # END SOLUTION


try:
    U.keep("d4_1", "deseason", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why shuffle for the gap and resample for the correlation?
#    <details><summary>Answer</summary>The gap is tested against "no difference", which shuffling creates. The correlation is estimated, and resampling shows how far the estimate moves from sample to sample.</details>
# 2. The weekend p-value is about 0.35. May the board say "the day of the week does not matter"?
#    <details><summary>Answer</summary>No. It may say the survey shows no clear difference. Failing to find an effect is not finding that there is none.</details>
# 3. The correlation's interval excludes zero. Why "qualify" and not "report"?
#    <details><summary>Answer</summary>The check answers "is it chance", not "is it cause". Season moves both series, and the sentence must say so.</details>
#
# ## Carry forward
#
# Lab 4.3 returns to the weekend gap: after the claim was dropped, a far larger gap was "found" at one site in one year.
