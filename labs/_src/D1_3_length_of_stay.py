# %% [markdown]
# # Lab 1.3 · Length of stay by origin
#
# Day 1 · Session 3 (Distributions) · 25 min.
#
# Question 1 of the plan: how many nights do parties from each origin market spend, and what share are day visits? The director heard that visitors "pop in and leave". You draw the distribution of nights, split it by origin as histograms and as box plots, and find the market whose box plot hides two kinds of trip.
#
# **AI policy.** The tutor may hint at plotting syntax. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.stays()`: the register after the decisions of lab 1.2 (40,000 stays, 320 of them with nights unknown). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · One histogram of nights for all parties (5 min)
# - [ ] 2 · Shares by origin, one panel each (7 min)
# - [ ] 3 · Box plots by origin (5 min)
# - [ ] 4 · Find the market with two kinds of trip (5 min)
# - [ ] 5 · Write the reading (3 min)
# - [ ] ✱ Stretch · Change the bin width to 7 nights and say what disappears

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
stays = U.stays().dropna(subset=["nights"])[["origin", "nights"]]
stays["nights"] = stays["nights"].astype(int)
print(len(stays), "stays with a known length;", f"{(stays['nights'] == 0).mean():.1%} are day visits")

# %% [markdown]
# ## 1 · One histogram for all parties (5 min)
#
# Nights is a count, so each bin is one night wide. Altair can count inside the chart: `y="count()"`.
#
# ✏️ **Exercise** · Write `hist_all(df)`: bars, `nights` on x in bins one night wide (`alt.Bin(step=1)`), the count of stays on y.

# %%
def hist_all(df):
    # BEGIN SOLUTION
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("nights:Q", bin=alt.Bin(step=1), title="Nights in the region"),
        y=alt.Y("count():Q", title="Stays"),
    ).properties(title="Length of stay, all parties")
    # END SOLUTION


# %%
try:
    c1 = hist_all(stays)
except NotImplementedError:
    c1 = U.reference("d1_3", "hist_all", stays)
U.keep("d1_3", "hist_all", c1)
ch = U.channels(c1)
U.check(U.marks(c1) == {"bar"} and ch["x"].get("field") == "nights" and ch["x"].get("bin") and ch["y"].get("aggregate") == "count",
        "bars, nights in bins on x, a count on y")
U.show(c1, "d1_3_hist_all")

# %% [markdown]
# **Look at.** The tallest bar is at 0. Then a second rise near 2 and a low third one near 7. One histogram of everyone mixes several kinds of visitor.

# %% [markdown]
# ## 2 · Shares by origin, one panel each (7 min)
#
# The markets differ in size by a factor of eight, so counts would only show which market is largest. Compare **shares**: inside each origin, the share of stays at each number of nights.
#
# ✏️ **Exercise** · Write `share_table(df)`: one row per origin and number of nights, columns `origin`, `nights`, `share`; the shares of one origin add up to 1.
# Then `hist_by_origin(shares)`: bars, nights on x, share on y, one row of panels per origin (`row="origin:N"`), all on the same scales.

# %%
def share_table(df):
    # BEGIN SOLUTION
    t = df.groupby(["origin", "nights"]).size().rename("stays").reset_index()
    t["share"] = t["stays"] / t.groupby("origin")["stays"].transform("sum")
    return t[["origin", "nights", "share"]]
    # END SOLUTION


def hist_by_origin(shares):
    # BEGIN SOLUTION
    return alt.Chart(shares).mark_bar(size=11).encode(
        x=alt.X("nights:Q", title="Nights in the region", scale=alt.Scale(domain=[-0.5, 31.5])),
        y=alt.Y("share:Q", title=None, axis=alt.Axis(format="%", tickCount=3)),
        row=alt.Row("origin:N", sort=U.ORIGINS, title=None, header=alt.Header(labelAngle=0, labelAlign="left")),
    ).properties(height=70, title=alt.Title("Length of stay by origin market", subtitle="Share of each market's stays, by nights in the region"))
    # END SOLUTION


# %%
try:
    shares = share_table(stays)
except NotImplementedError:
    shares = U.reference("d1_3", "shares")
U.keep("d1_3", "shares", shares)
sums = shares.groupby("origin")["share"].sum()
day = shares[shares["nights"] == 0].set_index("origin")["share"]
print("share of day visits:", {o: round(float(day.get(o, 0)), 3) for o in U.ORIGINS})
U.check(np.allclose(sums, 1) and abs(day["Tilal region"] - 0.80) < 0.02 and "Europe" not in day.index,
        "shares add up to 1 inside each origin; 80% of local parties are day visits and no European party is")
try:
    c2 = hist_by_origin(shares)
except NotImplementedError:
    c2 = U.reference("d1_3", "hist_by_origin", shares)
U.keep("d1_3", "hist_by_origin", c2)
ch = U.channels(c2)
U.check(ch["y"].get("field") == "share" and ch.get("row", {}).get("field") == "origin" and not U.resolved(c2),
        "share on y, one row of panels per origin, shared scales")
U.show(c2, "d1_3_hist_by_origin")

# %% [markdown]
# ## 3 · Box plots by origin (5 min)
#
# A box plot draws five numbers: the median, the quartiles and the whiskers. It takes one line per group, which makes many groups easy to compare.
#
# ✏️ **Exercise** · Write `box_by_origin(df)`: `mark_boxplot()`, nights on x, origin on y.

# %%
def box_by_origin(df):
    # BEGIN SOLUTION
    return alt.Chart(df).mark_boxplot(size=24).encode(
        x=alt.X("nights:Q", title="Nights in the region"),
        y=alt.Y("origin:N", sort=U.ORIGINS, title=None),
    ).properties(height=220, title="Length of stay by origin market")
    # END SOLUTION


# %%
try:
    c3 = box_by_origin(stays)
except NotImplementedError:
    c3 = U.reference("d1_3", "box", stays)
U.keep("d1_3", "box", c3)
U.check("boxplot" in U.marks(c3) and U.field(c3, "x") == "nights" and U.field(c3, "y") == "origin", "a box plot of nights for each origin")
five = stays.groupby("origin")["nights"].quantile([0.25, 0.5, 0.75]).unstack().reindex(U.ORIGINS)
print(five.to_string())
U.show(c3, "d1_3_box")

# %% [markdown]
# ## 4 · The market with two kinds of trip (5 min)
#
# "Other regions" has a median of 3 nights and "Asia" of 4: close. Their histograms are not alike.
#
# ✏️ **Exercise** · Write `two_humps(shares)`: return the list of origins whose shares have a **valley**: some number of nights `k` (1 or more) where the share is below half of the largest share before `k` and below half of the largest share after `k`, and that later share is at least 0.05 (a hump, not a stray value in the tail).

# %%
def two_humps(shares):
    # BEGIN SOLUTION
    out = []
    for origin, g in shares.groupby("origin"):
        s = g.set_index("nights")["share"].reindex(range(0, int(g["nights"].max()) + 1), fill_value=0.0)
        for k in range(1, len(s) - 1):
            if s[k] < 0.5 * s[:k].max() and s[k] < 0.5 * s[k + 1:].max() and s[k + 1:].max() >= 0.05:
                out.append(origin)
                break
    return out
    # END SOLUTION


# %%
try:
    HUMPS = two_humps(shares)
except NotImplementedError:
    HUMPS = U.reference("d1_3", "humps")
U.keep("d1_3", "humps", HUMPS)
other = shares[shares["origin"] == "Other regions"].set_index("nights")["share"]
print("origins with a valley:", HUMPS)
print("Other regions, share of stays by nights:", {int(k): round(float(v), 3) for k, v in other.items() if k <= 10})
U.check(HUMPS == ["Other regions"], "only 'Other regions' has two humps: a weekend of 1 to 3 nights and a week of 5 to 9")
short = float(other[other.index <= 3].sum())
print(f"'Other regions': {short:.0%} of stays last 1 to 3 nights, {1 - short:.0%} last 5 or more; none last 4")

# %% [markdown]
# **Look at.** The median of "Other regions" is 3 nights, a length that belongs to the short trips only, and the box runs from 2 to 6 across the valley. The box plot is not wrong. It answers "where is the middle half" and was asked "what kinds of trip are there".

# %% [markdown]
# ## 5 · The reading (3 min)
#
# ✏️ **Exercise** · Two sentences that answer question 1 for the director. Say what the chart shows and one thing it does not show. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("Visitors do not all pop in and leave: 80% of parties from the Tilal region are day visits, while parties from Europe stay a median of 7 nights and parties from other regions come either for a weekend of 1 to 3 nights (63%) or for about a week. "
            "The chart shows how long parties stay, not how many people or how much money each kind of trip brings, and 320 stays with no recorded length are left out.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d1_3", "reading")
U.keep("d1_3", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["80%", "7 nights", ["weekend", "two kinds", "two humps", "1 to 3"], ["not", "left out"]])

# %% [markdown]
# ## ✱ Stretch · A bin too wide
#
# Draw the histogram of "Other regions" with bins seven nights wide.

# %%
def stretch():
    # BEGIN SOLUTION
    d = stays[stays["origin"] == "Other regions"]
    c = alt.Chart(d).mark_bar().encode(x=alt.X("nights:Q", bin=alt.Bin(step=7)), y="count():Q")
    counts = (d["nights"] // 7).value_counts().sort_index()
    print("stays per 7-night bin:", counts.to_dict(), "· the valley at 4 nights is gone: the first bin swallows both humps")
    return c
    # END SOLUTION


try:
    U.show(stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why shares and not counts in the panels?
#    <details><summary>Answer</summary>The markets differ in size. Counts on one scale flatten the small markets; shares put every market's shape on the same footing.</details>
# 2. Two markets have medians one night apart. What must you still look at?
#    <details><summary>Answer</summary>The shape. One is a single hump; the other has a weekend hump and a week hump with almost nothing at 4.</details>
# 3. When is a box plot the better choice?
#    <details><summary>Answer</summary>With many groups and one-humped distributions, when the question is about the middle and the spread, and when a note says how many values each box holds.</details>
#
# ## Carry forward
#
# The two kinds of trip from other regions return in lab 1.4, where one number has to describe them.
