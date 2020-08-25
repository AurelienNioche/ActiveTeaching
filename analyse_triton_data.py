import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from plot.subplot import chocolate, box, efficiency_cost, p_recall_error


# EXT = '_exp'
EXT = "_exp_omni_spec"

DATA_FOLDER = os.path.join("data", f"data{EXT}")
DATA_FILE = os.path.join("data", f"chocolate_triton{EXT}.csv")
FIG_CHOCOLATE_PATH = os.path.join("fig", f"chocolate_triton{EXT}.pdf")
FIG_BOXPLOT_PATH = os.path.join("fig", f"boxplot_triton{EXT}.pdf")

os.makedirs("data", exist_ok=True)


def preprocess_data():

    path, dirs, files = next(os.walk(DATA_FOLDER))
    file_count = len(files)

    row_list = []

    for i, p in tqdm(enumerate(os.scandir(DATA_FOLDER)), total=file_count):
        df = pd.read_csv(p.path, index_col=[0])

        # max_iter = max(df["iter"])
        # last_iter = df[df["iter"] == max_iter]
        # n_learnt = last_iter["n_learnt"].iloc[0]

        last_ss_idx = max(df["ss_idx"])

        n_learnt = df.query("ss_idx==@last_ss_idx & ss_iter==0")["n_learnt"].iloc[0]

        row = {
            "Agent ID": i,
            "Learner": df["md_learner"][0],
            "Psychologist": df["md_psy"][0],
            "Teacher": df["md_teacher"][0],
            "Items learnt": n_learnt,
        }
        row_list.append(row)

    df = pd.DataFrame(row_list)
    df.to_csv(DATA_FILE)
    return df


def main(force=True):

    if not os.path.exists(DATA_FILE) or force:
        df = preprocess_data()
    else:
        df = pd.read_csv(DATA_FILE, index_col=[0])

    print(type(df["Items learnt"][0]))

    teachers = sorted(np.unique(df["Teacher"]))
    learners = sorted(np.unique(df["Learner"]))
    psy = sorted(np.unique(df["Psychologist"]))

    chocolate.plot(
        df=df,
        teachers=teachers,
        learners=learners,
        psychologists=psy,
        fig_path=FIG_CHOCOLATE_PATH
    )

    box.plot(
        df=df,
        fig_path=FIG_BOXPLOT_PATH
    )


if __name__ == "__main__":
    main()