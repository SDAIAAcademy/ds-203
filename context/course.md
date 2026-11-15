---
course: "Exploratory Analysis and Visualisation"
code: "DS-203"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-203/"
---

# Exploratory Analysis and Visualisation

Answer a director's questions from her own data: written questions first, charts that do not mislead, patterns checked against chance, and a report that reruns from raw data

Participants answer a fictional regional tourism board's questions by exploring its data, starting every analysis from written questions. They profile tables, examine distributions, relationships and change over time, build charts with a grammar of graphics and scales that do not mislead, and test by resampling whether a pattern could be chance. They repair misleading charts and write findings that state what is and is not shown, in a notebook that reruns from raw data.

- **Audience:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.
- **Prerequisites:** FN-101 Python for Data and AI Work; FN-104 SQL and Data Wrangling; DS-201 Statistical Inference by Simulation; Makes a basic chart in any plotting library; Pre-work: about two hours of dataframe and plotting practice, labs/P0_prework_dataframes_plotting.ipynb, before the supervised entry quiz; Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.
- **Case study:** Tilal Regional Tourism Board: Tilal Regional Tourism Board (مجلس تِلال الإقليمي للسياحة) is a fictional board of a highland region with nine visitor sites. Its director's brief is answered from three years of seeded synthetic data, 2023 to 2025: monthly arrivals by five origin markets, 150,000 ticket sales, 40,000 visitor stays, the daily occupancy of 40 hotels, 6,000 survey responses in Arabic and English and 2,418 complaints. The data holds what the sessions teach: entry errors in the stay register, a summer season, two festivals, a busiest site that is not the worst, satisfaction that falls overall while it rises in every origin market, and patterns that are only chance. Participants work as Leen Al-Suwayigh, the board's analyst; stays and hotels appear under pseudonymised keys and small groups are not published.

## Outcomes

- LO1 (Awareness): Distinguish exploratory from confirmatory analysis and explain why a pattern found by exploring needs a fresh test, given five findings from a past board report
- LO2 (Applied): Prepare an analysis plan listing questions, units of observation, variables and the comparison that answers each, given the director's brief and the data dictionary
- LO3 (Applied): Analyse distributions, relationships and change over time with summaries and charts suited to each variable type, given three years of visitor, occupancy and survey tables
- LO4 (Applied): Use a grammar of graphics to map variables to position, colour and facets with honest scales, baselines and labels, given six misleading charts from earlier reports
- LO5 (Applied): Test whether an apparent difference or correlation could arise by chance, using permutation or bootstrap resampling, given three patterns the board wants to announce
- LO6 (Performance): Deliver a reproducible exploratory report that states findings, uncertainty, open questions and limits for a non-specialist reader, given an unseen dataset and a named audience

## Day 1: Questions and first looks

Before any chart: what is asked, what one row is, what the values look like and which summary describes them

#### [day1#title] Questions and first looks

*SDAIA Academy · Exploratory Analysis and Visualisation*

Day 1: Before any chart: what is asked, what one row is, what the values look like and which summary describes them

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-203

#### [day1#agenda] Questions and first looks

*Today*

- **Session 1 · Write the questions first**: From a brief to questions that name a unit of observation, variables and a comparison, and what exploring can and cannot establish
- **Session 2 · Profiling a table**: What to find out about a table before trusting a single number from it: grain, key, types, missing values, ranges and categories
- **Session 3 · Distributions**: Histograms, density and box plots: what each shows of a distribution and what each hides
- **Session 4 · Summaries that fit the shape**: Choosing a centre and a spread by the shape of the variable: long tails, counts, zero-heavy variables and scores

#### [day1#the-board] Tilal Regional Tourism Board: three years, six tables

*The case study*

- **9** visitor sites in a highland region
- **150,000** ticket sales, 2023 to 2025
- **40,000** visitor stays in the register
- **6,000** survey responses, Arabic and English

You work as **Leen Al-Suwayigh**, the board's analyst. **Nawal Al-Rashoud**, the director, wrote the brief. Aws Al-Hudaif runs sites and ticketing, Rashed Al-Shalan collects the hotels' occupancy returns, Atheer Al-Muhaya owns the survey and the complaints log, Nayef Al-Jumaah drew the charts of last year's report, Hanouf Al-Rumaihi is the data protection officer. The board, its people and every record are fictional and generated with a fixed seed.

#### [day1#how-the-course-works] Question, chart, reading: in that order, every time

*The method of this course*

1. **1 · Ask** a question with a unit and a comparison
2. **2 · Look** with a chart and a summary that fit the variable
3. **3 · Write** two sentences: what it shows, what it does not
4. **4 · Check** could it be chance, and does it rerun

| Part of the course | Assistant |
| --- | --- |
| Supervised quizzes, and the first draft of every chart reading | Off |
| Plotting and dataframe syntax in the labs | A tutor that hints one step at a time and writes no chart for you |
| The capstone | Free; assisted charts and sentences are marked and defended live |

#### [day1#setup-and-data-rules] One notebook proves the setup; three rules govern the data

*Before the first lab*

- **Setup check.** Open `00_setup_check.ipynb` in Colab or locally and run all cells. It imports the libraries, reads the six tables and draws one chart.
  ```text
  uv sync
  uv run jupyter lab
  ```
- **Handled as personal data.** The data is synthetic and is still handled as the board would handle the real thing:
  - stays and hotels appear only under pseudonymised keys
  - no chart singles out one visitor or one hotel
  - small groups are not published, and a rate travels with its denominator

### Session 1: Write the questions first

#### [day1#s1] Write the questions first

*Session 1*

- Rewrite a vague request as a question with a unit, variables and a comparison
- Name the unit of observation of each table before joining or counting
- Distinguish an exploratory question from a confirmatory one

#### [day1#the-brief] Five asks, none of them answerable as written

*What the director sent*

**Nawal Al-Rashoud:** Who is actually coming, and do they stay? I keep hearing that our visitors "pop in and leave".

**Nawal Al-Rashoud:** Atheer's team logged a lot of complaints about the Cable Car. Is that our problem site?

**Nawal Al-Rashoud:** Satisfaction went down last year. Why, and whose fault is it?

> **The trap.** Open the data now and you will chart whatever is easiest to chart, then call it the answer.

#### [day1#anatomy-of-a-question] An answerable question names four things

*The tool of this session*

| Part | It says | Ask 3, rewritten |
| --- | --- | --- |
| **Unit of observation** | what one row is | one complaint; one ticket sale |
| **Variables** | which columns are used | site; tickets in the sale |
| **Comparison** | what is set against what | complaints per thousand visitors, by site |
| **Kind** | exploring, or testing a claim fixed in advance | exploratory |

> **The test.** Could a colleague answer it without phoning you? "How many complaints per thousand visitors does each site receive?" passes. "Is it our problem site?" does not.

#### [day1#unit-of-observation] "Visitors" is a different thing in every table

*What one row is*

| Table | One row is | Rows |
| --- | --- | --- |
| arrivals | one origin market in one month | 180 |
| tickets | one ticket sale at one site | 150,000 |
| stays | one visiting party's stay in the region | 40,000 |
| occupancy | one hotel on one day | 43,840 |
| survey | one visitor's response after a site visit | 6,000 |
| complaints | one complaint | 2,418 |

- Counting rows counts units: 40,000 stays are parties, not people.
- Two tables meet only after both are brought to one unit, such as the week.

#### [day1#exploratory-or-confirmatory] Exploring finds questions; confirming answers one fixed in advance

*Two kinds of work*

- **Exploratory.**
  - You look at the data to see what is there
  - Many cuts, many charts, the choice made after looking
  - Output: patterns worth a question
  - Honest wording: "we saw", "in this data"
- **Confirmatory.**
  - The comparison was written down before the data was seen
  - One planned analysis on data not used to find the pattern
  - Output: evidence for or against a claim
  - Honest wording: "the test planned in advance showed"

> **Why a found pattern needs a fresh test.** The data that suggested a pattern cannot also confirm it: you chose the pattern because it stood out there.

#### [day1#the-plan] The plan is a table, and it passes a checklist

*One page before any chart*

```python
# file: one entry of the plan
{"question": "How many complaints per thousand visitors does each site receive over the three years?",
 "table": "complaints", "also": ["tickets"],
 "unit": "one complaint logged by the visitor experience team",
 "variables": ["site", "tickets"],
 "comparison": "complaints per thousand visitors by site, with the count and the visitors beside it",
 "kind": "exploratory"}
```

- The checklist rejects a question with a word nobody can measure, a unit that is not the table's, fewer than two variables, or no comparison.
- It does not judge whether the question is interesting. That stays with you and the director.

#### [day1#what-the-plan-cannot-do] The plan answers "what happened", not "why"

*A narrower promise*

**Ask 5:** "Satisfaction went down last year. Why, and whose fault is it?"

**Plan:** "Did mean satisfaction change from 2024 to 2025 inside each origin market, and did the mix of markets among respondents change?"

- The data can show where the fall sits.
- It cannot assign a cause: nothing was varied on purpose.
- Say so in the plan, before the director expects more.

#### [day1#check-question] Which rewrite can be answered?

*Checkpoint*

**Question:** The director asks: "Did the festivals bring people, or would they have come anyway?" Which rewrite belongs in the plan?

- A. Were the festivals successful for the region?
- B. How many arrivals were recorded in the festival months?
- C. By how much did arrivals in each festival month exceed the baseline for that month of the year?
- D. Did the festivals cause visitors to choose Tilal over other regions?

#### [day1#lab-1-1] Five questions from the brief

Lab 1.1 · 25 min

Turn the director's brief into five questions, each with its table, unit of observation, variables and comparison, and pass the plan checklist before any chart is drawn.

[D1_1_brief_questions.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D1_1_brief_questions.ipynb)

- [ ] Read the brief; name the table and the unit behind each ask (5 min)
- [ ] Write five questions with variables and comparison (12 min)
- [ ] Run the plan checklist and fix what fails (5 min)
- [ ] Write what the plan leaves out (3 min)
- [ ] ✱ Stretch: Add the question the brief did not ask and should have

### Session 2: Profiling a table

#### [day1#s2] Profiling a table

*Session 2*

- Test whether a table has the grain and the key its dictionary claims
- Locate missing values and impossible values, and say whom they affect
- Record each data issue with its evidence and a decision

#### [day1#profile-before-plot] A profile asks six things of a table

*Before the first chart of a table*

- **1 · Grain and key.** Is one row what the dictionary says? Is the key unique?
- **2 · Types.** Are dates dates and numbers numbers, or text that looks like them?
- **3 · Missing values.** How many, and above all where?
- **4 · Ranges.** Smallest and largest: can they be true?
- **5 · Categories.** How many distinct values, and how spelled?
- **6 · Coverage.** Which period and which groups does the table hold?

#### [day1#summarize-statement] One statement profiles every column

*Lab 1.2, opening cell*

```text
      column_name column_type        min         max  approx_unique  null_percentage
          stay_id     VARCHAR  T0002344e   Tfffb8d8e          39407             0.00
     arrival_date     VARCHAR 2023-01-01  2032-10-25           1137             0.00
           origin     VARCHAR       Asia       gulf               7             0.00
           nights      BIGINT          0         999             28             0.00
        spend_sar      DOUBLE       14.0     76181.0           8565             6.45
```

- Four of the planted issues are visible in these five lines. Find them before the next slide.
- `SUMMARIZE` is DuckDB's; `df.describe(include="all")` gives a similar table in pandas.

#### [day1#grain-and-key] 40,600 rows hold 40,000 stays

*Lab 1.2, step 1*

- **40,600** rows in the export
- **40,000** distinct stay keys
- **600** rows that repeat an earlier row in every column

- Every repeated key is an exact copy: a double entry, safe to drop.
- Had the copies differed in any column, the repair would be the owner's decision, not yours.
- Left in, the copies make every count 1.5% too high and nothing looks wrong.

#### [day1#where-missing-sits] The share of missing values matters less than where they sit

*Lab 1.2, step 2*

| Item | Value |
| --- | --- |
| Day visits | 21.7% without spend |
| Overnight stays | 2.1% without spend |

- Overall, spend is missing in 2,577 of 40,000 stays: 6.4%, which sounds harmless.
- Day visitors spend least and answer least. An average over the rows that remain leans toward overnight visitors.
- The decision: keep the rows, report the share missing by group, never fill in a typical value.

#### [day1#impossible-values] A code that poses as a number moves every summary

*Lab 1.2, step 3*

- **11.26** mean nights with the 320 rows of 999 left in
- **3.30** mean nights without them

- 999 means "not recorded". It is in 0.8% of the rows and more than triples the mean.
- One market is stored as `Gulf`, `GCC` and `gulf ` with a trailing space: 586 stays would fall out of any group-by.
- 14 stays arrive in 2032.

> **Look at the smallest and the largest value of every column**, and at every distinct value of a category with few of them.

#### [day1#issue-log] An issue log holds evidence and a decision someone can dispute

*The output of a profile*

| Issue | Rows | Decision |
| --- | --- | --- |
| Rows that repeat an earlier row in every column | 600 | drop the copies |
| Nights is 999 where the length was not recorded | 320 | set to missing |
| The Gulf market under three spellings | 586 | recode to one spelling |
| Spend missing, mostly for day visits | 2,577 | keep and report the share |
| Arrival dates in 2032 | 14 | set to missing; ask the owner |

The log travels with every chart made from the table. The supplied clean register, `U.stays()`, applies exactly these decisions, and every later lab starts from it.

#### [day1#check-profile] What do you do with the 999s?

*Checkpoint*

**Question:** 320 stays have 999 in the column nights. The data dictionary does not mention the value. What goes into the issue log?

- A. Set them to missing, record the 320 rows, and ask the register's owner what 999 stands for
- B. Replace them with the median length of stay so that no row is lost
- C. Keep them: a few very long stays are plausible in a tourism region
- D. Delete the 320 rows from the register before any analysis

#### [day1#lab-1-2] Profile the stay register

Lab 1.2 · 25 min

Profile the visitor table, find rows entered twice, a code that poses as a number, one market under three spellings and spend that is missing for day visitors, and log three issues with evidence and a decision.

[D1_2_profile_stays.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D1_2_profile_stays.ipynb)

- [ ] Shape, grain and key: is one row one stay? (5 min)
- [ ] Types and missing values: where spend is missing (6 min)
- [ ] Ranges and categories: values that cannot be true (6 min)
- [ ] Log three issues with evidence and a decision (6 min)
- [ ] Write the reading (2 min)
- [ ] ✱ Stretch: Find the fifth issue, in the dates

### Session 3: Distributions

#### [day1#s3] Distributions

*Session 3*

- Draw a histogram with a bin width that suits the variable
- Compare groups of unequal size by shares on a common scale
- Recognise a distribution with two humps that a box plot hides

#### [day1#what-a-distribution-is] A distribution answers "which values, how often"

*One variable at a time*

Figure: Lab 1.3, step 1: nights in the region, all parties, one bin per night.

- Read four things: where the bulk is, how wide, how many humps, how long the tail.
- Here: a spike at 0, a hump at 2, a low hump near 7, a tail to 31.
- Three humps in one histogram usually mean three kinds of unit mixed together.

#### [day1#bin-width] The bin width decides what a histogram can show

*The one choice a histogram has*

- **Too wide.** Bins of 7 nights put 13,205 of the 17,367 stays from other regions into the first bar. Two humps become one.
- **Fitted to the variable.** Nights is a count: one bin per night. Spend spans three orders of magnitude: equal steps on a log scale.
- **Too narrow.** Bins of 10 riyals of spend leave a handful of stays in each bar: the shape drowns in noise.

> **Try two or three widths** and keep the one where the shape stops changing. Say the width in the axis title or the caption.

#### [day1#shares-not-counts] To compare groups of unequal size, compare shares

*Lab 1.3, step 2*

Figure: Five histograms of nights, one per origin market, as shares on a common scale: Tilal region 80% at zero nights; Other regions with a hump at 2 nights and another at 6 to 7; Gulf and Asia with one hump at 3 to 4; Europe spread from 2 to more than 20 nights

- Counts would show the size of each market, not its shape.
- 80% of parties from the Tilal region are day visits; none from Europe.
- "Other regions" has two humps with nothing at 4 nights.

#### [day1#box-plot] A box plot draws five numbers and takes one line per group

*Lab 1.3, step 3*

Figure: The same stays as the five histograms.

- Box: first quartile, median, third quartile. Whiskers: the rest, short of far points.
- Good for many groups and for comparing middles and spreads.
- "Other regions" and "Asia" look alike here: medians 3 and 4, boxes 2 to 6 and 2 to 5.

#### [day1#what-the-box-hides] The box cannot show two humps

*Lab 1.3, step 4*

| Nights, "Other regions" | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Share of stays | 15% | 31% | 16% | 0% | 4% | 10% | 10% | 7% | 4% |

- 63% of these stays last 1 to 3 nights and 37% last 5 or more. None lasts 4.
- The median, 3 nights, belongs to the short trips only. The box, 2 to 6, runs straight across the valley.
- The box plot is not wrong. It was asked "what kinds of trip are there" and answers "where is the middle half".

#### [day1#density-and-small-groups] Smooth curves and small groups both invent detail

*Two cautions*

- **Density curves.** A density plot is a smoothed histogram with a bandwidth in place of a bin width. It overlays well, and it draws mass where no value can be: below zero nights, between whole nights. For counts and scores, prefer bars.
- **Small groups.** A histogram of 40 values has bumps that mean nothing. Read a group's size before its shape: Europe has 2,166 stays here, one site in one month may have a dozen.

> **Responsible use.** A point drawn for one extreme party can single out an identifiable visitor. Show far points only where a group is large, or summarise them.

#### [day1#check-distribution] Which chart for which question?

*Checkpoint*

**Question:** Aws Al-Hudaif asks whether visitors from other regions come for one kind of trip or several. You have their 17,367 stays with the nights of each. What do you draw first?

- A. A box plot of nights for that market
- B. A bar with the mean number of nights and an error bar
- C. A histogram of nights with bins seven nights wide
- D. A histogram of nights with one bin for each night

#### [day1#lab-1-3] Length of stay by origin

Lab 1.3 · 25 min

Compare length of stay by visitor origin with histograms and box plots, and find the market whose box plot hides two kinds of trip.

[D1_3_length_of_stay.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D1_3_length_of_stay.ipynb)

- [ ] One histogram of nights for all parties (5 min)
- [ ] Shares by origin, one panel each (7 min)
- [ ] Box plots by origin (5 min)
- [ ] Find the market with two kinds of trip (5 min)
- [ ] Write the reading (3 min)
- [ ] ✱ Stretch: Change the bin width to 7 nights and say what disappears

### Session 4: Summaries that fit the shape

#### [day1#s4] Summaries that fit the shape

*Session 4*

- Predict from mean and median which way a variable is skewed
- Choose a centre and a spread that the tail does not move
- Summarise a zero-heavy variable and a score without a single mean

#### [day1#mean-follows-tail] The gap between mean and median is a first reading of the shape

*Lab 1.4, step 1*

| Variable | Mean | Median | Mean / median |
| --- | --- | --- | --- |
| Spend per party, riyals | 2,736 | 1,498 | 1.83 |
| Nights | 3.30 | 2 | 1.65 |
| Booking lead, days | 16.2 | 6 | 2.70 |
| Satisfaction, 1 to 5 | 4.12 | 4 | 1.03 |

- A mean far above the median says "long right tail" before any chart is drawn.
- Mean and median that agree do not prove symmetry: satisfaction is piled against the top of its scale.

#### [day1#spread-that-describes] "Mean plus or minus one standard deviation" can describe nobody

*Lab 1.4, step 2*

- **Spend, as often reported.** 2,736 ± 3,788 riyals. The lower end is 1,051 riyals below zero. No party spent that.
- **Spend, by quartiles.** Median 1,498; half of the parties between 571 and 3,392. Three amounts that real parties spent.

- The standard deviation squares distances, so a few large bills dominate it.
- Removing the top 1% of spend cuts the standard deviation by 24% and the median by 1.5%.

#### [day1#log-scale] Variables that multiply are symmetric on a log scale

*Lab 1.4, step 3*

Figure: Spend per party, equal steps on a log scale.

- Spend is nights times party size times a daily rate.
- On a log scale, equal distances are equal ratios.
- Geometric mean 1,344 riyals: near the median 1,498, half the mean 2,736.

#### [day1#zero-heavy] A zero-heavy variable needs two numbers

*Lab 1.4, step 4*

- **36%** of parties did not book at all: lead time 0
- **14 days** median lead of those who booked
- **6 days** median of everyone, which describes neither group

- Two populations share one column: walk-ins and bookers.
- First the share at zero, then a summary of the rest.
- The same shape: spend on tickets among all residents, complaints per visitor, days absent.

#### [day1#scores-need-shares] A score from 1 to 5 is summarised by shares

*Lab 1.4, step 5*

| Item | Value |
| --- | --- |
| 5 | 39.2% |
| 4 | 38.3% |
| 3 | 18.1% |
| 2 | 4.1% |
| 1 | 0.4% |

- "77% score 4 or 5" is a sentence a board can repeat. "Mean 4.12" hides whether the rest are at 3 or at 1.
- A mean of scores assumes the step from 4 to 5 equals the step from 1 to 2. It is still used to compare groups, as Day 2 will; show the shares beside it.

#### [day1#summary-carries-n] Every question gets a chart, a summary and two sentences

*The evidence for outcome 3*

| Shape | Centre | Spread | Chart |
| --- | --- | --- | --- |
| Long right tail (spend) | median, or geometric mean | quartiles | histogram on a log scale |
| Count with humps (nights) | median, with the share in each hump | shares by range | bars, one per value |
| Zero-heavy (booking lead) | share of zeros, median of the rest | quartiles of the rest | two parts |
| Score (satisfaction) | share scoring 4 or 5 | all five shares | bars of shares |

> **A summary always carries** the number of values it rests on and what was left out: here the 2,577 stays with no stated spend, most of them day visits.

#### [day1#check-summary] Which sentence goes into the report?

*Checkpoint*

**Question:** A museum records minutes spent inside by each visitor. 45% of the records show 0 minutes because those visitors used only the cafe. The others stay a median of 70 minutes. Which summary is honest?

- A. Visitors spend a mean of 41 minutes in the museum
- B. 45% of visitors use only the cafe; the others stay a median of 70 minutes
- C. The median visitor spends 25 minutes in the museum
- D. Museum visitors stay a median of 70 minutes inside

#### [day1#lab-1-4] Centre and spread for four variables

Lab 1.4 · 25 min

Choose centre and spread measures for four skewed variables (spend, nights, booking lead time, satisfaction) and say what each summary leaves out.

[D1_4_centre_spread.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D1_4_centre_spread.ipynb)

- [ ] Mean and median of the four variables, and the gap between them (5 min)
- [ ] Spread: standard deviation against quartiles (5 min)
- [ ] Spend on a log scale: the geometric mean (5 min)
- [ ] A zero-heavy variable needs two numbers (4 min)
- [ ] A score from 1 to 5 needs shares (3 min)
- [ ] Choose and write the reading (3 min)
- [ ] ✱ Stretch: Remove the top 1% of spend and see which summaries move

#### [day1#wrap-up] Three things to keep

*Day 1*

- **The question comes first.** Unit of observation, variables, comparison, and whether you are exploring or confirming. A plan that passes a checklist before any chart.
- **Profile, then log.** Grain, types, missing values, ranges, categories, coverage. Each issue with its rows and a decision someone can dispute.
- **Shape before summary.** Look at the distribution, then choose the centre and the spread that describe it. Always with the number of values and what was left out.

#### [day1#next] Relationships and time

*Day 2*

Two variables at once, counts against rates, three years of monthly arrivals, and a total that says the opposite of its parts.

- Keep your plan from lab 1.1 at hand: Day 2 answers questions 2 to 5.
- Every lab starts from the supplied tables. Nothing from today's notebooks is needed.

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

#### [day2#small-cells] Cut finer and the highest rates rest on the fewest cases

*Lab 2.2, steps 4 and 5*

| Site × origin | Complaints | Visitors | Published |
| --- | --- | --- | --- |
| Terrace Farms × Asia | 6 | 441 | withheld |
| Terrace Farms × Europe | 4 | 321 | withheld |
| Cloud Lookout × Asia | 6 | 1,769 | withheld |
| Honey Museum × Asia | 8 | 2,075 | withheld |

- The board's rule: publish a cell only with at least **10 complaints and 1,000 visitors**.
- Four of 45 cells are held back. Two of them would have shown the highest rates in the table.
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

## Day 3: Building honest charts

A chart as a specification: marks, encodings and scales chosen so that the picture and the numbers agree

#### [day3#title] Building honest charts

*SDAIA Academy · Exploratory Analysis and Visualisation*

Day 3: A chart as a specification: marks, encodings and scales chosen so that the picture and the numbers agree

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-203

#### [day3#agenda] Building honest charts

*Today*

- **Session 1 · Marks, encodings and scales**: A chart is data, marks, encodings and scales; choosing the channel for the comparison that matters
- **Session 2 · Small multiples**: Small multiples: when panels beat one crowded chart, and what shared and free scales each let a reader compare
- **Session 3 · Charts that mislead**: Six ways a correct number becomes a wrong impression, and the repair for each
- **Session 4 · Colour, labels and Arabic text**: Colour that survives colour-vision deficiency and print, labels that carry the finding, and charts that read in Arabic and English

#### [day3#review-day-2] What does the director need beside this number?

*Review · Day 2*

**Question:** A report says: "Branch C has the most late deliveries: 310 this quarter." Before the sentence is printed, what has to stand beside 310?

- A. The average number of late deliveries per branch
- B. The number of late deliveries in the quarter before
- C. A p-value for the difference between the branches
- D. The deliveries Branch C made, so 310 becomes a rate

### Session 1: Marks, encodings and scales

#### [day3#s1] Marks, encodings and scales

*Session 1*

- Describe any chart as data, marks, encodings and scales
- Rank position, length, area and colour by how precisely they are read
- Build a layered chart from a written specification

#### [day3#chart-as-specification] Every chart is four decisions

*The grammar of graphics*

| Part | The decision | In lab 3.1 |
| --- | --- | --- |
| **Data** | what one row is | one site: complaints, visitors, rate |
| **Marks** | the shape drawn for each row | a circle, a rule, a text |
| **Encodings** | which column drives which visual channel | rate → x, site → y, visitors → size |
| **Scales** | how values become positions, sizes and colours | x from zero; sites sorted by rate |

> **Why think this way.** "Bar chart" and "scatter plot" are names for a few common combinations. The four parts describe all of them, and tell you what to change.

#### [day3#channels-ranked] Give the most precise channel to the comparison that matters

*Not all channels are read equally well*

| Item | Value |
| --- | --- |
| Position on a common scale | most precise |
| Length |  |
| Angle and slope |  |
| Area |  |
| Colour intensity | least precise |

- Colour hue tells categories apart; it does not order them.
- A small difference shows in position long before it shows in area or shade.

#### [day3#specification-to-code] The written specification and the code have the same four parts

*Lab 3.1, steps 2 and 3*

```python
alt.Chart(rates).mark_circle().encode(                       # data, mark
    x=alt.X("per_thousand:Q",                                # encoding: a quantity
            scale=alt.Scale(zero=True),                      # scale: from zero
            title="Complaints per thousand visitors, 2023 to 2025"),
    y=alt.Y("site:N", sort="-x", title=None),                # a name, sorted by x
).properties(title="Complaints per thousand visitors by site")
```

- `:Q` a quantity, `:N` a name, `:O` an order, `:T` a time. The type picks the default scale.
- Sorting and titles are part of the specification, not decoration.

#### [day3#layers] Layers share the data and the scales, and add one mark each

*Lab 3.1, step 4*

Figure: Rule, circle and text: three layers.

- The rate has position; the visitors have area.
- The largest circle is fifth from the top.
- One chart now says what lab 2.2 needed a paragraph for.

```python
alt.layer(rule, dot, label)
```

#### [day3#change-one-mark] Change one part and you can say what was gained and lost

*Lab 3.1, step 5*

Figure: The same data, x and y, as bars.

- A bar's length already carries the rate, so size is taken: **the visitors drop off the chart**.
- Bars are familiar and read fast.
- A bar is measured from its base. A point is read by its place.

> **The rule that follows.** Bars and areas need an axis from zero. Points and lines may use an axis that starts elsewhere, if the chart says so.

#### [day3#check-grammar] Which channel for which variable?

*Checkpoint*

**Question:** A chart must let a manager compare average waiting time across 12 clinics, and also show roughly how many patients each clinic sees. Which specification serves that?

- A. Clinic on y, patients on x, waiting time as circle size
- B. Clinic on y sorted by wait, waiting time on x, patients as circle size
- C. Clinic on y, patients on x, waiting time as colour intensity
- D. A pie chart with one slice per clinic, sized by waiting time

#### [day3#lab-3-1] A chart from a written specification

Lab 3.1 · 25 min

Rebuild one chart from a written specification: complaint rates by site as marks, encodings, scales and a text layer.

[D3_1_chart_from_spec.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D3_1_chart_from_spec.ipynb)

- [ ] Read the specification: data, marks, encodings (3 min)
- [ ] The base chart: position for the rate (6 min)
- [ ] Sort, start the scale at zero, write the titles (5 min)
- [ ] A second encoding and a text layer (6 min)
- [ ] Change one mark and say what the reader loses (3 min)
- [ ] Write the reading (2 min)
- [ ] ✱ Stretch: Write the specification of a chart from lab 1.3 in the same form

### Session 2: Small multiples

#### [day3#s2] Small multiples

*Session 2*

- Replace a crowded chart with small multiples
- Choose shared scales to compare levels and free scales to compare shapes
- State the scale choice on the chart

#### [day3#crowded-chart] Five lines on one panel answer one question and hide four

*Lab 3.2, step 1*

Figure: Monthly arrivals by origin market.

- You can read which market is largest.
- When does Europe peak? Does Asia have a season? The bottom tenth of the chart holds three lines.
- The legend has to be decoded for every line.

#### [day3#shared-scales] Small multiples: the same chart, one panel per group

*Lab 3.2, step 2*

Figure: One y scale for all panels.

- No legend: each panel is labelled. Once one panel is understood, all are.
- A **shared scale** compares levels across panels: who is big.
- Asia and Europe are still flat lines.

#### [day3#free-scales] A scale per panel shows each group's shape

*Lab 3.2, step 3*

Figure: Each panel has its own scale from zero.

- Europe peaks in **December**, in every other market's low season.
- Asia has almost no season and the steepest growth.
- Heights can no longer be compared across panels, and the chart says so.

#### [day3#which-scale-for-which-question] The question chooses the scale

*Lab 3.2, steps 4 and 5*

| The reader should compare | Scales | Because |
| --- | --- | --- |
| levels: which market is largest | shared | heights mean the same in every panel |
| shapes: who has a season, and when | free, from zero | each shape fills its panel |
| growth: who grew fastest | shared, on an index | every line starts at 100 |

> **What goes wrong.** Free scales with no note. The reader compares heights across panels anyway and concludes that all markets are the same size.

#### [day3#limits-of-small-multiples] Small multiples trade exact comparison for clarity

*When panels stop helping*

- **They suit.** Three to about twenty groups; one simple chart repeated; a reader who compares patterns.
- **They strain.** Two lines whose gap is the message: put those on one panel, where the gap has position.
- **They need.** A deliberate order of panels, identical axes in type, and few tick labels on each.

> **A useful middle way.** Draw every group in grey in every panel and highlight one. The reader gets the shape and the place among the others.

#### [day3#check-facets] Shared or free?

*Checkpoint*

**Question:** Weekly sales of 8 product lines are drawn as small multiples. The largest line sells fifty times the smallest. The manager asks: "Which lines have a December peak?" Which design answers that?

- A. A shared y scale, so that all eight panels can be compared
- B. A single panel with eight lines, one colour for each line
- C. A y scale per panel from zero, with a note that scales differ
- D. A y scale per panel, fitted tightly to each line's range

#### [day3#lab-3-2] Arrivals in small multiples

Lab 3.2 · 25 min

Facet arrivals by origin market, draw the panels with shared and with free scales and choose the one that answers each question.

[D3_2_facet_arrivals.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D3_2_facet_arrivals.ipynb)

- [ ] Five lines in one panel: what can be read (4 min)
- [ ] One panel per market, shared scale (5 min)
- [ ] The same panels with free scales (5 min)
- [ ] What each version answers: peak month and peak-to-trough ratio (5 min)
- [ ] Choose, order the panels and say the scale on the chart (4 min)
- [ ] Write the reading (2 min)
- [ ] ✱ Stretch: Index each market to 2023 = 100 and compare with the free-scale version

### Session 3: Charts that mislead

#### [day3#s3] Charts that mislead

*Session 3*

- Name the fault of a misleading chart
- Repair a chart by changing its scale, window, measure or encoding
- Say what a reader concludes before and after the repair

#### [day3#six-faults] Six charts, every number correct, every impression wrong

*The board's earlier report*

| Fault | What it does | Repair |
| --- | --- | --- |
| **Cut baseline** | a bar's axis does not start at zero | start at zero, or change the mark |
| **Picked window** | a few periods chosen out of many | show the whole series |
| **Count for rate** | counts compared across unequal groups | divide by the denominator |
| **Two axes** | two scales stretched until shapes agree | one variable against the other |
| **Running total** | a cumulative line, which can only rise | plot the amount per period |
| **Uneven steps** | unequal periods drawn as equal steps | equal periods on a time axis |

#### [day3#fault-cut-baseline] "Satisfaction collapsed in 2025"

*Fault 1 · Cut baseline*

Figure: As published: the axis runs from 4.0 to 4.2.

Figure: Repaired: bars from zero.

- A bar says "this much". Cut the base and the 2025 bar is half the 2024 bar for a fall of 2%.
- If 0.08 matters, use points on a stated axis, with intervals.

#### [day3#fault-picked-window] "Arrivals up 37% in a year"

*Fault 2 · Picked window*

Figure: As published: two months of thirty-six.

Figure: Repaired: every month.

- October 2024 was the first Honey Festival. The typical yearly growth is about 7%.
- Ask of any two-point comparison: why these two points?

#### [day3#fault-count-for-rate] "The Cable Car is our problem site"

*Fault 3 · Count for rate*

Figure: As published: complaints.

Figure: Repaired: per thousand visitors.

- The picture of yesterday's lab 2.2: the busiest site leads any count.
- The repair changes the **measure**, not the drawing.

#### [day3#fault-two-axes] "Hotels follow the sites exactly"

*Fault 4 · Two axes*

Figure: As published: two y axes, each fitted to its line.

Figure: Repaired: one variable against the other.

- With two free axes, any two series can be made to overlap. Where they cross means nothing.
- The scatter shows the relation at its true strength: 0.70, loosely.

#### [day3#fault-running-total] "Local visits keep climbing"

*Fault 5 · Running total*

Figure: As published: arrivals since January 2023.

Figure: Repaired: arrivals per month.

- A running total rises whenever anything arrives at all. It cannot show a fall.
- Local arrivals fell 6% over two years: 258,000 in 2023, 242,000 in 2025.

#### [day3#fault-uneven-steps] "Arrivals fell off a cliff in 2025"

*Fault 6 · Uneven steps*

Figure: As published: years, a half year and two months.

Figure: Repaired: three periods of equal length.

- A year, half a year and a month were drawn as equal steps.
- Yearly arrivals: 842,000, 914,000, 998,000.

#### [day3#before-you-publish] Five questions before a chart goes out

*Lab 3.3, step 4*

- Does a bar or an area start at zero?
- Is the whole period shown, in equal steps?
- Is it the right measure: rate, per period, per unit?
- Is there one y axis?
- Does the title say what the chart shows, and no more?

- **The test of a repair.** Write what a reader concludes from the chart before and after. If the two sentences agree, the fault was cosmetic. In all six cases here they disagree.

#### [day3#check-misleading] Name the fault

*Checkpoint*

**Question:** A slide shows app downloads "since launch" as a line that rises every month, under the title "Growth is accelerating". Monthly downloads have in fact been falling for half a year. Which fault is this, and which repair?

- A. Cut baseline: restart the y axis of the line at zero
- B. Picked window: add the months before the launch
- C. Two axes: move downloads to a second panel
- D. Running total: plot the downloads of each month

#### [day3#lab-3-3] Repair six misleading charts

Lab 3.3 · 25 min

Repair six misleading charts from the board's earlier report and name each fault: a cut baseline, a picked window, counts for rates, two axes, a running total and uneven time steps.

[D3_3_repair_six_charts.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D3_3_repair_six_charts.ipynb)

- [ ] Name the fault of each of the six charts (5 min)
- [ ] Repair charts 1 to 3: baseline, window, rate (9 min)
- [ ] Repair charts 4 to 6: two axes, running total, time steps (9 min)
- [ ] Write what a reader now concludes (2 min)
- [ ] ✱ Stretch: Find a seventh chart in your own work and name its fault

### Session 4: Colour, labels and Arabic text

#### [day3#s4] Colour, labels and Arabic text

*Session 4*

- Choose a palette by the type of variable and test it for colour-vision deficiency
- Add a second channel so that colour is never the only carrier
- Produce one chart in Arabic and in English from the same code

#### [day3#palette-by-variable] The type of the variable chooses the kind of palette

*Colour is an encoding*

- **Categorical.** Names with no order: origin market, site. Distinct hues of similar weight. Five to seven at most.
- **Sequential.** Low to high: a count, a rate. One hue from light to dark, as in the heatmap of lab 2.1.
- **Diverging.** Two directions from a midpoint: above and below a baseline. Two hues meeting in a neutral colour.

> **What goes wrong.** A rainbow for a quantity: the eye sees bands where the data has none. Or a light-to-dark ramp for names: the reader sees an order that does not exist.

#### [day3#colour-vision] Test the palette for colour-vision deficiency

*Lab 3.4, step 1*

Figure: The draft chart: five lines of yearly arrivals indexed to 100 in 2023, in red, green, orange, brown and blue, with axis titles year and index and the title Arrivals

- Under red-green deficiency the draft's red and green are **7 units** apart: hard to tell.
- The Okabe-Ito palette keeps every pair above **18**.
- Do not trust the look on your own screen.

#### [day3#second-channel] Colour is never the only carrier

*Lab 3.4, step 2*

Figure: Safe palette, and a dash pattern per market.

- A second channel repeats the first: dash for lines, shape for points.
- Better still, **label the lines directly** at their ends and drop the legend.
- The test: print the chart in grey. Can each line still be named?

#### [day3#labels-carry-the-finding] The title states the finding; the rest says how to read it

*The words on a chart*

| Text | Draft | Finished |
| --- | --- | --- |
| Title | Arrivals | Arrivals grew fastest from the smallest markets |
| Subtitle | none | Yearly arrivals by origin market, 2023 = 100 |
| y axis | index | Arrivals, 2023 = 100 |
| Legend | origin | Origin market |

- A title that names the finding can be checked against the chart. "Arrivals" cannot be wrong, or useful.
- Units, the base of an index, the period and the source belong on the chart, since charts get copied without their page.

#### [day3#one-function-two-languages] The words live in a file; the chart is drawn by one function

*Lab 3.4, step 3*

```python
L = U.js("labels.json")                       # every text, in Arabic and English

def chart(data, lang):
    T = L["text"][lang]                       # title, subtitle, x, y, legend
    d = data.assign(origin_label=data["origin"].map(L["origins"]) if lang == "ar" else data["origin"])
    return alt.Chart(d).mark_line().encode(
        x=alt.X("year:O", title=T["x"]), y=alt.Y("index:Q", title=T["y"]),
        color=alt.Color("origin_label:N", title=T["legend"]),
    ).properties(title=alt.Title(T["title"], subtitle=T["subtitle"]))
```

- The data keeps its own column; the labels are mapped at drawing time.
- Two charts copied and edited by hand drift apart at the first correction.

#### [day3#arabic-details] In Arabic the words move; the data does not

*Lab 3.4, step 4*

Figure: The Arabic version, from the same function.

- Title anchored at the right; y axis on the right.
- House style of this course: Western digits, and time from left to right, in both versions.
- Let the text engine shape and order Arabic. **Never reverse or reshape strings by hand.**

#### [day3#check-colour] Which change comes first?

*Checkpoint*

**Question:** A line chart of four regions uses red, green, blue and orange lines and a legend. It will be printed in a bilingual annual report. Which single change helps the most readers?

- A. Label each line at its end, and give each its own dash pattern
- B. Make the four lines thicker so that the colours show better
- C. Use four shades of one blue, from light to dark
- D. Add the region names to the legend in both languages

#### [day3#lab-3-4] One chart, two languages, safe colours

Lab 3.4 · 25 min

Make one chart readable in Arabic and English and colour-blind safe: test the palette, add a second channel and draw both language versions from one function.

[D3_4_bilingual_chart.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D3_4_bilingual_chart.ipynb)

- [ ] Test the supplied palette for colour-vision deficiency (4 min)
- [ ] A safe palette and a second channel (6 min)
- [ ] One function, two languages: titles and names from a label file (7 min)
- [ ] Arabic details: axis side, alignment, digits (5 min)
- [ ] Write the reading (3 min)
- [ ] ✱ Stretch: Replace the legend with a label at the end of each line

#### [day3#wrap-up] A chart is decisions you can defend

*Day 3*

- **Four parts.** Data, marks, encodings, scales. Position goes to the comparison that matters.
- **Panels.** Shared scales for levels, free scales for shapes, and the choice written on the chart.
- **Six faults.** Baseline, window, measure, axes, running totals, steps. Test a repair by what a reader concludes.
- **The finish.** A tested palette, a second channel, a title that states the finding, one function for two languages.

#### [day3#next] Check and report

*Day 4*

Could it be chance, how to draw what is not known, why the best of many comparisons looks real, and a report that anyone can run again.

- Tomorrow uses the bootstrap and the permutation test of DS-201. Reread your notes on both.
- In lab 4.4 you choose your capstone dataset.

## Day 4: Check and report

Which patterns survive a chance check, how to draw what is not known, and a report that anyone can run again

#### [day4#title] Check and report

*SDAIA Academy · Exploratory Analysis and Visualisation*

Day 4: Which patterns survive a chance check, how to draw what is not known, and a report that anyone can run again

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-203

#### [day4#agenda] Check and report

*Today*

- **Session 1 · Could it be chance**: Applying the resampling of DS-201 to patterns found by exploring: which rule for which pattern, and what to do with the result
- **Session 2 · Showing uncertainty**: Drawing uncertainty: interval marks, what a bar hides, and captions that say what the interval is
- **Session 3 · The traps of exploring**: Why the best of many comparisons looks real, how to count the comparisons made, and what turns an exploratory finding into a confirmed one
- **Session 4 · A report that reruns**: What makes a report rerun: raw data read-only, one path from raw data to the page, fixed seeds, and findings written with their limits

#### [day4#review-day-3] Where may this axis start?

*Review · Day 3*

**Question:** A service desk's monthly response time moved between 41 and 46 minutes over two years. The changes must be visible. Which chart is honest?

- A. Bars, with the y axis from 40 to 47 minutes
- B. Bars, with the y axis from 0 to 50 minutes
- C. A line with points, y axis from 40 to 47, range stated in the title
- D. A filled area, with the y axis from 40 to 47 minutes

### Session 1: Could it be chance

#### [day4#s1] Could it be chance

*Session 1*

- Choose shuffling for a gap between groups and resampling for an interval
- Resample the unit that was sampled, here the week
- Decide to report, qualify or drop a pattern and give the reason

#### [day4#three-patterns] Three patterns, and three decisions open for each

*What the board wants to announce*

- **The weekend.** "Weekend visitors are more satisfied than weekday visitors."
- **Sites and hotels.** "When the sites are busy, the hotels fill."
- **The Honey Museum.** "At the Honey Museum, weekend visitors were far more satisfied in 2025."

| Decision | Meaning |
| --- | --- |
| **Report** | the pattern stands and matters |
| **Qualify** | it stands, with a stated limit |
| **Drop** | the data does not support announcing it |

#### [day4#which-rule] Shuffle to test a difference; resample to put an interval on an estimate

*From DS-201, in one slide*

|  | Permutation test | Bootstrap |
| --- | --- | --- |
| **Question** | could this gap arise if the label meant nothing? | how far could this estimate move with another sample? |
| **Procedure** | shuffle the labels, recompute the gap | draw the units again with replacement, recompute |
| **Result** | a p-value | an interval |
| **Here** | the weekend gap | the weekly correlation |

> **New today.** Not the procedures: choosing between them, choosing the unit to resample, and deciding what to do with the result.

#### [day4#weekend-gap] Shuffled labels give this gap one time in three

*Lab 4.1, steps 1 to 3*

Figure: Gaps under shuffled labels; the lines mark the observed gap.

- Weekend 4.13, weekday 4.11: a gap of **+0.02**.
- p-value about **0.35**.
- Decision: **drop** the claim.

#### [day4#drop-is-not-no-effect] "Drop" means "this data cannot tell", not "there is no difference"

*The sentence that goes in the report*

- **Not supported.** "The day of the week makes no difference to satisfaction."
- **Supported.** "The survey shows no clear difference between weekend and weekday visitors (gap 0.02 point, p about 0.35)."

- A p-value of 0.35 is the absence of evidence for a difference. It is not evidence of absence.
- To claim "no difference worth acting on", give the interval of the gap and say what size would matter.

#### [day4#resample-the-unit] Resample the unit that was sampled: here, the week

*Lab 4.1, steps 4 and 5*

- **43,840 hotel-days.** Forty hotels share one day's weather and one day's ticket total. Days in a week resemble each other. Resampling them as if independent gives an interval far too narrow.
- **156 weeks.** One row per week for the whole region. Draw 156 weeks with replacement, recompute the correlation, repeat 5,000 times.

```python
k = gen.integers(0, len(x), len(x))        # 156 weeks, drawn with replacement
r[i] = np.corrcoef(x[k], y[k])[0, 1]
```

> **What goes wrong.** Counting rows as evidence. The number that matters is how many independent units there are.

#### [day4#correlation-interval] The correlation is not chance, and still needs a qualifier

*Lab 4.1, steps 5 and 6*

- **0.70** weekly tickets and hotel occupancy
- **0.60 to 0.78** 95% bootstrap interval, 156 weeks
- **0.44** with each calendar month's mean removed

- The interval stays far from zero: weeks with busy sites do have fuller hotels.
- Part of the 0.70 is the shared season. What remains is smaller and still positive.
- Decision: **qualify**. The check answers "is it chance", never "is it cause".

#### [day4#what-a-chance-check-settles] A chance check answers one question out of four

*Before deciding*

| Question | Answered by | Session |
| --- | --- | --- |
| Could it be chance? | a permutation test or a bootstrap interval | this one |
| Is it large enough to matter? | the size of the effect, in the units of the decision | this one |
| Was it found by searching? | counting the comparisons that were made | 4.3 |
| Is it the mix, the season or the measure? | the checks of Day 2 | 2.2 to 2.4 |

> **The decision carries its reason.** "Drop: p about 0.35 and a gap of 0.02." "Qualify: interval 0.60 to 0.78; season raises both."

#### [day4#check-chance] Which procedure, on which unit?

*Checkpoint*

**Question:** A school network has test scores of 4,000 pupils in 40 schools. Twenty schools used a new timetable. The analyst wants an interval for the difference in mean score between the two groups of schools. What should be resampled?

- A. The 4,000 pupils, drawn again with replacement
- B. The timetable labels of the pupils, shuffled
- C. The 4,000 scores, drawn within each school
- D. The 40 schools, drawn again with replacement

#### [day4#lab-4-1] Chance checks on two patterns

Lab 4.1 · 25 min

Permutation-test the claimed weekend effect on satisfaction and bootstrap the correlation between weekly ticket sales and hotel occupancy; decide for each whether to report, qualify or drop it.

[D4_1_chance_checks.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D4_1_chance_checks.ipynb)

- [ ] The weekend gap in satisfaction, as claimed (3 min)
- [ ] Shuffle the weekend labels: the p-value (7 min)
- [ ] Decide: report, qualify or drop (2 min)
- [ ] The correlation of weekly tickets and occupancy (3 min)
- [ ] Bootstrap the weeks: an interval (7 min)
- [ ] Decide, and write the reading (3 min)
- [ ] ✱ Stretch: Remove the season from both series and bootstrap again

### Session 2: Showing uncertainty

#### [day4#s2] Showing uncertainty

*Session 2*

- Add an interval to every estimate on a chart
- Read overlapping and separate intervals without overclaiming
- Write a caption that names the interval, the sample size and the limit

#### [day4#what-a-bar-hides] "Terrace Farms is our best-rated site"

*The earlier report*

Figure: As published: mean satisfaction in 2025.

- Each bar is one number drawn as if it were exact.
- The bars rest on **59 to 510** responses. The chart does not say which.
- And yesterday's fault 1: bars on an axis from 3.8.

#### [day4#interval-per-site] Every estimate on a chart gets an interval

*Lab 4.2, steps 1 and 2*

| Site | Responses | Mean | 95% interval |
| --- | --- | --- | --- |
| Terrace Farms | 59 | 4.24 | 4.02 to 4.44 |
| Souq Walk | 442 | 4.22 | 4.13 to 4.30 |
| Honey Museum | 167 | 4.10 | 3.97 to 4.24 |
| Cable Car | 510 | 3.93 | 3.84 to 4.00 |
| Wadi Trail | 132 | 3.91 | 3.76 to 4.05 |

- The fewer the responses, the wider the interval: roughly with one over the square root of n.
- The site at the top has the widest interval of all.

#### [day4#points-with-intervals] A point, a line for the interval, and n beside the name

*Lab 4.2, step 3*

Figure: Mean satisfaction in 2025 with 95% bootstrap intervals.

- A point is read by position, so the axis may run from 3.6 to 4.6.
- Seven of the other eight intervals overlap that of Terrace Farms.

#### [day4#reading-intervals] Overlap does not prove equality: compute the interval of the difference

*Lab 4.2, step 4*

- Two intervals that do not overlap: the groups differ.
- Two intervals that overlap: this sample cannot order them. They may still differ.
- For a claim about two groups, resample both and take the difference each time.

- **Guided against unguided visits, 2025.** Difference in mean satisfaction: **+0.39** point, interval **+0.31 to +0.47**, from 680 guided and 1,520 unguided responses. The whole interval is far above zero: **report**.

> **What goes wrong.** Reading "overlapping" as "the same" and announcing that all sites perform equally.

#### [day4#marks-for-uncertainty] Uncertainty has its own marks

*Which mark for which chart*

- **Point and interval.** For a few estimates by group. The default of this course.
- **Band around a line.** For an estimate over time: a shaded band from the lower to the upper end at each date.
- **The data itself.** With small groups, draw every value as a faint point behind the estimate. Twelve points say "twelve" better than any interval.

> **Avoid** a bar with a whisker on top: the bar still says "this much from zero", and readers judge by the bar. And never draw an interval without saying what it is.

#### [day4#caption-for-uncertainty] The caption names the interval, the sample and the limit

*Lab 4.2, step 5*

**As published:** Terrace Farms is our best-rated site.

**Rewritten:** Mean satisfaction in 2025 by site with 95% bootstrap intervals. The Souq Walk (4.22, n = 442) rates above the Cable Car (3.93, n = 510); Terrace Farms' 4.24 rests on 59 responses and cannot be ranked first. The intervals show how far each mean could move with another sample of respondents; they do not correct for who chose to answer or for the mix of visitors at each site.

- An interval covers sampling variation only.
- Who answers a survey, how the question is put and the mix of visitors are outside it.

#### [day4#check-uncertainty] What may the report say?

*Checkpoint*

**Question:** Two call centres have mean satisfaction 4.3 (interval 4.1 to 4.5, n = 80) and 4.1 (interval 4.0 to 4.2, n = 600). The intervals overlap. Which statement is supported?

- A. The two centres deliver the same level of satisfaction
- B. This sample cannot rank them; the difference needs its own interval
- C. The first centre is better, since its mean is higher
- D. The second centre is better, since its interval is narrower

#### [day4#lab-4-2] Intervals on the satisfaction chart

Lab 4.2 · 25 min

Add intervals to the satisfaction bar chart of the earlier report, find which sites can be told apart and rewrite its caption.

[D4_2_intervals_caption.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D4_2_intervals_caption.ipynb)

- [ ] The chart as published, and the responses behind each bar (3 min)
- [ ] A bootstrap interval for each site (7 min)
- [ ] Points with intervals, sorted, with the sample size (7 min)
- [ ] The interval of a difference: guided against unguided visits (4 min)
- [ ] Rewrite the caption (4 min)
- [ ] ✱ Stretch: Draw the 2025 intervals by origin market inside one site

### Session 3: The traps of exploring

#### [day4#s3] The traps of exploring

*Session 3*

- Count the comparisons behind a reported pattern
- Simulate the most striking gap that chance alone produces among that many comparisons
- Mark a finding exploratory or confirmed and name the check it needs

#### [day4#the-headline] "At the Honey Museum, weekend visitors were far more satisfied in 2025"

*A week after the weekend claim was dropped*

- **+0.30** weekend minus weekday, on a 1 to 5 scale
- **0.03** p-value by permutation, taken alone
- **167** responses: 68 weekend, 99 weekday

- Fourteen times the gap that was dropped this morning.
- It passes a chance check. It is large enough to matter.
- One question is left: **how was it found?**

#### [day4#count-the-comparisons] It was the most striking of 27 comparisons

*Lab 4.3, step 2*

Figure: Twenty-seven points, one per site and year, showing the weekend minus weekday gap in satisfaction in standard errors, sorted: they scatter from about minus 1.5 to plus 2.2 around zero, with the Honey Museum 2025 highlighted at the top as the only one beyond 2

- Nine sites, three years: 27 gaps were looked at. One was kept.
- 16 are above zero, 11 below.

#### [day4#at-least-one] With 27 comparisons of nothing, a "finding" is the likely outcome

*Lab 4.3, step 3*

```text
# file: the chance of at least one p-value below 0.05
 1 comparison      1 - 0.95^1    =   5%
 5 comparisons     1 - 0.95^5    =  23%
27 comparisons     1 - 0.95^27   =  75%
135 comparisons    1 - 0.95^135  =  99.9%
```

- A p-value of 0.05 means: one time in twenty, nothing looks like something.
- Look twenty-seven times and it is three chances in four.
- 135 is what the search becomes if it also splits by origin market.

#### [day4#simulate-the-search] Check the method that was used, search included

*Lab 4.3, step 4*

Figure: The most striking of 27 gaps when the labels mean nothing.

- Shuffle the weekend labels inside every site and year; keep the most striking of the 27 gaps; repeat.
- Its median is 2.3 standard errors. The headline's is 2.2.
- A gap as striking as the headline turns up in **about half** of the shuffles.

#### [day4#forking-paths] Every choice made after looking is a comparison

*Beyond 27*

- Which groups: weekend, or Friday alone, or school holidays?
- Which measure: the mean, or the share of 5s?
- Which rows: all responses, or "excluding" a bad month?
- Which period: 2025, or the last six months?

- **In the board's past report.** "Visitors who arrive on a Tuesday spend the most": spend tabulated by every day of the week, every origin and every purpose, and the largest cell reported.

> **No bad faith is needed.** An honest analyst who looks until something stands out has run many tests and remembers one.

#### [day4#exploratory-or-confirmed] What makes a finding confirmed is the order of events

*Lab 4.3, step 5*

- **Confirmed.** The question was written down **before** the data that answers it was looked at. "Guided visits are rated higher": noticed in the 2023 survey, written down, then tested once on the 2024 survey.
- **Exploratory.** The data suggested the question. "Hotels in the Ridge zone fill up before the Honey Festival": seen in a chart of 2024 while looking for something else.

- Exploratory is a label, not an insult: it is where questions come from.
- The same data cannot both suggest a pattern and confirm it.

#### [day4#from-exploratory-to-confirmed] An exploratory finding is reported with its count and its next test

*Lab 4.3, step 6*

1. **1 · Label** "Exploratory", in the sentence itself
2. **2 · Count** how many comparisons it was chosen from
3. **3 · Write down** the question, before new data exists
4. **4 · Test once** on data that did not suggest it

> **In the report.** "Exploratory: among 27 comparisons, the most striking gap was 0.30 point at the Honey Museum in 2025; shuffled labels produce one as striking about half the time. The question will be tested once on the 2026 survey."

#### [day4#check-exploring] What is this finding worth?

*Checkpoint*

**Question:** An analyst compares churn between customers who did and did not use each of 40 app features. One feature shows a difference with p = 0.02. The team wants to announce "Feature X reduces churn". What should the analyst say?

- A. It is exploratory: expected among 40 looks; test it once on new customers
- B. It is confirmed, because the p-value is well below 0.05
- C. It will be confirmed once the test is rerun with more shuffles
- D. It should be discarded and left out of the report entirely

#### [day4#lab-4-3] Count the comparisons

Lab 4.3 · 25 min

Count the comparisons behind a headline pattern, simulate the most striking of 27 chance gaps, mark five past findings exploratory or confirmed and rewrite the finding.

[D4_3_count_comparisons.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D4_3_count_comparisons.ipynb)

- [ ] The headline gap and its p-value, taken alone (4 min)
- [ ] All 27 site-year gaps (5 min)
- [ ] The chance of at least one small p-value among 27 (2 min)
- [ ] Simulate the most striking of 27 gaps under no effect (6 min)
- [ ] Mark five past findings exploratory or confirmed (5 min)
- [ ] Rewrite the finding (3 min)
- [ ] ✱ Stretch: Count again with origin added to site and year

### Session 4: A report that reruns

#### [day4#s4] A report that reruns

*Session 4*

- Render a report from raw data with one command and prove that two runs agree
- Find what makes a report change between runs
- Write findings with their check, their limit and an open question

#### [day4#what-reruns-means] A report that reruns has one path from the raw data to the page

*The promise*

1. **Raw data** read-only, never edited by hand
2. **One source** text and code together, parameters at the top
3. **One command** runs everything in a fresh process
4. **The page** every number computed by that run

- No number is typed; no chart is pasted.
- A correction to the data reaches every figure at the next render.
- Somebody else can run it and get the same page.

#### [day4#two-renders-differ] Render twice and compare: the first test of any report

*Lab 4.4, steps 1 and 2*

```text
first render : out/draft_a.html, digest 27942ef6cebc
second render: out/draft_b.html, digest 319a4f665407
  correlation_high: 0.783 then 0.78
  correlation_low:  0.602 then 0.6
```

- Nothing was changed between the two runs. The bootstrap drew different resamples.
- A fixed seed, passed as a parameter, makes two runs agree.
- A third decimal is enough for two people to hold two versions of "the" report.

#### [day4#stale-cache] A cached number is a number with no code behind it

*Lab 4.4, step 3*

| In the report | From the cache | From the raw data |
| --- | --- | --- |
| Stays | 40,600 | 40,000 |
| Stays from the Gulf | 5,553 | 6,063 |
| Mean length of stay, nights | 11.27 | 3.30 |

- The summary was saved once, before lab 1.2 found the duplicate rows, the 999 nights and the three spellings of "Gulf".
- It was right on the day it was saved. Later decisions about the data never reached it.

#### [day4#findings-table] Every finding carries its status, its check and its limit

*Lab 4.4, step 4*

| Finding | Status | Check | Limit |
| --- | --- | --- | --- |
| Weeks with more ticket sales are weeks with fuller hotels (0.70) | exploratory | bootstrap of 156 weeks: 0.60 to 0.78 | season raises both; no causal claim |
| Guided visits were rated 0.4 point higher in 2025 | confirmed | question written before the 2024 survey was opened | visitors choose a guided visit |
| Weekend gap at the Honey Museum (0.30) | exploratory | most striking of 27; as striking in half of shuffles | to be tested on the 2026 survey |

> **The table is the report's spine.** A reader with two minutes reads it and nothing else, so no finding may sit in it without a limit.

#### [day4#writing-for-the-director] An exploratory report says what was seen, how sure, and what is still open

*The reader is not an analyst*

- **Findings first**, each one sentence with its number, in the reader's words.
- **One chart per finding**, titled with the finding, drawn with its uncertainty.
- **Open questions**: what the data suggested and has not tested.
- **Limits**: what the data cannot show, and who is missing from it.

- **Words to keep out.** "Proves", "causes", "significant" with no number, "the data says". An exploratory report writes "we saw", "in this data", "to be tested".

#### [day4#capstone-briefing] An exploratory report on a dataset you have not seen

*Capstone day*

- **Ruwaq Museums Network.** One row per visit: museum, visitor type, minutes inside, exit rating. For the head of programmes.
- **Awan Parks Department.** One row per maintenance request: park, category, days to close, resident rating. For the head of operations.
- **Miqdam Driving Schools.** One row per driving test: branch, attempt, waiting days, result. For the director of training.

- Submit a public repository: a notebook that reruns with a fixed seed, the rendered report, a README with the findings table.
- Defend it live in **8 minutes**, and redraw one chart with a different encoding when asked.

#### [day4#check-report] Will this report rerun?

*Checkpoint*

**Question:** A colleague sends a notebook and a PDF report. In the notebook, one cell loads `cleaned_final_v3.csv` from their desktop, and the bootstrap has no seed. Which request comes first?

- A. Set a seed, so that the intervals stop changing
- B. Send the cleaned file along with the notebook
- C. List the library versions that were used
- D. Start from the raw data, with the cleaning steps as code

#### [day4#lab-4-4] A report that reruns

Lab 4.4 · 25 min

Render a notebook to a report from raw data, find why two runs disagree and why the cached numbers are stale, then choose the capstone dataset.

[D4_4_report_reruns.ipynb](https://sdaiaacademy.github.io/ds-203/labs/D4_4_report_reruns.ipynb)

- [ ] Render the draft twice and compare (5 min)
- [ ] Fix the seed (4 min)
- [ ] Read raw data, not the cache (5 min)
- [ ] Check the findings table: status, check and limit (4 min)
- [ ] Choose the capstone dataset and write two questions (7 min)
- [ ] ✱ Stretch: Write the one line of a change log that says which numbers differ between two renders

#### [day4#wrap-up] Four habits to take home

*Day 4, and the course*

- **Ask first.** A question with a unit and a comparison, written before the chart.
- **Set it against something.** A unit, a denominator, a baseline, a mix.
- **Draw it honestly.** Position for what matters, scales that fit the mark, uncertainty on the chart.
- **Say how you know.** Chance checked, comparisons counted, status and limit stated, and it reruns.

#### [day4#next] Your report, your defence

*Capstone*

Tonight: read the data dictionary of your dataset and turn your two questions into a one-page plan.

- Do not open the data before the plan is written.
- Bring the repository with a first render that reruns, however short.

## Capstone: Capstone: the exploratory report and its defence

Each participant defends an exploratory report on an unseen dataset in eight minutes, and redraws one chart on request

#### [capstone#title] Capstone: the exploratory report and its defence

*SDAIA Academy · Exploratory Analysis and Visualisation*

Capstone: Each participant defends an exploratory report on an unseen dataset in eight minutes, and redraws one chart on request

Data Science Track · 4 teaching days + capstone day · 8 min talk and demo · DS-203

#### [capstone#agenda] How the day runs

*Capstone*

- **Expectations and final prep**: the rubric, the format of the defence, one last render from a clean run
- **Defences**: eight minutes each: five to present, three for the redraw and questions
- **Review and closing**: peer feedback, the trainer's review, the follow-up task

#### [capstone#what-you-submit] A public repository that a stranger can rerun

*The submission*

- **The plan.** Three to five questions with unit, variables and comparison, committed before the data was opened.
- **The report.** One source that reads the raw file, with parameters and a fixed seed at the top, and the page rendered from a clean run.
- **The README.** The named reader, the link to the report, and each finding with its status, its check and its limit.

> **Assistants are allowed today.** Charts and sentences written with one are marked in the notebook, and you defend them like the rest.

#### [capstone#rubric] The rubric

*How the repository is scored*

| Item | Value |
| --- | --- |
| Plan and questions | 15% |
| Analysis and charts | 30% |
| Honesty and uncertainty | 20% |
| Chance checks | 15% |
| Reproducibility and writing | 20% |

> **Full marks on honesty** go to the report that says what it does not know: intervals named, small groups handled, limits in the reader's words.

#### [capstone#format] 8 minutes for each defence

*Format*

- **1 · The reader and the questions.** Who the report is for and what it set out to answer. One minute.
- **2 · Findings, checks, limits.** Two or three findings with their charts, how each was checked, what stays open. Four minutes.
- **3 · The redraw.** The assessor names one chart and one change of encoding. You redraw it live and say what a reader would now conclude. Three minutes, with questions.

> **Peer feedback.** After each defence, everyone writes one strength, one question and one suggestion.

#### [capstone#running-order] Who presents when

*Running order*

| # | Presenter | Dataset |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first defence*

Render once more from a clean run, open the report on this screen, and have the notebook ready for the redraw.

#### [capstone#now-presenting] Report, redraw and questions

*Now presenting*

#### [capstone#review] What the defences showed

*Trainer review*

- **Strongest patterns.** What several reports got right: a plan that came first, a chart that drew its uncertainty, a limit stated plainly.
- **Common gaps.** What most reports would fix next: comparisons not counted, a rate without its denominator, a number typed by hand.
- **One surprise.** A redraw that changed what the room concluded.

#### [capstone#what-next] Keep going

*After the course*

- **The follow-up task:** within two weeks, an exploratory note on a dataset of the national Open Data Platform that touches your own work. The brief is in `labs/followup/README.md`.
- **Your report stays yours:** keep it rerunning, and test one of its exploratory findings when new data arrives.
- **Next Academy courses:** DS-205 Designing and Reading Experiments, for testing what exploration suggests; DS-207 Responsible Data Practice and Conduct in Analytical Work, for releasing tables of small groups.

#### [capstone#thanks] Thank you

*SDAIA Academy*

Exploratory Analysis and Visualisation
