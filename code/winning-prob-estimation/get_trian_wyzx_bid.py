
def ints(s):
    res = []
    for ss in s:
        res.append(float(ss))
    return res


def combine(yzx, zw, wyzx):
    fi1 = open(yzx, 'r')
    fi2 = open(zw, 'r')
    fof = open(wyzx, 'w')

    zw_dict = {}
    for line in fi2:
        s = line.strip().split()
        z = int(s[0])
        w = float(s[1])
        zw_dict[z] = w
    fi2.close()

    for line in fi1:
        data = ints(line.replace(":1", "").split())
        z = int(data[1])
        w = zw_dict[z]
        o_line = '\t'.join([str(w)] + [line])
        fof.write(o_line)
    fi1.close()
    fof.close()


advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
for adv in advs:
    print adv

    input_full_file = '../data/{}/train.yzx.bid.txt'.format(adv)
    win_prob_file = '../results/win-prob/{}.bid.winprob.txt'.format(adv)
    output_wyzx_file = '../data/{}/train.wyzx.bid.txt'.format(adv)

    combine(input_full_file, win_prob_file, output_wyzx_file)