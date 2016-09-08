
import random
from sklearn.metrics import mean_squared_error
import math
import numpy


def load_weights(weight_file):
    featWeight = {}
    fi = open(weight_file, 'r')
    for line in fi:
        s = line.split()
        feat = float(s[0])
        weight = float(s[1])
        featWeight[feat] = weight
    fi.close()
    return featWeight


def normal_distribution(x, mu, sigma):
    # print x, math.pow(x,2), - math.pow(x, 2), - math.pow(x, 2) / 2
    # print math.exp(- math.pow(x, 2) / 2), math.sqrt(2 * math.pi)
    return math.exp(-((x - mu) ** 2) / (2 * (sigma ** 2))) / (math.sqrt(2 * math.pi) * sigma)
    # return stats.norm.pdf(x, 0, 1)


def ints(s):
    res = []
    for ss in s:
        res.append(int(ss))
    return res


def get_sigma(train_yzx):
    train_z = []
    fi = open(train_yzx, 'r')
    for line in fi:
        z = ints(line.replace(":1", "").split())[1]
        train_z.append(z)
    fi.close()
    sigma = numpy.std(train_z)
    return sigma


def output_prediction(featWeight, sigma, yzx, zp):
    fi = open(yzx, 'r')
    fo = open(zp, 'w')

    for line in fi:
        data = ints(line.replace(":1", "").split())
        pred = 0.0
        for i in range(2, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat] + normal_distribution(1.0, 0.0, sigma)
        fo.write('%d\t%.6f\n' % (data[1], pred))
    fo.close()
    fi.close()


advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
data_folder = '../data/'
result_folder = '../results/market-price/'

# bias, uimp, kimp, bid
setting = 'bias'

eta = 0.01
lamb = 0.01

for adv in advs:
    print ('running ' + adv)
    if setting == 'bid':
        train_yzx = data_folder + adv + '/train.yzx.imp.txt'
    else:
        train_yzx = data_folder + adv + '/train.yzx.bid.txt'
    train_zp = result_folder + adv + '/train.zp.' + setting + '.txt'

    test_yzx_bid = data_folder + adv + '/test.yzx.bid.txt'
    test_zp_bid = result_folder + adv + '/test.zp.bid.' + setting + '.txt'

    test_yzx_win = data_folder + adv + '/test.yzx.win.txt'
    test_zp_win = result_folder + adv + '/test.zp.win.' + setting + '.txt'

    test_yzx_lose = data_folder + adv + '/test.yzx.lose.txt'
    test_zp_lose = result_folder + adv + '/test.zp.lose.' + setting + '.txt'

    weight_file = result_folder + adv + '/log/weights.new.' + setting + '.' + str(eta) + '.' + str(lamb) + '.txt'
    featWeight = load_weights(weight_file)
    sigma = get_sigma(train_yzx)

    output_prediction(featWeight, sigma, train_yzx, train_zp)
    output_prediction(featWeight, sigma, test_yzx_bid, test_zp_bid)
    output_prediction(featWeight, sigma, test_yzx_win, test_zp_win)
    output_prediction(featWeight, sigma, test_yzx_lose, test_zp_lose)
