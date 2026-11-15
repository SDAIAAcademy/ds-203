# %% [markdown]
# # Lab 2.3 · Monthly arrivals, season and festivals
#
# Day 2 · Session 3 (Change over time) · 25 min.
#
# Question 4 of the plan: by how much did arrivals in each festival month exceed what season and trend lead us to expect? The board ran the Honey Festival in October 2024 and October 2025 and Heritage Nights in February 2025. You draw three years of monthly arrivals, separate the summer season from the trend, see why "the same month last year" finds one festival and misses another, and build a baseline that finds all three months.
#
# **AI policy.** The tutor may hint at plotting syntax. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.monthly_total()`: 36 months of total arrivals, from `data/arrivals.csv`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · A line chart of monthly arrivals (4 min)
# - [ ] 2 · The seasonal profile of a festival-free year (5 min)
# - [ ] 3 · Change on the same month a year earlier (5 min)
# - [ ] 4 · A baseline from season and trend; the months above it (7 min)
# - [ ] 5 · Mark the festival months and write the reading (4 min)
# - [ ] ✱ Stretch · Repeat the baseline for one origin market

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
m = U.monthly_total()
m["year"], m["moy"] = m["month"].dt.year, m["month"].dt.month
print(m.head(3).to_string(), f"\n{len(m)} months")

# %% [markdown]
# ## 1 · The line (4 min)
#
# Time goes on x, in order and to scale. A line says "these points follow one another".
#
# ✏️ **Exercise** · Write `line(m)`: a line with a point at each month, `month` on x as a time, `arrivals` on y from zero.

# %%
def line(m):
    # BEGIN SOLUTION
    return alt.Chart(m).mark_line(point=True).encode(
        x=alt.X("month:T", title=None),
        y=alt.Y("arrivals:Q", title="Arrivals per month", scale=alt.Scale(zero=True)),
    ).properties(title="Monthly arrivals, all origin markets", width=620)
    # END SOLUTION


# %%
try:
    c_line = line(m)
except NotImplementedError:
    c_line = U.reference("d2_3", "line", m)
U.keep("d2_3", "line", c_line)
ch = U.channels(c_line)
U.check("line" in U.marks(c_line) and ch["x"].get("type") == "temporal" and ch["y"].get("field") == "arrivals", "a line of arrivals over time, x as a time axis")
U.show(c_line, "d2_3_line")

# %% [markdown]
# **Look at.** Three summer peaks, each higher than the last, and three spikes that are not in summer. Peak, rise and spike are season, trend and event. The rest of the lab pulls them apart.

# %% [markdown]
# ## 2 · The seasonal profile (5 min)
#
# 2023 had no festival. Its shape is the season. A **seasonal index** divides each month by the year's monthly average: 1.0 is an average month.
#
# ✏️ **Exercise** · Write `seasonal_index(m)`: a series indexed by month of the year (1 to 12) with the 2023 arrivals of that month divided by the mean of the twelve 2023 months.

# %%
def seasonal_index(m):
    # BEGIN SOLUTION
    y = m[m["year"] == 2023].set_index("moy")["arrivals"]
    return (y / y.mean()).rename("index")
    # END SOLUTION


# %%
try:
    IDX = seasonal_index(m)
except NotImplementedError:
    IDX = U.reference("d2_3", "index")
IDX.index = [int(i) for i in IDX.index]
U.keep("d2_3", "index", IDX)
print({k: round(float(v), 2) for k, v in IDX.items()})
U.check(abs(IDX.mean() - 1) < 1e-9 and int(IDX.idxmax()) == 7 and abs(IDX[7] - 1.43) < 0.01 and abs(IDX[1] - 0.78) < 0.01,
        "July is 43% above an average month and January 22% below")

# %% [markdown]
# ## 3 · The same month a year earlier (5 min)
#
# Comparing October with September mixes the festival with the end of summer. Comparing October with last October removes the season.
#
# ✏️ **Exercise** · Write `year_on_year(m)`: the table with a column `yoy`, arrivals divided by arrivals twelve months earlier, minus 1 (missing for 2023).

# %%
def year_on_year(m):
    # BEGIN SOLUTION
    t = m.sort_values("month").copy()
    t["yoy"] = t["arrivals"] / t["arrivals"].shift(12) - 1
    return t
    # END SOLUTION


# %%
try:
    YOY = year_on_year(m)
except NotImplementedError:
    YOY = U.reference("d2_3", "yoy")
    YOY["month"] = pd.to_datetime(YOY["month"])
U.keep("d2_3", "yoy", YOY)
y = YOY.dropna(subset=["yoy"]).assign(label=lambda d: pd.to_datetime(d["month"]).dt.strftime("%Y-%m")).set_index("label")["yoy"]
print({k: f"{v:+.0%}" for k, v in y.items()})
TYPICAL = float(y.median())
print(f"typical change on a year earlier (median of 24 months): {TYPICAL:+.1%}")
U.check(abs(y["2024-10"] - 0.374) < 0.005 and abs(y["2025-02"] - 0.270) < 0.005 and abs(y["2025-10"] - 0.071) < 0.005,
        "October 2024 is up 37% and February 2025 up 27% on a year earlier; October 2025 is up 7%, an ordinary month")

# %% [markdown]
# **Look at.** October 2025 had a festival and looks ordinary. It is compared with October 2024, which had the same festival. A year-on-year change measures the difference between two years, and an event that repeats disappears from it.

# %% [markdown]
# ## 4 · A baseline from season and trend (7 min)
#
# Build what each month would have been without an event: the same month of 2023 (the season), grown by the typical yearly growth (the trend).
#
# ✏️ **Exercise** · Write `with_baseline(m, growth)`: the table with `baseline` = arrivals of the same month of 2023 times `(1 + growth)` to the power of years since 2023, and `excess` = arrivals divided by baseline, minus 1.
# Then `above(t, threshold)`: the list of months (as `"YYYY-MM"`) after 2023 whose excess is above the threshold.

# %%
def with_baseline(m, growth):
    # BEGIN SOLUTION
    t = m.sort_values("month").copy()
    y2023 = t[t["year"] == 2023].set_index("moy")["arrivals"]
    t["baseline"] = t["moy"].map(y2023) * (1 + growth) ** (t["year"] - 2023)
    t["excess"] = t["arrivals"] / t["baseline"] - 1
    return t
    # END SOLUTION


def above(t, threshold):
    # BEGIN SOLUTION
    hit = t[(t["year"] > 2023) & (t["excess"] > threshold)]
    return list(pd.to_datetime(hit["month"]).dt.strftime("%Y-%m"))
    # END SOLUTION


# %%
try:
    BASE = with_baseline(m, TYPICAL)
except NotImplementedError:
    BASE = U.reference("d2_3", "base")
    BASE["month"] = pd.to_datetime(BASE["month"])
U.keep("d2_3", "base", BASE)
try:
    HITS = above(BASE, 0.10)
except NotImplementedError:
    HITS = U.reference("d2_3", "hits")
U.keep("d2_3", "hits", HITS)
ex = BASE[BASE["year"] > 2023].assign(label=lambda d: pd.to_datetime(d["month"]).dt.strftime("%Y-%m")).set_index("label")
print("months more than 10% above the baseline:", HITS)
for k in HITS:
    print(f"  {k}: {int(ex.loc[k, 'arrivals']):,} arrivals against a baseline of {ex.loc[k, 'baseline']:,.0f}: {ex.loc[k, 'excess']:+.0%}, about {ex.loc[k, 'arrivals'] - ex.loc[k, 'baseline']:,.0f} extra")
rest = ex.drop(index=HITS)["excess"]
print(f"the other {len(rest)} months lie between {rest.min():+.1%} and {rest.max():+.1%} of the baseline")
U.check(HITS == ["2024-10", "2025-02", "2025-10"], "the baseline finds all three festival months, and only those")
U.check(abs(ex.loc["2025-10", "excess"] - 0.288) < 0.01 and rest.abs().max() < 0.06, "both Octobers are about 29% above the baseline; no other month is more than 5% away from it")

# %% [markdown]
# ## 5 · Mark the months, write the reading (4 min)
#
# The chart below is supplied: actual arrivals as a line, the baseline as a dashed line, the three months marked. Read it, then write.
#
# ✏️ **Exercise** · Two sentences that answer question 4. Say what the chart shows and what it cannot show. Assistant off.

# %%
long = pd.concat([BASE.assign(series="Arrivals", value=BASE["arrivals"]), BASE.assign(series="Baseline: 2023 season with trend", value=BASE["baseline"])])[["month", "series", "value"]]
long["month"] = pd.to_datetime(long["month"])
marks = BASE[pd.to_datetime(BASE["month"]).dt.strftime("%Y-%m").isin(HITS)][["month", "arrivals"]].assign(month=lambda d: pd.to_datetime(d["month"]))
c_base = alt.layer(
    alt.Chart(long).mark_line().encode(x=alt.X("month:T", title=None), y=alt.Y("value:Q", title="Arrivals per month", scale=alt.Scale(zero=True)),
                                       color=alt.Color("series:N", title=None, scale=alt.Scale(range=[U.OKABE_ITO[0], "#777777"])), strokeDash=alt.StrokeDash("series:N", legend=None)),
    alt.Chart(marks).mark_point(size=160, shape="diamond", filled=True, color=U.OKABE_ITO[4]).encode(x="month:T", y="arrivals:Q"),
).properties(title="Three months stand above the seasonal baseline", width=620)
U.show(c_base, "d2_3_baseline")


def reading():
    # BEGIN SOLUTION
    return ("Arrivals follow a summer season (July is 43% above an average month) on a trend of about 7% a year, and three months stand apart from it: October 2024 and October 2025, each about 29% above the seasonal baseline, and February 2025, 18% above; no other month is more than 5% from the baseline. "
            "The chart shows that the festival months had roughly 12,000 to 21,000 more arrivals than season and trend predict, not that the festivals caused them or that those visitors would not have come in another month.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d2_3", "reading")
U.keep("d2_3", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["29%", "18%", ["baseline", "expected"], ["not", "cannot"]])

# %% [markdown]
# ## ✱ Stretch · One market
#
# Repeat the baseline for arrivals from the Gulf and compare its excess in the festival months with the total's.

# %%
def stretch():
    # BEGIN SOLUTION
    a = U.arrivals()
    g = a[a["origin"] == "Gulf"].drop(columns="origin").assign(year=lambda d: d["month"].dt.year, moy=lambda d: d["month"].dt.month)
    growth = float(year_on_year(g)["yoy"].median())
    b = with_baseline(g, growth).assign(label=lambda d: d["month"].dt.strftime("%Y-%m")).set_index("label")
    out = {k: round(float(b.loc[k, "excess"]), 3) for k in ["2024-10", "2025-02", "2025-10"]}
    print(f"Gulf: typical growth {growth:+.0%}; excess in the festival months {out}: smaller than the total's, the festivals drew mostly visitors from inside the Kingdom")
    return out
    # END SOLUTION


try:
    U.keep("d2_3", "gulf", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is October compared with other Octobers and not with September?
#    <details><summary>Answer</summary>September to October includes the end of the summer season. The same month of another year has the same season.</details>
# 2. Why did the year-on-year change miss October 2025?
#    <details><summary>Answer</summary>It compares with October 2024, which had the same festival. A repeated event cancels out of a year-on-year change.</details>
# 3. What does "29% above the baseline" assume?
#    <details><summary>Answer</summary>That 2023 shows the season without events and that growth is steady. If either is wrong, so is the excess.</details>
#
# ## Carry forward
#
# Lab 3.2 draws the same arrivals by origin market in small multiples; lab 3.3 repairs a chart that picked two of these 36 months. Forecasting from season and trend is the subject of DS-304.
