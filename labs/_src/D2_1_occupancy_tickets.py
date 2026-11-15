# %% [markdown]
# # Lab 2.1 · Occupancy against ticket sales
#
# Day 2 · Session 1 (Two variables at once) · 25 min.
#
# Question 2 of the plan: on days when more tickets are sold at the sites, is a larger share of hotel rooms sold? Aws Al-Hudaif says yes, Rashed Al-Shalan is not sure. You bring the two tables to one unit, draw 43,840 points, watch them turn into a solid block, and make the relation visible with transparency, a binned heatmap and binned medians.
#
# **AI policy.** The tutor may hint at plotting syntax. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.occupancy()` (one hotel on one day) and `U.tickets()` (one sale). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Join hotel-days to daily ticket sales (4 min)
# - [ ] 2 · A scatter with transparency (5 min)
# - [ ] 3 · Bin both axes: a heatmap of counts (6 min)
# - [ ] 4 · Median occupancy by level of ticket sales (5 min)
# - [ ] 5 · One number at two units: hotel-days and weeks (3 min)
# - [ ] 6 · Write the reading (2 min)
# - [ ] ✱ Stretch · Colour the binned medians by weekend and weekday

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
occ = U.occupancy()
tix = U.tickets()
print(occ.head(3).to_string(), "\n")
print(tix.head(3).to_string())

# %% [markdown]
# ## 1 · One unit for both tables (4 min)
#
# A hotel-day cannot meet a ticket sale. Count the tickets per day, then give every hotel-day the tickets sold that day.
#
# ✏️ **Exercise** · Write `hotel_days(occ, tix)`: the occupancy table with two more columns, `tickets_day` (tickets sold at all sites on that date) and `rate` (rooms sold divided by rooms). Return the columns `date`, `hotel_id`, `rooms`, `rate`, `tickets_day`.

# %%
def hotel_days(occ, tix):
    # BEGIN SOLUTION
    daily = tix.groupby("sale_date")["tickets"].sum().rename("tickets_day")
    d = occ.join(daily, on="date")
    d["rate"] = d["rooms_sold"] / d["rooms"]
    return d[["date", "hotel_id", "rooms", "rate", "tickets_day"]]
    # END SOLUTION


# %%
try:
    hd = hotel_days(occ, tix)
    U.keep("d2_1", "shape", [len(hd), int(hd["tickets_day"].isna().sum())])
except NotImplementedError:
    U.reference("d2_1", "shape")
    hd = U.hotel_days()
print(len(hd), "hotel-days; tickets per day from", int(hd["tickets_day"].min()), "to", int(hd["tickets_day"].max()))
U.check(len(hd) == 43_840 and hd["tickets_day"].notna().all() and hd["rate"].between(0, 1).all(),
        "43,840 hotel-days, each with the day's ticket sales and a rate between 0 and 1: the join lost and added no row")

# %% [markdown]
# **Look at.** The number of rows did not change. A join that adds rows has repeated something; a join that loses rows has dropped something. Count before and after, every time.

# %% [markdown]
# ## 2 · A scatter with transparency (5 min)
#
# Drawn with solid points, 43,840 hotel-days form a block: where points overlap, one point and a thousand look the same. Transparency turns overlap into darkness.
#
# ✏️ **Exercise** · Write `scatter(df, opacity)`: `mark_circle` with the given opacity and a small size, `tickets_day` on x, `rate` on y.

# %%
def scatter(df, opacity):
    # BEGIN SOLUTION
    return alt.Chart(df[["tickets_day", "rate"]]).mark_circle(opacity=opacity, size=8).encode(
        x=alt.X("tickets_day:Q", title="Tickets sold at the sites that day"),
        y=alt.Y("rate:Q", title="Share of the hotel's rooms sold", axis=alt.Axis(format="%")),
    ).properties(title=f"43,840 hotel-days, opacity {opacity}")
    # END SOLUTION


# %%
pts = hd[["tickets_day", "rate"]]
try:
    c_solid, c_clear = scatter(hd, 1.0), scatter(hd, 0.04)
except NotImplementedError:
    c_solid, c_clear = U.reference("d2_1", "solid", pts), U.reference("d2_1", "clear", pts)
U.keep("d2_1", "solid", c_solid)
U.keep("d2_1", "clear", c_clear)
mp = U.mark_props(c_clear)
U.check(U.marks(c_clear) <= {"circle", "point"} and mp.get("opacity", 1) <= 0.1 and U.field(c_clear, "x") == "tickets_day" and U.field(c_clear, "y") == "rate",
        "points with an opacity of 0.1 or less, tickets on x, rate on y")
U.show(c_solid, "d2_1_scatter_solid")
U.show(c_clear, "d2_1_scatter_clear")

# %% [markdown]
# **Look at.** With opacity 0.04 a dark band rises from left to right. Notice the horizontal stripes: a hotel with 8 rooms can only be 0, 1/8, 2/8 ... full, so its points sit on nine lines. That is banding, a feature of the unit, not of tourism.

# %% [markdown]
# ## 3 · Bin both axes (6 min)
#
# A heatmap counts the points in each cell of a grid and shows the count as colour. Nothing overlaps, and the eye reads density directly.
#
# ✏️ **Exercise** · Write `heat(df)`: `mark_rect`, `tickets_day` binned on x (about 30 bins), `rate` binned on y (about 20 bins), the count of hotel-days as colour.

# %%
def heat(df):
    # BEGIN SOLUTION
    return alt.Chart(df[["tickets_day", "rate"]]).mark_rect().encode(
        x=alt.X("tickets_day:Q", bin=alt.Bin(maxbins=30), title="Tickets sold at the sites that day"),
        y=alt.Y("rate:Q", bin=alt.Bin(maxbins=20), title="Share of the hotel's rooms sold", axis=alt.Axis(format="%")),
        color=alt.Color("count():Q", title="Hotel-days", scale=alt.Scale(scheme="viridis")),
    ).properties(title="Where the 43,840 hotel-days are")
    # END SOLUTION


# %%
try:
    c_heat = heat(hd)
except NotImplementedError:
    c_heat = U.reference("d2_1", "heat", pts)
U.keep("d2_1", "heat", c_heat)
ch = U.channels(c_heat)
U.check(U.marks(c_heat) == {"rect"} and ch["x"].get("bin") and ch["y"].get("bin") and ch.get("color", {}).get("aggregate") == "count",
        "rectangles, both axes binned, colour for the count")
U.show(c_heat, "d2_1_heat")

# %% [markdown]
# ## 4 · Median occupancy by level of ticket sales (5 min)
#
# The heatmap shows where the points are. To read "how much", summarise y inside bins of x.
#
# ✏️ **Exercise** · Write `binned_median(df)`: cut `tickets_day` into 8 groups with equal numbers of hotel-days (`pd.qcut(..., 8)`), and return a table with one row per group: `tickets_mid` (the group's median tickets), `median_rate`, `hotel_days`.

# %%
def binned_median(df):
    # BEGIN SOLUTION
    g = df.groupby(pd.qcut(df["tickets_day"], 8), observed=True)
    return g.agg(tickets_mid=("tickets_day", "median"), median_rate=("rate", "median"), hotel_days=("rate", "size")).reset_index(drop=True)
    # END SOLUTION


# %%
try:
    bm = binned_median(hd)
except NotImplementedError:
    bm = U.reference("d2_1", "binned")
U.keep("d2_1", "binned", bm)
print(bm.round(3).to_string(index=False))
LOW, HIGH = float(bm["median_rate"].iloc[0]), float(bm["median_rate"].iloc[-1])
U.check(len(bm) == 8 and bm["median_rate"].is_monotonic_increasing and abs(LOW - 0.396) < 0.01 and abs(HIGH - 0.771) < 0.01,
        "median occupancy rises in every step, from about 40% on the quietest days to about 77% on the busiest")
c_med = alt.Chart(bm).mark_line(point=True).encode(
    x=alt.X("tickets_mid:Q", title="Tickets sold at the sites that day (median of each eighth)"),
    y=alt.Y("median_rate:Q", title="Median share of rooms sold", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
).properties(title="Median occupancy by level of ticket sales")
U.show(c_med, "d2_1_binned_median")

# %% [markdown]
# ## 5 · One number at two units (3 min)
#
# The correlation coefficient puts the relation into one number. Which number depends on the unit.
#
# ✏️ **Exercise** · Write `two_correlations(hd, weekly)`: the Pearson correlation of `rate` and `tickets_day` over hotel-days, and of `occupancy` and `tickets` over the 156 weeks of `U.weekly()`, as a pair.

# %%
def two_correlations(hd, weekly):
    # BEGIN SOLUTION
    return float(hd["rate"].corr(hd["tickets_day"])), float(weekly["occupancy"].corr(weekly["tickets"]))
    # END SOLUTION


# %%
wk = U.weekly()
try:
    R_HD, R_WEEK = two_correlations(hd, wk)
except NotImplementedError:
    R_HD, R_WEEK = U.reference("d2_1", "corr")
U.keep("d2_1", "corr", [R_HD, R_WEEK])
print(f"correlation over 43,840 hotel-days: {R_HD:.2f}; over 156 weeks, all hotels together: {R_WEEK:.2f}")
U.check(abs(R_HD - 0.39) < 0.02 and abs(R_WEEK - 0.70) < 0.02, "0.39 for hotel-days and 0.70 for weeks: the same data, two units, two numbers")

# %% [markdown]
# **Look at.** Adding up 40 hotels and 7 days averages away what is particular to one hotel on one day. The weekly number answers "does the region's occupancy move with the sites?"; the hotel-day number answers "can I tell one hotel's night from the day's ticket sales?". Neither is the correlation.

# %% [markdown]
# ## 6 · The reading (2 min)
#
# ✏️ **Exercise** · Two sentences that answer question 2. Say what the charts show and one thing they do not show. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("On the busiest eighth of days at the sites the median hotel sells 77% of its rooms, against 40% on the quietest eighth, and the median rises at every step in between. "
            "This shows that hotels and sites are busy together, not that visits to the sites fill the hotels: season and weekends drive both, and for a single hotel on a single day the link is loose (correlation 0.39).")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d2_1", "reading")
U.keep("d2_1", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["77%", "40%", ["not", "does not"]])

# %% [markdown]
# ## ✱ Stretch · Weekend and weekday
#
# Compute the binned medians separately for weekend days (`U.weekend(dates)`) and weekdays and draw two lines.

# %%
def stretch():
    # BEGIN SOLUTION
    d = hd.assign(day=np.where(U.weekend(hd["date"]), "Friday or Saturday", "Sunday to Thursday"))
    d["bin"] = pd.qcut(d["tickets_day"], 8)
    t = d.groupby(["day", "bin"], observed=True).agg(tickets_mid=("tickets_day", "median"), median_rate=("rate", "median")).reset_index()
    print(t.pivot(index="bin", columns="day", values="median_rate").round(3).to_string())
    return alt.Chart(t[["day", "tickets_mid", "median_rate"]]).mark_line(point=True).encode(x="tickets_mid:Q", y="median_rate:Q", color="day:N", strokeDash="day:N")
    # END SOLUTION


try:
    U.show(stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why did the first scatter look like a rectangle?
#    <details><summary>Answer</summary>Overplotting: once a place holds one solid point, more points there change nothing. 43,840 points hid where most of them are.</details>
# 2. What do the horizontal stripes mean?
#    <details><summary>Answer</summary>Small hotels can only take a few occupancy values. The stripes come from the unit of observation, not from visitors.</details>
# 3. The weekly correlation is 0.70, the hotel-day one 0.39. Which is right?
#    <details><summary>Answer</summary>Both, for different questions. Say the unit with the number, or the number means nothing.</details>
#
# ## Carry forward
#
# Lab 4.1 asks whether the weekly correlation could be chance and puts an interval on it. It starts from `U.weekly()`, not from this notebook.
