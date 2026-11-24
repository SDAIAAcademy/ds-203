---
course: "Exploratory Analysis and Visualisation"
code: "DS-203"
version: "2027.2.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-203/slides/day1.html"
---

# Exploratory Analysis and Visualisation

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
