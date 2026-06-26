from protein.lattice3d import random_fold
from protein.energy3d import energy

def solve(protein, it=2000):
    best=1e9
    best_fold=None

    for _ in range(it):
        f=random_fold(protein.length)
        e=energy(protein,f)
        if e<best:
            best=e
            best_fold=f

    return best_fold,best