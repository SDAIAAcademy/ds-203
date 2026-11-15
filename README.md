<!-- academy:title -->
# Exploratory Analysis and Visualisation

التحليل الاستكشافي وتصور البيانات

Data Science Track · SDAIA Academy · DS-203 · Level 200

REPLACE: one line under the title: what participants can do after the course

Participants answer a fictional regional tourism board's questions by exploring its data, starting every analysis from written questions. They profile tables, examine distributions, relationships and change over time, build charts with a grammar of graphics and scales that do not mislead, and test by resampling whether a pattern could be chance. They repair misleading charts and write findings that state what is and is not shown, in a notebook that reruns from raw data.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-203/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Distinguish exploratory from confirmatory analysis and explain why a pattern found by exploring needs a fresh test, given five findings from a past board report | Awareness | each finding marked exploratory or confirmed, with the check it would need |
| LO2 | Prepare an analysis plan listing questions, units of observation, variables and the comparison that answers each, given the director's brief and the data dictionary | Applied | a one-page plan checked against a checklist before any chart is drawn |
| LO3 | Analyse distributions, relationships and change over time with summaries and charts suited to each variable type, given three years of visitor, occupancy and survey tables | Applied | a chart, a summary statistic and a two-sentence reading per question |
| LO4 | Use a grammar of graphics to map variables to position, colour and facets with honest scales, baselines and labels, given six misleading charts from earlier reports | Applied | six repaired charts, each with the fault and the fix named |
| LO5 | Test whether an apparent difference or correlation could arise by chance, using permutation or bootstrap resampling, given three patterns the board wants to announce | Applied | each pattern's resampling result and a decision to report, qualify or drop it |
| LO6 | Deliver a reproducible exploratory report that states findings, uncertainty, open questions and limits for a non-specialist reader, given an unseen dataset and a named audience | Performance | a rendered report and notebook that rerun from raw data, defended live |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Questions and first looks | Write the questions first; Profiling a table; Distributions; Summaries that fit the shape | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Relationships and time | Two variables at once; Counts, rates and denominators; Change over time; When the total reverses | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Building honest charts | Marks, encodings and scales; Small multiples; Charts that mislead; Colour, labels and Arabic text | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Check and report | Could it be chance; Showing uncertainty; The traps of exploring; A report that reruns | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Turn the director's brief into five questions with unit and comparison | [`D1_1_turn_director_s.ipynb`](labs/D1_1_turn_director_s.ipynb) |
| 1.2 | Day 1 · Session 2 | Profile the visitor table and log three data issues | [`D1_2_profile_visitor_table.ipynb`](labs/D1_2_profile_visitor_table.ipynb) |
| 1.3 | Day 1 · Session 3 | Compare length of stay by visitor origin with histograms and box plots | [`D1_3_compare_length_stay.ipynb`](labs/D1_3_compare_length_stay.ipynb) |
| 1.4 | Day 1 · Session 4 | Choose centre and spread measures for four skewed variables | [`D1_4_choose_centre_spread.ipynb`](labs/D1_4_choose_centre_spread.ipynb) |
| 2.1 | Day 2 · Session 1 | Plot occupancy against ticket sales with transparency and binning | [`D2_1_plot_occupancy_against.ipynb`](labs/D2_1_plot_occupancy_against.ipynb) |
| 2.2 | Day 2 · Session 2 | Convert complaints to rates per thousand visitors; mark cells too small to publish | [`D2_2_convert_complaints_rates.ipynb`](labs/D2_2_convert_complaints_rates.ipynb) |
| 2.3 | Day 2 · Session 3 | Plot monthly arrivals and mark seasonality and two festival effects | [`D2_3_plot_monthly_arrivals.ipynb`](labs/D2_3_plot_monthly_arrivals.ipynb) |
| 2.4 | Day 2 · Session 4 | Find the satisfaction reversal once visitor origin is taken into account | [`D2_4_find_satisfaction_reversal.ipynb`](labs/D2_4_find_satisfaction_reversal.ipynb) |
| 3.1 | Day 3 · Session 1 | Rebuild one chart from a written specification | [`D3_1_rebuild_one_chart.ipynb`](labs/D3_1_rebuild_one_chart.ipynb) |
| 3.2 | Day 3 · Session 2 | Facet arrivals by origin market; choose shared or free scales | [`D3_2_facet_arrivals_origin.ipynb`](labs/D3_2_facet_arrivals_origin.ipynb) |
| 3.3 | Day 3 · Session 3 | Repair six misleading charts and name each fault | [`D3_3_repair_six_misleading.ipynb`](labs/D3_3_repair_six_misleading.ipynb) |
| 3.4 | Day 3 · Session 4 | Make one chart readable in Arabic and English and colour-blind safe | [`D3_4_make_one_chart.ipynb`](labs/D3_4_make_one_chart.ipynb) |
| 4.1 | Day 4 · Session 1 | Permutation-test the claimed weekend effect; bootstrap one correlation | [`D4_1_permutation_test_claimed.ipynb`](labs/D4_1_permutation_test_claimed.ipynb) |
| 4.2 | Day 4 · Session 2 | Add intervals to a satisfaction bar chart and rewrite its caption | [`D4_2_add_intervals_satisfaction.ipynb`](labs/D4_2_add_intervals_satisfaction.ipynb) |
| 4.3 | Day 4 · Session 3 | Count the comparisons behind a headline pattern and rewrite the finding | [`D4_3_count_comparisons_behind.ipynb`](labs/D4_3_count_comparisons_behind.ipynb) |
| 4.4 | Day 4 · Session 4 | Render a notebook to a report from raw data; choose the capstone dataset | [`D4_4_render_notebook_report.ipynb`](labs/D4_4_render_notebook_report.ipynb) |
<!-- /academy:labs -->

## Capstone

An exploratory report on an unseen synthetic or approved public dataset, in a public repository whose README links the report and lists each finding with its check; eight-minute defence with one chart redrawn on request

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-104 SQL and Data Wrangling
- DS-201 Statistical Inference by Simulation
- Makes a basic chart in any plotting library

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Analysis environment and notebooks:** Python with uv and JupyterLab or marimo, R with Quarto
- **Dataframes and analytical SQL engine:** DuckDB, Polars, pandas
- **Plotting with a grammar of graphics:** Vega-Altair, plotnine, ggplot2
- **Resampling:** NumPy and SciPy, R with the infer package
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- NDMO Open Data Policy: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
