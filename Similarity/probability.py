import matplotlib.pyplot as plt
import scipy.stats as stats

from setup import POLARITY_SCALE

# Value to be added to divisors to avoid division by zero. 
INFINITESIMAL = 1e-64

DISTRIBUTIONS_LENGTH = POLARITY_SCALE * 3
DISTRIBUTIONS_STEP = POLARITY_SCALE / 10


def normalDistribution(mean, std, prob, step=DISTRIBUTIONS_STEP, leftlimit=-DISTRIBUTIONS_LENGTH / 2,
                       rightlimit=DISTRIBUTIONS_LENGTH / 2):
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


def KLdivergence(d1, d2):  # d1 and d2 are dicts containing a normal distribution

    d1 = list(d1.values())
    d2 = list(d2.values())
    r = stats.entropy(d1, d2)
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
