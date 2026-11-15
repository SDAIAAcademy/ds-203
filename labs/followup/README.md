# Follow-up task · An exploratory note on an open dataset

Due two weeks after the last day of the course. About four hours of work. The trainer records whether it was handed in and gives short written feedback; it carries no marks.

## The task

1. Choose one dataset from the national Open Data Platform (https://open.data.gov.sa) that touches your own work. Read its licence and its description before downloading. Take a dataset of aggregated or non-personal records only.
2. Write a plan of three questions in the form of lab 1.1 before you open the file: unit of observation, variables, comparison, exploratory or confirmatory.
3. Profile the table and log at least two data issues with their evidence and your decision.
4. Answer the three questions, each with one chart, one summary statistic and a two-sentence reading.
5. For one pattern, run a chance check by permutation or bootstrap and decide to report, qualify or drop it. Say how many comparisons you looked at before choosing that pattern.
6. Write a one-page note for a colleague who is not an analyst: the findings table (status, check, limit) and two open questions.

## What to hand in

A link to a repository, or a folder, with the plan, the notebook that reruns from the downloaded file with a fixed seed, and the rendered note. State the dataset's title, its publisher, the date you downloaded it and its licence at the top of the note.

## How it differs from the capstone

The data is real. Expect what synthetic data spares you: a dictionary that is incomplete, categories that changed over the years, totals that do not add up. Write these down as limits; do not repair them silently.

## A checklist before you send it

- [ ] The plan was committed before the first chart.
- [ ] Every rate shows its numerator and denominator.
- [ ] No bar or area starts above zero; every axis title is a phrase, not a column name.
- [ ] One chart shows its uncertainty and says what the interval is.
- [ ] The note uses "we saw" and "in this data", and no "proves" or "causes".
- [ ] A second run of the notebook gives the same numbers.
