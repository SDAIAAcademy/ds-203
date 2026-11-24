"""The district maps of Day 2, session 2 (slides map-of-counts and map-of-rates).

A parallel example, not a lab: a neighbouring highland region of nine districts, drawn as a tile
grid (one square per district, no real boundaries). The event is a first-aid call-out to a visitor
in 2025; the exposure is the number of visitor-days spent in the district. All values are
synthetic and seeded. The script prints every number the slides quote and writes two SVG files.

    uv run python _tools/d2_2_map_exposure.py            # print the numbers
    uv run python _tools/d2_2_map_exposure.py --figs ../assets/figs
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tilal as U  # noqa: E402

SEED = 2032
MIN_CALLS = 10  # fewer events than this: the area is greyed out, its count shown, its rate not coloured

# district, column, row on the tile grid, visitor-days (thousands), underlying call-outs per 100,000 visitor-days
DISTRICTS = [
    ("North-West", 0, 0, 45, 140),
    ("North", 1, 0, 140, 55),
    ("North-East", 2, 0, 60, 90),
    ("West", 0, 1, 310, 35),
    ("Central", 1, 1, 820, 30),
    ("East", 2, 1, 230, 40),
    ("South-West", 0, 2, 95, 45),
    ("South", 1, 2, 180, 38),
    ("South-East", 2, 2, 12, 55),
]


def table() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    d = pd.DataFrame(DISTRICTS, columns=["district", "col", "row", "visitor_days_k", "true_rate"])
    d["calls"] = rng.poisson(d["visitor_days_k"] * 1000 * d["true_rate"] / 100_000)
    d["per_100k"] = (100_000 * d["calls"] / (d["visitor_days_k"] * 1000)).round(1)
    d["enough"] = d["calls"] >= MIN_CALLS
    return d.drop(columns="true_rate")


def tile_map(d: pd.DataFrame, field: str, title: str, label: str):
    """One tile per district. Each map has its own colour scale, from zero to its largest value."""
    alt = U.alt()
    rate = field == "per_100k"
    coloured = d["enough"] if rate else pd.Series(True, index=d.index)
    top = d.loc[coloured, field].max()
    shown = d.assign(
        shade=np.where(coloured, d[field] / top, 0.0),
        coloured=coloured,
        label=[(f"{v:,.0f}" if ok else f"{c} calls") for v, ok, c in zip(d[field], coloured, d["calls"])],
    )
    base = alt.Chart(shown).encode(x=alt.X("col:O", axis=None), y=alt.Y("row:O", axis=None)).properties(width=270, height=270)
    tiles = base.mark_rect(stroke="white", strokeWidth=3).encode(
        color=alt.Color("shade:Q", scale=alt.Scale(scheme="blues", domain=[0, 1]), legend=None)
    ).transform_filter("datum.coloured")
    grey = base.mark_rect(stroke="white", strokeWidth=3, color="#d9d9d9").transform_filter("!datum.coloured")
    names = base.mark_text(dy=-14, fontSize=12).encode(text="district:N", color=alt.condition("datum.shade > 0.6", alt.value("white"), alt.value("#222")))
    values = base.mark_text(dy=8, fontSize=17, fontWeight="bold").encode(text="label:N", color=alt.condition("datum.shade > 0.6", alt.value("white"), alt.value("#222")))
    return (tiles + grey + names + values).properties(title=alt.TitleParams(title, subtitle=label))


def main(figs: str | None) -> None:
    d = table()
    r = np.corrcoef(d["calls"], d["visitor_days_k"])[0, 1]
    by_count = d.sort_values("calls", ascending=False)["district"].tolist()
    by_rate = d[d["enough"]].sort_values("per_100k", ascending=False)["district"].tolist()

    pd.set_option("display.width", 140)
    print(d.to_string(index=False))
    print(f"total calls {d['calls'].sum()}, total visitor-days {d['visitor_days_k'].sum()} thousand")
    print(f"correlation of calls with visitor-days across districts: {r:.2f}")
    print("rank by count:", by_count)
    print("rank by rate (enough calls):", by_rate)
    central = d.set_index("district").loc["Central"]
    print(f"Central: {central.calls} calls, {central.visitor_days_k:,}k visitor-days, "
          f"share of calls {central.calls / d['calls'].sum():.0%}, share of visitor-days {central.visitor_days_k / d['visitor_days_k'].sum():.0%}, "
          f"rank by rate {by_rate.index('Central') + 1} of {len(by_rate)}")

    # the story the slides tell must hold in the numbers
    assert by_count[0] == "Central", "the busiest district must lead by count"
    assert by_rate[0] != by_count[0], "the leader by rate must differ from the leader by count"
    assert by_rate.index("Central") >= len(by_rate) - 2, "Central must be near the bottom by rate"
    assert r > 0.9, "the count map must mirror the exposure map"
    assert (~d["enough"]).sum() == 1, "exactly one district has too few calls to colour"

    if figs:
        out = Path(figs)
        out.mkdir(parents=True, exist_ok=True)
        alt = U.alt()
        counts = tile_map(d, "calls", "First-aid call-outs", "visitors, 2025")
        exposure = tile_map(d, "visitor_days_k", "Visitor-days", "thousands, 2025")
        alt.hconcat(counts, exposure, spacing=30).save(str(out / "d2_2_map_counts.svg"))
        tile_map(d, "per_100k", "Call-outs per 100,000 visitor-days",
                 f"2025; grey: fewer than {MIN_CALLS} calls").save(str(out / "d2_2_map_rates.svg"))
        print("figures written:", ", ".join(p.name for p in sorted(out.glob("d2_2_map_*.svg"))))


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args[args.index("--figs") + 1] if "--figs" in args else None)
