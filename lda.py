import sys
import random

t_c = {}
tw_c = {}
td_c = {}

d_w = {}
d_w_t = {}
w_S = set()

ITER_NUM = 10000
TOPIC_NUM = 2
ALPHA = 0.01
BETA = 0.01

p_k = [0] * TOPIC_NUM
print p_k

def input():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        items = line.strip().split('\t')
        doc = items[0]
        word_L = items[1:]
        for word in word_L:
            d_w.setdefault(doc, list())
            d_w[doc].append(word)
            w_S.add(word)

def init():
    for d, w_L in d_w.items():
        for w in w_L:
            for t in range(TOPIC_NUM):
                t_c.setdefault(t, 0)
                tw_c.setdefault(t, dict())
                tw_c[t].setdefault(w, 0)
                td_c.setdefault(t, dict())
                td_c[t].setdefault(d, 0)

    for d, w_L in d_w.items():
        for w in w_L:
            r = random.random()
            if r < 0.5:
                t = 0
            else:
                t = 1
            
            d_w_t.setdefault(d, dict())
            d_w_t[d].setdefault(w, t)
            
            t_c[t] += 1
            tw_c[t][w] += 1
            td_c[t][d] += 1

            print d_w_t[d][w]

def sampling():
    for iter in range(ITER_NUM):
        print "iters is %d" % iter
        for d, w_L in d_w.items():
            for w in w_L:
                t = d_w_t[d][w]
                t_c[t] -= 1
                tw_c[t][w] -= 1
                td_c[t][d] -= 1

                for k in range(TOPIC_NUM):
                    p_k[k] = (tw_c[k][w] + BETA) * (td_c[k][d] + ALPHA) * 1.0 / (t_c[k] + BETA*len(w_S))
                sum = 0
                for k in range(TOPIC_NUM):
                    sum += p_k[k]
                for k in range(TOPIC_NUM):
                    p_k[k] /= sum
                for k in range(1, TOPIC_NUM):
                    p_k[k] += p_k[k-1]
                r = random.random()
                for k in range(TOPIC_NUM):
                    if(r<=p_k[k]):
                        t = k
                        break
                d_w_t[d][w] = t
                t_c[t] += 1
                tw_c[t][w] += 1
                td_c[t][d] += 1

def output():
    for d, w_L in d_w.items():
        for w in w_L:
            print "%s\t%s\t%d" % (d, w, d_w_t[d][w])

if __name__ == "__main__":
    input()
    print "input end..."
    init()
    print "init end..."
    sampling()
    print "samplint end..."
    output()
    print "output end..."
