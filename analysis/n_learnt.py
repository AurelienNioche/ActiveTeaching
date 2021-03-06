import os

import pandas as pd


def row_for_single_run(csv_path):

    df = pd.read_csv(csv_path, index_col=[0])

    agent_id = df["agent"].iloc[0]

    last_iter = max(df["iter"])
    is_last_iter = df["iter"] == last_iter

    n_learnt = df[is_last_iter]["n_learnt"].iloc[0]
    n_seen = df[is_last_iter]["n_seen"].iloc[0]

    is_last_ss = df["ss_idx"] == max(df["ss_idx"]) - 1

    ss_n_iter = df["ss_n_iter"][0] - 1

    is_last_iter_ss = df["ss_iter"] == ss_n_iter

    n_learnt_end_ss = df[is_last_ss & is_last_iter_ss]["n_learnt"].iloc[0]

    return {
        "agent": agent_id,
        "learner": df["md_learner"][0],
        "psy": df["md_psy"][0],
        "teacher": df["md_teacher"][0],
        "n_learnt": n_learnt,
        "n_learnt_end_ss": n_learnt_end_ss,
        "n_seen": n_seen,
        "ratio_n_learnt_n_seen": n_learnt / n_seen
    }


def preprocess_cond(cond_data_folder, preprocess_data_file):

    teach_f = [
        p for p in os.scandir(cond_data_folder) if not p.name.startswith(".")
    ]

    row_list = []

    for j, tp in enumerate(teach_f):
        print("teacher data folder:", tp.name)

        csv_files = [p for p in os.scandir(tp.path) if p.name.endswith("csv")]

        for k, csv_file in enumerate(csv_files):
            row = row_for_single_run(csv_file.path)
            row_list.append(row)

    print("*" * 100)

    os.makedirs(os.path.dirname(preprocess_data_file), exist_ok=True)

    df = pd.DataFrame(row_list)
    df.to_csv(preprocess_data_file)
    return df


def get_data(dataset_name, condition_name, force=False):

    preprocess_folder = os.path.join("data", "preprocessed", dataset_name)
    os.makedirs(preprocess_folder, exist_ok=True)

    pp_data_file = os.path.join(preprocess_folder, f"{condition_name}.csv")

    if not os.path.exists(pp_data_file) or force:
        cond_data_folder = os.path.join("data", "triton",
                                        dataset_name, condition_name)
        df = preprocess_cond(cond_data_folder=cond_data_folder,
                             preprocess_data_file=pp_data_file)
    else:
        df = pd.read_csv(pp_data_file, index_col=[0])

    return df
