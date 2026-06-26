import random, math
from protein.lattice3d import generate_fold
from protein.energy3d import compute_energy


def run_sa(sequence, iterations=300, temp=8):
    current = generate_fold(sequence)
    curr_e = compute_energy(sequence, current)

    best = current
    best_e = curr_e

    curve = []

    for _ in range(iterations):
        new = generate_fold(sequence)
        new_e = compute_energy(sequence, new)

        if new_e < curr_e:
            current, curr_e = new, new_e
        else:
            prob = math.exp((curr_e - new_e) / temp)
            if random.random() < prob:
                current, curr_e = new, new_e

        if curr_e < best_e:
            best, best_e = current, curr_e

        temp *= 0.995
        curve.append(curr_e)

    return best, best_e, curve