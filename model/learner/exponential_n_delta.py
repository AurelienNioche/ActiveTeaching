import numpy as np
from . generic import Learner

EPS = np.finfo(np.float).eps


class ExponentialNDelta(Learner):

    def __init__(self, n_item):

        self.n_pres = np.zeros(n_item, dtype=int)
        self.last_pres = np.zeros(n_item, dtype=int)

    def p_seen(self, param, is_item_specific, now):

        seen = self.n_pres >= 1
        if np.sum(seen) == 0:
            return None, []

        if is_item_specific:
            init_forget = param[seen, 0]
            rep_effect = param[seen, 1]
        else:
            init_forget, rep_effect = param

        fr = init_forget * (1 - rep_effect) ** (self.n_pres[seen] - 1)
        # if delta is None:
        last_pres = self.last_pres[seen]
        delta = now - last_pres
        # else:
        #     delta = delta[seen]
        p = np.exp(-fr * delta)
        return p, seen

    def log_lik_grid(self, item, grid_param, response, timestamp):

        fr = grid_param[:, 0] \
             * (1 - grid_param[:, 1]) ** (self.n_pres[item] - 1)

        delta = timestamp - self.last_pres[item]
        p_success = np.exp(- fr * delta)

        p = p_success if response else 1-p_success

        log_lik = np.log(p + EPS)
        return log_lik

    @classmethod
    def log_lik(cls, param, hist, success, timestamp):
        a, b = param

        log_p_hist = np.zeros(len(hist))

        for item in np.unique(hist):

            is_item = hist == item
            rep = timestamp[is_item]
            n = len(rep)

            log_p_item = np.zeros(n)
            # !!! To adapt for xp
            log_p_item[0] = -np.inf  # whatever the model, p=0
            # !!! To adapt for xp
            for i in range(1, n):
                delta_rep = rep[i] - rep[i-1]
                fr = a * (1 - b) ** (i - 1)
                log_p_item[i] = -fr * delta_rep

            log_p_hist[is_item] = log_p_item
        p_hist = np.exp(log_p_hist)
        failure = np.invert(success)
        p_hist[failure] = 1 - p_hist[failure]
        log_lik = np.log(p_hist + EPS)
        sum_ll = log_lik.sum()
        return sum_ll

    def p(self, item, param, now, is_item_specific):

        if is_item_specific:
            init_forget = param[item, 0]
            rep_effect = param[item, 1]
        else:
            init_forget, rep_effect = param

        fr = init_forget * (1 - rep_effect) ** (self.n_pres[item] - 1)

        delta = now - self.last_pres[item]
        return np.exp(- fr * delta)

    def update(self, item, timestamp):

        self.last_pres[item] = timestamp
        self.n_pres[item] += 1