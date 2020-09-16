import os
import pandas as pd

from plot.subplot import box, chocolate, hist


def row_for_single_run(csv_path):

    df = pd.read_csv(csv_path, index_col=[0])

    agent_id = df["agent"].iloc[0]

    last_iter = max(df["iter"])
    is_last_iter = df["iter"] == last_iter

    n_learnt = df[is_last_iter]["n_learnt"].iloc[0]

    is_last_ss = df["ss_idx"] == max(df["ss_idx"]) - 1

    ss_n_iter = df["ss_n_iter"][0] - 1

    is_last_iter_ss = df["ss_iter"] == ss_n_iter

    n_learnt_end_ss = df[is_last_ss & is_last_iter_ss]["n_learnt"].iloc[0]

    return {
        "Agent ID": agent_id,
        "Learner": df["md_learner"][0],
        "Psychologist": df["md_psy"][0],
        "Teacher": df["md_teacher"][0],
        "Items learnt one day later": n_learnt,
        "Items learnt end last session": n_learnt_end_ss}


def preprocess_cond(cond_data_folder, preprocess_data_file):

    teach_f = [p for p in os.scandir(cond_data_folder.path)
               if not p.name.startswith(".")]

    row_list = []

    for j, tp in enumerate(teach_f):
        print("teacher data folder", tp.name)

        csv_files = \
            [p for p in os.scandir(tp.path)
             if p.name.endswith("csv")]

        for k, csv_file in enumerate(csv_files):
            row = row_for_single_run(csv_file.path)
            row_list.append(row)

    print("*" * 100)

    df = pd.DataFrame(row_list)
    df.to_csv(preprocess_data_file)
    return df


def main(force=False, fig_folder="fig"):

    root_data_folder = os.path.join("data", "triton")
    assert os.path.exists(root_data_folder)

    cond_f = [p for p in os.scandir(root_data_folder)
              if not p.name.startswith(".")]

    for i, cp in enumerate(cond_f):
        print("cond data folder", cp.name)

        pp_data_file = os.path.join(
            "data",
            "preprocessed",
            f"{cp.name}-here-i-am.csv")

        if not os.path.exists(pp_data_file) or force:
            df = preprocess_cond(cond_data_folder=cp,
                                 preprocess_data_file=pp_data_file)
        else:
            df = pd.read_csv(pp_data_file, index_col=[0])

        for v in ("Items learnt one day later",
                  "Items learnt end last session"):

            lab = v.replace("Items learnt", "").replace(" ", "-")

            fig_path = os.path.join(fig_folder, f"{ cp.name}_box_{lab}_here-i-am.pdf")
            box.plot(df=df, fig_path=fig_path, learnt_label=v)

            fig_path = os.path.join(fig_folder, f"{cp.name}_hist_here-i-am.pdf")
            hist.plot(learnt_label=v, df=df, fig_path=fig_path)


if __name__ == "__main__":
    main()
