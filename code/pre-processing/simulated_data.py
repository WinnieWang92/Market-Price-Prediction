#!/usr/bin/python
import random
import math
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error

bufferCaseNum = 1000000
eta = 0.01  # learning rate
lamb = 1E-6
featWeight = {}  # weights of feature
trainRounds = 10
random.seed(10)
initWeight = 0.05

def nextInitWeight():
    return (random.random() - 0.5) * initWeight

def ints(s):
    res = []
    for ss in s:
        res.append(int(ss))
    return res

def sigmoid(p):
    return 1.0 / (1.0 + math.exp(-p))



def test(path):
    y = []  # list of true clk
    yp = [] # list of predicted clk
    fi = open(path, 'r')
    for line in fi:
        data = ints(line.replace(":1", "").split())
        clk = data[0]
        mp = data[1]
        fsid = 2  # feature start id
        pred = 0.0
        for i in range(fsid, len(data)):
            feat = data[i] #feature
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        y.append(clk)
        yp.append(pred)
    fi.close()
    auc = roc_auc_score(y, yp)
    rmse = math.sqrt(mean_squared_error(y, yp))
    print str(round) + '\t' + str(auc) + '\t' + str(rmse)

advss = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476']
# advss = ['all']
data_folder = '../data/'
for aadv in advss:
    print 'running ' + aadv
    train_yzx_bid = data_folder + aadv + '/train.yzx.bid.txt'
    train_yzx_imp = data_folder + aadv + '/train.yzx.imp.txt'
    train_wzb_imp = data_folder + aadv + '/train.wzb.imp.txt'
    train_wzb_lose = data_folder + aadv + '/train.wzb.lose.txt'
    # train_wyzx_uimp = data_folder + aadv + '/train.wyzx.uimp.txt'
    
    
    original_ecpc = 0.  # original eCPC from train.yzx.base.txt
    total_cost_train = 0    # total original cost during the train data
    
    # read in train.yzx.base for original_ecpc
    fi = open(train_yzx_bid, 'r')
    first = True
    imp_num = 0
    clk_num = 0
    for line in fi:
        s = line.strip().split()
        click = int(s[0])  # y
        cost = int(s[1])  # z
        imp_num += 1
        clk_num += click
        total_cost_train += cost
    fi.close()
    original_ecpc = total_cost_train * 1.0 / clk_num
    print 'Finish loading train.yzx.bid.txt'

    for round in range(0, trainRounds):
        # train for this round
        print 'Round:', round
        fi = open(train_yzx_bid, 'r')
        lineNum = 0
        trainData = []
        for line in fi:
            lineNum = (lineNum + 1) % bufferCaseNum
            trainData.append(ints(line.replace(":1", "").split()))
            if lineNum == 0:
                for data in trainData:
                    clk = data[0]
                    # mp = data[1]
                    fsid = 2  # feature start id
                    # predict
                    pred = 0.0
                    for i in range(fsid, len(data)):
                        feat = data[i]
                        if feat not in featWeight:
                            featWeight[feat] = nextInitWeight()
                        pred += featWeight[feat]
                    pred = sigmoid(pred)
                    # start to update weight
                    # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ]
                    for i in range(fsid, len(data)):
                        feat = data[i]
                        featWeight[feat] = featWeight[feat] * (1 - lamb) + eta * (clk - pred)
                trainData = []

        if len(trainData) > 0:
            for data in trainData:
                clk = data[0]
                # mp = data[1]
                fsid = 2  # feature start id
                # predict
                pred = 0.0
                for i in range(fsid, len(data)):
                    feat = data[i]
                    if feat not in featWeight:
                        featWeight[feat] = nextInitWeight()
                    pred += featWeight[feat]
                pred = sigmoid(pred)
                # start to update weight
                # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ]
                for i in range(fsid, len(data)):
                    feat = data[i]
                    featWeight[feat] = featWeight[feat] * (1 - lamb) + eta * (clk - pred)
        fi.close()

        # test for this round
        # test()

    #adv_bid_discount = {'1458':4, '2259':2, '2261':3, '2821':4, '2997':4, '3358':4, '3386':4, '3427':4, '3476':4, 'all':4}
    adv_bid_discount = {'1458':4, '2259':4, '2261':4, '2821':4, '2997':4, '3358':4, '3386':4, '3427':4, '3476':4, 'all':4}
    discount = 4
    for adv in adv_bid_discount:
        if adv in train_yzx_bid:
            discount = adv_bid_discount[adv]
    
    win_num = 0
    bid_num = 0
    bid_max = 300
    fi = open(train_yzx_bid, 'r')
    fo1 = open(train_yzx_imp, 'w')
    fo2 = open(train_wzb_imp, 'w')
    fo3 = open(train_wzb_lose, 'w')
    print 'Begin to bid'
    for line in fi:
        data = ints(line.replace(":1", "").split())
        pred = 0.0
        mp = int(data[1])  # market price
        for i in range(2, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        # simulate bid
        bid = int(min(original_ecpc * pred / discount, bid_max))
        bid_num += 1
        if bid > mp:
            win_num += 1
            fo1.write(line)
            #w = win_prob(bid)
            # s = line.strip().split()
            nl = '\t'.join(["1"] + [str(mp)] + [str(bid)])
            fo2.write(nl + '\n')
    
        else:
            nl = '\t'.join(["0"] + [str(mp)] + [str(bid)])
            fo3.write(nl + '\n')
    print 'Win ration:', float(win_num) / float(bid_num)
    fo1.close()
    fo2.close()
    fo3.close()
    fi.close()
