<!-- academy:title -->
# Exploratory Analysis and Visualisation

التحليل الاستكشافي وتصور البيانات

Data Science Track · SDAIA Academy · DS-203 · Level 200

Answer a director's questions from her own data: written questions first, charts that do not mislead, patterns checked against chance, and a report that reruns from raw data

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
| Capstone | Capstone: the exploratory report and its defence |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Tilal Regional Tourism Board.** Tilal Regional Tourism Board (مجلس تِلال الإقليمي للسياحة) is a fictional board of a highland region with nine visitor sites. Its director's brief is answered from three years of seeded synthetic data, 2023 to 2025: monthly arrivals by five origin markets, 150,000 ticket sales, 40,000 visitor stays, the daily occupancy of 40 hotels, 6,000 survey responses in Arabic and English and 2,418 complaints. The data holds what the sessions teach: entry errors in the stay register, a summer season, two festivals, a busiest site that is not the worst, satisfaction that falls overall while it rises in every origin market, and patterns that are only chance. Participants work as Leen Al-Suwayigh, the board's analyst; stays and hotels appear under pseudonymised keys and small groups are not published.

The hint-only tutor instruction of the course (`labs/tutor_instruction.md`) is for plotting and dataframe syntax. No lab calls a model, and the first draft of every chart reading is written with the assistant off.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Five questions from the brief | [`D1_1_brief_questions.ipynb`](labs/D1_1_brief_questions.ipynb) |
| 1.2 | Day 1 · Session 2 | Profile the stay register | [`D1_2_profile_stays.ipynb`](labs/D1_2_profile_stays.ipynb) |
| 1.3 | Day 1 · Session 3 | Length of stay by origin | [`D1_3_length_of_stay.ipynb`](labs/D1_3_length_of_stay.ipynb) |
| 1.4 | Day 1 · Session 4 | Centre and spread for four variables | [`D1_4_centre_spread.ipynb`](labs/D1_4_centre_spread.ipynb) |
| 2.1 | Day 2 · Session 1 | Occupancy against ticket sales | [`D2_1_occupancy_tickets.ipynb`](labs/D2_1_occupancy_tickets.ipynb) |
| 2.2 | Day 2 · Session 2 | Complaint rates and small cells | [`D2_2_complaint_rates.ipynb`](labs/D2_2_complaint_rates.ipynb) |
| 2.3 | Day 2 · Session 3 | Monthly arrivals, season and festivals | [`D2_3_monthly_arrivals.ipynb`](labs/D2_3_monthly_arrivals.ipynb) |
| 2.4 | Day 2 · Session 4 | The satisfaction reversal | [`D2_4_satisfaction_reversal.ipynb`](labs/D2_4_satisfaction_reversal.ipynb) |
| 3.1 | Day 3 · Session 1 | A chart from a written specification | [`D3_1_chart_from_spec.ipynb`](labs/D3_1_chart_from_spec.ipynb) |
| 3.2 | Day 3 · Session 2 | Arrivals in small multiples | [`D3_2_facet_arrivals.ipynb`](labs/D3_2_facet_arrivals.ipynb) |
| 3.3 | Day 3 · Session 3 | Repair six misleading charts | [`D3_3_repair_six_charts.ipynb`](labs/D3_3_repair_six_charts.ipynb) |
| 3.4 | Day 3 · Session 4 | One chart, two languages, safe colours | [`D3_4_bilingual_chart.ipynb`](labs/D3_4_bilingual_chart.ipynb) |
| 4.1 | Day 4 · Session 1 | Chance checks on two patterns | [`D4_1_chance_checks.ipynb`](labs/D4_1_chance_checks.ipynb) |
| 4.2 | Day 4 · Session 2 | Intervals on the satisfaction chart | [`D4_2_intervals_caption.ipynb`](labs/D4_2_intervals_caption.ipynb) |
| 4.3 | Day 4 · Session 3 | Count the comparisons | [`D4_3_count_comparisons.ipynb`](labs/D4_3_count_comparisons.ipynb) |
| 4.4 | Day 4 · Session 4 | A report that reruns | [`D4_4_report_reruns.ipynb`](labs/D4_4_report_reruns.ipynb) |
<!-- /academy:labs -->

## Capstone

An exploratory report on an unseen synthetic or approved public dataset, in a public repository whose README links the report and lists each finding with its check; eight-minute defence with one chart redrawn on request

**Submission:** A link to a public GitHub repository with a notebook that reruns from the raw data with a fixed seed, the rendered report for a named non-specialist reader, and a README that links the report and lists each finding with its check, its status (exploratory or confirmed) and its limit; charts and sentences written with an assistant are marked in the notebook. The commit history and a report rendered from a clean run are part of the evidence. Then an eight-minute live defence, in which the assessor asks for one chart to be redrawn with a different encoding and the participant says what a reader would now conclude.

**Assessment.** A supervised entry quiz and exit check without an assistant (20%), the capstone repository on the rubric (60%: plan and questions 15, analysis and charts 30, honesty and uncertainty 20, chance checks 15, reproducibility and writing 20) and the live defence with one chart redrawn on request (20%). Passing is 70% overall and at least 60% on both the capstone rubric and the supervised check. The supervised items are not in this repository.

**Pre-work and follow-up.** `labs/P0_prework_dataframes_plotting.ipynb` is two hours of dataframe and plotting practice before Day 1. The follow-up task, in `labs/followup/README.md`, is an exploratory note on a dataset of the national Open Data Platform within two weeks of the course.

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-104 SQL and Data Wrangling
- DS-201 Statistical Inference by Simulation
- Makes a basic chart in any plotting library
- Pre-work: about two hours of dataframe and plotting practice, `labs/P0_prework_dataframes_plotting.ipynb`, before the supervised entry quiz
- Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run `00_setup_check` before Day 1; see `labs/README.md`.

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
<!-- /academy:sources -->

### National references

- NDMO Open Data Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/OpenDataPolicy.pdf
- NDMO Data Classification Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf
- Personal Data Protection Law and its implementing regulations: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf and https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- SDAIA AI Ethics Principles: https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf
