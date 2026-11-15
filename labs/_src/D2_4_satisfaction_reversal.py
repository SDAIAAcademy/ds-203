# %% [markdown]
# # Lab 2.4 · The satisfaction reversal
#
# Day 2 · Session 4 (When the total reverses) · 25 min.
#
# Question 5 of the plan: did mean satisfaction change from 2024 to 2025 inside each origin market, and did the mix of markets among respondents change? The director wrote "satisfaction went down last year, whose fault is it?". You compute the fall, split it by origin, find that every market went up, and show how both statements are true at once.
#
# **AI policy.** The tutor may hint at dataframe and plotting syntax. The sentence for the board is your own first draft, assistant off.
#
# **Reference state.** `U.survey()`: 6,000 responses, of which 2,000 from 2024 and 2,200 from 2025. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Mean satisfaction by year (3 min)
# - [ ] 2 · Mean satisfaction by origin and year (5 min)
# - [ ] 3 · The mix of respondents by year (4 min)
# - [ ] 4 · 2025 at the 2024 mix (6 min)
# - [ ] 5 · One chart of the reversal (4 min)
# - [ ] 6 · Write the sentence the board may print (3 min)
# - [ ] ✱ Stretch · Find a second variable that could move the total the same way

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
s = U.survey()
s = s[s["year"].isin([2024, 2025])][["year", "origin", "site", "guided", "satisfaction"]]
print(s.groupby("year").size().to_dict())

# %% [markdown]
# ## 1 · The total (3 min)
#
# ✏️ **Exercise** · Write `by_year(s)`: a series of mean satisfaction for 2024 and 2025.

# %%
def by_year(s):
    # BEGIN SOLUTION
    return s.groupby("year")["satisfaction"].mean()
    # END SOLUTION


# %%
try:
    TOTAL = by_year(s)
except NotImplementedError:
    TOTAL = U.reference("d2_4", "total")
TOTAL.index = [int(i) for i in TOTAL.index]
U.keep("d2_4", "total", TOTAL)
print(f"mean satisfaction 2024: {TOTAL[2024]:.3f} · 2025: {TOTAL[2025]:.3f} · change {TOTAL[2025] - TOTAL[2024]:+.3f}")
U.check(abs(TOTAL[2024] - 4.150) < 0.002 and abs(TOTAL[2025] - 4.071) < 0.002, "overall, satisfaction fell from 4.15 to 4.07")

# %% [markdown]
# ## 2 · Inside each origin market (5 min)
#
# ✏️ **Exercise** · Write `by_origin_year(s)`: a table with one row per origin (in the order of `U.ORIGINS`) and the columns 2024, 2025 and `change`.

# %%
def by_origin_year(s):
    # BEGIN SOLUTION
    t = s.pivot_table(index="origin", columns="year", values="satisfaction", aggfunc="mean").reindex(U.ORIGINS)
    t["change"] = t[2025] - t[2024]
    return t
    # END SOLUTION


# %%
try:
    PARTS = by_origin_year(s)
except NotImplementedError:
    PARTS = U.reference("d2_4", "parts")
PARTS.columns = [int(c) if str(c).isdigit() else c for c in PARTS.columns]
U.keep("d2_4", "parts", PARTS)
print(PARTS.round(3).to_string())
U.check((PARTS["change"] > 0.08).all() and (PARTS["change"] < 0.12).all(), "satisfaction rose in every one of the five markets, by about 0.1 point")

# %% [markdown]
# **Look at.** Down overall, up in every part. Both tables are computed correctly from the same 4,200 responses. A total is a weighted average of its parts, and you have not looked at the weights yet.

# %% [markdown]
# ## 3 · The mix (4 min)
#
# ✏️ **Exercise** · Write `mix(s)`: a table with one row per origin and the columns 2024 and 2025: the share of that year's responses that came from the origin.

# %%
def mix(s):
    # BEGIN SOLUTION
    n = s.pivot_table(index="origin", columns="year", values="satisfaction", aggfunc="size").reindex(U.ORIGINS)
    return n / n.sum()
    # END SOLUTION


# %%
try:
    MIX = mix(s)
except NotImplementedError:
    MIX = U.reference("d2_4", "mix")
MIX.columns = [int(c) for c in MIX.columns]
U.keep("d2_4", "mix", MIX)
print((MIX * 100).round(0).astype(int).to_string())
U.check(np.allclose(MIX.sum(), 1) and abs(MIX.loc["Tilal region", 2024] - 0.40) < 0.005 and abs(MIX.loc["Tilal region", 2025] - 0.26) < 0.005,
        "respondents from the Tilal region fell from 40% to 26% of the survey; Gulf, Asia and Europe together rose from 25% to 44%")
print("check the total as a weighted average:", round(float((PARTS[2024] * MIX[2024]).sum()), 3), round(float((PARTS[2025] * MIX[2025]).sum()), 3))

# %% [markdown]
# **Look at.** The markets that score lowest (Gulf 3.7, Asia 3.4, Europe 3.3 in 2024) grew from a quarter of the responses to almost half. Each is more satisfied than it was; there are simply more of them in the average.

# %% [markdown]
# ## 4 · 2025 at the 2024 mix (6 min)
#
# To compare two years as if the visitors had not changed, hold the mix fixed: weight the 2025 means by the 2024 shares. This is **standardisation**.
#
# ✏️ **Exercise** · Write `standardised(parts, mix)`: the mean satisfaction 2025 would have had with the 2024 mix.

# %%
def standardised(parts, mix):
    # BEGIN SOLUTION
    return float((parts[2025] * mix[2024]).sum())
    # END SOLUTION


# %%
try:
    STD = standardised(PARTS, MIX)
except NotImplementedError:
    STD = U.reference("d2_4", "std")
U.keep("d2_4", "std", STD)
print(f"2024 as observed: {TOTAL[2024]:.3f} · 2025 as observed: {TOTAL[2025]:.3f} · 2025 at the 2024 mix: {STD:.3f}")
print(f"change from the markets themselves: {STD - TOTAL[2024]:+.3f} · change from the mix: {TOTAL[2025] - STD:+.3f} · together {TOTAL[2025] - TOTAL[2024]:+.3f}")
U.check(abs(STD - 4.250) < 0.003, "with the 2024 mix of visitors, 2025 would have scored 4.25: up 0.10, not down 0.08")

# %% [markdown]
# ## 5 · One chart of the reversal (4 min)
#
# ✏️ **Exercise** · Write `reversal_chart(parts, total)`: one line per origin from its 2024 mean to its 2025 mean, and the total as a sixth line that stands out. Build a long table with the columns `group`, `year` (as text) and `mean` first; use `detail` or `color` for the group, and a different colour or dash for the total.

# %%
def reversal_chart(parts, total):
    # BEGIN SOLUTION
    rows = [{"group": o, "year": str(y), "mean": float(parts.loc[o, y]), "kind": "origin market"} for o in parts.index for y in (2024, 2025)]
    rows += [{"group": "All respondents", "year": str(y), "mean": float(total[y]), "kind": "all respondents"} for y in (2024, 2025)]
    t = pd.DataFrame(rows)
    base = alt.Chart(t).encode(
        x=alt.X("year:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("mean:Q", title="Mean satisfaction, 1 to 5", scale=alt.Scale(domain=[3.0, 4.8])),
        detail="group:N",
        color=alt.Color("kind:N", title=None, scale=alt.Scale(domain=["origin market", "all respondents"], range=[U.OKABE_ITO[0], U.OKABE_ITO[4]])),
        strokeDash=alt.StrokeDash("kind:N", legend=None),
    )
    labels = alt.Chart(t[t["year"] == "2025"]).mark_text(align="left", dx=8, fontSize=13).encode(x="year:N", y="mean:Q", text="group:N")
    return alt.layer(base.mark_line(point=True), labels).properties(title="Every market up, the total down", width=380, height=320)
    # END SOLUTION


# %%
try:
    c_rev = reversal_chart(PARTS, TOTAL)
except NotImplementedError:
    c_rev = U.reference("d2_4", "chart")
U.keep("d2_4", "chart", c_rev)
ch = U.channels(c_rev)
U.check("line" in U.marks(c_rev) and ch["y"].get("field") == "mean" and ch["x"].get("field") == "year", "lines of mean satisfaction from 2024 to 2025")
U.check(max(len(v) for v in c_rev.to_dict()["datasets"].values()) >= 12, "six lines of two points each: the five markets and the total")
U.show(c_rev, "d2_4_reversal")

# %% [markdown]
# **Look at.** The y axis starts at 3.0, not at zero. For lines that compare positions on a 1 to 5 scale that is honest; for bars it would not be. Day 3, session 3 comes back to this.

# %% [markdown]
# ## 6 · The sentence the board may print (3 min)
#
# ✏️ **Exercise** · Two sentences. The first states what happened, with numbers; the second states what this does not show. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("Mean satisfaction fell from 4.15 in 2024 to 4.07 in 2025 although it rose by about 0.1 point in every origin market: visitors from the Gulf, Asia and Europe, who score lower, grew from 25% to 44% of respondents, and with the 2024 mix the 2025 score would have been 4.25. "
            "This does not show that any site got worse or whose fault the fall is; it shows that the board is now surveying a different mix of visitors, and it rests on who answered the survey, not on all visitors.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d2_4", "reading")
U.keep("d2_4", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["4.15", "4.07", ["4.25", "every origin", "every market", "each market"], ["mix", "share"], ["not", "does not"]])

# %% [markdown]
# ## ✱ Stretch · Another variable that could do the same
#
# Guided visits score higher. Did the share of guided visits change between the years? If it had fallen, it would pull the total down in the same way.

# %%
def stretch():
    # BEGIN SOLUTION
    g = s.groupby("year")["guided"].mean()
    m_ = s.groupby(["guided", "year"])["satisfaction"].mean().unstack()
    print("share of guided visits:", {int(k): round(float(v), 3) for k, v in g.items()})
    print(m_.round(3).to_string())
    print("The guided share barely moved, so it does not explain the fall. Any variable that shifts the mix must be checked the same way.")
    return float(g[2025] - g[2024])
    # END SOLUTION


try:
    U.keep("d2_4", "guided_shift", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. How can every group rise while the total falls?
#    <details><summary>Answer</summary>The total is a weighted average. The weights moved toward the groups with lower scores.</details>
# 2. Which number answers "are we serving visitors better"?
#    <details><summary>Answer</summary>The change inside each market, or 2025 at the 2024 mix: up about 0.10. The raw total answers "what does the average respondent say now".</details>
# 3. What would make you distrust the split itself?
#    <details><summary>Answer</summary>Small groups. Europe had 120 responses in 2024; a change of 0.1 there is within what chance does, which Day 4 measures.</details>
#
# ## Carry forward
#
# The cut-axis bar chart that announced "satisfaction collapsed" is chart 1 of lab 3.3. Whether a change of 0.1 in a group of 120 could be chance is the subject of Day 4.
