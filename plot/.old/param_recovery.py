import numpy as np

from utils.brokenaxes import brokenaxes


def fig_parameter_recovery(
        fig, gs, xlims, pr,
        param_labels, cond_labels,
        timestamps,
        inferred_param,
        true_param, colors,
        background,
        time_per_iter):

    n_cond = len(cond_labels)

    if xlims is None:
        ax = fig.add_subplot(gs)
    else:
        ax = brokenaxes(fig=fig, subplot_spec=gs, xlims=xlims)

    for j in range(n_cond):

        i_pr = param_labels.index(pr)

        dt = cond_labels[j]
        means = inferred_param[j][:, i_pr]
        true_p = true_param[i_pr]

        ax.axhline(true_p, linestyle='--', color='black',
                   alpha=.2)

        ax.plot(timestamps[j], means, color=colors[j], label=dt)
        # ax.fill_between(range(len(means)),
        #                 means-stds,
        #                 means+stds, alpha=.2, color=colors[j])

        ax.set_title(pr)
        ax.set_xlabel("Time")
        ax.set_ylabel(f"Value")

    if xlims is None:
        y2, y1 = ax.get_ylim()
    else:
        y2, y1 = ax.get_ylim()[0]

    x = np.arange(0, background.size*time_per_iter, time_per_iter)
    ax.fill_between(x, y1, y2,
                    where=background == 1,
                    facecolor='whitesmoke',
                    edgecolor='lightgrey',
                    label='Training')
    ax.set_ylim(y2, y1)

    ax.legend(loc='upper right')


# def fig_parameter_recovery_heterogeneous(
#         param_labels, cond_labels, post_means,
#         true_param, axes=None,
#         fig_name=None, colors=None,
#         fig_folder=None):
#
#     n_param = len(param_labels)
#     n_cond = len(cond_labels)
#
#     if axes is None:
#         fig, axes = plt.subplots(ncols=n_param, figsize=(12, 6))
#
#     if colors is None:
#         colors = [f'C{i}' for i in range(n_cond)]
#
#     for idx_cond in range(n_cond):
#
#         cd = cond_labels[idx_cond]
#
#         pm_cond = post_means[idx_cond]
#         n_item = len(pm_cond)
#
#         # print("Cond", cd)
#         # print("*" * 40)
#
#         for item in range(n_item):
#
#             pm_cond_item = np.array(post_means[idx_cond][item]).T
#             # print(f"item {item}")
#             # print("-" * 40)
#
#             if pm_cond_item.size == 0:
#                 # print("skip")
#                 continue
#
#             x = np.asarray(pm_cond_item[0, :], dtype=int)
#             v = pm_cond_item[1:, :]
#             # print("x", x)
#
#             for idx_param in range(n_param):
#
#                 ax = axes[idx_param, idx_cond]
#
#                 true_pr = true_param[item, idx_param]
#
#                 y = v[idx_param]
#                 # print(f"recov pr {idx_param}: {y}")
#
#                 y = np.abs(true_pr-y)
#                 # print(f"error pr {idx_param}: {y}")
#
#                 ax.plot(
#                     x, y, color=colors[idx_cond],
#                     drawstyle="steps-post",
#                     alpha=0.5, linewidth=0.5, label=cd)
#
#                 handles, labels = ax.get_legend_handles_labels()
#                 by_label = dict(zip(labels, handles))
#                 ax.legend(by_label.values(), by_label.keys(),
#                           loc='upper right')
#
#                 ax.set_title(param_labels[idx_param])
#                 ax.set_xlabel("Time")
#                 ax.set_ylabel(f"Error")
#
#     if fig_name is not None and fig_folder is not None:
#         save_fig(fig_folder=fig_folder, fig_name=fig_name)