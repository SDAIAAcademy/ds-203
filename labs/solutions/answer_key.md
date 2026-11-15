# Answer key · what is planted in the data and which lab finds it

For trainers. Every number here comes from a run of the solution notebooks on the data generated with seed 203. `truth.json` in this folder holds the generator's own record.

## Day 1

| Lab | Planted | Expected result |
|---|---|---|
| 1.1 | Five asks in `brief.md`, none answerable as written | A plan of five questions, each with table, unit, variables, comparison and kind, that passes `U.plan_check`. Ask 3 needs `tickets` as a second table. All five are exploratory |
| 1.2 | Rows entered twice | 40,600 rows, 40,000 distinct stays, 600 duplicates |
| 1.2 | A code posing as a number | 320 stays with `nights` = 999; mean nights 11.27 with them, 3.30 without |
| 1.2 | One market under three spellings | 586 rows: `GCC` 405, `gulf ` (with a trailing space) 181 |
| 1.2 | Spend missing, not at random | 2,577 missing: 21.7% of day visits, 2.1% of overnight stays |
| 1.2 | Impossible dates | 14 arrival dates in 2032 |
| 1.3 | Two humps hidden by a box plot | "Other regions": a hump at 2 nights and one at 6 to 7, nothing at 4. 80% of Tilal-region parties are day visits; Europe's median is 7 nights |
| 1.4 | Four shapes | Spend: mean 2,736, median 1,498, quartiles 571 and 3,392, geometric mean 1,344. Booking lead: 36% zero, median 14 days among the rest. Satisfaction: 77% score 4 or 5 |

## Day 2

| Lab | Planted | Expected result |
|---|---|---|
| 2.1 | A relation hidden by overplotting; banding from small hotels | Median occupancy from 40% in the quietest eighth of days to 77% in the busiest. Correlation 0.39 across hotel-days, 0.70 across 156 weeks |
| 2.2 | The busiest site leads the count | Cable Car: 599 complaints, first by count, fifth by rate (5.94 per thousand). Terrace Farms: 167 complaints, first by rate (13.82). Wadi Trail 11.35 |
| 2.2 | Small cells | Four of 45 site-by-origin cells fail the rule (10 complaints and 1,000 visitors): Terrace Farms × Asia (6 of 441), Terrace Farms × Europe (4 of 321), Cloud Lookout × Asia (6 of 1,769), Honey Museum × Asia (8 of 2,075) |
| 2.3 | Season, trend and three festival months | Seasonal index: July 1.43, January 0.78. Median growth on a year earlier 6.9%. Year on year: October 2024 +37%, February 2025 +27%, October 2025 +7%. Against the baseline: +28.6%, +18.4%, +28.8%; every other month within 5% |
| 2.4 | A reversal by mix | 4.15 in 2024, 4.07 in 2025; up about 0.10 in each of the five markets. Respondent mix 40/35/12/7/6% in 2024, 26/30/19/13/12% in 2025. 2025 at the 2024 mix: 4.25 |

## Day 3

| Lab | Planted | Expected result |
|---|---|---|
| 3.1 | none: a specification to follow | Rule, circle and text layers; rate on x from zero, sites sorted by rate, visitors on size. As bars, the size channel is lost |
| 3.2 | A winter market invisible on a shared scale | Peak month: Europe 12, Asia 8, the other three 7. Peak to trough: Gulf 4.13, Europe 2.41, Other regions 2.02, Tilal region 1.41, Asia 1.37. Shared scale for levels, free scales for shapes |
| 3.3 | Six charts, one fault each | 1 cut baseline · 2 picked window · 3 count for rate · 4 two axes · 5 running total · 6 uneven steps. Local arrivals fall from 258,197 (2023) to 241,911 (2025) under the "keeps climbing" chart |
| 3.4 | A palette that fails red-green deficiency; labels in one language | Draft palette: closest pair 7.3 (deuteranopia). Okabe-Ito first five: at least 18.1. Index 2025 (2023 = 100): Asia 167, Europe 157, Gulf 142, Other regions 117, Tilal region 94 |

## Day 4

| Lab | Planted | Expected result |
|---|---|---|
| 4.1 | A weekend gap that is noise | Gap +0.021 (2,478 weekend, 3,522 weekday responses), permutation p about 0.35: **drop** |
| 4.1 | A correlation that is real and seasonal | 0.70, bootstrap interval about 0.60 to 0.78 over 156 weeks: **qualify** ("report" is accepted if the reading carries the qualifier). With month-of-year means removed: 0.44, interval 0.31 to 0.56 |
| 4.2 | A top-ranked site on few responses | Terrace Farms 4.24 on 59 responses, interval 4.02 to 4.44; seven of the other eight intervals overlap it. Guided minus unguided in 2025: +0.39, interval +0.31 to +0.47: **report** |
| 4.3 | A headline chosen from 27 comparisons | Honey Museum 2025: gap +0.30, 68 weekend and 99 weekday responses, p about 0.03 alone, 2.2 standard errors, the only one of 27 beyond 2. Chance of at least one p below 0.05 among 27: 75%. A gap as striking somewhere among 27: about 0.55 of shuffles |
| 4.3 | Five past findings | F1 confirmed · F2 exploratory · F3 confirmed · F4 exploratory · F5 exploratory |
| 4.4 | A report with no seed | Two renders differ in the ends of the bootstrap interval only |
| 4.4 | A stale cache | Cache: 40,600 stays, 5,553 Gulf stays, mean 11.27 nights. From the raw data: 40,000, 6,063, 3.30 |
| 4.4 | Two flaws in the findings table | Row 3 has no limit; row 4 (Honey Museum) is marked "confirmed" without a plan |

The weekend pattern at the Honey Museum is chance by construction: the generator gives no site a weekend effect and searches seeds until the smallest of the 27 p-values lies between 0.01 and 0.03 and the next one is above 0.06.

## The capstone datasets

Each of the three files in `capstone/data/` has 12,150 rows (12,000 events and 150 rows entered twice), 240 missing values in its skewed measure, a season, one event month (Ruwaq: March 2025; Awan: November 2024; Miqdam: June 2025), a rating that rises inside each of four groups from 2024 to 2025 while the mix of groups shifts towards the lower-rated ones, and no weekday effect. A participant who finds a weekday pattern has found chance.
