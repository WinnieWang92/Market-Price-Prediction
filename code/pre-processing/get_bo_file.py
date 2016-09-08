"""
to get a file in the following format:

bid price, [winning indicators]

in the increasing order
"""
import operator

import collections

advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
data_folder = '../data/'


for adv in advs:
    print 'running ' + adv
    train_wzb_imp = data_folder + adv + '/train.wzb.imp.txt'
    train_wzb_lose = data_folder + adv + '/train.wzb.lose.txt'
    bid_indicators = data_folder + adv + '/train.bo.txt'

    fi1 = open(train_wzb_imp, 'r')  # winning file
    fi2 = open(train_wzb_lose, 'r')  # losing file
    fo = open(bid_indicators, 'w')

    bo_dict = {}
    for line in fi1:
        s = line.strip().split()
        price = int(s[1])  # z
        indicator = int(s[0])
        if price in bo_dict:
            bo_dict[price].append(indicator)
        else:
            indicators = [indicator]
            bo_dict[price] = indicators
    fi1.close()

    for line in fi2:
        s = line.strip().split()
        price = int(s[2])  # b
        indicator = int(s[0])
        if price in bo_dict:
            bo_dict[price].append(indicator)
        else:
            indicators = [indicator]
            bo_dict[price] = indicators
    fi2.close()

    # sorted_bo_dict = sorted(bo_dict.items(), key=operator.itemgetter(0))
    sorted_bo_dict = collections.OrderedDict(sorted(bo_dict.items()))
    for key in sorted_bo_dict:
        # print key, sorted_bo_dict[key]
        ln = str(key)
        for o in sorted_bo_dict[key]:
            ln += '\t' + str(o)
        fo.write(ln + '\n')
    fo.close()