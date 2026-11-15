# %% [markdown]
# # Lab 1.1 · Five questions from the brief
#
# Day 1 · Session 1 (Write the questions first) · 25 min.
#
# Nawal Al-Rashoud, director of Tilal Regional Tourism Board, sent a brief with five asks. None of them can be answered as written. You turn each into a question that names a table, a unit of observation, the variables and the comparison that answers it. The plan passes a checklist before any chart is drawn. Every later lab answers one line of this plan.
#
# **AI policy.** Assistant off: the plan is your own first draft. Nothing here needs plotting syntax.
#
# **Reference state.** `data/brief.md` and `data/data_dictionary.json`. No data table is opened in this lab, on purpose.
#
# **Tasks**
# - [ ] 1 · Read the brief; name the table and the unit behind each ask (5 min)
# - [ ] 2 · Write five questions with variables and comparison (12 min)
# - [ ] 3 · Run the plan checklist and fix what fails (5 min)
# - [ ] 4 · Write what the plan leaves out (3 min)
# - [ ] ✱ Stretch · Add the question the brief did not ask and should have

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
print(U.brief())

# %%
DD = U.dictionary()
for name, t in DD.items():
    print(f"{name:11s} unit: {t['unit']:45s} columns: {', '.join(t['columns'])}")

# %% [markdown]
# ## 1 · The table and the unit behind each ask (5 min)
#
# A **unit of observation** is what one row is. The same word in the brief ("visitors") is a party in one table, a ticket sale in another and a survey response in a third.
#
# ✏️ **Exercise** · Return a dictionary: ask number (1 to 5) to the name of the main table that answers it.

# %%
def main_tables():
    # BEGIN SOLUTION
    return {1: "stays", 2: "occupancy", 3: "complaints", 4: "arrivals", 5: "survey"}
    # END SOLUTION


# %%
try:
    TABLES = main_tables()
except NotImplementedError:
    TABLES = U.reference("d1_1", "tables")
TABLES = {int(k): v for k, v in TABLES.items()}
U.keep("d1_1", "tables", TABLES)
for k in sorted(TABLES):
    print(f"ask {k}: {TABLES[k]:11s} one row is {DD[TABLES[k]]['unit']}")
U.check(U.matches("d1_1", "tables_key", {str(k): v for k, v in TABLES.items()}), "each ask has the table whose rows hold what it asks about")

# %% [markdown]
# **Look at.** Ask 2 needs two tables with different units: a hotel on a day, and a ticket sale. Before they meet, both must be brought to one unit. Ask 3 needs a second table as well: complaints alone cannot say which site is worst.

# %% [markdown]
# ## 2 · Five questions (12 min)
#
# A question is ready when someone else could answer it without phoning you. It needs:
#
# - `question`: one sentence that ends with a question mark and holds no word nobody can measure ("why", "problem", "fault", "actually");
# - `table`: the main table; `also`: other tables it needs;
# - `unit`: the unit of observation of the main table, copied from the dictionary;
# - `variables`: at least two columns;
# - `comparison`: what is set against what;
# - `kind`: `"exploratory"` (you are looking for what is there) or `"confirmatory"` (the comparison was fixed before the data was seen and the data was not used to find it).
#
# ✏️ **Exercise** · Write the five entries. The first is done.

# %%
def plan():
    q1 = {"question": "How many nights do visiting parties from each origin market spend in the region, and what share are day visits?",
          "table": "stays", "also": [], "unit": DD["stays"]["unit"], "variables": ["origin", "nights"],
          "comparison": "the distribution of nights by origin market, and the share of parties with 0 nights per market",
          "kind": "exploratory"}
    # BEGIN SOLUTION
    q2 = {"question": "In weeks when more tickets are sold at the sites, is a larger share of hotel rooms sold?",
          "table": "occupancy", "also": ["tickets"], "unit": DD["occupancy"]["unit"], "variables": ["rooms_sold", "rooms", "tickets", "sale_date"],
          "comparison": "the share of rooms sold per week against the tickets sold per week",
          "kind": "exploratory"}
    q3 = {"question": "How many complaints per thousand visitors does each site receive over the three years?",
          "table": "complaints", "also": ["tickets"], "unit": DD["complaints"]["unit"], "variables": ["site", "tickets"],
          "comparison": "complaints per thousand visitors by site, with the count and the visitors beside it",
          "kind": "exploratory"}
    q4 = {"question": "By how much did arrivals in each festival month exceed what season and trend lead us to expect for that month?",
          "table": "arrivals", "also": [], "unit": DD["arrivals"]["unit"], "variables": ["month", "arrivals", "origin"],
          "comparison": "arrivals in a festival month against the baseline for the same month of the year",
          "kind": "exploratory"}
    q5 = {"question": "Did mean satisfaction change from 2024 to 2025 inside each origin market, and did the mix of markets among respondents change?",
          "table": "survey", "also": [], "unit": DD["survey"]["unit"], "variables": ["visit_date", "origin", "satisfaction"],
          "comparison": "mean satisfaction in 2025 against 2024 by origin market, and the share of each market between the two years",
          "kind": "exploratory"}
    return [q1, q2, q3, q4, q5]
    # END SOLUTION


# %% [markdown]
# ## 3 · The checklist (5 min)
#
# `U.plan_check(plan)` returns one line for everything that fails. An empty list is a pass. Fix your entries above and run again.

# %%
try:
    PLAN = plan()
except NotImplementedError:
    PLAN = U.reference("d1_1", "plan")
U.keep("d1_1", "plan", PLAN)
fails = U.plan_check(PLAN)
for line in fails:
    print(" ·", line)
U.check(not fails, "the plan passes the checklist: five questions, each with table, unit, variables, comparison and kind")
U.check(all(q["kind"] == "exploratory" for q in PLAN), "all five are exploratory: nothing was fixed before these three years of data existed")
print()
for i, q in enumerate(PLAN, 1):
    print(f"Q{i} [{q['table']}; {q['unit']}] {q['question']}\n    compare: {q['comparison']}\n")

# %% [markdown]
# **Look at.** Ask 5 said "why, and whose fault is it". The plan cannot answer "why": it can show whether satisfaction changed inside each market and whether the markets changed. That is a narrower promise, and one the data can keep.

# %% [markdown]
# ## 4 · What the plan leaves out (3 min)
#
# ✏️ **Exercise** · Two sentences for the director: what this plan will not tell her, and what it would take to find out. Assistant off.

# %%
def left_out():
    # BEGIN SOLUTION
    return ("This plan describes what happened in 2023 to 2025; it cannot say why satisfaction fell or whether the festivals caused the extra arrivals, "
            "because every question is exploratory and nothing was fixed before the data existed. "
            "A cause needs a comparison planned in advance and checked on data we have not looked at, such as next season's survey.")
    # END SOLUTION


# %%
try:
    NOTE = left_out()
except NotImplementedError:
    NOTE = U.reference("d1_1", "note")
U.keep("d1_1", "note", NOTE)
U.say("What the plan leaves out", NOTE)
U.reading_check(NOTE, [["why", "cause"], ["exploratory", "in advance", "planned", "new data", "not looked"]], "the note")

# %% [markdown]
# ## ✱ Stretch · The question nobody asked
#
# The brief never asks who is missing from the data. Write one more plan entry about a group the tables may not see, and run it through the checklist.

# %%
def stretch():
    # BEGIN SOLUTION
    q = {"question": "What share of stay records has no stated spend, and does that share differ between day visits and overnight stays?",
         "table": "stays", "also": [], "unit": DD["stays"]["unit"], "variables": ["spend_sar", "nights"],
         "comparison": "the share of records with spend missing, day visits against overnight stays", "kind": "exploratory"}
    return U.plan_check(PLAN[:4] + [q])
    # END SOLUTION


try:
    print("checklist on the extra question:", stretch() or "passes")
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Ask 2 uses a table of hotel-days and a table of sales. Why can they not be compared row by row?
#    <details><summary>Answer</summary>Their rows are different things. Both must first be counted per day or per week; the plan says per week.</details>
# 2. Why is "Is the Cable Car our problem site?" not a question the data can answer?
#    <details><summary>Answer</summary>"Problem" has no measure. "Complaints per thousand visitors by site" has one, and it names the denominator.</details>
# 3. What would make question 5 confirmatory?
#    <details><summary>Answer</summary>Writing the comparison down now and answering it with the 2026 survey, which nobody has looked at.</details>
#
# ## Carry forward
#
# The five questions are the course's agenda: Q1 in labs 1.3 and 1.4, Q2 in 2.1 and 4.1, Q3 in 2.2, Q4 in 2.3, Q5 in 2.4. Each of those labs starts from the supplied files, not from your notebook.
