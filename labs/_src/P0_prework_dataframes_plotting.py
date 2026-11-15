# %% [markdown]
# # Pre-work · Dataframes and a first chart
#
# Before Day 1 · about two hours, at your own pace.
#
# The course assumes that you can filter, group and join a table in Python or SQL (FN-101, FN-104), that you have met the bootstrap and the permutation test (DS-201) and that you can make a basic chart in some plotting library. This notebook lets you check the first and the last of these on the tables of the course, and shows you the plotting library the labs use, Vega-Altair. If an exercise takes you far longer than its time, revise that topic before Day 1.
#
# **AI policy.** This is practice, so use any help you like. In the course itself, quizzes and the first draft of every chart reading are done without an assistant.
#
# **Reference state.** `U.arrivals()` and `U.tickets()`, as supplied. Nothing else is needed.
#
# **Tasks**
# - [ ] 1 · Filter and sort (15 min)
# - [ ] 2 · Group and summarise (20 min)
# - [ ] 3 · The same summary in SQL (20 min)
# - [ ] 4 · Bring two tables to one unit and join (25 min)
# - [ ] 5 · A first chart in Altair (25 min)
# - [ ] 6 · Read the data dictionary and the brief (15 min)

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
arrivals = U.arrivals()
tickets = U.tickets()
print(arrivals.head(3).to_string(index=False))
print(tickets.head(3).to_string(index=False))

# %% [markdown]
# ## 1 · Filter and sort (15 min)
#
# ✏️ **Exercise** · Write `gulf_2025(a)`: the rows of `arrivals` for the origin `"Gulf"` in 2025, sorted from the month with the most arrivals to the month with the fewest.

# %%
def gulf_2025(a):
    # BEGIN SOLUTION
    return a[(a["origin"] == "Gulf") & (a["month"].dt.year == 2025)].sort_values("arrivals", ascending=False)
    # END SOLUTION


# %%
try:
    G = gulf_2025(arrivals)
except NotImplementedError:
    G = U.reference("p0", "gulf").assign(month=lambda d: pd.to_datetime(d["month"]))
U.keep("p0", "gulf", G)
print(G.head(3).to_string(index=False))
U.check(len(G) == 12 and G["arrivals"].is_monotonic_decreasing and G["month"].iloc[0].month == 7, "twelve months of 2025, July first")

# %% [markdown]
# ## 2 · Group and summarise (20 min)
#
# ✏️ **Exercise** · Write `by_year_origin(a)`: one row per year and origin with the total `arrivals`, as a table with the columns `year`, `origin`, `arrivals`.

# %%
def by_year_origin(a):
    # BEGIN SOLUTION
    return a.assign(year=a["month"].dt.year).groupby(["year", "origin"], as_index=False)["arrivals"].sum()
    # END SOLUTION


# %%
try:
    Y = by_year_origin(arrivals)
except NotImplementedError:
    Y = U.reference("p0", "yearly")
U.keep("p0", "yearly", Y)
print(Y.pivot(index="origin", columns="year", values="arrivals").to_string())
U.check(len(Y) == 15 and int(Y["arrivals"].sum()) == int(arrivals["arrivals"].sum()) and int(Y[Y["year"] == 2023]["arrivals"].sum()) == 842_275,
        "fifteen rows that still add up to all arrivals; 842,275 in 2023")

# %% [markdown]
# **Look at.** The check compares the total before and after grouping. You will do this after every grouping and every join in the course.

# %% [markdown]
# ## 3 · The same summary in SQL (20 min)
#
# DuckDB runs SQL directly on a dataframe that is in scope.
#
# ✏️ **Exercise** · Write `tickets_by_site_sql()`: a SQL query, as a string, that returns one row per `site` with `visitors` (the sum of `tickets`) and `sales` (the number of rows), ordered by `visitors`, largest first.

# %%
def tickets_by_site_sql():
    # BEGIN SOLUTION
    return """
        SELECT site, sum(tickets) AS visitors, count(*) AS sales
        FROM tickets
        GROUP BY site
        ORDER BY visitors DESC
    """
    # END SOLUTION


# %%
try:
    S = duckdb.sql(tickets_by_site_sql()).df()
except NotImplementedError:
    S = U.reference("p0", "by_site")
U.keep("p0", "by_site", S)
print(S.to_string(index=False))
U.check(len(S) == 9 and S["site"].iloc[0] == "Cable Car" and int(S["visitors"].iloc[0]) == 100_822 and int(S["sales"].sum()) == 150_000,
        "nine sites; the Cable Car first with 100,822 visitors; 150,000 sales in all")

# %% [markdown]
# **Look at.** `visitors` and `sales` differ: one sale holds 1 to 8 tickets. Which of the two is "the number of visitors" depends on what one row is. Day 1 starts there.

# %% [markdown]
# ## 4 · One unit, then join (25 min)
#
# ✏️ **Exercise** · Write `tickets_and_arrivals(t, a)`: one row per month with `tickets` (tickets sold in the month) and `arrivals` (arrivals of all origins in the month). Bring each table to one row per month first, then join the two.

# %%
def tickets_and_arrivals(t, a):
    # BEGIN SOLUTION
    tm = t.assign(month=t["sale_date"].dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False)["tickets"].sum()
    am = a.groupby("month", as_index=False)["arrivals"].sum()
    return tm.merge(am, on="month", how="inner", validate="one_to_one")
    # END SOLUTION


# %%
try:
    M = tickets_and_arrivals(tickets, arrivals)
except NotImplementedError:
    M = U.reference("p0", "monthly").assign(month=lambda d: pd.to_datetime(d["month"]))
U.keep("p0", "monthly", M)
print(M.head(3).to_string(index=False))
U.check(len(M) == 36 and int(M["tickets"].sum()) == int(tickets["tickets"].sum()) and int(M["arrivals"].sum()) == int(arrivals["arrivals"].sum()),
        "36 months, and neither total changed in the join")

# %% [markdown]
# ## 5 · A first chart in Altair (25 min)
#
# An Altair chart is built from three calls: the data, the mark, and the encodings that say which column drives which visual property. `:Q` marks a quantity, `:N` a name, `:T` a time.
#
# ```python
# alt.Chart(table).mark_line().encode(x="month:T", y="arrivals:Q")
# ```
#
# ✏️ **Exercise** · Write `first_chart(m)`: a line of `arrivals` over `month` from the table of step 4, with a y axis titled "Arrivals per month" and a chart title of your own.

# %%
def first_chart(m):
    # BEGIN SOLUTION
    return alt.Chart(m).mark_line().encode(
        x=alt.X("month:T", title=None),
        y=alt.Y("arrivals:Q", title="Arrivals per month"),
    ).properties(title="Arrivals peak every July", width=560)
    # END SOLUTION


# %%
try:
    c = first_chart(M)
except NotImplementedError:
    c = U.reference("p0", "chart")
U.keep("p0", "chart", c)
ch = U.channels(c)
U.check(U.marks(c) == {"line"} and ch["x"].get("field") == "month" and ch["y"].get("field") == "arrivals" and "Arrivals per month" in U.text_of(c),
        "a line of arrivals over the months, with a worded y axis")
U.show(c)

# %% [markdown]
# **Look at.** Change `mark_line()` to `mark_bar()` or `mark_point()` and run the cell again. The data and the encodings stay; only the mark changes. Day 3 is built on this idea.

# %% [markdown]
# ## 6 · Read before Day 1 (15 min)
#
# Read the director's brief and the data dictionary. Day 1 opens with them, and no table is opened until the questions are written.

# %%
print(U.brief())

# %%
for name, d in U.dictionary().items():
    print(f"{name}: one row is {d['unit']} ({d['rows']} rows)")
    for col, meaning in d["columns"].items():
        print(f"    {col}: {meaning}")

# %% [markdown]
# ## Self-check
#
# 1. Could you write steps 1 to 4 without looking anything up?
#    <details><summary>If not</summary>Revise grouping and joins (FN-101, FN-104) before Day 1. The labs give you 25 minutes each and assume these.</details>
# 2. Can you say in one sentence what a bootstrap interval is and what a permutation test tests?
#    <details><summary>If not</summary>Reread your DS-201 material. Day 4 applies both and does not teach them again.</details>
