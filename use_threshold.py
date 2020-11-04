import datetime

import numpy as np
from tqdm import tqdm


def use_threshold(n_item, param, review_ts, eval_ts, thr,
                  eval_thr):

    is_item_specific = len(np.asarray(param).shape) > 1

    n_pres = np.zeros(n_item, dtype=int)
    last_pres = np.zeros(n_item)

    for i, ts in enumerate(review_ts):

        if np.max(n_pres) == 0:
            item = 0
        else:
            seen = n_pres > 0
            if is_item_specific:
                init_forget = param[seen, 0]
                rep_effect = param[seen, 1]
            else:
                init_forget, rep_effect = param

            log_p_seen = \
                -init_forget \
                * (1 - rep_effect) ** (n_pres[seen] - 1) \
                * (ts - last_pres[seen])

            if np.sum(seen) == n_item or np.min(log_p_seen) <= np.log(thr):
                item = np.flatnonzero(seen)[np.argmin(log_p_seen)]
            else:
                item = np.argmin(seen)

        n_pres[item] += 1
        last_pres[item] = ts

    seen = n_pres > 0
    if is_item_specific:
        init_forget = param[seen, 0]
        rep_effect = param[seen, 1]
    else:
        init_forget, rep_effect = param

    log_p_seen = \
        -init_forget \
        * (1 - rep_effect) ** (n_pres[seen] - 1) \
        * (eval_ts - last_pres[seen])

    n_learnt = np.sum(log_p_seen > np.log(eval_thr))
    print("threshold n learnt", n_learnt)
    print()


def main():

    np.random.seed(123)

    n_item = 50

    param = [[0.0006, 0.44] for _ in range(n_item)]
    param = np.asarray(param)

    ss_n_iter = 100
    time_per_iter = 4
    n_sec_day = 24 * 60 ** 2
    n_ss = 6
    eval_ts = n_ss * n_sec_day
    review_ts = np.hstack([
            np.arange(x, x + (ss_n_iter * time_per_iter), time_per_iter)
            for x in np.arange(0, n_sec_day * n_ss, n_sec_day)
        ])

    print(review_ts)
    print(eval_ts)

    thr = 0.90

    a = datetime.datetime.now()

    use_threshold(
        n_item=n_item, param=param, review_ts=review_ts,
        eval_ts=eval_ts, thr=thr, eval_thr=thr)

    print("[Time to execute ", datetime.datetime.now() - a, "]")


if __name__ == "__main__":
    main()