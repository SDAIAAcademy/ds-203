---
course: "Exploratory Analysis and Visualisation"
code: "DS-203"
version: "2027.2.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-203/slides/day2.html"
---

# Exploratory Analysis and Visualisation

## Day 2: Relationships and time

Two variables together, counts against rates, change over time, and a total that says the opposite of its parts

#### [day2#title] Relationships and time

*SDAIA Academy · Exploratory Analysis and Visualisation*

Day 2: Two variables together, counts against rates, change over time, and a total that says the opposite of its parts

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-203

#### [day2#agenda] Relationships and time

*Today*

- **Session 1 · Two variables at once**: Scatter plots when there are tens of thousands of points: transparency, binning, and one number that depends on the unit
- **Session 2 · Counts, rates and denominators**: Why a count ranks by size, how to choose a denominator, and which cells are too small to publish
- **Session 3 · Change over time**: Reading a time series as trend, season and events, and choosing what to compare a month with
- **Session 4 · When the total reverses**: Totals are weighted averages: how a change of mix reverses a comparison, and which answer serves which question

#### [day2#review-day-1] Which summary would you send the director?

*Review · Day 1*

**Question:** Spend per stay has a mean of 2,736 riyals and a median of 1,498. It is missing for 22% of day visits and 2% of overnight stays. Which sentence is honest?

- A. A typical party spends about 2,700 riyals in the region
- B. Half of the parties that reported spend spent under 1,500 riyals; day visits are under-reported
- C. Spend is about 1,500 riyals once missing values are filled in
- D. Spend cannot be summarised until the largest stays are removed

### Session 1: Two variables at once

#### [day2#s1] Two variables at once

*Session 1*

- Bring two tables to one unit of observation before relating them
- Reveal a relation in an overplotted scatter with transparency and binning
- Explain why a correlation changes with the unit it is computed on

#### [day2#one-unit-first] Two tables relate only at one unit of observation

*Before two variables can meet*

1. **tickets** 150,000 sales, summed to tickets per day
2. **occupancy** 43,840 hotel-days, rooms sold over rooms
3. **one table** 43,840 rows: a hotel, a day, its occupancy, the day's tickets

- Bring each table to the unit of the answer, then join.
- **Count the rows before and after.** More rows: something was repeated. Fewer: something was dropped.
- The day's ticket total is repeated on 40 hotels. That is intended, and it has a consequence you will see.

#### [day2#overplotting] 43,840 opaque points draw a block, not a relation

*The first attempt*

Figure: Every point is there. Nothing can be read.

- A scatter plot shows each unit as a point. Past a few thousand, points hide points.
- The block says only where data exists: 152 to 836 tickets a day, 0 to 100% of rooms.
- **Overplotting** hides density, and density is the message.

#### [day2#transparency] Transparency turns overlap into darkness

*Repair 1 · Lab 2.1, step 2*

Figure: The same points at opacity 0.04.

- A dark band now rises from left to right.
- The horizontal stripes are **banding**: a hotel of 8 rooms can only be 0, 1/8, 2/8 … full, nine possible values.
- Banding is a feature of the unit, not of tourism. Name it so that nobody explains it.

```python
alt.Chart(hd).mark_circle(size=8, opacity=0.04).encode(x="tickets_day:Q", y="rate:Q")
```

#### [day2#binned-heatmap] Bin both axes and colour by count

*Repair 2 · Lab 2.1, step 3*

Figure: A histogram in two dimensions.

- Each cell counts the hotel-days that fall in it. The count goes to colour.
- It works for a million points as well as for forty thousand.
- It shows **where** the points are. It does not yet say **how much** occupancy rises.

#### [day2#binned-medians] To read "how much", summarise y inside bins of x

*Repair 3 · Lab 2.1, step 4*

Figure: Eight groups of days, equal in size, by tickets sold.

- Cut the days into eighths by tickets sold; take the median occupancy of each.
- Quietest eighth: **40%** of rooms sold. Busiest eighth: **77%**.
- The y axis runs from 0 to 100%, so the rise is drawn at its true size.

#### [day2#correlation-and-unit] One relation, two units, two correlations

*Lab 2.1, step 5*

- **0.39** across 43,840 hotel-days
- **0.70** across 156 weeks, all hotels together

- Adding up 40 hotels and 7 days averages away what is particular to one hotel on one night.
- Weeks answer: does the region's occupancy move with the sites?
- Hotel-days answer: can one hotel's night be told from the day's ticket sales?

> **There is no "the correlation".** Report the coefficient with its unit and its number of units.

#### [day2#what-a-relation-does-not-say] A relation between two series is not yet a reason

*The second sentence of the reading*

- Summer raises ticket sales. Summer raises hotel bookings.
- Festivals do the same, in October and February.
- Two series that share a calendar move together whether or not one feeds the other.

- **What the reading may say.** "Weeks with more ticket sales are weeks with fuller hotels (0.70 across 156 weeks). Both rise in summer and at festivals, so the data does not show that site visits fill hotels."

#### [day2#check-two-variables] Which picture, and which number?

*Checkpoint*

**Question:** A transport authority has 2 million trips, each with distance and fare. An analyst wants to show how fare rises with distance. What should the first chart be?

- A. A scatter plot of every trip, so that no trip is left out
- B. A scatter plot of 200 trips picked at random from the file
- C. The correlation of fare and distance, printed as one figure
- D. A binned heatmap of the trips, then the median fare by distance band

#### [day2#lab-2-1] Occupancy against ticket sales

Lab 2.1 · 25 min

Plot hotel occupancy against ticket sales for 43,840 hotel-days, first as a solid block, then with transparency, a binned heatmap and binned medians.

[D2_1_occupancy_tickets.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D2_1_occupancy_tickets.ipynb)

- [ ] Join hotel-days to daily ticket sales (4 min)
- [ ] A scatter with transparency (5 min)
- [ ] Bin both axes: a heatmap of counts (6 min)
- [ ] Median occupancy by level of ticket sales (5 min)
- [ ] One number at two units: hotel-days and weeks (3 min)
- [ ] Write the reading (2 min)
- [ ] ✱ Stretch: Colour the binned medians by weekend and weekday

### Session 2: Counts, rates and denominators

#### [day2#s2] Counts, rates and denominators

*Session 2*

- Convert counts to rates with a denominator that fits the question
- Compare a ranking by count with a ranking by rate
- Colour a map by a rate on its exposure, not by a count
- Mark the cells of a table that a publication rule holds back

#### [day2#counts-rank-size] A ranking by count is mostly a ranking by size

*Ask 3 of the brief*

| Site | Complaints | Visitors |
| --- | --- | --- |
| Cable Car | 599 | 100,822 |
| Souq Walk | 394 | 77,599 |
| Tilal Fort | 296 | 53,558 |
| Wadi Trail | 243 | 21,408 |
| Terrace Farms | 167 | 12,083 |

- "A lot of complaints about the Cable Car": 599 of 2,418, a quarter of the log.
- It also receives a quarter of all visitors.
- The count answers "where is the workload?". It does not answer "where does a visit go wrong most often?".

#### [day2#choose-a-denominator] The denominator is whoever could have produced the event

*The choice that decides the answer*

| Question | Rate | Denominator |
| --- | --- | --- |
| Where does a visit go wrong most often? | complaints per thousand visitors | tickets sold at the site |
| Which market complains most readily? | complaints per thousand visitors of that origin | tickets sold to that origin |
| Is the queue the issue on busy days? | queue complaints per thousand visitors, by day | tickets sold that day |

- Per thousand, so that the reader sees numbers like 5.9, not 0.0059.
- A rate travels with its two parts: **599 of 100,822**.

#### [day2#aggregate-then-join] Bring each table to the unit of the answer, then join

*Lab 2.2, step 2*

```sql
-- file: DuckDB
WITH c AS (SELECT site, count(*)     AS complaints FROM complaints GROUP BY site),
     v AS (SELECT site, sum(tickets) AS visitors   FROM tickets    GROUP BY site)
SELECT site, complaints, visitors,
       1000.0 * complaints / visitors AS per_thousand
FROM c JOIN v USING (site)
ORDER BY per_thousand DESC
```

- Nine rows in, nine rows out. The totals still read 2,418 complaints and all tickets sold.
- Joining the raw tables on `site` pairs every complaint with every sale: millions of rows and a rate that means nothing.

#### [day2#two-rankings] By rate, the Cable Car is fifth and the smallest site is first

*Lab 2.2, step 3*

Figure: Complaints per thousand visitors, 2023 to 2025.

- Cable Car: first by count, **fifth** by rate (5.9).
- Terrace Farms: seventh by count, **first** by rate (13.8), on 167 complaints.
- Wadi Trail is high on both readings of "problem": fourth by count (243), second by rate (11.4).

#### [day2#map-of-counts] A map coloured by count shows where the visitors are

*The same fault on a map*

Figure: A neighbouring region, nine districts as equal tiles. Synthetic data.

- A **choropleth** colours each area by one number.
- Central holds 261 of 714 call-outs (37%) and 43% of the visitor-days.
- Across the nine districts, call-outs and visitor-days correlate at **0.98**. The left map repeats the right one.

#### [day2#map-of-rates] Colour the rate on the exposure, not the count

*Divide, then colour*

Figure: Call-outs per 100,000 visitor-days, 2025. Synthetic data.

- The base is whoever could have needed a call-out: visitor-days, not residents or square kilometres.
- Central: first by count, **seventh of eight** by rate (32).
- North-West: sixth by count, **first** by rate: 63 calls on 45,000 visitor-days, 140.
- South-East: 6 calls; one more moves its rate by a sixth. Grey, with its count.

#### [day2#small-cells] Cut finer and some of the highest rates rest on the fewest cases

*Lab 2.2, steps 4 and 5*

| Site × origin | Complaints | Visitors | Published |
| --- | --- | --- | --- |
| Terrace Farms × Asia | 6 | 441 | withheld |
| Terrace Farms × Europe | 4 | 321 | withheld |
| Cloud Lookout × Asia | 6 | 1,769 | withheld |
| Honey Museum × Asia | 8 | 2,075 | withheld |

- The board's rule: publish a cell only with at least **10 complaints and 1,000 visitors**.
- Four of 45 cells are held back. Two of them, above 12 per thousand on 6 and 4 complaints, would have been among the four highest rates in the table.
- One more complaint moves a rate built on 4 by a quarter.

#### [day2#withheld-is-not-hidden] A withheld cell beside a published total can be recovered

*The stretch of lab 2.2*

- **By subtraction.** Honey Museum: 139 complaints in total, four origin cells published, one withheld. The fifth is 139 minus the four: 8.
- **What the analyst does.**
  - marks every cell that fails the rule
  - checks each row and column for a single withheld cell
  - hands the table to the person who owns the rule

> **Where this continues.** Second-cell suppression, differencing between releases and the classification of outputs are taught in DS-207. Here you learn to see the problem and to mark the cells.

#### [day2#check-rates] Which sentence can be printed?

*Checkpoint*

**Question:** A city logs 420 pothole reports in District A (300 km of road) and 150 in District B (60 km of road). The mayor asks where the roads are worse. What do you report?

- A. District B: 2.5 reports per km of road against 1.4 in District A
- B. District A: it has almost three times as many reports as B
- C. Both: the city has 570 reports on 360 km, or 1.6 per km
- D. Neither: reports per resident are needed before any answer

#### [day2#lab-2-2] Complaint rates and small cells

Lab 2.2 · 25 min

Convert complaints to rates per thousand visitors by site and by origin, compare the two rankings and mark the cells too small to publish.

[D2_2_complaint_rates.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D2_2_complaint_rates.ipynb)

- [ ] Count complaints by site and rank the sites (3 min)
- [ ] Visitors by site, and complaints per thousand visitors (6 min)
- [ ] Set the two rankings side by side (3 min)
- [ ] Rates by site and origin (5 min)
- [ ] Apply the publication rule (5 min)
- [ ] Write the reading (3 min)
- [ ] ✱ Stretch: Show that one withheld cell can be recovered from the row total

### Session 3: Change over time

#### [day2#s3] Change over time

*Session 3*

- Draw a time series so that season and trend can be told apart
- Compare a month with the same month a year earlier and with a seasonal baseline
- Mark the months that exceed the baseline and say by how much

#### [day2#trend-season-event] A monthly line holds three things at once

*Reading a time series*

Figure: Arrivals per month, all origin markets.

- **Trend:** each summer peak is higher than the last.
- **Season:** the same shape every year, highest in July.
- **Events:** three spikes that are not in summer.

> **Draw it this way.** Time on x, left to right, evenly spaced; a line for a continuous series; the y axis from zero when sizes are compared.

#### [day2#seasonal-profile] A seasonal index says how a month compares with an average month

*Lab 2.3, step 2*

- **1.43** July: 43% above an average month
- **0.78** January: 22% below

- Divide each month of 2023 by the mean of its twelve months.
- Twelve numbers with a mean of 1.
- 2023 had no festival, so its shape is the season alone.

> **What goes wrong.** "Arrivals rose 30% from May to July" describes the calendar. It happens every year.

#### [day2#year-on-year] The same month a year earlier removes the season, and hides what repeats

*Lab 2.3, step 3*

| Month | Festival | Change on a year earlier |
| --- | --- | --- |
| October 2024 | Honey Festival, first edition | +37% |
| February 2025 | Heritage Nights, first edition | +27% |
| October 2025 | Honey Festival, second edition | +7% |

- A typical month grew **6.9%** on the year before.
- October 2025 looks ordinary because it is compared with October 2024, which had the same festival.

#### [day2#seasonal-baseline] A baseline is what the month would have been: season times trend

*Lab 2.3, step 4*

Figure: Actual arrivals and the baseline, dashed.

- Baseline: the same month of 2023, grown by the typical yearly growth.
- October 2024: **+29%**. February 2025: **+18%**. October 2025: **+29%**.
- Every other month sits within 5% of the baseline.

#### [day2#what-a-baseline-is] A baseline is a choice, and the excess inherits it

*What the reading must carry*

- **It rests on one year.** 2023 is the only year without a festival. A wet July in 2023 would sit in every later baseline.
- **It assumes steady growth.** One growth figure for every month and every market. Session 4 shows the markets grew at different speeds.
- **It does not name a cause.** "29% above the baseline in the festival month" is what the data shows. A school holiday in the same month would look the same.

> **In the report.** State the baseline in one line under the chart, and give the excess as a percentage and as arrivals.

#### [day2#check-time] Compared with what?

*Checkpoint*

**Question:** A library ran a reading campaign in March 2025. Loans were 9,000 in February 2025, 11,500 in March 2025 and 11,000 in March 2024. Loans grew 3% a year before the campaign. Which statement is supported?

- A. The campaign raised loans by 28%, from 9,000 to 11,500
- B. Loans stood 4.5% above the level expected without a campaign
- C. Loans stood about 1.5% above a baseline of 11,330 for March 2025
- D. The campaign failed, since loans rose less than in a normal year

#### [day2#lab-2-3] Monthly arrivals, season and festivals

Lab 2.3 · 25 min

Plot monthly arrivals, separate the summer season from the trend and mark the two festival effects against a seasonal baseline.

[D2_3_monthly_arrivals.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D2_3_monthly_arrivals.ipynb)

- [ ] A line chart of monthly arrivals (4 min)
- [ ] The seasonal profile of a festival-free year (5 min)
- [ ] Change on the same month a year earlier (5 min)
- [ ] A baseline from season and trend; the months above it (7 min)
- [ ] Mark the festival months and write the reading (4 min)
- [ ] ✱ Stretch: Repeat the baseline for one origin market

### Session 4: When the total reverses

#### [day2#s4] When the total reverses

*Session 4*

- Split a total into what each group does and how large each group is
- Detect a reversal between a total and its groups
- Report a comparison at a fixed mix

#### [day2#two-true-tables] Satisfaction fell overall and rose in every market

*Ask 5 of the brief*

| All respondents | 2024 | 2025 |
| --- | --- | --- |
| Mean satisfaction | 4.15 | 4.07 |

| Origin market | 2024 | 2025 |
| --- | --- | --- |
| Tilal region | 4.50 | 4.60 |
| Other regions | 4.20 | 4.30 |
| Gulf | 3.70 | 3.80 |
| Asia | 3.41 | 3.49 |
| Europe | 3.30 | 3.41 |

> **Both tables are right.** They come from the same 4,200 responses, and nobody made an arithmetic error.

#### [day2#weighted-average] A total is a weighted average: the weights are the mix

*The mechanism*

```text
# file: what the overall mean is
overall mean  =  sum over groups of ( share of the group  ×  mean of the group )

2024:  0.40 × 4.50  +  0.35 × 4.20  +  0.12 × 3.70  +  0.07 × 3.41  +  0.06 × 3.30   =  4.15
2025:  0.26 × 4.60  +  0.30 × 4.30  +  0.19 × 3.80  +  0.13 × 3.49  +  0.12 × 3.41   =  4.07
```

- The total moves when the group means move, **or** when the shares move.
- Here the means all rose by about 0.1 and the shares moved against them.

#### [day2#the-mix-changed] The markets that score lowest grew from a quarter of the responses to almost half

*Lab 2.4, step 3*

| Item | Value |
| --- | --- |
| Tilal region | 40% → 26% |
| Other regions | 35% → 30% |
| Gulf | 12% → 19% |
| Asia | 7% → 13% |
| Europe | 6% → 12% |

Bars: share of survey responses in 2025. Values: 2024 → 2025.

- International visitors rate lower in both years, and there are far more of them in 2025.
- That is the board's own strategy working: Day 3 shows international arrivals up 42% to 67% since 2023.

#### [day2#reversal-chart] One chart can hold the parts and the total

*Lab 2.4, step 5*

Figure: Mean satisfaction, 1 to 5. Each line is labelled at its end.

- Five lines up, one line down: the reader sees the reversal before reading a word.
- The total differs from the parts in colour **and** in line style.
- The axis starts at 3.0. For positions on a 1 to 5 scale that is fair; for bars it would not be.

#### [day2#fixed-mix] Hold the mix fixed, and the comparison answers one question

*Lab 2.4, step 4*

- **4.15** 2024, as surveyed
- **4.07** 2025, as surveyed
- **4.25** 2025 means at the 2024 mix

```python
at_2024_mix = (mean_2025_by_origin * share_2024_by_origin).sum()   # 4.25
```

- With last year's mix of visitors, this year would have scored **up 0.10**, not down 0.08.
- Say which mix was used. Another reference mix gives another figure, with the same direction here.

#### [day2#which-answer] The total and the fixed-mix figure answer different questions

*Neither number is "the right one"*

| Question | Figure | Answer |
| --- | --- | --- |
| How satisfied was the average respondent this year? | the total | 4.07, down 0.08 |
| Did the experience of comparable visitors improve? | by market, or at a fixed mix | up about 0.10 in every market |
| Why did the total fall? | the change of mix | more visitors from markets that rate lower |

> **When to suspect a reversal.** Groups differ in level, and their shares changed between the things you compare. Check the mix before explaining any change in a total.

#### [day2#check-reversal] What do you check first?

*Checkpoint*

**Question:** A centre's pass rate fell from 82% to 76%. Evening courses always pass less often than day courses, and evening enrolment doubled. What comes before writing "teaching quality fell"?

- A. Wait for one more year of results so that the fall is certain
- B. Compare pass rates inside day and evening courses, and the shares of each
- C. Recompute the pass rate for day courses only and report that figure
- D. Weight the pass rate by enrolment so that large courses count for more

#### [day2#lab-2-4] The satisfaction reversal

Lab 2.4 · 25 min

Find the satisfaction reversal once visitor origin is taken into account: down overall from 2024 to 2025, up in every origin market.

[D2_4_satisfaction_reversal.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D2_4_satisfaction_reversal.ipynb)

- [ ] Mean satisfaction by year (3 min)
- [ ] Mean satisfaction by origin and year (5 min)
- [ ] The mix of respondents by year (4 min)
- [ ] 2025 at the 2024 mix (6 min)
- [ ] One chart of the reversal (4 min)
- [ ] Write the sentence the board may print (3 min)
- [ ] ✱ Stretch: Find a second variable that could move the total the same way

#### [day2#wrap-up] A number depends on what it is set against

*Day 2*

- **Its unit.** 0.39 by hotel-day, 0.70 by week. Say which.
- **Its denominator.** First by count, fifth by rate. Print both parts.
- **Its baseline.** +7% on last year, +29% on the season. State the baseline.
- **Its mix.** Down overall, up in every market. Check the shares.

#### [day2#next] Building honest charts

*Day 3*

A chart as a specification, small multiples, six misleading charts to repair, and one chart in Arabic and English.

- Tonight, look at one chart in a report you receive at work and ask where its y axis starts.
- Every lab of Day 3 starts from the supplied tables.
