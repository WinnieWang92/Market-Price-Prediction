
import numpy as np
import matplotlib.pyplot as plt



def fs(s):
    res = []
    res.append(s[0])
    for i in range(1, len(s)):
        res.append(float(s[i]))
    return res

advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
settings = ['bias', 'uimp', 'kimp', 'bid']
head = '../results/evaluation/rmse.eval.'

eval_bias = head + settings[0] + '.txt'
eval_uimp = head + settings[1] + '.txt'
eval_kimp = head + settings[2] + '.txt'
eval_bid = head + settings[3] + '.txt'
eval_list = [eval_bias, eval_uimp, eval_kimp, eval_bid]

adv_eval = {}
# for eval_file in eval_list:
fi1 = open(eval_bias, 'r')
fi2 = open(eval_uimp, 'r')
fi3 = open(eval_kimp, 'r')
fi4 = open(eval_bid, 'r')
line_num = 0
for line1 in fi1:
    line2 = fi2.readline()
    line3 = fi3.readline()
    line4 = fi4.readline()
    if line_num != 0:
        s1 = fs(line1.strip().split())
        s2 = fs(line2.strip().split())
        s3 = fs(line3.strip().split())
        s4 = fs(line4.strip().split())

        adv = s1[0]

        adv_eval[adv] = {}
        adv_eval[adv]['bias'] = s1[1:4]
        adv_eval[adv]['uimp'] = s2[1:4]
        adv_eval[adv]['kimp'] = s3[1:4]
        adv_eval[adv]['bid'] = s4[1:4]
    line_num += 1
fi1.close()
fi2.close()
fi3.close()
fi4.close()

for adv in advs:
    n_groups = 3

    rmse_bias = adv_eval[adv]['bias']
    rmse_uimp = adv_eval[adv]['uimp']
    rmse_kimp = adv_eval[adv]['kimp']
    rmse_bid = adv_eval[adv]['bid']

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.17

    opacity = 0.4
    rects1 = plt.bar(index + bar_width, rmse_bias, bar_width, alpha=opacity, color='r', label='BIAS')
    rects2 = plt.bar(index + bar_width * 2, rmse_uimp, bar_width, alpha=opacity, color='g', label='UOMP')
    rects3 = plt.bar(index + bar_width * 3, rmse_kimp, bar_width, alpha=opacity, color='b', label='KMMP')
    rects4 = plt.bar(index + bar_width * 4, rmse_bid, bar_width, alpha=opacity, color='k', label='FULL')

    plt.xlabel('TEST SET')
    plt.ylabel('RMSE')
    plt.title('iPinYou campaign ' + adv)
    plt.xticks(index + bar_width * 3, ('Winning Data', 'Losing Data', 'Full'))

    lower_bound = min(min(rmse_bias), min(rmse_uimp), min(rmse_kimp), min(rmse_bid)) * 0.25
    upper_bound = max(max(rmse_bias), max(rmse_uimp), max(rmse_kimp), max(rmse_bid)) * 1.5
    plt.ylim(lower_bound, upper_bound)
    plt.legend()

    plt.tight_layout()
    # plt.show()
    plt.savefig('../results/evaluation/' + adv + '_rmse.png', dpi=300)
    plt.close()
