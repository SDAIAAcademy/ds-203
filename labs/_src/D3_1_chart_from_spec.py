# %% [markdown]
# # Lab 3.1 · A chart from a written specification
#
# Day 3 · Session 1 (Marks, encodings and scales) · 25 min.
#
# Atheer Al-Muhaya does not send a sketch. She sends a specification: the data, the marks, and which variable goes to which channel. You build the chart from it, part by part, and see that a chart in a grammar of graphics is that specification written as code. Then you change one mark and say what the reader loses.
#
# **AI policy.** The tutor may hint at plotting syntax, one step at a time. The reading is your own first draft, assistant off.
#
# **Reference state.** `U.site_rates()`: complaints, visitors and complaints per thousand visitors for the nine sites (the result of lab 2.2, supplied). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Read the specification: data, marks, encodings (3 min)
# - [ ] 2 · The base chart: position for the rate (6 min)
# - [ ] 3 · Sort, start the scale at zero, write the titles (5 min)
# - [ ] 4 · A second encoding and a text layer (6 min)
# - [ ] 5 · Change one mark and say what the reader loses (3 min)
# - [ ] 6 · Write the reading (2 min)
# - [ ] ✱ Stretch · Write the specification of a chart from lab 1.3 in the same form

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
rates = U.site_rates()
print(rates.round(2).to_string(index=False))

# %% [markdown]
# **The specification**
#
# | Part | Value |
# |---|---|
# | Data | one row per site, nine rows: `site`, `complaints`, `visitors`, `per_thousand` |
# | Marks | a thin rule from zero to the rate; a circle at the rate; the rate as text beside the circle |
# | x | `per_thousand`, a quantity; the axis starts at zero; title "Complaints per thousand visitors, 2023 to 2025" |
# | y | `site`, a name; sorted from the highest rate to the lowest; no axis title |
# | size | `visitors`, a quantity, on the circle only; legend title "Visitors" |
# | text | `per_thousand` with one decimal |
# | Title | "Complaints per thousand visitors by site" |

# %% [markdown]
# ## 1 · Read the specification (3 min)
#
# Altair names four types of variable: `quantitative` (a quantity), `ordinal` (ordered categories), `nominal` (names) and `temporal` (times).
#
# ✏️ **Exercise** · Return the encodings of the specification as a dictionary: channel to `(field, type)`.

# %%
def encodings():
    # BEGIN SOLUTION
    return {"x": ("per_thousand", "quantitative"), "y": ("site", "nominal"),
            "size": ("visitors", "quantitative"), "text": ("per_thousand", "quantitative")}
    # END SOLUTION


# %%
try:
    ENC = {k: list(v) for k, v in encodings().items()}
except NotImplementedError:
    ENC = U.reference("d3_1", "enc")
U.keep("d3_1", "enc", ENC)
for k, v in ENC.items():
    print(f" · {k:5s} {v[0]:13s} {v[1]}")
U.check(U.matches("d3_1", "enc_key", ENC), "four channels, each with the field and the type the specification gives")

# %% [markdown]
# ## 2 · The base chart (6 min)
#
# ✏️ **Exercise** · Write `base(df)`: circles, the rate on x, the site on y. Nothing else yet.

# %%
def base(df):
    # BEGIN SOLUTION
    return alt.Chart(df).mark_circle().encode(x="per_thousand:Q", y="site:N")
    # END SOLUTION


# %%
try:
    c1 = base(rates)
except NotImplementedError:
    c1 = U.reference("d3_1", "base")
U.keep("d3_1", "base", c1)
ch = U.channels(c1)
U.check(U.marks(c1) <= {"circle", "point"} and ch["x"].get("field") == "per_thousand" and ch["x"].get("type") == "quantitative" and ch["y"].get("field") == "site" and ch["y"].get("type") == "nominal",
        "circles; the rate as a quantity on x; the site as a name on y")
U.show(c1, "d3_1_base")

# %% [markdown]
# **Look at.** The chart is already correct and already hard to use: sites are in alphabetical order, so the eye has to sort nine dots, and the axis titles are column names.

# %% [markdown]
# ## 3 · Sort, scale, titles (5 min)
#
# ✏️ **Exercise** · Write `polished(df)`: the same marks, with y sorted by the rate from highest to lowest (`sort="-x"`), the x scale starting at zero, and the titles of the specification.

# %%
def polished(df):
    # BEGIN SOLUTION
    return alt.Chart(df).mark_circle().encode(
        x=alt.X("per_thousand:Q", scale=alt.Scale(zero=True), title="Complaints per thousand visitors, 2023 to 2025"),
        y=alt.Y("site:N", sort="-x", title=None),
    ).properties(title="Complaints per thousand visitors by site")
    # END SOLUTION


# %%
try:
    c2 = polished(rates)
except NotImplementedError:
    c2 = U.reference("d3_1", "polished")
U.keep("d3_1", "polished", c2)
ch = U.channels(c2)
U.check(ch["y"].get("sort") == "-x" and ch["x"].get("scale", {}).get("zero", True) is True and "domain" not in ch["x"].get("scale", {}),
        "y sorted by the rate; the x scale starts at zero")
U.check("per thousand visitors" in U.text_of(c2).lower() and "per_thousand" not in U.text_of(c2), "the titles are words a reader knows, not column names")
U.show(c2, "d3_1_polished")

# %% [markdown]
# ## 4 · A second encoding and a text layer (6 min)
#
# Layers share the data and the scales. Build the three marks from one base and add them with `alt.layer(...)` or `+`.
#
# ✏️ **Exercise** · Write `full(df)`: the rule from zero to the rate, the circle with `visitors` mapped to size, and the rate as text with one decimal to the right of the circle.

# %%
def full(df):
    # BEGIN SOLUTION
    b = alt.Chart(df).encode(
        x=alt.X("per_thousand:Q", scale=alt.Scale(zero=True), title="Complaints per thousand visitors, 2023 to 2025"),
        y=alt.Y("site:N", sort="-x", title=None),
    )
    rule = b.mark_rule(color="#999999").encode(x2=alt.datum(0))
    dot = b.mark_circle(opacity=1).encode(size=alt.Size("visitors:Q", title="Visitors", scale=alt.Scale(range=[60, 700])))
    label = b.mark_text(align="left", dx=16, fontSize=13).encode(text=alt.Text("per_thousand:Q", format=".1f"))
    return alt.layer(rule, dot, label).properties(title="Complaints per thousand visitors by site")
    # END SOLUTION


# %%
try:
    c3 = full(rates)
except NotImplementedError:
    c3 = U.reference("d3_1", "full")
U.keep("d3_1", "full", c3)
ch = U.channels(c3)
U.check({"rule", "text"} <= U.marks(c3) and U.marks(c3) & {"circle", "point"}, "three layers: a rule, a circle and a text")
U.check(ch.get("size", {}).get("field") == "visitors" and ch.get("text", {}).get("field") == "per_thousand", "visitors mapped to size, the rate written as text")
U.show(c3, "d3_1_full")

# %% [markdown]
# **Look at.** The largest circle is fifth from the top. One chart now says what lab 2.2 needed a paragraph for: the busiest site has an ordinary rate, and the two highest rates belong to small sites.

# %% [markdown]
# ## 5 · Change one mark (3 min)
#
# The same data and the same x and y, as bars. A bar already uses its length for the rate.
#
# ✏️ **Exercise** · Write `as_bars(df)`: a bar chart with the same x and y. Then `lost()`: return which encoding of the specification has no good place on a bar: `"x"`, `"y"`, `"size"` or `"text"`.

# %%
def as_bars(df):
    # BEGIN SOLUTION
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("per_thousand:Q", title="Complaints per thousand visitors, 2023 to 2025"),
        y=alt.Y("site:N", sort="-x", title=None),
    ).properties(title="Complaints per thousand visitors by site")
    # END SOLUTION


def lost():
    # BEGIN SOLUTION
    return "size"
    # END SOLUTION


# %%
try:
    c4 = as_bars(rates)
except NotImplementedError:
    c4 = U.reference("d3_1", "bars")
U.keep("d3_1", "bars", c4)
try:
    LOST = lost()
except NotImplementedError:
    LOST = U.reference("d3_1", "lost")
U.keep("d3_1", "lost", LOST)
U.check(U.marks(c4) == {"bar"} and U.field(c4, "x") == "per_thousand", "a bar chart of the same rates")
U.check(LOST == "size", "a bar's size is its length, which is taken: the visitors behind each rate drop off the chart")
U.show(c4, "d3_1_bars")

# %% [markdown]
# ## 6 · The reading (2 min)
#
# ✏️ **Exercise** · Two sentences: what the finished chart lets a reader see at a glance, and what it does not show. Assistant off.

# %%
def reading():
    # BEGIN SOLUTION
    return ("Sorted by rate, Terrace Farms (13.8 complaints per thousand visitors) and the Wadi Trail (11.4) stand far above the other seven sites, which lie between 4.2 and 6.7, and the circle sizes show that these two are among the smallest sites while the largest, the Cable Car, is fifth. "
            "The chart does not show what the complaints are about, nor how sure the rates of the small sites are.")
    # END SOLUTION


# %%
try:
    READING = reading()
except NotImplementedError:
    READING = U.reference("d3_1", "reading")
U.keep("d3_1", "reading", READING)
U.say("Reading", READING)
U.reading_check(READING, ["13.8", ["Terrace Farms"], ["not", "does not"]])

# %% [markdown]
# ## ✱ Stretch · A specification of your own
#
# Write the specification of the five-panel histogram of lab 1.3 as a dictionary with the keys `data`, `mark`, `x`, `y`, `row`.

# %%
def stretch():
    # BEGIN SOLUTION
    return {"data": "one row per origin and number of nights: origin, nights, share",
            "mark": "bar", "x": ("nights", "quantitative"), "y": ("share", "quantitative"), "row": ("origin", "nominal")}
    # END SOLUTION


try:
    print(U.keep("d3_1", "spec13", stretch()))
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. What are the four parts of a chart in a grammar of graphics?
#    <details><summary>Answer</summary>Data, marks, encodings (which variable goes to which channel) and scales (how values become positions, sizes and colours).</details>
# 2. Why was the rate put on position and the visitors on size, not the other way round?
#    <details><summary>Answer</summary>Position on a common scale is read most precisely, and the rate is the comparison the question asks for. Size is read roughly, which is enough for "a small site".</details>
# 3. What did sorting change in the data?
#    <details><summary>Answer</summary>Nothing. It changed which comparison is easy: neighbours in the order are neighbours in rate.</details>
#
# ## Carry forward
#
# Labs 3.2 to 3.4 use the same parts: facets in 3.2, scales in 3.3, colour and text in 3.4.
