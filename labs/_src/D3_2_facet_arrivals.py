# %% [markdown]
# # Lab 3.2 · Arrivals in small multiples
#
# Day 3 · Session 2 (Small multiples) · 25 min.
#
# Five origin markets on one chart are five tangled lines, and the largest market flattens the others. You give each market its own panel, once with one shared scale and once with a scale per panel, work out what each version lets a reader compare, and choose one for each of three questions.
#
# **AI policy.** The tutor may hint at plotting syntax. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.arrivals()`: 36 months by five origin markets, 180 rows. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Five lines in one panel: what can be read (4 min)
# - [ ] 2 · One panel per market, shared scale (5 min)
# - [ ] 3 · The same panels with free scales (5 min)
# - [ ] 4 · What each version answers: peak month and peak-to-trough ratio (5 min)
# - [ ] 5 · Choose, order the panels and say the scale on the chart (4 min)
# - [ ] 6 · Write the reading (2 min)
# - [ ] ✱ Stretch · Index each market to 2023 = 100 and compare with the free-scale version

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
a = U.arrivals()
print(a.head(5).to_string())
print(a.groupby("origin")["arrivals"].mean().round(0).reindex(U.ORIGINS).to_string())

# %% [markdown]
# ## 1 · One panel (4 min)
#
# ✏️ **Exercise** · Write `one_panel(a)`: a line per origin, `month` on x, `arrivals` on y, `origin` on colour.

# %%
def one_panel(a):
    # BEGIN SOLUTION
    return alt.Chart(a).mark_line().encode(
        x=alt.X("month:T", title=None), y=alt.Y("arrivals:Q", title="Arrivals per month"),
        color=alt.Color("origin:N", sort=U.ORIGINS, title="Origin market"),
    ).properties(title="Monthly arrivals by origin market", width=560)
    # END SOLUTION


# %%
try:
    c1 = one_panel(a)
except NotImplementedError:
    c1 = U.reference("d3_2", "one")
U.keep("d3_2", "one", c1)
U.check(U.marks(c1) == {"line"} and U.field(c1, "color") == "origin" and U.field(c1, "y") == "arrivals", "five lines told apart by colour")
U.show(c1, "d3_2_one_panel")

# %% [markdown]
# **Look at.** You can read which market is largest and that the two large ones peak in summer. Try to say when Europe peaks, or whether Asia has a season at all: the bottom of the chart is three lines in a tenth of its height.

# %% [markdown]
# ## 2 · One panel per market, shared scale (5 min)
#
# ✏️ **Exercise** · Write `shared(a)`: the same line, one panel per origin in a single row of five (`.facet(column=...)` or `column=` in the encoding), all panels on the same y scale. Keep each panel narrow.

# %%
def shared(a):
    # BEGIN SOLUTION
    return alt.Chart(a).mark_line().encode(
        x=alt.X("month:T", title=None, axis=alt.Axis(format="%y", tickCount=3)),
        y=alt.Y("arrivals:Q", title="Arrivals per month"),
        column=alt.Column("origin:N", sort=U.ORIGINS, title=None),
    ).properties(width=120, height=220, title="Monthly arrivals by origin market, one scale for all panels")
    # END SOLUTION


# %%
try:
    c2 = shared(a)
except NotImplementedError:
    c2 = U.reference("d3_2", "shared")
U.keep("d3_2", "shared", c2)
ch = U.channels(c2)
facet_field = (ch.get("column") or ch.get("facet") or ch.get("row") or {}).get("field")
U.check(facet_field == "origin" and U.resolved(c2).get("scale", {}).get("y") != "independent", "one panel per origin, all on one y scale")
U.show(c2, "d3_2_shared")

# %% [markdown]
# ## 3 · Free scales (5 min)
#
# ✏️ **Exercise** · Write `free(a)`: the same panels, each with its own y scale (`.resolve_scale(y="independent")`). Every scale still starts at zero.

# %%
def free(a):
    # BEGIN SOLUTION
    return alt.Chart(a).mark_line().encode(
        x=alt.X("month:T", title=None, axis=alt.Axis(format="%y", tickCount=3)),
        y=alt.Y("arrivals:Q", title="Arrivals per month", scale=alt.Scale(zero=True)),
        column=alt.Column("origin:N", sort=U.ORIGINS, title=None),
    ).properties(width=120, height=220, title="Monthly arrivals by origin market, each panel on its own scale").resolve_scale(y="independent")
    # END SOLUTION


# %%
try:
    c3 = free(a)
except NotImplementedError:
    c3 = U.reference("d3_2", "free")
U.keep("d3_2", "free", c3)
ch = U.channels(c3)
U.check(U.resolved(c3).get("scale", {}).get("y") == "independent", "each panel has its own y scale")
U.check(ch["y"].get("scale", {}).get("zero", True) is True and "domain" not in ch["y"].get("scale", {}), "every free scale still starts at zero, so heights inside a panel stay in proportion")
U.show(c3, "d3_2_free")

# %% [markdown]
# **Look at.** Europe turns out to peak in winter, when every other market is at its lowest. That was on the first chart too, three pixels high.

# %% [markdown]
# ## 4 · What each version answers (5 min)
#
# Put numbers on what the two versions show.
#
# ✏️ **Exercise** · Write `profile(a)`: one row per origin with `mean` (mean monthly arrivals), `peak_month` (the month of the year, 1 to 12, with the highest mean arrivals over the three years) and `peak_to_trough` (highest month-of-year mean divided by the lowest).

# %%
def profile(a):
    # BEGIN SOLUTION
    t = a.assign(moy=a["month"].dt.month).groupby(["origin", "moy"])["arrivals"].mean().unstack()
    out = pd.DataFrame({"mean": a.groupby("origin")["arrivals"].mean(), "peak_month": t.idxmax(axis=1), "peak_to_trough": t.max(axis=1) / t.min(axis=1)})
    return out.reindex(U.ORIGINS)
    # END SOLUTION


# %%
try:
    PROF = profile(a)
except NotImplementedError:
    PROF = U.reference("d3_2", "profile")
U.keep("d3_2", "profile", PROF)
print(PROF.round(2).to_string())
U.check(int(PROF.loc["Europe", "peak_month"]) == 12 and int(PROF.loc["Gulf", "peak_month"]) == 7 and abs(PROF.loc["Gulf", "peak_to_trough"] - 4.13) < 0.05,
        "Europe peaks in December, the Gulf in July; the Gulf's peak month has four times the arrivals of its lowest month")
U.check(PROF["mean"].idxmax() == "Other regions" and PROF["mean"].max() / PROF["mean"].min() > 7, "the largest market is about eight times the smallest: on a shared scale the small ones are flat")

# %% [markdown]
# ## 5 · Choose (4 min)
#
# ✏️ **Exercise** · Write `choices()`: for each question return `"shared"` or `"free"`.
# Then `final(a)`: the free-scale version with the panels in the order of `U.ORIGINS` and a title or subtitle that tells the reader that each panel has its own scale.

# %%
QUESTIONS = ["Which market brings the most visitors?", "In which month does each market peak?", "Which market has the strongest season?"]


def choices():
    # BEGIN SOLUTION
    return {QUESTIONS[0]: "shared", QUESTIONS[1]: "free", QUESTIONS[2]: "free"}
    # END SOLUTION


def final(a):
    # BEGIN SOLUTION
    return free(a).properties(title=alt.Title("Europe comes in winter, everyone else in summer",
                                              subtitle="Monthly arrivals by origin market. Each panel has its own scale from zero: compare shapes, not heights"))
    # END SOLUTION


# %%
try:
    CH = choices()
except NotImplementedError:
    CH = U.reference("d3_2", "choices")
U.keep("d3_2", "choices", CH)
for q in QUESTIONS:
    print(f" · {q} → {CH[q]}")
U.check(U.matches("d3_2", "choices_key", CH), "levels need a shared scale; shapes, peaks and seasons need a scale per panel")
try:
    c5 = final(a)
except NotImplementedError:
    c5 = U.reference("d3_2", "final")
U.keep("d3_2", "final", c5)
U.check("scale" in U.text_of(c5).lower() and U.resolved(c5).get("scale", {}).get("y") == "independent", "the chart itself says that each panel has its own scale")
U.show(c5, "d3_2_final")

# %% [markdown]
# ## 6 · The reading (2 min)
#
# ✏️ **Exercise** · Two sentences on the final chart: what it shows, and what a reader must not conclude from it. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("Four of the five markets peak in July or August and Europe peaks in December, and the season is strongest for the Gulf, whose best month has about four times the arrivals of its weakest. "
            "Each panel has its own scale, so the chart does not show that the markets are of similar size: visitors from other regions outnumber visitors from Europe by about eight to one.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d3_2", "reading")
U.keep("d3_2", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["December", ["four times", "4 times", "4.1"], ["scale"], ["not", "does not"]])

# %% [markdown]
# ## ✱ Stretch · An index in place of free scales
#
# Divide each market's arrivals by its own 2023 monthly mean, times 100. All five now share one scale honestly.

# %%
def stretch():
    # BEGIN SOLUTION
    base = a[a["month"].dt.year == 2023].groupby("origin")["arrivals"].mean()
    t = a.assign(index=a["arrivals"] / a["origin"].map(base) * 100)
    print(t.groupby("origin")["index"].agg(["min", "max"]).round(0).reindex(U.ORIGINS).to_string())
    return alt.Chart(t).mark_line().encode(x="month:T", y=alt.Y("index:Q", title="Arrivals, 2023 monthly mean = 100"),
                                           column=alt.Column("origin:N", sort=U.ORIGINS, title=None)).properties(width=120, height=220)
    # END SOLUTION


try:
    U.show(stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. What does a shared scale let a reader compare across panels?
#    <details><summary>Answer</summary>Levels: a point twice as high is twice as many arrivals, in any panel.</details>
# 2. What does a free scale cost?
#    <details><summary>Answer</summary>Heights no longer compare across panels. The chart must say so, and each scale should still start at zero.</details>
# 3. When is one panel with five lines the better chart?
#    <details><summary>Answer</summary>When the lines are of similar size and cross, and the crossing is the story. Here they differ eightfold.</details>
#
# ## Carry forward
#
# The yearly arrivals by market return in lab 3.4 as the chart that must read in Arabic and English.
