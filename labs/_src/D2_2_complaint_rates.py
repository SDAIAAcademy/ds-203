# %% [markdown]
# # Lab 2.2 · Complaint rates and small cells
#
# Day 2 · Session 2 (Counts, rates and denominators) · 25 min.
#
# Question 3 of the plan: how many complaints per thousand visitors does each site receive? The director heard that the Cable Car has "a lot of complaints". It also has the most visitors. You turn counts into rates, set the two rankings side by side, break the rates down by origin market and apply the board's publication rule to the cells that are too small to publish.
#
# **AI policy.** The tutor may hint at SQL and dataframe syntax. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.complaints()`, `U.tickets()` and `data/publication_rule.json`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Count complaints by site and rank the sites (3 min)
# - [ ] 2 · Visitors by site, and complaints per thousand visitors (6 min)
# - [ ] 3 · Set the two rankings side by side (3 min)
# - [ ] 4 · Rates by site and origin (5 min)
# - [ ] 5 · Apply the publication rule (5 min)
# - [ ] 6 · Write the reading (3 min)
# - [ ] ✱ Stretch · Show that one withheld cell can be recovered from the row total

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
complaints = U.complaints()
tickets = U.tickets()
RULE = U.js("publication_rule.json")
print(len(complaints), "complaints ·", int(tickets["tickets"].sum()), "visitors (tickets sold)")
print(RULE["rule"])

# %% [markdown]
# ## 1 · Counts (3 min)
#
# ✏️ **Exercise** · Write `counts_by_site(complaints)`: a series of the number of complaints per site, largest first.

# %%
def counts_by_site(complaints):
    # BEGIN SOLUTION
    return complaints.groupby("site").size().sort_values(ascending=False).rename("complaints")
    # END SOLUTION


# %%
try:
    COUNTS = counts_by_site(complaints)
except NotImplementedError:
    COUNTS = U.reference("d2_2", "counts")
U.keep("d2_2", "counts", COUNTS)
print(COUNTS.to_string())
U.check(COUNTS.index[0] == "Cable Car" and int(COUNTS.iloc[0]) == 599, "the Cable Car has the most complaints: 599 of 2,418")

# %% [markdown]
# ## 2 · A denominator (6 min)
#
# A count compares sites only if they are the same size. The fair comparison divides by what was exposed to the risk of complaining: visitors. One ticket is one visitor.
#
# ✏️ **Exercise** · Write `rates_by_site(complaints, tickets)` with one SQL statement (`duckdb.sql(...).df()`): one row per site with `complaints`, `visitors` (the sum of `tickets`) and `per_thousand` (complaints per thousand visitors). Aggregate each table to one row per site **before** joining.

# %%
def rates_by_site(complaints, tickets):
    # BEGIN SOLUTION
    return duckdb.sql("""
        WITH c AS (SELECT site, count(*) AS complaints FROM complaints GROUP BY site),
             v AS (SELECT site, sum(tickets) AS visitors FROM tickets GROUP BY site)
        SELECT v.site, c.complaints, v.visitors, 1000.0 * c.complaints / v.visitors AS per_thousand
        FROM v JOIN c USING (site)
        ORDER BY per_thousand DESC
    """).df()
    # END SOLUTION


# %%
try:
    RATES = rates_by_site(complaints, tickets)
except NotImplementedError:
    RATES = U.reference("d2_2", "rates")
U.keep("d2_2", "rates", RATES)
RATES = RATES.sort_values("per_thousand", ascending=False).reset_index(drop=True)
print(RATES.round(2).to_string(index=False))
by = RATES.set_index("site")
U.check(int(RATES["complaints"].sum()) == 2418 and int(RATES["visitors"].sum()) == int(tickets["tickets"].sum()),
        "no complaint and no visitor was lost or doubled in the join")
U.check(RATES["site"].iloc[0] == "Terrace Farms" and abs(by.loc["Terrace Farms", "per_thousand"] - 13.82) < 0.05 and abs(by.loc["Cable Car", "per_thousand"] - 5.94) < 0.05,
        "Terrace Farms has the highest rate, 13.8 per thousand; the Cable Car has 5.9")

# %% [markdown]
# **Look at.** Joining the two raw tables on `site` first would pair every complaint at a site with every sale at that site: millions of rows and a rate that means nothing. Bring each table to the unit of the answer, then join.

# %% [markdown]
# ## 3 · Two rankings (3 min)
#
# ✏️ **Exercise** · Write `two_ranks(rates)`: the table with two more columns, `rank_count` and `rank_rate` (1 is highest), sorted by `rank_count`.

# %%
def two_ranks(rates):
    # BEGIN SOLUTION
    r = rates.copy()
    r["rank_count"] = r["complaints"].rank(ascending=False).astype(int)
    r["rank_rate"] = r["per_thousand"].rank(ascending=False).astype(int)
    return r.sort_values("rank_count").reset_index(drop=True)
    # END SOLUTION


# %%
try:
    RANKS = two_ranks(RATES)
except NotImplementedError:
    RANKS = U.reference("d2_2", "ranks")
U.keep("d2_2", "ranks", RANKS)
print(RANKS[["site", "complaints", "visitors", "per_thousand", "rank_count", "rank_rate"]].round(2).to_string(index=False))
rk = RANKS.set_index("site")
U.check(rk.loc["Cable Car", "rank_count"] == 1 and rk.loc["Cable Car", "rank_rate"] == 5 and rk.loc["Terrace Farms", "rank_count"] == 7 and rk.loc["Terrace Farms", "rank_rate"] == 1,
        "first by count is fifth by rate; seventh by count is first by rate")
c_rate = alt.Chart(RATES).mark_bar().encode(
    y=alt.Y("site:N", sort="-x", title=None), x=alt.X("per_thousand:Q", title="Complaints per thousand visitors, 2023 to 2025"),
).properties(title="By rate, the small sites lead")
U.show(c_rate, "d2_2_rates")

# %% [markdown]
# ## 4 · Rates by site and origin (5 min)
#
# Atheer Al-Muhaya wants the table split by origin market, for the public report.
#
# ✏️ **Exercise** · Write `cells(complaints, tickets)`: one row per site and origin (all 45 combinations) with `complaints`, `visitors` and `per_thousand`. A combination with visitors and no complaint must appear with 0 complaints.

# %%
def cells(complaints, tickets):
    # BEGIN SOLUTION
    v = tickets.groupby(["site", "origin"])["tickets"].sum().rename("visitors")
    c = complaints.groupby(["site", "origin"]).size().rename("complaints")
    t = pd.concat([c, v], axis=1).fillna({"complaints": 0}).reset_index()
    t["complaints"] = t["complaints"].astype(int)
    t["per_thousand"] = t["complaints"] / t["visitors"] * 1000
    return t
    # END SOLUTION


# %%
try:
    CELLS = cells(complaints, tickets)
except NotImplementedError:
    CELLS = U.reference("d2_2", "cells")
U.keep("d2_2", "cells", CELLS)
print(CELLS.sort_values("per_thousand", ascending=False).head(6).round(2).to_string(index=False))
U.check(len(CELLS) == 45 and int(CELLS["complaints"].sum()) == 2418, "45 cells that still add up to 2,418 complaints")

# %% [markdown]
# ## 5 · The publication rule (5 min)
#
# A rate from 4 complaints among 321 visitors moves by a quarter if one more visitor complains, and a small cell can point at identifiable people. The board's own rule, in `publication_rule.json`: a cell with fewer than 10 complaints or fewer than 1,000 visitors is not published. It follows the board's reading of the open-data and classification policies it works under; the thresholds are the board's.
#
# ✏️ **Exercise** · Write `apply_rule(cells, rule)`: the table with a column `publish` (True or False), and `shown`, which is the rate rounded to one decimal as text for a published cell and `"withheld"` for the others.

# %%
def apply_rule(cells, rule):
    # BEGIN SOLUTION
    t = cells.copy()
    t["publish"] = (t["complaints"] >= rule["min_complaints"]) & (t["visitors"] >= rule["min_visitors"])
    t["shown"] = np.where(t["publish"], t["per_thousand"].round(1).astype(str), "withheld")
    return t
    # END SOLUTION


# %%
try:
    PUB = apply_rule(CELLS, RULE)
except NotImplementedError:
    PUB = U.reference("d2_2", "pub")
U.keep("d2_2", "pub", PUB)
held = PUB[~PUB["publish"].astype(bool)]
print(held[["site", "origin", "complaints", "visitors"]].to_string(index=False))
print()
print(PUB.pivot(index="site", columns="origin", values="shown")[U.ORIGINS].to_string())
U.check(len(held) == 4 and set(held["site"]) == {"Terrace Farms", "Honey Museum", "Cloud Lookout"},
        "four cells are withheld, all for visitors from Asia or Europe at three smaller sites")

# %% [markdown]
# **Look at.** Two of the four withheld cells would have shown rates above 12 per thousand, among the highest in the table, resting on 6 and 4 complaints. The rule removes exactly the numbers a headline would have picked.

# %% [markdown]
# ## 6 · The reading (3 min)
#
# ✏️ **Exercise** · Two sentences that answer question 3 for the director. Give every rate with its denominator, and say what is not published. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("The Cable Car has the most complaints (599) because it has the most visitors (100,822): its rate, 5.9 per thousand visitors, is fifth of nine, while Terrace Farms has 13.8 per thousand (167 complaints among 12,083 visitors) and the Wadi Trail 11.4. "
            "By origin market, four site-by-origin cells rest on fewer than 10 complaints or 1,000 visitors and are withheld, so the table does not show whether visitors from Asia or Europe complain more at the small sites.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d2_2", "reading")
U.keep("d2_2", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["5.9", "13.8", ["per thousand", "per 1,000"], ["withheld", "not published", "suppressed"]])

# %% [markdown]
# ## ✱ Stretch · A withheld cell that can be recovered
#
# The public table also prints each site's total. Take a site with exactly one withheld cell and recover its complaints from the total and the four published cells.

# %%
def stretch():
    # BEGIN SOLUTION
    n_held = (~PUB["publish"].astype(bool)).groupby(PUB["site"]).sum()
    site = n_held[n_held == 1].index[0]
    row = PUB[PUB["site"] == site]
    total = int(row["complaints"].sum())
    shown = int(row.loc[row["publish"].astype(bool), "complaints"].sum())
    print(f"{site}: total {total}, published cells {shown}, so the withheld cell holds {total - shown} complaints")
    print("A second cell in the row or the total must be withheld as well. Differencing is treated in DS-207.")
    return total - shown
    # END SOLUTION


try:
    U.keep("d2_2", "recovered", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is "599 complaints" not evidence that the Cable Car is the worst site?
#    <details><summary>Answer</summary>It has the most visitors. Per thousand visitors it is fifth of nine.</details>
# 2. Why aggregate before joining?
#    <details><summary>Answer</summary>The tables have different units. A join of raw rows on site pairs every complaint with every sale and multiplies both.</details>
# 3. A cell shows 12.5 complaints per thousand visitors from 4 complaints. Why is it withheld?
#    <details><summary>Answer</summary>One complaint more or less moves the rate by a quarter, and so small a group can point at particular people.</details>
#
# ## Carry forward
#
# The count chart of the earlier report returns in lab 3.3 as one of six misleading charts. Small cells, differencing and the classification of outputs are the subject of DS-207.
