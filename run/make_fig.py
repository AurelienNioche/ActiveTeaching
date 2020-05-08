import os

import numpy as np

from learner.learner import Learner

from plot.plot import DataFig, plot

SCRIPT_NAME = os.path.basename(__file__).split(".")[0]

FIG_FOLDER = os.path.join("fig", SCRIPT_NAME)
os.makedirs(FIG_FOLDER, exist_ok=True)


def make_fig(data, param_recovery, tk):

    n_obs = tk.terminal_t
    n_param = len(tk.param)

    n_iter = tk.n_iter
    n_iter_per_ss = tk.n_iter_per_ss
    n_iter_between_ss = tk.n_iter_between_ss

    training = np.zeros(tk.terminal_t, dtype=bool)
    training[:] = np.tile([1, ]*tk.n_iter_per_ss
                          + [0, ]*tk.n_iter_between_ss,
                          tk.n_ss)

    cond_labels = list(data.keys())
    cond_labels_param_recovery = list(param_recovery.keys()) \
        if param_recovery is not None else []

    data_fig = DataFig(cond_labels=cond_labels,
                       training=training, info=tk.info(), threshold=tk.thr,
                       exam=tk.terminal_t,
                       param=tk.param,
                       param_labels=tk.param_labels,
                       cond_labels_param_recovery=cond_labels_param_recovery)

    for i, cd in enumerate(cond_labels_param_recovery):
        hist = \
            {
                "post_mean": np.zeros((n_obs, n_param)),
                "post_std": np.zeros((n_obs, n_param))
            }
        c_iter_ss = 0
        for begin_ss in np.arange(0, n_iter, n_iter_per_ss):

            for key in hist.keys():
                split = \
                    param_recovery[cd][key][begin_ss:begin_ss+n_iter_per_ss]
                last = split[-1, :]
                t = c_iter_ss*(n_iter_per_ss+n_iter_between_ss)
                start, end = t, t + n_iter_per_ss
                hist[key][start: end] = split
                start, end = end, end+n_iter_between_ss
                hist[key][start: end] = last

            c_iter_ss += 1
        # for t, t_is_teaching in enumerate(training):
        #     if t_is_teaching:
        #         pm = parameter_recovery[cd]['post_mean'][c_iter, :]
        #         psd = parameter_recovery[cd]['post_std'][c_iter, :]
        #         c_iter += 1
        #     hist_pm[t] = pm
        #     hist_psd[t] = psd
        data_fig.add(
            post_mean=hist["post_mean"],
            post_std=hist["post_std"],
        )

    for i, cd in enumerate(cond_labels):

        hist = data[cd]

        seen_in_the_end = list(np.unique(hist))

        n_seen = np.zeros(n_obs, dtype=int)
        n_learnt = np.zeros(n_obs, dtype=int)
        p = [[] for _ in seen_in_the_end]

        it = 0

        learner = Learner.get(tk)

        for t in range(tk.terminal_t):

            t_is_teaching = training[t]

            seen = learner.seen
            sum_seen = np.sum(seen)

            n_seen[t] = sum_seen

            if sum_seen > 0:

                items_seen_at_t = np.arange(tk.n_item)[seen]
                p_at_t = learner.p_seen()

                for item, p_item in zip(items_seen_at_t, p_at_t):
                    idx_in_the_end = seen_in_the_end.index(item)
                    tup = (t, p_item)
                    p[idx_in_the_end].append(tup)

                n_learnt[t] = np.sum(p_at_t > tk.thr)

            item = None
            if t_is_teaching:
                item = hist[it]
                it += 1

            learner.update_one_step_only(item=item)

        data_fig.add(
            n_learnt=n_learnt,
            n_seen=n_seen,
            p=p,
        )

    plot(data=data_fig, fig_folder=FIG_FOLDER, fig_name=tk.extension)
