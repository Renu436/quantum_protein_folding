import numpy as np


def build_qubo(sequence, a=2, b=5):
    """Build a symmetric QUBO matrix for an HP sequence.

    Parameters are lower-case to satisfy lint rules.
    """
    n = len(sequence)
    Q = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 2, n):
            if sequence[i] == 'H' and sequence[j] == 'H':
                Q[i][j] -= a

    for i in range(n):
        Q[i][i] += b

    return Q