

advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476']
# input_folder = '../../make-ipinyou-data/'
data_folder = '../data/'

train_yzx_bid_all = data_folder + 'all/train.yzx.bid.txt'
train_yzx_imp_all = data_folder + 'all/train.yzx.imp.txt'
train_wzb_imp_all = data_folder + 'all/train.wzb.imp.txt'
train_wzb_lose_all = data_folder + 'all/train.wzb.lose.txt'
test_yzx_bid_all = data_folder + 'all/test.yzx.bid.txt'

fo1 = open(train_yzx_bid_all, 'w')
fo2 = open(train_yzx_imp_all, 'w')
fo3 = open(train_wzb_imp_all, 'w')
fo4 = open(train_wzb_lose_all, 'w')
fo5 = open(test_yzx_bid_all, 'w')

for adv in advs:
    train_yzx_bid = data_folder + adv + '/train.yzx.bid.txt'
    train_yzx_imp = data_folder + adv + '/train.yzx.imp.txt'
    train_wzb_imp = data_folder + adv + '/train.wzb.imp.txt'
    train_wzb_lose = data_folder + adv + '/train.wzb.lose.txt'
    test_yzx_bid = data_folder + adv + '/test.yzx.bid.txt'

    fi1 = open(train_yzx_bid, 'r')
    fi2 = open(train_yzx_imp, 'r')
    fi3 = open(train_wzb_imp, 'r')
    fi4 = open(train_wzb_lose, 'r')
    fi5 = open(test_yzx_bid, 'r')

    for line in fi1:
        fo1.write(line)
    fi1.close()

    for line in fi2:
        fo2.write(line)
    fi2.close()

    for line in fi3:
        fo3.write(line)
    fi3.close()

    for line in fi4:
        fo4.write(line)
    fi4.close()

    for line in fi5:
        fo5.write(line)
    fi5.close()

fo1.close()
fo2.close()
fo3.close()
fo4.close()
fo5.close()

