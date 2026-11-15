"""Write the synthetic data of Tilal Regional Tourism Board into labs/data/ and labs/capstone/data/.

    uv run python prepare_data.py

Fixed seed, the same bytes on every run. The board, its region, its sites, its hotels and every
record are fictional: no real visitor, hotel or organisation is described. The files are
committed; run this only to rebuild them.

What is planted, and which lab finds it, is listed in solutions/answer_key.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 203
LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
CAP = LABS / "capstone" / "data"

DAYS = pd.date_range("2023-01-01", "2025-12-31", freq="D")
MONTHS = pd.period_range("2023-01", "2025-12", freq="M")
ORIGINS = ["Tilal region", "Other regions", "Gulf", "Asia", "Europe"]
# site id, name, share of sales, ticket price in riyals, complaint-rate multiplier
SITES = [("S1", "Cable Car", 0.26, 40, 1.00), ("S2", "Souq Walk", 0.18, 10, 0.80), ("S3", "Tilal Fort", 0.14, 25, 0.90),
         ("S4", "Juniper Park", 0.12, 15, 0.70), ("S5", "Stone Village", 0.09, 30, 1.10), ("S6", "Honey Museum", 0.07, 20, 0.75),
         ("S7", "Cloud Lookout", 0.06, 15, 1.20), ("S8", "Wadi Trail", 0.05, 35, 1.80), ("S9", "Terrace Farms", 0.03, 20, 2.60)]
SITE_NAMES = [s[1] for s in SITES]
# how much more (or less) each origin market goes to each site than the average visitor
AFFINITY = {"Tilal region": {"Souq Walk": 1.5, "Cable Car": 0.8, "Terrace Farms": 1.4},
            "Other regions": {},
            "Gulf": {"Cable Car": 1.3, "Honey Museum": 1.3},
            "Asia": {"Cable Car": 1.3, "Terrace Farms": 0.5},
            "Europe": {"Wadi Trail": 3.0, "Stone Village": 2.0, "Terrace Farms": 0.5, "Cable Car": 0.7}}

LEVEL = {"Tilal region": 22000, "Other regions": 30000, "Gulf": 9000, "Asia": 4000, "Europe": 3000}
GROWTH = {"Tilal region": -0.05, "Other regions": 0.06, "Gulf": 0.18, "Asia": 0.30, "Europe": 0.25}
SEASON = {"Tilal region": [0.90, 0.90, 0.95, 1.00, 1.00, 1.10, 1.20, 1.20, 1.00, 0.95, 0.90, 0.90],
          "Other regions": [0.75, 0.78, 0.90, 0.95, 0.95, 1.25, 1.50, 1.45, 0.95, 0.90, 0.80, 0.82],
          "Gulf": [0.50, 0.55, 0.70, 0.80, 0.90, 1.50, 1.90, 1.80, 0.90, 0.75, 0.60, 0.60],
          "Asia": [0.95, 0.95, 1.00, 1.05, 1.00, 1.00, 1.10, 1.10, 1.00, 1.00, 0.95, 0.90],
          "Europe": [1.40, 1.40, 1.30, 1.00, 0.70, 0.60, 0.60, 0.60, 0.80, 1.10, 1.20, 1.30]}
# the two planted festivals: month -> multiplier by origin (lab 2.3)
FESTIVALS = {"2024-10": ("Honey Festival", {"Tilal region": 1.30, "Other regions": 1.40, "Gulf": 1.15}),
             "2025-10": ("Honey Festival", {"Tilal region": 1.30, "Other regions": 1.40, "Gulf": 1.15}),
             "2025-02": ("Heritage Nights", {"Tilal region": 1.20, "Other regions": 1.30, "Gulf": 1.10, "Europe": 1.10})}

# satisfaction, 1 to 5: mean by origin in 2024, the gain in 2025, and the mix of responses by year (lab 2.4)
SAT_2024 = {"Tilal region": 4.50, "Other regions": 4.20, "Gulf": 3.70, "Asia": 3.40, "Europe": 3.30}
SAT_SHIFT = {2023: -0.03, 2024: 0.0, 2025: 0.10}
SURVEY_N = {2023: 1800, 2024: 2000, 2025: 2200}
SURVEY_MIX = {2023: [0.42, 0.35, 0.11, 0.06, 0.06], 2024: [0.40, 0.35, 0.12, 0.07, 0.06], 2025: [0.26, 0.30, 0.19, 0.13, 0.12]}
GUIDED_LIFT = 0.55  # on the hidden score that orders responses inside an origin and year

COMPLAINT_RATE = 6.0  # per thousand visitors, before the site multiplier
PUBLISH_MIN_COMPLAINTS, PUBLISH_MIN_VISITORS = 10, 1000


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        df.to_csv(path, index=False, lineterminator="\n", compression={"method": "gzip", "mtime": 0, "compresslevel": 9})
    else:
        df.to_csv(path, index=False, lineterminator="\n")


def write_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def keys(rng, n: int, prefix: str) -> list[str]:
    """Pseudonymised keys: a prefix and eight hexadecimal digits, unique, in no meaningful order."""
    out: set[str] = set()
    while len(out) < n:
        out.update(f"{prefix}{v:08x}" for v in rng.integers(0, 16 ** 8, size=n - len(out)))
    out_list = sorted(out)
    rng.shuffle(out_list)
    return out_list


def is_weekend(dates) -> np.ndarray:
    """Friday and Saturday."""
    return np.isin(pd.DatetimeIndex(dates).day_of_week, [4, 5])


# ---------------------------------------------------------------- arrivals

def make_arrivals(rng) -> pd.DataFrame:
    rows = []
    for o in ORIGINS:
        season = np.array(SEASON[o]) / np.mean(SEASON[o])
        for i, m in enumerate(MONTHS):
            v = LEVEL[o] * (1 + GROWTH[o]) ** (i / 12) * season[m.month - 1]
            v *= FESTIVALS.get(str(m), ("", {}))[1].get(o, 1.0)
            v *= 1 + rng.normal(0, 0.025)
            rows.append({"month": str(m), "origin": o, "arrivals": int(round(v))})
    return pd.DataFrame(rows)


def day_origin_weights(arrivals: pd.DataFrame) -> pd.DataFrame:
    """One weight for each day and origin: the month's arrivals spread over its days, weekends busier."""
    wide = arrivals.pivot(index="month", columns="origin", values="arrivals")[ORIGINS]
    month = DAYS.to_period("M").astype(str)
    w = wide.loc[month].to_numpy(float) / DAYS.days_in_month.to_numpy()[:, None]
    w *= np.where(is_weekend(DAYS), 1.45, 0.82)[:, None]
    return pd.DataFrame(w, index=DAYS, columns=ORIGINS)


def draw_day_origin(rng, weights: pd.DataFrame, n: int, days_mask=None, origin=None):
    w = weights.to_numpy().copy()
    if days_mask is not None:
        w[~days_mask] = 0
    if origin is not None:
        keep = np.array([o == origin for o in ORIGINS])
        w[:, ~keep] = 0
    flat = rng.choice(w.size, size=n, p=(w / w.sum()).ravel())
    d, o = np.unravel_index(flat, w.shape)
    return DAYS[d], np.array(ORIGINS)[o]


def draw_sites(rng, origins: np.ndarray) -> np.ndarray:
    out = np.empty(len(origins), dtype=object)
    for o in ORIGINS:
        p = np.array([s[2] * AFFINITY[o].get(s[1], 1.0) for s in SITES])
        idx = np.where(origins == o)[0]
        out[idx] = rng.choice(SITE_NAMES, size=len(idx), p=p / p.sum())
    return out


# ---------------------------------------------------------------- tickets, complaints, occupancy

def make_tickets(rng, weights) -> pd.DataFrame:
    dates, origins = draw_day_origin(rng, weights, 150_000)
    sites = draw_sites(rng, origins)
    qty = np.clip(1 + rng.poisson(np.where(origins == "Tilal region", 1.3, 1.8)), 1, 8)
    price = pd.Series(sites).map({s[1]: s[3] for s in SITES}).to_numpy()
    discount = rng.choice([1.0, 0.85, 0.7], size=len(qty), p=[0.7, 0.2, 0.1])
    df = pd.DataFrame({"sale_date": dates, "site": sites, "origin": origins, "tickets": qty,
                       "amount_sar": np.round(qty * price * discount).astype(int)})
    df = df.sort_values(["sale_date", "site", "origin"], kind="stable").reset_index(drop=True)
    df.insert(0, "sale_id", [f"K{i:07d}" for i in range(1, len(df) + 1)])
    df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")
    return df


def make_complaints(rng, tickets: pd.DataFrame) -> pd.DataFrame:
    mult = {s[1]: s[4] for s in SITES}
    cats = ["queue", "cleanliness", "price", "signage", "staff", "access"]
    rows = []
    for (site, origin), g in tickets.groupby(["site", "origin"], sort=True):
        visitors = int(g["tickets"].sum())
        n = int(rng.poisson(visitors * COMPLAINT_RATE / 1000 * mult[site] * (1.15 if origin == "Europe" else 1.0)))
        p = np.array([3.0 if site == "Cable Car" else 1.0, 1.0, 1.0, 2.0 if site in ("Wadi Trail", "Terrace Farms") else 1.0, 0.8, 0.7])
        for d, c in zip(rng.choice(g["sale_date"].to_numpy(), size=n), rng.choice(cats, size=n, p=p / p.sum())):
            rows.append({"complaint_date": d, "site": site, "origin": origin, "category": c})
    df = pd.DataFrame(rows).sort_values(["complaint_date", "site", "origin", "category"], kind="stable").reset_index(drop=True)
    df.insert(0, "complaint_id", [f"C{i:05d}" for i in range(1, len(df) + 1)])
    return df


def make_occupancy(rng, tickets: pd.DataFrame) -> pd.DataFrame:
    daily = tickets.groupby("sale_date")["tickets"].sum().reindex(DAYS.strftime("%Y-%m-%d")).fillna(0).to_numpy(float)
    z = (np.log(daily + 1) - np.log(daily + 1).mean()) / np.log(daily + 1).std()
    zones = ["Centre", "Ridge", "Valley", "Old Town"]
    shared = np.repeat(rng.normal(0, 0.28, len(DAYS) // 7 + 1), 7)[: len(DAYS)]  # business the sites do not explain, week by week
    frames = []
    for h in range(1, 41):
        rooms = int(np.clip(round(float(np.exp(rng.normal(np.log(45), 0.9)))), 8, 240))
        base = rng.normal(0.2, 0.5)
        logit = base + 0.42 * z + shared + 0.25 * is_weekend(DAYS) + rng.normal(0, 0.9, len(DAYS))
        sold = rng.binomial(rooms, 1 / (1 + np.exp(-logit)))
        frames.append(pd.DataFrame({"date": DAYS.strftime("%Y-%m-%d"), "hotel_id": f"H{h:02d}", "zone": zones[(h * 7) % 4],
                                    "rooms": rooms, "rooms_sold": sold}))
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------- stays (the visitor table)

def make_stays(rng, weights):
    n = 40_000
    dates, origins = draw_day_origin(rng, weights, n)
    nights = np.zeros(n, dtype=int)
    for o in ORIGINS:
        idx = np.where(origins == o)[0]
        k = len(idx)
        if o == "Tilal region":
            v = np.where(rng.random(k) < 0.80, 0, 1 + rng.poisson(0.6, k))
        elif o == "Other regions":  # two kinds of trip: a weekend and a week
            v = np.where(rng.random(k) < 0.62, 1 + rng.binomial(2, 0.5, k), 5 + rng.poisson(2.2, k))
        elif o == "Gulf":
            v = 1 + rng.negative_binomial(4, 0.5, k)
        elif o == "Asia":
            v = 1 + rng.negative_binomial(3, 0.5, k)
        else:
            v = 2 + rng.negative_binomial(3, 0.35, k)
        nights[idx] = v
    party = np.clip(1 + rng.poisson(1.8, n), 1, 9)
    spend = np.exp(rng.normal(np.log(180 + 420 * nights) + 0.25 * np.log(party), 0.75))
    lead = np.where(rng.random(n) < np.where(nights == 0, 0.75, 0.25), 0,
                    np.clip(np.round(np.exp(rng.normal(np.log(14), 1.1, n))), 1, 365)).astype(int)
    purpose = np.empty(n, dtype=object)
    for o, p in {"Tilal region": [0.70, 0.22, 0.03, 0.05], "Other regions": [0.60, 0.25, 0.07, 0.08], "Gulf": [0.72, 0.15, 0.05, 0.08],
                 "Asia": [0.55, 0.05, 0.30, 0.10], "Europe": [0.75, 0.03, 0.12, 0.10]}.items():
        idx = np.where(origins == o)[0]
        purpose[idx] = rng.choice(["leisure", "family visit", "business", "event"], size=len(idx), p=p)
    acc = np.where(nights == 0, "none", rng.choice(["hotel", "apartment", "with family", "camp"], size=n, p=[0.55, 0.25, 0.15, 0.05]))
    df = pd.DataFrame({"stay_id": keys(rng, n, "T"), "arrival_date": dates.strftime("%Y-%m-%d"), "origin": origins,
                       "purpose": purpose, "party_size": party, "nights": nights, "accommodation": acc,
                       "spend_sar": np.round(spend).astype(float), "booking_lead_days": lead,
                       "age_band": rng.choice(["18-29", "30-44", "45-59", "60+"], size=n, p=[0.27, 0.38, 0.24, 0.11])})
    df = df.sort_values(["arrival_date", "stay_id"], kind="stable").reset_index(drop=True)
    clean = df.copy()

    # the planted data issues of lab 1.2
    issues = {}
    miss = rng.random(n) < np.where(df["nights"] == 0, 0.22, 0.02)           # 1: spend missing, mostly for day visitors
    df.loc[miss, "spend_sar"] = np.nan
    issues["spend_missing"] = int(miss.sum())
    issues["spend_missing_share_day_visitors"] = round(float(miss[(df["nights"] == 0).to_numpy()].mean()), 4)
    issues["spend_missing_share_overnight"] = round(float(miss[(df["nights"] > 0).to_numpy()].mean()), 4)
    sentinel = rng.choice(n, size=320, replace=False)                       # 2: 999 stands for "not recorded"
    df.loc[sentinel, "nights"] = 999
    issues["nights_999"] = 320
    gulf = np.where(df["origin"] == "Gulf")[0]                               # 3: one market, three spellings
    r = rng.random(len(gulf))
    df.loc[gulf[r < 0.07], "origin"] = "GCC"
    df.loc[gulf[(r >= 0.07) & (r < 0.10)], "origin"] = "gulf "
    issues["origin_spellings"] = {"GCC": int((r < 0.07).sum()), "gulf ": int(((r >= 0.07) & (r < 0.10)).sum())}
    typo = rng.choice(n, size=14, replace=False)                            # 4: arrival years that have not happened
    df.loc[typo, "arrival_date"] = df.loc[typo, "arrival_date"].str.replace(r"^202\d", "2032", regex=True)
    issues["dates_2032"] = 14
    dup = df.iloc[rng.choice(n, size=600, replace=False)]                   # 5: 600 rows entered twice
    df = pd.concat([df, dup], ignore_index=True).sort_values(["arrival_date", "stay_id"], kind="stable").reset_index(drop=True)
    issues["duplicate_rows"] = 600
    issues["rows"] = len(df)
    return df, clean, issues


# ---------------------------------------------------------------- survey

def quota_scores(n: int, mean: float) -> np.ndarray:
    """n whole scores from 1 to 5 whose mean is as close to `mean` as n allows, highest first."""
    k = np.arange(1, 6)
    lo, hi = -5.0, 12.0
    for _ in range(60):
        mu = (lo + hi) / 2
        p = np.exp(-((k - mu) ** 2) / (2 * 0.95 ** 2))
        p /= p.sum()
        lo, hi = (mu, hi) if (p * k).sum() < mean else (lo, mu)
    raw = p * n
    counts = np.floor(raw).astype(int)
    for i in np.argsort(-(raw - counts))[: n - counts.sum()]:
        counts[i] += 1
    return np.repeat(k[::-1], counts[::-1])


COMMENTS = {
    "en": {5: ["Wonderful views and helpful staff.", "The best stop of our trip.", "Clean, calm and well organised."],
           4: ["A good visit, we would come back.", "Nice site, the guide knew a lot.", "Worth the ticket."],
           3: ["Fine, but the queue was long.", "Average. Signs were hard to follow.", "Good view, little shade."],
           2: ["Too crowded and the toilets were not clean.", "Expensive for what it offers.", "We could not find the entrance."],
           1: ["Waited over an hour and left.", "Closed without notice. Very disappointing.", "Dirty and badly kept."]},
    "ar": {5: ["إطلالة رائعة وموظفون متعاونون.", "أجمل محطة في رحلتنا.", "المكان نظيف وهادئ ومنظم."],
           4: ["زيارة جيدة وسنعود مرة أخرى.", "موقع جميل والمرشد ملمّ بالتفاصيل.", "يستحق قيمة التذكرة."],
           3: ["لا بأس، لكن الطابور كان طويلًا.", "تجربة متوسطة واللوحات غير واضحة.", "الإطلالة جميلة والظل قليل."],
           2: ["ازدحام شديد ودورات المياه غير نظيفة.", "السعر مرتفع مقارنة بما يقدمه الموقع.", "لم نجد المدخل بسهولة."],
           1: ["انتظرنا أكثر من ساعة ثم غادرنا.", "الموقع مغلق دون إشعار. مخيّب للآمال.", "المكان غير نظيف وسيئ الصيانة."]},
}
P_ARABIC = {"Tilal region": 0.97, "Other regions": 0.95, "Gulf": 0.93, "Asia": 0.05, "Europe": 0.04}
P_GUIDED = {"Cable Car": 0.10, "Souq Walk": 0.55, "Tilal Fort": 0.45, "Juniper Park": 0.15, "Stone Village": 0.40,
            "Honey Museum": 0.50, "Cloud Lookout": 0.05, "Wadi Trail": 0.35, "Terrace Farms": 0.40}


def perm_p(x: np.ndarray, flag: np.ndarray, rng, b: int = 2000) -> float:
    obs = x[flag].mean() - x[~flag].mean()
    n1 = int(flag.sum())
    hits = 0
    for _ in range(b):
        s = rng.permutation(x)
        hits += abs(s[:n1].mean() - s[n1:].mean()) >= abs(obs)
    return (hits + 1) / (b + 1)


def make_survey(rng, weights):
    frames = []
    for year, n in SURVEY_N.items():
        counts = np.round(np.array(SURVEY_MIX[year]) * n).astype(int)
        counts[0] += n - counts.sum()
        mask = (DAYS.year == year)
        for o, k in zip(ORIGINS, counts):
            dates, _ = draw_day_origin(rng, weights, int(k), days_mask=mask, origin=o)
            frames.append(pd.DataFrame({"visit_date": dates, "origin": o, "year": year}))
    df = pd.concat(frames, ignore_index=True)
    df["site"] = draw_sites(rng, df["origin"].to_numpy())
    df["language"] = np.where(rng.random(len(df)) < df["origin"].map(P_ARABIC), "ar", "en")
    df["guided"] = (rng.random(len(df)) < df["site"].map(P_GUIDED)).astype(int)
    weekend = is_weekend(df["visit_date"])

    # Scores are fixed by quota inside each origin and year (the planted reversal is exact), and ordered inside
    # the cell by a hidden score that guided visits lift. Nothing else enters: site and day of the week have no
    # effect on satisfaction. The chance patterns of labs 4.1 and 4.3 are found by trying seeds until a striking
    # one appears, which is how a searched pattern arises in a real report.
    for attempt in range(400):
        g = np.random.default_rng(SEED * 1000 + attempt)
        hidden = g.normal(0, 1, len(df)) + GUIDED_LIFT * df["guided"].to_numpy()
        sat = np.zeros(len(df), dtype=int)
        for (o, y), idx in df.groupby(["origin", "year"], sort=True).indices.items():
            order = idx[np.argsort(-hidden[idx], kind="stable")]
            sat[order] = quota_scores(len(idx), SAT_2024[o] + SAT_SHIFT[y])
        x = sat.astype(float)
        gap_all = x[weekend].mean() - x[~weekend].mean()
        if not (0.02 <= gap_all <= 0.06):
            continue
        p_all = perm_p(x, weekend, g, 1000)
        if not (0.12 <= p_all <= 0.60):
            continue
        cells = []
        for (s, y), idx in df.groupby(["site", "year"], sort=True).indices.items():
            w = weekend[idx]
            cells.append((perm_p(x[idx], w, g, 1500), s, int(y), float(x[idx][w].mean() - x[idx][~w].mean()), int(w.sum()), int((~w).sum())))
        cells.sort()
        if 0.01 <= cells[0][0] <= 0.03 and cells[0][2] == 2025 and cells[0][3] > 0 and cells[1][0] > 0.06:
            break
    else:
        raise SystemExit("no seed gave the planted chance pattern; widen the search")
    df["satisfaction"] = sat
    lang = df["language"].to_numpy()
    pick = rng.integers(0, 3, len(df))
    comment = np.array([COMMENTS[l][s][i] for l, s, i in zip(lang, sat, pick)], dtype=object)
    comment[rng.random(len(df)) < 0.35] = ""
    df["comment"] = comment
    df = df.sort_values(["visit_date", "site", "origin"], kind="stable").reset_index(drop=True)
    df.insert(0, "response_id", [f"R{i:05d}" for i in range(1, len(df) + 1)])
    df["visit_date"] = df["visit_date"].dt.strftime("%Y-%m-%d")
    truth = {"attempt": attempt, "weekend_gap_all": round(float(gap_all), 4), "weekend_p_all_about": round(float(p_all), 3),
             "headline_cell": {"site": cells[0][1], "year": cells[0][2], "gap": round(cells[0][3], 3), "p_about": round(cells[0][0], 4),
                               "n_weekend": cells[0][4], "n_weekday": cells[0][5]},
             "cells_compared": len(cells), "cells_below_0.05": int(sum(c[0] < 0.05 for c in cells))}
    return df.drop(columns="year"), truth


# ---------------------------------------------------------------- supplied text files

BRIEF = """# Brief from the director

To: Leen Al-Suwayigh, analyst
From: Nawal Al-Rashoud, director, Tilal Regional Tourism Board
Subject: What the last three years tell us, before the board meets

Leen, the board meets in two weeks and I want to walk in knowing where we stand. I do not need
a dashboard. I need answers I can repeat.

1. Who is actually coming, and do they stay? I keep hearing that our visitors "pop in and leave".
2. Aws says a busy day at the sites means full hotels. Rashed is not so sure. Which is it?
3. Atheer's team logged a lot of complaints about the Cable Car. Is that our problem site?
4. Did the festivals bring people, or would they have come anyway?
5. Satisfaction went down last year. Why, and whose fault is it?

Use what we have: the arrivals estimates, ticket sales, the stay register, the hotels' occupancy
returns, the visitor survey and the complaints log, 2023 to 2025. Hanouf reminds everyone that
nothing about an identifiable visitor leaves the building, and that small groups do not go in
a public table.

Nawal
"""

DICTIONARY = {
    "arrivals": {"file": "arrivals.csv", "unit": "one origin market in one month", "rows": 180, "columns": {
        "month": "year and month, 2023-01 to 2025-12", "origin": "origin market, five values", "arrivals": "the board's estimate of visitors who arrived"}},
    "tickets": {"file": "tickets.csv.gz", "unit": "one ticket sale at one site", "rows": 150000, "columns": {
        "sale_id": "sale number", "sale_date": "date of the sale", "site": "one of nine sites", "origin": "origin market the buyer stated",
        "tickets": "tickets in the sale, which is the number of visitors", "amount_sar": "amount paid in riyals"}},
    "stays": {"file": "stays.csv.gz", "unit": "one visiting party's stay in the region", "rows": "about 40,000", "columns": {
        "stay_id": "pseudonymised key of the stay, never a name", "arrival_date": "date the party arrived", "origin": "origin market",
        "purpose": "leisure, family visit, business or event", "party_size": "people in the party", "nights": "nights spent in the region; 0 is a day visit",
        "accommodation": "hotel, apartment, with family, camp or none", "spend_sar": "what the party said it spent in the region, riyals",
        "booking_lead_days": "days between booking and arrival; 0 is no booking", "age_band": "age band of the person who answered"}},
    "occupancy": {"file": "occupancy.csv.gz", "unit": "one hotel on one day", "rows": 43840, "columns": {
        "date": "the night", "hotel_id": "pseudonymised hotel code", "zone": "one of four zones", "rooms": "rooms the hotel has", "rooms_sold": "rooms sold that night"}},
    "survey": {"file": "survey.csv", "unit": "one visitor's response after a site visit", "rows": 6000, "columns": {
        "response_id": "response number", "visit_date": "date of the visit", "origin": "origin market", "site": "site visited",
        "language": "language of the response, ar or en", "guided": "1 when the visit was a guided one", "satisfaction": "overall satisfaction, 1 (low) to 5 (high)",
        "comment": "a short free-text comment, often empty"}},
    "complaints": {"file": "complaints.csv", "unit": "one complaint logged by the visitor experience team", "rows": "about 2,400", "columns": {
        "complaint_id": "complaint number", "complaint_date": "date logged", "site": "site complained about", "origin": "origin market of the visitor",
        "category": "queue, cleanliness, price, signage, staff or access"}},
}

PAST_FINDINGS = [
    {"id": "F1", "finding": "International visitors stay longer than visitors from other regions of the Kingdom.",
     "how": "The 2023 plan named this comparison before the stay register was opened; the 2023 register was then used once, for this."},
    {"id": "F2", "finding": "Visitors who arrive on a Tuesday spend the most.",
     "how": "The analyst tabulated spend by every day of the week, every origin and every purpose, and reported the largest cell."},
    {"id": "F3", "finding": "Guided visits are rated higher than unguided ones.",
     "how": "First noticed in the 2023 survey. The board then wrote the question down and tested it on the 2024 survey, which had not been looked at."},
    {"id": "F4", "finding": "Hotels in the Ridge zone fill up before the Honey Festival.",
     "how": "Seen in a chart of 2024 occupancy while looking for something else. Not checked on another year."},
    {"id": "F5", "finding": "Satisfaction at the Wadi Trail drops in months with rain.",
     "how": "Found after trying weather, school holidays and day of the week against satisfaction at each of nine sites."},
]
PAST_KEY = {"F1": {"status": "confirmed", "check": "none: the comparison was planned and the data used once"},
            "F2": {"status": "exploratory", "check": "name the Tuesday comparison in advance and test it on a new year of stays"},
            "F3": {"status": "confirmed", "check": "none: found in one year, written down, tested on a year not yet seen"},
            "F4": {"status": "exploratory", "check": "test the same weeks before the 2025 festival, stated before looking"},
            "F5": {"status": "exploratory", "check": "count the comparisons tried, then test rain months at the Wadi Trail on new responses"}}

LABELS = {
    "sites": {"Cable Car": "العربات المعلّقة", "Souq Walk": "جولة السوق", "Tilal Fort": "قلعة تِلال", "Juniper Park": "منتزه العرعر",
              "Stone Village": "القرية الحجرية", "Honey Museum": "متحف العسل", "Cloud Lookout": "مطلّ السحاب", "Wadi Trail": "درب الوادي",
              "Terrace Farms": "المدرّجات الزراعية"},
    "origins": {"Tilal region": "منطقة تِلال", "Other regions": "مناطق المملكة الأخرى", "Gulf": "دول الخليج", "Asia": "آسيا", "Europe": "أوروبا"},
    "text": {"en": {"title": "Arrivals grew fastest from the smallest markets", "subtitle": "Yearly arrivals by origin market, 2023 = 100",
                    "x": "Year", "y": "Arrivals, 2023 = 100", "legend": "Origin market", "source": "Source: Tilal Regional Tourism Board, arrivals estimates (synthetic data)"},
             "ar": {"title": "أسرع نموّ في أعداد القادمين جاء من أصغر الأسواق", "subtitle": "أعداد القادمين سنويًا بحسب سوق المصدر، سنة 2023 = 100",
                    "x": "السنة", "y": "القادمون، 2023 = 100", "legend": "سوق المصدر", "source": "المصدر: مجلس تِلال الإقليمي للسياحة، تقديرات أعداد القادمين (بيانات اصطناعية)"}},
}


# ---------------------------------------------------------------- the capstone datasets (not used in class)

def capstone_set(seed: int, units: list[str], groups: list[str], cols: dict, event_month: str) -> pd.DataFrame:
    """A two-year event table with a season, one event month, a reversal by group between the years and no weekday effect."""
    rng = np.random.default_rng(seed)
    days = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    season = 1 + 0.35 * np.sin((days.day_of_year.to_numpy() - 20) / 365 * 2 * np.pi)
    w = season * np.where(days.to_period("M").astype(str) == event_month, 1.6, 1.0) * np.where(days.year == 2025, 1.12, 1.0)
    n = 12_000
    d = days[rng.choice(len(days), size=n, p=w / w.sum())]
    year = d.year.to_numpy()
    mix = {2024: [0.45, 0.30, 0.15, 0.10], 2025: [0.25, 0.27, 0.24, 0.24]}
    group = np.where(year == 2024, rng.choice(groups, size=n, p=mix[2024]), rng.choice(groups, size=n, p=mix[2025]))
    unit_p = np.array([0.24, 0.18, 0.15, 0.13, 0.11, 0.09, 0.06, 0.04])
    unit = rng.choice(units, size=n, p=unit_p)
    gi = pd.Series(group).map({g: i for i, g in enumerate(groups)}).to_numpy()
    base = np.array([4.4, 4.1, 3.6, 3.3])[gi] + np.where(year == 2025, 0.10, 0.0)
    rating = np.clip(np.round(base + rng.normal(0, 0.9, n)), 1, 5).astype(int)
    skew = np.round(np.exp(rng.normal(np.log(cols["skew_median"]) + 0.25 * gi, 0.8, n)), cols.get("skew_digits", 0))
    count = np.clip(1 + rng.poisson(1.2 + 0.5 * gi, n), 1, 12)
    flag = (rng.random(n) < 0.12 + 0.05 * (unit == units[-1]) + 0.03 * gi).astype(int)
    df = pd.DataFrame({cols["date"]: d.strftime("%Y-%m-%d"), cols["unit"]: unit, cols["group"]: group, cols["count"]: count,
                       cols["skew"]: skew, cols["rating"]: rating, cols["flag"]: flag})
    df.loc[rng.choice(n, size=240, replace=False), cols["skew"]] = np.nan
    df = pd.concat([df, df.iloc[rng.choice(n, size=150, replace=False)]], ignore_index=True)
    df = df.sort_values([cols["date"], cols["unit"], cols["group"]], kind="stable").reset_index(drop=True)
    df.insert(0, cols["id"], keys(rng, len(df), cols["prefix"]))
    return df


CAPSTONE = {
    "ruwaq_museums": {
        "organisation": "Ruwaq Museums Network", "audience": "the network's head of programmes, who is not an analyst",
        "units": ["Main Gallery", "Science Hall", "Craft House", "Coin Room", "Maritime Wing", "Children's Museum", "Manuscript Hall", "Garden Pavilion"],
        "groups": ["school group", "family", "adult", "tourist"], "event_month": "2025-03",
        "cols": {"id": "visit_id", "prefix": "V", "date": "visit_date", "unit": "museum", "group": "visitor_type", "count": "party_size",
                 "skew": "minutes_inside", "skew_median": 55, "rating": "rating", "flag": "member"},
        "meaning": {"visit_id": "pseudonymised key of one visit", "visit_date": "date of the visit", "museum": "one of eight museums", "visitor_type": "school group, family, adult or tourist",
                    "party_size": "people in the party", "minutes_inside": "minutes between entry and exit scans", "rating": "exit rating, 1 to 5", "member": "1 when the party holds a membership"}},
    "awan_parks": {
        "organisation": "Awan Parks Department", "audience": "the head of park operations, who is not an analyst",
        "units": ["Central Park", "Lake Park", "North Gardens", "Hill Park", "Palm Walk", "East Playground", "Riverside", "Old Orchard"],
        "groups": ["lighting", "cleaning", "play equipment", "irrigation"], "event_month": "2024-11",
        "cols": {"id": "request_id", "prefix": "Q", "date": "opened_date", "unit": "park", "group": "category", "count": "visits_needed",
                 "skew": "days_to_close", "skew_median": 3, "skew_digits": 1, "rating": "resident_rating", "flag": "reopened"},
        "meaning": {"request_id": "pseudonymised key of one maintenance request", "opened_date": "date the request was opened", "park": "one of eight parks", "category": "lighting, cleaning, play equipment or irrigation",
                    "visits_needed": "crew visits before the request was closed", "days_to_close": "days from opening to closing", "resident_rating": "rating by the resident who reported, 1 to 5", "reopened": "1 when the request was opened again"}},
    "miqdam_driving": {
        "organisation": "Miqdam Driving Schools", "audience": "the schools' director of training, who is not an analyst",
        "units": ["Airport Road", "University", "North Gate", "Corniche", "Industrial", "Old Town", "Hillside", "East Ring"],
        "groups": ["18-21", "22-29", "30-44", "45+"], "event_month": "2025-06",
        "cols": {"id": "test_id", "prefix": "D", "date": "test_date", "unit": "branch", "group": "age_band", "count": "attempt",
                 "skew": "wait_days", "skew_median": 9, "rating": "course_rating", "flag": "failed"},
        "meaning": {"test_id": "pseudonymised key of one driving test", "test_date": "date of the test", "branch": "one of eight branches", "age_band": "age band of the learner",
                    "attempt": "which attempt this test was", "wait_days": "days waited for the test slot", "course_rating": "learner's rating of the course, 1 to 5", "failed": "1 when the test was failed"}},
}


def main() -> None:
    rng = np.random.default_rng(SEED)
    arrivals = make_arrivals(rng)
    weights = day_origin_weights(arrivals)
    tickets = make_tickets(rng, weights)
    complaints = make_complaints(rng, tickets)
    occupancy = make_occupancy(rng, tickets)
    stays, stays_clean, issues = make_stays(rng, weights)
    survey, survey_truth = make_survey(rng, weights)

    write_csv(arrivals, DATA / "arrivals.csv")
    write_csv(tickets, DATA / "tickets.csv.gz")
    write_csv(complaints, DATA / "complaints.csv")
    write_csv(occupancy, DATA / "occupancy.csv.gz")
    write_csv(stays, DATA / "stays.csv.gz")
    write_csv(survey, DATA / "survey.csv")
    (DATA / "brief.md").write_text(BRIEF, encoding="utf-8", newline="\n")
    write_json(DICTIONARY, DATA / "data_dictionary.json")
    write_json(PAST_FINDINGS, DATA / "past_findings.json")
    write_json(LABELS, DATA / "labels.json")
    write_json({"min_complaints": PUBLISH_MIN_COMPLAINTS, "min_visitors": PUBLISH_MIN_VISITORS,
                "rule": "The board's own publication rule: a cell with fewer than 10 complaints or fewer than 1,000 visitors is not published."},
               DATA / "publication_rule.json")
    h = survey_truth["headline_cell"]
    write_json({"weekend_claim": "Weekend visitors are more satisfied than weekday visitors.",
                "headline": f"At the {h['site']}, weekend visitors were far more satisfied than weekday visitors in {h['year']}.",
                "headline_site": h["site"], "headline_year": h["year"],
                "how_found": "Nayef Al-Jumaah compared weekend and weekday satisfaction at each of the nine sites in each of the three years and kept the largest gap."},
               DATA / "claims.json")

    visitors = tickets.groupby("site")["tickets"].sum()
    truth = {"seed": SEED, "festivals": {k: v[0] for k, v in FESTIVALS.items()}, "stays_issues": issues,
             "stays_clean_rows": len(stays_clean), "survey": survey_truth, "satisfaction_2024": SAT_2024, "satisfaction_shift": SAT_SHIFT,
             "survey_mix": SURVEY_MIX, "complaint_rate_multiplier": {s[1]: s[4] for s in SITES},
             "visitors_by_site": {k: int(v) for k, v in visitors.items()}, "complaints": len(complaints), "past_findings_key": PAST_KEY}
    write_json(truth, LABS / "solutions" / "truth.json")

    for i, (name, c) in enumerate(CAPSTONE.items()):
        write_csv(capstone_set(SEED * 10 + i, c["units"], c["groups"], c["cols"], c["event_month"]), CAP / f"{name}.csv")
    write_json({name: {"organisation": c["organisation"], "audience": c["audience"], "file": f"data/{name}.csv",
                       "unit": c["meaning"][c["cols"]["id"]].replace("pseudonymised key of ", ""), "columns": c["meaning"]}
                for name, c in CAPSTONE.items()}, LABS / "capstone" / "datasets.json")
    print("arrivals", len(arrivals), "tickets", len(tickets), "complaints", len(complaints), "occupancy", len(occupancy),
          "stays", len(stays), "survey", len(survey))
    print(json.dumps(survey_truth, indent=1))


if __name__ == "__main__":
    main()
