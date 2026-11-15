# %% [markdown]
# # Lab 1.4 · Centre and spread for four variables
#
# Day 1 · Session 4 (Summaries that fit the shape) · 25 min.
#
# The board's report gives one mean for everything. Four of its variables are skewed, each in its own way: spend has a long right tail, nights is a count with two humps, booking lead time is zero for a third of the parties, and satisfaction is a score from 1 to 5 piled up at the top. You compute the usual summaries, see where they mislead, and choose a centre and a spread for each.
#
# **AI policy.** The tutor may hint at dataframe syntax. The choices and the reading are your own first draft, assistant off.
#
# **Reference state.** `U.stays()` and `U.survey()`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Mean and median of the four variables, and the gap between them (5 min)
# - [ ] 2 · Spread: standard deviation against quartiles (5 min)
# - [ ] 3 · Spend on a log scale: the geometric mean (5 min)
# - [ ] 4 · A zero-heavy variable needs two numbers (4 min)
# - [ ] 5 · A score from 1 to 5 needs shares (3 min)
# - [ ] 6 · Choose and write the reading (3 min)
# - [ ] ✱ Stretch · Remove the top 1% of spend and see which summaries move

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
stays = U.stays()
survey = U.survey()
VARS = {"spend_sar": stays["spend_sar"].dropna(), "nights": stays["nights"].dropna(),
        "booking_lead_days": stays["booking_lead_days"].dropna(), "satisfaction": survey["satisfaction"].astype(float)}
for k, v in VARS.items():
    print(f"{k:18s} n = {len(v):,}")

# %% [markdown]
# ## 1 · Mean and median (5 min)
#
# ✏️ **Exercise** · Write `centres(x)` returning `(mean, median)` of a series.

# %%
def centres(x):
    # BEGIN SOLUTION
    return float(x.mean()), float(x.median())
    # END SOLUTION


# %%
try:
    CENT = {k: centres(v) for k, v in VARS.items()}
except NotImplementedError:
    CENT = {k: tuple(v) for k, v in U.reference("d1_4", "centres").items()}
U.keep("d1_4", "centres", CENT)
U.table(["variable", "mean", "median", "mean / median"], [[k, m, md, (m / md if md else float("nan"))] for k, (m, md) in CENT.items()])
U.check(1.6 < CENT["spend_sar"][0] / CENT["spend_sar"][1] < 2.1 and abs(CENT["spend_sar"][1] - 1498) < 5, "mean spend is close to twice the median: the tail pulls the mean")
U.check(VARS["satisfaction"].skew() < 0 < VARS["spend_sar"].skew(), "satisfaction is skewed the other way: its tail points to the low scores, and mean and median barely differ")

# %% [markdown]
# **Look at.** A mean far above the median says "long right tail" before any chart is drawn. For satisfaction the two nearly agree, and the variable is still skewed: scores pile up against the top of the scale and trail off toward 1. Agreement of mean and median is not proof of symmetry.

# %% [markdown]
# ## 2 · Spread (5 min)
#
# ✏️ **Exercise** · Write `spreads(x)` returning `(standard deviation, first quartile, third quartile)`.

# %%
def spreads(x):
    # BEGIN SOLUTION
    return float(x.std()), float(x.quantile(0.25)), float(x.quantile(0.75))
    # END SOLUTION


# %%
try:
    SPR = {k: spreads(v) for k, v in VARS.items()}
except NotImplementedError:
    SPR = {k: tuple(v) for k, v in U.reference("d1_4", "spreads").items()}
U.keep("d1_4", "spreads", SPR)
U.table(["variable", "sd", "q1", "q3", "mean - sd"], [[k, sd, q1, q3, CENT[k][0] - sd] for k, (sd, q1, q3) in SPR.items()])
U.check(CENT["spend_sar"][0] - SPR["spend_sar"][0] < 0, "for spend, mean minus one standard deviation is below zero: 'mean plus or minus sd' describes nobody")
U.check(SPR["spend_sar"][1] > 0 and SPR["spend_sar"][2] > SPR["spend_sar"][1], "the quartiles of spend are real amounts that half the parties fall between")

# %% [markdown]
# ## 3 · Spend on a log scale (5 min)
#
# Spend multiplies: a longer stay, a larger party, a dearer hotel. On a log scale such a variable is close to symmetric. The mean of the logs, turned back into riyals, is the **geometric mean**.
#
# ✏️ **Exercise** · Write `geometric_mean(x)`. Then `hist_log(df)`: bars of `spend_sar` binned on a log scale. Bin `log10(spend)` yourself into steps of 0.1 and draw one rectangle per bin (`mark_rect`, with `x`, `x2`, `y` and `y2=alt.Y2Datum(0)`), from the bin's lower edge to its upper edge in riyals, on `alt.Scale(type="log")`.

# %%
def geometric_mean(x):
    # BEGIN SOLUTION
    return float(np.exp(np.log(x).mean()))
    # END SOLUTION


def hist_log(df):
    # BEGIN SOLUTION
    lo = np.floor(np.log10(df["spend_sar"]) * 10) / 10
    t = lo.value_counts().sort_index().rename("stays").rename_axis("lo").reset_index()
    t["from_sar"], t["to_sar"] = 10 ** t["lo"], 10 ** (t["lo"] + 0.1)
    return alt.Chart(t).mark_rect().encode(
        x=alt.X("from_sar:Q", scale=alt.Scale(type="log"), title="Spend per party, riyals (log scale)"), x2="to_sar:Q",
        y=alt.Y("stays:Q", title="Stays"), y2=alt.Y2Datum(0),
    ).properties(title="Spend is close to symmetric on a log scale")
    # END SOLUTION


# %%
spend = stays.dropna(subset=["spend_sar"])[["spend_sar"]]
try:
    GM = geometric_mean(VARS["spend_sar"])
except NotImplementedError:
    GM = U.reference("d1_4", "gm")
U.keep("d1_4", "gm", GM)
print(f"geometric mean {GM:,.0f} riyals; median {CENT['spend_sar'][1]:,.0f}; mean {CENT['spend_sar'][0]:,.0f}")
U.check(abs(GM / CENT["spend_sar"][1] - 1) < 0.12, "the geometric mean sits near the median, far below the mean")
try:
    c3 = hist_log(spend)
except NotImplementedError:
    c3 = U.reference("d1_4", "hist_log")
U.keep("d1_4", "hist_log", c3)
U.check(U.channels(c3)["x"].get("scale", {}).get("type") == "log" and U.marks(c3) <= {"bar", "rect"}, "one rectangle per bin on a log scale of riyals")
U.show(c3, "d1_4_hist_log")

# %% [markdown]
# ## 4 · A zero-heavy variable needs two numbers (4 min)
#
# Booking lead time is 0 for every party that did not book. The others booked days or months ahead. One centre for both groups describes neither.
#
# ✏️ **Exercise** · Write `zero_and_rest(x)` returning `(share of zeros, median of the values above zero)`.

# %%
def zero_and_rest(x):
    # BEGIN SOLUTION
    return float((x == 0).mean()), float(x[x > 0].median())
    # END SOLUTION


# %%
try:
    ZERO, REST = zero_and_rest(VARS["booking_lead_days"])
except NotImplementedError:
    ZERO, REST = U.reference("d1_4", "zero")
U.keep("d1_4", "zero", [ZERO, REST])
print(f"{ZERO:.0%} of parties did not book; those who did booked a median of {REST:.0f} days ahead. The mean of all, {CENT['booking_lead_days'][0]:.1f} days, and the median of all, {CENT['booking_lead_days'][1]:.0f} days, mix the two groups.")
U.check(0.33 < ZERO < 0.40 and 12 <= REST <= 16, "more than a third of the parties did not book; the rest booked about two weeks ahead")

# %% [markdown]
# ## 5 · A score from 1 to 5 needs shares (3 min)
#
# The distance from 4 to 5 is not known to equal the distance from 1 to 2, so a mean of scores leans on an assumption. Shares do not.
#
# ✏️ **Exercise** · Write `score_shares(x)`: a series with the share of each score, 1 to 5, in order.

# %%
def score_shares(x):
    # BEGIN SOLUTION
    return x.astype(int).value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fill_value=0.0)
    # END SOLUTION


# %%
try:
    SH = score_shares(VARS["satisfaction"])
except NotImplementedError:
    SH = U.reference("d1_4", "shares")
SH.index = [int(i) for i in SH.index]
U.keep("d1_4", "shares", SH)
TOP2, LOW2 = float(SH[4] + SH[5]), float(SH[1] + SH[2])
print({k: round(float(v), 3) for k, v in SH.items()}, f"· 4 or 5: {TOP2:.0%} · 1 or 2: {LOW2:.0%}")
U.check(abs(SH.sum() - 1) < 1e-9 and 0.70 < TOP2 < 0.82, "three responses in four score 4 or 5")

# %% [markdown]
# ## 6 · Choose, and write the reading (3 min)
#
# ✏️ **Exercise** · Return your choice for each variable as `{"variable": (centre, spread)}` using these words: `"mean"`, `"median"`, `"geometric mean"`, `"share of zeros and median of the rest"`, `"share scoring 4 or 5"`, `"standard deviation"`, `"quartiles"`, `"all five shares"`, `"share at 1 to 3 and at 5 or more nights"`. Then two sentences for the report. Assistant off.

# %%
def choices():
    # BEGIN SOLUTION
    return {"spend_sar": ("median", "quartiles"),
            "nights": ("median", "share at 1 to 3 and at 5 or more nights"),
            "booking_lead_days": ("share of zeros and median of the rest", "quartiles"),
            "satisfaction": ("share scoring 4 or 5", "all five shares")}
    # END SOLUTION


def reading():
    # BEGIN SOLUTION
    return ("A typical party spends about 1,500 riyals (median; half of the parties fall between 570 and 3,390), not the mean of 2,740, which a few large bills pull up. "
            "36% of parties did not book ahead and the others booked a median of 14 days before arrival, and 77% of survey responses score 4 or 5; these summaries leave out the 2,577 stays with no stated spend, most of them day visits.")
    # END SOLUTION


# %%
try:
    CH = {k: tuple(v) for k, v in choices().items()}
except NotImplementedError:
    CH = {k: tuple(v) for k, v in U.reference("d1_4", "choices").items()}
U.keep("d1_4", "choices", CH)
for k, v in CH.items():
    print(f" · {k:18s} centre: {v[0]} · spread: {v[1]}")
U.check(CH["spend_sar"][0] in ("median", "geometric mean") and CH["spend_sar"][1] == "quartiles", "spend: a centre the tail does not move, with quartiles")
U.check(CH["booking_lead_days"][0] == "share of zeros and median of the rest", "booking lead: two numbers")
U.check(CH["satisfaction"][0] != "mean" or CH["satisfaction"][1] == "all five shares", "satisfaction: shares stand beside or in place of the mean")
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d1_4", "reading")
U.keep("d1_4", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["median", ["36%", "a third"], ["leave out", "missing", "not"]])

# %% [markdown]
# ## ✱ Stretch · Which summaries survive the tail
#
# Drop the top 1% of spend and recompute mean, standard deviation, median and quartiles.

# %%
def stretch():
    # BEGIN SOLUTION
    x = VARS["spend_sar"]
    cut = x[x <= x.quantile(0.99)]
    rows = [["mean", x.mean(), cut.mean()], ["sd", x.std(), cut.std()], ["median", x.median(), cut.median()], ["q3", x.quantile(0.75), cut.quantile(0.75)]]
    U.table(["summary", "all", "without top 1%"], rows)
    return {r[0]: round(float(r[2] / r[1] - 1), 3) for r in rows}
    # END SOLUTION


try:
    print("relative change:", U.keep("d1_4", "trim", stretch()))
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Mean spend is 2,740 riyals, the median 1,500. Which goes into a sentence about "the typical party"?
#    <details><summary>Answer</summary>The median. Half of the parties spend less than it. About seven in ten spend less than the mean.</details>
# 2. Why is "mean booking lead 16.2 days" a poor summary?
#    <details><summary>Answer</summary>It averages parties who did not book at all with parties who booked weeks ahead. Nobody behaves like the average.</details>
# 3. What does a summary always carry with it?
#    <details><summary>Answer</summary>The number of values it rests on and what was left out, here the stays with spend missing.</details>
#
# ## Carry forward
#
# Day 2 starts from the same supplied tables. The median and the quartiles of spend are quoted on the Day 2 review slide.
