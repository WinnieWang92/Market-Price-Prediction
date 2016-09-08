import math
from sklearn.metrics import mean_squared_error


def load_z_zp(file):
    z = []
    zp = []
    fi = open(file, 'r')
    for line in fi:
        data = line.split()
        mp = float(data[0])
        pred = float(data[1])
        z.append(mp)
        zp.append(pred)
    fi.close()
    return [z, zp]


def eval(file):
    z = load_z_zp(file)[0]
    zp = load_z_zp(file)[1]
    return math.sqrt(mean_squared_error(z, zp))


advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
settings = ['bias', 'uimp', 'kimp', 'bid']
result_folder = '../results/market-price/'

for setting in settings:
    print 'for ' + setting
    eval_file = '../results/evaluation/rmse.eval.' + setting + '.txt'
    fo = open(eval_file, 'w')
    fo.write('adv' + '\t' + 'rmse_win' + '\t' + 'rmse_lose' + '\t' + 'rmse_all' + '\n')
    for adv in advs:
        test_zp_bid = result_folder + adv + '/test.zp.bid.' + setting + '.txt'
        test_zp_win = result_folder + adv + '/test.zp.win.' + setting + '.txt'
        test_zp_lose = result_folder + adv + '/test.zp.lose.' + setting + '.txt'

        rmse_win = eval(test_zp_win)
        rmse_lose = eval(test_zp_lose)
        rmse_all = eval(test_zp_bid)
        line = adv + '\t' + str(rmse_win) + '\t' + str(rmse_lose) + '\t' + str(rmse_all) + '\n'
        fo.write(line)
        print ('Adv: ' + adv + '\t' + 'rmse_win: ' + str(rmse_win) + '\t' + 'rmse_lose: ' + str(rmse_lose) + '\t' + 'rmse_all: ' + str(rmse_all))
    fo.close()
