import numpy as np


def qubo_to_ising(q):
    """Convert a QUBO matrix `q` to Ising parameters (h, couplings, offset)."""
    n = len(q)
    h = np.zeros(n)
    couplings = {}
    offset = 0.0

    for i in range(n):
        h[i] += q[i][i] / 2
        offset += q[i][i] / 2

        for j in range(i + 1, n):
            if q[i][j] != 0:
                couplings[(i, j)] = q[i][j] / 4
                h[i] += q[i][j] / 4
                h[j] += q[i][j] / 4
                offset += q[i][j] / 4

    return h, couplings, offset