# Raphael Rocha da Silva
# 2018/02/04 

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from pprint import pprint

from setup import MAXPOLARITY

# Value to be added to divisors to avoid division by zero. 
INFINITESIMAL = 1e-64

DISTRIBUTIONS_LENGTH = MAXPOLARITY * 3
DISTRIBUTIONS_STEP = MAXPOLARITY / 50


def normalDistribution(mean, std, prob, step=DISTRIBUTIONS_STEP, leftlimit=-DISTRIBUTIONS_LENGTH / 2,
                       rightlimit=DISTRIBUTIONS_LENGTH / 2):
    # Returns a dict {(x->y)} where y is the probability density of the value x according to normal distribution

    std += INFINITESIMAL

    normalContinuous = stats.norm(mean, std)

    r = {}
    discreteContinuousRange = []

    left = int(leftlimit / step)
    right = int(rightlimit / step)

    # Discretize
    for i in [j * step for j in range(left, right)]:
        r[i] = normalContinuous.pdf(
            i) + INFINITESIMAL  # Soma para evitar divisão por zero no KL (ele retornava inf em alguns casos)

    # Normalize so the distribution adds to 1 (rounding errors during discretization may have caused the sum to be different than 1)
    s = sum(r.values())
    for i in r:
        r[i] = r[i] / s

        # Weight the distribution by the respective probability
    for i in r:
        r[i] = r[i] * prob

    return r


def normalDistributionZero(step=DISTRIBUTIONS_STEP, leftlimit=-DISTRIBUTIONS_LENGTH / 2,
                           rightlimit=DISTRIBUTIONS_LENGTH / 2):
    left = int(leftlimit / step)
    right = int(rightlimit / step)

    r = {}

    for i in [j * step for j in range(left, right)]:
        r[i] = 0 + INFINITESIMAL
    return r


# def normalizeTwoDistributions (d1, d2):
# greatest = max(d1+d2)
# smallest = min(d1+d2)

# n_d1 = []
# n_d2 = []

# for i in d1:
# n_d1.append((i-smallest)/(greatest-smallest))

# for i in d2:
# n_d2.append((i-smallest)/(greatest-smallest))

# return d1, d2


def KLdivergence(d1, d2):  # d1 and d2 are dicts containing a normal distribution

    # pprint(d1)
    # print()
    # pprint(d2)
    # print()

    # m = max(list(d1.values()) +  list(d2.values()))

    # print(m)
    # input()

    d1 = list(d1.values())
    d2 = list(d2.values())

    # for i in reversed(range(len(d1))):
    # if d1[i] < m/100 and d2[i] < m/100:
    # del d1[i]
    # del d2[i]

    # pprint(d1)
    # pprint(d2)
    # print(len(d1))
    # input()

    r = stats.entropy(d1, d2)
    # r = float("%.3g" % r)
    return r


def integralDivergence(d1, d2):  # não sei se isso existe
    d1 = list(d1.values())
    d2 = list(d2.values())

    diff = 0
    union = 0

    for i in range(len(d1)):
        diff += abs(d1[i] - d2[i])
        union += max(abs(d1[i]), abs(d2[i]))

    return diff / union


import numpy as np
from scipy.linalg import norm
from scipy.spatial.distance import euclidean

_SQRT2 = np.sqrt(2)  # sqrt(2) with default precision np.float64


def hellingerDistance(d1, d2):
    d1 = list(d1.values())
    d2 = list(d2.values())
    return np.sqrt(np.sum((np.sqrt(d1) - np.sqrt(d2)) ** 2)) / _SQRT2


# To visualize the distributions:

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)


def plotDistribution(d, title="", label=""):
    l = sorted(d.items())
    x, y = zip(*l)  # unpack a list of pairs into two tuples
    ax1.plot(x, y, alpha=.7, label=label)
    plt.title(title)
    plt.legend()
    plt.pause(0.1)


def clearChart():
    ax1.cla()

# d_cam_c = normalDistribution(88, 0, 0.25)
##d_cam_c = normalDistribution(60, 80, 0.5)
##pprint(sorted(d_cam_c.values()))
##print(sum(list(d_cam_c.values())))
# d_cam_s = normalDistribution(54, 79, 0.19)

# z = normalDistributionZero()

# plotDistribution(d_cam_s)
# plotDistribution(d_cam_c)

# print(KLdivergence(d_cam_s, d_cam_c))
# print(KLdivergence(d_cam_c, d_cam_s))
# print(hellingerDistance(d_cam_c, d_cam_s))
# print(integralDivergence(d_cam_c, d_cam_s))
# print()
# print(KLdivergence(d_cam_s, z))
# print(KLdivergence(z, d_cam_s))
# print(hellingerDistance(z, d_cam_s))
# print(integralDivergence(z, d_cam_s))
# print()
# input()


# TO TEST:

# n1 = normalDistributionDiscretized (50, 13)
# n2 = normalDistributionDiscretized (40, 26)

# plotDistribution(n1)
# plotDistribution(n2)


# t1 = KLdivergence(n1, n2)
# t2 = KLdivergence(n2, n1)

# print (t1, t2)

# input()


# exit()


# h = [186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
# 187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
# 161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180]

# h = [50,75,20,75]

# h.sort()

# hmean = np.mean(h)

# hstd = np.std(h)

# pdf = stats.norm.pdf(h, hmean, hstd)

# print (pdf)

# normalContinuous = stats.norm(hmean, hstd)

# print (normalContinuous.pdf(5))

# discreteContinuous = []
# discreteContinuousRange = []
# for i in [j * 1 for j in range(-100, 100)]:
# discreteContinuous.append(normalContinuous.pdf(i))
# discreteContinuousRange.append(i)

# plt.plot(h, pdf, alpha=.7) # including h here is crucial
# plt.plot(discreteContinuousRange, discreteContinuous, alpha=.7) # including h here is crucial

# plt.pause(1)

# input()
