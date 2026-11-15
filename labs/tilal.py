"""Helpers for the DS-203 labs: the data of Tilal Regional Tourism Board, chart checks and safety nets.

    import tilal as U

pandas, NumPy, Vega-Altair and the standard library. Nothing calls a model.

Environment variables
    DS203_QUICK=1      fewer resamples, for a fast run
    DS203_STRICT=1     solution runs: a failed check stops the run
    DS203_WRITE_REF=1  the trainer's run that writes data/reference/ (the safety nets read it)
    DS203_FIGS=<dir>   the trainer's run that also saves every chart shown as an SVG file
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

for _stream in (sys.stdout, sys.stderr):  # a Windows console or a redirected run may not default to UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"
OUT = LABS / "out"

QUICK = os.environ.get("DS203_QUICK", "0") == "1"
STRICT = os.environ.get("DS203_STRICT", "0") == "1"
WRITE_REF = os.environ.get("DS203_WRITE_REF", "0") == "1"
FIGS = os.environ.get("DS203_FIGS", "")
MODE = "quick" if QUICK else "full"
SEED = 203

ORIGINS = ["Tilal region", "Other regions", "Gulf", "Asia", "Europe"]
SITES = ["Cable Car", "Souq Walk", "Tilal Fort", "Juniper Park", "Stone Village", "Honey Museum", "Cloud Lookout", "Wadi Trail", "Terrace Farms"]
# Okabe and Ito's palette, chosen to stay apart for the common colour-vision deficiencies
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442", "#000000"]


def pick(full, quick):
    """The full value, or the small one in quick mode."""
    return quick if QUICK else full


def rng(offset: int = 0) -> np.random.Generator:
    """A seeded generator. The same offset gives the same draws on every run."""
    return np.random.default_rng(SEED + offset)


# ---------------------------------------------------------------- checks and safety nets

def check(ok, what: str) -> bool:
    """Print a tick or a cross. In a solution run (DS203_STRICT=1) a cross stops the run."""
    ok = bool(ok)
    print(("✅ " if ok else "❌ ") + what)
    if STRICT and not ok:
        raise AssertionError(what)
    return ok


def _jsonable(v):
    if isinstance(v, pd.DataFrame):
        return {"__frame__": json.loads(v.to_json(orient="split", date_format="iso"))}
    if isinstance(v, pd.Series):
        return {"__series__": json.loads(v.to_json(orient="split", date_format="iso"))}
    if isinstance(v, np.ndarray):
        return {"__array__": v.tolist()}
    if isinstance(v, (np.floating, np.integer, np.bool_)):
        return v.item()
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set)):
        return [_jsonable(x) for x in v]
    return v


def _unjson(v):
    if isinstance(v, dict):
        if "__array__" in v:
            return np.array(v["__array__"])
        if "__frame__" in v:
            f = v["__frame__"]
            return pd.DataFrame(f["data"], index=f["index"], columns=f["columns"])
        if "__series__" in v:
            s = v["__series__"]
            return pd.Series(s["data"], index=s["index"], name=s.get("name"))
        return {k: _unjson(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_unjson(x) for x in v]
    return v


def _store(lab: str) -> Path:
    return REF / f"{lab}.{MODE}.json"


def keep(lab: str, name: str, value):
    """Return value. In the trainer's run, also store it as the reference of this exercise."""
    if WRITE_REF:
        REF.mkdir(parents=True, exist_ok=True)
        path = _store(lab)
        store = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        store[name] = {"__chart__": _chart_store(value)} if _is_chart(value) else _jsonable(value)
        path.write_text(json.dumps(store, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def reference(lab: str, name: str, data: pd.DataFrame | None = None):
    """The reference result of an exercise, so the cells after it run when it is not done yet.

    For a chart exercise pass the dataframe the chart is drawn from: the stored specification is put back on it.
    """
    if STRICT:
        raise AssertionError(f"the solution run reached the safety net of {lab}/{name}")
    print(f"↪ exercise not done yet: using the reference result for {name}")
    value = json.loads(_store(lab).read_text(encoding="utf-8"))[name]
    if isinstance(value, dict) and "__chart__" in value:
        A, s = alt(), value["__chart__"]
        kind = next((c for k, c in (("layer", A.LayerChart), ("facet", A.FacetChart), ("vconcat", A.VConcatChart), ("hconcat", A.HConcatChart),
                                    ("concat", A.ConcatChart), ("repeat", A.RepeatChart)) if k in s), A.Chart)
        chart = kind.from_dict(s, validate=False)
        if "datasets" not in value["__chart__"]:
            chart.data = data
        return chart
    return _unjson(value)


def _chart_store(chart) -> dict:
    """A chart's specification with its data when the data is small, without it otherwise."""
    full = chart.to_dict(validate=True)
    full.pop("config", None)
    if len(json.dumps(full)) > 60_000:
        full.pop("datasets", None)
        full.pop("data", None)
    return full


# ---------------------------------------------------------------- the data

def _csv(name: str, **kw) -> pd.DataFrame:
    return pd.read_csv(DATA / name, **kw)


def arrivals() -> pd.DataFrame:
    """180 rows: one origin market in one month. month (first day of the month), origin, arrivals."""
    df = _csv("arrivals.csv")
    df["month"] = pd.to_datetime(df["month"] + "-01")
    return df


def tickets() -> pd.DataFrame:
    """150,000 ticket sales at nine sites. One row is one sale; `tickets` is the number of visitors in it."""
    return _csv("tickets.csv.gz", parse_dates=["sale_date"])


def stays_raw() -> pd.DataFrame:
    """The stay register exactly as exported, with its data issues (lab 1.2). Dates are text here."""
    return _csv("stays.csv.gz", keep_default_na=True)


def stays() -> pd.DataFrame:
    """The stay register after the decisions of lab 1.2's issue log.

    Rows entered twice dropped; 999 nights and impossible arrival dates set to missing; one spelling per origin.
    Spend stays missing where it was not given. This is the reference state of every later lab that uses stays.
    """
    df = stays_raw().drop_duplicates().reset_index(drop=True)
    df["origin"] = df["origin"].str.strip().replace({"GCC": "Gulf", "gulf": "Gulf"})
    df["nights"] = df["nights"].where(df["nights"] != 999)
    df["arrival_date"] = pd.to_datetime(df["arrival_date"])
    df.loc[df["arrival_date"] > "2025-12-31", "arrival_date"] = pd.NaT
    return df


def occupancy() -> pd.DataFrame:
    """43,840 rows: one hotel on one day. rooms, rooms_sold; hotel_id is a code, never a name."""
    return _csv("occupancy.csv.gz", parse_dates=["date"])


def survey() -> pd.DataFrame:
    """6,000 survey responses, satisfaction 1 to 5, with a short comment in Arabic or English."""
    df = _csv("survey.csv", parse_dates=["visit_date"], keep_default_na=False)
    df["year"] = df["visit_date"].dt.year
    df["weekend"] = weekend(df["visit_date"])
    return df


def complaints() -> pd.DataFrame:
    """About 2,400 complaints by site, origin and category."""
    return _csv("complaints.csv", parse_dates=["complaint_date"])


def js(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def brief() -> str:
    return (DATA / "brief.md").read_text(encoding="utf-8")


def dictionary() -> dict:
    """The data dictionary: for each table its file, its unit of observation and its columns."""
    return js("data_dictionary.json")


def weekend(dates) -> np.ndarray:
    """True on Friday and Saturday, the weekend in the Kingdom."""
    return np.isin(pd.DatetimeIndex(dates).day_of_week, [4, 5])


# ---------------------------------------------------------------- charts: Vega-Altair with the course defaults

_ALT = None


def alt():
    """Vega-Altair with the course defaults: readable type, no row limit, a palette safe for colour-vision deficiency."""
    global _ALT
    if _ALT is None:
        import altair

        altair.data_transformers.disable_max_rows()

        @altair.theme.register("tilal", enable=True)
        def _theme():
            return altair.theme.ThemeConfig({"config": {
                "view": {"continuousWidth": 520, "continuousHeight": 300, "stroke": None},
                "axis": {"labelFontSize": 13, "titleFontSize": 14, "titleFontWeight": "normal", "grid": True, "gridOpacity": 0.4},
                "legend": {"labelFontSize": 13, "titleFontSize": 13, "titleFontWeight": "normal"},
                "header": {"labelFontSize": 13, "titleFontSize": 14, "titleFontWeight": "normal"},
                "title": {"fontSize": 16, "anchor": "start", "subtitleFontSize": 13, "subtitleColor": "#555"},
                "range": {"category": OKABE_ITO},
                "bar": {"color": OKABE_ITO[0]}, "line": {"color": OKABE_ITO[0]}, "point": {"color": OKABE_ITO[0]},
                "area": {"color": OKABE_ITO[0]}, "rect": {"color": OKABE_ITO[0]}, "tick": {"color": OKABE_ITO[0]},
            }})

        _ALT = altair
    return _ALT


def _is_chart(v) -> bool:
    return hasattr(v, "to_dict") and hasattr(v, "mark_point") or type(v).__name__.endswith("Chart")


def spec(chart) -> dict:
    """The chart's Vega-Lite specification without its data: what a check reads."""
    d = chart.to_dict(validate=True)
    d.pop("datasets", None)
    d.pop("data", None)
    d.pop("config", None)
    d.pop("$schema", None)
    return d


def _walk(node, found: list):
    if isinstance(node, dict):
        found.append(node)
        for v in node.values():
            _walk(v, found)
    elif isinstance(node, list):
        for v in node:
            _walk(v, found)


def marks(chart) -> set[str]:
    """The mark types a chart uses, in all its layers and panels: {"bar"}, {"line", "point"}."""
    nodes: list = []
    _walk(spec(chart), nodes)
    out = set()
    for n in nodes:
        m = n.get("mark")
        if m:
            out.add(m if isinstance(m, str) else m.get("type"))
    return out


def channels(chart) -> dict:
    """Every encoding of a chart, in all its layers: channel -> its definition (field, type, scale, ...).

    Facets given with `.facet(...)` or `row=` and `column=` appear as "facet", "row" and "column".
    """
    nodes: list = []
    s = spec(chart)
    _walk(s, nodes)
    out: dict = {}
    for n in nodes:
        enc = n.get("encoding")
        if isinstance(enc, dict):
            for k, v in enc.items():
                if isinstance(v, dict) and k not in out:
                    out[k] = v
        fac = n.get("facet")
        if isinstance(fac, dict):
            if "field" in fac:
                out.setdefault("facet", fac)
            for k in ("row", "column"):
                if isinstance(fac.get(k), dict):
                    out.setdefault(k, fac[k])
    return out


def field(chart, channel: str):
    """The field a channel shows, or None: field(chart, "x") -> "nights"."""
    return channels(chart).get(channel, {}).get("field")


def mark_props(chart) -> dict:
    """The properties of the first mark that has any: {"type": "point", "opacity": 0.05}."""
    nodes: list = []
    _walk(spec(chart), nodes)
    for n in nodes:
        if isinstance(n.get("mark"), dict):
            return n["mark"]
    return {}


def resolved(chart) -> dict:
    """The chart's `resolve` block: {"scale": {"y": "independent"}} when panels or layers have their own scale."""
    nodes: list = []
    _walk(spec(chart), nodes)
    for n in nodes:
        if "resolve" in n:
            return n["resolve"]
    return {}


def text_of(chart) -> str:
    """Every title, subtitle and axis or legend title of the chart, joined: what a reader can read on it."""
    nodes: list = []
    _walk(spec(chart), nodes)
    out = []
    for n in nodes:
        t = n.get("title")
        if isinstance(t, str):
            out.append(t)
        elif isinstance(t, list):
            out += [str(x) for x in t]
        elif isinstance(t, dict):
            for k in ("text", "subtitle"):
                x = t.get(k)
                out += [x] if isinstance(x, str) else list(x or [])
    return " | ".join(out)


def show(chart, name: str | None = None):
    """Return the chart for display. In the trainer's run with DS203_FIGS set, also save it as an SVG file."""
    chart.to_dict(validate=True)  # a specification that does not validate fails here, not in the browser
    if FIGS and name:
        Path(FIGS).mkdir(parents=True, exist_ok=True)
        chart.save(str(Path(FIGS) / f"{name}.svg"))
    return chart


# ---------------------------------------------------------------- the written parts: plans and readings

UNITS = {"arrivals": "origin-month", "tickets": "sale", "stays": "stay", "occupancy": "hotel-day", "survey": "response", "complaints": "complaint"}


def plan_check(plan: list[dict]) -> list[str]:
    """The checklist a plan passes before any chart is drawn. Returns what fails, one line each."""
    dd = dictionary()
    fails = []
    if len(plan) != 5:
        fails.append(f"the brief has five asks: the plan has {len(plan)} questions")
    for i, q in enumerate(plan, 1):
        tag = f"Q{i}"
        text = str(q.get("question", ""))
        if not text.strip().endswith("?") or len(text.split()) < 8:
            fails.append(f"{tag}: write the question as one full sentence that ends with a question mark")
        if re.search(r"\b(why|whose fault|problem|actually|good|bad)\b", text.lower()):
            fails.append(f"{tag}: the question still holds a word nobody can measure (why, problem, fault, good, bad)")
        table = q.get("table")
        if table not in dd:
            fails.append(f"{tag}: name one table of the data dictionary as the main table")
            continue
        if q.get("unit") != dd[table]["unit"]:
            fails.append(f"{tag}: the unit of observation is the one the dictionary gives for {table}")
        cols = set(dd[table]["columns"])
        for other in q.get("also", []):
            cols |= set(dd.get(other, {}).get("columns", {}))
        var = q.get("variables", [])
        if len(var) < 2 or any(v not in cols for v in var):
            fails.append(f"{tag}: list at least two variables, each a column of the tables named")
        comp = str(q.get("comparison", ""))
        if not re.search(r"\b(against|between|by|per|with|before|than)\b", comp.lower()) or len(comp.split()) < 5:
            fails.append(f"{tag}: the comparison says what is set against what (by, between, against, per)")
        if q.get("kind") not in ("exploratory", "confirmatory"):
            fails.append(f"{tag}: mark the question exploratory or confirmatory")
    return fails


def reading_check(text: str, must: list, what: str = "the reading") -> bool:
    """A written reading passes when it has two sentences or more and holds every number or word in `must`.

    An entry of `must` may be a list of alternatives: ["median", "typical"].
    """
    t = " ".join(str(text).split())
    low = t.lower().replace(",", "")
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", t) if len(s.split()) >= 4]
    missing = []
    for m in must:
        alts = m if isinstance(m, (list, tuple)) else [m]
        if not any(str(a).lower().replace(",", "") in low for a in alts):
            missing.append(str(alts[0]))
    ok = len(sentences) >= 2 and not missing
    detail = "" if ok else (" · missing: " + ", ".join(missing) if missing else " · write at least two full sentences")
    return check(ok, f"{what} has two sentences and its numbers{detail}")


def table(header: list[str], rows: list[list], fmt: str = "{:.4g}") -> None:
    """Print a small aligned table."""
    cells = [[fmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) for i, h in enumerate(header)]
    print("  ".join(h.ljust(w) for h, w in zip(header, widths)))
    for r in cells:
        print("  ".join(c.rjust(w) for c, w in zip(r, widths)))


def say(title: str, text: str) -> None:
    """Print a written reading under its title, so that it stands in the notebook's output."""
    print(f"{title}\n  " + "\n  ".join(" ".join(str(text).split()).replace(". ", ".\n").split("\n")))


# ---------------------------------------------------------------- lab 3.3: the six charts of the earlier report

def monthly_total() -> pd.DataFrame:
    """Total arrivals per month, all origins: month, arrivals."""
    return arrivals().groupby("month", as_index=False)["arrivals"].sum()


def site_rates() -> pd.DataFrame:
    """Complaints, visitors and complaints per thousand visitors by site."""
    v = tickets().groupby("site")["tickets"].sum().rename("visitors")
    c = complaints().groupby("site").size().rename("complaints")
    df = pd.concat([c, v], axis=1).reset_index()
    df["per_thousand"] = df["complaints"] / df["visitors"] * 1000
    return df


def weekly() -> pd.DataFrame:
    """One row per week: tickets sold at the nine sites and the share of hotel rooms sold. 156 full weeks."""
    t = tickets().groupby("sale_date")["tickets"].sum().rename("tickets")
    o = occupancy().groupby("date")[["rooms_sold", "rooms"]].sum()
    d = pd.concat([t, o], axis=1).fillna(0)
    d["week"] = (np.arange(len(d)) // 7)
    w = d.groupby("week").agg(week_start=("tickets", lambda s: s.index[0]), tickets=("tickets", "sum"),
                              rooms_sold=("rooms_sold", "sum"), rooms=("rooms", "sum"), days=("tickets", "size"))
    w = w[w["days"] == 7].drop(columns="days").reset_index(drop=True)
    w["occupancy"] = w["rooms_sold"] / w["rooms"]
    return w


def hotel_days() -> pd.DataFrame:
    """One row per hotel and day with the day's ticket sales at all sites: date, hotel_id, rooms, rate, tickets_day."""
    daily = tickets().groupby("sale_date")["tickets"].sum().rename("tickets_day")
    d = occupancy().join(daily, on="date")
    d["rate"] = d["rooms_sold"] / d["rooms"]
    return d[["date", "hotel_id", "rooms", "rate", "tickets_day"]]


def misleading(k: int):
    """Chart k (1 to 6) of the earlier report, as Nayef Al-Jumaah drew it: (chart, data, caption).

    Each has one fault. The data handed back is what the repair needs, sometimes more than the chart used.
    """
    A = alt()
    if k == 1:  # the baseline is cut
        s = survey().groupby("year", as_index=False)["satisfaction"].mean()
        c = A.Chart(s).mark_bar().encode(x=A.X("year:O", title="Year"),
                                         y=A.Y("satisfaction:Q", title="Mean satisfaction", scale=A.Scale(domain=[4.0, 4.2], clamp=True)))
        return c.properties(title="Satisfaction collapsed in 2025"), s, "Satisfaction collapsed in 2025"
    if k == 2:  # two months picked out of thirty-six
        m = monthly_total()
        pickd = m[m["month"].isin(pd.to_datetime(["2023-10-01", "2024-10-01"]))].assign(label=lambda d: d["month"].dt.strftime("%b %Y"))
        up = round((pickd["arrivals"].iloc[1] / pickd["arrivals"].iloc[0] - 1) * 100)
        c = A.Chart(pickd).mark_bar().encode(x=A.X("label:N", title=None, sort=None), y=A.Y("arrivals:Q", title="Arrivals"))
        return c.properties(title=f"Arrivals up {up}% in a year"), m, f"Arrivals up {up}% in a year"
    if k == 3:  # counts where rates are needed
        r = site_rates()
        c = A.Chart(r).mark_bar().encode(y=A.Y("site:N", sort="-x", title=None), x=A.X("complaints:Q", title="Complaints, 2023 to 2025"))
        return c.properties(title="The Cable Car is our problem site"), r, "The Cable Car is our problem site"
    if k == 4:  # two axes, each stretched to make the lines meet
        w = weekly()
        base = A.Chart(w).encode(x=A.X("week_start:T", title=None))
        l1 = base.mark_line(color="#D55E00").encode(y=A.Y("tickets:Q", title="Tickets per week", scale=A.Scale(domain=[w["tickets"].min() * 0.95, w["tickets"].max() * 1.05])))
        l2 = base.mark_line(color="#0072B2").encode(y=A.Y("occupancy:Q", title="Hotel occupancy", scale=A.Scale(domain=[w["occupancy"].min() - 0.01, w["occupancy"].max() + 0.01])))
        c = A.layer(l1, l2).resolve_scale(y="independent")
        return c.properties(title="Hotels follow the sites exactly"), w, "Hotels follow the sites exactly"
    if k == 5:  # a running total cannot go down
        a = arrivals()
        r = a[a["origin"] == "Tilal region"].sort_values("month").assign(running=lambda d: d["arrivals"].cumsum())
        c = A.Chart(r).mark_line().encode(x=A.X("month:T", title=None), y=A.Y("running:Q", title="Arrivals since January 2023"))
        return c.properties(title="Local visits keep climbing"), r, "Local visits keep climbing"
    if k == 6:  # uneven steps of time drawn as even steps
        m = monthly_total()
        steps = pd.DataFrame({"period": ["2023", "2024", "Jan-Jun 2025", "Jul 2025", "Aug 2025"],
                              "arrivals": [int(m[m["month"].dt.year == 2023]["arrivals"].sum()), int(m[m["month"].dt.year == 2024]["arrivals"].sum()),
                                           int(m[(m["month"] >= "2025-01-01") & (m["month"] <= "2025-06-01")]["arrivals"].sum()),
                                           int(m[m["month"] == "2025-07-01"]["arrivals"].iloc[0]), int(m[m["month"] == "2025-08-01"]["arrivals"].iloc[0])]})
        c = A.Chart(steps).mark_line(point=True).encode(x=A.X("period:N", sort=None, title=None), y=A.Y("arrivals:Q", title="Arrivals in the period"))
        return c.properties(title="Arrivals fell off a cliff in 2025"), m, "Arrivals fell off a cliff in 2025"
    raise ValueError("k is 1 to 6")


FAULTS = {"cut baseline": "a bar or area whose axis does not start at zero",
          "picked window": "a few periods chosen out of many",
          "count for rate": "a count compared across groups of unequal size",
          "two axes": "two scales on one chart, stretched until the shapes agree",
          "running total": "a cumulative line, which can only rise",
          "uneven steps": "periods of unequal length drawn as equal steps",
          "colour only": "groups told apart by colour alone",
          "no fault": "nothing misleads here"}


# ---------------------------------------------------------------- lab 3.4: colour-vision deficiency

_CVD = {"deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
        "protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]}


def _lin(hexcode: str) -> np.ndarray:
    c = np.array([int(hexcode.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def simulate(hexcode: str, kind: str = "deuteranopia") -> str:
    """The colour as a viewer with the named deficiency sees it (the matrices of Machado, Oliveira and Fernandes, 2009)."""
    lin = np.clip(np.array(_CVD[kind]) @ _lin(hexcode), 0, 1)
    srgb = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return "#" + "".join(f"{int(round(v * 255)):02x}" for v in np.clip(srgb, 0, 1))


def _lab(hexcode: str) -> np.ndarray:
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = (m @ _lin(hexcode)) / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def closest_pair(palette: list[str], kind: str | None = None) -> tuple[float, str, str]:
    """The two colours of a palette that are hardest to tell apart, and their distance in CIELAB units (below about 10 is hard to tell apart)."""
    cols = [simulate(c, kind) if kind else c for c in palette]
    best = (1e9, "", "")
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            d = float(np.linalg.norm(_lab(cols[i]) - _lab(cols[j])))
            if d < best[0]:
                best = (d, palette[i], palette[j])
    return best


# ---------------------------------------------------------------- lab 4.4: a report that reruns

def render_report(params: dict, name: str = "board_note") -> dict:
    """Run report/board_note.py from top to bottom in a fresh kernel and write out/<name>.html.

    `params` replaces the report's parameter cell. Returns the path of the HTML file, the numbers the report
    printed and a digest of them: two runs that agree have the same digest.
    """
    import nbformat
    from nbclient import NotebookClient
    from nbconvert import HTMLExporter

    cells, kind, buf = [], None, []

    def flush():
        if kind and "".join(buf).strip():
            text = "\n".join(buf).strip("\n")
            if kind == "markdown":
                text = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in text.split("\n"))
                cells.append(nbformat.v4.new_markdown_cell(text))
            else:
                if text.startswith("# parameters"):
                    text = "# parameters\nPARAMS = " + repr(params)
                cells.append(nbformat.v4.new_code_cell(text))

    for line in (LABS / "report" / "board_note.py").read_text(encoding="utf-8").splitlines():
        if line.startswith("# %%"):
            flush()
            kind, buf = ("markdown" if "[markdown]" in line else "code"), []
        else:
            buf.append(line)
    flush()
    nb = nbformat.v4.new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}})
    env = dict(os.environ)
    env.pop("DS203_WRITE_REF", None)
    env.pop("DS203_FIGS", None)
    NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": str(LABS)}}).execute(env=env)
    numbers = {}
    for c in nb.cells:
        for o in c.get("outputs", []):
            m = re.search(r"^NUMBERS (\{.*\})$", o.get("text", ""), re.M)
            if m:
                numbers.update(json.loads(m.group(1)))
    html, _ = HTMLExporter(exclude_input=True).from_notebook_node(nb)
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{name}.html"
    path.write_text(html, encoding="utf-8")
    digest = hashlib.sha256(json.dumps(numbers, sort_keys=True).encode()).hexdigest()[:12]
    return {"path": str(path.relative_to(LABS)).replace("\\", "/"), "numbers": numbers, "digest": digest, "kilobytes": round(len(html) / 1024)}


def digest(obj) -> str:
    """A short fingerprint of an answer, so that a check can compare it without printing the key."""
    return hashlib.sha256(json.dumps(_jsonable(obj), sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:10]


def matches(lab: str, name: str, value) -> bool:
    """True when an answer has the fingerprint of the key. The trainer's run records the fingerprint."""
    path = REF / "keys.json"
    store = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    key = f"{lab}/{name}"
    if WRITE_REF:
        store[key] = digest(value)
        REF.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(store, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return store.get(key) == digest(value)
