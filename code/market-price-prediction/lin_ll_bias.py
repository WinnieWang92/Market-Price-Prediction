#!/usr/bin/python
import random

from scipy import stats
from sklearn.metrics import mean_squared_error
import math
import numpy
import theano.tensor as T
initWeight = 0.05


def nextInitWeight():
    return (random.random() - 0.5) * initWeight


def ints(s):
    res = []
    for ss in s:
        res.append(int(ss))
    return res


def normal_distribution(x, mu, sigma):
    # print x, math.pow(x,2), - math.pow(x, 2), - math.pow(x, 2) / 2
    # print math.exp(- math.pow(x, 2) / 2), math.sqrt(2 * math.pi)
    return math.exp(-((x - mu) ** 2) / (2 * (sigma ** 2))) / (math.sqrt(2 * math.pi) * sigma)
    # return stats.norm.pdf(x, 0, 1)


def negative_log_likelihood(z, zp, sigma):
    likelihood = 0.
    for i in range(len(z)):
        x = (z[i] - zp[i]) / sigma
        nd = normal_distribution(x, 0, 1)
        # nd = stats.norm.pdf(x, 0, 1)
        if nd != 0:
            likelihood -= math.log(nd)
    return likelihood


def loss(z, zp, featWeight, sigma):
    nll = negative_log_likelihood(z, zp, sigma)
    param_sqr = []
    for key in featWeight:
        param_sqr.append(float(featWeight[key]) ** 2)
    l2 = math.sqrt(sum(param_sqr))
    return nll + l2


def train(train_yzx, test_yzx, log_file):
    print ('For ' + train_yzx.split('/')[-1])
    bufferCaseNum = 1000000
    # bufferCaseNum = 10
    featWeight = {}
    trainRounds = 30
    random.seed(10)

    train_z = []
    fi = open(train_yzx, 'r')
    for line in fi:
        z = ints(line.replace(":1", "").split())[1]
        train_z.append(z)
    fi.close()
    sigma = numpy.std(train_z)

    fo_log = open(log_file, 'w')
    train_ll = 0.
    for round in range(0, trainRounds):
        # train for this round
        train_pred = []

        fi = open(train_yzx, 'r')  # train.yzx
        lineNum = 0
        trainData = []
        for line in fi:
            lineNum = (lineNum + 1) % bufferCaseNum
            trainData.append(ints(line.replace(":1", "").split()))
            if lineNum == 0:
                for data in trainData:
                    mp = data[1]
                    fsid = 2 # feature start id
                    # predict
                    pred = 0.0
                    for i in range(fsid, len(data)):
                        feat = data[i]
                        if feat not in featWeight:
                            featWeight[feat] = nextInitWeight()
                        # pred += featWeight[feat]
                        # pred += featWeight[feat] + stats.norm.pdf(1.0, 0.0, sigma)
                        pred += featWeight[feat] + normal_distribution(1.0, 0.0, sigma)
                    train_pred.append(pred)
                    # start to update weight
                    # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ]
                    for i in range(fsid, len(data)):
                        feat = data[i]
                        featWeight[feat] = featWeight[feat] * (1 - eta * lamb) + eta * (mp - pred)
                trainData = []

        if len(trainData) > 0:
            for data in trainData:
                mp = data[1]
                fsid = 2 # feature start id
                # predict
                pred = 0.0
                for i in range(fsid, len(data)):
                    feat = data[i]
                    if feat not in featWeight:
                        featWeight[feat] = nextInitWeight()
                    # pred += featWeight[feat]
                    # pred += featWeight[feat] + stats.norm.pdf(1.0, 0.0, sigma)
                    pred += featWeight[feat] + normal_distribution(1.0, 0.0, sigma)
                train_pred.append(pred)
                # start to update weight
                # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ]
                for i in range(fsid, len(data)):
                    feat = data[i]
                    featWeight[feat] = featWeight[feat] * (1 - eta * lamb) + eta * (mp - pred)
        fi.close()


        # test for this round
        z = []
        zp = []
        fi = open(test_yzx, 'r')
        for line in fi:
            data = ints(line.replace(":1", "").split())
            mp = data[1]
            fsid = 2 # feature start id
            pred = 0.0
            for i in range(fsid, len(data)):
                feat = data[i]
                if feat in featWeight:
                    # pred += featWeight[feat]
                    # pred += featWeight[feat] + stats.norm.pdf(1.0, 0.0, sigma)
                    pred += featWeight[feat] + normal_distribution(1.0, 0.0, sigma)
            z.append(mp)
            zp.append(pred)
        fi.close()
        sigma_test = numpy.std(z)
        # test_ll = mean_squared_error(z, zp)
        # new_train_ll = mean_squared_error(train_z, train_pred)
        test_ll = loss(z, zp, featWeight, sigma_test)
        new_train_ll = loss(train_z, train_pred, featWeight, sigma)
        if 0 < (train_ll - new_train_ll) / new_train_ll < 0.000005:
            train_ll = new_train_ll
            # rmse = math.sqrt(mean_squared_error(z, zp))
            res = str(round) + '\t' + str(train_ll) + '\t' + str(test_ll)
            fo_log.write(res + '\n')
            print ('Round: ' + str(round) + '\t' + 'Train: ' + str(train_ll) + '\t' + 'Test: ' + str(test_ll))
            break
        train_ll = new_train_ll
        # rmse = math.sqrt(mean_squared_error(z, zp))
        res = str(round) + '\t' + str(train_ll) + '\t' + str(test_ll)
        fo_log.write(res + '\n')
        print ('Round: ' + str(round) + '\t' + 'Train: ' + str(train_ll) + '\t' + 'Test: ' + str(test_ll))
    fo_log.close()
    return featWeight


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

eta = 0.001
lamb = 100
setting = 'bid'  # bias, bid
print ('eta = ' + str(eta) + '\t' + 'lambda = ' + str(lamb))
ll_file = result_folder + 'll.new.' + setting + '.' + str(eta) + '.' + str(lamb) + '.txt'
fo = open(ll_file, 'w')
for adv in advs:
    print 'for ' + setting
    print ('running ' + adv)

    if setting == 'bias':
        train_yzx = data_folder + adv + '/train.yzx.imp.txt'
    if setting == 'bid':
        train_yzx = data_folder + adv + '/train.yzx.bid.txt'
    train_zp = result_folder + adv + '/train.zp.' + setting + '.txt'

    test_yzx_bid = data_folder + adv + '/test.yzx.bid.txt'
    test_zp_bid = result_folder + adv + '/test.zp.bid.' + setting + '.txt'

    test_yzx_win = data_folder + adv + '/test.yzx.win.txt'
    test_zp_win = result_folder + adv + '/test.zp.win.' + setting + '.txt'

    test_yzx_lose = data_folder + adv + '/test.yzx.lose.txt'
    test_zp_lose = result_folder + adv + '/test.zp.lose.' + setting + '.txt'

    log_file = result_folder + adv + '/log/log.new.' + setting + '.' + str(eta) + '.' + str(lamb) + '.txt'
    weight_file = result_folder + adv + '/log/weights.new.' + setting + '.' + str(eta) + '.' + str(lamb) + '.txt'

    featWeight = train(train_yzx, test_yzx_bid, log_file)

    fo_weight = open(weight_file, 'w')
    for key in featWeight:
        fo_weight.write(str(key) + '\t' + str(featWeight[key]) + '\n')
    fo_weight.close()

    sigma = get_sigma(train_yzx)

    output_prediction(featWeight, sigma, train_yzx, train_zp)
    output_prediction(featWeight, sigma, test_yzx_bid, test_zp_bid)
    output_prediction(featWeight, sigma, test_yzx_win, test_zp_win)
    output_prediction(featWeight, sigma, test_yzx_lose, test_zp_lose)

    best_ll_on_test = 10 ** 1000
    best_train = 0.
    best_rnd = 0
    fi = open(log_file, 'r')
    for line in fi:
        s = line.split()
        rnd = int(s[0])
        train_ll = float(s[1])
        test_ll = float(s[2])
        if test_ll < best_ll_on_test:
            best_ll_on_test = test_ll
            best_train = train_ll
            best_rnd = rnd
    fi.close()
    fo.write(str(adv) + '\t' + str(best_rnd) + '\t' + str(best_train) + '\t' + str(best_ll_on_test) + '\n')
fo.close()



