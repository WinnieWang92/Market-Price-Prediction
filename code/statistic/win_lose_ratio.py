
def get_line_num(file):
    fi = open(file, 'r')
    line_num = 0
    for line in fi:
        line_num += 1
    fi.close()
    return line_num



advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
data_folder = '../data/'
result_folder = '../results/evaluation/'

win_lose_ratio = result_folder + 'win.lose.ratio.csv'
fo = open(win_lose_ratio, 'w')
head = 'Campaign, , ,Train, , , ,Test, ' + '\n'
fo.write(head)
head2= ' ,Win Volume,Lose Volume,Full Volume,Win:Lose,Win Volume,Lose Volume,Full Volume,Win:Lose' + '\n'
fo.write(head2)
for adv in advs:
    train_win_file = data_folder + adv + '/train.wzb.imp.txt'
    train_lose_file = data_folder + adv + '/train.wzb.lose.txt'
    test_win_file = data_folder + adv + '/test.yzx.win.txt'
    test_lose_file = data_folder + adv + '/test.yzx.lose.txt'

    train_win = get_line_num(train_win_file)
    train_lose = get_line_num(train_lose_file)
    train_all = train_win + train_lose
    train_ratio = float(train_win) / float(train_lose)

    test_win = get_line_num(test_win_file)
    test_lose = get_line_num(test_lose_file)
    test_all = test_win + test_lose
    test_ratio = float(test_win) / float(test_lose)

    nl = str(adv) + ',' + str(train_win) + ',' + str(train_lose) + ',' + str(train_all) + ',' + str(train_ratio) \
         + ',' + str(test_win) + ',' + str(test_lose) + ',' + str(test_all) + ',' + str(test_ratio) + '\n'
    fo.write(nl)
fo.close()