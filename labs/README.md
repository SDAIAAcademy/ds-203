# Exploratory Analysis and Visualisation: labs

Sixteen 25-minute labs on the data of one fictional organisation, Tilal Regional Tourism Board, a pre-work notebook, the capstone brief and the follow-up task. All data is synthetic and generated with a fixed seed. No lab calls or downloads a model; everything runs on a laptop CPU or in Google Colab.

## Quick start

- **Google Colab:** open a notebook from the table below. Its first cell clones this repository and installs `requirements-colab.txt`.
- **Locally:** install [uv](https://docs.astral.sh/uv/), then from this folder:

```
uv sync
uv run jupyter lab
```

On Windows, start Jupyter with `PYTHONUTF8=1` set (PowerShell: `$env:PYTHONUTF8 = "1"`), so that the Arabic labels of lab 3.4 are read correctly.

Run `00_setup_check.ipynb` first. It imports the libraries, reads the six tables and draws one chart.

## The notebooks

| Unit | Session | Notebook |
|---|---|---|
| Before Day 1 | Setup check | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/00_setup_check.ipynb) |
| Before Day 1 | Pre-work · Dataframes and a first chart | [`P0_prework_dataframes_plotting.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/P0_prework_dataframes_plotting.ipynb) |
| Day 1 | Session 1 · Write the questions first | [`D1_1_brief_questions.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D1_1_brief_questions.ipynb) |
| Day 1 | Session 2 · Profiling a table | [`D1_2_profile_stays.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D1_2_profile_stays.ipynb) |
| Day 1 | Session 3 · Distributions | [`D1_3_length_of_stay.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D1_3_length_of_stay.ipynb) |
| Day 1 | Session 4 · Summaries that fit the shape | [`D1_4_centre_spread.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D1_4_centre_spread.ipynb) |
| Day 2 | Session 1 · Two variables at once | [`D2_1_occupancy_tickets.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D2_1_occupancy_tickets.ipynb) |
| Day 2 | Session 2 · Counts, rates and denominators | [`D2_2_complaint_rates.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D2_2_complaint_rates.ipynb) |
| Day 2 | Session 3 · Change over time | [`D2_3_monthly_arrivals.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D2_3_monthly_arrivals.ipynb) |
| Day 2 | Session 4 · When the total reverses | [`D2_4_satisfaction_reversal.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D2_4_satisfaction_reversal.ipynb) |
| Day 3 | Session 1 · Marks, encodings and scales | [`D3_1_chart_from_spec.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D3_1_chart_from_spec.ipynb) |
| Day 3 | Session 2 · Small multiples | [`D3_2_facet_arrivals.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D3_2_facet_arrivals.ipynb) |
| Day 3 | Session 3 · Charts that mislead | [`D3_3_repair_six_charts.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D3_3_repair_six_charts.ipynb) |
| Day 3 | Session 4 · Colour, labels and Arabic text | [`D3_4_bilingual_chart.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D3_4_bilingual_chart.ipynb) |
| Day 4 | Session 1 · Could it be chance | [`D4_1_chance_checks.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D4_1_chance_checks.ipynb) |
| Day 4 | Session 2 · Showing uncertainty | [`D4_2_intervals_caption.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D4_2_intervals_caption.ipynb) |
| Day 4 | Session 3 · The traps of exploring | [`D4_3_count_comparisons.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D4_3_count_comparisons.ipynb) |
| Day 4 | Session 4 · A report that reruns | [`D4_4_report_reruns.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-203/blob/main/labs/D4_4_report_reruns.ipynb) |
| Capstone | The brief, the rubric and three unseen datasets | [`capstone/README.md`](capstone/README.md) |
| After the course | The follow-up task | [`followup/README.md`](followup/README.md) |

## How a lab works

- Every lab starts from the **supplied tables**, read through the helper module `tilal.py` (`import tilal as U`). Nothing from an earlier notebook is needed, so a lab that was not finished does not block the next one.
- An exercise is a function to complete. Until it is written, the cells after it use the **reference result** from `data/reference/` and say so, so the notebook always runs to the end.
- Each exercise is followed by a check that prints ✅ or ❌ with a reason. Chart exercises are checked by reading the chart's specification, so different code that draws the same chart passes.
- Every lab ends with a written reading of two sentences: what the chart shows and what it does not. It is written without an assistant.
- The solutions are in `solutions/`, one notebook per lab, and `solutions/answer_key.md` lists what is planted in the data and which lab finds it.
- `DS203_QUICK=1` runs the resampling labs with fewer resamples. The trainer's run uses `DS203_STRICT=1`, which fails if a solution reaches a safety net.

## The data

| File in `data/` | One row is | Rows |
|---|---|---|
| `arrivals.csv` | one origin market in one month | 180 |
| `tickets.csv.gz` | one ticket sale at one site | 150,000 |
| `stays.csv.gz` | one visiting party's stay (raw export, with planted data issues) | 40,600 |
| `occupancy.csv.gz` | one hotel on one day | 43,840 |
| `survey.csv` | one visitor's survey response | 6,000 |
| `complaints.csv` | one complaint | 2,418 |

Also in `data/`: `brief.md` (the director's brief), `data_dictionary.json`, `labels.json` (Arabic and English texts for charts), `publication_rule.json` (the board's rule for small cells), `claims.json` and `past_findings.json` (Day 4).

`prepare_data.py` regenerates every file from seed 203 (`uv run python prepare_data.py`, about a minute). The board, its people, its hotels and its visitors are fictional.

## The tutor

`tutor_instruction.md` is the instruction for a tutoring assistant named Bawsala. Paste it into an assistant the Academy has approved. It hints one step at a time at plotting and dataframe syntax, and it does not write a chart or a reading for you.

## Editing the labs

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py` (`uv run python _tools/py2nb.py` from this folder), which also writes the solutions to `solutions/`. Edit the sources, not the notebooks. The reference results in `data/reference/` are written by running a source with `DS203_WRITE_REF=1`.
