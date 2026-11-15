# Capstone · An exploratory report on a dataset you have not seen

The capstone is individual. You take **one dataset you have not seen**, explore it, and write an **exploratory report for a named reader who is not an analyst**. You publish the work in a **public repository** whose README links the rendered report and lists each finding with its check. Then you defend it in an **eight-minute live defence**, during which the assessor asks you to redraw one chart with a different encoding and to say what a reader would now conclude.

## The datasets

Choose one of the three in `data/`. Each is synthetic, was generated for this course and was not used in class. `datasets.json` holds the organisation, the reader and the meaning of every column.

| File | One row is | The reader |
|---|---|---|
| `data/ruwaq_museums.csv` | one visit to one of eight museums of the Ruwaq Museums Network | the network's head of programmes |
| `data/awan_parks.csv` | one maintenance request in one of eight parks of the Awan Parks Department | the head of park operations |
| `data/miqdam_driving.csv` | one driving test at one of eight branches of Miqdam Driving Schools | the schools' director of training |

You may use an approved public dataset in place of these, for example one from the national Open Data Platform, if the trainer agrees before the capstone day. It must hold no personal data, and its licence must allow publication of your charts.

Treat the data as its organisation would treat the real thing: no chart singles out one person, small groups are not published, and a rate travels with its denominator.

## Minimum requirements

1. **A plan written before the data is opened.** Three to five questions, each with its unit of observation, its variables and the comparison that answers it, in the form of lab 1.1. Commit it first: the commit history is part of the evidence.
2. **A profile of the table** with an issue log: what you found, the rows it concerns and what you decided.
3. **An answer to each question**: a chart, a summary statistic and a two-sentence reading (what it shows, what it does not).
4. **Honest charts**: scales that fit the mark, a title that states the finding, labels a reader understands, colour that is not the only carrier.
5. **At least one chance check** by permutation or bootstrap, with a decision to report, qualify or drop, and at least one chart that draws its uncertainty.
6. **A findings table** in the report and in the README: each finding with its status (exploratory or confirmed), its check and its limit, and a list of open questions.
7. **A report that reruns**: one notebook or script that reads the raw file, has its parameters and a fixed seed at the top, and renders the report with one command. Render it twice and say in the README that the two runs agree.

Charts and sentences written with an assistant are marked as such in the notebook. You will be asked about them.

## The repository

```
README.md            the reader, the findings table, the link to the report, how to rerun
plan.md              the plan, committed before the first look at the data
report.py or .ipynb  the one source of the report
report.html          the rendered report
data/                the raw file, unchanged
```

`labs/report/board_note.py` and `U.render_report` of lab 4.4 show one way to do this; any tool that gives one path from the raw data to the page is accepted.

## The defence · 8 minutes

| Minutes | What happens |
|---|---|
| 5 | You present: the reader and the questions, two or three findings with their charts, the checks, the limits and the open questions |
| 3 | The assessor names one of your charts and one change of encoding (for example: bars to points with intervals, colour to facets, a count to a rate). You redraw it live and say what a reader would now conclude. Questions follow in the time left |

## The rubric

| Criterion | Weight | Full marks look like |
|---|---|---|
| Plan and questions | 15% | Questions with unit, variables and comparison, committed before the data was opened; exploratory and confirmatory work told apart |
| Analysis and charts | 30% | Summaries and charts that suit each variable; relationships, time and mix examined; every chart readable and honest |
| Honesty and uncertainty | 20% | Intervals drawn and named; counts with denominators; small groups handled; limits stated in the reader's words |
| Chance checks | 15% | The right resampling for the pattern, on the right unit, with the comparisons counted and a reasoned decision |
| Reproducibility and writing | 20% | One command from raw data to report, two runs that agree, a findings table with status, check and limit, prose a non-specialist can follow |

## What is not asked

No model, no forecast, no dashboard, no causal claim. A short report that reruns and says what it does not know is worth more than a long one that does neither.
