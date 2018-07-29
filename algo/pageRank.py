from __future__ import division
import numpy as np
from decimal import Decimal

debug=False

def pageRank(M, stop=None):
    N = M.shape[0]
    if debug: print N

    r = [Decimal(1/N) for x in range(N)]
    e = [1 for x in range(N)]
    if debug: print (r)
    if debug: print M

    if stop: counter = 0

    while not checkEpsilon(e):
        if stop:
            if counter == stop: break
        r1 = np.dot(r, M.T)
        if debug: print str(x) + ": " + str(r1)
        if debug: print "e: " + str(np.subtract(r1, r))
        e = np.subtract(r1, r)
        r = r1

        if stop: counter += 1

    return r

def checkEpsilon(e):
    for x in e:
        if x != 0: return False

    return True
