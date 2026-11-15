# %% [markdown]
# # Setup check
#
# Run every cell once before Day 1. It imports the libraries the labs use, reads the six tables of Tilal Regional Tourism Board and draws one chart. Nothing here calls or downloads a model.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-203.git"
    if not Path("/content/ds-203").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-203"], check=True)
    os.chdir("/content/ds-203/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("tilal.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import tilal as U
alt = U.alt()
pd.set_option("display.width", 160)
print("mode:", U.MODE)

# %%
import importlib

missing = []
for name in ("numpy", "pandas", "scipy", "altair", "duckdb", "vl_convert", "nbconvert"):
    try:
        mod = importlib.import_module(name)
        print(f"✅ {name} {getattr(mod, '__version__', '')}")
    except ImportError:
        missing.append(name)
        print(f"❌ {name} is missing")

# %%
counts = {"arrivals": len(U.arrivals()), "tickets": len(U.tickets()), "stays": len(U.stays()), "occupancy": len(U.occupancy()),
          "survey": len(U.survey()), "complaints": len(U.complaints())}
print(counts)
U.check(counts == {"arrivals": 180, "tickets": 150_000, "stays": 40_000, "occupancy": 43_840, "survey": 6_000, "complaints": 2_418},
        "the six tables are complete")

# %%
m = U.monthly_total()
chart = alt.Chart(m).mark_line().encode(x=alt.X("month:T", title=None), y=alt.Y("arrivals:Q", title="Arrivals per month")).properties(title="If you see a line with three summer peaks, charts work")
U.check(U.marks(chart) == {"line"} and len(m) == 36, "a chart of 36 months was built")
U.show(chart)

# %%
if missing:
    print("Missing:", ", ".join(missing), "· locally run `uv sync` in labs/; in Colab rerun the first cell.")
else:
    print("Ready for Day 1.")
