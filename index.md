---
course: "Exploratory Analysis and Visualisation"
code: "DS-203"
version: "2027.2.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-203/index.html"
---

# Exploratory Analysis and Visualisation

التحليل الاستكشافي والتمثيل المرئي للبيانات

Data Science Track · 4 teaching days + capstone day · 26 hours · Level 200

Answer a director's questions from her own data: written questions first, charts that do not mislead, patterns checked against chance, and a report that reruns from raw data

Participants answer a fictional regional tourism board's questions by exploring its data, starting every analysis from written questions. They profile tables, examine distributions, relationships and change over time, build charts with a grammar of graphics and scales that do not mislead, and test by resampling whether a pattern could be chance. They repair misleading charts and write findings that state what is and is not shown, in a notebook that reruns from raw data.

**Who it is for:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Tilal Regional Tourism Board.** Tilal Regional Tourism Board (مجلس تِلال الإقليمي للسياحة) is a fictional board of a highland region with nine visitor sites. Its director's brief is answered from three years of seeded synthetic data, 2023 to 2025: monthly arrivals by five origin markets, 150,000 ticket sales, 40,000 visitor stays, the daily occupancy of 40 hotels, 6,000 survey responses in Arabic and English and 2,418 complaints. The data holds what the sessions teach: entry errors in the stay register, a summer season, two festivals, a busiest site that is not the worst, satisfaction that falls overall while it rises in every origin market, and patterns that are only chance. Participants work as Leen Al-Suwayigh, the board's analyst; stays and hotels appear under pseudonymised keys and small groups are not published.

## The course

### Day 1: Questions and first looks

Slides: https://sdaiaacademy.github.io/ds-203/slides/day1.md

- **Session 1: Write the questions first**
  - Rewrite a vague request as a question with a unit, variables and a comparison
  - Name the unit of observation of each table before joining or counting
  - Distinguish an exploratory question from a confirmatory one
  - [Lab 1.1: Five questions from the brief (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D1_1_brief_questions.ipynb)
- **Session 2: Profiling a table**
  - Test whether a table has the grain and the key its dictionary claims
  - Locate missing values and impossible values, and say whom they affect
  - Record each data issue with its evidence and a decision
  - [Lab 1.2: Profile the stay register (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D1_2_profile_stays.ipynb)
- **Session 3: Distributions**
  - Draw a histogram with a bin width that suits the variable
  - Compare groups of unequal size by shares on a common scale
  - Recognise a distribution with two humps that a box plot hides
  - [Lab 1.3: Length of stay by origin (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D1_3_length_of_stay.ipynb)
- **Session 4: Summaries that fit the shape**
  - Predict from mean and median which way a variable is skewed
  - Choose a centre and a spread that the tail does not move
  - Summarise a zero-heavy variable and a score without a single mean
  - [Lab 1.4: Centre and spread for four variables (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D1_4_centre_spread.ipynb)

### Day 2: Relationships and time

Slides: https://sdaiaacademy.github.io/ds-203/slides/day2.md

- **Session 1: Two variables at once**
  - Bring two tables to one unit of observation before relating them
  - Reveal a relation in an overplotted scatter with transparency and binning
  - Explain why a correlation changes with the unit it is computed on
  - [Lab 2.1: Occupancy against ticket sales (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D2_1_occupancy_tickets.ipynb)
- **Session 2: Counts, rates and denominators**
  - Convert counts to rates with a denominator that fits the question
  - Compare a ranking by count with a ranking by rate
  - Colour a map by a rate on its exposure, not by a count
  - Mark the cells of a table that a publication rule holds back
  - [Lab 2.2: Complaint rates and small cells (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D2_2_complaint_rates.ipynb)
- **Session 3: Change over time**
  - Draw a time series so that season and trend can be told apart
  - Compare a month with the same month a year earlier and with a seasonal baseline
  - Mark the months that exceed the baseline and say by how much
  - [Lab 2.3: Monthly arrivals, season and festivals (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D2_3_monthly_arrivals.ipynb)
- **Session 4: When the total reverses**
  - Split a total into what each group does and how large each group is
  - Detect a reversal between a total and its groups
  - Report a comparison at a fixed mix
  - [Lab 2.4: The satisfaction reversal (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D2_4_satisfaction_reversal.ipynb)

### Day 3: Building honest charts

Slides: https://sdaiaacademy.github.io/ds-203/slides/day3.md

- **Session 1: Marks, encodings and scales**
  - Describe any chart as data, marks, encodings and scales
  - Rank position, length, area and colour by how precisely they are read
  - Build a layered chart from a written specification
  - [Lab 3.1: A chart from a written specification (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D3_1_chart_from_spec.ipynb)
- **Session 2: Small multiples**
  - Replace a crowded chart with small multiples
  - Choose shared scales to compare levels and free scales to compare shapes
  - State the scale choice on the chart
  - [Lab 3.2: Arrivals in small multiples (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D3_2_facet_arrivals.ipynb)
- **Session 3: Charts that mislead**
  - Name the fault of a misleading chart
  - Repair a chart by changing its scale, window, measure or encoding
  - Say what a reader concludes before and after the repair
  - [Lab 3.3: Repair six misleading charts (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D3_3_repair_six_charts.ipynb)
- **Session 4: Colour, labels and Arabic text**
  - Choose a palette by the type of variable and test it for colour-vision deficiency
  - Add a second channel so that colour is never the only carrier
  - Produce one chart in Arabic and in English from the same code
  - [Lab 3.4: One chart, two languages, safe colours (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D3_4_bilingual_chart.ipynb)

### Day 4: Check and report

Slides: https://sdaiaacademy.github.io/ds-203/slides/day4.md

- **Session 1: Could it be chance**
  - Choose shuffling for a gap between groups and resampling for an interval
  - Resample the unit that was sampled, here the week
  - Decide to report, qualify or drop a pattern and give the reason
  - [Lab 4.1: Chance checks on two patterns (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D4_1_chance_checks.ipynb)
- **Session 2: Showing uncertainty**
  - Add an interval to every estimate on a chart
  - Read overlapping and separate intervals without overclaiming
  - Write a caption that names the interval, the sample size and the limit
  - [Lab 4.2: Intervals on the satisfaction chart (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D4_2_intervals_caption.ipynb)
- **Session 3: The traps of exploring**
  - Count the comparisons behind a reported pattern
  - Simulate the most striking gap that chance alone produces among that many comparisons
  - Mark a finding exploratory or confirmed and name the check it needs
  - [Lab 4.3: Count the comparisons (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D4_3_count_comparisons.ipynb)
- **Session 4: A report that reruns**
  - Render a report from raw data with one command and prove that two runs agree
  - Find what makes a report change between runs
  - Write findings with their check, their limit and an open question
  - [Lab 4.4: A report that reruns (25 min)](https://sdaiaacademy.github.io/ds-203/labs/D4_4_report_reruns.ipynb)

### Capstone: Capstone: the exploratory report and its defence

Slides: https://sdaiaacademy.github.io/ds-203/slides/capstone.md

## Capstone

An exploratory report on an unseen synthetic or approved public dataset, in a public repository whose README links the report and lists each finding with its check; eight-minute defence with one chart redrawn on request

**What you submit:** A link to a public GitHub repository with a notebook that reruns from the raw data with a fixed seed, the rendered report for a named non-specialist reader, and a README that links the report and lists each finding with its check, its status (exploratory or confirmed) and its limit; charts and sentences written with an assistant are marked in the notebook. The commit history and a report rendered from a clean run are part of the evidence. Then an eight-minute live defence, in which the assessor asks for one chart to be redrawn with a different encoding and the participant says what a reader would now conclude.

**Rubric:**

- Plan and questions: 15%
- Analysis and charts: 30%
- Honesty and uncertainty: 20%
- Chance checks: 15%
- Reproducibility and writing: 20%

## Outcomes

- **LO1** Distinguish exploratory from confirmatory analysis and explain why a pattern found by exploring needs a fresh test, given five findings from a past board report (Awareness) Evidence: each finding marked exploratory or confirmed, with the check it would need
- **LO2** Prepare an analysis plan listing questions, units of observation, variables and the comparison that answers each, given the director's brief and the data dictionary (Applied) Evidence: a one-page plan checked against a checklist before any chart is drawn
- **LO3** Analyse distributions, relationships and change over time with summaries and charts suited to each variable type, given three years of visitor, occupancy and survey tables (Applied) Evidence: a chart, a summary statistic and a two-sentence reading per question
- **LO4** Use a grammar of graphics to map variables to position, colour and facets with honest scales, baselines and labels, given six misleading charts from earlier reports (Applied) Evidence: six repaired charts, each with the fault and the fix named
- **LO5** Test whether an apparent difference or correlation could arise by chance, using permutation or bootstrap resampling, given three patterns the board wants to announce (Applied) Evidence: each pattern's resampling result and a decision to report, qualify or drop it
- **LO6** Deliver a reproducible exploratory report that states findings, uncertainty, open questions and limits for a non-specialist reader, given an unseen dataset and a named audience (Performance) Evidence: a rendered report and notebook that rerun from raw data, defended live

## Tools

- **Analysis environment and notebooks:** Python with uv and JupyterLab or marimo, R with Quarto
- **Dataframes and analytical SQL engine:** DuckDB, Polars, pandas
- **Plotting with a grammar of graphics:** Vega-Altair, plotnine, ggplot2
- **Resampling:** NumPy and SciPy, R with the infer package

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-104 SQL and Data Wrangling
- DS-201 Statistical Inference by Simulation
- Makes a basic chart in any plotting library
- Pre-work: about two hours of dataframe and plotting practice, labs/P0_prework_dataframes_plotting.ipynb, before the supervised entry quiz
- Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.

## Sources

### National references

- [Open Data Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/OpenDataPolicy.pdf)
- [Data Classification Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Principles of AI Ethics (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [Open Data Platform (the follow-up task takes one of its datasets)](https://open.data.gov.sa/en/home)

### Libraries used in the labs

- [Vega-Altair: encodings, marks and data types](https://altair-viz.github.io/user_guide/encodings/index.html)
- [Vega-Altair: layered, faceted and concatenated charts](https://altair-viz.github.io/user_guide/compound_charts.html)
- [Vega-Altair: scale and guide resolution (shared and independent scales)](https://altair-viz.github.io/user_guide/scale_resolve.html)
- [Vega-Altair: large datasets](https://altair-viz.github.io/user_guide/large_datasets.html)
- [Vega-Lite: scales](https://vega.github.io/vega-lite/docs/scale.html)
- [DuckDB: the SUMMARIZE statement](https://duckdb.org/docs/stable/guides/meta/summarize)
- [SciPy: scipy.stats.bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
- [SciPy: scipy.stats.permutation_test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
- [nbconvert: executing notebooks](https://nbconvert.readthedocs.io/en/latest/execute_api.html)
- [plotnine, a grammar of graphics for Python (an interchangeable example)](https://plotnine.org/)
- [Quarto: computations in Python (an interchangeable example for reports)](https://quarto.org/docs/computations/python.html)

### Charts, colour and text direction

- [Wilkinson: The Grammar of Graphics, second edition (Springer, 2005)](https://link.springer.com/book/10.1007/0-387-28695-0)
- [Wickham (2010): A layered grammar of graphics](https://vita.had.co.nz/papers/layered-grammar.html)
- [Cleveland and McGill (1984): Graphical perception: theory, experimentation, and application to the development of graphical methods](https://www.jstor.org/stable/2288400)
- [Wilke: Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)
- [Healy: Data Visualization, a practical introduction](https://socviz.co/)
- [Okabe and Ito: Color Universal Design, how to make figures that are friendly to colour-blind people](https://jfly.uni-koeln.de/color/)
- [Machado, Oliveira and Fernandes (2009): A physiologically-based model for simulation of color vision deficiency](https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html)
- [W3C Internationalization: structural markup and right-to-left text](https://www.w3.org/International/questions/qa-html-dir)

### Exploring and checking

- [Wickham, Çetinkaya-Rundel and Grolemund: R for Data Science, second edition, exploratory data analysis](https://r4ds.hadley.nz/EDA.html)
- [Gelman and Loken (2013): The garden of forking paths](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)
- [Ismay, Kim and Valdivia: Statistical Inference via Data Science (ModernDive)](https://moderndive.com/)

---

SDAIA Academy · Data Science Track · Exploratory Analysis and Visualisation

Course version 2027.2.0 · engine 1.0.0 · built 2026-11-24 · commit 275c4e8
