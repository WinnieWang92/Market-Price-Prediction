
# cumulative winning prob
# laplace smoothing
def get_bid_landscape(mps):
    upper = 301
    init_val = 1
    mp_num = 0  # market price num
    mp_dict = {}
    for i in range(0, upper):
        mp_dict[i] = init_val
        mp_num += init_val
    winfun = {}
    for mp in mps:
        if mp in mp_dict:
            mp_dict[mp] += 1
            mp_num += 1
        else:
            mp_dict[mp] = init_val
            mp_num += init_val
    # mp_num_tmp = max (mp_dict.keys()[0] - 1, 1)
    mp_num_tmp = 1
    # for key in mp_dict.keys():
    for key in range(0, upper):
        w = (mp_num_tmp * 1.0) / (mp_num * 1.0)
        mp_num_tmp += mp_dict[key]
        winfun[key] = w
    return winfun


def win_prob(bid):
    if bid in winfun:
        return winfun[bid]
    for key in sorted(winfun):
        if bid <= key:
            return winfun[key]
    return 1.



advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
data_folder = '../data/'


for adv in advs:
    print 'running ' + adv
    train_yzx_imp = data_folder + adv + '/train.yzx.imp.txt'
    train_wzb_imp = data_folder + adv + '/train.wzb.imp.txt'
    train_wyzx_uimp = data_folder + adv + '/train.wyzx.uimp.txt'

    mps = []
    winfun = {}
    fi = open(train_yzx_imp, 'r')
    for line in fi:
        s = line.strip().split()
        # print s
        cost = int(s[1])  # z
        mps.append(cost)
    fi.close()
    winfun = get_bid_landscape(mps)

    # output win prob
    win_prob_file = '../results/win-prob/{}.uimp.winprob.txt'.format(adv)
    print 'output win prob to ' + win_prob_file
    fof = open(win_prob_file, 'w')
    for bid in range(302):
        fof.write('%d\t%.8f\n' % (bid, win_prob(bid)))
    fof.close()

    # read in train.wyzx.imp for to calculate w
    fi1 = open(train_yzx_imp, 'r')
    fi2 = open(train_wzb_imp, 'r')
    fo = open(train_wyzx_uimp, 'w')
    for line1 in fi1:
        line2 = fi2.readline()
        s1 = line1.strip().split()
        s2 = line2.strip().split()
        bid = int(s2[2])
        w = win_prob(bid)
        nl = '\t'.join([str(w)] + s1[0:])
        fo.write(nl + '\n')
    fi1.close()
    fi2.close()
    fo.close()
