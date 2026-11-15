# %% [markdown]
# # Lab 3.3 · Repair six misleading charts
#
# Day 3 · Session 3 (Charts that mislead) · 25 min.
#
# Last year's board report had six charts drawn by Nayef Al-Jumaah. Every number in them is correct and every one leaves a wrong impression. You name the fault of each, repair it by changing the scale, the window, the measure or the encoding, and write what a reader now concludes.
#
# **AI policy.** The tutor may hint at plotting syntax. Naming the faults and the reading are your own first draft, assistant off.
#
# **Reference state.** `U.misleading(k)` for k from 1 to 6 returns the chart as published, the data a repair needs and the chart's headline. The code of each original is in `tilal.py`; start your repair from it. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Name the fault of each of the six charts (5 min)
# - [ ] 2 · Repair charts 1 to 3: baseline, window, rate (9 min)
# - [ ] 3 · Repair charts 4 to 6: two axes, running total, time steps (9 min)
# - [ ] 4 · Write what a reader now concludes (2 min)
# - [ ] ✱ Stretch · Find a seventh chart in your own work and name its fault

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
ORIG = {k: U.misleading(k) for k in range(1, 7)}
for k, (chart, data, headline) in ORIG.items():
    print(f"chart {k}: \"{headline}\" · marks {sorted(U.marks(chart))} · data handed to the repair: {list(data.columns)} ({len(data)} rows)")

# %%
# Run this cell once for each k and look at the chart before you name its fault.
k = 1
U.show(ORIG[k][0], f"d3_3_orig_{k}")

# %%
for k in range(2, 7):
    U.show(ORIG[k][0], f"d3_3_orig_{k}")
print("fault names:", list(U.FAULTS))

# %% [markdown]
# ## 1 · Name the faults (5 min)
#
# The fault list of this session, in `U.FAULTS`: `cut baseline`, `picked window`, `count for rate`, `two axes`, `running total`, `uneven steps`, `colour only`, `no fault`.
#
# ✏️ **Exercise** · Return a dictionary: chart number to the name of its fault. Each chart has one, and no name is used twice.

# %%
def faults():
    # BEGIN SOLUTION
    return {1: "cut baseline", 2: "picked window", 3: "count for rate", 4: "two axes", 5: "running total", 6: "uneven steps"}
    # END SOLUTION


# %%
try:
    NAMED = faults()
except NotImplementedError:
    NAMED = U.reference("d3_3", "faults")
NAMED = {int(k): v for k, v in NAMED.items()}
U.keep("d3_3", "faults", NAMED)
for k in sorted(NAMED):
    print(f" · chart {k}: {NAMED[k]}: {U.FAULTS.get(NAMED[k], '?')}")
U.check(U.matches("d3_3", "faults_key", {str(k): v for k, v in NAMED.items()}), "six charts, six faults, each named")

# %% [markdown]
# ## 2 · Repair charts 1 to 3 (9 min)
#
# **Chart 1** shows mean satisfaction by year as bars on an axis from 4.0 to 4.2. A bar's length is its message: cut the axis and a fall of 2% looks like a collapse.
# **Chart 2** compares two Octobers and leaves out the other 34 months. **Chart 3** ranks sites by the number of complaints.
#
# ✏️ **Exercise** · Write the three repairs. Each takes the data of `U.misleading(k)[1]`.
# - `repair1(s)`: the same bars on the full scale, from 0 to 5.
# - `repair2(m)`: all 36 months as a line, so the two Octobers can be seen in context.
# - `repair3(r)`: complaints per thousand visitors, sorted.

# %%
def repair1(s):
    # BEGIN SOLUTION
    return alt.Chart(s).mark_bar().encode(
        x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("satisfaction:Q", title="Mean satisfaction, 1 to 5", scale=alt.Scale(domain=[0, 5])),
    ).properties(title="Mean satisfaction: 4.14, 4.15, 4.07", width=300)
    # END SOLUTION


def repair2(m):
    # BEGIN SOLUTION
    return alt.Chart(m).mark_line(point=True).encode(
        x=alt.X("month:T", title=None), y=alt.Y("arrivals:Q", title="Arrivals per month", scale=alt.Scale(zero=True)),
    ).properties(title="October 2024 was a festival month; the trend is about 7% a year", width=600)
    # END SOLUTION


def repair3(r):
    # BEGIN SOLUTION
    return alt.Chart(r).mark_bar().encode(
        y=alt.Y("site:N", sort="-x", title=None), x=alt.X("per_thousand:Q", title="Complaints per thousand visitors, 2023 to 2025"),
    ).properties(title="By rate, Terrace Farms and the Wadi Trail lead")
    # END SOLUTION


# %%
def rows(chart):
    """The largest number of rows any dataset of the chart holds."""
    return max(len(v) for v in chart.to_dict()["datasets"].values())


FIX = {}
for k, fn in ((1, repair1), (2, repair2), (3, repair3)):
    try:
        FIX[k] = fn(ORIG[k][1])
    except NotImplementedError:
        FIX[k] = U.reference("d3_3", f"fix{k}")
    U.keep("d3_3", f"fix{k}", FIX[k])
    U.show(FIX[k], f"d3_3_fix_{k}")
y1 = U.channels(FIX[1])["y"].get("scale", {})
U.check("bar" not in U.marks(FIX[1]) or y1.get("domain", [0])[0] == 0, "chart 1: bars measured from zero (or no bars at all)")
U.check(rows(FIX[2]) >= 36 and U.channels(FIX[2])["x"].get("type") == "temporal", "chart 2: every one of the 36 months is on the chart, on a time axis")
U.check("per_thousand" in (U.field(FIX[3], "x"), U.field(FIX[3], "y")), "chart 3: a rate, not a count")

# %% [markdown]
# **Look at.** On chart 1 the fall from 4.15 to 4.07 is now barely visible, which is what a fall of 2% of the value looks like. If such a difference matters, bars are the wrong mark: points on an axis that starts at 4 would be honest, because a point's message is its position, not its length.

# %% [markdown]
# ## 3 · Repair charts 4 to 6 (9 min)
#
# **Chart 4** draws weekly tickets and hotel occupancy on two y axes, each stretched until the lines meet: with two free axes any two series can be made to "follow each other". **Chart 5** is a running total of local arrivals, and a running total can only rise. **Chart 6** steps through two years, a half-year and two months as if they were equal periods.
#
# ✏️ **Exercise** · Write the three repairs.
# - `repair4(w)`: one axis for each variable: a scatter of weekly occupancy against weekly tickets.
# - `repair5(r)`: arrivals per month from the Tilal region, not the running total, from zero.
# - `repair6(m)`: periods of equal length: the three yearly totals as bars, or all 36 months as a line.

# %%
def repair4(w):
    # BEGIN SOLUTION
    return alt.Chart(w).mark_circle(size=40, opacity=0.6).encode(
        x=alt.X("tickets:Q", title="Tickets sold per week", scale=alt.Scale(zero=False)),
        y=alt.Y("occupancy:Q", title="Share of hotel rooms sold in the week", axis=alt.Axis(format="%"), scale=alt.Scale(zero=False)),
    ).properties(title="Busier weeks at the sites are fuller weeks at the hotels, loosely")
    # END SOLUTION


def repair5(r):
    # BEGIN SOLUTION
    return alt.Chart(r).mark_line().encode(
        x=alt.X("month:T", title=None), y=alt.Y("arrivals:Q", title="Arrivals per month from the Tilal region", scale=alt.Scale(zero=True)),
    ).properties(title="Local arrivals are drifting down", width=600)
    # END SOLUTION


def repair6(m):
    # BEGIN SOLUTION
    yearly = m.assign(year=m["month"].dt.year).groupby("year", as_index=False)["arrivals"].sum()
    return alt.Chart(yearly).mark_bar().encode(
        x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)), y=alt.Y("arrivals:Q", title="Arrivals in the year"),
    ).properties(title="Arrivals rose in both years", width=300)
    # END SOLUTION


# %%
for k, fn in ((4, repair4), (5, repair5), (6, repair6)):
    try:
        FIX[k] = fn(ORIG[k][1])
    except NotImplementedError:
        FIX[k] = U.reference("d3_3", f"fix{k}")
    U.keep("d3_3", f"fix{k}", FIX[k])
    U.show(FIX[k], f"d3_3_fix_{k}")
U.check(U.resolved(FIX[4]).get("scale", {}).get("y") != "independent" and {U.field(FIX[4], "x"), U.field(FIX[4], "y")} == {"tickets", "occupancy"},
        "chart 4: one variable on each axis, no second y axis")
U.check(U.field(FIX[5], "y") == "arrivals", "chart 5: arrivals per month, not their running total")
x6 = U.channels(FIX[6])["x"]
U.check(x6.get("field") != "period" and (x6.get("field") == "year" or (x6.get("type") == "temporal" and rows(FIX[6]) >= 36)), "chart 6: steps of equal length on the time axis")
loc = ORIG[5][1].assign(year=lambda d: d["month"].dt.year).groupby("year")["arrivals"].sum()
yr = ORIG[6][1].assign(year=lambda d: d["month"].dt.year).groupby("year")["arrivals"].sum()
print("local arrivals by year:", loc.to_dict(), f"· change 2023 to 2025: {loc[2025] / loc[2023] - 1:+.1%}")
print("all arrivals by year:", yr.to_dict(), f"· change 2023 to 2025: {yr[2025] / yr[2023] - 1:+.1%}")

# %% [markdown]
# ## 4 · What a reader now concludes (2 min)
#
# ✏️ **Exercise** · Two sentences: what the six repaired charts say together, and one thing even the repaired charts do not show. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("Repaired, the six charts say that satisfaction moved from 4.15 to 4.07 and did not collapse, that arrivals grew by about 7% a year with a festival spike and did not jump 37%, that the highest complaint rates are at two small sites and not at the Cable Car, that hotels and sites move together only loosely, that local arrivals fell by 6% over two years and that total arrivals rose in both years. "
            "None of the charts shows uncertainty, so they do not tell a reader which of these differences could be chance.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d3_3", "reading")
U.keep("d3_3", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["4.07", ["rate", "per thousand"], ["not", "do not"]])

# %% [markdown]
# ## ✱ Stretch · The seventh chart
#
# Take one chart you made in the last year. Write its headline, its fault from `U.FAULTS` (or `"no fault"`) and the repair in one line.

# %%
def stretch():
    # BEGIN SOLUTION
    return {"headline": "Call volume doubled", "fault": "picked window", "repair": "show all 24 months, not the quietest and the busiest"}
    # END SOLUTION


try:
    print(stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Is an axis that does not start at zero always a fault?
#    <details><summary>Answer</summary>No. It is a fault for marks whose length or area is the message (bars, areas). Points and lines show position, and may use the range of the data, clearly labelled.</details>
# 2. Why can a chart with two y axes not be trusted to show that two series move together?
#    <details><summary>Answer</summary>Each axis can be stretched and shifted freely, so the lines can be made to meet or cross anywhere. Plot one against the other.</details>
# 3. Every number in the six originals was correct. What was wrong?
#    <details><summary>Answer</summary>The mapping from numbers to ink: the scale, the window, the measure or the encoding led the eye to a comparison the numbers do not support.</details>
#
# ## Carry forward
#
# The repaired chart 1 has no intervals. Lab 4.2 adds them to a satisfaction chart.
