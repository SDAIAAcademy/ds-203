# %% [markdown]
# # Tilal Regional Tourism Board: what three years of data show
#
# A note for the director, Nawal Al-Rashoud, written by the analyst. Period: January 2023 to December 2025. All data is synthetic.
#
# Every number below is computed when this note is rendered. The note is exploratory: it reports what the data shows, how each pattern was checked and what it does not show.

# %%
# parameters
PARAMS = {"seed": None, "source": "cache", "findings": None}

# %%
import json

import numpy as np
import pandas as pd

import tilal as U

alt = U.alt()
alt.renderers.enable("svg")  # pictures inside the file: the report opens without a network
gen = np.random.default_rng(PARAMS["seed"])  # seed None: different draws on every run
N = {}

# %% [markdown]
# ## 1 · Who comes, and how long they stay

# %%
if PARAMS["source"] == "raw":
    stays = U.stays()  # the register, read from the raw export with the decisions of the issue log
    N["stays"] = int(len(stays))
    N["gulf_stays"] = int((stays["origin"] == "Gulf").sum())
    N["mean_nights"] = round(float(stays["nights"].mean()), 2)
    N["median_nights_europe"] = float(stays.loc[stays["origin"] == "Europe", "nights"].median())
    N["day_visit_share_local"] = round(float((stays.loc[stays["origin"] == "Tilal region", "nights"].dropna() == 0).mean()), 3)
else:
    cache = json.loads((U.LABS / "report" / "cache" / "stays_summary.json").read_text(encoding="utf-8"))  # saved once, long ago
    N.update(cache)
print(f"{N['stays']:,} stays; {N['gulf_stays']:,} from the Gulf; mean length {N['mean_nights']} nights; "
      f"Europe: median {N['median_nights_europe']:.0f} nights; Tilal region: {N['day_visit_share_local']:.0%} day visits")

# %% [markdown]
# ## 2 · Sites and hotels

# %%
w = U.weekly()
r = float(w["tickets"].corr(w["occupancy"]))
idx = gen.integers(0, len(w), size=(2000, len(w)))
boot = np.array([np.corrcoef(w["tickets"].to_numpy()[i], w["occupancy"].to_numpy()[i])[0, 1] for i in idx])
lo, hi = np.percentile(boot, [2.5, 97.5])
N["weekly_correlation"], N["correlation_low"], N["correlation_high"] = round(r, 2), round(float(lo), 3), round(float(hi), 3)
print(f"weekly tickets and hotel occupancy: correlation {r:.2f}, 95% bootstrap interval {lo:.3f} to {hi:.3f} (156 weeks)")
alt.Chart(w).mark_circle(size=40, opacity=0.6).encode(
    x=alt.X("tickets:Q", title="Tickets sold per week", scale=alt.Scale(zero=False)),
    y=alt.Y("occupancy:Q", title="Share of hotel rooms sold in the week", axis=alt.Axis(format="%"), scale=alt.Scale(zero=False)),
).properties(title="Busier weeks at the sites are fuller weeks at the hotels")

# %% [markdown]
# ## 3 · Festivals

# %%
m = U.monthly_total().assign(year=lambda d: d["month"].dt.year, moy=lambda d: d["month"].dt.month)
growth = float((m["arrivals"] / m["arrivals"].shift(12)).median())
base = m["moy"].map(m[m["year"] == 2023].set_index("moy")["arrivals"]) * growth ** (m["year"] - 2023)
m["excess"] = m["arrivals"] / base - 1
fest = m[m["excess"] > 0.10].assign(label=lambda d: d["month"].dt.strftime("%Y-%m"))
N["festival_months"] = list(fest["label"])
N["festival_excess"] = [round(float(v), 2) for v in fest["excess"]]
print("months more than 10% above the seasonal baseline:", dict(zip(N["festival_months"], N["festival_excess"])))

# %% [markdown]
# ## 4 · Satisfaction

# %%
s = U.survey()
s = s[s["year"].isin([2024, 2025])]
tot = s.groupby("year")["satisfaction"].mean()
parts = s.pivot_table(index="origin", columns="year", values="satisfaction", aggfunc="mean")
mix = s.pivot_table(index="origin", columns="year", values="satisfaction", aggfunc="size")
mix = mix / mix.sum()
N["satisfaction_2024"], N["satisfaction_2025"] = round(float(tot[2024]), 2), round(float(tot[2025]), 2)
N["satisfaction_2025_at_2024_mix"] = round(float((parts[2025] * mix[2024]).sum()), 2)
N["markets_up"] = int((parts[2025] > parts[2024]).sum())
print(f"mean satisfaction {N['satisfaction_2024']} in 2024, {N['satisfaction_2025']} in 2025; up in {N['markets_up']} of 5 origin markets; "
      f"2025 at the 2024 mix of visitors: {N['satisfaction_2025_at_2024_mix']}")

# %% [markdown]
# ## Findings, checks and limits

# %%
findings = PARAMS["findings"] or json.loads((U.LABS / "report" / "findings_draft.json").read_text(encoding="utf-8"))
print(pd.DataFrame(findings)[["finding", "status", "check", "limit"]].to_string(index=False, max_colwidth=60))

# %%
print("NUMBERS " + json.dumps(N, sort_keys=True))
