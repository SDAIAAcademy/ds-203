# %% [markdown]
# # Lab 3.4 · One chart, two languages, safe colours
#
# Day 3 · Session 4 (Colour, labels and Arabic text) · 25 min.
#
# The board publishes in Arabic and in English, and part of every audience has a colour-vision deficiency, most often between red and green. The draft chart of arrivals by origin market fails both readers: its colours collapse under colour-vision deficiency and its labels exist in one language. You test the palette, replace it and add a second channel, then draw the Arabic and the English version from one function and a label file.
#
# **AI policy.** The tutor may hint at plotting syntax. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.arrivals()` and `data/labels.json` (the Arabic names of sites and origin markets, and the chart's texts in both languages). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Test the supplied palette for colour-vision deficiency (4 min)
# - [ ] 2 · A safe palette and a second channel (6 min)
# - [ ] 3 · One function, two languages: titles and names from a label file (7 min)
# - [ ] 4 · Arabic details: axis side, alignment, digits (5 min)
# - [ ] 5 · Write the reading (3 min)
# - [ ] ✱ Stretch · Replace the legend with a label at the end of each line

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
L = U.js("labels.json")
a = U.arrivals()
yearly = a.assign(year=a["month"].dt.year).groupby(["origin", "year"], as_index=False)["arrivals"].sum()
yearly["index"] = yearly["arrivals"] / yearly.groupby("origin")["arrivals"].transform("first") * 100
print(yearly.pivot(index="origin", columns="year", values="index").round(1).reindex(U.ORIGINS).to_string())

DRAFT_PALETTE = ["#d62728", "#2ca02c", "#ff7f0e", "#8c564b", "#1f77b4"]
draft = alt.Chart(yearly).mark_line(point=True).encode(
    x=alt.X("year:O", title="year"), y=alt.Y("index:Q", title="index", scale=alt.Scale(zero=False)),
    color=alt.Color("origin:N", sort=U.ORIGINS, scale=alt.Scale(range=DRAFT_PALETTE)),
).properties(title="Arrivals", width=380)
U.show(draft, "d3_4_draft")

# %% [markdown]
# ## 1 · Test the palette (4 min)
#
# `U.simulate(colour, kind)` returns a colour as a viewer with `"deuteranopia"` or `"protanopia"` (the two common red-green deficiencies) sees it. `U.closest_pair(palette, kind)` returns the distance between the two colours of a palette that are hardest to tell apart, and the pair. Distances are in CIELAB units: below about 10, two thin lines are hard to tell apart.
#
# ✏️ **Exercise** · Write `hardest(palette)`: the smallest of the closest-pair distances under normal vision (`kind=None`), deuteranopia and protanopia.

# %%
def hardest(palette):
    # BEGIN SOLUTION
    return min(U.closest_pair(palette, kind)[0] for kind in (None, "deuteranopia", "protanopia"))
    # END SOLUTION


# %%
try:
    D_DRAFT, D_SAFE = hardest(DRAFT_PALETTE), hardest(U.OKABE_ITO[:5])
except NotImplementedError:
    D_DRAFT, D_SAFE = U.reference("d3_4", "distances")
U.keep("d3_4", "distances", [D_DRAFT, D_SAFE])
for kind in (None, "deuteranopia", "protanopia"):
    d, c1, c2 = U.closest_pair(DRAFT_PALETTE, kind)
    print(f"draft palette, {kind or 'normal vision':13s}: closest pair {c1} and {c2}, distance {d:.1f}; seen as {U.simulate(c1, kind) if kind else c1} and {U.simulate(c2, kind) if kind else c2}")
print(f"hardest pair: draft {D_DRAFT:.1f} · Okabe and Ito's first five colours {D_SAFE:.1f}")
U.check(D_DRAFT < 10 and D_SAFE > 15, "the draft's red and green fall within 10 units of each other for a red-green deficiency; the safe palette keeps every pair above 15")

# %% [markdown]
# ## 2 · A safe palette and a second channel (6 min)
#
# Even a good palette fails in a grey photocopy. The rule is that colour never carries a distinction alone: give the same variable a second channel, such as the dash of the line or the shape of the point.
#
# ✏️ **Exercise** · Write `safe(df)`: the draft with the first five colours of `U.OKABE_ITO` and with `origin` also mapped to `strokeDash` or `shape`. Give both scales the same `domain` (the list `U.ORIGINS`) and the same legend title: the two legends then merge into one.

# %%
def safe(df):
    # BEGIN SOLUTION
    return alt.Chart(df).mark_line(strokeWidth=2.5).encode(
        x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("index:Q", title="Arrivals, 2023 = 100", scale=alt.Scale(zero=False)),
        color=alt.Color("origin:N", title="Origin market", scale=alt.Scale(domain=U.ORIGINS, range=U.OKABE_ITO[:5])),
        strokeDash=alt.StrokeDash("origin:N", title="Origin market", scale=alt.Scale(domain=U.ORIGINS)),
    ).properties(title="Arrivals by origin market", width=380)
    # END SOLUTION


# %%
try:
    c2 = safe(yearly)
except NotImplementedError:
    c2 = U.reference("d3_4", "safe")
U.keep("d3_4", "safe", c2)
ch = U.channels(c2)
pal = ch.get("color", {}).get("scale", {}).get("range", [])
U.check(isinstance(pal, list) and len(pal) >= 5 and min(U.closest_pair(pal[:5], k)[0] for k in (None, "deuteranopia", "protanopia")) > 15,
        "five colours that stay more than 15 units apart under both deficiencies")
second = [c for c in ("strokeDash", "shape") if ch.get(c, {}).get("field") == "origin"]
U.check(len(c2.to_dict()["datasets"]) == 1, "one dataset behind the chart")
U.check(bool(second), f"the origin is carried by a second channel as well ({', '.join(second) or 'none yet'})")
U.show(c2, "d3_4_safe")

# %% [markdown]
# **Look at.** The y axis does not start at zero. For an index drawn as lines that is acceptable: the message is the position relative to 100, and the title says "2023 = 100".

# %% [markdown]
# ## 3 · One function, two languages (7 min)
#
# Never keep two copies of a chart's code. Keep one function and a table of texts. `L["text"][lang]` holds the title, subtitle, axis titles, legend title and a source line for the report; `L["origins"]` maps each origin market to its Arabic name.
#
# ✏️ **Exercise** · Write `bilingual(df, lang)` for `lang` in `("en", "ar")`: the safe chart with every text taken from `L`, and the origin names shown in the chart's language. Add a column with the name to show; do not rename the data's own `origin` column.

# %%
def bilingual(df, lang):
    # BEGIN SOLUTION
    T = L["text"][lang]
    names = {o: (L["origins"][o] if lang == "ar" else o) for o in U.ORIGINS}
    d = df.assign(origin_label=df["origin"].map(names))
    order = [names[o] for o in U.ORIGINS]
    ar = lang == "ar"
    legend = alt.Legend(orient="left" if ar else "right", symbolStrokeWidth=2.5, symbolSize=400)
    return alt.Chart(d).mark_line(strokeWidth=2.5).encode(
        x=alt.X("year:O", title=T["x"], axis=alt.Axis(labelAngle=0)),
        y=alt.Y("index:Q", title=T["y"], scale=alt.Scale(zero=False), axis=alt.Axis(orient="right" if ar else "left", format="d")),
        color=alt.Color("origin_label:N", title=T["legend"], scale=alt.Scale(domain=order, range=U.OKABE_ITO[:5]), legend=legend),
        strokeDash=alt.StrokeDash("origin_label:N", title=T["legend"], scale=alt.Scale(domain=order), legend=legend),
    ).properties(width=380, title=alt.Title(T["title"], subtitle=T["subtitle"], anchor="end" if ar else "start"))
    # END SOLUTION


# %%
CHARTS = {}
for lang in ("en", "ar"):
    try:
        CHARTS[lang] = bilingual(yearly, lang)
    except NotImplementedError:
        CHARTS[lang] = U.reference("d3_4", f"chart_{lang}")
    U.keep("d3_4", f"chart_{lang}", CHARTS[lang])
    U.show(CHARTS[lang], f"d3_4_chart_{lang}")
for lang in ("en", "ar"):
    txt = U.text_of(CHARTS[lang])
    T = L["text"][lang]
    U.check(all(T[k] in txt for k in ("title", "subtitle", "x", "y", "legend")), f"{lang}: title, subtitle, axis titles and legend title all come from the label file")
values = str(CHARTS["ar"].to_dict()["datasets"])
U.check(L["origins"]["Gulf"] in values and "Gulf" in values, "the Arabic chart shows the Arabic names and the data keeps its own origin column")

# %% [markdown]
# ## 4 · Arabic details (5 min)
#
# Translation is not enough. An Arabic reader starts at the right, so what reads as text moves there: the title is anchored at the end, the y axis and its numbers stand on the right, the legend on the left. The board's house style keeps two things the same in both languages: digits are Western (2025, not ٢٠٢٥) and time runs from left to right, as in its tables.
#
# ✏️ **Exercise** · Make sure `bilingual(df, "ar")` puts the y axis on the right (`axis=alt.Axis(orient="right")`) and anchors the title at the end (`alt.Title(..., anchor="end")`), and that the English version keeps the defaults. Then run the checks.

# %%
ar, en = CHARTS["ar"], CHARTS["en"]
ya, ye = U.channels(ar)["y"].get("axis", {}), U.channels(en)["y"].get("axis", {})
ta, te = ar.to_dict().get("title", {}), en.to_dict().get("title", {})
U.check(ya.get("orient") == "right" and ye.get("orient", "left") == "left", "the y axis is on the right in Arabic and on the left in English")
U.check(isinstance(ta, dict) and ta.get("anchor") == "end" and (not isinstance(te, dict) or te.get("anchor", "start") == "start"), "the Arabic title is anchored at the end, the English one at the start")
U.check(not [c for c in U.text_of(ar) if 1632 <= ord(c) <= 1641], "digits are Western in both versions, as the house style asks")
U.check(U.channels(ar)["x"].get("sort") is None and U.channels(ar)["x"].get("scale", {}).get("reverse") is None, "time runs left to right in both versions, as the house style asks")

# %% [markdown]
# **Look at.** Open the two charts side by side. The lines are identical; everything a reader reads as words has moved. In a browser and in the rendered report the Arabic text is shaped and ordered by the text engine. Never reverse or reshape Arabic strings by hand.

# %% [markdown]
# ## 5 · The reading (3 min)
#
# ✏️ **Exercise** · Two sentences on the finished chart, in English: what it shows, and what it leaves out. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("From 2023 to 2025 arrivals from Asia rose by 67%, from Europe by 57% and from the Gulf by 42%, against 17% from other regions of the Kingdom, while arrivals from the Tilal region fell by 6%. "
            "An index shows growth, not size: the chart does not show that the two markets inside the Kingdom still bring about two visitors in three.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d3_4", "reading")
U.keep("d3_4", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["67%", ["fell", "down", "declin"], ["not", "does not"]])
tot = yearly[yearly["year"] == 2025].set_index("origin")["arrivals"]
print(f"share of 2025 arrivals from inside the Kingdom: {(tot['Tilal region'] + tot['Other regions']) / tot.sum():.0%}")

# %% [markdown]
# ## ✱ Stretch · Direct labels
#
# A legend makes the eye travel. Put each market's name at the end of its line and drop the legend.

# %%
def stretch(lang="en"):
    # BEGIN SOLUTION
    names = {o: (L["origins"][o] if lang == "ar" else o) for o in U.ORIGINS}
    d = yearly.assign(origin_label=yearly["origin"].map(names))
    base = alt.Chart(d).encode(x=alt.X("year:O", title=L["text"][lang]["x"], axis=alt.Axis(labelAngle=0)),
                               y=alt.Y("index:Q", title=L["text"][lang]["y"], scale=alt.Scale(zero=False)),
                               color=alt.Color("origin_label:N", legend=None, scale=alt.Scale(range=U.OKABE_ITO[:5]), sort=[names[o] for o in U.ORIGINS]))
    ends = alt.Chart(d[d["year"] == 2025]).mark_text(align="left", dx=8, fontSize=13).encode(x="year:O", y="index:Q", text="origin_label:N")
    return alt.layer(base.mark_line(point=True), ends).properties(width=380, title=L["text"][lang]["title"])
    # END SOLUTION


try:
    U.show(stretch("en"), "d3_4_direct_labels")
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. The draft's red and green are far apart for you. Why test?
#    <details><summary>Answer</summary>For a red-green deficiency they are within a few units of each other. You cannot see the problem by looking; you compute it or simulate it.</details>
# 2. Why a second channel when the palette is already safe?
#    <details><summary>Answer</summary>Print, photocopies, projectors and small marks defeat any palette. Dash or shape survives all of them.</details>
# 3. What moves in the Arabic version, and what stays?
#    <details><summary>Answer</summary>Moves: title alignment, the y axis, the legend, every text. Stays, by the board's house style: Western digits and time from left to right.</details>
#
# ## Carry forward
#
# The report of lab 4.4 takes its texts from the same label file.
