import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

FILE_DELIMITER = '\t'

advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
data_folder = '../data/'
result_folder = '../results/evaluation/'

group_files = ['train.wzb.imp.txt', 'train.wzb.lose.txt', 'train.yzx.bid.txt',
               'test.yzx.win.txt', 'test.yzx.lose.txt', 'test.yzx.bid.txt']

group = ['train_win', 'train_lose', 'train_full', 'test_win', 'test_lose', 'test_full']

for i in range(0, 6):
    j = 1
    for adv in advs:
        adv_arr = []
        file = data_folder + adv + '/' + group_files[i]
        f = open(file, 'r')
        for line in f:
            data = line.rstrip('\r\n').split()
            if len(data) > 1:
                adv_arr.append(float(data[1]))
        X = np.array(adv_arr)
        n = X.size
        X_mean = np.mean(X)
        X_std = np.std(X)
        X_se = X_std / np.sqrt(n)
        dof = n - 1
        alpha = 1.0 - 0.95
        conf_interval = t.ppf(1 - alpha / 2., dof) * X_std * np.sqrt(1. + 1. / n)

        plt.errorbar(j, X_mean, yerr=X_std, fmt='-o')
        j += 1
    fig = plt.gca()
    # fig.axes.get_xaxis().set_visible(False)
    fig.spines["top"].set_visible(False)
    fig.spines["right"].set_visible(False)
    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                    labelbottom="on", left="on", right="off", labelleft="on")
    plt.xticks(range(1, 11), advs)
    # plt.ylim(X_mean - conf_interval - 2, X_mean + conf_interval + 2)
    plt.ylim([-50, 300])
    plt.xlim([0, 11])
    plt.xlabel('campaign')
    plt.ylabel('market price')
    plt.title(group[i] + '_data')
    plt.savefig(result_folder + 'mp_statistic_' + group[i] + '.png')
    plt.close()