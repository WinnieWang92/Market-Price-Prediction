#!/usr/bin/python
import sys
from collections import defaultdict

def win_prob(bid):
    if bid in zw_dict:
        return zw_dict[bid]
    last_key = -1
    for key in zw_dict:
        if last_key == -1:
            last_key = key
        if bid <= key:
            return zw_dict[last_key]
        else:
            last_key = key
    return 1.

advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
data_folder = '../data/'


for adv in advs:
    print 'running ' + adv
    train_bo = data_folder + adv + '/train.bo.txt'
    train_wzb_imp = data_folder + adv + '/train.wzb.imp.txt'
    train_wyzx_uimp = data_folder + adv + '/train.wyzx.uimp.txt'
    train_wyzx_uimp_km = data_folder + adv + '/train.wyzx.uimp.km.txt'

    # build zb dictionary
    bo_dict = defaultdict(list)
    # add smooth data
    upper = 301
    for i in range(0, upper):
        bo_dict[i].append(1)

    fi = open(train_bo, 'r')
    size = upper
    for line in fi:
        s = line.strip().split()
        #b = int(s[0])  # boolean value
        b = int(s[0])  # bid price
        for i in range(1, len(s)):
            o = int(s[i])   # indicator
            bo_dict[b].append(o)
            size += 1
    fi.close()

    size0 = size - 1

    # build bdn list
    bdns = []
    wins = 0
    for z in bo_dict:
        wins = sum(bo_dict[z])  # times of winning
        b = z   # bid price bj
        d = wins    # wins with bid price bj
        n = size0   # loses with bid price bj-1
        bdn = [b, d, n]
        bdns.append(bdn)

        size0 -= len(bo_dict[z])  # len


    # build new winning probability
    zw_dict = {}
    min_p_w = 0
    bdns_length = len(bdns)
    count = 0
    p_l_tmp = (size - 1.0) / size
    for bdn in bdns:
        count += 1
        b = float(bdn[0])
        d = float(bdn[1])
        n = float(bdn[2])
        p_l = p_l_tmp   # losing probability with bid price b
        p_w = max(1.0 - p_l, min_p_w)   # winning probability with bid price b
        zw_dict[int(b)] = p_w
        if count < bdns_length:
            p_l_tmp = (n - d) / n * p_l_tmp


    # read train.wyzx.imp to build train.wyzx.uimp.km
    fi1 = open(train_wyzx_uimp, 'r')  # train.wyzx.uimp
    fi2 = open(train_wzb_imp, 'r')    #train.wzb.imp
    fo = open(train_wyzx_uimp_km, 'w')  # train.wyzx.uimp.km
    for line1 in fi1:
        line2 = fi2.readline()
        s1 = line1.strip().split()
        s2 = line2.strip().split()
        bid = int(s2[2])
        s1[0] = str(win_prob(bid))
        fo.write('\t'.join(s1) + '\n')
    fi1.close()
    fi2.close()
    fo.close()
    print 'Finished creating file:', (train_wyzx_uimp_km.split('/'))[-1]
    print '-------------------'

    # output win prob
    win_prob_file = '../results/win-prob/{}.kimp.winprob.txt'.format(adv)
    print 'output win prob to ' + win_prob_file
    fof = open(win_prob_file, 'w')
    for bid in range(302):
        fof.write('%d\t%.8f\n' % (bid, win_prob(bid)))
    fof.close()
